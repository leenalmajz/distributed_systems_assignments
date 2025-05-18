from typing import List
class AuthenticationManager():
    def __init__(self):
        self.basic_tokens: List[str] = []
        self.admin_tokens: List[str] = []
        self.secretary_tokens: List[str] = []
        self.agent_tokens: List[str] = []

    def save_token(self, token: str, role: str):
        if role == "basic":
            self.basic_tokens.append(token)
        elif role == "admin":
            self.admin_tokens.append(token)
        elif role == "secretary":
            self.secretary_tokens.append(token)
        elif role == "agent":
            self.agent_tokens.append(token)

    def delete_token(self, token: str, role: int):
        try:
            if role == "basic":
                self.basic_tokens.remove(token)
            elif role == "admin":
                self.admin_tokens.remove(token)
            elif role == "secretary":
                self.secretary_tokens.remove(token)
            elif role == "agent":
                self.agent_tokens.remove(token)
        except ValueError as e:
            return False
    
    def auth_admin(self, token: str):
        if token in self.admin_tokens:
            return True
        return False
    
    def auth_any(self, token: str):
        if token in self.admin_tokens or token in self.agent_tokens:
            return True
        return False