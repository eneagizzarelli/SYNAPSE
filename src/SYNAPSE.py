import time

from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation
from client_data import initialize_client_data, increment_client_number_of_connections, write_client_session_duration_in_seconds
from classification import attack_happened, get_sentence, get_classification, get_attack_object, print_attack_object

def main():
    initialize_client_data()
    increment_client_number_of_connections()
    
    terminal_prompt = load_terminal_prompt()
    args = parse_terminal_argument(terminal_prompt)
    terminal_messages = load_terminal_messages(args.terminal_personality)

    session_start_time = time.time()

    try:
        terminal_simulation(terminal_messages)
    except KeyboardInterrupt:
        print("\nlogout")
    except EOFError:
        print("\nlogout")

    session_end_time = time.time()
    session_duration_in_seconds = session_end_time - session_start_time
    session_duration_in_seconds = round(session_duration_in_seconds, 2)
    write_client_session_duration_in_seconds(session_duration_in_seconds)

    if(attack_happened()):
        sentence = get_sentence()

        print("Attack happened.")

        # classification = get_classification(sentence)
        # attack_object = get_attack_object(classification)
        # print_attack_object(attack_object)
    else :
        print("No attack happened.")

if __name__ == "__main__":
    main()