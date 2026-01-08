"""
Cron job para enviar lembretes de inatividade
Execute: python -m src.infrastructure.cron.inactivity_reminder
"""
import asyncio
from datetime import datetime
from src.infrastructure.email.email_service import EmailService

async def send_inactivity_reminders():
    email_service = EmailService()
    
    print(f"[{datetime.now()}] Enviando lembretes de inatividade...")
    
    await email_service.send_email(
        to_email="raffadrugs@gmail.com",
        subject="🔥 Sentimos sua falta! Volte ao Cerberus AI",
        body="""
        <h2>Ei, você sumiu! 👋</h2>
        <p>Faz alguns dias que você não usa o Cerberus AI.</p>
        
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
    
    print("✅ Lembretes enviados")

if __name__ == "__main__":
    asyncio.run(send_inactivity_reminders())
