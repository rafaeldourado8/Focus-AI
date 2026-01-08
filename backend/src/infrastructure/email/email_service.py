import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import get_settings

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        settings = get_settings()
        
        print(f"\n{'='*60}")
        print(f"📧 EMAIL PARA: {to_email}")
        print(f"📝 ASSUNTO: {subject}")
        print(f"{'='*60}\n")
        
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"⚠️  Email error: {e}")
            return True
    
    @staticmethod
    def send_activation_code(email: str, code: str):
        settings = get_settings()
        
        print(f"\n{'='*60}")
        print(f"📧 CÓDIGO DE ATIVAÇÃO PARA: {email}")
        print(f"🔑 CÓDIGO: {code}")
        print(f"{'='*60}\n")
        
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
            return True
