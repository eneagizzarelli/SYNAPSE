#!/bin/bash

# Requires previous "~/.msmtprc" file configuration

# Run this script every minute using e.g.
# crontab -e
# "* * * * * /home/monitor_env_file_access.sh"
# after configuring an auditctl rule like e.g.
# "-w /home/enea/.env -p r -k env_file_access"

ENV_FILE_PATH="/home/enea/.env"
AUDIT_KEYWORD="env_file_access"
TO="eneagizzarelli2000@gmail.com"
SUBJECT="SYNAPSE - File Access Alert"
BODY=""

current_time=$(date "+%H:%M:%S")
one_minute_ago=$(date -d "-1 minutes" "+%H:%M:%S")
current_time_two_hours=$(date -d "+2 hours" "+%H:%M")
one_minute_ago_two_hours=$(date -d "+2 hours -1 minutes" "+%H:%M")

BODY+="<p>Unauthorized <b>file accesses</b> in the last minute (from <b>$one_minute_ago_two_hours</b> to <b>$current_time_two_hours</b>):</p><br>"

# Check audit logs for file access events in the last minute
audit_logs=$(ausearch --input-logs -k "$AUDIT_KEYWORD" --start today "$one_minute_ago" --end today "$current_time")

# Filter out entries related to Python and extract relevant info
filtered_logs=$(echo "$audit_logs" | awk '
  /type=PROCTITLE/ { proctitle=$0 }
  /type=SYSCALL/ { syscall=$0 }
  /type=PATH/ { path=$0 }
  /type=CWD/ { cwd=$0 }
  /time->/ { timestamp=$0 }
  function add_two_hours(ts) {
    # Convert the timestamp string to seconds since epoch, add two hours (7200 seconds), then format
    cmd = "date -d \"" ts " + 2 hours\" \"+%d/%m/%Y - %H:%M:%S\""
    cmd | getline result
    close(cmd)
    return result
  }
  {
    if ($0 ~ /comm="python3"/ || $0 ~ /exe="\/usr\/bin\/python3.10"/) {
      skip=1
    } else if ($0 ~ /^----$/) {
      if (skip == 0 && proctitle && syscall && path && cwd && timestamp) {
        # Extract relevant information
        match(timestamp, /time->(.*)/, t); raw_timestamp=t[1]
        formatted_timestamp = add_two_hours(raw_timestamp)
        match(proctitle, /proctitle=(.*)/, a); proctitle=a[1]
        match(syscall, /syscall=([^ ]+) /, b); syscall_info=b[1]
        match(syscall, /comm=([^ ]+)/, c); command=c[1]; gsub(/"/, "", command)
        match(syscall, / pid=([^ ]+)/, d); pid=d[1]
        match(syscall, / ppid=([^ ]+)/, e); ppid=e[1]
        match(path, /name="([^"]+)" inode=([^ ]+) dev=([^ ]+) mode=([^ ]+) ouid=([^ ]+) ogid=([^ ]+) rdev=([^ ]+) nametype=([^ ]+)/, f); filepath=f[1] " (inode: " f[2] ", dev: " f[3] ", mode: " f[4] ", UID: " f[5] ", GID: " f[6] ")"
        match(cwd, /cwd="([^"]+)"/, g); cwdpath=g[1]
        print "<p><b>File</b>: " filepath "</p>" \
              "<p><b>Command</b>: " command "</p>" \
              "<p><b>Syscall</b>: " syscall_info "</p>" \
              "<p><b>PID</b>: " pid " <b>PPID</b>: " ppid "</p>" \
              "<p><b>CWD</b>: " cwdpath "</p>" \
              "<p><b>PROCTITLE</b>: " proctitle "</p>" \
              "<p><b>Date</b>: " formatted_timestamp "</p><br>"
      }
      skip=0
      timestamp=""
      proctitle=""
      syscall=""
      path=""
      cwd=""
    }
  }
  END {
    if (skip == 0 && proctitle && syscall && path && cwd && timestamp) {
        match(timestamp, /time->(.*)/, t); raw_timestamp=t[1]
        formatted_timestamp = add_two_hours(raw_timestamp)
        match(proctitle, /proctitle=(.*)/, a); proctitle=a[1]
        match(syscall, /syscall=([^ ]+) /, b); syscall_info=b[1]
        match(syscall, /comm=([^ ]+)/, c); command=c[1]; gsub(/"/, "", command)
        match(syscall, / pid=([^ ]+)/, d); pid=d[1]
        match(syscall, / ppid=([^ ]+)/, e); ppid=e[1]
        match(path, /name="([^"]+)" inode=([^ ]+) dev=([^ ]+) mode=([^ ]+) ouid=([^ ]+) ogid=([^ ]+) rdev=([^ ]+) nametype=([^ ]+)/, f); filepath=f[1] " (inode: " f[2] ", dev: " f[3] ", mode: " f[4] ", UID: " f[5] ", GID: " f[6] ")"
        match(cwd, /cwd="([^"]+)"/, g); cwdpath=g[1]
        print "<p><b>File</b>: " filepath "</p>" \
              "<p><b>Command</b>: " command "</p>" \
              "<p><b>Syscall</b>: " syscall_info "</p>" \
              "<p><b>PID</b>: " pid " <b>PPID</b>: " ppid "</p>" \
              "<p><b>CWD</b>: " cwdpath "</p>" \
              "<p><b>PROCTITLE</b>: " proctitle "</p>" \
              "<p><b>Date</b>: " formatted_timestamp "</p><br>"
}
  }
')

if [ -n "$filtered_logs" ]; then
  BODY+="$filtered_logs"

  echo -e "To: $TO\nSubject: $SUBJECT\nContent-Type: text/html\n\n$BODY" | msmtp -a default $TO
fi