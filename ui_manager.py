from abc import ABC, abstractmethod
from typing_extensions import Union, TypedDict
from typing import Dict, List, Callable, Any
import reflex as rx
import keyboard
import os
import asyncio # For async operations in process_question

# Import necessary classes and types
from model_API import ModelType, SiliconflowModelAPI, GeminiModelAPI # Added GeminiModelAPI
from model_response_handler import SiliconflowModelResponseHandler, GeminiModelResponseHandler # Added GeminiModelResponseHandler
# Import components for the main page layout
from ui_manager_reflex_components.navbar import app_navbar
from ui_manager_reflex_components.chat_area import chat_display_area
from ui_manager_reflex_components.action_bar import chat_input_bar
# Settings modal is usually part of navbar or sidebar, so not directly in main layout stack
# from ui_manager_reflex_components.settings_modals import new_chat_modal (already in navbar)


class UIManager(ABC):
    """
    UIManager is an abstract base class that defines the interface for user interface managers.
    Concrete implementations of this class should provide specific behavior for displaying information,
    handling output state, and managing events.
    Attributes:
        _paused_response_output(bool): Indicates whether the UI should pause response output.
    """
    def __init__(self):
        super().__init__()
        self._paused_response_output = False

    @property
    def paused_response_output(self):
        """property to shown if the UI should terminate the output"""
        return self._paused_response_output

    @paused_response_output.setter
    def paused_response_output(self, new_value:bool):
        self._paused_response_output = new_value

    @abstractmethod
    def show_enter_info(self):
        """
        Display the enter information to the user.
        """
        pass
    
    @abstractmethod
    def show_exit_info(self):
        """
        Display the exit information to the user.
        """
        pass

    @abstractmethod
    def show_error_info(self,e:Exception):
        """
        Display the error information to the user.
        """
        pass
    
    @abstractmethod
    def display_text_output(self, output: str, **kwargs):
        """
        Display the text output to the user.
        """
        pass

    # TODO
    @abstractmethod
    def display_img_output(self):
        """
        Display the image output to the user.
        """
        pass
    
    # TODO
    @abstractmethod
    def display_audio_output(self):
        """
        Display the audio output to the user.
        """
        pass

    # etc.....

    @abstractmethod
    def handle_signal(self, signal:str):
        """
        Handle the signal received.
        XXX: currently there are signal 'display_starts' and 'display_ends'""
        """
        pass



class CLIManager(UIManager):
    def __init__(self,teminate_output_hot_key:str="q"):
        super().__init__()
        self.reasoning_style_ouput = False
        self.SEP = "#"*30
        self.hotkey_char = teminate_output_hot_key
        self.temp_hotkey = None
        

    def show_enter_info(self):
        print("欢迎来到语言大模型应用！在下方输入您想问大模型的问题。输入'Ctrl+Z'（Windows）或'Ctrl+D'（Unix/Linux/Mac）以退出应用。")


    def show_exit_info(self):
        print("\n欢迎下次使用！")


    def show_error_info(self, e:Exception):
        print(f"出现错误:{str(e)}")
        print(f"自动退出程序！")
        
        
    def get_user_input(self) -> str:
        return input(">>> ").strip()

    def termintate_llm_output(self):
        self.paused_response_output = True

    def handle_signal(self, signal:str):
        if signal == "display_ends":
            print()
            if self.temp_hotkey:
                self.reasoning_style_ouput = False
                keyboard.clear_hotkey(self.temp_hotkey)
        elif signal == "display_starts":
            print(f"输入'{self.hotkey_char}'中止模型输出：")
            self.paused_response_output = False
            self.temp_hotkey = keyboard.add_hotkey(self.hotkey_char,self.termintate_llm_output,suppress=True)

    def display_text_output(self, output: str, reasoning: bool):
        if(reasoning and not self.reasoning_style_ouput) or (not reasoning and self.reasoning_style_ouput):
            print(self.SEP)
            self.reasoning_style_ouput = not self.reasoning_style_ouput
        print(output, end="", flush=True)

    def display_img_output(self):
        pass

    def display_audio_output(self):
        pass

# TODO：
# https://reflex.dev/docs/events/decentralized-event-handlers/

# HACK: I'm not sure the following code works, u can recode it anyway, but hope that you get what I expected? 
# Define QA TypedDict (if not already moved to a central types file)
class QA(TypedDict): # Keep QA definition
    question: str
    answer: str

# Create ReflexUIManagerState
class ReflexUIManagerState(rx.State):
    """Manages the state for the Reflex UI."""
    _chats: dict[str, list[QA]] = {"General": []}
    current_chat: str = "General"
    processing: bool = False
    is_new_chat_modal_open: bool = False
    user_question: str = ""  # Stores the question being actively processed or typed by the user
    selected_model_str: str = ModelType.SILICONFLOW_DEEPSEEK_R1.value  # Default model
    api_keys: dict[str, str] = {} # Stores API keys like {"SILICONFLOW": "key1", "GEMINI": "key2"}
    show_long_thinking: bool = True
    current_llm_output: str = "" # Holds the streaming output from LLM for display
    interrupt_requested: bool = False

    # For interaction with ModelAPI and ResponseHandler
    # model_api: Any = None  # No longer storing a single model_api here
    # response_handler: Any = None # No longer storing a single response_handler here
    ui_manager: UIManager = None # To call UIManager methods and access its model APIs

    # Computed Variables for Chats
    @rx.var
    def chat_titles(self) -> list[str]:
        """Returns a list of chat titles."""
        return list(self._chats.keys())

    @rx.var
    def selected_chat_messages(self) -> list[QA]:
        """Returns messages for the current_chat."""
        return self._chats.get(self.current_chat, [])

    # Basic Chat Management Event Handlers
    def create_chat(self, form_data: dict[str, Any]):
        """Creates a new chat."""
        new_chat_name = form_data.get("new_chat_name", "").strip()
        if new_chat_name and new_chat_name not in self._chats:
            self._chats[new_chat_name] = []
            self.current_chat = new_chat_name # Optionally switch to the new chat
        self.is_new_chat_modal_open = False # Close modal

    def delete_chat(self, chat_name: str):
        """Deletes a specified chat."""
        if chat_name in self._chats and len(self._chats) > 1:
            del self._chats[chat_name]
            if self.current_chat == chat_name:
                self.current_chat = list(self._chats.keys())[0] # Set to the first available chat
        elif len(self._chats) == 1 and chat_name in self._chats:
            # Prevent deleting the last chat, or handle as preferred (e.g., clear it)
            print("Cannot delete the last chat.") # Or show a UI message

    def set_chat(self, chat_name: str):
        """Sets the current_chat."""
        if chat_name in self._chats:
            self.current_chat = chat_name

    def set_is_new_chat_modal_open(self, is_open: bool):
        """Controls the new chat modal visibility."""
        self.is_new_chat_modal_open = is_open

    def set_user_question(self, question: str):
        """Sets the user_question."""
        self.user_question = question
        
    def add_message_to_current_chat(self, qa_pair: QA):
        """Appends a QA pair to the current chat's message list."""
        if self.current_chat in self._chats:
            self._chats[self.current_chat].append(qa_pair)
        else:
            # Handle error: current chat not found
            print(f"Error: Current chat '{self.current_chat}' not found.")

    def update_last_message_answer(self, answer_chunk: str):
        """Appends answer_chunk to the answer of the last QA pair in the current chat."""
        if self.current_chat in self._chats and self._chats[self.current_chat]:
            self._chats[self.current_chat][-1]["answer"] += answer_chunk
        # self.current_llm_output = "" # Clear the temporary display holder
        # current_llm_output is directly bound to UI, so it updates automatically.
        # We might want to clear it explicitly if the display logic requires it *after* streaming.

    def clear_current_llm_output(self):
        """Sets current_llm_output to an empty string."""
        self.current_llm_output = ""
        
    def request_interrupt(self):
        """Sets the interrupt_requested flag to True."""
        self.interrupt_requested = True

    # Event handlers for settings
    def set_selected_model(self, model_name: str):
        """Sets the selected model string."""
        self.selected_model_str = model_name

    def set_siliconflow_api_key(self, key: str):
        """Sets the SiliconFlow API key."""
        self.api_keys["SILICONFLOW"] = key
        self.api_keys = self.api_keys.copy() # To trigger reactivity if displaying keys

    def set_gemini_api_key(self, key: str):
        """Sets the Gemini API key."""
        self.api_keys["GEMINI"] = key
        self.api_keys = self.api_keys.copy() # To trigger reactivity

    def set_ui_manager_instance(self, ui_manager: UIManager):
        """Sets the UIManager instance."""
        self.ui_manager = ui_manager
        
    async def process_question(self, form_data: dict[str, Any]):
        """
        Processes the user_question by calling the LLM API and handling the response.
        This is an event handler called by the form submission in the UI.
        """
        question = form_data.get('question', self.user_question) # Use form_data or existing user_question
        if not question or not question.strip():
            self.user_question = "" # Clear if only whitespace
            return

        # Add user question to chat immediately
        self.add_message_to_current_chat(QA(question=question, answer=""))
        self.user_question = "" # Clear input field after submission

        self.processing = True
        self.interrupt_requested = False
        self.current_llm_output = "" # Clear any previous streaming output display
        yield # Allow UI to update with processing state and cleared input

        current_model_api = None
        current_response_handler = None
        api_key_to_use = None

        try:
            if not self.selected_model_str:
                self.ui_manager.show_error_info(Exception("No model selected. Please select a model in settings."))
                self.processing = False; yield; return
            
            model_type_enum = ModelType(self.selected_model_str) # Convert string to Enum

            # Determine API client, response handler, and API key based on selected model
            if "SILICONFLOW" in model_type_enum.name: # Check if it's a SiliconFlow model
                api_key_to_use = self.api_keys.get("SILICONFLOW")
                if not api_key_to_use and not os.getenv("SILICONFLOW_API_KEY"): # Check state first, then env
                    self.ui_manager.show_error_info(Exception("SiliconFlow API key not set. Please set it in settings."))
                    self.processing = False; yield; return
                current_model_api = self.ui_manager.siliconflow_api
                current_response_handler = self.ui_manager.siliconflow_response_handler
            elif "GEMINI" in model_type_enum.name: # Check if it's a Gemini model
                api_key_to_use = self.api_keys.get("GEMINI")
                if not api_key_to_use and not os.getenv("GEMINI_API_KEY"): # Check state first, then env
                    self.ui_manager.show_error_info(Exception("Gemini API key not set. Please set it in settings."))
                    self.processing = False; yield; return
                current_model_api = self.ui_manager.gemini_api
                current_response_handler = self.ui_manager.gemini_response_handler
            else:
                self.ui_manager.show_error_info(Exception(f"Model {self.selected_model_str} is not supported by any configured API service."))
                self.processing = False; yield; return

            if not current_model_api or not current_response_handler:
                self.ui_manager.show_error_info(Exception("Selected model API or handler not available."))
                self.processing = False; yield; return

            # LLM Call
            response_stream = await rx.call_blocking(
                current_model_api.ask_LLM,
                query=question,
                model_type=model_type_enum,
                api_key=api_key_to_use # Pass the key to ask_LLM
            )
            
            # Handle Response Stream
            if self.ui_manager:
                await rx.call_blocking(
                    current_response_handler.handle_text_response,
                    response_stream,
                    self.ui_manager,
                    show_reasoning=self.show_long_thinking
                )
            else:
                print("Error: UIManager instance not available in state for response handling.")
                self.add_message_to_current_chat(QA(question="Error", answer="UI manager not available for response."))

        except ValueError: # Handles issues with ModelType(self.selected_model_str)
            self.ui_manager.show_error_info(Exception(f"Invalid model selected: {self.selected_model_str}"))
            self.processing = False; yield; return
        except Exception as e:
            if self.ui_manager:
                self.ui_manager.show_error_info(e) # Use the UIManager's error display
            else:
                print(f"Error in process_question: {e}") # Log if no UI manager
        finally:
            # This will be handled by "display_ends" signal if response_handler calls it.
            # If an exception occurs before/during response_handler call, ensure processing is False.
            if self.processing: # Check if it wasn't already set to False by display_ends
                self.processing = False
                self.current_llm_output = "" # Clear any partial output
            yield


class ReflexUIManager(UIManager):
    def __init__(self): # Removed siliconflow_api_key argument
        super().__init__()
        self.state = ReflexUIManagerState()

        # Initialize all supported model APIs and handlers
        # These can attempt to load keys from env or be initialized without keys,
        # relying on keys passed from self.state.api_keys during ask_LLM call.
        self.siliconflow_api = SiliconflowModelAPI(api_key=os.getenv("SILICONFLOW_API_KEY")) # Initialize with env var as fallback
        self.gemini_api = GeminiModelAPI(api_key=os.getenv("GEMINI_API_KEY")) # Initialize with env var as fallback
        
        self.siliconflow_response_handler = SiliconflowModelResponseHandler()
        self.gemini_response_handler = GeminiModelResponseHandler()

        # Set the UIManager instance in the state, so state can call manager's methods
        # or access its properties (like the model_api instances)
        self.state.set_ui_manager_instance(self)
        # self.state.set_api_clients is no longer needed as the state will use ui_manager
        # to access the specific model API and handler based on selected_model_str.

    @property
    def paused_response_output(self) -> bool:
        """
        Returns whether the response output should be paused, based on Reflex state.
        This overrides the base UIManager property.
        """
        if self.state: # Ensure state is initialized
            return self.state.interrupt_requested
        return False # Default if state is not available

    # The setter from UIManager ABC for _paused_response_output is not strictly needed
    # for ReflexUIManager if interrupt_requested is the sole driver from the UI.
    # However, to fully comply with the ABC, if some internal logic in ReflexUIManager
    # needed to *force* a pause outside of user request, one might implement it.
    # For now, user-driven interruption is via self.state.request_interrupt().

    def show_enter_info(self):
        """Display enter information (e.g., welcome message or initial setup)."""
        # Example: Could set an initial message in the chat or log
        print("Reflex UI Manager: Welcome!")
        # self.state.add_message_to_current_chat(QA(question="System", answer="Welcome to the chat!"))

    def show_exit_info(self):
        """Display exit information."""
        print("Reflex UI Manager: Exiting.")

    def show_error_info(self, e: Exception):
        """Display error information in the chat."""
        error_message = f"An error occurred: {str(e)}"
        print(f"Error displayed in UI: {error_message}") # Also log it
        # Ensure this runs in the event loop if it modifies state that the UI observes
        # For simple state var changes, direct assignment is fine.
        # If it needs to be an event, wrap it.
        self.state.add_message_to_current_chat(QA(question="Error", answer=error_message))
        self.state.processing = False # Ensure processing stops on error

    def display_text_output(self, output: str, **kwargs):
        """Display text output by updating the last message's answer in the state."""
        # This method is called by the response_handler (likely from a non-Reflex thread)
        # It needs to update Reflex state.
        # `update_last_message_answer` should be designed to be callable like this.
        # If `update_last_message_answer` itself needs to be an event or trigger yields,
        # this gets more complex. For now, assume it's a direct state update.
        self.state.update_last_message_answer(output)
        # If current_llm_output is used for *only* streaming part, update it here too.
        # self.state.current_llm_output += output # Or set it if it's the full stream part

    def display_img_output(self):
        """Display image output (placeholder)."""
        self.state.add_message_to_current_chat(QA(question="System", answer="Image output not yet supported."))

    def display_audio_output(self):
        """Display audio output (placeholder)."""
        self.state.add_message_to_current_chat(QA(question="System", answer="Audio output not yet supported."))

    def handle_signal(self, signal: str):
        """Handle signals for display start/end."""
        if signal == "display_starts":
            self.state.processing = True
            self.state.current_llm_output = "" # Clear temporary display area
            self.state.interrupt_requested = False
            print("Signal: display_starts")
        elif signal == "display_ends":
            self.state.processing = False
            # The full response is now in selected_chat_messages[-1].answer
            # current_llm_output was for the streaming part, clear it.
            self.state.current_llm_output = "" 
            if self.state.interrupt_requested:
                self.state.add_message_to_current_chat(QA(question="System", answer="Output interrupted by user."))
                self.state.interrupt_requested = False # Reset flag
            print("Signal: display_ends")

# Main UI Page Function
def reflex_chat_app_page(manager: ReflexUIManager) -> rx.Component:
    """
    Constructs the main UI page for the Reflex chat application.
    Components bind to manager.state for properties and event handlers.
    Event handlers that need access to manager's non-state parts (like model_api directly,
    though we moved it to state) would need manager instance.
    However, typical Reflex pattern is State.method.
    """
    return rx.vstack(
        app_navbar(),       # Navbar component
        chat_display_area(),# Chat messages display area
        chat_input_bar(),   # Input bar for user messages
        # Modals like new_chat_modal are part of app_navbar or sidebar,
        # and their visibility is controlled by manager.state.
        # Example: new_chat_modal() is rendered by app_navbar.
        spacing="0", # Remove spacing between main layout components if desired
        align_items="stretch", # Ensure components stretch to full width
        width="100%",
        height="100vh", # Full viewport height
    )



