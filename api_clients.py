import google-generativeai as genai
import openai
from typing import Dict, Any


api_keys = {
    'gemini' : 'AIzaSyDymbsRQp89sbxD_9dLvMIuFA8RFMELqdk',
    'chatgpt' : 'YOUR_CHATGPT_API_KEY',
    'OpenAI' : 'YOUR_OPENAI_API_KEY',
    'openai' : 'YOUR_OPENAI_API_KEY'
}

def create_api_clients(api_keys: Dict[str, str]) -> Dict[str, Any]:
    """
    Create and return a dictionary of API clients based on provided API keys.
    Supported keys: 'gemini', 'chatgpt', 'OpenAI', 'openai'
    """
    clients = {}

    # Initialize Gemini API client if key is provided
    if 'gemini' in api_keys:
        genai.configure(api_key=api_keys['gemini'])
        clients['gemini'] = genai

    # Initialize OpenAI API client if key is provided
    openai_keys = ['chatgpt', 'OpenAI', 'openai']
    for key in openai_keys:
        if key in api_keys:
            openai.api_key = api_keys[key]
            clients[key] = openai
            break  # Use the first available OpenAI key

    return clients

