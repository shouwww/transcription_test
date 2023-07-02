import pyaudio
import wave

# 録音する時間（秒）
RECORD_SECONDS = 5
# 音声ファイル名
WAVE_OUTPUT_FILENAME = "output.wav"

# 録音デバイスの設定
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

print("録音開始")

# 音声データを格納するリスト
frames = []

# 録音開始
for i in range(0, int(44100 / 1024 * RECORD_SECONDS)):
    data = stream.read(1024)
    frames.append(data)

print("録音終了")

# 録音デバイスを閉じる
stream.stop_stream()
stream.close()
audio.terminate()

# 音声データをファイルに保存
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(1)
wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(frames))
wf.close()

print("保存完了")
