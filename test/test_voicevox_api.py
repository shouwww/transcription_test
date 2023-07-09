import requests # APIを使う
import json # APIで取得するJSONデータを処理する
import pyaudio # wavファイルを再生する
import time # タイムラグをつける

# 文字列の入力
text = "私の名前はずんだもんです。東北地方の応援マスコットをしています。得意なことはしゃべることです。"

# 音声合成クエリの作成
res1 = requests.post('http://127.0.0.1:50021/audio_query',params = {'text': text, 'speaker': 1})
# 音声合成データの作成
res2 = requests.post('http://127.0.0.1:50021/synthesis',params = {'speaker': 1},data=json.dumps(res1.json()))
# 
data = res2.content

res3 = requests.get('http://127.0.0.1:50021/speakers')
res3.encoding = res3.apparent_encoding
print(res3)
print(type(res3))
print(res3.status_code)
#print(res3.content)
res3_json = res3.json()
for data in res3_json:
    print(data['name'])
    for style in data['styles']:
        print(style)


"""
# PyAudioのインスタンスを生成
p = pyaudio.PyAudio()

# ストリームを開く
stream = p.open(format=pyaudio.paInt16,  # 16ビット整数で表されるWAVデータ
                channels=1,  # モノラル
                rate=24000,  # サンプリングレート
                output=True)

# 再生を少し遅らせる（開始時ノイズが入るため）
time.sleep(0.2) # 0.2秒遅らせる

# WAV データを直接再生する
stream.write(data)  

# ストリームを閉じる
stream.stop_stream()
stream.close()

# PyAudio のインスタンスを終了する
p.terminate()
"""