import os
from google.adk.models.lite_llm import LiteLlm
from pathlib import Path


# TODO: CHECK IF ENV IS SET

# -------------MODEL CONFIG----------------- #
GEMINI_MODEL = "gemini-2.5-flash"
ENABLE_THOUGHT = True

BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_DEEPSEEK_R1 = "openai/deepseek-ai/DeepSeek-R1"
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

DEEPSEEK_MODEL = LiteLlm(
                model=MODEL_DEEPSEEK_R1,
                api_key=SILICONFLOW_API_KEY,
                api_base=BASE_URL
            )


# -------------RAG ENGINE CONFIG----------------- #
RAG_CORPUS = os.environ.get("RAG_CORPUS")
RAG_TOP_K = 5
RAG_DISTANCE_THRESHOLD = 0.6

# -------------USER PLAYER DB CONFIG----------------- #
USER_PLAYER_DATA_FILE = "basketball_coach//data//test_players.json"
USER_PLAYER_DATA_DIR = "basketball_coach//data"


# -------------VIDEO ANALYZE CONFIG----------------- #
DEFAULT_VIDEO_UPLOAD_DIR = Path.cwd() / "basketball_coach" / "videos"
DEFAULT_VIDEO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)