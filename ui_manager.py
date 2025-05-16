from abc import ABC, abstractmethod
from typing_extensions import Union
from typing import Dict,List,Callable
import reflex as rx
import keyboard


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
class ReflexUIManager(UIManager):
    def __init__(self):
        super().__init__()
        self.state = rx.State()
        self.state.add_var("example",0)

    @rx.event
    def some_event_trigger(self):
        self.state.example += 1



