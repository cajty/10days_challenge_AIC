from agent import EmailSupportAgent
from models import EmailRequest


def print_separator():
    """Print a visual separator."""
    print("=" * 60)

def get_user_input(prompt):
    """Get user input with error handling."""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit(0)

def display_response(response):
    """Display the agent's response in a formatted way."""
    print_separator()
    print("🎫 SUPPORT TICKET CREATED")
    print_separator()
    print(f"Ticket ID: {response.ticket_id}")
    print(f"Customer: {response.customer_name} ({response.customer_email})")
    print(f"Category: {response.category.upper()}")
    print(f"Sentiment: {response.sentiment.upper()}")
    print(f"Urgency: {response.urgency.upper()}")
    print(f"Requires Human: {'YES' if response.requires_human else 'NO'}")
    print(f"Timestamp: {response.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print_separator()
    print("📧 SUGGESTED RESPONSE:")
    print_separator()
    print(response.suggested_response)
    print_separator()

def initialize_agent():
    """Initialize the email support agent."""
    try:
        agent = EmailSupportAgent()
        print("✅ Agent initialized successfully!")
        return agent
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return None

def collect_email_details():
    """Collect email details from user input."""
    print("\n📨 NEW EMAIL SIMULATION")
    print("Enter email details (or 'quit' to exit):")

    customer_name = get_user_input("Customer Name: ")
    if customer_name.lower() == 'quit':
        return None

    customer_email = get_user_input("Customer Email: ")
    if customer_email.lower() == 'quit':
        return None

    subject = get_user_input("Subject: ")
    if subject.lower() == 'quit':
        return None

    message = collect_message()
    if message is None:
        return None

    return {
        'name': customer_name,
        'email': customer_email,
        'subject': subject,
        'message': message
    }

def collect_message():
    """Collect multi-line message from user."""
    print("Message (press Enter twice when done):")
    message_lines = []

    while True:
        line = get_user_input("")
        if line.lower() == 'quit':
            return None
        if line == "" and message_lines:
            break
        message_lines.append(line)

    message = "\n".join(message_lines)

    if not message.strip():
        print("❌ Message cannot be empty!")
        return ""

    return message

def create_and_process_email(agent, email_data):
    """Create email request and process it."""
    try:
        email_request = EmailRequest(
            from_email=email_data['email'],
            from_name=email_data['name'],
            subject=email_data['subject'],
            message=email_data['message']
        )
    except Exception as e:
        print(f"❌ Error creating email request: {e}")
        return False

    print("\n🔄 Processing email...")
    try:
        response = agent.process_email(email_request)
        display_response(response)
        return True
    except Exception as e:
        print(f"❌ Error processing email: {e}")
        return False

def should_continue_chat():
    """Check if user wants to continue chatting."""
    continue_chat = get_user_input("\nProcess another email? (y/n): ")
    return continue_chat.lower() in ['y', 'yes']

def chat_mode():
    """Interactive chat mode with the agent."""
    print("🤖 EMAIL SUPPORT AGENT CHAT")
    print("Type 'quit' to exit")
    print_separator()

    agent = initialize_agent()
    if not agent:
        return

    while True:
        email_data = collect_email_details()
        if email_data is None:
            break

        if email_data['message'] == "":
            continue

        create_and_process_email(agent, email_data)

        if not should_continue_chat():
            break

    print("\n👋 Thank you for using Email Support Agent!")

def demo_mode():
    """Run demo with pre-defined examples."""
    print("🎬 DEMO MODE - Sample Email Processing")
    print_separator()

    # Initialize agent
    try:
        agent = EmailSupportAgent()
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return

    # Demo emails
    demo_emails = [
        {
            "name": "John Smith",
            "email": "john@example.com",
            "subject": "Urgent: Order not delivered",
            "message": "I am very frustrated! My order was supposed to arrive yesterday but it's still not here. This is unacceptable. I need it urgently for my meeting tomorrow."
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah@example.com",
            "subject": "Billing question",
            "message": "Hi there! I noticed I was charged twice for my recent purchase. Could you please help me understand what happened? Thanks!"
        },
        {
            "name": "Mike Davis",
            "email": "mike@example.com",
            "subject": "App not working",
            "message": "The mobile app keeps crashing when I try to log in. I've tried restarting my phone but the technical issue persists."
        }
    ]

    for i, email_data in enumerate(demo_emails, 1):
        print(f"\n📧 DEMO EMAIL {i}/3")
        print(f"From: {email_data['name']} ({email_data['email']})")
        print(f"Subject: {email_data['subject']}")
        print(f"Message: {email_data['message']}")

        # Create and process email
        try:
            email_request = EmailRequest(
                from_email=email_data['email'],
                from_name=email_data['name'],
                subject=email_data['subject'],
                message=email_data['message']
            )

            print(f"\n🔄 Processing demo email {i}...")
            response = agent.process_email(email_request)
            display_response(response)

            if i < len(demo_emails):
                input("\nPress Enter to continue to next demo...")

        except Exception as e:
            print(f"❌ Error processing demo email {i}: {e}")

def main():
    """Main function."""
    print("🤖 WELCOME TO EMAIL SUPPORT AGENT")
    print_separator()
    print("Choose an option:")
    print("1. Chat Mode (Interactive)")
    print("2. Demo Mode (Pre-defined examples)")
    print("3. Quit")
    print_separator()

    choice = get_user_input("Enter your choice (1-3): ")

    if choice == "1":
        chat_mode()
    elif choice == "2":
        demo_mode()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again and select 1, 2, or 3.")

if __name__ == "__main__":
    main()