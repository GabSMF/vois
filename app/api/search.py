from fastapi import APIRouter, HTTPException, Depends
from app.api.dto import (
    SearchRequest, SearchResponse, CaptureSearchRequest, CaptureSearchResponse,
    SearchResultDTO
)
from app.config.di_config import get_search_service, get_capture_repository

router = APIRouter()


@router.post("/global", response_model=SearchResponse)
async def global_search(
    request: SearchRequest,
    search_service = Depends(get_search_service)
):
    """Search across all captures"""
    try:
        results, total = await search_service.search(
            query=request.query,
            limit=request.limit,
            offset=request.offset
        )

        return SearchResponse(
            query=request.query,
            results=[
                SearchResultDTO(
                    capture_id=result.capture_id,
                    content_type=result.content_type,
                    content_id=result.content_id,
                    text=result.text,
                    timestamp=result.timestamp,
                    score=result.score
                )
                for result in results
            ],
            total=total,
            limit=request.limit,
            offset=request.offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/captures/{capture_id}", response_model=CaptureSearchResponse)
async def capture_search(
    capture_id: str,
    request: CaptureSearchRequest,
    search_service = Depends(get_search_service),
    capture_repo = Depends(get_capture_repository)
):
    """Search within a specific capture"""
    try:
        # Check if capture exists
        capture = await capture_repo.get(capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture not found")

        results = await search_service.search_capture(
            capture_id=capture_id,
            query=request.query,
            limit=request.limit
        )

        return CaptureSearchResponse(
            capture_id=capture_id,
            query=request.query,
            results=[
                SearchResultDTO(
                    capture_id=result.capture_id,
                    content_type=result.content_type,
                    content_id=result.content_id,
                    text=result.text,
                    timestamp=result.timestamp,
                    score=result.score
                )
                for result in results
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))