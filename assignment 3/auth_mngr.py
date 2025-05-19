from typing import List
class AuthorizationManager():
    def __init__(self):
        # We create a token every time someone logs in, and based on their role, the token gets saved in one of these lists. 
        # Whenever a user calls any APIs, they need their tokens, which then gets checked in one of the classes functions, whether they are admins or agents.
        self.basic_tokens: List[str] = []
        self.admin_tokens: List[str] = []
        self.secretary_tokens: List[str] = []
        self.agent_tokens: List[str] = []

    def save_token(self, token: str, role: str):
        '''
        Saves the user's login token to a list specified by the user's role
        '''
        if role == "basic":
            self.basic_tokens.append(token)
        elif role == "admin":
            self.admin_tokens.append(token)
        elif role == "secretary":
            self.secretary_tokens.append(token)
        elif role == "agent":
            self.agent_tokens.append(token)

    def delete_token(self, token: str, role: int):
        '''
        Deletes the user's login token from a list specified by the user's role
        '''
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
        '''
        Checks whether the token sent belongs to an admin or not
        '''
        if token in self.admin_tokens:
            return True
        return False
    
    def auth_any(self, token: str):
        '''
        Checks whether the token sent belongs to either an admin or an agent or not
        '''
        if token in self.admin_tokens or token in self.agent_tokens:
            return True
        return False