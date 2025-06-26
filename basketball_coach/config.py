import os

# -------------MODEL CONFIG----------------- #
MODEl = "gemini-2.5-flash"
ENABLE_THOUGHT = True

# -------------RAG ENGINE CONFIG----------------- #
RAG_CORPUS = os.environ.get("RAG_CORPUS")
RAG_TOP_K = 5
RAG_DISTANCE_THRESHOLD = 0.6

# -------------USER PLAYER DB CONFIG----------------- #
USER_PLAYER_DATA_FILE = "basketball_coach//data//players.json"
USER_PLAYER_DATA_DIR = "basketball_coach//data"