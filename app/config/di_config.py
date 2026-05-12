"""Simple service wiring using module-level instances."""
from app.infrastructure.implementations import create_in_memory_repositories


implementations = create_in_memory_repositories()

capture_repository = implementations["capture_repository"]
image_repository = implementations["image_repository"]
timeline_repository = implementations["timeline_repository"]
transcription_repository = implementations["transcription_repository"]
processing_job_repository = implementations["processing_job_repository"]
search_service = implementations["search_service"]
file_service = implementations["file_service"]
processing_service = implementations["processing_service"]
