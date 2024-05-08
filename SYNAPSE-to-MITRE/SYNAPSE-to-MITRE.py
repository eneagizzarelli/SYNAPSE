import os

from classification import attack_happened, get_sentence, remove_classification_history, get_classification, get_attack_object, print_attack_object_to_file

ssh_client_info = os.getenv('SSH_CLIENT')

if ssh_client_info:
    client_ip = ssh_client_info.split()[0]

print(client_ip)

base_path = "/home/user/SYNAPSE/logs/"

def main():
    pass
    # for classification_file in os.listdir(base_path):
    #     if os.path.isfile(base_path + classification_file):
    #         client_ip = classification_file.split('_')[0]
    # if(attack_happened()):
    #     sentence = get_sentence()

    #     print(sentence)

    #     classification = get_classification(sentence)
    #     attack_object = get_attack_object(classification)
    #     print_attack_object_to_file(attack_object)
    # else :
    #     print("No attack happened.")

    # remove_classification_history()

if __name__ == "__main__":
    main()