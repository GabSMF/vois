"""Simple application settings and configuration."""

import os
from pathlib import Path


API_V1_PREFIX = "/api/v1"
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
TITLE = "Vois Capture API Gateway"
DESCRIPTION = "Simple multimedia capture service"
VERSION = "1.0.0"

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "8000"))

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/mp3", "audio/m4a"]
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
