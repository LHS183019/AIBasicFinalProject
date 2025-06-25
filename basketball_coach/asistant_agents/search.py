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
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from ..config import RAG_CORPUS
from google.adk.tools import google_search  # Import the tool

load_dotenv()
google_search_agent = Agent(
   name="google_search_agent",
   model="gemini-2.0-flash", 
   description=(
       "Agent to answer questions using Google Search."
       " If you can't find answer through basketball_RAG_search, "
       "go ahead and stick with google search!"
       ),
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[google_search]
)



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
    similarity_top_k=5,
    vector_distance_threshold=0.6,
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
)