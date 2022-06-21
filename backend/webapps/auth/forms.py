from fastapi import Request
from typing import List


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: str = None
        self.password: str = None
        
    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        print('HI HELLO: ', self.username, self.password)

    async def is_valid(self):
        if not self.username:
            self.errors.append("Valid Email is mandatory")
        if not self.password:
            self.errors.append("Password needs to be > 6 chars")
        if not self.errors:
            return True
        return False
