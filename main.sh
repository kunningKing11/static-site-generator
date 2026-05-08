#!/bin/bash
uv run src/main.py
cd public && uv run python -m http.server 8888

