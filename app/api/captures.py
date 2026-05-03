from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.api.dto import (
    CreateCaptureRequest, CreateCaptureResponse,
    UploadResponse, StatusResponse, TimelineResponse,
    ProcessResponse, DeleteResponse
)
from app.config.di_config import (
    get_capture_repository, get_image_repository,
    get_timeline_repository, get_transcription_repository,
    get_processing_job_repository, get_file_service, get_processing_service
)
from app.config.settings import settings

router = APIRouter()


@router.post("/", response_model=CreateCaptureResponse)
async def create_capture(
    request: CreateCaptureRequest,
    capture_repo = Depends(get_capture_repository)
):
    """Create a new capture"""
    try:
        capture = await capture_repo.create(
            title=request.title,
            description=request.description
        )
        return CreateCaptureResponse.from_capture(capture)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{capture_id}/audio", response_model=UploadResponse)
async def upload_audio(
    capture_id: str,
    file: UploadFile = File(...),
    capture_repo = Depends(get_capture_repository),
    file_service = Depends(get_file_service)
):
    """Upload audio file for a capture"""
    # Validate file type
    if file.content_type not in settings.allowed_audio_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_audio_types)}"
        )

    # Validate file size (if content length is available)
    if hasattr(file, 'size') and file.size > settings.max_upload_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_upload_size} bytes"
        )

    try:
        # Check if capture exists
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        # Save file
        file_data = await file.read()
        file_path = await file_service.save_file(
            file_data=file_data,
            file_name=file.filename,
            file_type="audio"
        )

        # Update capture status
        await capture_repo.update_status(capture_id, "audio_uploaded")

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
async def upload_image(
    capture_id: str,
    file: UploadFile = File(...),
    capture_repo = Depends(get_capture_repository),
    image_repo = Depends(get_image_repository),
    file_service = Depends(get_file_service)
):
    """Upload image file for a capture"""
    # Validate file type
    if file.content_type not in settings.allowed_image_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_image_types)}"
        )

    # Validate file size (if content length is available)
    if hasattr(file, 'size') and file.size > settings.max_upload_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_upload_size} bytes"
        )

    try:
        # Check if capture exists
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        # Save file
        file_data = await file.read()
        file_path = await file_service.save_file(
            file_data=file_data,
            file_name=file.filename,
            file_type="image"
        )

        # Create image record
        image = await image_repo.create(
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
async def get_status(
    capture_id: str,
    capture_repo = Depends(get_capture_repository),
    processing_repo = Depends(get_processing_job_repository)
):
    """Get capture processing status"""
    try:
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        # Get processing jobs
        jobs = await processing_repo.get_by_capture(capture_id)

        return StatusResponse.from_capture_and_jobs(capture, jobs)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{capture_id}/timeline", response_model=TimelineResponse)
async def get_timeline(
    capture_id: str,
    capture_repo = Depends(get_capture_repository),
    timeline_repo = Depends(get_timeline_repository)
):
    """Get capture timeline"""
    try:
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        events = await timeline_repo.get_by_capture(capture_id)

        return TimelineResponse.from_events(capture_id, events)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{capture_id}/process", response_model=ProcessResponse)
async def process_capture(
    capture_id: str,
    capture_repo = Depends(get_capture_repository),
    processing_repo = Depends(get_processing_job_repository),
    processing_service = Depends(get_processing_service)
):
    """Start processing for a capture"""
    try:
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        # Update status to processing
        await capture_repo.update_status(capture_id, "processing")

        # Create processing jobs
        transcription_job = await processing_repo.create(
            capture_id=capture_id,
            job_type="transcription"
        )

        image_job = await processing_repo.create(
            capture_id=capture_id,
            job_type="image_processing"
        )

        # Queue background tasks
        transcription_task_id = await processing_service.queue_transcription(capture_id)
        image_task_id = await processing_service.queue_image_processing(capture_id)

        # Update jobs with task IDs
        await processing_repo.update_result(
            transcription_job.id,
            "queued",
            {"task_id": transcription_task_id}
        )
        await processing_repo.update_result(
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
async def delete_capture(
    capture_id: str,
    capture_repo = Depends(get_capture_repository),
    image_repo = Depends(get_image_repository),
    timeline_repo = Depends(get_timeline_repository),
    transcription_repo = Depends(get_transcription_repository),
    processing_repo = Depends(get_processing_job_repository),
    file_service = Depends(get_file_service)
):
    """Delete a capture and all associated data"""
    try:
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        # Get all images for cleanup
        images = await image_repo.get_by_capture(capture_id)

        # Delete associated data
        await timeline_repo.delete_by_capture(capture_id)
        await transcription_repo.delete_by_capture(capture_id)
        await processing_repo.delete_by_capture(capture_id)

        # Delete image files
        for image in images:
            await file_service.delete_file(image.file_path)
        await image_repo.delete_by_capture(capture_id)

        # Delete capture
        await capture_repo.delete(capture_id)

        return DeleteResponse(
            capture_id=capture_id,
            status="deleted"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))