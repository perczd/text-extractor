#!/usr/bin/env bash
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Tesseract path: $(which tesseract)"
