"""
Infrastructure implementations - concrete classes only.
"""
from typing import Optional, List, Dict
from datetime import datetime
import uuid
import os
from pathlib import Path

from app.domain.models import (
    Capture, CaptureImage, TimelineEvent,
    Transcription, ProcessingJob, SearchResult, CaptureStatus, ProcessingStatus
)


class InMemoryCaptureRepository:
    """In-memory implementation of capture repository."""

    def __init__(self):
        self._captures: Dict[str, Capture] = {}

    async def create(self, title: str, description: Optional[str] = None) -> Capture:
        capture_id = str(uuid.uuid4())
        capture = Capture(
            id=capture_id,
            title=title,
            status=CaptureStatus.CREATED,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            description=description
        )
        self._captures[capture_id] = capture
        return capture

    async def get(self, capture_id: str) -> Optional[Capture]:
        return self._captures.get(capture_id)

    async def update(self, capture: Capture) -> Capture:
        capture.updated_at = datetime.utcnow()
        self._captures[capture.id] = capture
        return capture

    async def delete(self, capture_id: str) -> bool:
        if capture_id in self._captures:
            del self._captures[capture_id]
            return True
        return False

    async def update_status(self, capture_id: str, status: str) -> Capture:
        capture = self._captures.get(capture_id)
        if capture:
            capture.status = CaptureStatus(status)
            capture.updated_at = datetime.utcnow()
            return capture
        raise ValueError(f"Capture {capture_id} not found")


class InMemoryImageRepository:
    """In-memory implementation of image repository."""

    def __init__(self):
        self._images: Dict[str, CaptureImage] = {}
        self._by_capture: Dict[str, List[str]] = {}

    async def create(
        self,
        capture_id: str,
        file_path: str,
        timestamp: Optional[float] = None,
        description: Optional[str] = None
    ) -> CaptureImage:
        image_id = str(uuid.uuid4())
        image = CaptureImage(
            id=image_id,
            capture_id=capture_id,
            file_path=file_path,
            created_at=datetime.utcnow(),
            timestamp=timestamp,
            description=description
        )
        self._images[image_id] = image

        if capture_id not in self._by_capture:
            self._by_capture[capture_id] = []
        self._by_capture[capture_id].append(image_id)

        return image

    async def get(self, image_id: str) -> Optional[CaptureImage]:
        return self._images.get(image_id)

    async def get_by_capture(self, capture_id: str) -> List[CaptureImage]:
        image_ids = self._by_capture.get(capture_id, [])
        return [self._images[image_id] for image_id in image_ids if image_id in self._images]

    async def delete(self, image_id: str) -> bool:
        if image_id in self._images:
            image = self._images[image_id]
            if image.capture_id in self._by_capture:
                self._by_capture[image.capture_id].remove(image_id)
            del self._images[image_id]
            return True
        return False


class InMemoryTimelineRepository:
    """In-memory implementation of timeline repository."""

    def __init__(self):
        self._events: Dict[str, TimelineEvent] = {}
        self._by_capture: Dict[str, List[str]] = {}

    async def create(
        self,
        capture_id: str,
        timestamp: float,
        event_type: str,
        content: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> TimelineEvent:
        event_id = str(uuid.uuid4())
        event = TimelineEvent(
            id=event_id,
            capture_id=capture_id,
            timestamp=timestamp,
            event_type=event_type,
            created_at=datetime.utcnow(),
            content=content,
            metadata=metadata
        )
        self._events[event_id] = event

        if capture_id not in self._by_capture:
            self._by_capture[capture_id] = []
        self._by_capture[capture_id].append(event_id)

        return event

    async def get_by_capture(self, capture_id: str) -> List[TimelineEvent]:
        event_ids = self._by_capture.get(capture_id, [])
        return [self._events[event_id] for event_id in event_ids if event_id in self._events]

    async def delete_by_capture(self, capture_id: str) -> bool:
        if capture_id in self._by_capture:
            for event_id in self._by_capture[capture_id]:
                if event_id in self._events:
                    del self._events[event_id]
            del self._by_capture[capture_id]
            return True
        return False


class InMemoryTranscriptionRepository:
    """In-memory implementation of transcription repository."""

    def __init__(self):
        self._transcriptions: Dict[str, Transcription] = {}
        self._by_capture: Dict[str, List[str]] = {}

    async def create(
        self,
        capture_id: str,
        text: str,
        language: str = "en",
        confidence: Optional[float] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> Transcription:
        transcription_id = str(uuid.uuid4())
        transcription = Transcription(
            id=transcription_id,
            capture_id=capture_id,
            text=text,
            created_at=datetime.utcnow(),
            language=language,
            confidence=confidence,
            start_time=start_time,
            end_time=end_time
        )
        self._transcriptions[transcription_id] = transcription

        if capture_id not in self._by_capture:
            self._by_capture[capture_id] = []
        self._by_capture[capture_id].append(transcription_id)

        return transcription

    async def get_by_capture(self, capture_id: str) -> List[Transcription]:
        transcription_ids = self._by_capture.get(capture_id, [])
        return [self._transcriptions[t_id] for t_id in transcription_ids if t_id in self._transcriptions]

    async def delete_by_capture(self, capture_id: str) -> bool:
        if capture_id in self._by_capture:
            for transcription_id in self._by_capture[capture_id]:
                if transcription_id in self._transcriptions:
                    del self._transcriptions[transcription_id]
            del self._by_capture[capture_id]
            return True
        return False


class InMemoryProcessingJobRepository:
    """In-memory implementation of processing job repository."""

    def __init__(self):
        self._jobs: Dict[str, ProcessingJob] = {}
        self._by_capture: Dict[str, List[str]] = {}

    async def create(
        self,
        capture_id: str,
        job_type: str,
        celery_task_id: Optional[str] = None
    ) -> ProcessingJob:
        job_id = str(uuid.uuid4())
        job = ProcessingJob(
            id=job_id,
            capture_id=capture_id,
            job_type=job_type,
            status=ProcessingStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            celery_task_id=celery_task_id
        )
        self._jobs[job_id] = job

        if capture_id not in self._by_capture:
            self._by_capture[capture_id] = []
        self._by_capture[capture_id].append(job_id)

        return job

    async def get(self, job_id: str) -> Optional[ProcessingJob]:
        return self._jobs.get(job_id)

    async def get_by_capture(self, capture_id: str) -> List[ProcessingJob]:
        job_ids = self._by_capture.get(capture_id, [])
        return [self._jobs[job_id] for job_id in job_ids if job_id in self._jobs]

    async def update_status(self, job_id: str, status: str) -> ProcessingJob:
        job = self._jobs.get(job_id)
        if job:
            job.status = ProcessingStatus(status)
            job.updated_at = datetime.utcnow()
            return job
        raise ValueError(f"Job {job_id} not found")

    async def update_result(
        self,
        job_id: str,
        status: str,
        result: Optional[dict] = None,
        error_message: Optional[str] = None
    ) -> ProcessingJob:
        job = self._jobs.get(job_id)
        if job:
            job.status = ProcessingStatus(status)
            job.result = result
            job.error_message = error_message
            job.updated_at = datetime.utcnow()
            if status == "completed":
                job.completed_at = datetime.utcnow()
            return job
        raise ValueError(f"Job {job_id} not found")

    async def delete_by_capture(self, capture_id: str) -> bool:
        if capture_id in self._by_capture:
            for job_id in self._by_capture[capture_id]:
                if job_id in self._jobs:
                    del self._jobs[job_id]
            del self._by_capture[capture_id]
            return True
        return False


class InMemorySearchService:
    """In-memory implementation of search service (no-op)."""

    async def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[SearchResult], int]:
        return [], 0

    async def search_capture(
        self,
        capture_id: str,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        return []

    async def index_transcription(
        self,
        capture_id: str,
        transcription_id: str,
        text: str
    ) -> str:
        return transcription_id

    async def index_image(
        self,
        capture_id: str,
        image_id: str,
        description: str
    ) -> str:
        return image_id

    async def delete_capture_documents(self, capture_id: str) -> bool:
        return True


class LocalFileService:
    """Local filesystem implementation of file service."""

    def __init__(self, base_dir: str = "./uploads"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self,
        file_data: bytes,
        file_name: str,
        file_type: str
    ) -> str:
        if file_type == "audio":
            extension = ".mp3"
        elif file_type == "image":
            extension = ".jpg"
        else:
            extension = ".bin"

        unique_name = f"{file_name}_{uuid.uuid4().hex}{extension}"
        file_path = self.base_dir / unique_name

        with open(file_path, "wb") as f:
            f.write(file_data)

        return str(file_path)

    async def delete_file(self, file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    async def get_file(self, file_path: str) -> Optional[bytes]:
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception:
            return None


class NoOpProcessingService:
    """No-op processing service."""

    async def queue_transcription(self, capture_id: str) -> str:
        return f"transcription_{capture_id}_{uuid.uuid4().hex}"

    async def queue_image_processing(self, capture_id: str) -> str:
        return f"image_processing_{capture_id}_{uuid.uuid4().hex}"

    async def queue_translation_review(self, capture_id: str) -> str:
        return f"translation_review_{capture_id}_{uuid.uuid4().hex}"

    async def get_task_status(self, task_id: str) -> dict:
        return {
            "task_id": task_id,
            "status": "completed",
            "result": None,
            "error": None
        }


def create_in_memory_repositories():
    return {
        "capture_repository": InMemoryCaptureRepository(),
        "image_repository": InMemoryImageRepository(),
        "timeline_repository": InMemoryTimelineRepository(),
        "transcription_repository": InMemoryTranscriptionRepository(),
        "processing_job_repository": InMemoryProcessingJobRepository(),
        "search_service": InMemorySearchService(),
        "file_service": LocalFileService(),
        "processing_service": NoOpProcessingService(),
    }
