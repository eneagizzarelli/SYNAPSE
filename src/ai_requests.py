import openai
from dotenv import dotenv_values
import readline

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

model = "gpt-3.5-turbo-0125"

def generate_response(messages):
    response = openai.completions.create(model = model, prompt = messages, temperature = 0.0, max_tokens = 800)
    terminal_msg = response.choices[0].message.content
    terminal_message = {"role": 'assistant', "content": terminal_msg}
    
    return terminal_message

# def generate_tab_completions(text):
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # You can choose a different engine based on your preference
#         prompt=text,
#         max_tokens=5,  # Adjust the number of tokens based on your needs
#         n=5,  # Adjust the number of completions returned based on your needs
#         stop=None
#     )
#     completions = [choice['text'].strip() for choice in response['choices']]
#     return completions

# def completer(text, state):
#     completions = generate_tab_completions(text)
#     matches = [option for option in completions if option.startswith(text)]
#     if state < len(matches):
#         return matches[state]
#     else:
#         return None

# import readline
# readline.set_completer(completer)
# readline.parse_and_bind('tab: complete')

# user_input = input("Enter text: ")
# print("You entered:", user_input)