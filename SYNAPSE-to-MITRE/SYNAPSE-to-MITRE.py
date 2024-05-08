import os

from classification import attack_happened, get_sentence, remove_classification_history, get_classification, get_attack_object, print_attack_object_to_file

base_path = "/home/user/SYNAPSE/"

def main():
    for client_ip in os.listdir(base_path + "logs/"):
        if os.path.isdir(base_path + "logs/" + client_ip):
            for classification_file in os.listdir(base_path + "logs/" + client_ip):
                if os.path.isfile(base_path + "logs/" + client_ip + "/" + classification_file) and classification_file.startswith(client_ip + "_classification_history_"):
                    if(attack_happened(classification_file, client_ip)):
                        sentence = get_sentence(classification_file, client_ip)

                        print(sentence)

                        classification = get_classification(sentence)
                        attack_object = get_attack_object(classification)
                        print_attack_object_to_file(attack_object, client_ip)
                    else :
                        print("No attack happened.")

                    remove_classification_history(classification_file, client_ip)

if __name__ == "__main__":
    main()