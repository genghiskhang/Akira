from akira import app
from akira.models import SessionLocal, Annotator, Assignment, Item
from pydantic import BaseModel

@app.get('/judge/assignment/{secret}')
async def get_assignment(secret: str):
    session = SessionLocal()
    try:
        assignments = Assignment.by_secret(session, secret)
        return assignments
    except Exception as e:
        return f'Failed to get assignments: {e}'
    finally:
        session.close()