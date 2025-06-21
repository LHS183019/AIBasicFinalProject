from google.adk import Agent
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.genai import Client
from google.genai import types
from PIL import Image
from io import BytesIO

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
    
  


root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description="""An agent that generates images and answer questions about the images.""",
    instruction="""You are an agent whose job is to generate or edit an image based on the user's prompt.
""",
    tools=[generate_image, load_artifacts],
)