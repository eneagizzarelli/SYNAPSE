import os
import json

from classification import get_ips_and_domains_from_classification_file, get_ip_reputation, get_domain_reputation, attack_happened, get_sentence, rename_classification_history, remove_classification_history, get_classifications, get_attack_objects, print_attack_objects_to_file

SYNAPSE_path = "/home/enea/SYNAPSE/"

logs_path = SYNAPSE_path + "logs/"

def main():
    print("Starting SYNAPSE-to-MITRE mapping...\n")
    
    # iterate over all client IPs previously connected to the server
    for client_ip in os.listdir(logs_path):
        logs_ip_path = logs_path + client_ip + "/"

        if os.path.isdir(logs_ip_path):
            logs_ip_attacks_path = logs_ip_path + client_ip + "_attacks/"
            
            client_ip_reputation = 0
            # load client data structure and extract IP reputation
            with open(logs_ip_path + client_ip + "_data.json", "r") as client_data_file:
                data = json.load(client_data_file)
                client_ip_reputation = data["ip_info"]["reputation"]

            print("IP: " + client_ip + " (reputation = " + str(client_ip_reputation) + ")\n")

            # get all classification history files for the current client IP
            classification_files = [
                f for f in os.listdir(logs_ip_attacks_path)
                if os.path.isfile(logs_ip_attacks_path + f) and f.startswith(client_ip + "_classification_history_")
            ]

            # sort the classification files in ascending order
            classification_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

            # iterate over all classification history files
            for classification_file in classification_files:
                print("- " + classification_file + ": ")

                # get IPs and domains from classification history file
                ips, domains = get_ips_and_domains_from_classification_file(classification_file, client_ip)
                
                ips_and_reputations = []
                # print IPs together with respective reputation
                print("\tIPs found:")
                for ip in ips:
                    ip_reputation = get_ip_reputation(ip)
                    ips_and_reputations.append((ip, ip_reputation))
                    print("\t\t- " + ip + " (reputation = " + str(ip_reputation) + ")")

                domains_and_reputations = []
                # print domains together with respective reputation
                print("\tDomains found:")
                for domain in domains:
                    domain_reputation = get_domain_reputation(domain)
                    domains_and_reputations.append((domain, domain_reputation))
                    print("\t\t- " + domain + " (reputation = " + str(domain_reputation) + ")")

                # check if attack happened by asking AI
                if(attack_happened(classification_file, client_ip, client_ip_reputation, ips_and_reputations, domains_and_reputations)):
                    print("\n\tAttack happened -> ", end="")

                    # if attack happened, get unstructured CTI sentence from AI
                    sentence = get_sentence(classification_file, client_ip)

                    print(sentence + "\n")

                    # get top three attack IDs and attack objects from unstructured CTI sentence
                    top_3_classifications = get_classifications(sentence)
                    attack_objects = get_attack_objects(top_3_classifications)
                    # print sentence and attack objects to file
                    attack_directory_number = print_attack_objects_to_file(attack_objects, sentence, client_ip)

                    # rename and move classification history into attack history file after processing
                    rename_classification_history(classification_file, attack_directory_number, client_ip)
                # attack not happened
                else :
                    print("\nNo attack happened.\n")

                    # remove classification history file after processing
                    remove_classification_history(classification_file, client_ip)

    print("SYNAPSE-to-MITRE mapping finished.")

if __name__ == "__main__":
    main()