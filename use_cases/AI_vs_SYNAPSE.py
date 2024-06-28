import sys
import subprocess

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

process = subprocess.Popen(
    ['python3', 'SYNAPSE.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

while True:
    output = process.stdout.readline()
    if output:
        print(f"Script output: {output.strip()}")
    else:
        break

process.stdin.close()
process.stdout.close()
process.stderr.close()
process.wait()