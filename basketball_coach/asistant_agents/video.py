import os
import google.genai as genai
from google.genai import types
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

from ..config import GEMINI_MODEL,DEFAULT_VIDEO_UPLOAD_DIR
from ..prompts import *

import mimetypes # 用于猜测MIME类型



# -----------------------------ASISTANT FUNCTION--------------------------------# 

def file_name_check(file_path: str):
    if not os.path.isabs(file_path):
        potential_file_path = DEFAULT_VIDEO_UPLOAD_DIR / file_path
    else:
        return file_path
    if potential_file_path.exists():
        actual_file_path = str(potential_file_path)
    else:
        # 如果默认路径下没有，再考虑是不是用户真的就想说文件名而不是路径
        # 或者此时应该要求用户提供完整路径
        actual_file_path = file_path # 保持原样，让list_supported_video_files去检查
    return actual_file_path

def get_file_size_mb(file_path: str) -> dict:
    file_path = file_name_check(file_path)
    """
    Gets the size of a file in megabytes (MB).

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in megabytes (MB), rounded down.
             Returns an error message (str) if the file is not found or an access error occurs.
    """
    try:
        size_in_bytes = os.path.getsize(file_path)
        size_in_mb = size_in_bytes // (1024 * 1024)
        return {"size_mb": size_in_mb}
    except FileNotFoundError:
        return {"error": f"File not found at '{file_path}'"}
    except OSError as e:
        return {"error": f"Error accessing file '{file_path}': {e}"}

def list_supported_video_files(directory_path: str) -> dict:
    """
    Retrieves a list of video files supported by Gemini 2.5 Flash from a given directory.

    Args:
        directory_path (str): The path to the directory to scan.

    Returns:
        list[str]: A list where each element is the filename (e.g., "my_video.mp4")
                   of a supported video file found in the directory.
        str: An error message if the directory does not exist or is not accessible.
    """
    # Define the MIME types supported by Gemini 2.5 Flash for video understanding
    # Based on official documentation: video/mp4, video/x-flv, video/quicktime, video/mpeg,
    # video/mpegs, video/mpg, video/webm, video/wmv, video/3gpp
    supported_video_mimetypes = {
        "video/mp4",
        "video/x-flv",
        "video/quicktime",
        "video/mpeg",
        "video/mpegs", # Less common, but listed
        "video/mpg",   # Less common, but listed
        "video/webm",
        "video/wmv",
        "video/3gpp",
    }

    if not os.path.isdir(directory_path):
        return {"error": f"Directory not found or is not a valid directory: '{directory_path}'"}


    video_files = []
    try:
        # Walk through the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                # Guess the MIME type based on the file extension
                mime_type, _ = mimetypes.guess_type(file_path)

                # Check if the guessed MIME type is in our supported list
                if mime_type and mime_type in supported_video_mimetypes:
                    video_files.append(filename) # Only append the filename
    except OSError as e:
        return {"error": f"Error accessing directory '{directory_path}': {e}"}
    return {"video_files": video_files}


# -----------------------------GEMINI VISION MODEL REQUEST--------------------------------# 
def send_video_request(file_path: str, prompt: str) -> dict:
    file_path = file_name_check(file_path)
    
    """
    Sends a video analysis request to Gemini 2.5 Flash,
    choosing between inline data (for <20MB) and file upload (for >=20MB).

    Args:
        file_path (str): The path to the video file.
        prompt (str): The prompt for Gemini to analyze the video.

    Returns:
        str: The text response from Gemini, or an error message.
    """
    if not os.path.exists(file_path):
        return {"error": f"Video file does not exist at '{file_path}'"}
    if not os.path.isfile(file_path):
        return {"error": f"Path '{file_path}' is not a file."}

    # 获取文件大小
    file_size_mb_result = get_file_size_mb(file_path)

    if isinstance(file_size_mb_result, str): # Error from get_file_size_mb
        return file_size_mb_result

    file_size_mb = file_size_mb_result

    # 猜测 MIME 类型
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith('video/'):
        return {"error": f"Could not determine video MIME type for '{file_path}' or it's not a video."}

    client = genai.Client()
    response = None
    uploaded_file = None # Keep track of uploaded file for deletion

    try:
        # 这里用 20MB 作为粗略的分界线，实际可能需要微调
        if file_size_mb["size_mb"] < 20: # Use inline_data for smaller files
            print("Using inline_data method for video request (file < 20MB).")
            with open(file_path, 'rb') as f:
                video_bytes = f.read()

            contents = types.Content(
                parts=[
                    types.Part(inline_data=types.Blob(data=video_bytes, mime_type=mime_type)),
                    types.Part(text=prompt)
                ],
                role="model"
            )
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=types.GenerateContentConfig(temperature=0.3)
            )
        else: # Use file upload for larger files
            print("Using file upload method for video request (file >= 20MB).")
            # Upload the file
            uploaded_file = client.files.upload(file=file_path, config={"mime_type":mime_type})
            print(f"Uploaded file ID: {uploaded_file.name}")

            contents = [uploaded_file, prompt]
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents
            )
    except Exception as e:
        return {"error": f"with prompt{prompt},An error occurred during video request: {e}"}
    finally:
        # Always attempt to delete the uploaded file if it was uploaded
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name) # type:ignore
                print(f"Deleted uploaded file with ID: {uploaded_file.name}")
            except Exception as delete_e:
                print(f"Warning: Failed to delete uploaded file {uploaded_file.name}: {delete_e}")

    # Return the response text in a dictionary, or an error if no response.
    return {"response_text": response.text} if response else {"error": "No response received from Gemini."}



# -----------------------------THREE FUNCTION SENDING DIFFERENT PROMPT TO GEMINI--------------------------------# 
def analyze_players_in_video(file_path: str) -> dict:
    """
    详细分析篮球视频以列出可识别的球员及其球衣号码。
    """
    prompt = analyze_players_prompt
    return send_video_request(file_path, prompt)

def analyze_scoring_in_video(file_path: str) -> dict:
    """
    详细分析篮球视频中的得分事件，提供详细的结构化输出。
    """
    prompt = analyze_scoring_prompt
    return send_video_request(file_path, prompt)

def analyze_errors_and_fouls_in_video(file_path: str) -> dict:
    """
    详细分析篮球视频中的失误和犯规，提供详细的结构化输出。
    """
    prompt = analyze_errors_and_fouls_prompt
    return send_video_request(file_path, prompt)

def perform_comprehensive_video_analysis(file_path: str) -> dict:
    """
    对篮球视频进行一次快速、简化的综合性分析，包括球员信息、得分和失误/犯规。
    """    
    comprehensive_prompt = comprehensive_analysis_prompt
    return send_video_request(file_path, comprehensive_prompt)

# --- Agent 定义 ---
basketball_video_proccessor = Agent(
    name="basketball_video_proccessor",
    model=GEMINI_MODEL,
    description=video_analysis_description,
    instruction=video_analysis_instruction,
    tools=[
        FunctionTool(analyze_players_in_video),
        FunctionTool(analyze_scoring_in_video),
        FunctionTool(analyze_errors_and_fouls_in_video),
        FunctionTool(perform_comprehensive_video_analysis),
        FunctionTool(list_supported_video_files)
    ]
)

