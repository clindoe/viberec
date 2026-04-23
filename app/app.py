"""
VibeRec — Streamlit Demo
Run: streamlit run app/app.py  (from project root)
"""

import os
import sys
import warnings
import pickle

import numpy as np
import pandas as pd
import faiss
import torch
import torch.nn as nn
import plotly.express as px
import streamlit as st

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config as cfg

# ── NCF model definition (mirrors Day 21 notebook) ───────────────
class NCFModel(nn.Module):
    def __init__(self, input_dim=256, hidden=None, dropout_1=0.3, dropout_2=0.2):
        super().__init__()
        if hidden is None:
            hidden = [256, 128, 64]
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden[0]), nn.ReLU(), nn.Dropout(dropout_1),
            nn.Linear(hidden[0], hidden[1]), nn.ReLU(), nn.Dropout(dropout_2),
            nn.Linear(hidden[1], hidden[2]), nn.ReLU(),
            nn.Linear(hidden[2], 1), nn.Sigmoid(),
        )

    def forward(self, u, m):
        return self.net(torch.cat([u, m], dim=1))


# ── Core artifacts (needed for movie-based mode) ─────────────────
@st.cache_resource(show_spinner="Loading VibeRec…")
def load_artifacts():
    movie_emb = np.load(cfg.MOVIE_VIBE_EMBEDDINGS).astype("float32")
    with open(cfg.MOVIE_ID_TO_IDX, "rb") as f:
        m2i = pickle.load(f)
    i2m = {v: k for k, v in m2i.items()}

    vecs_n = movie_emb.copy()
    faiss.normalize_L2(vecs_n)

    faiss_movie = faiss.read_index(cfg.FAISS_MOVIE_INDEX)

    with open(cfg.NOVELTY_SCORES, "rb") as f:
        nov_raw = pickle.load(f)
    nov_arr = np.array(
        [nov_raw.get(i2m[i], {}).get("combined", 0.5) for i in range(len(i2m))],
        dtype="float32",
    )

    ncf = NCFModel(
        input_dim=cfg.VIBE_EMBED_DIM * 2,
        hidden=cfg.NCF_HIDDEN,
        dropout_1=cfg.DROPOUT_NCF_1,
        dropout_2=cfg.DROPOUT_NCF_2,
    )
    ncf.load_state_dict(torch.load(cfg.NCF_CKPT, map_location="cpu"))
    ncf.eval()

    umap_meta_path = os.path.join(cfg.EMBEDDINGS_DIR, "umap_movie_meta.pkl")
    with open(umap_meta_path, "rb") as f:
        umap_meta_list = pickle.load(f)
    umap_df = pd.DataFrame(umap_meta_list)

    meta = pd.read_csv(cfg.MOVIES_MASTER)

    return {
        "movie_emb": movie_emb,
        "vecs_n": vecs_n,
        "m2i": m2i,
        "i2m": i2m,
        "faiss_movie": faiss_movie,
        "nov_arr": nov_arr,
        "ncf": ncf,
        "umap_df": umap_df,
        "meta": meta,
    }


# ── User profiles — lazy-loaded only when user-based mode is used ─
@st.cache_resource(show_spinner="Loading user profiles…")
def load_user_artifacts():
    user_emb = np.load(cfg.USER_TASTE_PROFILES).astype("float32")
    with open(cfg.USER_ID_TO_IDX, "rb") as f:
        u2i = pickle.load(f)
    return {"user_emb": user_emb, "u2i": u2i}


# ── Backend functions ─────────────────────────────────────────────

def search_movie(title: str, meta: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Fuzzy title search, ranked by numVotes."""
    mask = meta["title"].str.contains(title, case=False, na=False)
    return (
        meta[mask]
        .sort_values("numVotes", ascending=False)
        [["movieId", "title", "year", "genres", "avgRating"]]
        .head(top_n)
    )


def get_recommendations(
    movie_id: int, alpha: float, arts: dict, top_k: int = 10
) -> pd.DataFrame:
    """
    Item-to-item recommendations.
    score = alpha * vibe_cosine_sim + (1 - alpha) * novelty
    """
    m2i, i2m = arts["m2i"], arts["i2m"]
    if movie_id not in m2i:
        return pd.DataFrame()

    s_idx = m2i[movie_id]
    query = arts["vecs_n"][s_idx : s_idx + 1]
    vibe_sims = (arts["vecs_n"] @ query.T).squeeze(1)
    scores = alpha * vibe_sims + (1.0 - alpha) * arts["nov_arr"]
    scores[s_idx] = -999.0

    top_idxs = np.argpartition(scores, -top_k)[-top_k:]
    top_idxs = top_idxs[np.argsort(scores[top_idxs])[::-1]]

    rows = []
    meta_idx = arts["meta"].set_index("movieId")
    for i in top_idxs:
        mid = i2m[i]
        if mid not in meta_idx.index:
            continue
        r = meta_idx.loc[mid]
        yr = r["year"]
        rows.append(
            {
                "movieId": mid,
                "title": r["title"],
                "year": int(yr) if yr == yr else "?",
                "genres": r["genres"],
                "avgRating": r.get("avgRating", None),
                "vibe_score": round(float(vibe_sims[i]), 4),
                "final_score": round(float(scores[i]), 4),
                "emb_idx": int(i),
            }
        )
    return pd.DataFrame(rows)


def get_user_recommendations(
    user_id: int, alpha: float, arts: dict, user_arts: dict, top_k: int = 10
) -> pd.DataFrame:
    """
    User-personalised recommendations.
    final  = alpha * vibe_sim + (1-alpha) * novelty
    blended = 0.5 * ncf_score + 0.5 * final
    """
    if user_id not in user_arts["u2i"]:
        return pd.DataFrame()

    u_idx = user_arts["u2i"][user_id]
    taste = user_arts["user_emb"][u_idx : u_idx + 1].copy().astype("float32")
    faiss.normalize_L2(taste)
    vibe_sims = (arts["vecs_n"] @ taste.T).squeeze(1)

    # NCF in batches
    u_vec = torch.tensor(
        np.tile(user_arts["user_emb"][u_idx], (len(arts["m2i"]), 1)), dtype=torch.float32
    )
    m_vec = torch.tensor(arts["movie_emb"], dtype=torch.float32)
    ncf_parts = []
    with torch.no_grad():
        for s in range(0, len(arts["m2i"]), 2048):
            out = (
                arts["ncf"](u_vec[s : s + 2048], m_vec[s : s + 2048])
                .squeeze(1)
                .numpy()
            )
            ncf_parts.append(out)
    ncf_scores = np.concatenate(ncf_parts)

    final = alpha * vibe_sims + (1.0 - alpha) * arts["nov_arr"]
    blended = 0.5 * ncf_scores + 0.5 * final

    top_idxs = np.argpartition(blended, -top_k)[-top_k:]
    top_idxs = top_idxs[np.argsort(blended[top_idxs])[::-1]]

    i2m = arts["i2m"]
    rows = []
    meta_idx = arts["meta"].set_index("movieId")
    for i in top_idxs:
        mid = i2m[i]
        if mid not in meta_idx.index:
            continue
        r = meta_idx.loc[mid]
        yr = r["year"]
        rows.append(
            {
                "movieId": mid,
                "title": r["title"],
                "year": int(yr) if yr == yr else "?",
                "genres": r["genres"],
                "avgRating": r.get("avgRating", None),
                "vibe_score": round(float(vibe_sims[i]), 4),
                "ncf_score": round(float(ncf_scores[i]), 4),
                "blended": round(float(blended[i]), 4),
                "emb_idx": int(i),
            }
        )
    return pd.DataFrame(rows)


def make_umap_plot(seed_emb_idx: int, rec_emb_idxs: list, umap_df: pd.DataFrame):
    """Scatter plot of seed + recommendations in UMAP vibe space."""
    all_idxs = [seed_emb_idx] + rec_emb_idxs
    subset = umap_df[umap_df["emb_idx"].isin(all_idxs)].copy()

    def role(row):
        if row["emb_idx"] == seed_emb_idx:
            return "Seed"
        return "Recommendation"

    subset["role"] = subset.apply(role, axis=1)
    subset["label"] = subset["title"].str[:30]

    # Background (sampled for speed)
    bg = umap_df[~umap_df["emb_idx"].isin(all_idxs)].sample(
        min(3000, len(umap_df)), random_state=0
    )
    bg["role"] = "All movies"
    bg["label"] = ""

    plot_df = pd.concat([bg, subset], ignore_index=True)

    color_map = {"All movies": "#d0d0d0", "Recommendation": "#2196F3", "Seed": "#F44336"}
    size_map = {"All movies": 3, "Recommendation": 10, "Seed": 14}

    fig = px.scatter(
        plot_df,
        x="umap_x",
        y="umap_y",
        color="role",
        color_discrete_map=color_map,
        size=[size_map[r] for r in plot_df["role"]],
        hover_name="label",
        hover_data={"umap_x": False, "umap_y": False, "role": False},
        title="Vibe Space — UMAP projection",
    )
    fig.update_layout(
        legend_title_text="",
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
    )
    fig.update_traces(marker=dict(opacity=0.7), selector=dict(name="All movies"))
    return fig


# ── Streamlit UI ──────────────────────────────────────────────────

st.set_page_config(
    page_title="VibeRec",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎬 VibeRec")
st.caption("Vibe-aware movie recommendations · CNN + LSTM vibe encoder + NCF collaborative filter")

arts = load_artifacts()

# ── Sidebar controls ──────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")
    mode = st.radio("Recommendation mode", ["Movie-based", "User-based"], index=0)
    alpha = st.slider(
        "α — Vibe ↔ Novelty",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.05,
        help="1.0 = pure vibe similarity · 0.0 = pure novelty · 0.8 default",
    )
    top_k = st.slider("Results to show", min_value=5, max_value=20, value=10, step=5)

    st.markdown("---")
    st.markdown(
        "**α knob:** controls how much the recommendation follows "
        "the seed's vibe vs. surfacing less popular, novel films."
    )

# ── Movie-based mode ──────────────────────────────────────────────
if mode == "Movie-based":
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        query = st.text_input("Search a movie title", placeholder="e.g. The Dark Knight")
    with col_btn:
        st.write("")
        recommend_btn = st.button("Recommend", type="primary")

    chosen_id = None
    if query:
        results = search_movie(query, arts["meta"])
        if results.empty:
            st.warning("No movies found.")
        else:
            options = {
                f"{r['title']} ({int(r['year']) if r['year']==r['year'] else '?'})": r["movieId"]
                for _, r in results.iterrows()
            }
            chosen_label = st.selectbox("Select movie", list(options.keys()))
            chosen_id = options[chosen_label]

            seed_row = arts["meta"].loc[arts["meta"]["movieId"] == chosen_id]
            if not seed_row.empty:
                r = seed_row.iloc[0]
                with st.expander("Seed movie details"):
                    st.markdown(
                        f"**{r['title']}** ({int(r['year']) if r['year']==r['year'] else '?'})"
                    )
                    st.caption(f"Genres: {r['genres']}")
                    if r["avgRating"] == r["avgRating"]:
                        st.caption(f"IMDb rating: {r['avgRating']:.1f}")

    if recommend_btn and chosen_id:
        with st.spinner("Computing recommendations…"):
            recs = get_recommendations(chosen_id, alpha, arts, top_k=top_k)

        if recs.empty:
            st.error("Could not find recommendations for this movie.")
        else:
            st.subheader(f"Top {len(recs)} recommendations  (α = {alpha})")
            n_cols = min(5, len(recs))
            cols = st.columns(n_cols)
            for i, (_, rec) in enumerate(recs.iterrows()):
                with cols[i % n_cols]:
                    st.markdown(f"**{rec['title']}**")
                    st.caption(f"{rec['year']}  ·  {rec['genres']}")
                    st.metric("Vibe score", f"{rec['vibe_score']:.3f}")
                    if rec["avgRating"] == rec["avgRating"]:
                        st.caption(f"IMDb {rec['avgRating']:.1f}")

            # UMAP plot
            st.subheader("Vibe space")
            seed_emb_idx = arts["m2i"].get(chosen_id, None)
            if seed_emb_idx is not None and "emb_idx" in recs.columns:
                rec_emb_idxs = recs["emb_idx"].tolist()
                fig = make_umap_plot(seed_emb_idx, rec_emb_idxs, arts["umap_df"])
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("Full results table"):
                st.dataframe(
                    recs[["title", "year", "genres", "avgRating", "vibe_score", "final_score"]],
                    use_container_width=True,
                )

# ── User-based mode ───────────────────────────────────────────────
else:
    user_arts = load_user_artifacts()

    user_input = st.text_input(
        "Enter user ID",
        placeholder="e.g. 12345",
        help=f"Valid range: any user in the MovieLens 25M dataset ({len(user_arts['u2i']):,} users)",
    )
    user_btn = st.button("Get recommendations", type="primary")

    if user_btn and user_input:
        try:
            uid = int(user_input.strip())
        except ValueError:
            st.error("Please enter a valid integer user ID.")
            uid = None

        if uid is not None:
            if uid not in user_arts["u2i"]:
                st.error(
                    f"User {uid} not found in taste profiles. "
                    "Try a user with at least 10 ratings in the dataset."
                )
            else:
                with st.spinner("Running NCF + vibe blend…"):
                    recs = get_user_recommendations(uid, alpha, arts, user_arts, top_k=top_k)

                if recs.empty:
                    st.error("No recommendations returned.")
                else:
                    st.subheader(f"Top {len(recs)} personalised picks  (α = {alpha})")
                    n_cols = min(5, len(recs))
                    cols = st.columns(n_cols)
                    for i, (_, rec) in enumerate(recs.iterrows()):
                        with cols[i % n_cols]:
                            st.markdown(f"**{rec['title']}**")
                            st.caption(f"{rec['year']}  ·  {rec['genres']}")
                            st.metric("Blended score", f"{rec['blended']:.3f}")
                            if rec["avgRating"] == rec["avgRating"]:
                                st.caption(f"IMDb {rec['avgRating']:.1f}")

                    with st.expander("Full results table"):
                        st.dataframe(
                            recs[["title", "year", "genres", "avgRating",
                                  "vibe_score", "ncf_score", "blended"]],
                            use_container_width=True,
                        )
