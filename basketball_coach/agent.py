from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools import agent_tool

from .asistant_agents.search import basketball_search_agent,player_db_agent,google_search_agent
from .asistant_agents.guardrail import safety_input_agent
from .asistant_agents.strategy import strategy_maker_agent
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
    planner=BuiltInPlanner(

            thinking_config=genai_types.ThinkingConfig(include_thoughts=ENABLE_THOUGHT)
        ),
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.8,
        top_p=0.9
    ),
    include_contents="default",
    tools=[agent_tool.AgentTool(google_search_agent),
           agent_tool.AgentTool(safety_input_agent),
           agent_tool.AgentTool(basketball_search_agent),
           agent_tool.AgentTool(player_db_agent),
           agent_tool.AgentTool(strategy_maker_agent),
           ],
)        
    
    # safety_settings=[
    #         genai_types.SafetySetting(  # avoid false alarm about rolling dice.
    #             category=genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    #             threshold=genai_types.HarmBlockThreshold.OFF,
    #         )],
 
    #     ),