from Module_17.HW_mod_17.hw_17_4.app.backend.db import SessionLocal

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


