from typing import Union
from openai import OpenAI


class AIBot(OpenAI): 

    '''AI bot that handles conversation with AI model'''
    
    def __init__(self, token: str, model: str = "gpt-5-nano"): 
        from typing import Any
        import os
        
        super().__init__(api_key=token)

        if os.path.exists("message_history.json") is False: 
            import json
            with open("message_history.json", "w") as j: 
                json.dump([], j, indent=4)
        
        # Set model
        self.__model = model
        
        # Conversation history
        self.__messages: list[dict[str, Any]] = []
        
        # Tools
        # TODO: Add tools for later use
        self.__tools: list[dict[str, Any]] = []
        
    def set_model(self, model: str): 
        '''Set ai model'''
        self.__model = model

    def get_model(self) -> str: 
        '''Return ai model'''
        return self.__model

    def get_messages(self): 
        '''Return message history'''
        return self.__messages

    def append_messages(self, role: str, content: Union[str, list]) -> None: 
        '''
        Append message with role to message history
        
        Params: 
            role: system (background info), user (user responses), assistant (AI)
            msg: message the role made
        '''
        
        # Create ai processable message
        ai_msg = {
            "role": role, 
            "content": content
        }
        
        # Append to message history
        self.__messages.append(ai_msg)

    def clear_messages(self) -> None: 
        '''Clear contained message history'''
        self.__messages = []
        
    def load_messages(self, messages: list[dict]) -> None: 
        '''Load message history from saved json file'''
        self.__messages = messages
        
    def upload_files(self, filename: str, )
        
    def talk_to_llm(self) -> None: 
        '''Talk to AI using stored messages'''
        # Generate AI response based on stored messages
        response = self.responses.create(
            model=self.__model,
            input=self.__messages,
            tools=self.__tools
        )        
        msg = response.output_text
        self.append_messages("assistant", msg)