from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools import agent_tool
from google.adk.code_executors import BuiltInCodeExecutor

search_agent = Agent(
   name="basic_search_agent",
   model="gemini-2.0-flash", 
   description="Agent to answer questions using Google Search.",
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[google_search]
)