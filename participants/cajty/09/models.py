from datetime import datetime
from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    from_email: str
    from_name: str = "Customer"
    subject: str
    message: str


class SupportResponse(BaseModel):
    """Response sent back to n8n."""
    ticket_id: str
    urgency: str = Field(description="low, medium, high, critical")
    category: str = Field(description="order, billing, technical, general")
    sentiment: str = Field(description="positive, neutral, negative")
    suggested_response: str
    requires_human: bool
    customer_name: str
    customer_email: str
    timestamp: datetime


