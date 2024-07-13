import os
import json

from classification import attack_happened, get_sentence, rename_classification_history, remove_classification_history, get_classifications, get_attack_objects, print_attack_objects_to_file

logs_path = "/home/enea/SYNAPSE/logs/"

def main():
    print("Starting SYNAPSE-to-MITRE mapping...\n")
    
    # iterate over all client IPs previously connected to the server
    for client_ip in os.listdir(logs_path): 
        if os.path.isdir(logs_path + client_ip):
            
            ip_reputation = 0
            with open(logs_path + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
                # load client data structure and extract IP reputation
                data = json.load(client_data_file)
                ip_reputation = data["ip_info"]["reputation"]

            print("IP: " + client_ip + " (reputation = " + str(ip_reputation) + ")\n")

            # get all classification history files for the current client IP
            classification_files = [
                f for f in os.listdir(logs_path + client_ip + "/" + client_ip + "_attacks")
                if os.path.isfile(logs_path + client_ip + "/" + client_ip + "_attacks/" + f) and f.startswith(client_ip + "_classification_history_")
            ]

            # sort the classification files in ascending order
            classification_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

            # iterate over all classification history files
            for classification_file in classification_files:
                print("- " + classification_file + ": ", end="")

                # check if attack happened by asking AI
                if(attack_happened(classification_file, client_ip, ip_reputation)):

                    print("Attack happened.\n")

                    # if attack happened, get unstructured CTI sentence from AI
                    sentence = get_sentence(classification_file, client_ip)

                    print("\tUnstructured CTI: " + sentence + "\n")

                    # get top three attack IDs and attack objects from unstructured CTI sentence
                    top_3_classifications = get_classifications(sentence)
                    attack_objects = get_attack_objects(top_3_classifications)
                    # print sentence and attack objects to file
                    attack_directory_number = print_attack_objects_to_file(attack_objects, sentence, client_ip)

                    # rename and move classification history into attack history file after processing
                    rename_classification_history(classification_file, attack_directory_number, client_ip)
                # attack not happened
                else :
                    print("No attack happened.\n")

                    # remove classification history file after processing
                    remove_classification_history(classification_file, client_ip)

    print("SYNAPSE-to-MITRE mapping finished.")

if __name__ == "__main__":
    main()