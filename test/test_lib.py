from transcription_chat.lib.whisper_check import WhisperCtrl
from transcription_chat.lib.record_audio import RecordMic
import time

whis = WhisperCtrl()
rec_mic = RecordMic()

rec_mic.start_rec()
whis.start_a2t()
time.sleep(30)
rec_mic.stop_rec()
whis.stop_a2t()
while True:
    if whis.transcribe_queue.empty():
        break
    else:
        trans_data = whis.transcribe_queue.get()
        print(trans_data['text'])
