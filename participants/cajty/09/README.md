# Email Support Agent

An AI-powered email support agent that automatically analyzes customer emails and generates appropriate responses using Google's Gemini API.

## Features

- **Sentiment Analysis**: Automatically detects positive, negative, or neutral sentiment in customer emails
- **Issue Categorization**: Classifies emails into categories (order, billing, technical, general)
- **Urgency Assessment**: Determines priority levels (critical, high, medium, low)
- **Automated Response Generation**: Creates personalized responses based on analysis
- **Human Escalation**: Flags emails that require human intervention
- **Interactive Modes**: Both demo and chat modes available

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

Run the application:
```bash
python main.py
```

Choose from two modes:
1. **Chat Mode**: Interactive mode for processing custom emails
2. **Demo Mode**: Pre-configured examples to see the agent in action

## Project Structure

- `main.py` - Main application with interactive CLI
- `agent.py` - Core email support agent implementation
- `models.py` - Pydantic models for email requests and responses
- `requirements.txt` - Python dependencies

## Technologies Used

- **FastAPI** - Web framework (ready for API endpoints)
- **Pydantic** - Data validation and serialization
- **Smolagents** - AI agent framework
- **Google Gemini** - AI model for text analysis
- **Python-dotenv** - Environment variable management

## API Models

### EmailRequest
- `from_email`: Customer email address
- `from_name`: Customer name
- `subject`: Email subject line
- `message`: Email message content

### SupportResponse
- `ticket_id`: Generated ticket identifier
- `urgency`: Priority level assessment
- `category`: Issue classification
- `sentiment`: Emotion analysis
- `suggested_response`: Generated reply
- `requires_human`: Escalation flag
- `customer_name`: Customer information
- `customer_email`: Customer email
- `timestamp`: Processing time

