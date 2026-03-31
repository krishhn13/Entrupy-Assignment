from app.db.session import SessionLocal

def get_db():
        db = SessionLocal()
        try:
                yield db
        except:
                print("Something went wrong")
        finally:
                db.close()