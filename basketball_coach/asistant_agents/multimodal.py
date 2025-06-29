from google.adk import Agent
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.genai import Client
from google.genai import types

client = Client()
    
async def generate_image(prompt: str, tool_context: 'ToolContext'):
    """Generates an image based on the prompt."""
    response = client.models.generate_content(
        model='gemini-2.0-flash-preview-image-generation',
        contents=prompt,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )
    if not response.candidates:
        return {'status': 'failed'}
    
    respons_text = ""
    for part in response.candidates[0].content.parts: # type: ignore
        if part.text is not None:
            respons_text += part.text
        elif part.inline_data is not None:
            await tool_context.save_artifact(
                'image.png',
                types.Part.from_bytes(data=(part.inline_data.data), mime_type='image/png'), # type: ignore
            )
            break
  
    return {
        'status': 'success',
        'detail': 'Image generated successfully and stored in artifacts.',
        'filename': 'image.png',
        'tool_response': respons_text
    }
    
  
image_generate_agent = Agent(
    model='gemini-2.0-flash',
    name='image_generate_agent',
    description="""An agent that generates images and answer questions about the images.""",
    instruction="""You are an agent whose job is to generate or edit an image based on the user's prompt.
""",
    tools=[generate_image, load_artifacts],
)

import os
import wave
from google.adk.tools.agent_tool import AgentTool
from ..config import DEFAULT_TTS_AUDIO_DIR

# def file_name_check(file_path: str):
#     if not os.path.isabs(file_path):
#         potential_file_path = DEFAULT_TTS_AUDIO_DIR / file_path
#     else:
#         return file_path
#     if potential_file_path.exists():
#         actual_file_path = str(potential_file_path)
#     else:
#         # 如果默认路径下没有，再考虑是不是用户真的就想说文件名而不是路径
#         # 或者此时应该要求用户提供完整路径
#         actual_file_path = file_path # 保持原样，让list_supported_video_files去检查
#     return actual_file_path


def save_wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    filename = DEFAULT_TTS_AUDIO_DIR / filename
    with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

async def send_tts_request(content:str, tool_context: 'ToolContext') -> dict:
    """TTS(text to speech), generate audio based on the content provided."""
    try:
        response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=content,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Kore',
                    )
                )
            ),
        )
        )
        data = response.candidates[0].content.parts[0].inline_data.data # type: ignore
        await tool_context.save_artifact(
                'tts.wav',
                types.Part.from_bytes(data=(data), mime_type='audio/wav'), # type: ignore
            )

    except Exception as e:
        return {"error": f"Error occur when sending tts request {e}"}
    else:
        return {
        'status': 'success',
        'detail': 'TTS audio generated successfully and stored in artifacts.',
        'filename': 'tts.wav'
    }
    
# def send_tts_request(file_name:str,content:str, tool_context: 'ToolContext') -> dict:
#     """TTS(text to speech), generate audio based on the content provided."""
#     try:
#         response = client.models.generate_content(
#         model="gemini-2.5-flash-preview-tts",
#         contents=content,
#         config=types.GenerateContentConfig(
#             response_modalities=["AUDIO"],
#             speech_config=types.SpeechConfig(
#                 voice_config=types.VoiceConfig(
#                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                     voice_name='Kore',
#                     )
#                 )
#             ),
#         )
#         )
#         data = response.candidates[0].content.parts[0].inline_data.data # type: ignore
        
#         save_wave_file(file_name_check(file_name), data) # Saves the file to current directory

#         return {"status":"success","file_path":f"{file_name_check(file_name)}"}
#     except Exception as e:
#         return {"error": f"Error occur when sending tts request {e}"}


    
tts_agent = Agent(
    model='gemini-2.0-flash',
    name='tts_agent',
    description="""一个将文本转化为语音的代理，能够合成自然流畅的语音并进行播放。""", # Updated description
    instruction="""你是一个文本转语音（TTS）代理。
    - 你的核心职责是将用户提供的文本内容转换成高质量的语音。
    - 当用户请求将某段文本转换为语音时，请调用你的工具 `send_tts_request`。
    - 成功生成语音后，请告知用户音频已准备好并已保存为工件。
    - 你不负责生成图像、分析视频或其他非TTS相关任务。
    - 始终使用清晰、自然的语音进行回复。
""",
    tools=[send_tts_request, load_artifacts],
)


multimodal_agent = Agent(
    model='gemini-2.0-flash',
    name='multimodal_agent',
    description="""一个多模态代理，能够处理文本、图像和语音相关的任务。""", # New description
    instruction="""你是一个多模态交互代理。
    - 根据用户的请求，决定是生成图像（调用 `image_generate_agent`）还是将文本转换为语音（调用 `tts_agent`）。
    - 当用户要求生成图像时，将任务委托给 `image_generate_agent`。
    - 当用户要求将文本转换为语音时，将任务委托给 `tts_agent`。
    - 如果用户的请求不明确或需要两种模态的组合，请尝试引导用户明确其意图。
    - 你不直接处理这些模态任务，而是协调和调用专业的子代理来完成。
""", 
    tools=[AgentTool(tts_agent),AgentTool(image_generate_agent)]
)

root_agent = multimodal_agent
