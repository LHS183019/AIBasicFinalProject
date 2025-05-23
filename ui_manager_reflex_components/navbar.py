import reflex as rx
from ..ui_manager import ReflexUIManagerState # Assuming ui_manager.py is in the parent directory
# We need to import the sidebar to pass its trigger to the navbar.
from .sidebar import chat_management_sidebar
# Import new_chat_modal from settings_modals
from .settings_modals import new_chat_modal

def app_navbar() -> rx.Component:
    """
    The main application navigation bar.
    Includes current chat display, and buttons for new chat and sidebar.
    """
    # Define the trigger for the sidebar first
    sidebar_trigger = rx.icon_button(rx.icon("menu"), size="lg", variant="ghost")
    
    return rx.hstack(
        # Hamburger menu to open the chat management sidebar
        chat_management_sidebar(trigger=sidebar_trigger), # Sidebar is now part of the hstack

        # Display current chat name
        rx.badge(
            ReflexUIManagerState.current_chat,
            color_scheme="accent", # Use accent color for consistency
            variant="solid",
            size="2",
            padding_x="1em",
        ),
        
        rx.spacer(), # Pushes items to the sides
        
        # Button to open the new chat modal
        rx.icon_button(
            rx.icon("plus-circle"),
            on_click=lambda: ReflexUIManagerState.set_is_new_chat_modal_open(True),
            size="lg",
            variant="ghost",
        ),
        
        # Placeholder for settings/model selection trigger
        # rx.icon_button(
        #     rx.icon("settings"),
        #     # on_click=... # Needs a state variable and modal for settings
        #     size="lg",
        #     variant="ghost",
        #     disabled=True, # For now
        # ),

        # The new_chat_modal itself (it's hidden until its 'open' state is true)
        new_chat_modal(), # No trigger needed here as visibility is state-controlled

        align_items="center",
        justify_content="space-between", # Ensure items are spaced out
        padding_x="1em",
        padding_y="0.5em",
        border_bottom=f"1px solid {rx.color('mauve', 5)}", # Theme-aware border
        width="100%",
        position="sticky", # Make navbar sticky
        top="0",
        z_index="1000", # Ensure it's above other content, increased z-index
        bg=rx.theme_var("colors.panel_solid"), # Theme-aware background
    )
