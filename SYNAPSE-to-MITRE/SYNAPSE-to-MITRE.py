import os

from classification import attack_happened, get_sentence, remove_classification_history, get_classification, get_attack_object, print_attack_object_to_file

logs_path = "/home/enea/SYNAPSE/logs/"

def main():
    print("Starting SYNAPSE-to-MITRE mapping...\n")
    
    # iterate over all client IPs previously connected to the server
    for client_ip in os.listdir(logs_path): 
        if os.path.isdir(logs_path + client_ip):

            print("IP: " + client_ip + "\n")

            # get all classification history files for the current client IP
            classification_files = [
                f for f in os.listdir(logs_path + client_ip)
                if os.path.isfile(logs_path + client_ip + "/" + f) and f.startswith(client_ip + "_classification_history_")
            ]

            # sort the classification files in ascending order
            classification_files.sort()

            # iterate over all classification history files
            for classification_file in classification_files:
                print("- " + classification_file + ": ", end="")

                # check if attack happened by asking AI
                if(attack_happened(classification_file, client_ip)):

                    print("Attack happened.\n")

                    # if attack happened, get unstructured CTI sentence from AI
                    sentence = get_sentence(classification_file, client_ip)

                    print("\tUnstructured CTI: " + sentence + "\n")

                    # get attack ID and attack object from unstructured CTI sentence
                    classification = get_classification(sentence)
                    attack_object = get_attack_object(classification)
                    # print sentence and attack object to file
                    print_attack_object_to_file(attack_object, sentence, client_ip)
                # attack not happened
                else :
                    print("No attack happened.\n")
                
                # remove classification history file after processing
                remove_classification_history(classification_file, client_ip)

    print("SYNAPSE-to-MITRE mapping finished.")

if __name__ == "__main__":
    main()