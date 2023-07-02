import time
import whisper
import pyaudio
import wave

start_time = time.time()
model = whisper.load_model("medium")
load_time = time.time() - start_time
start_time = time.time()
result = model.transcribe("test/test.mp3", verbose=True, language="ja")
print(result["text"])
elapsed_time = time.time() - start_time
print(f'load time:{load_time}')
print(f'elapsed time:{elapsed_time}')
