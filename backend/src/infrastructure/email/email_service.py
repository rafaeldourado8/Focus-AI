import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import get_settings

class EmailService:
    @staticmethod
    def send_activation_code(email: str, code: str):
        settings = get_settings()
        
        # MODO DESENVOLVIMENTO: Mostrar código no console
        print(f"\n{'='*60}")
        print(f"📧 CÓDIGO DE ATIVAÇÃO PARA: {email}")
        print(f"🔑 CÓDIGO: {code}")
        print(f"{'='*60}\n")
        
        # Tentar enviar email (se falhar, não bloqueia o registro)
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USER
            msg['To'] = email
            msg['Subject'] = 'Focus AI - Código de Ativação'
            
            body = f"""
            <html>
            <body>
                <h2>Bem-vindo ao Focus AI!</h2>
                <p>Seu código de ativação é:</p>
                <h1 style="color: #6366f1; letter-spacing: 5px;">{code}</h1>
                <p>Este código expira em 24 horas.</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"⚠️  Email error (código mostrado acima): {e}")
            return True  # Retorna True mesmo com erro para não bloquear
