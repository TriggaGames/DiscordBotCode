class AIBot: 
    
    '''AI bot that handles conversation with AI model'''
    
    def __init__(self, token: str, model: str = "gpt-5-nano"): 
        from typing import Any
        import os

        if os.path.exists("message_history.json") is False: 
            import json
            with open("message_history.json", "w") as j: 
                json.dump([], j, indent=4)
        
        # Base ai necessities
        self.__token = token
        self.__model = model
        
        # Conversation history
        self.__messages: list[dict[str, Any]] = []
        
    def set_token(self, token: str): 
        '''Set ai token'''
        self.__token = token
        
    def set_model(self, model: str): 
        '''Set ai model'''
        self.__model = model

    def get_messages(self): 
        '''Return message history'''
        return self.__messages

    def append_messages(self, role: str, msg: str) -> None: 
        '''
        Append message with role to message history
        
        Params: 
            role: system (background info), user (user responses), assistant (AI)
            msg: message the role made
        '''
        
        # Create ai processable message
        ai_msg = {
            "role": role, 
            "content": msg
        }
        
        # Append to message history
        self.__messages.append(ai_msg)

    def clear_messages(self) -> None: 
        '''Clear contained message history'''
        self.__messages = []
        
    def load_messages(self, messages: list[dict]) -> None: 
        '''Load message history from saved json file'''
        self.__messages = messages
        
    def talk_to_llm(self) -> None: 
        '''Talk to AI using stored messages'''
        from openai import OpenAI
        # Create client instance
        client = OpenAI(api_key=self.__token)
        # Generate AI response based on stored messages
        response = client.responses.create(
            model=self.__model,
            input=self.__messages,
            store=True
        )        
        msg = response.output_text
        self.append_messages("assistant", msg)