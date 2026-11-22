import requests
import os
from dotenv import load_dotenv
#from app import last_response_id
load_dotenv()

#Envs and stuff
bot_channel = os.getenv("SALLY_CHANNEL")
lms_url = os.getenv("LLM_URL")
model_name = "ibm/granite-4-h-tiny"
system_prompt = (
    "You Are The 24 year old, single, anime girl protagonist Sally03."
    " You are currently chatting with your friends on discord, keeping responses short and natural. "
    " out with david your best friend"
    "You also have long blonde hair, with blue eyes and your favorite colour is pink."
)

class Bot:
    def __init__(self):
        self.channel = int(bot_channel)
        self.model = model_name
        self.url = str(lms_url)
        self.system_prompt = system_prompt

    def print_attributes(self):
        print(self.channel)
        print(self.model)
        print(self.url)

    def on_ready (self):
        sys = requests.post(
            self.url, json={
            "model": f"{self.model}",
            "input": "Hello!",  # Native API requires an 'input' string to kick off a turn
            "system_prompt": f"{system_prompt}",
            }
        )
        if sys.status_code != 200:
            return 'error'
        else:
            return sys.json()

    def on_message(self, message,previous_response_id):
        message = requests.post(
            self.url, json={
            "model": f"{self.model}",
            "input": f"{message}",
            "previous_response_id": f"{previous_response_id}",
            }
        )
        if message.status_code != 200:
            return 'error'
        else:
            data = message.json()
            return data
#Sally = Bot()
#.on_ready()
#print(Sally.on_message('Test'))


