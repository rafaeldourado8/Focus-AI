"""
Migração: Adiciona colunas de configurações do usuário
Execute: docker-compose exec backend python -m src.infrastructure.database.migrations.add_user_settings
"""
from src.infrastructure.database.connection import get_db
from sqlalchemy import text

def migrate():
    db = next(get_db())
    
    try:
        print("🔄 Adicionando colunas de configurações...")
        
        db.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS name VARCHAR,
            ADD COLUMN IF NOT EXISTS debug_mode BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS language VARCHAR DEFAULT 'pt-BR',
            ADD COLUMN IF NOT EXISTS notifications BOOLEAN DEFAULT TRUE;
        """))
        
        db.commit()
        print("✅ Migração concluída com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro na migração: {e}")
        raise

if __name__ == "__main__":
    migrate()
