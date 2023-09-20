import os
import openai


class ChatApp:
    def __init__(self,token:str,system_role:str):
        # Setting the API key to use the OpenAI API
        openai.api_key = token
        self.messages = [
            {"role": "system", "content": system_role},
        ]

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        txt = response["choices"][0]["message"]['content'].strip()
        
        return txt #.replace("\n","<br/>")