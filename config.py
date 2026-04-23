"""
config.py - Central configuration for VibeRec.
All paths, hyperparameters, and constants live here.
Import this module wherever you need a setting.
"""

import os
import torch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_RAW       = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED = os.path.join(PROJECT_ROOT, "data", "processed")
MODELS_DIR     = os.path.join(PROJECT_ROOT, "models")
EMBEDDINGS_DIR = os.path.join(PROJECT_ROOT, "embeddings")
NOTEBOOKS_DIR  = os.path.join(PROJECT_ROOT, "notebooks")

# Raw dataset files
MOVIELENS_RATINGS = os.path.join(DATA_RAW, "ml-25m", "ratings.csv")
MOVIELENS_MOVIES  = os.path.join(DATA_RAW, "ml-25m", "movies.csv")
MOVIELENS_TAGS    = os.path.join(DATA_RAW, "ml-25m", "tags.csv")
MOVIELENS_LINKS   = os.path.join(DATA_RAW, "ml-25m", "links.csv")

IMDB_BASICS   = os.path.join(DATA_RAW, "imdb", "title.basics.tsv")
IMDB_RATINGS  = os.path.join(DATA_RAW, "imdb", "title.ratings.tsv")

CMU_SUMMARIES = os.path.join(DATA_RAW, "cmu", "plot_summaries.txt")
CMU_METADATA  = os.path.join(DATA_RAW, "cmu", "movie.metadata.tsv")

GLOVE_PATH    = os.path.join(DATA_RAW, "glove", "glove.6B.300d.txt")

# Processed files
MOVIES_MASTER       = os.path.join(DATA_PROCESSED, "movies_master.csv")
RATINGS_TRAIN       = os.path.join(DATA_PROCESSED, "ratings_train.csv")
RATINGS_TEST        = os.path.join(DATA_PROCESSED, "ratings_test.csv")
PLOT_SEQUENCES      = os.path.join(DATA_PROCESSED, "plot_sequences.npy")
REVIEW_SEQUENCES    = os.path.join(DATA_PROCESSED, "review_sequences.npy")
WORD2IDX_PATH       = os.path.join(DATA_PROCESSED, "word2idx.pkl")
EMBEDDING_MATRIX    = os.path.join(DATA_PROCESSED, "embedding_matrix.npy")
METADATA_FEATURES   = os.path.join(DATA_PROCESSED, "metadata_features.npy")

# Model / embedding outputs
VIBE_ENCODER_CKPT       = os.path.join(MODELS_DIR, "vibe_encoder_best.pt")
NCF_CKPT                = os.path.join(MODELS_DIR, "ncf_best.pt")
MOVIE_VIBE_EMBEDDINGS   = os.path.join(EMBEDDINGS_DIR, "movie_vibe_embeddings.npy")
MOVIE_ID_TO_IDX         = os.path.join(EMBEDDINGS_DIR, "movie_id_to_idx.pkl")
USER_TASTE_PROFILES     = os.path.join(EMBEDDINGS_DIR, "user_taste_profiles.npy")
USER_ID_TO_IDX          = os.path.join(EMBEDDINGS_DIR, "user_id_to_idx.pkl")
NOVELTY_SCORES          = os.path.join(EMBEDDINGS_DIR, "novelty_scores.pkl")
FAISS_MOVIE_INDEX       = os.path.join(EMBEDDINGS_DIR, "faiss_movie.index")
FAISS_USER_INDEX        = os.path.join(EMBEDDINGS_DIR, "faiss_user.index")
TASTE_TWINS             = os.path.join(EMBEDDINGS_DIR, "taste_twins.pkl")

# ---------------------------------------------------------------------------
# Device
# ---------------------------------------------------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------------------------------------------------------------------
# Text / Vocabulary
# ---------------------------------------------------------------------------
VOCAB_SIZE        = 40_000   # top-K words kept
PLOT_MAX_LEN      = 500      # token length for plot sequences
REVIEW_MAX_LEN    = 200      # token length for review/tag sequences
EMBEDDING_DIM     = 300      # GloVe dimension
PAD_TOKEN         = "<PAD>"
UNK_TOKEN         = "<UNK>"

# ---------------------------------------------------------------------------
# Vibe Encoder
# ---------------------------------------------------------------------------
CNN_FILTERS       = 128      # filters per kernel size
CNN_KERNELS       = [3, 4, 5]
CNN_OUT_DIM       = 128      # after projection
LSTM_HIDDEN       = 128      # per direction
LSTM_LAYERS       = 2
LSTM_OUT_DIM      = 128      # after projection
METADATA_DIM      = 23       # one-hot genres + normalized scalars
METADATA_PROJ_DIM = 64
VIBE_EMBED_DIM    = 128      # final movie vibe embedding dimension
DROPOUT_VIBE      = 0.3

TRIPLET_MARGIN    = 0.5
VIBE_LR           = 1e-3
VIBE_WEIGHT_DECAY = 1e-5
VIBE_EPOCHS       = 20
VIBE_BATCH_SIZE   = 128

# ---------------------------------------------------------------------------
# NCF Model
# ---------------------------------------------------------------------------
NCF_HIDDEN        = [256, 128, 64]  # MLP layer sizes
DROPOUT_NCF_1     = 0.3
DROPOUT_NCF_2     = 0.2
NCF_LR            = 1e-3
NCF_EPOCHS        = 15
NCF_BATCH_SIZE    = 512
NCF_NEG_RATIO     = 4            # negatives per positive sample

# ---------------------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------------------
DEFAULT_ALPHA     = 0.8      # vibe similarity weight
TOP_K             = 10       # default number of recommendations
MIN_RATINGS       = 10       # minimum ratings for a movie to be included
HIGH_RATING_THRESH = 4.0     # threshold for "liked" movies
TASTE_TWINS_K     = 50       # nearest taste-twin users to find

# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
EVAL_K            = 10       # Precision/Recall/NDCG @K
TRAIN_SPLIT       = 0.8      # temporal train/test split ratio
