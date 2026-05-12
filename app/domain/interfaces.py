"""
Abstract interfaces - contracts for repositories and services
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict, Any
from app.domain.models import (
    Capture, CaptureImage, TimelineEvent, Transcription,
    ProcessingJob, SearchResult
)


class CaptureRepository(ABC):
    @abstractmethod
    async def create(self, title: str, description: Optional[str] = None) -> Capture:
        pass

    @abstractmethod
    async def get(self, capture_id: str) -> Optional[Capture]:
        pass

    @abstractmethod
    async def update(self, capture: Capture) -> Capture:
        pass

    @abstractmethod
    async def delete(self, capture_id: str) -> bool:
        pass

    @abstractmethod
    async def update_status(self, capture_id: str, status: str) -> Capture:
        pass


class ImageRepository(ABC):
    @abstractmethod
    async def create(
        self,
        capture_id: str,
        file_path: str,
        timestamp: Optional[float] = None,
        description: Optional[str] = None
    ) -> CaptureImage:
        pass

    @abstractmethod
    async def get(self, image_id: str) -> Optional[CaptureImage]:
        pass

    @abstractmethod
    async def get_by_capture(self, capture_id: str) -> List[CaptureImage]:
        pass

    @abstractmethod
    async def delete(self, image_id: str) -> bool:
        pass


class TimelineRepository(ABC):
    @abstractmethod
    async def create(
        self,
        capture_id: str,
        timestamp: float,
        event_type: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TimelineEvent:
        pass

    @abstractmethod
    async def get_by_capture(self, capture_id: str) -> List[TimelineEvent]:
        pass

    @abstractmethod
    async def delete_by_capture(self, capture_id: str) -> bool:
        pass


class TranscriptionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        capture_id: str,
        text: str,
        language: str = "en",
        confidence: Optional[float] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> Transcription:
        pass

    @abstractmethod
    async def get_by_capture(self, capture_id: str) -> List[Transcription]:
        pass

    @abstractmethod
    async def delete_by_capture(self, capture_id: str) -> bool:
        pass


class ProcessingJobRepository(ABC):
    @abstractmethod
    async def create(
        self,
        capture_id: str,
        job_type: str,
        celery_task_id: Optional[str] = None
    ) -> ProcessingJob:
        pass

    @abstractmethod
    async def get(self, job_id: str) -> Optional[ProcessingJob]:
        pass

    @abstractmethod
    async def get_by_capture(self, capture_id: str) -> List[ProcessingJob]:
        pass

    @abstractmethod
    async def update_status(self, job_id: str, status: str) -> ProcessingJob:
        pass

    @abstractmethod
    async def update_result(
        self,
        job_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> ProcessingJob:
        pass

    @abstractmethod
    async def delete_by_capture(self, capture_id: str) -> bool:
        pass


class SearchService(ABC):
    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[SearchResult], int]:
        pass

    @abstractmethod
    async def search_capture(
        self,
        capture_id: str,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        pass

    @abstractmethod
    async def index_transcription(
        self,
        capture_id: str,
        transcription_id: str,
        text: str
    ) -> str:
        pass

    @abstractmethod
    async def index_image(
        self,
        capture_id: str,
        image_id: str,
        description: str
    ) -> str:
        pass

    @abstractmethod
    async def delete_capture_documents(self, capture_id: str) -> bool:
        pass


class FileService(ABC):
    @abstractmethod
    async def save_file(
        self,
        file_data: bytes,
        file_name: str,
        file_type: str
    ) -> str:
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        pass

    @abstractmethod
    async def get_file(self, file_path: str) -> Optional[bytes]:
        pass


class ProcessingService(ABC):
    @abstractmethod
    async def queue_transcription(self, capture_id: str) -> str:
        pass

    @abstractmethod
    async def queue_image_processing(self, capture_id: str) -> str:
        pass

    @abstractmethod
    async def queue_translation_review(self, capture_id: str) -> str:
        pass

    @abstractmethod
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        pass