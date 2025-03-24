from akira import app, constants
from akira.models import SessionLocal, Annotator, Assignment, Item
from pydantic import BaseModel

class ModelRequest(BaseModel):
    action: str
    data: list

@app.get('/admin')
async def admin():
    return 'Admin'

@app.get('/admin/assignments')
async def assignments():
    return generate_assignments(N=100, R=3, J=15, K=15)

@app.get('/admin/annotator')
async def get_annotator():
    return 'Annotator'

@app.post('/admin/annotator')
async def post_annotator(annotator: ModelRequest):
    action = annotator.action
    data = annotator.data
    session = SessionLocal()
    if action == constants.CREATE:
        try:
            new_annotator = Annotator.create(session, **data[0])
            if new_annotator:
                return f'Successfully created annotator \'{new_annotator.name}\''
        except Exception as e:
            return f'Failed to create annotator: {e}'
        finally:
            session.close()
    elif action == constants.BULK_CREATE:
        try:
            new_annotators = Annotator.bulk_create(session, data)
            if not any(ann is None for ann in new_annotators):
                return f'Successfully created {len(new_annotators)} annotators'
            return f'Partially created, failed to create some annotators: {[data[i]["email"] for i, ann in enumerate(new_annotators) if ann is None]}'
        except Exception as e:
            return f'Failed to create annotators: {e}'
        finally:
            session.close()
    session.close()
    return 'Invalid action specified...'

@app.post('/admin/item')
async def post_item(item: ModelRequest):
    action = item.action
    data = item.data
    session = SessionLocal()
    if action == constants.BULK_CREATE:
        try:
            new_items = Item.bulk_create(session, data)
            if not any(item is None for item in new_items):
                return f'Successfully created {len(new_items)} items'
            return f'Partially created, failed to create some annotators: {[data[i]["name"] for i, ann in enumerate(new_items) if ann is None]}'
        except Exception as e:
            return f'Failed to create items: {e}'
        finally:
            session.close()
    session.close()
    return 'Invalid action specified...'

@app.post('/admin/start')
async def start():
    session = SessionLocal()
    try:
        num_items = Item.num_items(session)
        num_annotators = Annotator.num_items(session)
        new_assignments = Assignment.bulk_create(session, generate_assignments(N=num_items, R=constants.R, J=num_annotators, K=constants.K))
        return f'Successfully created {len(new_assignments)} assignments'
    except Exception as e:
        return f'Failed to create assignments: {e}'
    finally:
        session.close()

def generate_assignments(N, R, J, K):
    participant_seen_count = [0] * N
    judge_participant_count = [[0] * N for _ in range(J)]
    waves = []
    remaining_participants = set(range(N))
    
    while remaining_participants:
        wave = [[] for _ in range(J)]
        participants_to_assign = sorted([(i, participant_seen_count[i]) for i in remaining_participants], key=lambda x: x[1])

        for participant, _ in participants_to_assign:
            for judge in range(J):
                if judge_participant_count[judge][participant] < 1 and len(wave[judge]) < K:
                    wave[judge].append(participant)
                    judge_participant_count[judge][participant] += 1
                    participant_seen_count[participant] += 1
                    if participant_seen_count[participant] == R:
                        remaining_participants.remove(participant)
                    break
        waves.append(wave)
    return waves