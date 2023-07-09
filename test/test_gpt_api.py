import os
import openai


def test():
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "大谷翔平について教えて"},
        ],
    )
    print(response.choices[0]["message"]["content"].strip())


def main():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    amount_tokens = 0
    chat = []

    setting = input("ChatGPTに設定を加えますか？ y/n\n")
    if setting == "y" or setting == "Y":
        content = input("内容を入力してください。\n")
        chat.append({"role": "system", "content": content})

    print("チャットをはじめます。q または quit で終了します。")
    print("-"*50)
    while True:
        user = input("<あなた>\n")
        if user == "q" or user == "quit":
            print(f"トークン数は{amount_tokens}でした。")
            break
        else:
            chat.append({"role": "user", "content": user})

        print("<ChatGPT>")
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat)
        msg = response["choices"][0]["message"]["content"].lstrip()
        amount_tokens += response["usage"]["total_tokens"]
        print(msg)
        chat.append({"role": "assistant", "content": msg})


if __name__ == "__main__":
    main()
