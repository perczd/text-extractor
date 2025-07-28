#!/usr/bin/env bash
set -o errexit

echo "Installing Python dependencies..."
python -m pip install --user -r requirements.txt

echo "Skipping system package installs (Render restrictions)"
echo "Tesseract path: $(which tesseract)"
