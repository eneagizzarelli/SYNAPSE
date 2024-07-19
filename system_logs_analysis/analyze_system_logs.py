import os
import sys
import shutil
from collections import deque

SYNAPSE_path = "/home/enea/SYNAPSE/"
SYSTEM_LOGS_ANALYSIS_path = SYNAPSE_path + "system_logs_analysis/"

sys.path.append(SYNAPSE_path + "src")
from ai_requests import generate_response

analyzed_system_logs_path = SYSTEM_LOGS_ANALYSIS_path + "analyzed_system_logs/"
var_log_path = "/var/log/"

# CHANGE HERE NUM OF LINES TO ANALYZE FOR EACH LOG FILE
AUTH_NUM_LINES = 100
KERN_NUM_LINES = 50
SYSLOG_NUM_LINES = 50

def main():
    print("Starting logs analysis...\n")

    count_analysis_files = 0
    # create system logs directory if not exists
    if not os.path.exists(analyzed_system_logs_path):
        os.makedirs(analyzed_system_logs_path)
    else:
        # iterate over file in the analyzed_system_logs folder
        for analysis_file in os.listdir(analyzed_system_logs_path):
            # if analysis file is found
            if analysis_file.startswith("analysis_"):
                # increment number of analysis files
                count_analysis_files += 1
    current_analysis_file_path = analyzed_system_logs_path + "analysis_" + str(count_analysis_files) + ".txt"

    print("\tauth.log analysis started...")

    # copy auth.log file to "local" folder
    shutil.copy(var_log_path + "auth.log", analyzed_system_logs_path + "auth.log")
    
    auth_messages = [{"role": "system", "content": "Your role is to analyze the following 'auth.log' file of an Ubuntu Linux OS. " +
                      "Read it and schematize the aspects you think more relevant to consider. " +
                      "You just need to output the result of your analysis without additional chat-like text, no summaries, nothing explaining more than necessary. " +
                      "In case of multiple login attempts, group them by the same IP address. " +
                      "Be aware: your output will be written inside a .txt file, so avoid useless markup like '#' or '*'.\n\n"}]
    
    # open "local" auth.log file
    with open(analyzed_system_logs_path + "auth.log", "r") as auth_log_file:
        # read last AUTH_NUM_LINES lines
        auth_log_lines = deque(auth_log_file, maxlen=AUTH_NUM_LINES)
        # append lines to messages to send to AI
        auth_messages.append({"role": "system", "content": ''.join(auth_log_lines)})

    # check if auth.log file is empty
    if(len(auth_log_lines) == 0):
        auth_analysis = {"role": "assistant", "content": "No data found in 'auth.log' file."}
    else:
        # if not empty, generate response from AI
        auth_analysis = generate_response(auth_messages)

    # write analysis to file
    with open(current_analysis_file_path, "w") as analysis_file:
        analysis_file.write("---------- auth.log analysis ----------\n\n")
        analysis_file.write(auth_analysis["content"] + "\n\n")

    # remove "local" auth.log file
    os.remove(analyzed_system_logs_path + "auth.log")

    print("\tauth.log analysis completed.\n")

    print("\tkern.log analysis started...")

    # copy kern.log file to "local" folder
    shutil.copy(var_log_path + "kern.log", analyzed_system_logs_path + "kern.log")

    kern_messages = [{"role": "system", "content": "Your role is to analyze the following 'kern.log' file of an Ubuntu Linux OS. " +
                      "Read it and schematize the aspects you think more relevant to consider. " +
                      "You just need to output the result of your analysis without additional chat-like text, no summaries, nothing explaining more than necessary. " + 
                      "Be aware: your output will be written inside a .txt file, so avoid useless markup like '#' or '*'.\n\n"}]

    # open "local" kern.log file
    with open(analyzed_system_logs_path + "kern.log", "r") as kern_log_file:
        # read last KERN_NUM_LINES lines
        kern_log_lines = deque(kern_log_file, maxlen=KERN_NUM_LINES)
        # append lines to messages to send to AI
        kern_messages.append({"role": "system", "content": ''.join(kern_log_lines)})

    # check if kern.log file is empty
    if(len(kern_log_lines) == 0):
        kern_analysis = {"role": "assistant", "content": "No data found in 'kern.log' file."}
    else:
        # if not empty, generate response from AI
        kern_analysis = generate_response(kern_messages)

    # write analysis to file
    with open(current_analysis_file_path, "a") as analysis_file:
        analysis_file.write("---------- kern.log analysis ----------\n\n")
        analysis_file.write(kern_analysis["content"] + "\n\n")

    # remove "local" kern.log file
    os.remove(analyzed_system_logs_path + "kern.log")

    print("\tkern.log analysis completed.\n")

    print("\tsyslog analysis started...")

    # copy syslog file to "local" folder
    shutil.copy(var_log_path + "syslog", analyzed_system_logs_path + "syslog")

    syslog_messages = [{"role": "system", "content": "Your role is to analyze the following 'syslog' file of an Ubuntu Linux OS. " +
                      "Read it and schematize the aspects you think more relevant to consider. " +
                      "You just need to output the result of your analysis without additional chat-like text, no summaries, nothing explaining more than necessary. " +
                      "Be aware: your output will be written inside a .txt file, so avoid useless markup like '#' or '*'.\n\n"}]

    # open "local" syslog file
    with open(analyzed_system_logs_path + "syslog", "r") as syslog_file:
        # read last SYSLOG_NUM_LINES lines
        syslog_lines = deque(syslog_file, maxlen=SYSLOG_NUM_LINES)
        # append lines to messages to send to AI
        syslog_messages.append({"role": "system", "content": ''.join(syslog_lines)})

    # check if syslog file is empty
    if(len(syslog_lines) == 0):
        syslog_analysis = {"role": "assistant", "content": "No data found in 'syslog' file."}
    else:
        # if not empty, generate response from AI
        syslog_analysis = generate_response(syslog_messages)

    # write analysis to file
    with open(current_analysis_file_path, "a") as analysis_file:
        analysis_file.write("---------- syslog analysis ----------\n\n")
        analysis_file.write(syslog_analysis["content"])

    # remove "local" syslog file
    os.remove(analyzed_system_logs_path + "syslog")

    print("\tsyslog analysis completed.\n")

    print("Logs analysis finished.")

if __name__ == "__main__":
    main()