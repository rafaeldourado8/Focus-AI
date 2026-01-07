from src.domain.user import User
from src.infrastructure.database.user_repository import UserRepository
from src.infrastructure.auth.auth_service import AuthService
from src.infrastructure.email.email_service import EmailService
import secrets

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, email: str, password: str) -> dict:
        if not AuthService.validate_password_strength(password):
            raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and numbers")
        
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        password_hash = AuthService.hash_password(password)
        activation_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        user = User(
            email=email,
            password_hash=password_hash,
            is_active="false",
            activation_code=activation_code
        )
        created_user = self.user_repository.create(user)
        
        EmailService.send_activation_code(email, activation_code)
        
        return {
            "user_id": created_user.id,
            "email": created_user.email,
            "message": "Registration successful. Check your email for activation code."
        }