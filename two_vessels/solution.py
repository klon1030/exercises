# -*- coding: cp1251 -*-
# � �������� ������ ���� ��� ������ ������������ A � B. ��� �������������
# ����� �������, ��� A > B. � ������ ��������� ������ ����������� ���
# ����������� ����� ����������.
# ����������� � ��������������� �������.
# ������� ��� �������� ���� ��� ������ ������ ������:
# 1. ��������� ����� A;
# 2. ��������� ����� B.
# �����, ���� � ������ �� ������� ���������� ���� ���������, ������������ ��������,
# �� ���������, ��� ��� ������ ��������� ��������� "�����" �� ������� ����� ������
# ����� ��������. ����� ��������� ����� ����������� ��� ������� 1 � 2.
# �� � ����� ������� �������� � ������� �������� ��������� � ������� ������ ��������� �������
# � �������� ������������ ������� ��� � ���� ��������� ������.
# ������� get_first_solution() ��������� ����� ������� ��� ������� ������.
def get_first_solution(v1, v2, q, sol = []):
        """����� ������� ��� ������� ������.
����:
v1 > 0 - ����� ������� ������;
v2 > 0 - ����� ������� ������;
0 < q <= max(v1, v2) - ����� ��������, ������� ���� ��������;
sol - �������, ���������� �� ���������� ����.
�����:
������� ���� [...,({A: x, B: y}, action) ,...],
��� x - ������� ������ �������� � ������ ������ A,
y - ������� ������ �������� � ������ ������ B,
action - ��������, � ������� �������� �� ������� � ������� ���������."""
        (A, B) = (v1, v2) if v1 > v2 else (v2, v1)
        
        if sol == []:
        # ���� ������ ���� ������� ������ �������
                sol = [({A: A, B: 0}, acts.fA)]
        
        last_step = sol[-1]
        state = last_step[0]
        (x, y) = (state[A], state[B])
        if q in (x, y):
        # ���� ������� ��������� �������� ��������� ����� ��������, �� �����������
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
