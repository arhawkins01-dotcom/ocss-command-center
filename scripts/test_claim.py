# Simple unit test to simulate Worker Self-Pull logic from app/app.py
units = {
    'OCSS North': {
        'supervisor': 'Alex Martinez',
        'team_leads': ['Sarah Johnson'],
        'support_officers': ['Michael Chen', 'Jessica Brown'],
        'assignments': {
            'Sarah Johnson': ['181000'],
            'Michael Chen': ['181001'],
            'Jessica Brown': ['181002']
        }
    },
    'OCSS South': {
        'supervisor': 'Priya Singh',
        'team_leads': ['David Martinez'],
        'support_officers': ['Amanda Wilson'],
        'assignments': {
            'David Martinez': ['181001'],
            'Amanda Wilson': ['181000']
        }
    }
}

reports_by_caseload = {'181000': [], '181001': [], '181002': []}

def simulate_pull(unit_name, cur_worker, pull_worker, pull_caseload):
    print(f"Simulating pull in unit={unit_name} as current_worker='{cur_worker}' trying to pull as '{pull_worker}' caseload='{pull_caseload}'")
    # Validate current worker
    if not cur_worker:
        return "ERROR: current worker not set"
    if pull_worker != cur_worker:
        return "ERROR: you can only pull for yourself"
    # Check already assigned across units
    already_assigned = None
    for uname, u in units.items():
        for person, caselist in u.get('assignments', {}).items():
            if pull_caseload in caselist:
                already_assigned = (uname, person)
                break
        if already_assigned:
            break
    if already_assigned:
        if already_assigned[0] == unit_name and already_assigned[1] == pull_worker:
            return f"INFO: caseload {pull_caseload} already assigned to you in unit {unit_name}"
        else:
            return f"ERROR: caseload {pull_caseload} already assigned to {already_assigned[1]} in unit {already_assigned[0]}"
    # Assign
    units[unit_name].setdefault('assignments', {}).setdefault(pull_worker, []).append(pull_caseload)
    return f"SUCCESS: caseload {pull_caseload} claimed by {pull_worker} in unit {unit_name}"

# Test 1: valid self-pull where caseload is currently assigned to someone else (should error)
print(simulate_pull('OCSS North', 'Michael Chen', 'Michael Chen', '181001'))
# Test 2: valid self-pull for an unassigned caseload
print(simulate_pull('OCSS North', 'Michael Chen', 'Michael Chen', '181000'))
# Verify assignments after Test 2
print('\nAssignments for OCSS North:')
print(units['OCSS North']['assignments'])
# Test 3: attempt to pull as a different worker (should error)
print(simulate_pull('OCSS North', 'Michael Chen', 'Jessica Brown', '181002'))
