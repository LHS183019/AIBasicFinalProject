# Multi-Model AI Chat Application

This project is a web-based, multi-model AI chat application built with Python and the [Reflex](https://reflex.dev/) framework. It allows users to interact with various Large Language Models (LLMs) from different providers, manage chat sessions, and configure API keys directly within the application.

## Features

*   **Interactive Web UI:** Modern and responsive user interface built with Reflex.
*   **Real-time Streaming:** LLM responses are streamed in real-time for a dynamic chat experience.
*   **Multiple Chat Sessions:** Users can create, delete, and switch between different chat conversations.
*   **Dynamic Model Selection:** Supports selection between various models from providers like SiliconFlow and Gemini (as defined in `model_API.py`).
*   **In-App API Key Management:** API keys for SiliconFlow and Gemini can be configured and updated directly within the application's settings.
*   **Response Interruption:** Users can interrupt the generation of LLM responses.
*   **Markdown Rendering:** Chat messages are rendered with Markdown support for rich text formatting.

## Getting Started

Follow these instructions to set up and run the application locally.

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```
*(Replace `<repository_url>` and `<repository_directory>` with actual values)*

### 2. Set Up Python Environment

Ensure you have Python 3.10 or newer installed. It's recommended to use a virtual environment:

```bash
python -m venv .venv
# On Windows
# .venv\Scripts\activate
# On macOS/Linux
# source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

API keys are required to use the language models. There are two primary ways to configure them:

*   **Via `.env` File (Initial Defaults/Fallbacks):**
    Create a `.env` file in the root directory of the project and add your API keys. This file is typically loaded at application startup.
    ```env
    SILICONFLOW_API_KEY="your_siliconflow_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    # OPENAI_AGENTS_DISABLE_TRACING=1 # Optional, for LangSmith tracing
    ```
    The application will use these as initial default keys or as fallbacks if keys are not set within the app's UI.

*   **In-App UI Management:**
    API keys can also be managed (added/updated) directly within the application's settings interface, usually found in the sidebar. Keys set in the UI are stored in the application's state and are prioritized for API calls.

### 5. Run the Application

Use the Reflex CLI to run the application:

```bash
reflex run
```

### 6. Access in Browser

Once the application is running (compilation may take a moment), open your web browser and navigate to:

[http://localhost:3000](http://localhost:3000)

(The port may vary if 3000 is already in use; check the output from the `reflex run` command.)

## Module Descriptions

*   **`main.py`**:
    Initializes and configures the Reflex web application. It sets up the `ReflexUIManager` and adds the main application page, making the app ready to be served by the Reflex CLI.

*   **`ui_manager.py`**:
    Contains the core UI logic and state management for the Reflex application.
    *   `ReflexUIManager`: Orchestrates the web UI, handling the setup of model APIs and response handlers, and providing implementations for UI-related abstract methods (like error display, signal handling).
    *   `ReflexUIManagerState`: The Reflex state class that holds all UI-related variables (e.g., chat messages, API keys, selected model, processing status), event handlers for UI interactions, and computed properties that drive the web interface.

*   **`ui_manager_reflex_components/` (Directory)**:
    This directory contains various `.py` files, each defining specific UI components (e.g., `navbar.py`, `chat_area.py`, `sidebar.py`, `settings_modals.py`) built with Reflex. These components form the building blocks of the application's user interface.

*   **`model_API.py`**:
    Handles direct communication with the different LLM provider APIs (e.g., SiliconFlow, Gemini). It includes classes like `SiliconflowModelAPI` and `GeminiModelAPI` responsible for making API requests, managing API key usage for those requests, and listing available `ModelType`s.

*   **`model_response_handler.py`**:
    Processes the responses received from the LLM APIs. It's responsible for handling streaming data (if applicable) and ensuring it's correctly passed to the `ReflexUIManager` (via its `display_text_output` method) for display in the UI.

## Development Notes

*(This section can be updated based on current team practices. The original text about `development`, `feature:ui`, `feature:ai` branches might need review for current relevance.)*

### Git Workflow
Maintain a clear branching strategy. For instance:
*   `main`: Stable releases.
*   `development`: Integration branch for new features.
*   `feature/*`: Individual feature branches (e.g., `feature/multi-modal-input`, `feature/tts-output`).

Merge features into `development`, and once stable, merge `development` into `main`.

### Updating `requirements.txt`
If you add new dependencies during development, update `requirements.txt`:
```bash
pip install pipreqs
pipreqs . --encoding=utf8 --force
```

### Code Style and Quality
*   **Type Hinting:** Use Python's `typing` module for type hints.
*   **Docstrings & Comments:** Write clear docstrings for classes and functions. Use comments (TODO, FIXME, NOTE, XXX, HACK, BUG) to highlight areas needing attention or explanation.
*   **Exception Handling:** Implement robust error handling using try-except blocks, providing informative messages to the user or logs.
*   **LLM Assistance:** Utilize AI coding assistants for suggestions, refactoring, and documentation, but always critically review and thoroughly test the generated code.

### Useful Documentation
*   [Reflex Docs](https://reflex.dev/docs/getting-started/introduction/)
*   [Reflex Chat Template Example](https://reflex.dev/templates/reflex-chat/)
*   [Siliconflow API Docs](https://docs.siliconflow.com/cn/userguide/introduction)
*   [Gemini API Docs](https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn) (Note: May require VPN depending on region)
*   [OpenAI API Docs](https://platform.openai.com/docs/overview) (Note: May require VPN depending on region)

(The original "開發手冊" and "开发约定Git" sections have been integrated or updated above. Specific team workflow details can be further refined by the team.)