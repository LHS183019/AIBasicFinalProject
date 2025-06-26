import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor
from ..prompts import * 
from .search import player_data_recorder, basketball_rag_search_agent
from ..config import GEMINI_MODEL, DEEPSEEK_MODEL
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
tactic_board_draw = Agent(
    name="tactic_maker_brainstorm",
    model=GEMINI_MODEL,
    description=tactic_maker_brainstorm_description,
    instruction=tactic_maker_brainstorm_instruction
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
    tools=[AgentTool(player_data_recorder), AgentTool(tactic_maker_brainstorm)]
)

root_agent = basketball_tactic_maker