from akira import app

@app.route('/admin')
def admin():
    return 'Admin'

@app.route('/admin/test_generate')
def test_generate():
    return generate_assignments(N=100, R=3, J=15, K=5)

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