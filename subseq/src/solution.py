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


#test__gen_next_chunk_by_head()


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


#test__gen_next_chunk()
        

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
        'expected': (['1', '2', '3'], '5')
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


#test__gen_chunks()



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


def find_solution(subseq):
    for chunk_size in range(1, len(subseq)+1):
        res = []
        for (head, full_resid) in gen_head(subseq, chunk_size):
            #print chunk_size, '"%s" "%s"' % (head, resid)
            if len(full_resid) >= chunk_size:
                next_chunk_res = gen_next_chunk_by_head(full_resid, head, chunk_size)
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
                res += [calc_num_idx_in_str_2(int(chunks[0])) - len(head)]
            else:
                chunks = []
                tail = full_resid
                if tail != '':
                    tail_num = gen_tail_num_by_head(head, tail, chunk_size, len(subseq))
                    if tail_num == '':
                        continue
                    res += [calc_num_idx_in_str_2(int(tail_num)) - len(head)]
                else:
                    res += [calc_num_idx_in_str_2(int(head))]
        if res != []:
            return min(res)


# Функция для профилирования:
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

# Первый тест основной фуункции поиска решения:
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


# Второй тест основной функции поиска решения:
# Этот тест падает на подпоследовательностях, начинающихся с нулей
# (чтобы игнорировать такие последовательности вызывать с crash_lock = False)
# и на какой-то достаточно длинной последовательности (для n = 1000) пока не понял
# почему.
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
                    print s[pos:(pos+width)]
                    return
    print 'test2__find_solution() passed'


#test2__find_solution(crash_lock = False)


def main():
    try:
        with open("in.txt") as fin:
            fout = open('out.txt', 'w')
            for line in fin:
                subseq = line.strip()
                fout.write('%d\n' % (find_solution(subseq)+1))        
    except IOError:
        print("Ошибка при открытии файла 'in.txt'. Возможно, его не существует?")
        sys.exit(1)        
        

if __name__ == '__main__':
    main()
