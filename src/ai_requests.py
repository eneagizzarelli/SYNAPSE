import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_tab_completions(text):
    response = openai.chat.completions.create(model = model, messages = text, temperature = 0.5, max_tokens = 100, n = 10)
    completions = [choice.message.content for choice in response.choices]

    print(completions)

    return completions

def completer(text, state):
    text = [{"role": 'system', "content": text}]

    completions = generate_tab_completions(text)

    matches = [option for option in completions if option.startswith(text)]
    
    if state < len(matches):
        return matches[state]
    else:
        return None
    
readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

def generate_response(messages):
    response = openai.chat.completions.create(model = model, messages = messages, temperature = 0.0, max_tokens = 800)
    msg = response.choices[0].message.content
    message = {"role": 'assistant', "content": msg}
    
    return message