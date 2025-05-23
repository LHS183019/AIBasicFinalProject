import reflex as rx
from ..ui_manager import ReflexUIManagerState # Assuming ui_manager.py is in the parent directory
# Import modals and settings components
from .settings_modals import new_chat_modal, model_selection_dropdown, api_key_management_section

# --- Sidebar Components ---

def sidebar_chat_item(chat_name: str) -> rx.Component:
    """Displays a single chat item in the sidebar."""
    return rx.hstack(
        rx.button(
            chat_name,
            on_click=lambda: [
                ReflexUIManagerState.set_chat(chat_name),
                # rx.set_value(ReflexUIManagerState.drawer_open, False) # Close drawer - need state var for drawer
            ],
            variant="ghost", # Less obtrusive look
            is_active=ReflexUIManagerState.current_chat == chat_name,
            flex_grow=1,
            justify_content="start", # Align text to the left
        ),
        rx.icon_button(
            rx.icon("trash-2"),
            on_click=lambda: ReflexUIManagerState.delete_chat(chat_name),
            color_scheme="red",
            variant="ghost",
        ),
        width="100%",
        padding_x="0.5em",
        # Highlight if current chat
        bg=rx.cond(ReflexUIManagerState.current_chat == chat_name, "lightblue", "transparent"),
    )

def chat_management_sidebar(trigger: rx.Component) -> rx.Component:
    """
    A drawer sidebar for managing chats.
    The 'trigger' argument is a component that will open this drawer.
    """
    return rx.drawer.root(
        rx.drawer.trigger(trigger), # The component that opens the drawer
        rx.drawer.overlay(), # Dims the background
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.drawer.header(
                        rx.text("Chat Sessions", size="5", weight="bold")
                    ),
                    rx.button(
                        "New Chat",
                        on_click=lambda: ReflexUIManagerState.set_is_new_chat_modal_open(True),
                        width="100%",
                        margin_bottom="1em",
                    ),
                    rx.scroll_area(
                        rx.vstack(
                            rx.foreach(
                                ReflexUIManagerState.chat_titles,
                                sidebar_chat_item,
                            ),
                            align_items="stretch",
                            width="100%",
                        ),
                        type="auto", 
                        scrollbars="vertical",
                        style={"height": "70vh"} # Example height
                    ),
                    # Use imported Model Selection & API Keys components
                    rx.heading("Settings", size="4", margin_top="1em", padding_x="0.5em"),
                    model_selection_dropdown(),
                    api_key_management_section(),
                    
                    rx.drawer.footer(
                        # rx.button("Close", on_click=rx.drawer.close()) # Standard way to close drawer
                        # The drawer does not have a rx.drawer.close() component directly,
                        # it's usually a button that when clicked would set a state var that controls drawer's open prop.
                        # However, Reflex's drawer might handle this internally if the button is inside rx.drawer.close_button
                        # For now, let's assume the drawer is closed by clicking outside or via a dedicated close button if one exists.
                        # If a state variable controls the drawer's open state (e.g., `drawer_open`),
                        # then a close button would set `drawer_open` to `False`.
                        # For simplicity, we rely on clicking the overlay or an explicit close button if added.
                        # The chat_management_sidebar doesn't currently have its own open/close state variable in ReflexUIManagerState.
                        # This is usually handled by the `rx.drawer.root` and `rx.drawer.trigger`.
                        # A dedicated close button could be added:
                        rx.button("Close Drawer", on_click=rx.drawer.close()) # This should work if placed correctly
                    ),
                    align_items="stretch",
                    spacing="3",
                    padding="1em",
                    height="100%",
                ),
                # direction="left", # Default is left
            )
        )
    )
