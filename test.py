import json

'''
[
    {
        "role": "assistant", 
        "content": "Your mom gay"
    }
]
'''

with open("test.json", "r") as j: 
    data = json.load(j)

data.append({"role": "your mom", "content": "you're gay"})

with open("test.json", "w") as j: 
    json.dump(data, j, indent=4)