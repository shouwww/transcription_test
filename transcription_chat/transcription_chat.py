import os
import sys
base_path = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(base_path, '.'))
import time
import threading
import requests
import json
import pyaudio
import streamlit as st

from libs.whisper_check import WhisperCtrl
from libs.record_audio import RecordMic
from libs.chat_gpt import GptCtrl


class Worker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.should_stop = threading.Event()
        self.whisper = None
        self.mic = None
        self.trans_txt = ''
        self.trans_comp = False
        self.state_is_running = False
    # End def

    def set_clsses(self, whisper, mic):
        self.whisper = whisper
        self.mic = mic

    def set_model(self, model):
        self.whisper.set_model(model=model)

    def run(self):
        self.trans_txt = ''
        self.state_is_running = True
        self.mic.start_rec()
        self.whisper.start_a2t()
        while not self.should_stop.wait(1):
            if self.whisper.transcribe_queue.empty():
                pass
            else:
                trans_data = self.whisper.transcribe_queue.get()
                self.trans_txt = self.trans_txt + trans_data['text']
        # End while
        self.mic.stop_rec()
        while self.mic.rec_thread.is_alive():
            time.sleep(1)
        self.whisper.stop_a2t()
        while self.whisper.a2t_thread.is_alive():
            time.sleep(1)
        while True:
            if self.whisper.transcribe_queue.empty():
                break
            else:
                trans_data = self.whisper.transcribe_queue.get()
                self.trans_txt = self.trans_txt + trans_data['text']
        self.state_is_running = False
        self.trans_comp = True
        print('app: stop woker')
    # End def

    def __del__(self):
        self.mic.stop_rec()
        self.whisper.stop_a2t()
        print('app: worker del')
# End class


class Speaker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.should_stop = threading.Event()
        self.base_html = 'http://127.0.0.1:50021/'
    # End def

    def set_info(self, speaker_id, text):
        self.speraker_id = speaker_id
        self.text = text

    def run(self):
        param = {'text': self.text, 'speaker': self.speraker_id}
        r1 = requests.post(self.base_html + 'audio_query', params=param)
        param = {'speaker': self.speraker_id}
        r2 = requests.post(self.base_html + 'synthesis', params=param, data=json.dumps(r1.json()))
        data = r2.content
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        time.sleep(0.2)
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
# End class


def main():
    st.set_page_config(page_title="chat test", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")
    st.title("chat")

    USER_NAME = "user"
    ASSISTANT_NAME = "assistant"

    # init session
    if 'worker' not in st.session_state:
        st.session_state.worker = None
    worker = st.session_state.worker
    if 'whisper' not in st.session_state:
        st.session_state.whisper = WhisperCtrl()
    if 'mic' not in st.session_state:
        st.session_state.mic = RecordMic()
    if 'gpt' not in st.session_state:
        st.session_state.gpt = GptCtrl()
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []
    if "model_name" not in st.session_state:
        st.session_state['model_name'] = 'tiny'
    if "trans_txt" not in st.session_state:
        st.session_state['trans_txt'] = ''

    with st.sidebar:
        whisper_model = st.selectbox('whisper model', ('tiny', 'base', 'small', 'medium', 'large'))
        if whisper_model != st.session_state['model_name']:
            st.session_state.whisper.set_model(whisper_model)
            st.session_state['model_name'] = whisper_model
        # End if
        gpt_model = st.selectbox('GPT model', ('gpt-3.5-turbo', 'gpt-4', 'gpt-4-32k'))
        if gpt_model:
            st.session_state.gpt.set_model(gpt_model)
        # End if
        st.write(f'token {st.session_state.gpt.amount_tokens}')
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Start_rec_trans', disabled=worker is not None):
                st.session_state['trans_txt'] = ''
                worker = st.session_state.worker = Worker(daemon=True)
                st.session_state.worker.set_clsses(st.session_state.whisper, st.session_state.mic)
                st.session_state.worker.start()
                st.experimental_rerun()
        with col2:
            if st.button('Stop_rec_trans', disabled=worker is None):
                st.session_state.worker.should_stop.set()
                # wait finish worker
                st.session_state.worker.join()
                st.session_state['trans_txt'] = st.session_state.worker.trans_txt
                del st.session_state.worker
                st.session_state.worker = None
                worker = st.session_state.worker = None
                st.experimental_rerun()
        with col3:
            if st.button('reload'):
                st.session_state.trans_txt = ''
            # End if
        # End with
        placeholder = st.empty()
        if worker is None:
            placeholder.markdown(f'script md:{st.session_state.trans_txt}')
        else:
            while worker.is_alive():
                placeholder.markdown(f'[rec]script md:{st.session_state.worker.trans_txt}')
                time.sleep(1)
    # End sidber

    user_msg = st.chat_input("ここにメッセージを入力")
    if user_msg or st.session_state['trans_txt'] != '':
        # Show previous chat logs
        for chat in st.session_state.chat_log:
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])

        # Show latest messages
        if user_msg:
            pass
        else:
            user_msg = st.session_state['trans_txt']
        # End if
        assistant_msg = "もう一度入力してください"
        with st.chat_message(USER_NAME):
            st.write(user_msg)
        with st.chat_message(ASSISTANT_NAME):
            st.write(assistant_msg)

        sperker = Speaker(daemon=True)
        sperker.set_info(speaker_id=1, text=assistant_msg)
        sperker.start()

        # Add Chat Log
        st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
        st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
        user_msg = ''


if __name__ == '__main__':
    main()
