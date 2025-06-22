from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools import agent_tool
from google.adk.code_executors import BuiltInCodeExecutor
from asistant_agents.knowledge_collect import search_agent
from asistant_agents.toolkit import code_agent,safety_input_agent
import prompt as my_prompt

root_agent = Agent(
    name="Basketball_Coach",
    model="gemini-2.5-flash",
    description=(
        my_prompt.Basketball_Coach_description
    ),
    instruction=(
        my_prompt.Basketball_Coach_instruction
    ),
    planner=BuiltInPlanner(
            thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
        ),
    tools=[agent_tool.AgentTool(search_agent),agent_tool.AgentTool(code_agent),agent_tool.AgentTool(safety_input_agent)],
)

