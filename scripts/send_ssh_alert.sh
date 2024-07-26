#!/bin/bash

# Requires previous "~/.msmtprc" file configuration

# Run this script using e.g.
# "session optional /usr/lib/aarch64-linux-gnu/security/pam_exec.so /home/send_ssh_alert.sh"

# email details
TO="eneagizzarelli2000@gmail.com"
SUBJECT=""
BODY=""

# configure date format
DATE=$(date -d "+2 hours" +"%d/%m/%Y - %H:%M:%S")

BODY+="<p><b>Honeypot</b>: SYNAPSE</p>"
BODY+="<p><b>User</b>: $PAM_USER</p>"
BODY+="<p><b>IP</b>: $PAM_RHOST</p>"
BODY+="<p><b>Date</b>: $DATE</p>"

# Send email using msmtp
case "$PAM_TYPE" in
  open_session)
    SUBJECT="SYNAPSE - SSH Login Alert"
    BODY+="<p><b>Type</b>: Login</p>"
    ;;
  close_session)
    SUBJECT="SYNAPSE - SSH Logout Alert"
    BODY+="<p><b>Type</b>: Logout</p>"
    ;;
esac

echo -e "To: $TO\nSubject: $SUBJECT\nContent-Type: text/html\n\n$BODY" | msmtp -a default $TO