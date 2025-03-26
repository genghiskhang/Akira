from akira import app, constants
from akira.models import SessionLocal, Annotator, Assignment, Item, Decision
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse
import secrets

class ModelRequest(BaseModel):
    action: str
    data: list

@app.get('/judge/login/{secret}')
async def login(secret: str):
    session = SessionLocal()
    token = secrets.token_urlsafe(32)
    try:
        annotator = session.query(Annotator).filter(Annotator.secret == secret).one_or_none()
        if annotator is None:
            return 'Annotator does not exist'
        if not annotator.token:
            annotator.token = token
        token = annotator.token
        session.commit()
    except Exception as e:
        return f'Failed to start session: {e}'
    if token is None:
        return f'Failed to start session'
    response = JSONResponse(content={ 'message':'login good' })
    response.set_cookie(key='session', value=token, httponly=True, secure=False, max_age=360)
    return response

@app.get('/judge/session_test')
async def session_test(request: Request):
    token = request.cookies['session']
    if not token:
        return f'No token'
    if 'counter' not in request.session:
        request.session['counter'] = 0
    request.session['counter'] += 1
    return request.session['counter']

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