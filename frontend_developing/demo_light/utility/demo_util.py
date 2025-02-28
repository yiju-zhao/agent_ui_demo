import streamlit as st
from typing import List, Callable


def render_button_grid(
    items: List[str],
    key_suffix: str,
    callback: Callable[[str], None],
    session_state: dict,
    selected_key: str,
    num_columns: int = 2,
):
    """Render a grid of buttons with selection state.

    Args:
        items: List of strings to render as buttons
        key_suffix: Suffix for button keys
        callback: Function to call when button is clicked
        session_state: Streamlit session state
        selected_key: Key to store selected item in session state
        num_columns: Number of columns in the grid
    """
    columns = st.columns(num_columns)
    chunk_size = (len(items) + num_columns - 1) // num_columns

    for i, col in enumerate(columns):
        with col:
            start = i * chunk_size
            end = (i + 1) * chunk_size
            for item in items[start:end]:
                is_selected = session_state.get(selected_key) == item
                if st.button(
                    item,
                    key=f"{item}_{key_suffix}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                ):
                    # Let the callback handle the toggle logic
                    callback(item)
