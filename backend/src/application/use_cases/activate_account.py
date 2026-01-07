from src.infrastructure.database.user_repository import UserRepository
from src.infrastructure.auth.auth_service import AuthService

class ActivateAccountUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, email: str, code: str) -> dict:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        
        if user.is_active == "true":
            raise ValueError("Account already activated")
        
        if user.activation_code != code:
            raise ValueError("Invalid activation code")
        
        self.user_repository.activate_user(user.id)
        token = AuthService.create_access_token({"sub": user.id})
        
        return {
            "access_token": token,
            "message": "Account activated successfully"
        }
