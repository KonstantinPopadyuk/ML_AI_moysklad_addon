from aiogram import types
from aiogram.filters import BaseFilter

class AllowedUserFilter(BaseFilter):
    def __init__(self, allowed_users: set):
        self.allowed_users = allowed_users

    async def __call__(self, message: types.Message) -> bool:
        """Check if the user is allowed."""
        return str(message.from_user.id) in self.allowed_users
    
allowed_users = {'245289439'} 
allowed_users_filter = AllowedUserFilter(allowed_users)