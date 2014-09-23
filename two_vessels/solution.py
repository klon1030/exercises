def get_first_solution(A, B, q, sol = []):
        return None


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
        
    )
    for d in test_cases:
        d_in = d['input']
        res = get_first_solution(d_in['A'], d_in['B'], d_in['q'])
        if res != d['expected']:
            print '''\
test failed
test case:
%(test_case_data)s
got:
%(res)s
''' % {'test_case_data': d,
       'res': res}

            
test__get_first_solution()


