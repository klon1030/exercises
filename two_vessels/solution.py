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
def get_first_solution(A, B, q, sol = []):
        """Поиск решения для первого случая.
Вход:
A - объём первого сосуда;
B - объём второго сосуда;
q - объём жидкости, который надо получить;
sol - решение, полученное на предыдущем шаге.
Выход:
Решение вида [...,((x, y), action) ,...],
где (x, y) - текущие объёмы жидкостей в сосудах,
action - действие, с помощью которого мы перешли в текущее состояние."""
        if sol == []:
        # есть тольно один вариант анчала решения
                sol = [((A, 0), acts.fA)]
                return get_first_solution( A, B, q, sol)
        (x, y) = sol[-1][0]
        if q in (x, y):
        # если текущее состояние содержит требуемый объём жидкости, то заканчиваем
                return sol
        if x > B and y == 0:
                sol += [((x-B, B), acts.A2B)]
                return get_first_solution(A, B, q, sol)
        if x > B and y == B:
                sol += [((x, 0), acts.eB)]
                return get_first_solution(A, B, q, sol)
        if x < B and y == 0:
                sol += [((0, x), acts.A2B)]
                return get_first_solution(A, B, q, sol)
        if x < B and y == B:
                sol += [((x, 0), acts.eB)]
                return get_first_solution(A, B, q, sol)
        if x == 0:
                sol += [((A, y), acts.fA),
                        ((A - (B-y), B), acts.A2B)]
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
        'expected': [((5, 0), acts.fA)]
        },
        {
        'input': {
            'A': 5,
            'B': 3,
            'q': 2,
            },
        'expected': [((5, 0), acts.fA),
                     ((2, 3), acts.A2B)]
        },
        {
        'input': {
            'A': 5,
            'B': 3,
            'q': 1,
            },
        'expected': [((5, 0), acts.fA),
                     ((2, 3), acts.A2B),
                     ((2, 0), acts.eB),
                     ((0, 2), acts.A2B),
                     ((5, 2), acts.fA),
                     ((4, 3), acts.A2B),
                     ((4, 0), acts.eB),
                     ((1, 3), acts.A2B)]
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


