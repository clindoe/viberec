# VibeRec

A hybrid movie recommender that learns a 128-dimensional *vibe embedding* for each film from plot text, user tags, and metadata, then blends it with neural collaborative filtering via a tuneable α parameter.

---

## Results

| Model | Precision@10 | Recall@10 | NDCG@10 | HR@10 | MRR |
|-------|-------------|-----------|---------|-------|-----|
| Popularity | 0.0593 | 0.0630 | 0.0797 | 0.363 | 0.175 |
| Genre-Match | 0.0145 | 0.0147 | 0.0218 | 0.122 | 0.067 |
| SVD (k=64) | 0.0982 | 0.1149 | 0.1347 | 0.512 | 0.268 |
| **VibeRec** | **0.0393** | **0.0375** | **0.0478** | **0.271** | **0.113** |

Evaluated on 1,000 held-out test users. VibeRec prioritises vibe coherence and novel discovery over pure hit-rate maximisation; SVD optimises directly for the ranking metrics used here.

---

## Project Structure

```
VibeRec/
├── config.py                    # All paths and hyperparameters
├── VibeRec.ipynb                # Main notebook (Days 1–26)
├── app/
│   └── app.py                   # Streamlit demo (Days 27–28)
├── notebooks/
│   ├── writeup.ipynb            # Technical write-up (Days 29–30)
│   ├── day26_report.md          # Qualitative case studies
│   ├── day26_analysis.py        # Script that generates day26_report.md
│   ├── results_vibrec.csv       # VibeRec evaluation results
│   ├── results_baselines.csv    # Baseline results
│   └── results_ablation.csv     # Ablation study results
├── models/
│   ├── vibe_encoder_best.pt     # Trained CNN+LSTM vibe encoder (~97 MB)
│   └── ncf_best.pt              # Trained NCF model (~421 KB)
├── embeddings/
│   ├── movie_vibe_embeddings.npy  # 12k × 128 movie vibe vectors
│   ├── movie_id_to_idx.pkl
│   ├── user_taste_profiles.npy    # 162k × 128 user taste vectors
│   ├── user_id_to_idx.pkl
│   ├── faiss_movie.index          # FAISS inner-product index (movies)
│   ├── faiss_user.index           # FAISS inner-product index (users)
│   ├── novelty_scores.pkl         # Popularity + vibe-space novelty
│   ├── umap_coords.npy            # 2D UMAP projections
│   └── umap_movie_meta.pkl
└── data/
    ├── raw/                     # MovieLens 25M, IMDb TSVs, CMU summaries, GloVe
    └── processed/               # Tokenised sequences, embedding matrix, metadata
```

---

## Setup

```bash
git clone <repo-url>
cd VibeRec
pip install -r requirements.txt
```

Data and pre-trained model weights must be present in `data/` and `models/`. See `VibeRec.ipynb` for the full data pipeline.

---

## Run the Demo

```bash
streamlit run app/app.py
```

The app loads on `http://localhost:8501`.

**Movie-based mode:** search a title, pick from dropdown, adjust α slider, click Recommend.
**User-based mode:** enter a MovieLens user ID, click Get recommendations.

**α slider:**
- α = 1.0 → pure vibe similarity (coherent style/tone)
- α = 0.5 → balanced blend
- α = 0.0 → pure novelty (seed-independent)

---

## Architecture

```
Plot text   →  CNN (3,4,5-gram × 128 filters) → 128d
Tag text    →  LSTM (2-layer, 128 hidden)      → 128d   → Concat → MLP → 128d vibe emb
Metadata    →  Linear(23 → 64)                → 64d

Vibe emb   ──→ FAISS cosine  ──→ α × vibe_sim              ┐
User taste ──→ NCF MLP       ──→ (1-α) blend + novelty  ──→ final score
```

---

## Training

| Component | Loss | Epochs | Batch | Optimiser |
|-----------|------|--------|-------|-----------|
| VibeEncoder | Triplet (margin=0.5) | 20 | 128 | Adam 1e-3 |
| NCF | BCE (4× neg sampling) | 15 | 512 | Adam 1e-3 |

---

## References

- He et al. (2017) — Neural Collaborative Filtering
- Kim (2014) — CNN for Sentence Classification
- Hochreiter & Schmidhuber (1997) — LSTM
- Pazzani & Billsus (2007) — Content-Based Recommendation Systems
- Burke (2002) — Hybrid Recommender Systems
