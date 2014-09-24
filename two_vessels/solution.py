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
def get_first_solution(v1, v2, q, sol = []):
        """Поиск решения для первого случая.
Вход:
v1 > 0 - объём первого сосуда;
v2 > 0 - объём второго сосуда;
0 < q <= max(v1, v2) - объём жидкости, который надо получить;
sol - решение, полученное на предыдущем шаге.
Выход:
Решение вида [...,({A: x, B: y}, action) ,...],
где x - текущий объёмы жидкости в сосуде объёма A,
y - текущий объёмы жидкости в сосуде объёма B,
action - действие, с помощью которого мы перешли в текущее состояние."""
        (A, B) = (v1, v2) if v1 > v2 else (v2, v1)
        
        if sol == []:
        # есть тольно один вариант анчала решения
                sol = [({A: A, B: 0}, acts.fA)]
        
        last_step = sol[-1]
        state = last_step[0]
        (x, y) = (state[A], state[B])
        if q in (x, y):
        # если текущее состояние содержит требуемый объём жидкости, то заканчиваем
                return sol
        if y == B:
                sol += [({A: x, B: 0}, acts.eB)]
        if x > B and y == 0:
                sol += [({A: x-B, B: B}, acts.A2B),]
        if x < B and y == 0:
                sol += [({A: 0, B: x}, acts.A2B)]
        if x == 0:
                sol += [({A: A, B: y}, acts.fA),
                        ({A: A - (B-y), B: B}, acts.A2B)]
        return get_first_solution(A, B, q, sol)


class Actions:
	A2B = 1     # transfer A -> B
	B2A = 2     # transfer B -> A
	fA = 3      # fill A
	eA = 4      # empty A
	fB = 5      # fill B
	eB = 6      # empty B

	
acts = Actions


def test__get_first_solution():
    test_cases = (
        {
        'input': {
            'A': 5,
            'B': 3,
            'q': 5,
            },
        'expected': [({5:5, 3:0}, acts.fA)]
        },
        {
        'input': {
            'A': 5,
            'B': 3,
            'q': 2,
            },
        'expected': [({5:5, 3:0}, acts.fA),
                     ({5:2, 3:3}, acts.A2B)]
        },
        {
        'input': {
            'A': 5,
            'B': 3,
            'q': 1,
            },
        'expected': [({5:5, 3:0}, acts.fA),
                     ({5:2, 3:3}, acts.A2B),
                     ({5:2, 3:0}, acts.eB),
                     ({5:0, 3:2}, acts.A2B),
                     ({5:5, 3:2}, acts.fA),
                     ({5:4, 3:3}, acts.A2B),
                     ({5:4, 3:0}, acts.eB),
                     ({5:1, 3:3}, acts.A2B)]
        },
    )
    test_OK = True
    for d in test_cases:
        d_in = d['input']
        res = get_first_solution(d_in['A'], d_in['B'], d_in['q'])
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
