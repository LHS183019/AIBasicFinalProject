import reflex as rx
from ..ui_manager import ReflexUIManagerState # Assuming ui_manager.py is in the parent directory
from ..model_API import ModelType # Import ModelType for dropdown

# --- Modals ---

def new_chat_modal() -> rx.Component:
    """
    A modal dialog to create a new chat.
    Visibility is controlled by ReflexUIManagerState.is_new_chat_modal_open.
    """
    return rx.dialog.root(
        # Trigger is managed externally by buttons that set is_new_chat_modal_open to True
        rx.dialog.content(
            rx.dialog.title("Create New Chat"),
            rx.dialog.description(
                "Enter a name for your new chat session."
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Chat Name",
                        name="new_chat_name", # Used by form_data in create_chat
                        id="new_chat_name_modal_input", # Unique ID
                    ),
                    rx.hstack(
                        rx.dialog.close( # Button to close the dialog
                            rx.button(
                                "Cancel",
                                color_scheme="gray",
                                variant="soft",
                                # No explicit on_click needed if it just closes, 
                                # but good to ensure state is updated if user cancels via ESC or overlay click
                                on_click=lambda: ReflexUIManagerState.set_is_new_chat_modal_open(False)
                            )
                        ),
                        rx.button("Create", type="submit"), # Form submission
                        spacing="3",
                        margin_top="1em",
                        justify="end",
                    ),
                    align_items="stretch",
                ),
                on_submit=ReflexUIManagerState.create_chat,
                # reset_on_submit=True, # Reflex handles this
            ),
        ),
        open=ReflexUIManagerState.is_new_chat_modal_open,
        on_open_change=ReflexUIManagerState.set_is_new_chat_modal_open, # Syncs state if closed via ESC/overlay
    )

# --- Placeholder Components for Settings ---

def model_selection_dropdown() -> rx.Component:
    """
    Provides a dropdown for selecting the language model.
    """
    # Prepare items for rx.select from ModelType enum
    # Each item is a tuple (label, value)
    model_options = [(model.name.replace("_", " ").title(), model.value) for model in ModelType]

    return rx.vstack(
        rx.text("Model Selection:", weight="medium"),
        rx.select(
            model_options, # Use dynamically generated options
            placeholder="Select a Model",
            value=ReflexUIManagerState.selected_model_str,
            on_change=ReflexUIManagerState.set_selected_model, # Use the new handler
            width="100%", # Ensure select takes full width of its container
        ),
        align_items="start", # Align text label to the start
        width="100%",
    )

def api_key_management_section() -> rx.Component:
    """
    Provides input fields for managing API keys for different services.
    """
    return rx.vstack(
        rx.text("API Key Management:", weight="medium", margin_bottom="0.5em"),
        rx.input(
            placeholder="SiliconFlow API Key",
            value=ReflexUIManagerState.api_keys.get("SILICONFLOW", ""), # Display current key
            on_change=ReflexUIManagerState.set_siliconflow_api_key, # Update on change
            type="password",
            width="100%",
            margin_bottom="0.5em",
        ),
        rx.input(
            placeholder="Gemini API Key",
            value=ReflexUIManagerState.api_keys.get("GEMINI", ""), # Display current key
            on_change=ReflexUIManagerState.set_gemini_api_key, # Update on change
            type="password",
            width="100%",
        ),
        align_items="start", # Align text label and inputs to the start
        width="100%",
    )

def general_settings_modal() -> rx.Component:
    """
    A modal for general settings, including model selection and API keys.
    (This is an example of how you might group settings)
    """
    # For now, this modal is not explicitly used but shows how placeholders can be grouped.
    # You would need a state variable like `is_settings_modal_open` to control it.
    return rx.dialog.root(
        # rx.dialog.trigger(rx.button("Open Settings")), # Example trigger
        rx.dialog.content(
            rx.dialog.title("Settings"),
            rx.vstack(
                model_selection_dropdown(),
                rx.divider(width="100%", margin_y="1em"),
                api_key_management_section(),
                rx.hstack(
                    rx.dialog.close(rx.button("Done", color_scheme="blue")),
                    justify="end",
                    margin_top="1em",
                    width="100%",
                ),
                spacing="4",
                align_items="stretch",
            ),
        ),
        # open=ReflexUIManagerState.is_settings_modal_open, # Example state binding
        # on_open_change=ReflexUIManagerState.set_is_settings_modal_open, # Example state binding
    )
