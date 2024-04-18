import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    terminal_msg = response.choices[0].message.content
    terminal_message = {"role": 'assistant', "content": terminal_msg}
    
    return terminal_message