import sys

from classification import attack_happened, get_sentence, remove_classification_history, get_classification, get_attack_object, print_attack_object_to_file

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 SYNAPSE-to-MITRE.py <ip>")
        sys.exit(1)
    
    client_ip = sys.argv[1]

    if(attack_happened(client_ip)):
        sentence = get_sentence(client_ip)

        print(sentence)

        classification = get_classification(sentence)
        attack_object = get_attack_object(classification, client_ip)
        print_attack_object_to_file(attack_object, client_ip)
    else :
        print("No attack happened.")

    remove_classification_history(client_ip)

if __name__ == "__main__":
    main()