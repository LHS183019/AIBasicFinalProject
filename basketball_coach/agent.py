from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools import agent_tool

from .asistant_agents.search import basketball_search_agent,player_db_agent
from .asistant_agents.guardrail import safety_input_agent
from . import prompts as my_prompts
from .config import MODEl, ENABLE_THOUGHT

root_agent = Agent(
    name="Basketball_Coach",
    model=MODEl,
    description=(
        my_prompts.basketball_coach_description
    ),
    instruction=(
        my_prompts.basketball_coach_instruction
    ),
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.9,
    ),
    # include_contents="default",
    planner=BuiltInPlanner(

            thinking_config=genai_types.ThinkingConfig(include_thoughts=ENABLE_THOUGHT)
        ),
    tools=[
           agent_tool.AgentTool(safety_input_agent),
           agent_tool.AgentTool(basketball_search_agent),
           agent_tool.AgentTool(player_db_agent),
           ],
)        
    
    # safety_settings=[
    #         genai_types.SafetySetting(  # avoid false alarm about rolling dice.
    #             category=genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    #             threshold=genai_types.HarmBlockThreshold.OFF,
    #         )],
 
    #     ),