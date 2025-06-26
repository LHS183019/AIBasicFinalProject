import asyncio
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
import os

BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_DEEPSEEK_R1 = "openai/deepseek-ai/DeepSeek-R1"
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

DEEPSEEK_MODEL = LiteLlm(
                model=MODEL_DEEPSEEK_R1,
                api_key=SILICONFLOW_API_KEY,
                api_base=BASE_URL
            )


AGENT_NAME = "calculator_agent"
# Agent Definition
code_agent = LlmAgent(
    name=AGENT_NAME,
    model=DEEPSEEK_MODEL,
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.
    """,
    description="Executes Python code to perform calculations.",
)

root_agent = code_agent