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

def gen_seq_str(n):
    return ''.join(map(str, range(1, n)))        

##for i in range(0, 999):
##    res = find_subseq(str(i), gen_num_seq())
##    if res < i:
##        print i

def calc_num_idx_in_str(i):
    if i <= 10:
        return i-1
    if i <= 100:
        return 10 + 2*(i-10) - 1
    if i <= 1000:
        return 10 + 2*(100 - 10) + 3*(i - 100) - 1

##res = []
##str_len = int(1e4)
##s = gen_seq_str(str_len)
##max_num = int(1e6)
##for i in range(str_len, max_num):
##    idx = s.find(str(i))
##    if idx == -1:
##        continue
##    if calc_num_idx_in_str(i) = idx:
##        res += [(str(i), idx)]


def split_str_in_chunks(s, chunk_size):
    (chunks_num, tail_len) = divmod(len(s), chunk_size)
    body = [s[i*chunk_size:(i+1)*chunk_size] for i in range(0, chunks_num)]
    if tail_len == 0:
        tail = ''
    else:
        tail = s[-tail_len:]
    return (body, tail)


def test__split_str_in_chunks():
    test_cases = (
        {
        'input':{
            's': '123456',
            'chunk_size': 2
            },
        'expected': (['12', '34', '56'], '')
        },
        {
        'input':{
            's': '123456',
            'chunk_size': 3
            },
        'expected': (['123', '456'], '')
        },
        {
        'input':{
            's': '123456',
            'chunk_size': 4
            },
        'expected': (['1234'], '56')
        },
        )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = split_str_in_chunks(i['s'], i['chunk_size'])
        if res != tc['expected']:
            test_OK = False
            print 'test test__split_str_in_chunks failed'
            print 'test_case:', tc
            print 'got:', res
            print 
    if test_OK:
        print 'test__split_str_in_chunks() passed'


test__split_str_in_chunks()


def gen_templates(sample):
    for i in range(1, len(sample) + 1):
        for j in range(1, i+1):
            head = sample[:j]
            (body, tail) = split_str_in_chunks(sample[j:], i)
            if tail != '':
                print i, ':', ('*'*(i-j) + head), body, (tail + '*'*(i-len(tail)))
            else:
                print i, ':', ('*'*(i-j) + head), body, "''"


# Пример шаблонов, получаемых при "разрезании" искомой подпоследовательности
# на куски. Разрезание идёт для поиска идущих подряд чисел
sample = '889'
gen_templates(sample)


def find_last_nines_subseq(s):
    n = 0
    for i in s[::-1]:
        if i == '9':
            n += 1
    if n == 0:
        return ''
                
    return s[-n-1:]


def test__find_last_nines_subseq():
    test_name = 'test__find_last_nines_subseq'
    tested_func = find_last_nines_subseq
    test_cases = (
        {
        'input':{
            's': '434'
            },
        'expected': ''
        },
        {
        'input':{
            's': '8889'
            },
        'expected': '89'
        },
        )
    test_OK = True
    for tc in test_cases:
        i = tc['input']
        res = tested_func(i['s'])
        if res != tc['expected']:
            test_OK = False
            print '%s failed' % test_name
            print 'test_case:', tc
            print 'got:', res
            print 
    if test_OK:
        print '%s passed' % test_name


test__find_last_nines_subseq()


def head_and_tail_tmpls_may_be_neighbours(head_chunk,
                                          tail_chunk,
                                          subseq_len):
    if subseq_len == len(head_chunk):
        return True
    head_str = head_chunk.strip('*')
    k = len(head_str)
    N = subseq_len
    
    head_num = int(head_str)
    inc_head = str(head_num+1)[-k:]
    inc_head_chunk = '*'*(len(head_chunk) - k) + inc_head
    
    return inc_head_chunk[-k:N-k] == tail_chunk[-k:N-k]


def test__head_and_tail_tmpls_may_be_neighbours():
    test_name = 'test__head_and_tail_tmpls_may_be_neighbours'
    tested_func = head_and_tail_tmpls_may_be_neighbours
    test_cases = (
        {
        'input':{
            'chunked_head': '****86',
            'chunked_tail': '4535**',
            'subseq_len': 6
            },
        'expected': True
        },
        {
        'input':{
            'chunked_head': '8645',
            'chunked_tail': '86**',
            'subseq_len': 6
            },
        'expected': True
        },
        {
        'input':{
            'chunked_head': '*864',
            'chunked_tail': '535*',
            'subseq_len': 6
            },
        'expected': False
        },
        {
        'input':{
            'chunked_head': '*864',
            'chunked_tail': '586*',
            'subseq_len': 6
            },
        'expected': True
        },
        {'input':{
            'chunked_head': '*869',
            'chunked_tail': '586*',
            'subseq_len': 6
            },
        'expected': False
        },
        {'input':{
            'chunked_head': '*869',
            'chunked_tail': '587*',
            'subseq_len': 6
            },
        'expected': True
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


test__head_and_tail_tmpls_may_be_neighbours()
    

def intersect_head_and_tail_chunks(head_chunk,
                                          tail_chunk,
                                          subseq_len):
    head_str = head_chunk.strip('*')
    k = len(head_str)
    N = subseq_len
    
    head_num = int(head_str)
    inc_head = str(head_num+1)[-k:]
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

test__intersect_head_and_tail_chunks()


def next_num_str(num_str):
    return str(int(num_str)+1)


def chunk_num_by_head_and_chunk(head,
                                chunk):
    k = len(head)
    head_num = int(head)
    inc_head = next_num_str(head)
    
    if chunk[-k:] == inc_head[-k:]:
        return chunk
    return ''


def tail_and_chunk_are_consistent(chunk,
                           tail):
    k = len(tail)
    inc_chunk = next_num_str(chunk)
    
    return inc_chunk[:k] == tail


def chunks_are_consistent(chunk1, chunk2):
    return chunk1.lstrip('0') == chunk1 and next_num_str(chunk1) == chunk2


def head_chunks_and_tail_are_consistent(head, chunks, tail):
    inc_head_str = chunk_num_by_head_and_chunk(head, chunks[0])
    if inc_head_str == '':
        return False
    for i in range(0, len(chunks)-1):
        if not chunks_are_consistent(chunks[i], chunks[i+1]):
            return False
    if tail != '' and not tail_and_chunk_are_consistent(chunks[-1], tail):
        return False
    return inc_head_str
    


def gen_templates(sample):
    for i in range(1, len(sample) + 1):
        for j in range(1, i+1):
            head = sample[:j]
            (body, tail) = split_str_in_chunks(sample[j:], i)
            chunk_size = (i-j+len(head))
            yield (head, body, tail, chunk_size)


def chunks_are_numbers(chunks):
    return reduce(lambda res, ch: res and ch.lstrip('0') == ch, chunks, True)


def find_solution(sample):
    for i in range(1, len(sample) + 1):
        fres = None
        for j in range(1, i+1):
            head = sample[:j]
            (body, tail) = split_str_in_chunks(sample[j:], i)
            if not chunks_are_numbers(body):
                continue
            if tail.lstrip('0') != tail:
                continue
            chunk_size = (i-j+len(head))
            
            if body != []:
                res = head_chunks_and_tail_are_consistent(head, body, tail)
                if res != False:
                    if fres == None:
                        fres = calc_num_idx_in_str(int(res)) - len(head)
                    else:
                        fres = min(fres, calc_num_idx_in_str(int(res)) - len(head))
            else:
                head_chunk = (chunk_size - len(head))*'*' + head
                tail_chunk = tail + (chunk_size - len(tail))*'*'
                res = intersect_head_and_tail_chunks(head_chunk, tail_chunk, len(subseq))
                if res != '':
                    if fres == None:
                        fres = calc_num_idx_in_str(int(res)) - len(head)
                    else:
                        fres = min(fres, calc_num_idx_in_str(int(res)) - len(head))
            #print (head,body, tail, i, j, fres)  
        if fres != None:
            return fres
    return None

##subseq = '88999'
##import time
##start = time.clock()
##find_subseq(subseq, gen_num_seq())
##dt1 = time.clock() - start
##t1 = time.clock()
##find_solution(subseq)
##dt2 = time.clock() - t1
##print dt1, dt2
##print 'naive res:', find_subseq(subseq, gen_num_seq())
##print 'mumbo jumbo res:', find_solution(subseq)
##
##for i in range(1, 1000):
##    subseq = str(i)
##    if find_subseq(subseq, gen_num_seq()) != find_solution(subseq):
##        print subseq
##        print 'naive res:', find_subseq(subseq, gen_num_seq())
##        print 'mumbo jumbo res:', find_solution(subseq)
##        break


def gen_head(subseq, chunk_size):
    return map(lambda i: (subseq[:i], subseq[i:]), range(1, chunk_size+1))


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


test__gen_head()


def is_dec_number(s):
    return len(s.lstrip('0')) == len(s)


def is_ten_pow(s):
    return s.rstrip('0') == '1'


def gen_next_chunk_by_head(resid, head, chunk_size):
    if len(resid) >= chunk_size:
        # Могут ли голова и следующий за ней "кусок" являться последовательными числами
        # с одинаковым количеством разрядов?
        h_len = len(head)
        head_inc = next_num_str(head)[-h_len:]
        chunk_c = resid[:chunk_size]
        # следующий "кусок" является десятичной записью числа (не начинается с нулей)
        # следующее число с таким же количеством разрядов не может быть степенью 10
        # "хвост" следующего числа должен быть на 1 больше головы
        if is_dec_number(chunk_c) and not is_ten_pow(chunk_c) and chunk_c[-h_len:] == head_inc:
            return (chunk_c, resid[chunk_size:])

    if len(resid) > chunk_size:
    # Возможно, тогда голова имеет вид "99...9" и следующий кусок
    # является числом вида "100...0"?
        chunk_c = resid[:(chunk_size+1)]
        if head.strip('9') == '' and\
           is_ten_pow(chunk_c):
            return (chunk_c, resid[(chunk_size+1):])
    # В противном случае: кусок с таким количеством разрядов не совместим с текущей головой.
    return None


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
        'expected': None
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
        'expected': None
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


test__gen_next_chunk_by_head()


def gen_next_chunk(resid, cur_chunk):
    chunk_size = len(cur_chunk)
    if len(resid) >= chunk_size:
        # Могут ли голова и следующий за ней "кусок" являться последовательными числами
        # с одинаковым количеством разрядов?
        cur_chunk_inc = next_num_str(cur_chunk)
        next_chunk_c = resid[:chunk_size]
        # следующий "кусок" является десятичной записью числа (не начинается с нулей)
        # следующее число с таким же количеством разрядов не может быть степенью 10
        # число из следующего куска должно быть на 1 больше числа из текущего куска
        if is_dec_number(next_chunk_c) and\
           not is_ten_pow(next_chunk_c) and\
           next_chunk_c == cur_chunk_inc:
            return (next_chunk_c, resid[chunk_size:])

    if len(resid) > chunk_size:
    # Возможно, тогда голова имеет вид "99...9" и следующий кусок
    # является числом вида "100...0"?
        next_chunk_c = resid[:(chunk_size+1)]
        if cur_chunk.strip('9') == '' and\
           is_ten_pow(next_chunk_c):
            return (next_chunk_c, resid[(chunk_size+1):])
    # В противном случае: кусок с таким количеством разрядов не совместим с текущим куском.
    return None


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
        'expected': None
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
        'expected': None
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


test__gen_next_chunk()
        

def gen_chunks(resid, first_chunk):
    chunk_size = len(first_chunk)
    chunks = [first_chunk]
    cur_chunk = first_chunk
    while len(resid) >= chunk_size:
        next_chunk_res = gen_next_chunk(resid, cur_chunk)
        if next_chunk_res == None:
            if len(resid) == chunk_size:
                return (chunks, resid)
            return None
        (next_chunk, resid) = next_chunk_res
        chunks += [next_chunk]
        cur_chunk = next_chunk
    return (chunks, resid)


def test__gen_chunks():
    test_name = 'test__gen_chunks'
    tested_func = gen_chunks
    test_cases = (
        {
        'input':{
            'first_chunk': '1',
            'resid': '234',
            },
        'expected': (['1', '2', '3', '4'], '')
        },
        {
        'input':{
            'first_chunk': '1',
            'resid': '235',
            },
        'expected': (['1', '2', '3'], 5)
        },
        {
        'input':{
            'first_chunk': '12',
            'resid': '131',
            },
        'expected': (['12', '13'], '1')
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '1001',
            },
        'expected': (['99', '100'], '1')
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '100',
            },
        'expected': (['99', '100'], '')
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '7',
            },
        'expected': (['99'], '7')
        },
        {
        'input':{
            'first_chunk': '99', 
            'resid': '10',
            },
        'expected': (['99'], '10')
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


test__gen_chunks()



def last_chunk_and_tail_are_consistent(last_chunk, tail):
    if tail == '':
        return True
    if last_chunk.strip('9') == '': # если последний кусок есть число 99..99
        return tail.strip('0') == '1' # tail должен выглядеть как 100.000
    inc_chunk = next_num_str(last_chunk)    
    return inc_chunk[:len(tail)] == tail


def gen_tail_num_by_head(head,
                         tail,
                         chunk_size,
                         subseq_len):
    head_chunk = '*'*(chunk_size - len(head)) + head
    if not is_dec_number(tail):
        return ''
    tail_chunk = tail + '*'*(chunk_size - len(tail))
    return intersect_head_and_tail_chunks(head_chunk, tail_chunk, subseq_len)


subseq = '88999'
def find_solution(subseq):
    for chunk_size in range(1, len(subseq)+1):
        res = []
        for (head, resid) in gen_head(subseq, chunk_size):
            if len(resid) >= chunk_size:
                next_chunk_res = gen_next_chunk_by_head(resid, head, chunk_size)
                if next_chunk_res == None:
                    continue
                (first_chunk, resid) = next_chunk_res
                chunks_res = gen_chunks(resid, first_chunk)
                if chunks_res == None:
                    continue
                (chunks, resid) = chunks_res
                tail = resid
                if not last_chunk_and_tail_are_consistent(chunks[-1], tail):
                    continue
                res += [calc_num_idx_in_str(int(chunks[0])) - len(head)]
            else:
                chunks = []
                tail = resid
                if tail != '':
                    tail_num = gen_tail_num_by_head(head, tail, chunk_size, len(subseq))
                    if tail_num == '':
                        continue
                    res += [calc_num_idx_in_str(int(tail_num)) - len(head)]
                else:
                    res += [calc_num_idx_in_str(int(head))]
        if res != []:
            return min(res)


subseq = '88999'
import time
start = time.clock()
find_subseq(subseq, gen_num_seq())
dt1 = time.clock() - start
t1 = time.clock()
find_solution(subseq)
dt2 = time.clock() - t1
print dt1, dt2
print 'naive res:', find_subseq(subseq, gen_num_seq())
print 'mumbo jumbo res:', find_solution(subseq)

for i in range(1, 1000):
    subseq = str(i)
    if find_subseq(subseq, gen_num_seq()) != find_solution(subseq):
        print subseq
        print 'naive res:', find_subseq(subseq, gen_num_seq())
        print 'mumbo jumbo res:', find_solution(subseq)
        break  

