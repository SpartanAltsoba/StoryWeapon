import os
from dotenv import load_dotenv
from openai import OpenAI  # Updated import statement

# Load environment variables
load_dotenv()

# Initialize the client correctly
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

try:
    # Create chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="o1-preview-2024-09-12",  # Corrected model name from "gpt-4o" to "gpt-4"
    )
    
    # Extract and print the response content
    response_content = chat_completion.choices[0].message.content
    print(response_content)

except Exception as e:
    print(f"An error occurred: {e}")