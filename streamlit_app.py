"""Streamlit entrypoint for Streamlit Cloud and CLI convenience.

This file simply imports the packaged application module which runs the
Streamlit UI on import. Streamlit Cloud will use this file as the app entrypoint.
"""

import app.app  # noqa: F401  # module import triggers Streamlit app initialization
