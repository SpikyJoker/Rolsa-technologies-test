from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
import model


class UserType(str, Enum):
    customer = "customer"
    admin = "admin"
    serviceman = "serviceman"


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    user_type: UserType


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RoofProfile(str, Enum):
    sloped = "Sloped"
    steep_sloped = "Steep-Sloped"
    flat = "Flat"
    dome = "Dome"
    other = "Other"


class PropertyBase(BaseModel):
    address_line1: str
    address_line2: Optional[str]
    city: str
    postcode: str
    property_type: str
    roof_size: Optional[int]
    roof_profile: Optional[RoofProfile]


class Property(PropertyBase):
    property_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ConsultationStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class Consultation(BaseModel):
    consultation_id: int
    property_id: int
    consultant_id: int
    consultation_date: datetime
    status: ConsultationStatus
    notes: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class EnergyCalculation(BaseModel):
    calculation_id: int
    user_id: int
    property_id: int
    energy_consumption: float
    date: datetime

    class Config:
        orm_mode = True


class CarbonFootprint(BaseModel):
    calculation_id: int
    user_id: int
    property_id: int
    carbon_released: float
    date: datetime

    class Config:
        orm_mode = True


class DocumentType(str, Enum):
    legal = "legal"
    compliance = "compliance"
    report = "report"
    invoice = "invoice"
    receipt = "receipt"
    article = "article"


class DocumentStatus(str, Enum):
    active = "active"
    archived = "archived"


class LegalDocument(BaseModel):
    document_id: int
    document_type: DocumentType
    title: str
    content: str
    version: str
    status: DocumentStatus
    expiry_date: Optional[datetime]
    created_by: int
    created_at: datetime
    last_modified_by: Optional[int]
    last_modified_at: Optional[datetime]

    class Config:
        orm_mode = True


class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    on_leave = "on_leave"


class Employee(BaseModel):
    employee_id: int
    user_id: int
    position: str
    manager_id: Optional[int]
    access_rights: str
    status: EmployeeStatus
    last_login: Optional[datetime]

    class Config:
        orm_mode = True


class TicketCategory(str, Enum):
    technical = "Technical"
    billing = "Billing"
    installation = "Installation"


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class CustomerTicket(BaseModel):
    ticket_id: int
    user_id: int
    assigned_to: Optional[int]
    category: TicketCategory
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        orm_mode = True


class SubscriptionStatus(str, Enum):
    active = "active"
    unsubscribed = "unsubscribed"


class NewsletterSubscription(BaseModel):
    subscription_id: int
    email: str
    status: SubscriptionStatus
    subscription_date: datetime
    unsubscribe_date: Optional[datetime]
    preferences: Optional[dict]

    class Config:
        orm_mode = True


class ChangeType(str, Enum):
    update = "update"
    delete = "delete"
    create = "create"


class AdminChange(BaseModel):
    change_id: int
    admin_id: int
    change_type: ChangeType
    changed_at: datetime
    table_affected: str
    record_id: int
    old_value: Optional[dict]
    new_value: Optional[dict]

    class Config:
        orm_mode = True
