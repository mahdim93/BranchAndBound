import USMMALB
import time
import sys

number_of_branchs = 0
number_of_solutions = 0

#  global variables for type II models
bestSole = []
sum_of_cycle_time = 0
number_of_stations = 0


def branch_and_bound_type_1(problem, i, sol, rem_cycle):
    global bestSole, number_of_stations
    global number_of_branchs, number_of_solutions
    number_of_branchs += 1
    if i >= problem.number_of_tasks:
        number_of_solutions += 1
        tmp, tmp2 = objective_type_1(problem, sol)
        if number_of_stations > tmp and problem.cycle_time >= tmp2:
            bestSole = sol.copy()
            number_of_stations = tmp
        return
    tmp = sol.copy()
    for j in range(problem.number_of_station):
        if tmp[j] is None:
            tmp[j] = 0
    for j in range(max(tmp)+2):
        if feasibility_precedences(i, j, sol.copy(), problem) and feasibility_cycle_time(problem, i, j, rem_cycle):
            if bound_type_1(problem, j, sol) and bound_type_1_2(problem, i, j, sol.copy()):
                sol[i] = j
                tmp = rem_cycle.copy()
                for m in range(problem.number_of_model):
                    tmp[j][m] -= problem.tasks_time[i][m]
                branch_and_bound_type_1(problem, i+1, sol.copy(), tmp)


def branch_and_bound_type_2(problem, i, sol):
    global bestSole, sum_of_cycle_time
    global number_of_branchs, number_of_solutions
    number_of_branchs += 1
    if i >= problem.number_of_tasks:
        number_of_solutions += 1
        tmp = objective_type_2(problem, sol)
        if sum_of_cycle_time > tmp:
            bestSole = sol.copy()
            sum_of_cycle_time = tmp
        return
    for j in range(problem.number_of_station):
        tmp = sol.copy()
        tmp[i] = j
        if feasibility_precedences(i, j, sol.copy(), problem) and bound_type_2(j, tmp, problem) < sum_of_cycle_time:
            sol[i] = j
            branch_and_bound_type_2(problem, i+1, sol.copy())


def feasibility_precedences(i, j, sol, problem):
    feasible = False
    tmp_1 = True
    tmp_2 = True
    for p in problem.precedences[i]:
        if sol[p] is not None:
            if sol[p] > j:
                tmp_1 = False
    for s in problem.successors[i]:
        if sol[s] is not None:
            if sol[s] > j:
                tmp_2 = False
    if tmp_1 or tmp_2:
        feasible = True
    return feasible


def bound_type_2(j, sol, problem):
    tmp = 0
    for i in range(problem.number_of_tasks):
        if sol[i] is None:
            for m in range(problem.number_of_model):
                tmp += problem.tasks_time[i][m]
    bound = tmp/(problem.number_of_station-j+1)
    cycle_time = objective_type_2(problem, sol)
    if bound > cycle_time:
        return bound
    else:
        return cycle_time


def bound_type_1(problem, j, sol):
    global number_of_stations, bestSole
    if len(bestSole) >= 1:
        tmp = sol.copy()
        for i in range(problem.number_of_station):
            if tmp[i] is None:
                tmp[i] = 0
        if (max(bestSole) < j) or (max(bestSole) < max(tmp)):
            return False
    return True


def bound_type_1_2(problem, i, j, sol):
    max_tmp = 0
    sol[i] = j
    for x in range(problem.number_of_station):
        if sol[x] is None:
            sol[x] = -1
    for m in range(problem.number_of_model):
        max_tmp = 0
        for j in range(1, max(sol)+2):
            tmp = 0
            for i in range(problem.number_of_tasks):
                if sol[i] == j:
                    tmp += problem.tasks_time[i][m]
            if max_tmp <= tmp:
                max_tmp = tmp
    if max_tmp > problem.cycle_time:
        return False
    return True


def feasibility_cycle_time(problem, i, j, rem_cycle):
    feasible = True
    for m in range(problem.number_of_model):
        if (rem_cycle[j][m] - problem.tasks_time[i][m]) < 0:
            feasible = False
    return feasible


def objective_type_2(problem, sol):
    cycle_time = 0
    for m in range(problem.number_of_model):
        max_tmp = 0
        for j in range(problem.number_of_station):
            tmp = 0
            for i in range(problem.number_of_tasks):
                if sol[i] == j:
                    tmp += problem.tasks_time[i][m]
            if max_tmp <= tmp:
                max_tmp = tmp
        cycle_time += max_tmp
    return cycle_time


def objective_type_1(problem, sol):
    max_tmp = 0
    for m in range(problem.number_of_model):
        for j in range(problem.number_of_station):
            tmp = 0
            for i in range(problem.number_of_tasks):
                if sol[i] == j:
                    tmp += problem.tasks_time[i][m]
            if max_tmp <= tmp:
                max_tmp = tmp
    return (max(sol)+1), max_tmp


if __name__ == '__main__':
    sys.setrecursionlimit(1500)
    problem = USMMALB.u_shaped_mixed_model_assembly_line_balancing("instance_n=20_17.alb", 1, 1, 4)
    if problem.type is 1:
        sol = []
        rem_cycle = []
        tmp = []
        number_of_stations = problem.number_of_station
        for i in range(problem.number_of_model):
            tmp.append(problem.cycle_time)
        for i in range(problem.number_of_tasks):
            rem_cycle.append(tmp.copy())
            sol.append(None)
        start_time = time.time()
        branch_and_bound_type_1(problem, 0, sol.copy(), rem_cycle.copy())  # minimum number of station
        spend_time = time.time() - start_time
        print(bestSole, number_of_stations)
        print("number of branches ", number_of_branchs, "number of solutions ", number_of_solutions)
        print("time ", spend_time)
    else:
        sol = []
        sum_of_cycle_time = sum(map(sum, problem.tasks_time))
        for i in range(problem.number_of_tasks):
            sol.append(None)
        start_time = time.time()
        branch_and_bound_type_2(problem, 0, sol.copy())  # minimum cycle time
        spend_time = time.time() - start_time
        print(bestSole, sum_of_cycle_time)
        print("number of branches ", number_of_branchs, "number of solutions ", number_of_solutions)
        print("time ", spend_time)
