"""
Database Schemas for RofaTech Digital Agency

Each Pydantic model represents a MongoDB collection (lowercased class name).
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Service(BaseModel):
    """
    Services offered by the agency
    Collection: "service"
    """
    title: str = Field(..., description="Service name, e.g., Web Development")
    slug: str = Field(..., description="URL-friendly unique identifier")
    description: str = Field(..., description="Short description of the service")
    features: Optional[List[str]] = Field(default=None, description="Key bullet points")
    icon: Optional[str] = Field(default=None, description="Icon name from lucide-react")
    featured: bool = Field(default=False, description="Whether to highlight on homepage")

class Project(BaseModel):
    """
    Case studies / portfolio projects
    Collection: "project"
    """
    title: str = Field(..., description="Project title")
    slug: str = Field(..., description="URL-friendly unique identifier")
    summary: str = Field(..., description="Short summary for cards")
    image: Optional[HttpUrl] = Field(default=None, description="Hero image URL")
    tags: Optional[List[str]] = Field(default=None, description="Tech or category tags")
    link: Optional[HttpUrl] = Field(default=None, description="Live site or demo link")
    featured: bool = Field(default=False, description="Showcase on homepage")

class Inquiry(BaseModel):
    """
    Leads from the contact form
    Collection: "inquiry"
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone or WhatsApp")
    company: Optional[str] = Field(default=None, description="Company name")
    service_interest: Optional[str] = Field(default=None, description="Which service they need")
    message: Optional[str] = Field(default=None, description="Message details")

# You can add more schemas like Testimonial, TeamMember later.