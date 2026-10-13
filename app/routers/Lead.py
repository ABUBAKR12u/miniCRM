from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from typing import Annotated
from app.database.connection import get_db
from app.models.Lead import Lead
from app.models.Activity import Activity
from app.scheme.Lead import CreateLead, UpdateLead, ResponseLead, LeadListResponse, ActivityResponse
from app.utils.securty import get_current_user

router = APIRouter(prefix="/leads", tags=["leads"])

connect = Annotated[Session, Depends(get_db)]

STATUSES = ["New", "Contacted", "Qualified", "Won", "Lost"]


@router.post("/", response_model=ResponseLead)
def create_lead(data: CreateLead, db: connect, current_user=Depends(get_current_user)):
    lead = Lead(
        name=data.name,
        phone=data.phone,
        email=data.email,
        source=data.source,
        note=data.note
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    activity = Activity(lead_id=lead.id, action="created", detail=f"Lead created by {current_user.username}")
    db.add(activity)
    db.commit()
    return lead


@router.get("/", response_model=LeadListResponse)
def get_leads(
    db: connect,
    current_user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    status: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc")
):
    query = select(Lead)

    if search:
        query = query.where(
            or_(
                Lead.name.ilike(f"%{search}%"),
                Lead.phone.ilike(f"%{search}%"),
                Lead.email.ilike(f"%{search}%"),
                Lead.source.ilike(f"%{search}%"),
                Lead.note.ilike(f"%{search}%")
            )
        )

    if status and status in STATUSES:
        query = query.where(Lead.status == status)

    sort_column = getattr(Lead, sort_by, Lead.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar()
    pages = (total + size - 1) // size
    items = db.execute(query.offset((page - 1) * size).limit(size)).scalars().all()

    return LeadListResponse(total=total, page=page, pages=pages, items=items)


@router.get("/{lead_id}", response_model=ResponseLead)
def get_lead(lead_id: int, db: connect, current_user=Depends(get_current_user)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}", response_model=ResponseLead)
def update_lead(lead_id: int, data: UpdateLead, db: connect, current_user=Depends(get_current_user)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if data.status and data.status not in STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {STATUSES}")

    update_data = data.model_dump(exclude_unset=True)
    old_status = lead.status

    for key, value in update_data.items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)

    if data.status and data.status != old_status:
        activity = Activity(
            lead_id=lead.id,
            action="status_changed",
            detail=f"{old_status} -> {data.status} by {current_user.username}"
        )
        db.add(activity)
        db.commit()

    return lead


@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: connect, current_user=Depends(get_current_user)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"msg": "Lead deleted"}


@router.get("/{lead_id}/activities", response_model=list[ActivityResponse])
def get_activities(lead_id: int, db: connect, current_user=Depends(get_current_user)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    activities = db.execute(
        select(Activity).where(Activity.lead_id == lead_id).order_by(Activity.created_at.desc())
    ).scalars().all()
    return activities
