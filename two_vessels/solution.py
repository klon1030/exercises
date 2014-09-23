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
def get_first_solution(A, B, q, sol = []):
        """����� ������� ��� ������� ������.
����:
A - ����� ������� ������;
B - ����� ������� ������;
q - ����� ��������, ������� ���� ��������;
sol - �������, ���������� �� ���������� ����.
�����:
������� ���� [...,((x, y), action) ,...],
��� (x, y) - ������� ������ ��������� � �������,
action - ��������, � ������� �������� �� ������� � ������� ���������."""
        if sol == []:
        # ���� ������ ���� ������� ������ �������
                return get_first_solution( A, B, q,
                                           [((A, 0), acts.fA)])
        cur_st = sol[-1][0]
        if q in cur_st:
        # ���� ������� ��������� �������� ��������� ����� ��������, �� �����������
                return sol
        return sol + [((A-B, B), acts.A2B)]


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


