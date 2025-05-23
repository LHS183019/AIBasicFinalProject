import reflex as rx
from ..ui_manager import ReflexUIManagerState, QA # Assuming ui_manager.py is in the parent directory

def render_qa_message(qa: QA) -> rx.Component:
    """Displays a single question and its corresponding answer."""
    return rx.box( # Outer box for each Q-A pair, helps with alignment if needed
        rx.box( # User question bubble
            rx.markdown(qa.question, component_map={"p": lambda text: rx.text(text, margin_bottom="0")}), # Remove default p margin
            text_align="left", # Align text within the bubble to the left
            bg="lightblue", # Using specified colors
            padding_x="1em", 
            padding_y="0.5em",
            border_radius="md", # "8px" is similar to "md"
            max_width="70%",
            float="right", # Make the bubble float to the right
            margin_y="0.25em", # Small margin between Q and A if they are close
            clear="both", # Ensure it doesn't wrap around other floated elements
        ),
        rx.box( # AI answer bubble
            rx.markdown(qa.answer, component_map={"p": lambda text: rx.text(text, margin_bottom="0")}),
            text_align="left",
            bg="lightgreen",
            padding_x="1em",
            padding_y="0.5em",
            border_radius="md",
            max_width="70%",
            float="left", # Make the bubble float to the left
            margin_y="0.25em",
            clear="both",
        ),
        width="100%", # Ensure the container for Q&A takes full width for float context
        display="block", # Using block to contain floats
        padding_y="0", # Padding is on individual bubbles now
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
                    rx.markdown(ReflexUIManagerState.current_llm_output, component_map={"p": lambda text: rx.text(text, margin_bottom="0")}),
                    text_align="left",
                    bg="lightyellow", 
                    padding_x="1em",
                    padding_y="0.5em",
                    border_radius="md",
                    max_width="70%", # Consistent max_width
                    align_self="flex-start", # Align to left like other AI messages
                    # margin_top will be handled by vstack spacing
                )
            ),
            align_items="stretch", 
            width="100%",
            spacing="0.5em", # Add spacing between messages in the vstack
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
