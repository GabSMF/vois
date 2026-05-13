from fastapi import APIRouter, HTTPException
from app.api.dto import (
    SearchRequest, SearchResponse, CaptureSearchRequest, CaptureSearchResponse,
    SearchResultDTO
)
from app.config.di_config import search_service, capture_repository

router = APIRouter()


@router.post("/global", response_model=SearchResponse)
async def global_search(request: SearchRequest):
    """Search across all captures."""
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
async def capture_search(capture_id: str, request: CaptureSearchRequest):
    """Search within a specific capture."""
    try:
        capture = await capture_repository.get(capture_id)
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
