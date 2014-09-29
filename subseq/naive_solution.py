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
    # Генератор элементов бесконечной последовательности
    i = 1
    while 1:
        s = str(i)
        for ch in s:
            yield ch
        i += 1


def find_solution_naively(subseq):
    return find_subseq(subseq, gen_num_seq()) + 1


def main():
    try:
        with open("in.txt") as fin:
            fout = open('out.txt', 'w')
            for line in fin:
                subseq = line.strip()
                fout.write('%d\n' % find_solution_naively(subseq))        
    except IOError:
        print("Ошибка при открытии файла 'in.txt'. Возможно, его не существует?")
        sys.exit(1)


if __name__ == '__main__':
    main()
