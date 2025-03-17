from flask import Flask, render_template, request, jsonify
import os
from google import genai
from google.genai import types
from api_handlers import get_philly_events, get_crash_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Gemini client
client = genai.Client(
    api_key='enter key',
)

# Global chat history
chat_history = []

def initialize_context():
    """Initialize context with events and Looker data"""
    try:
        # Get initial data
        events = get_philly_events()
        looker_data = get_crash_data()
        
        # Format events data
        events_str = "\n".join([
            f"- {event['name']} at {event['venue']} {event['street']} on {event['date']}" 
            for event in events
        ])
        
        # Create system context
        system_context = f"""You are a helpful AI assistant focused on Philadelphia.
You have access to the following data that was loaded when you started:

Current Philadelphia Events (Next 7 Days):
{events_str}

Crash Analysis Data:
{looker_data}

Instructions:
1. Use this event and crash data when answering relevant questions
2. For questions about events, reference the specific events listed above
3. For questions about crash data, use the analysis provided
4. For other questions about Philadelphia, you can provide general knowledge
5. Always maintain a natural, conversational tone
6. Use Google Search when needed for current information not in the provided data

Remember: Your events and crash data is from system initialization and represents that point in time."""

        # Add context to chat history
        chat_history.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=system_context)]
        ))

        print("Context initialized successfully")
        return True
        
    except Exception as e:
        print(f"Error initializing context: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'error': 'Message required'}), 400

        # Add user message to history
        chat_history.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        ))

        # Configure generation settings
        generate_content_config = types.GenerateContentConfig(
            temperature=0.9,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )

        # Generate response using full chat history
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=chat_history,
            config=generate_content_config,
        )

        # Add assistant response to history
        chat_history.append(types.Content(
            role="assistant",
            parts=[types.Part.from_text(text=response.text)]
        ))

        return jsonify({'response': response.text})

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize context before starting
    print("Initializing context...")
    if initialize_context():
        app.run(debug=True)
    else:
        print("Failed to initialize context")
        exit(1)
