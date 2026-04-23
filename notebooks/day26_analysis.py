"""
Day 26 — Qualitative Case Studies: formatted report generator.
Reads day26_case_studies.csv and writes day26_report.md
with per-seed tables (α=1.0 / 0.5 / 0.0) and analysis paragraphs.
"""

import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH     = os.path.join(PROJECT_ROOT, "notebooks", "day26_case_studies.csv")
OUT_PATH     = os.path.join(PROJECT_ROOT, "notebooks", "day26_report.md")

df = pd.read_csv(CSV_PATH)

ANALYSES = {
    "The Dark Knight": (
        "At α=1.0 (pure vibe), the encoder surfaces epic, morally weighty narratives — "
        "Lord of the Rings and 2001: A Space Odyssey share The Dark Knight's atmosphere of "
        "grandeur and existential stakes. At α=0.5, collaborative signals reinforce prestige-drama "
        "overlap while adding Ocean's Eleven, reflecting the same audience's taste for polished, "
        "high-craft films. At α=0.0 results become seed-independent (novelty-only scoring), "
        "demonstrating that a non-zero α is essential for coherent recommendations."
    ),
    "Mean Girls": (
        "Vibe similarity at α=1.0 surfaces older comedies with sharp social wit — "
        "School for Scoundrels and The Producers share Mean Girls' comedy-of-manners DNA "
        "despite the 40-year era gap, confirming the encoder captures tone over period. "
        "The α=0.5 blend retains genre fidelity while adding slightly more obscure entries "
        "that the same audience appreciated. "
        "At α=0.0 recommendations lose genre coherence entirely, confirming novelty alone "
        "cannot substitute for content-based signal."
    ),
    "Eternal Sunshine": (
        "At α=1.0, the encoder maps Eternal Sunshine to mystery-drama classics — Rashomon, "
        "The Usual Suspects, and Shadow of a Doubt all share its fractured-narrative, "
        "unreliable-reality vibe despite very different surface genres. "
        "At α=0.5 the mid-point shifts toward intimate character studies (Mishima, Mouchette) "
        "that the same cinephile audience rated highly. "
        "The α=0.0 collapse to identical results across all seeds confirms that "
        "novelty maximisation is seed-blind by design."
    ),
    "Before Sunrise": (
        "The vibe encoder correctly recognises Before Sunrise's contemplative, "
        "dialogue-driven European realism and surfaces Rohmer and Bunuel adjacent titles at α=1.0. "
        "At α=0.5, collaborative overlap adds quieter arthouse films that the same audience "
        "frequents — Late Autumn and The Cuckoo are strong cross-cultural matches. "
        "The α=0.0 collapse illustrates why the α knob exists: pure novelty erases "
        "all seed-specific signal."
    ),
    "Get Out": (
        "At α=1.0, the model clusters Get Out with classic comedy-romances "
        "(The White Sheik, Pauline at the Beach) — likely because its tightly scripted "
        "social dynamics and ensemble tension share textual vibe markers with dialogue-rich "
        "ensemble films more than the horror genre alone would suggest. "
        "At α=0.5 Kandahar appears, showing collaborative filtering pulling in audiences "
        "drawn to socially-charged, boundary-pushing cinema. "
        "This seed most clearly illustrates the gap between genre labels and learned vibe space."
    ),
    "Spirited Away": (
        "The vibe encoder places Spirited Away alongside mystery-crime classics at α=1.0, "
        "reflecting shared narrative themes of a protagonist navigating an unknown, rule-bound world. "
        "At α=0.5, intimate period dramas appreciated by arthouse/Ghibli audiences emerge. "
        "Spirited Away shares its α=1.0 neighbourhood with Eternal Sunshine and Good Will Hunting, "
        "indicating a broad 'prestige narrative' cluster in the learned vibe space — "
        "an area where richer tag data or a transformer encoder could better discriminate."
    ),
    "Good Will Hunting": (
        "Good Will Hunting occupies the same α=1.0 neighbourhood as Eternal Sunshine and "
        "Spirited Away, pointing to a 'prestige emotional drama' super-cluster in the vibe space. "
        "At α=0.5, film-noir and intimate European dramas emerge through collaborative overlap, "
        "reflecting cinephile fans' broad tastes. "
        "This clustering suggests the encoder captures emotional register and narrative weight "
        "rather than explicit genre, which is the intended behaviour for a vibe-based system."
    ),
    "Superbad": (
        "The vibe encoder correctly identifies Superbad's raunchy-comedy road-trip energy, "
        "surfacing Priscilla Queen of the Desert and Waking Ned Devine at α=1.0 — "
        "films sharing its ensemble-friends-on-a-journey exuberance across very different settings. "
        "At α=0.5, Leningrad Cowboys persists (strong vibe match) while Boudu Saved from Drowning "
        "enters as a collaborative signal. "
        "Superbad produces the most genre-coherent and intuitively satisfying recommendations "
        "across all alpha levels, suggesting comedy vibe is well-separated in embedding space."
    ),
    "Moonlight": (
        "Moonlight's quiet, intimacy-driven vibe is faithfully captured at α=1.0, "
        "retrieving tender romance-drama films from China, UK, and France alongside American titles. "
        "At α=0.5, the blend shifts toward international arthouse films with similar emotional "
        "restraint and unhurried pacing. "
        "Moonlight yields the most globally diverse recommendation set of all seeds, "
        "reflecting the encoder's cultural agnosticism when plot pacing and emotional register align."
    ),
}

def seed_table(seed_df, alpha):
    sub = seed_df[seed_df["alpha"] == alpha][["title", "year", "genres", "score"]].copy()
    sub = sub.reset_index(drop=True)
    sub.index += 1
    sub.columns = ["Title", "Year", "Genres", "Score"]
    sub["Score"] = sub["Score"].map("{:.4f}".format)
    return sub.to_markdown(index=True)


lines = []
lines.append("# Day 26 — Qualitative Case Studies\n")
lines.append(
    "10 seed movies spanning distinct vibe categories. "
    "For each seed, top-5 recommendations are shown at α=1.0 (pure vibe), "
    "α=0.5 (balanced), and α=0.0 (pure novelty).\n"
)
lines.append(
    "> **Note on α=0.0:** At α=0.0, the scoring function reduces to "
    "`score = novelty`, which is entirely seed-independent. "
    "This is by design — it serves as a control condition showing what happens "
    "when content signal is fully removed. All seeds share the same α=0.0 output.\n"
)

seeds = df["seed"].unique()
for seed in seeds:
    vibe = df.loc[df["seed"] == seed, "vibe"].iloc[0]
    lines.append(f"\n---\n\n## {seed}\n")
    lines.append(f"**Vibe category:** {vibe}\n")

    for alpha in [1.0, 0.5, 0.0]:
        lines.append(f"\n### α = {alpha}\n")
        lines.append(seed_table(df[df["seed"] == seed], alpha))
        lines.append("\n")

    analysis = ANALYSES.get(seed, "")
    if analysis:
        lines.append(f"\n**Analysis:** {analysis}\n")

with open(OUT_PATH, "w") as f:
    f.write("\n".join(lines))

print(f"[OK] Saved {OUT_PATH}")
