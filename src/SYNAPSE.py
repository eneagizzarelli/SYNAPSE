import os
from datetime import datetime
from time import sleep
import random

from initializations import load_prompts, parse_arguments, load_terminal_messages
from ai_requests import generate_response

today = datetime.now()
terminal_history_path = os.path.join("logs", "terminal_history.txt")
mysql_history_path = os.path.join("logs", "mysql_history.txt")

terminal_prompt, mysql_prompt = load_prompts()

def main():
    args = parse_arguments(terminal_prompt, mysql_prompt)

    terminal_messages = load_terminal_messages(args)

    while True:
        terminal_history = open(terminal_history_path, "a+", encoding="utf-8")

        try:
            response = generate_response(terminal_messages)

            msg = res.choices[0].message.content
            message = {"content": msg, "role": 'assistant'}

            if "$cd" in message["content"] or "$ cd" in message["content"]:
                message["content"] = message["content"].split("\n")[1]

            lines = []

            messages.append(message)

            logs.write(messages[len(messages) - 1]["content"])
            logs.close()

            logs = open("history.txt", "a+", encoding="utf-8")
            
            if "will be reported" in messages[len(messages) - 1]["content"]:
                print(messages[len(messages) - 1]["content"])
                raise KeyboardInterrupt 

            if "exit" in messages[len(messages) - 1]["content"]:
                print("logout")
                raise KeyboardInterrupt

            if "PING" in message["content"]:
                lines = message["content"].split("\n")
                print(lines[0])

                for i in range(1, len(lines)-5):
                    print(lines[i])
                    sleep(random.uniform(0.1, 0.5))
                
                for i in range(len(lines)-4, len(lines)-1):
                    print(lines[i])
                
                user_input = input(f'{lines[len(lines)-1]}'.strip() + " ")
                messages.append({"role": "user", "content": user_input + f"\t<{datetime.now()}>\n" })
                logs.write(" " + user_input + f"\t<{datetime.now()}>\n")

            else:
                user_input = input(f'\n{messages[len(messages) - 1]["content"]}'.strip() + " ")
                messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
                logs.write(" " + user_input + f"\t<{datetime.now()}>\n")
        except KeyboardInterrupt:
            messages.append({"role": "user", "content": "\n"})
            print("")
            break
        
        terminal_history.close()

if __name__ == "__main__":
    main()