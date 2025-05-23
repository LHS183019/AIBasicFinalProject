import reflex as rx
from ..ui_manager import ReflexUIManagerState, QA # Assuming ui_manager.py is in the parent directory

def render_qa_message(qa: QA) -> rx.Component:
    """Displays a single question and its corresponding answer."""
    return rx.box(
        rx.box(
            rx.markdown(qa.question),
            text_align="right",  # User messages on the right
            bg="lightblue",
            padding="0.5em",
            border_radius="md",
            margin_bottom="0.5em",
        ),
        rx.box(
            rx.markdown(qa.answer),
            text_align="left",  # AI messages on the left
            bg="lightgreen",
            padding="0.5em",
            border_radius="md",
        ),
        width="100%",
        padding_y="0.5em",
    )

def chat_display_area() -> rx.Component:
    """Displays the chat messages and the current LLM output."""
    return rx.box(
        rx.vstack(
            rx.foreach(
                ReflexUIManagerState.selected_chat_messages,
                render_qa_message,
            ),
            # Display streaming LLM output
            rx.cond(
                ReflexUIManagerState.current_llm_output != "",
                rx.box(
                    rx.markdown(ReflexUIManagerState.current_llm_output),
                    text_align="left",
                    bg="lightyellow", # Different background for streaming
                    padding="0.5em",
                    border_radius="md",
                    margin_top="0.5em",
                )
            ),
            align_items="stretch", # Make messages take full width
            width="100%",
        ),
        width="100%",
        height="70vh", # Example height, adjust as needed
        overflow_y="auto", # Make it scrollable
        border="1px solid #ddd",
        padding="1em",
        on_mount=rx.call_script("this.scrollTop = this.scrollHeight") # Auto-scroll to bottom
        # TODO: For true auto-scroll on new message, need a more dynamic way.
        # Reflex's rx.auto_scroll might be better if it works with rx.foreach updates.
        # For now, this scrolls on mount. A custom script or a different component structure might be needed for continuous auto-scroll.
    )
