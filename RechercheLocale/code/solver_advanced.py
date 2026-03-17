import random
import copy
import time

from schedule import Schedule

def solve(schedule):
    s = generate_solution(schedule)
    best = s.copy()

    s_score = evaluate(s, schedule)
    best_score = s_score

    if len(schedule.conflict_list) > 10000:
        time_limit = 295 
        start = time.time()

        while time.time() - start < time_limit:

            if s_score < best_score:
                best = s.copy()
                best_score = s_score

            neighbors = generate_neighbors(s, schedule)
            s, s_score = select_neighbor(neighbors)

    else:
        iterations = 1000

        for _ in range(iterations):

            if s_score < best_score:
                best = s.copy()
                best_score = s_score

            neighbors = generate_neighbors(s, schedule)
            s, s_score = select_neighbor(neighbors)

    return best


def generate_solution(schedule: Schedule):
    solution = {}
    
    courses = list(schedule.course_list)
    random.shuffle(courses)

    for course in courses:
        used_slots = set()
        
        for c1, c2 in schedule.conflict_list:
            if c1 == course and c2 in solution:
                used_slots.add(solution[c2])
            elif c2 == course and c1 in solution:
                used_slots.add(solution[c1])
        
        slot = 1
        while slot in used_slots:
            slot += 1
        
        solution[course] = slot

    return solution

def evaluate(solution, schedule):

    conflicts = 0
    conflicts_list = schedule.conflict_list

    for c1, c2 in conflicts_list:
        if solution[c1] == solution[c2]:
            conflicts += 1

    slots = schedule.get_n_creneaux(solution)

    return conflicts * 1000 + slots*20

def generate_neighbors(solution, schedule):

    neighbors = []

    courses = list(solution.keys())
    max_slot = schedule.get_n_creneaux(solution)

    course = random.choice(courses)

    for slot in range(1, max_slot + 2):

        new_solution = solution.copy()
        new_solution[course] = slot

        score = evaluate(new_solution, schedule)
        neighbors.append((new_solution, score))


    return neighbors

def select_neighbor(neighbors):
    best, best_score = neighbors[0]

    for n, score in neighbors:
        if score < best_score:
            best = n
            best_score = score

    return best, best_score