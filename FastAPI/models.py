from database import Base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Date,
    DECIMAL,
    JSON,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    user_type = Column(Enum("customer", "admin", "serviceman"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Property(Base):
    __tablename__ = "properties"

    property_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    postcode = Column(String(10), nullable=False)
    property_type = Column(String(50), nullable=False)
    roof_size = Column(Integer)
    roof_profile = Column(Enum("Sloped", "Steep-Sloped", "Flat", "Dome", "Other"))
    created_at = Column(DateTime, server_default=func.now())


class Consultation(Base):
    __tablename__ = "consultations"

    consultation_id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.property_id"))
    consultant_id = Column(Integer, ForeignKey("users.user_id"))
    consultation_date = Column(DateTime, nullable=False)
    status = Column(Enum("scheduled", "completed", "cancelled"), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class EnergyCalculation(Base):
    __tablename__ = "energy_calculation"

    calculation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.property_id"), nullable=False)
    energy_consumption = Column(DECIMAL(10, 2), nullable=False)
    date = Column(DateTime, server_default=func.now())


class CarbonFootprint(Base):
    __tablename__ = "carbon_footprint"

    calculation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.property_id"), nullable=False)
    carbon_released = Column(DECIMAL(10, 2), nullable=False)
    date = Column(DateTime, server_default=func.now())


class LegalDocument(Base):
    __tablename__ = "legal_documents"

    document_id = Column(Integer, primary_key=True, autoincrement=True)
    document_type = Column(
        Enum("legal", "compliance", "report", "invoice", "receipt", "article"),
        nullable=False,
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(String(50), nullable=False)
    status = Column(Enum("active", "archived"), nullable=False)
    expiry_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, server_default=func.now())
    last_modified_by = Column(Integer, ForeignKey("users.user_id"))
    last_modified_at = Column(DateTime, onupdate=func.now())


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    position = Column(String(100), nullable=False)
    manager_id = Column(Integer, ForeignKey("employees.employee_id"))
    access_rights = Column(String, nullable=False)  # Using String for SET type
    status = Column(Enum("active", "inactive", "on_leave"), nullable=False)
    last_login = Column(DateTime)


class CustomerTicket(Base):
    __tablename__ = "customer_tickets"

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    assigned_to = Column(Integer, ForeignKey("users.user_id"))
    category = Column(Enum("Technical", "Billing", "Installation"), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum("open", "in_progress", "resolved", "closed"), nullable=False)
    priority = Column(Enum("low", "medium", "high", "urgent"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    resolved_at = Column(DateTime)


class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"

    subscription_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    status = Column(Enum("active", "unsubscribed"), nullable=False)
    subscription_date = Column(DateTime, server_default=func.now())
    unsubscribe_date = Column(DateTime)
    preferences = Column(JSON)


class AdminChange(Base):
    __tablename__ = "admin_changes"

    change_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("users.user_id"))
    change_type = Column(Enum("update", "delete", "create"), nullable=False)
    changed_at = Column(DateTime, server_default=func.now())
    table_affected = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    old_value = Column(JSON)
    new_value = Column(JSON)
