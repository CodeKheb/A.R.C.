import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

model = Model("assets/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()

voice_command = None

def callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))

def listen():
    global voice_command

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    voice_command = text

def get_voice_command():
    global voice_command
    cmd = voice_command
    voice_command = None
    return cmd
