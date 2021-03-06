# -*- coding: cp1251 -*-
import itertools

def fetch_head(seq, n):
    return list(itertools.islice(seq, 0, n))


class RingBuffer:
    def __init__(self, buf_size, data_seq):
        self.buf_size = buf_size
        self.data = fetch_head(data_seq, buf_size)
        
    def append(self, x):
        self.data.pop(0)
        self.data.append(x)


def find_subseq(subseq, seq):
    sublist = list(subseq)
    seq_iter = iter(seq)
    buf = RingBuffer(len(sublist), seq_iter)
    i = 0
    while buf.data != sublist:
        buf.append(seq_iter.next())
        i += 1
    return i


def gen_num_seq():
    i = 1
    while 1:
        s = str(i)
        for ch in s:
            yield ch
        i += 1


def calc_num_idx_in_str_2(num):
    n = len(str(num))
    res = 0
    for i in range(1, n):
        res += i*9*pow(10, i-1)
    res += n*(num - pow(10, n-1))
    return res


def intersect_head_and_tail_chunks(head_chunk,
                                          tail_chunk,
                                          subseq_len):
    head_str = head_chunk.strip('*')
    k = len(head_str)
    N = subseq_len
    
    head_num = int(head_str)
    inc_head = ('%%0%dd' % k %(head_num+1))[-k:]
    inc_head_chunk = '*'*(len(head_chunk) - k) + inc_head

    if N == len(head_chunk):
        return tail_chunk.strip('*') + inc_head
    
    if inc_head_chunk[-k:N-k] == tail_chunk[-k:N-k]:
        return tail_chunk[:-k] + inc_head_chunk[-k:]
    return ''


def test__intersect_head_and_tail_chunks():
    test_name = 'test__intersect_head_and_tail_chunks'
    tested_func = intersect_head_and_tail_chunks
    test_cases = (
        {
        'input':{
            'chunked_head': '****86',
            'chunked_tail': '4535**',
            'subseq_len': 6
            },
        'expected': '453587'
        },
        {
        'input':{
            'chunked_head': '****89',
            'chunked_tail': '4535**',
            'subseq_len': 6
            },
        'expected': '453590'
        },
        {
        'input':{
            'chunked_head': '8645',
            'chunked_tail': '86**',
            'subseq_len': 6
            },
        'expected': '8646'
        },
        {
        'input':{
            'chunked_head': '*864',
            'chunked_tail': '535*',
            'subseq_len': 6
            },
        'expected': ''  # False
        },
        {
        'input':{
            'chunked_head': '*864',
            'chunked_tail': '586*',
            'subseq_len': 6
            },
        'expected': '5865'
        },
        {'input':{
            'chunked_head': '*869',
            'chunked_tail': '586*',
            'subseq_len': 6
            },
        'expected': ''  #False
        },
        {'input':{
            'chunked_head': '*869',
            'chunked_tail': '587*',
            'subseq_len': 6
            },
        'expected': '5870'
        },
        {'input':{
            'chunked_head': '*01',
            'chunked_tail': '2**',
            'subseq_len': 3
            },
        'expected': '202'
        },
        {'input':{
            'chunked_head': '**0',
            'chunked_tail': '12*',
            'subseq_len': 3
            },
        'expected': '121'
        },
        )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['chunked_head'], i['chunked_tail'], i['subseq_len'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print
    if test_OK:
        print '%s passed' % test_name

#test__intersect_head_and_tail_chunks()


def next_num_str(num_str):
    return str(int(num_str)+1)


def gen_head(subseq, chunk_size):
    len_wo_lead_zeros = len(subseq.lstrip('0'))
    zeros_num = len(subseq) - len_wo_lead_zeros
    start_idx = 1 if zeros_num == 0 else zeros_num
    return map(lambda i: (subseq[:i], subseq[i:]), range(start_idx, chunk_size+1))


def test__gen_head():
    test_name = 'test__gen_head'
    tested_func = gen_head
    test_cases = (
        {
        'input':{
            'subseq': '123456',
            'chunk_size': 4,
            },
        'expected': [('1', '23456'),
                     ('12', '3456'),
                     ('123', '456'),
                     ('1234', '56')]
        },
        {
        'input':{
            'subseq': '00123456',
            'chunk_size': 4,
            },
        'expected': [('00', '123456'),
                     ('001', '23456'),
                     ('0012', '3456')]
        },
        {
        'input':{
            'subseq': '00000123456',
            'chunk_size': 4,
            },
        'expected': []
        },
    )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['subseq'], i['chunk_size'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print
    if test_OK:
        print '%s passed' % test_name


#test__gen_head()


def is_dec_number(s):
    return len(s.lstrip('0')) == len(s)


def is_ten_pow(s):
    return s.rstrip('0') == '1'


def gen_next_chunk_by_head(resid, head, chunk_size):
    for exp_next_chunk_len in [chunk_size, chunk_size+1]:
        next_chunk_sz = min(exp_next_chunk_len, len(resid))
        chunk_c = resid[:next_chunk_sz]
        if not is_dec_number(chunk_c):
            return (None, None)
        expected_head_for_chunk_c = str(int(chunk_c)-1)[-len(head):]
        if expected_head_for_chunk_c == head:
            return (resid[:next_chunk_sz], resid[next_chunk_sz:])
    return (None, None)


def test__gen_next_chunk_by_head():
    test_name = 'test__gen_next_chunk_by_head'
    tested_func = gen_next_chunk_by_head
    test_cases = (
        {
        'input':{
            'head': '12',
            'resid': '3456',
            'chunk_size': 4,
            },
        'expected': (None, None)
        },
        {
        'input':{
            'head': '12',
            'resid': '3413',
            'chunk_size': 4,
            },
        'expected': ('3413', '')
        },
        {
        'input':{
            'head': '99', 
            'resid': '100',
            'chunk_size': 2,
            },
        'expected': ('100', '')
        },
        {
        'input':{
            'head': '99', 
            'resid': '1001',
            'chunk_size': 2,
            },
        'expected': ('100', '1')
        },
        {
        'input':{
            'head': '99', 
            'resid': '10',
            'chunk_size': 2,
            },
        'expected': (None, None)
        },
        {
        'input':{
            'head': '1', 
            'resid': '0',
            'chunk_size': 1,
            },
        'expected': (None, None)
        },
        {
        'input':{
            'head': '1', 
            'resid': '92',
            'chunk_size': 1,
            },
        'expected': (None, None)
        },
    )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['resid'], i['head'], i['chunk_size'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print
    if test_OK:
        print '%s passed' % test_name


#test__gen_next_chunk_by_head()


def gen_first_chunk(subseq, chunk_size):
    len_wo_lead_zeros = len(subseq.lstrip('0'))
    zeros_num = len(subseq) - len_wo_lead_zeros
    if chunk_size <= zeros_num:
        return [(None, None, None)]
    start_idx = zeros_num
    starts = range(start_idx, chunk_size)
    ends = map(lambda start: start + min(len(subseq) - start, chunk_size), starts)
    heads = map(lambda start: subseq[:start], starts)
    first_chunks = map(lambda start, end: subseq[start:end], starts, ends)
    resids = map(lambda start, end: None if  end - start < chunk_size else subseq[end:], starts, ends)
    res = filter(lambda (head, fch, resid): is_dec_number(fch), zip(heads, first_chunks, resids))
    return res


def test__gen_first_chunk():
    test_name = 'test__gen_first_chunk'
    tested_func = gen_first_chunk
    test_cases = (
        {
        'input':{
            'subseq': '12345678',
            'chunk_size': 3,
            },
        'expected': [('', '123', '45678'),
                     ('1', '234', '5678'),
                     ('12', '345', '678')]
        },
        {
        'input':{
            'subseq': '00123456',
            'chunk_size': 3,
            },
        'expected': [('00', '123', '456')]
        },
        {
        'input':{
            'subseq': '0123456',
            'chunk_size': 3,
            },
        'expected': [('0', '123', '456'),
                     ('01', '234', '56')]
        },
        {
        'input':{
            'subseq': '1234',
            'chunk_size': 3,
            },
        'expected': [('', '123', '4'),
                     ('1', '234', ''),
                     ('12', '34', None)]
        },
        {
        'input':{
            'subseq': '1234',
            'chunk_size': 4,
            },
        'expected': [('', '1234', ''),
                     ('1', '234', None),
                     ('12', '34', None),
                     ('123', '4', None)]
        },
        {
        'input':{
            'subseq': '01',
            'chunk_size': 1,
            },
        'expected': [(None, None, None)]
        },
        {
        'input':{
            'subseq': '022',
            'chunk_size': 3,
            },
        'expected': [('0', '22', None),
                     ('02', '2', None)]
        },
        {
        'input':{
            'subseq': '100',
            'chunk_size': 2,
            },
        'expected': [('', '10', '0')]
        },
    )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['subseq'], i['chunk_size'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print
    if test_OK:
        print '%s passed' % test_name


#test__gen_first_chunk()


def gen_next_chunk(resid, cur_chunk):
    chunk_size = len(cur_chunk)
    expected_next_chunk = next_num_str(cur_chunk)
    exp_next_chunk_len = len(expected_next_chunk)
    next_chunk_sz = min(exp_next_chunk_len, len(resid))
    if expected_next_chunk[:next_chunk_sz] == resid[:next_chunk_sz]:
        return (resid[:next_chunk_sz], resid[next_chunk_sz:])
    return (None, None)


def test__gen_next_chunk():
    test_name = 'test__gen_next_chunk'
    tested_func = gen_next_chunk
    test_cases = (
        {
        'input':{
            'cur_chunk': '1',
            'resid': '234',
            },
        'expected': ('2', '34')
        },
        {
        'input':{
            'cur_chunk': '12',
            'resid': '3413',
            },
        'expected': (None, None)
        },
        {
        'input':{
            'cur_chunk': '99', 
            'resid': '100',
            },
        'expected': ('100', '')
        },
        {
        'input':{
            'cur_chunk': '99', 
            'resid': '1001',
            },
        'expected': ('100', '1')
        },
        {
        'input':{
            'cur_chunk': '99', 
            'resid': '10',
            },
        'expected': ('10', '')
        },
    )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['resid'], i['cur_chunk'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print
    if test_OK:
        print '%s passed' % test_name


#test__gen_next_chunk()
        

def gen_chunks(resid, first_chunk):
    chunk_size = len(first_chunk)
    chunks = [first_chunk]
    cur_chunk = first_chunk
    while resid != '':
        (next_chunk, resid) = gen_next_chunk(resid, cur_chunk)
        if next_chunk == None:
            return None
        chunks += [next_chunk]
        cur_chunk = next_chunk
    return chunks


def test__gen_chunks():
    test_name = 'test__gen_chunks'
    tested_func = gen_chunks
    test_cases = (
        {
        'input':{
            'first_chunk': '1',
            'resid': '234',
            },
        'expected': ['1', '2', '3', '4']
        },
        {
        'input':{
            'first_chunk': '1',
            'resid': '235',
            },
        'expected': None
        },
        {
        'input':{
            'first_chunk': '12',
            'resid': '131',
            },
        'expected': ['12', '13', '1']
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '1001',
            },
        'expected': ['99', '100', '1']
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '100',
            },
        'expected': ['99', '100']
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '7',
            },
        'expected': None
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '10',
            },
        'expected': ['99', '10']
        },
    )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['resid'], i['first_chunk'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print
    if test_OK:
        print '%s passed' % test_name


#test__gen_chunks()



def gen_tail_num_by_head(head,
                         tail,
                         chunk_size,
                         subseq_len):
    if head == '':
        return tail
##    if head.strip('0') == '':
##        return ''
    head_chunk = '*'*(chunk_size - len(head)) + head
    if not is_dec_number(tail):
        return ''
    tail_chunk = tail + '*'*(chunk_size - len(tail))
    return intersect_head_and_tail_chunks(head_chunk, tail_chunk, subseq_len)


def find_solution(subseq):
    for chunk_size in range(1, len(subseq)+1):
        res = []
        for (head, first_chunk, resid) in gen_first_chunk(subseq, chunk_size):
            # �� ���������� �������� ��������� � "������ ������" ����� chunk_size:
            if head == None:
##                print 1, (head, first_chunk, resid)
                continue
            # ���� ��������� ��� �������� ������ ���� (�� ���� "�����")
            if resid == None:
                # ���� ���� ������, �� ��������� �� ������������� � ������� � ���� ���������� �������� �����
                if head != '':
##                    print 2, (head, first_chunk, resid)
                    tail_num = gen_tail_num_by_head(head, first_chunk, chunk_size, len(subseq))
                    if tail_num == '':
                        continue
                else:
##                    print 3, (head, first_chunk, resid)
                    tail_num = tail
                res += [calc_num_idx_in_str_2(int(tail_num)) - len(head)]
                continue                
            else:
##                print 4, (head, first_chunk, resid)
                # ���� ������ � ����� ���� ����������:
                if head == '' or str(int(first_chunk)-1)[-len(head):] == head:
                    if gen_chunks(resid, first_chunk) != None:
                        res += [calc_num_idx_in_str_2(int(first_chunk)) - len(head)]
                        continue
        if res != []:
            return min(res)
        
    len_wo_lead_zeros = len(subseq.lstrip('0'))
    zeros_num = len(subseq) - len_wo_lead_zeros
    if zeros_num > 0:
        if zeros_num == len(subseq):
            return calc_num_idx_in_str_2(int( '1'+subseq)) + 1
        else:
            return calc_num_idx_in_str_2(int(subseq[zeros_num:] + subseq[:zeros_num])) + len(subseq[zeros_num:])

# ������� ��� ��������������:
def profile__find_solution():
    subseq = '8899999'
    import time
    
    t1 = time.clock()
    naive_res = find_subseq(subseq, gen_num_seq())
    dt1 = time.clock() - t1
    
    t2 = time.clock()
    mumbo_jumbo_res = find_solution(subseq)
    dt2 = time.clock() - t2

    print
    print 'profile__find_solution() results:'
    print 'naive time', dt1
    print 'naive res:', naive_res
    print 'mumbo jumbo time:', dt2
    print 'mumbo jumbo res:', mumbo_jumbo_res
    print

    
#profile__find_solution()

# ������ ���� �������� �������� ������ �������:
def test1__find_solution():
    for i in range(1, 1000):
        subseq = str(i)
        if find_subseq(subseq, gen_num_seq()) != find_solution(subseq):
            print subseq
            print 'naive res:', find_subseq(subseq, gen_num_seq())
            print 'mumbo jumbo res:', find_solution(subseq)
            print 'test1__find_solution() failed'
            print
            break
    print 'test1__find_solution() passed'


#test1__find_solution()


def gen_seq_str(n):
    return ''.join(map(str, range(1, n)))


# ������ ���� �������� ������� ������ �������:
# ���� ���� ������ �� ����������������������, ������������ � �����
# (����� ������������ ����� ������������������ �������� � crash_lock = False)
# � �� �����-�� ���������� ������� ������������������ (��� n = 1000) ���� �� �����
# ������.
def test2__find_solution(n = 100, crash_lock = True):
    s = gen_seq_str(n)
    for width in range(1, n):
        if ((width * 100) % n == 0):
            print width
        for pos in range(0, n-width):
            subseq = s[pos:(pos+width)]
            if crash_lock or len(subseq) == len(subseq.lstrip('0')):
                if find_solution(subseq) != find_subseq(subseq, gen_num_seq()):
                    print 'test2__find_solution() failed at pos, width = ', pos, width
                    print 'got:', find_solution(subseq)
                    print 'expected:', find_subseq(subseq, gen_num_seq())
                    print s[pos:(pos+width)], subseq#, s
                    return
    print 'test2__find_solution() passed'


#test2__find_solution(n = 100)


def main():
    try:
        with open("in.txt") as fin:
            fout = open('out.txt', 'w')
            for line in fin:
                subseq = line.strip()
                fout.write('%d\n' % (find_solution(subseq)+1))        
    except IOError:
        print("������ ��� �������� ����� 'in.txt'. ��������, ��� �� ����������?")
        sys.exit(1)        
        

if __name__ == '__main__':
    pass
    main()
