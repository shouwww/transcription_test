import os
import math
import pyaudio
import numpy as np
import threading
import wave
import queue
import time


class RecordMic:

    def __init__(self, temp_dir='datas'):
        self.audio_name_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.record_second = 5
        self.tmp_dir = temp_dir
        self.silence_db = 50
        self.silent_cnt = 0
        os.makedirs(self.tmp_dir, exist_ok=True)
        self.rec_thread = None
        self.audio = pyaudio.PyAudio()
        print(f'mic:{self.tmp_dir}')
        # End for
    # End def

    def get_devices(self):
        self.audio = pyaudio.PyAudio()
        ret_datas = []
        for index in range(0, self.audio.get_device_count()):
            ret_datas.append(self.audio.get_device_info_by_index(index))
        # End for
        return ret_datas
    # End def

    def start_rec(self):
        print('mic:start rec')
        self.stop_event = threading.Event()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.rec_thread = threading.Thread(target=self._loop_rec, args=(self.stop_event,))
        self.rec_thread.start()
    # End def

    def _calc_db(self, frame):
        iframe = []
        for buf in frame:
            data = np.frombuffer(buf, dtype="int16")
            iframe.append(max(data))
        rms = (max(iframe))
        db = 20 * math.log10(rms) if rms > 0.0 else -math.inf
        return db
    # End def

    def set_silence_db(self, db_value):
        self.silence_db = db_value
    # End def

    def get_silence_db(self):
        return self.silence_db
    # End def

    def _save_tmp_wav(self, file_name, frame):
        db = self._calc_db(frame=frame)
        is_save = False
        if db > self.silence_db:
            wf = wave.open(file_name, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frame))
            wf.close()
            self.silent_cnt = 0
            is_save = True
        else:
            self.silent_cnt = self.silent_cnt + 1
            if self.silent_cnt > 4:
                self.stop_event.set()
            # End if
            is_save = False
        # End if
        print(f'mic:file name:{file_name}, RMS:{db}[db], save:{is_save}')
    # End def

    def stop_rec(self):
        print('mic:stop rec')
        if not (self.rec_thread is None):
            self.stop_event.set()
            self.rec_thread.join()
            print('mic:stop')
            self.stream.stop_stream()
            self.stream.close()
        return True
    # End def

    def _loop_rec(self, stop_event):
        cnt = 0
        while not stop_event.wait(0):
            frames = []
            for i in range(0, int(44100 / 1024 * self.record_second)):
                data = self.stream.read(1024)
                frames.append(data)
            # End for
            file_name = "_tmp_{}_.wav".format(cnt)
            file_path = os.path.join(self.tmp_dir, file_name)
            t = threading.Thread(target=self._save_tmp_wav, args=(file_path, frames,))
            t.start()
            # self.result_queue.put_nowait(frames)
            self.audio_name_queue.put_nowait(file_name)
            cnt = cnt + 1
        # End while
        t.join()
    # End deg

    def __del__(self):
        self.stop_rec()
        self.audio.terminate()
        print("mic:finish recording class")
    # End def
# End class


def main():
    rec_mic = RecordMic(temp_dir='datas')
    rec_mic.start_rec()
    time.sleep(15)
    rec_mic.stop_rec()
    while True:
        if rec_mic.audio_name_queue.empty():
            break
        else:
            print(rec_mic.audio_name_queue.get())


if __name__ == "__main__":
    main()
