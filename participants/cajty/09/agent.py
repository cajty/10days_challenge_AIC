from datetime import datetime
from smolagents import CodeAgent, OpenAIServerModel, tool
from models import EmailRequest, SupportResponse
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

@tool
def analyze_sentiment(message: str) -> str:
    """Analyze customer sentiment from email message.

    Args:
        message: The customer's email message text

    Returns:
        Sentiment classification: 'positive', 'negative', or 'neutral'
    """
    message_lower = message.lower()

    negative_words = ["angry", "frustrated", "terrible", "awful", "hate", "unacceptable"]
    positive_words = ["happy", "satisfied", "great", "excellent", "amazing", "love"]

    negative_count = sum(1 for word in negative_words if word in message_lower)
    positive_count = sum(1 for word in positive_words if word in message_lower)

    if negative_count > positive_count:
        return "negative"
    elif positive_count > negative_count:
        return "positive"
    else:
        return "neutral"

@tool
def categorize_issue(subject: str, message: str) -> str:
    """Categorize the customer issue.

    Args:
        subject: The email subject line
        message: The customer's email message text

    Returns:
        Issue category: 'order', 'billing', 'technical', or 'general'
    """
    text = (subject + " " + message).lower()

    if any(word in text for word in ["order", "shipping", "delivery", "tracking"]):
        return "order"
    elif any(word in text for word in ["bill", "charge", "payment", "refund", "money"]):
        return "billing"
    elif any(word in text for word in ["bug", "error", "not working", "broken", "technical"]):
        return "technical"
    else:
        return "general"

@tool
def assess_urgency(message: str, sentiment: str) -> str:
    """Assess urgency level of the issue.

    Args:
        message: The customer's email message text
        sentiment: The sentiment classification from analyze_sentiment

    Returns:
        Urgency level: 'critical', 'high', 'medium', or 'low'
    """
    message_lower = message.lower()

    critical_words = ["urgent", "emergency", "critical", "immediately", "asap"]
    high_words = ["important", "priority", "soon", "quickly"]

    if any(word in message_lower for word in critical_words):
        return "critical"
    elif any(word in message_lower for word in high_words) or sentiment == "negative":
        return "high"
    elif sentiment == "positive":
        return "low"
    else:
        return "medium"

@tool
def generate_response(category: str, sentiment: str, customer_name: str) -> str:
    """Generate appropriate customer response.

    Args:
        category: The issue category from categorize_issue
        sentiment: The sentiment classification from analyze_sentiment
        customer_name: The customer's name for personalization

    Returns:
        Personalized response message for the customer
    """
    greeting = f"Hi {customer_name},"

    if sentiment == "negative":
        empathy = "I understand your frustration and I'm here to help resolve this issue."
    else:
        empathy = "Thank you for reaching out to us."

    if category == "order":
        solution = "I'll check your order status and provide you with an update shortly."
    elif category == "billing":
        solution = "I'll review your billing inquiry and get back to you with clarification."
    elif category == "technical":
        solution = "I'll investigate this technical issue and work on a solution."
    else:
        solution = "I'll review your request and provide assistance."

    closing = "Please let me know if you have any other questions."

    return f"{greeting}\n\n{empathy} {solution}\n\n{closing}\n\nBest regards,\nCustomer Support Team"

class EmailSupportAgent:
    """Simple AI agent for email support processing."""

    def __init__(self):
        # Initialize the AI model
        self.model = OpenAIServerModel(
            model_id="gemini-2.0-flash",
            api_base="https://generativelanguage.googleapis.com/v1beta",
            api_key=GOOGLE_API_KEY,
        )

        # Create agent with tools
        self.agent = CodeAgent(
            model=self.model,
            tools=[
                analyze_sentiment,
                categorize_issue,
                assess_urgency,
                generate_response
            ]
        )


    def process_email(self, email: EmailRequest) -> SupportResponse:
        """Process email and return support response."""

        # Create analysis prompt
        prompt = f"""
        Analyze this customer email and provide structured information:

        From: {email.from_name} ({email.from_email})
        Subject: {email.subject}
        Message: {email.message}

        Use the available tools to:
        1. Analyze sentiment using analyze_sentiment
        2. Categorize the issue using categorize_issue  
        3. Assess urgency using assess_urgency
        4. Generate response using generate_response

        Provide clear analysis results.
        """

        # Get AI analysis
        analysis = self.agent.run(prompt)

        # Parse results and create response
        sentiment = self._extract_from_analysis(analysis, "sentiment", "neutral")
        category = self._extract_from_analysis(analysis, "category", "general")
        urgency = self._extract_from_analysis(analysis, "urgency", "medium")

        # Determine if human intervention needed
        requires_human = (
                urgency == "critical" or
                (urgency == "high" and sentiment == "negative")
        )

        # Generate response
        response_text = self._extract_response_from_analysis(analysis, email.from_name)

        # Create ticket ID
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return SupportResponse(
            ticket_id=ticket_id,
            urgency=urgency,
            category=category,
            sentiment=sentiment,
            suggested_response=response_text,
            requires_human=requires_human,
            customer_name=email.from_name,
            customer_email=email.from_email,
            timestamp=datetime.now()
        )

    def _extract_from_analysis(self, analysis: str, field: str, default: str) -> str:
        """Extract specific field from AI analysis."""
        analysis_lower = analysis.lower()

        field_mappings = {
            "sentiment": ["positive", "negative", "neutral"],
            "category": ["order", "billing", "technical", "general"],
            "urgency": ["critical", "high", "medium", "low"]
        }

        if field in field_mappings:
            return self._find_first_match(analysis_lower, field_mappings[field], default)

        return default

    def _find_first_match(self, text: str, options: list, default: str) -> str:
        """Find first matching option in text."""
        for option in options:
            if option in text:
                return option
        return default

    def _extract_response_from_analysis(self, analysis: str, customer_name: str) -> str:
        """Extract generated response from analysis."""
        lines = analysis.split('\n')
        response_lines = self._parse_response_lines(lines)

        if response_lines:
            return '\n'.join(response_lines)

        return self._get_fallback_response(customer_name)

    def _parse_response_lines(self, lines: list) -> list:
        """Parse response lines from analysis."""
        response_keywords = ["response:", "reply:", "message:"]
        response_lines = []
        capture = False

        for line in lines:
            if self._is_response_start(line, response_keywords):
                capture = True
                inline_response = self._extract_inline_response(line)
                if inline_response:
                    response_lines.append(inline_response)
                continue

            if capture:
                if line.strip():
                    response_lines.append(line.strip())
                else:
                    break

        return response_lines

    def _is_response_start(self, line: str, keywords: list) -> bool:
        """Check if line starts a response section."""
        return any(keyword in line.lower() for keyword in keywords)

    def _extract_inline_response(self, line: str) -> str:
        """Extract response text from same line as keyword."""
        if ":" in line:
            response_part = line.split(":", 1)[1].strip()
            return response_part if response_part else ""
        return ""

    def _get_fallback_response(self, customer_name: str) -> str:
        """Generate fallback response when extraction fails."""
        return (f"Hi {customer_name},\n\n"
                "Thank you for contacting us. We have received your message and will respond shortly.\n\n"
                "Best regards,\nCustomer Support Team")