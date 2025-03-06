import os
import requests
import dotenv
import logging


def get_nebula_response(api_key: str, prompt: str):
    """Fetch response from Nebula Inference API.

    Args:
        api_key: API key for authentication.
        prompt: User's query for the AI model.

    Returns:
        JSON response from the API.
    """
    url = "https://inference.nebulablock.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def verify_connection(api_key: str):
    """Verify API connection by sending a test request."""
    test_prompt = "Is this API working correctly?"
    response = get_nebula_response(api_key, test_prompt)
    return response is not None


if __name__ == '__main__':
    dotenv.load_dotenv()
    nebula_api_key = os.getenv("NEBULA_API_KEY")

    if not nebula_api_key:
        logging.error("NEBULA_API_KEY is missing.")
    else:
        logging.info("Attempting connection to Nebula Inference API...")
        if verify_connection(nebula_api_key):
            logging.info("Connected to Nebula Inference API successfully.")
            user_prompt = "Is Montreal a thriving hub for the AI industry?"
            response = get_nebula_response(nebula_api_key, user_prompt)
            logging.info(f"API Response: {response}")
        else:
            logging.error("Failed to connect to Nebula Inference API.")