import reflex as rx
from ..ui_manager import ReflexUIManagerState # Assuming ui_manager.py is in the parent directory

def chat_input_bar() -> rx.Component:
    """
    Creates the input bar for chat, including text input, send button,
    and an interrupt button.
    """
    return rx.form(
        rx.hstack(
            rx.input(
                placeholder="Type your message...",
                id="question", # For form submission data
                value=ReflexUIManagerState.user_question,
                on_change=ReflexUIManagerState.set_user_question,
                flex_grow=1,
                disabled=ReflexUIManagerState.processing,
            ),
            rx.button(
                "Send",
                type="submit", # Important for form submission
                loading=ReflexUIManagerState.processing,
                disabled=rx.cond(
                    ReflexUIManagerState.processing | (ReflexUIManagerState.user_question.strip() == ""),
                    True,
                    False
                ),
            ),
            rx.cond(
                ReflexUIManagerState.processing,
                rx.button(
                    "Interrupt",
                    on_click=ReflexUIManagerState.request_interrupt,
                    color_scheme="red",
                )
            ),
            align_items="center",
            width="100%",
        ),
        on_submit=ReflexUIManagerState.process_question, # Correct handler for form
        width="100%",
        # Prevent form submission from reloading the page (Reflex handles state)
        # This is typically default behavior in Reflex when on_submit is a State method.
        # If issues arise, add: on_submit=lambda data: ReflexUIManagerState.process_question(data)
        # and ensure process_question can handle the form data dict if needed,
        # or simply call it without arguments if it uses self.user_question.
        # For now, ReflexUIManagerState.process_question will use self.user_question.
        # We also need to clear the user_question after submit, which should be done in process_question or an event chain.
        # Resetting user_question will be handled within process_question or a subsequent event.
        reset_on_submit=False # We handle reset manually in process_question
    )
