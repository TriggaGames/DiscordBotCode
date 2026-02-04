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
  tools=[
      {
          "type": "code_interpreter",
          "container": {"type": "auto", "memory_limit": "4g"}
      }
  ],
  input="Can you create a python script solves for 1 + 1?",
  instructions=instructions,
  store=True
)

with open("open_ai_test.txt", "w") as f: 
    f.write("AI Response:\n")
    f.write(response.output_text)

# print(response.output_text)