# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool

from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from ..config import RAG_CORPUS,RAG_TOP_K,RAG_DISTANCE_THRESHOLD
from google.adk.tools import google_search  # Import the tool
from ..data.local_db_tools import *
from ..prompts import * 

load_dotenv()

# ---------------GOOGLE SEARCH AGENT----------------- #
google_search_agent = Agent(
   name="google_search_agent",
   model="gemini-2.0-flash", 
   description=(
       "Agent to answer questions using Google Search."
       " If you can't find answer through basketball_RAG_search, "
       "go ahead and stick with google search!"
       ),
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[google_search],
   output_key="google_search_result"
)

# ---------------RAG SEARCH AGENT----------------- #
ask_vertex_retrieval = VertexAiRagRetrieval(
    name="basketball_retrieve_rag_documentation",
    description=(
        "Use this tool to retrieve documentation and reference materials for"
        " the question about basketball from the RAG corpus,"
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=RAG_CORPUS,
        )
    ],
    similarity_top_k=RAG_TOP_K,
    vector_distance_threshold=RAG_DISTANCE_THRESHOLD
)

basketball_rag_search_agent = Agent(
    model="gemini-2.0-flash",
    name="basketball_rag_search_agent",
    description=(
        "An AI assistant that can retrieve documentation and reference materials for"
        " the question about basketball(including basketball technic,"
        " how to recover when getting harm from a game, famous basketball player"
        " etc.)"  
    ),
    instruction=(
        # "You are an chat AI, and you can find useful basketball related data using tool 'retrieve_rag_documentation'"
        "You are an AI assistant with access to specialized corpus of"
        " documents. Your role is to provide accurate and concise answers to"
        " questions based on documents that are retrievable using"
        " ask_vertex_retrieval. If no related result, say you can't find any related data."
    ),
    tools=[ask_vertex_retrieval],
    output_key="basketball_rag_result"
)

# ---------------LOCAL USER DATABASE SEARCH AGENT----------------- #

player_db_agent = Agent(
    model="gemini-2.0-flash",
    name="user_customized_players_information_database_service_agent",
    description=player_db_agent_description,
    instruction=player_db_agent_instruction,
    tools=[
        # 添加球员资料库工具
        FunctionTool(get_player_by_name),
        FunctionTool(list_all_players),
        FunctionTool(add_player),
        FunctionTool(update_player),
        FunctionTool(delete_player),
    ]
)

# ---------------INTERGRATE ALL SEARCH AGENT------------------------ #


merger_agent = Agent(
    name="parallel_search_results_merger_agent",
    model="gemini-2.5-flash",  # Or potentially a more powerful model if needed for synthesis
    instruction=merger_agent_instruction,
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs." 
)

parallel_search_agent = ParallelAgent(
     name="parallel_search_agent",
     sub_agents=[google_search_agent, basketball_rag_search_agent],
     description="Runs multiple research agents in p arallel to gather information."
)

sequential_search_pipeline_agent = SequentialAgent(
     name="sequential_search_pipeline_agent",
     # Run parallel research first, then merge
     sub_agents=[parallel_search_agent, merger_agent],
     description="Coordinates parallel research and synthesizes the results about a basketball-related inquiry, using both RAG system and google search to grounded the results."
 )

basketball_search_agent = Agent(
    name="powerful_basketball_related_search_agent",
    model="gemini-2.5-flash",
    description=basketball_search_agent_description,
    instruction=basketball_search_agent_instruction,
    tools=[AgentTool(player_db_agent), AgentTool(sequential_search_pipeline_agent)]
)

root_agent = basketball_search_agent