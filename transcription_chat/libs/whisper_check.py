import os
import glob
import time
import threading
import pyaudio
import wave
import queue
import whisper


class WhisperCtrl():

    def __init__(self, tmp_dir='datas'):
        self.wav_dir = tmp_dir
        self.stop_event = threading.Event()
        self.a2t_thread = None
        self.file_len = 0
        self.transcribe_queue = queue.Queue()
        self.state_run = False
        self.model = whisper.load_model('tiny')
        print(f'whis:dir={self.wav_dir}')
    # End def

    def set_model(self, model):
        del self.model
        self.model = whisper.load_model(model)
        print(f'whis:model changed {model}')
    # End def

    def start_a2t(self):
        self.stop_event = threading.Event()
        self.a2t_thread = threading.Thread(target=self._loop_a2t, args=(self.stop_event,))
        self.a2t_thread.start()
    # End def

    def stop_a2t(self):
        if not (self.a2t_thread is None):
            self.stop_event.set()
            self.a2t_thread.join()
            print('whis: stop')
        # End if
        return True
    # End def

    def _loop_a2t(self, stop_event):
        self.state_run = True
        print('whis: start')
        while not stop_event.wait(0.1):
            file_list = glob.glob(self.wav_dir + '/*.wav')
            self.file_len = len(file_list)
            print(f'whis:file len={self.file_len}')
            while self.file_len > 0:
                start_time = time.time()
                sorted(file_list, key=lambda f: os.stat(f).st_mtime, reverse=True)
                result = self.model.transcribe(file_list[0], language="ja")
                self.transcribe_queue.put_nowait(result)
                print(f'whis: transtime:{time.time() - start_time}, file={file_list[0]}')
                os.remove(file_list[0])
                file_list = glob.glob(self.wav_dir + '/*.wav')
                self.file_len = len(file_list)
            # End if
        # End while
        self.state_run = False
    # End def

    def get_txt_whisper(self):
        file_list = glob.glob(self.wav_dir + '/*.wav')
        if len(file_list) > 0:
            sorted(file_list, key=lambda f: os.stat(f).st_mtime, reverse=True)
            print(file_list)

    def __del__(self):
        print('whis:finish WhisperCtrl')
    # End def
# End class


def main():
    w2t = WhisperCtrl()
    w2t.get_txt_whisper()
    w2t.start_a2t()
    time.sleep(10)
    while True:
        print(f'len:{w2t.file_len}, state:{w2t.state_run}')
        if (w2t.file_len == 0) and (w2t.state_run is True):
            break
        # End if
    # End while
    while True:
        if w2t.transcribe_queue.empty():
            break
        else:
            print(w2t.transcribe_queue.get())
    w2t.stop_a2t()


if __name__ == "__main__":
    main()
