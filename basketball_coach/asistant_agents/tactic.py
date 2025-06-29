import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor
from ..prompts import * 
from .search import player_data_recorder, basketball_rag_search_agent
from ..config import GEMINI_MODEL, DEEPSEEK_MODEL, DEFAULT_HTML_DIR
load_dotenv()


# ---------------TWO MODEL CODING AGENT CONFIG------------------------ #
gemini_code_agent = Agent(
    name="code_agent",
    model=GEMINI_MODEL,
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.
    """,
    description="Executes Python code to perform calculations.",

)

deepseek_code_agent = Agent(
    name="code_agent",
    model=DEEPSEEK_MODEL,
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.
    """,
    description="Executes Python code to perform calculations.",
)


# ---------------CODE TACTIC BOARD DRAWING AGENT(UNIMPLEMENT)------------------------ #

import os

# helper function
def save_html(html_content: str, file_name: str) -> dict:
    """
    将 HTML 字符串保存到 .html 文件中，并返回操作结果。

    Args:
        html_content (str): 要保存的 HTML 内容字符串。
        file_name (str): 希望保存的文件名（不含路径），例如 "my_tactic" 或 "tactic_board.html"。

    Returns:
        dict: 一个包含操作结果的字典。
              - 'success' (bool): True 表示成功，False 表示失败。
              - 'file_path' (str): 成功保存时的文件完整路径，失败时为空字符串。
              - 'message' (str): 操作结果的简短描述或错误信息。
    """
    if not file_name.lower().endswith(".html"):
        file_name += ".html"
    file_path = DEFAULT_HTML_DIR / file_name

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return {
            'success': True,
            'file_path': str(file_path),
            'message': f"HTML content saved to {str(file_path)}"
        }
    except Exception as e:
        return {
            'success': False,
            'file_path': '',
            'message': f"An unexpected error occurred: {e}"
        }

tactic_visualizer_coder  = Agent(
    name="tactic_visualizer_coder",
    model=GEMINI_MODEL,
    code_executor=BuiltInCodeExecutor(),
    description=tactic_visualizer_coder_description,
    instruction=tactic_visualizer_coder_instruction
)

# ---------------INTERGRATE ALL TACTIC AGENT------------------------ #

# Tactics Analysis & Generation Agent
tactic_maker_brainstorm = Agent(
    name="tactic_maker_brainstorm",
    model=GEMINI_MODEL,
    description=tactic_maker_brainstorm_description,
    instruction=tactic_maker_brainstorm_instruction,
    tools=[AgentTool(basketball_rag_search_agent)]
)

# User Interaction & Feedback Agent
basketball_tactic_maker = Agent(
    name="powerful_basketball_tactic_maker_agent",
    model=GEMINI_MODEL,
    description=basketball_tactic_maker_description,
    instruction=basketball_tactic_maker_instruction,
    tools=[AgentTool(player_data_recorder), AgentTool(tactic_maker_brainstorm), AgentTool(tactic_visualizer_coder),FunctionTool(save_html)]
)

root_agent = basketball_tactic_maker