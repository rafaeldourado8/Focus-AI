from src.infrastructure.database.user_repository import UserRepository
from src.infrastructure.auth.auth_service import AuthService

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, email: str, password: str) -> dict:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        
        if user.is_active != "true":
            raise ValueError("Account not activated. Check your email.")
        
        if not AuthService.verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        token = AuthService.create_access_token({"sub": user.id})
        
        return {
            "user_id": user.id,
            "email": user.email,
            "access_token": token
        }