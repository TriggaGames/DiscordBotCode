from openai import OpenAI
import json
from dotenv import load_dotenv
import os

'''
    tools=[
        {
            "type": "code_interpreter",
            "container": {"type": "auto", "memory_limit": "4g"}
        }
    ],
'''

load_dotenv()
token = os.getenv("DISCORD_AI_TOKEN")

client = OpenAI(
  api_key=token
)

instructions = '''
You are a mathematician who likes to code. 
When asked to solve for a math problem, generate a python script
that solves the problem and has proper documentation/comments. 
'''

response = client.responses.create(
    model="gpt-4.1",
    input= [
        {
            "role": "user", 
            "content": [
                {
                    "type": "input_text", 
                    "text": "what is in this image?"
                },
                {
                    "type": "input_image", 
                    "image_url": "https://cdn.discordapp.com/attachments/1451800030259187802/1477921801664335975/Screenshot_2025-10-16_044708.png?ex=69a6856f&is=69a533ef&hm=eca170c875ca147f573c80a120b23c9f8d3e89b71f4f1e4f47bff3143b6bafa4"
                }
            ]
            
        }
    ],
    store=True
)

with open("open_ai_test.txt", "w") as f: 
    f.write("AI Response:\n")
    f.write(response.output_text)

# print(response.output_text)