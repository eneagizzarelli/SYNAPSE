import sys
import subprocess
import select

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

process = subprocess.Popen(
    ['python3', '../src/SYNAPSE.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

while True:
    ready, _, _ = select.select([process.stdout], [], [], 1.0)

    if ready:
        output = process.stdout.readline()
        if output:
            print(f"Script output: {output.strip()}")
        else:
            print("suca1")
            break

    if process.poll() is not None:
        print("suca2")
        break

process.stdin.close()
process.stdout.close()
process.stderr.close()
process.wait()