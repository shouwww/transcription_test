# transcription_test

Practice a transcription program using OpenAI's automatic transcription "Whisper"

## Features

I use whisper for voice input.
Streamlit is used for GUI.
Chatbot's answers are considered using ChatGPTAPI.
The bot answers with text on the GUI. It also outputs voice. VOICEVOX is used for voice output.

## Requirement

This program uses the following libraries

* torch, torchaudio, torchvision
* streamlit
* whisper
* openai-whisper
* openai

## Installation

torch Previous Version <https://download.pytorch.org/whl/torch_stable.html>

```bash
pip install torch==1.13.1
pip install torchaudio==0.13.1
pip install torchvision==1.14.1
pip install streamlit
pip install whisper
pip install openai-whisper
pip install openai
```

VOICEVOXのインストール
<https://voicevox.hiroshiba.jp/>

## Usage

DEMOの実行方法など、"hoge"の基本的な使い方を説明する

windows

```bash
git clone https://github.com/shouwww/transcription_test.git
cd transcription_test
set OPENAI_API_KEY=sk-***
streamlit run transcription_chat\transcription_chat.py
```

## Note

This program is for personal programming practice.

## Author

* shouwwwwww
* <https://github.com/shouwww>

## License

"transcription_test" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
