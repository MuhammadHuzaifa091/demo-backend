"""RepairRequest endpoints with role-based access control."""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.permissions import require_user_role, require_provider_role
from app.database.session import get_db
from app.core.users import current_active_user
from app.models.users import User
from app.models.repair_requests import RepairRequest
from app.schemas.repair_request import (
    RepairRequestCreate,
    RepairRequestUpdate,
    RepairRequest as RepairRequestSchema,
)

import os
import aiofiles
from pathlib import Path

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/voices")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=RepairRequestSchema, status_code=status.HTTP_201_CREATED)
async def create_repair_request(
    title: str = Form(...),
    description: str = Form(None),
    voice_file: UploadFile = File(None),
    current_user: User = Depends(require_user_role),
    session: AsyncSession = Depends(get_db),
) -> RepairRequestSchema:
    """Create a new repair request (Users only)."""
    # Validate that either description or voice_file is provided
    if not description and not voice_file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either description or voice file must be provided"
        )

    voice_file_path = None
    if voice_file:
        # Validate file type
        if not voice_file.content_type or not voice_file.content_type.startswith(('audio/', 'application/octet-stream')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only audio files are allowed"
            )

        # Generate unique filename
        file_extension = voice_file.filename.split(
            '.')[-1] if '.' in voice_file.filename else 'wav'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        voice_file_path = UPLOAD_DIR / unique_filename

        # Save file
        async with aiofiles.open(voice_file_path, 'wb') as f:
            content = await voice_file.read()
            await f.write(content)

        voice_file_path = str(voice_file_path)

    repair_request = RepairRequest(
        title=title,
        description=description,
        voice_file=voice_file_path,
        user_id=current_user.id,
    )
    session.add(repair_request)
    await session.commit()
    await session.refresh(repair_request)
    return repair_request


@router.get("/", response_model=List[RepairRequestSchema])
async def get_repair_requests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_provider_role),
    session: AsyncSession = Depends(get_db),
) -> List[RepairRequestSchema]:
    """Get all repair requests (Providers only)."""
    result = await session.execute(
        select(RepairRequest)
        .options(selectinload(RepairRequest.user))
        .offset(skip)
        .limit(limit)
        .order_by(RepairRequest.created_at.desc())
    )
    return result.scalars().all()


@router.get("/my-requests", response_model=List[RepairRequestSchema])
async def get_my_repair_requests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_user_role),
    session: AsyncSession = Depends(get_db),
) -> List[RepairRequestSchema]:
    """Get current user's repair requests (Users only)."""
    result = await session.execute(
        select(RepairRequest)
        .options(selectinload(RepairRequest.user))
        .where(RepairRequest.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(RepairRequest.created_at.desc())
    )
    return result.scalars().all()


@router.get("/voice/{filename}")
async def get_voice_file(
    filename: str,
    current_user: User = Depends(require_provider_role),
):
    """Serve voice files (Providers only)."""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice file not found"
        )
    return FileResponse(file_path)


@router.get("/{repair_request_id}", response_model=RepairRequestSchema)
async def get_repair_request(
    repair_request_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> RepairRequestSchema:
    """Get a single repair request by ID."""
    result = await session.execute(
        select(RepairRequest)
        .options(selectinload(RepairRequest.user))
        .where(RepairRequest.id == repair_request_id)
    )
    repair_request = result.scalar_one_or_none()

    if not repair_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repair request not found"
        )

    return repair_request


@router.put("/{repair_request_id}", response_model=RepairRequestSchema)
async def update_repair_request(
    repair_request_id: uuid.UUID,
    repair_request_update: RepairRequestUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
) -> RepairRequestSchema:
    """Update a repair request (only owner can update)."""
    result = await session.execute(
        select(RepairRequest).where(RepairRequest.id == repair_request_id)
    )
    repair_request = result.scalar_one_or_none()

    if not repair_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repair request not found"
        )

    if repair_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this repair request"
        )

    update_data = repair_request_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(repair_request, field, value)

    await session.commit()
    await session.refresh(repair_request)
    return repair_request


@router.delete("/{repair_request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_repair_request(
    repair_request_id: uuid.UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    """Delete a repair request (only owner can delete)."""
    result = await session.execute(
        select(RepairRequest).where(RepairRequest.id == repair_request_id)
    )
    repair_request = result.scalar_one_or_none()

    if not repair_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repair request not found"
        )

    if repair_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this repair request"
        )

    await session.delete(repair_request)
    await session.commit()
