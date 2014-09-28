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


##def gen_num_seq():
##    i = 1
##    while 1:
##        s = str(i)
##        for el in s:
##            yield s
##        i += 1

def gen_seq_str(n):
    return ''.join(map(str, range(0, n)))        

##for i in range(0, 999):
##    res = find_subseq(str(i), gen_num_seq())
##    if res < i:
##        print i

def calc_num_idx_in_str(i):
    if i <= 10:
        return i
    if i <= 100:
        return 10 + 2*(i-10)
    if i <= 1000:
        return 10 + 2*(100 - 10) + 3*(i - 100)

res = []
str_len = int(1e4)
s = gen_seq_str(str_len)
max_num = int(1e6)
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


def head_and_chunk_are_neighbours(n, head, chunk):
    nh = len(head)
    nt = len(tail)
    test_num_str = tail[:(n-nh)] + head
    test_num = int(test_num_str) + 1
    return tail == str(test_num)[-nt:]


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
    inc_head = '*'*(len(head_chunk) - k) + inc_head
    #print 'head[-k:ss_len-k]:', ('*'*(ch_sz-k)+head)[-k:ss_len-k]
    #print 'tail[-k:ss_len-k]:', (tail+'*'*(ch_sz-ss_len+k))[-k:ss_len-k]
    #chunked_head = '*'*(ch_sz - k) + head
    #chunked_tail = tail + '*'*(ch_sz - (ss_len-k))
    
    return inc_head[-k:N-k] == tail_chunk[-k:N-k]


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
    


##def head_and_tail_tmpls_may_be_neighbours(chunked_head,
##                                          chunked_tail,
##                                          subseq_len):
##    if subseq_len == len(chunked_head):
##        return True
##    k = len(chunked_head.strip('*'))
##    N = subseq_len
##    #print 'head[-k:ss_len-k]:', ('*'*(ch_sz-k)+head)[-k:ss_len-k]
##    #print 'tail[-k:ss_len-k]:', (tail+'*'*(ch_sz-ss_len+k))[-k:ss_len-k]
##    #chunked_head = '*'*(ch_sz - k) + head
##    #chunked_tail = tail + '*'*(ch_sz - (ss_len-k))
##    
##    return chunked_head[-k:N-k] == chunked_tail[-k:N-k]
