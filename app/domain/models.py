"""
Domain models - core business entities
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class CaptureStatus(Enum):
    CREATED = "created"
    AUDIO_UPLOADED = "audio_uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Capture:
    id: str
    title: str
    status: CaptureStatus
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None


@dataclass
class CaptureImage:
    id: str
    capture_id: str
    file_path: str
    created_at: datetime
    timestamp: Optional[float] = None
    description: Optional[str] = None


@dataclass
class TimelineEvent:
    id: str
    capture_id: str
    timestamp: float
    event_type: str
    created_at: datetime
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Transcription:
    id: str
    capture_id: str
    text: str
    created_at: datetime
    language: str = "en"
    confidence: Optional[float] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None


@dataclass
class ProcessingJob:
    id: str
    capture_id: str
    job_type: str
    status: ProcessingStatus
    created_at: datetime
    updated_at: datetime
    celery_task_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


@dataclass
class SearchResult:
    capture_id: str
    content_type: str  # "transcription" or "image"
    content_id: str
    text: str
    timestamp: Optional[float] = None
    score: Optional[float] = None