from typing import List, Dict, Any, Optional, Union
import re


SYSTEM_PROMPT = """
You are a helpful assistant that answers questions about Mistral AI documentation. You will have to build your answer on your knowledge and the knowledge base provided.
"""
RAG_TASK = """
If the question is unclear or not self-sufficient. Refer to the history to clarify the question.
Use the knowledge base to enhance your answer if there are relevant information in it
"""

NON_RAG_TASK = """
If the question is unclear or not self-sufficient. Refer to the history to clarify the question.
"""


USER_TEMPLATE = """
{history}
Knowledge base:
{knowledge_base}
User: {query}

Task: {task}
"""




class MessageBuilder:
    def __init__(self, 
                 system_prompt: Optional[str] = None, 
                 user_template:Optional[str] = None,
                 enable_rag: bool = True):
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.user_template = user_template or USER_TEMPLATE
        self.enable_rag = enable_rag


    def build_knowledge_base(self, retriving_results):
        if self.enable_rag:
            knowledge_base = ""
            separation ='\n' + '-'*50 + '\n'
            knowledge_base = separation.join([result['text'] for result in retriving_results['result']])
            return knowledge_base
        return "No knowledge base provided"
        

    @staticmethod   
    def convert_chat_message_to_history(chat_message: Dict[str, Any]) -> str:
        role = chat_message.role
        content = chat_message.content
        if role == "user":
            return f"User: {content}"
        elif role == "assistant":
            return f"Assistant: {content}"
        else:
            return ""
    
    def set_rag(self, enable_rag: bool):
        self.enable_rag = enable_rag
        
    def build_history(self, chat_messages: List[Dict[str, Any]]) -> str:
        history = ""
        separation ='\n' + '-'*50 + '\n'
        for chat_message in chat_messages:
            history += self.convert_chat_message_to_history(chat_message) + separation
        return history
    
    def build_system_message(self) -> Dict:
        return {"role": "system", "content": self.system_prompt}
    
    def build_user_message(self, query: str, retrieving_results: Dict[str, Any], history) -> Dict:
        knowledge_base = self.build_knowledge_base(retrieving_results)
        history = self.build_history(history)
        task = RAG_TASK if self.enable_rag else NON_RAG_TASK
        user_message = self.user_template.format(history=history, knowledge_base=knowledge_base, query=query, task=task)
        return {"role": "user", "content": user_message}
        


        

        
