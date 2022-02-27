from flask import Flask, request
from playsound import playsound
import os, time

app = Flask(__name__)

@app.route("/sound", methods=["POST"])
def sound():
    json = request.get_json()

    if not json:
        return "failed"

    state = json["state"]
    audio_file = None

    if state == "powerdown":
        msleep(1000) # Calibration.
        log_success("Playing powerdown audio")
        audio_file = os.path.join(os.path.dirname(__file__), "powerdown.wav")
        playsound(audio_file)

    elif state == "win":
        log_success("Playing win audio")
        audio_file = os.path.join(os.path.dirname(__file__), "impossible.wav") 
        playsound(audio_file)

    else:
        return "failed"
    
    return "success\n"

def msleep(ms):
    time.sleep(ms / 1000)

def log_success(data):
    """
    Log successful message.
    """
    print(f"\033[92m[{time.strftime('%Y-%m-%d %H:%M:%S')}]\033[0m {data}", flush=True)

if __name__ == "__main__":
    app.run()
