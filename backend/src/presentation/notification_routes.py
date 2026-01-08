from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.presentation.auth_routes import verify_token
from src.infrastructure.email.email_service import EmailService
from src.infrastructure.database.connection import get_db
from datetime import datetime

router = APIRouter()

class NotificationRequest(BaseModel):
    email: str
    settings: dict

@router.post("/settings-updated")
async def notify_settings_updated(
    request: NotificationRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(verify_token)
):
    """Notifica usuário sobre alteração de configurações"""
    email_service = EmailService()
    
    background_tasks.add_task(
        email_service.send_email,
        to_email=request.email,
        subject="⚙️ Configurações Atualizadas - Cerberus AI",
        body=f"""
        <h2>Suas configurações foram atualizadas!</h2>
        <p>Olá,</p>
        <p>Suas preferências no Cerberus AI foram salvas com sucesso em {datetime.now().strftime('%d/%m/%Y às %H:%M')}.</p>
        
        <h3>Configurações atuais:</h3>
        <ul>
            <li>Debug Mode: {'Ativado' if request.settings.get('debugMode') else 'Desativado'}</li>
            <li>Idioma: {request.settings.get('language', 'pt-BR')}</li>
            <li>Notificações: {'Ativadas' if request.settings.get('notifications') else 'Desativadas'}</li>
        </ul>
        
        <p>Continue aproveitando o Cerberus AI! 🚀</p>
        """
    )
    
    return {"message": "Notificação enviada"}

@router.post("/login-alert")
async def notify_login(
    background_tasks: BackgroundTasks,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Notifica usuário sobre novo login"""
    from src.infrastructure.database.user_repository import UserRepository
    from datetime import datetime
    
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_by_id(user_id)
        
        if not user or not user.notifications:
            return {"message": "Notificações desativadas"}
        
        email_service = EmailService()
        
        background_tasks.add_task(
            email_service.send_email,
            to_email=user.email,
            subject="🔐 Novo login detectado - Cerberus AI",
            body=f"""
            <h2>Novo acesso à sua conta</h2>
            <p>Olá,</p>
            <p>Detectamos um novo login na sua conta do Cerberus AI em {datetime.now().strftime('%d/%m/%Y às %H:%M')}.</p>
            
            <p><strong>Se foi você:</strong> Tudo certo! Continue aproveitando o Cerberus AI 🚀</p>
            <p><strong>Se não foi você:</strong> Altere sua senha imediatamente nas configurações.</p>
            
            <p>Mantenha sua conta segura!</p>
            """
        )
        
        return {"message": "Notificação enviada"}
    except Exception as e:
        print(f"Erro ao enviar notificação de login: {e}")
        return {"message": "Erro ao enviar notificação"}

@router.post("/inactivity-reminder")
async def send_inactivity_reminder(
    email: str,
    days_inactive: int
):
    """Envia lembrete de inatividade"""
    email_service = EmailService()
    
    await email_service.send_email(
        to_email=email,
        subject=f"🔥 Sentimos sua falta! Volte ao Cerberus AI",
        body=f"""
        <h2>Ei, você sumiu! 👋</h2>
        <p>Faz {days_inactive} dias que você não usa o Cerberus AI.</p>
        
        <h3>Novidades que você perdeu:</h3>
        <ul>
            <li>🚀 Novos modelos de IA mais rápidos</li>
            <li>🐛 Debug Mode aprimorado</li>
            <li>📊 Dashboard com métricas em tempo real</li>
        </ul>
        
        <p><a href="http://localhost:3000" style="background: #fff; color: #000; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; margin-top: 16px;">Voltar ao Cerberus AI</a></p>
        
        <p>Seu mentor técnico está esperando por você! 💻</p>
        """
    )
    
    return {"message": "Lembrete enviado"}
