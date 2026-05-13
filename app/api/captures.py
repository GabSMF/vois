from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.dto import (
    CreateCaptureRequest, CreateCaptureResponse,
    UploadResponse, StatusResponse, TimelineResponse,
    ProcessResponse, DeleteResponse
)
from app.config.di_config import (
    capture_repository,
    image_repository,
    timeline_repository,
    transcription_repository,
    processing_job_repository,
    file_service,
    processing_service
)
from app.config import settings

router = APIRouter()


@router.post("/", response_model=CreateCaptureResponse)
async def create_capture(request: CreateCaptureRequest):
    """Create a new capture."""
    try:
        capture = await capture_repository.create(
            title=request.title,
            description=request.description
        )
        return CreateCaptureResponse.from_capture(capture)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{capture_id}/audio", response_model=UploadResponse)
async def upload_audio(capture_id: str, file: UploadFile = File(...)):
    """Upload audio file for a capture."""
    if file.content_type not in settings.ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_AUDIO_TYPES)}"
        )

    if hasattr(file, 'size') and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE} bytes"
        )

    try:
        capture = await capture_repository.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        file_data = await file.read()
        file_path = await file_service.save_file(
            file_data=file_data,
            file_name=file.filename,
            file_type="audio"
        )

        await capture_repository.update_status(capture_id, "audio_uploaded")

        return UploadResponse(
            capture_id=capture_id,
            filename=file.filename,
            file_path=file_path,
            status="audio uploaded"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{capture_id}/images", response_model=UploadResponse)
async def upload_image(capture_id: str, file: UploadFile = File(...)):
    """Upload image file for a capture."""
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )

    if hasattr(file, 'size') and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE} bytes"
        )

    try:
        capture = await capture_repository.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        file_data = await file.read()
        file_path = await file_service.save_file(
            file_data=file_data,
            file_name=file.filename,
            file_type="image"
        )

        image = await image_repository.create(
            capture_id=capture_id,
            file_path=file_path,
            description=f"Uploaded image: {file.filename}"
        )

        return UploadResponse(
            capture_id=capture_id,
            filename=file.filename,
            file_path=file_path,
            status="image uploaded",
            image_id=image.id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{capture_id}/status", response_model=StatusResponse)
async def get_status(capture_id: str):
    """Get capture processing status."""
    try:
        capture = await capture_repository.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        jobs = await processing_job_repository.get_by_capture(capture_id)
        return StatusResponse.from_capture_and_jobs(capture, jobs)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{capture_id}/timeline", response_model=TimelineResponse)
async def get_timeline(capture_id: str):
    """Get capture timeline."""
    try:
        capture = await capture_repository.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        events = await timeline_repository.get_by_capture(capture_id)
        return TimelineResponse.from_events(capture_id, events)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{capture_id}/process", response_model=ProcessResponse)
async def process_capture(capture_id: str):
    """Start processing for a capture."""
    try:
        capture = await capture_repository.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        await capture_repository.update_status(capture_id, "processing")

        transcription_job = await processing_job_repository.create(
            capture_id=capture_id,
            job_type="transcription"
        )
        image_job = await processing_job_repository.create(
            capture_id=capture_id,
            job_type="image_processing"
        )

        transcription_task_id = await processing_service.queue_transcription(capture_id)
        image_task_id = await processing_service.queue_image_processing(capture_id)

        await processing_job_repository.update_result(
            transcription_job.id,
            "queued",
            {"task_id": transcription_task_id}
        )
        await processing_job_repository.update_result(
            image_job.id,
            "queued",
            {"task_id": image_task_id}
        )

        return ProcessResponse(
            capture_id=capture_id,
            status="processing started",
            jobs=[
                {"job_id": transcription_job.id, "type": "transcription", "task_id": transcription_task_id},
                {"job_id": image_job.id, "type": "image_processing", "task_id": image_task_id}
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{capture_id}", response_model=DeleteResponse)
async def delete_capture(capture_id: str):
    """Delete a capture and all associated data."""
    try:
        capture = await capture_repository.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        images = await image_repository.get_by_capture(capture_id)

        await timeline_repository.delete_by_capture(capture_id)
        await transcription_repository.delete_by_capture(capture_id)
        await processing_job_repository.delete_by_capture(capture_id)

        for image in images:
            await file_service.delete_file(image.file_path)

        await capture_repository.delete(capture_id)

        return DeleteResponse(
            capture_id=capture_id,
            status="deleted"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
