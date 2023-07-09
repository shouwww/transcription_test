import os
import openai


class GptCtrl():

    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.amount_tokens = 0
        self.chat = []
        self.model = 'gpt-3.5-turbo'
    # End def

    def set_model(self, model_name):
        self.model = model_name
    # End def

    def set_content(self, content):
        self.chat.append({"role": "system", "content": content})
    # End def

    def tolk_gpt(self, input):
        self.chat.append({"role": "user", "content": input})
        response = openai.ChatCompletion.create(model=self.model, messages=self.chat)
        msg = response["choices"][0]["message"]["content"].lstrip()
        self.amount_tokens += response["usage"]["total_tokens"]
        self.chat.append({"role": "assistant", "content": msg})
        return msg
# End class


def main():
    gpt = GptCtrl()
    while True:
        user = input("<あなた>\n")
        if user == "q" or user == "quit":
            print(f"トークン数は{gpt.amount_tokens}でした。")
            break
        else:
            ret = gpt.tolk_gpt(user)
            print('<GPT>')
            print(ret)


if __name__ == "__main__":
    main()
