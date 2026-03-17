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
        time_limit = 300 
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
    
    solution = dict()
    time_slot_idx = 1
    course_list = list(schedule.course_list) 
    while course_list:
        random_course = random.choice(course_list)
        assignation = time_slot_idx
        solution[random_course] = assignation
        course_list.remove(random_course)
        time_slot_idx += 1
        
    return solution

def evaluate(solution, schedule):

    conflicts = 0
    conflicts_list = schedule.conflict_list

    for c1, c2 in conflicts_list:
        if solution[c1] == solution[c2]:
            conflicts += 1

    slots = schedule.get_n_creneaux(solution)

    return conflicts * 1000 + slots

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