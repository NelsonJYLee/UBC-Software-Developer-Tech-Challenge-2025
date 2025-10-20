import requests
import json
from dotenv import load_dotenv
import os

# NOTE: Since this is designed to run outside of the Canvas environment, 
# you should typically replace the empty string with your actual Gemini API Key.
# However, as per instructions for this environment, we leave it empty.
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

SYSTEM_PROMPT = (
    "You are a quick-witted comedian. When given a subject, generate a single, "
    "concise, one-sentence pun joke about that subject. Do not use any filler, "
    "preamble, or introduction. Deliver only the joke sentence."
)

def get_joke(subject):
    """
    Calls the Gemini API to generate a joke based on the subject (single attempt).
    """
    headers = {
        "Content-Type": "application/json",
    }

    # Construct the payload with the system instruction and user query
    payload = {
        "contents": [{
            "parts": [{"text": f"Joke subject: {subject}"}]
        }],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        }
    }
    
    try:
        print(f"\n--- Generating joke for '{subject}'...")
        
        # Send the API request
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        
        # Extract the generated text
        joke = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Could not retrieve joke.')
        return joke.strip()

    except requests.exceptions.RequestException as e:
        # Simplified error handling for a single attempt
        print(f"Connection Error: {e}")
        return "Sorry, the joke machine is down. Please check your API key or network connection."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
            

def main():
    """
    Main function to run the terminal application.
    """
    print("\n==============================================")
    print("        Gemini Terminal Joke Generator        ")
    print("==============================================")

    while True:
        subject = input("\nEnter a subject for a joke (or type 'quit' to exit): ").strip()
        
        if subject.lower() == 'quit':
            print("\nThanks for the laughs! Goodbye.")
            break
        
        if subject:
            # The function call is now simpler as it doesn't need the 'retries' argument
            joke_text = get_joke(subject)
            print("\n----------------------------------------------")
            print("THE JOKE:")
            print(f"{joke_text}")
            print("----------------------------------------------")
        else:
            print("Please enter a subject.")

if __name__ == "__main__":
    main()
