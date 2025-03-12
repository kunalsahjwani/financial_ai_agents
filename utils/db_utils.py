from sqlalchemy import create_engine, text

def get_db_connection(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"):
    """Create a database connection and ensure vector extension is enabled"""
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # Test connection
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"Connected to PostgreSQL: {version}")
            
            # Enable vector extension
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            
        return engine
    except Exception as e:
        print(f"Database connection error: {e}")
        raise