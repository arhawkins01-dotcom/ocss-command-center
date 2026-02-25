import sys
import os

# Ensure repository root is first on sys.path during pytest collection so
# `from app import ...` resolves to the package in this workspace.
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
