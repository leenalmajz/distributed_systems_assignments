from typing import List
class AuthenticationManager():
    def __init__(self, admin_tokens: List[str], agent_tokens: List[str]):
        self.admin_tokens = admin_tokens
        self.agent_tokens = agent_tokens

    def auth_admin(self, token: str):
        if token in self.admin_tokens:
            return True
        return False
    
    def auth_any(self, token: str):
        if token in self.admin_tokens or token in self.agent_tokens:
            return True
        return False