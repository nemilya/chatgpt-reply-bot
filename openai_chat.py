import os
import requests
from dotenv import load_dotenv

class OpenAIChat:
    def __init__(self):
        load_dotenv()

        self.system_prompt_file = 'system_prompt.txt'

        self.api_base = os.getenv('OPENAI_API_BASE')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('MODEL')
        self.temperature = float(os.getenv('TEMPERATURE'))

        self.api_url = f"{self.api_base}/v1/chat/completions"

        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self):
        if os.path.exists(self.system_prompt_file):
            with open(self.system_prompt_file, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return os.getenv('SYSTEM_PROMPT')

    def get_response(self, user_message):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature
        }

        response = requests.post(self.api_url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            choices = response_data.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', 'No response')
            else:
                return "API returned no response content."
        else:
            return f"Error: {response.status_code}. Details: {response.text}"
