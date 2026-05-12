"""
Data Transfer Objects for API requests and responses
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.domain.models import Capture, TimelineEvent, ProcessingJob


# ===== Request DTOs =====

class CreateCaptureRequest(BaseModel):
    title: str
    description: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0


class CaptureSearchRequest(BaseModel):
    query: str
    limit: int = 10


# ===== Response DTOs =====

class CreateCaptureResponse(BaseModel):
    capture_id: str
    title: str
    status: str
    created_at: datetime
    description: Optional[str] = None

    @classmethod
    def from_capture(cls, capture: Capture) -> "CreateCaptureResponse":
        return cls(
            capture_id=capture.id,
            title=capture.title,
            status=capture.status.value,
            created_at=capture.created_at,
            description=capture.description
        )


class UploadResponse(BaseModel):
    capture_id: str
    filename: str
    file_path: str
    status: str
    image_id: Optional[str] = None


class JobStatus(BaseModel):
    job_id: str
    job_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class StatusResponse(BaseModel):
    capture_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    jobs: List[JobStatus]

    @classmethod
    def from_capture_and_jobs(
        cls, 
        capture: Capture, 
        jobs: List[ProcessingJob]
    ) -> "StatusResponse":
        return cls(
            capture_id=capture.id,
            status=capture.status.value,
            created_at=capture.created_at,
            updated_at=capture.updated_at,
            jobs=[
                JobStatus(
                    job_id=job.id,
                    job_type=job.job_type,
                    status=job.status.value,
                    created_at=job.created_at,
                    updated_at=job.updated_at,
                    completed_at=job.completed_at,
                    result=job.result,
                    error_message=job.error_message
                )
                for job in jobs
            ]
        )


class TimelineEventDTO(BaseModel):
    timestamp: float
    event_type: str
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class TimelineResponse(BaseModel):
    capture_id: str
    events: List[TimelineEventDTO]

    @classmethod
    def from_events(
        cls, 
        capture_id: str, 
        events: List[TimelineEvent]
    ) -> "TimelineResponse":
        return cls(
            capture_id=capture_id,
            events=[
                TimelineEventDTO(
                    timestamp=event.timestamp,
                    event_type=event.event_type,
                    content=event.content,
                    metadata=event.metadata,
                    created_at=event.created_at
                )
                for event in events
            ]
        )


class ProcessJobDTO(BaseModel):
    job_id: str
    type: str
    task_id: str


class ProcessResponse(BaseModel):
    capture_id: str
    status: str
    jobs: List[ProcessJobDTO]


class DeleteResponse(BaseModel):
    capture_id: str
    status: str


class SearchResultDTO(BaseModel):
    capture_id: str
    content_type: str  # "transcription" or "image"
    content_id: str
    text: str
    timestamp: Optional[float] = None
    score: Optional[float] = None


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultDTO]
    total: int
    limit: int
    offset: int


class CaptureSearchResponse(BaseModel):
    capture_id: str
    query: str
    results: List[SearchResultDTO]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"