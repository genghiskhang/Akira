from akira import app, constants
from akira.models import SessionLocal, Annotator, Assignment, Item, Decision
from pydantic import BaseModel

class ModelRequest(BaseModel):
    action: str
    data: list

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

@app.post('/judge/vote')
async def vote(decision: ModelRequest):
    action = decision.action
    data = decision.data
    session = SessionLocal()
    if action == constants.VOTE:
        try:
            Decision.vote(session, **data[0])
        except Exception as e:
            return f'Failed to submit vote: {e}'
        finally:
            session.close()
    session.close()
    return 'Vote'