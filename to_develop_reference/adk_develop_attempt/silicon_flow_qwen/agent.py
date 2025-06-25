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

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
import os
from google.genai import types as genai_types


# NOTE: Siliconflow VLM not support tool use

BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_QWEN_VL = "openai/Qwen/Qwen3-32B"
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

model_config = {
    "model": MODEL_QWEN_VL,
    "api_key": SILICONFLOW_API_KEY,
    "api_base": BASE_URL
}

root_agent = Agent(
        name="helpful_Asistant",
        # Key change: Wrap the LiteLLM model identifier
        model=LiteLlm(**model_config),
        description="",
        instruction="You are a helpful assistant powered by Qwen. "
    )

# Sample queries to test the agent: 

# # Agent will give weather information for the specified cities.
# # What's the weather in Tokyo?
# # What is the weather like in London?
# # Tell me the weather in New York?

# # Agent will not have information for the specified city.
# # How about Paris?  