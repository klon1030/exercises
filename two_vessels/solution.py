# -*- coding: cp1251 -*-
# В условиях задачи даны два сосуда вместимостей A и B. Длч определённости
# будем считать, что A > B. В случае обратного строго неравенства все
# рассуждения будут аналогичны.
# Комментарии к предполагаемому решению.
# Имеется два варианта того как начать решать задачу:
# 1. заполнить сосуд A;
# 2. заполнить сосуд B.
# Далее, если в каждом из случаев нарисовать граф состояний, сгруппировав состяния,
# то получится, что для любого состояния двигаться "вперёд" по решению можно только
# одним способом. Графы состояний будут различаться для случаев 1 и 2.
# Но в целом решение сводится к анализу категрии состояния в котором сейчас находится решение
# и принятия однозначного решения как и куда двигаться дальше.
# Функция get_first_solution() реализует поиск решения для первого случая.

# TODO: развернуть рекурсию в цикл.
def get_first_solution(v1, v2, q, sol = []):
    """Поиск решения для первого случая.
Вход:
v1 > 0 - объём первого сосуда;
v2 > 0 - объём второго сосуда;
0 < q <= max(v1, v2) - объём жидкости, который надо получить;
sol - решение, полученное на предыдущем шаге.
Выход:
Решение вида [...,({A: x, B: y}, action) ,...] - список "шагов",
где x - текущий объёмы жидкости в сосуде объёма A,
y - текущий объёмы жидкости в сосуде объёма B,
action - действие, с помощью которого мы перешли в текущее состояние."""
    (A, B) = (v1, v2) if v1 > v2 else (v2, v1)
    
    if sol == []:
    # есть тольно один вариант анчала решения
        sol = [({A: A, B: 0}, ACTS.fA)]
    
    last_step = sol[-1]
    state = last_step[0]
    (x, y) = (state[A], state[B])
    if q in (x, y):
    # если текущее состояние содержит требуемый объём жидкости, то заканчиваем
        return sol
    if y == B:
        sol += [({A: x, B: 0}, ACTS.eB)]
    if x > B and y == 0:
        sol += [({A: x-B, B: B}, ACTS.A2B),]
    if x < B and y == 0:
        sol += [({A: 0, B: x}, ACTS.A2B)]
    if x == 0:
        sol += [({A: A, B: y}, ACTS.fA),
                ({A: A - (B-y), B: B}, ACTS.A2B)]
    return get_first_solution(A, B, q, sol)


class ACTIONS:
    A2B = 1     # transfer A -> B
    B2A = 2     # transfer B -> A
    fA = 3      # fill A
    eA = 4      # empty A
    fB = 5      # fill B
    eB = 6      # empty B

	
ACTS = ACTIONS


def test__get_first_solution():
    test_cases = (
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'q': 5,
            },
        'expected': [({5:5, 3:0}, ACTS.fA)]
        },
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'q': 2,
            },
        'expected': [({5:5, 3:0}, ACTS.fA),
                     ({5:2, 3:3}, ACTS.A2B)]
        },
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'q': 1,
            },
        'expected': [({5:5, 3:0}, ACTS.fA),
                     ({5:2, 3:3}, ACTS.A2B),
                     ({5:2, 3:0}, ACTS.eB),
                     ({5:0, 3:2}, ACTS.A2B),
                     ({5:5, 3:2}, ACTS.fA),
                     ({5:4, 3:3}, ACTS.A2B),
                     ({5:4, 3:0}, ACTS.eB),
                     ({5:1, 3:3}, ACTS.A2B)]
        },
        {
        'input': {
            'v1': 3,
            'v2': 5,
            'q': 1,
            },
        'expected': [({5:5, 3:0}, ACTS.fA),
                     ({5:2, 3:3}, ACTS.A2B),
                     ({5:2, 3:0}, ACTS.eB),
                     ({5:0, 3:2}, ACTS.A2B),
                     ({5:5, 3:2}, ACTS.fA),
                     ({5:4, 3:3}, ACTS.A2B),
                     ({5:4, 3:0}, ACTS.eB),
                     ({5:1, 3:3}, ACTS.A2B)]
        },
    )
    test_OK = True
    for d in test_cases:
        d_in = d['input']
        res = get_first_solution(d_in['v1'], d_in['v2'], d_in['q'])
        if res != d['expected']:
            test_OK = False
            print '''\
test failed
test case:
%(test_case_data)s
got:

%(res)s
''' % {'test_case_data': d,
       'res': res}
    if test_OK:
            print 'test__get_first_solution() passed'

            
test__get_first_solution()


#TODO: развернуть рекурсию в цикл.
def get_second_solution(v1, v2, q, sol = []):
    (A, B) = (v1, v2) if v1 > v2 else (v2, v1)
    
    if sol == []:
    # есть тольно один вариант нaчала решения
        sol = [({A: 0, B: B}, ACTS.fB),
               ({A: B, B: 0}, ACTS.B2A),]
    
    last_step = sol[-1]
    state = last_step[0]
    (x, y) = (state[A], state[B])
    if q in (x, y):
    # если текущее состояние содержит требуемый объём жидкости, то заканчиваем
        return sol
    if y == 0:
        sol += [({A: x, B: B}, ACTS.fB),]
    if x + B < A and y == B:
        sol += [({A: x + B, B: 0}, ACTS.B2A)]
    if x + B > A and y == B:
        sol += [({A: A, B: B-(A-x)}, ACTS.B2A)]
    if x == A:
        sol += [({A: 0, B: y}, ACTS.eA),
                ({A: y, B: 0}, ACTS.B2A)]
    return get_second_solution(A, B, q, sol)


def test__get_second_solution():
    test_cases = (
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'q': 5,
            },
        'expected': [({5:0, 3:3}, ACTS.fB),
                     ({5:3, 3:0}, ACTS.B2A),
                     ({5:3, 3:3}, ACTS.fB),
                     ({5:5, 3:1}, ACTS.B2A),]
        },
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'q': 2,
            },
        'expected': [({5:0, 3:3}, ACTS.fB),
                     ({5:3, 3:0}, ACTS.B2A),
                     ({5:3, 3:3}, ACTS.fB),
                     ({5:5, 3:1}, ACTS.B2A),
                     ({5:0, 3:1}, ACTS.eA),
                     ({5:1, 3:0}, ACTS.B2A),
                     ({5:1, 3:3}, ACTS.fB),
                     ({5:4, 3:0}, ACTS.B2A),
                     ({5:4, 3:3}, ACTS.fB),
                     ({5:5, 3:2}, ACTS.B2A)]
        },
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'q': 1,
            },
        'expected': [({5:0, 3:3}, ACTS.fB),
                     ({5:3, 3:0}, ACTS.B2A),
                     ({5:3, 3:3}, ACTS.fB),
                     ({5:5, 3:1}, ACTS.B2A),]
        },
        {
        'input': {
            'v1': 3,
            'v2': 5,
            'q': 1,
            },
        'expected': [({5:0, 3:3}, ACTS.fB),
                     ({5:3, 3:0}, ACTS.B2A),
                     ({5:3, 3:3}, ACTS.fB),
                     ({5:5, 3:1}, ACTS.B2A),]
        },
    )
    test_OK = True
    for d in test_cases:
        d_in = d['input']
        res = get_second_solution(d_in['v1'], d_in['v2'], d_in['q'])
        if res != d['expected']:
            test_OK = False
            print '''\
test failed
test case:
%(test_case_data)s
got:

%(res)s
''' % {'test_case_data': d,
       'res': res}
    if test_OK:
            print 'test__get_second_solution() passed'


test__get_second_solution()



def sprint_sol_step(v1, v2, step):
    """Функция для генерации строки с описание текущего шага step для задачи
о переливании двух сосудов объёмами v1 и v2.
"""
    (state, action) = step
    
    (A_id, B_id) = (1, 2) if v1 > v2 else (2, 1)
    
    action_tmplts = {
            ACTS.A2B: 'transfer #%(A_id)d -> #%(B_id)d',
            ACTS.B2A: 'transfer #%(B_id)d -> #%(A_id)d',
            ACTS.eA: 'empty #%(A_id)d',
            ACTS.fA: 'fill #%(A_id)d',
            ACTS.eB: 'empty #%(B_id)d',
            ACTS.fB: 'fill #%(B_id)d',
            }
    action_str = action_tmplts[action] % {'A_id': A_id, 'B_id': B_id}
    return '%17s: %d \t%d' % (action_str, state[v1], state[v2])


def test__sprint_sol_step():
# TODO: неплохо бы вбить тесты на оставшиеся действия.
    test_cases = (
        {
        'input': {
            'v1': 5,
            'v2': 3,
            'step': ({5:2, 3:0}, ACTS.eB),
            },
        'expected': 'empty #2: 2 \t0'
        },
        {
        'input': {
            'v1': 3,
            'v2': 5,
            'step': ({5:2, 3:0}, ACTS.eB),
            },
        'expected': 'empty #1: 0 \t2'
        },
    )
    test_OK = True
    for d in test_cases:
        d_in = d['input']
        res = sprint_sol_step(d_in['v1'], d_in['v2'], d_in['step'])
        if res.strip() != d['expected']:
            test_OK = False
            print '''\
test__sprint_sol_step() failed
test case:
%(test_case_data)s
got:

%(res)s
''' % {'test_case_data': d,
       'res': res}
    if test_OK:
            print 'test__sprint_sol_step() passed'


                
test__sprint_sol_step()



def gcd(a, b):
    """ Вычисление НОД(a, b) по алгоритму Евклида с использованием рекурсии."""
    if b == 0:
        return abs(a);
    return gcd(b, a % b);



def solve(v1, v2, q):
    d = gcd(v1, v2)
    if d != 1 and q % d != 0 :
            return None
    res1 = get_first_solution(v1, v2, q)
    res2 = get_second_solution(v1, v2, q)
    if len(res1) > len(res2):
        return res2
    return res1


def print_solution(v1, v2, q):
    sol = solve(v1, v2, q)
    if sol == None:
        print 'невозможно решить задачу'
        return
    print "\t%17s: %d \t%d" % ('volumes:', v1, v2)
    print "-"*40
    print "\t%17s: 0 \t0" % ('init_state')
    for (i, step) in enumerate(sol):
        print '%d\t' % (i+1), sprint_sol_step(v1, v2, step)
