import time
import random
from functools import lru_cache
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles


class Parser:
    def __init__(self, string: str):
        self.string = string
        if string == None:
            self.n = 0
        else:
            self.n = len(string)


    def check(self) -> bool:
        s = self.string
        n = self.n


        @lru_cache(maxsize=None)
        def parse_T(i: int, j: int) -> frozenset:


            if j - i < 1:
                return frozenset()

            result = set()

            if j - i == 1 and s[i:j+1] == "ab":
                result.add(1)

            for k in range(i + 1, j):
                if s[k + 1] == 'a':

                    left = parse_S(i, k)
                    right = parse_T(k + 2, j)
                    for v1 in left:
                        for v2 in right:
                            result.add(v1 + v2 + 1)

            return frozenset(result)

        @lru_cache(maxsize=None)
        def parse_S(i: int, j: int) -> frozenset:


            if j - i < 1:
                return frozenset()

            result = set()
            s_sub = s[i:j+1]


            if j - i == 1 and s_sub == "bb":
                result.add(0)


            if s[i] == 'a' and j - i > 1:
                t = parse_T(i+1, j)
                for v in t:
                    result.add(1+v)



            for k in range(i + 1, j):

                left = parse_T(i, k)
                right = parse_T(k + 1, j)
                for v1 in left:
                    for v2 in right:
                        if v1 == v2:
                            result.add(v1 + v2)

            for k in range(i + 1, j):
                if s[k + 1:k + 3] == "ab":

                    left = parse_S(i, k)
                    right = parse_S(k + 3, j)
                    for v1 in left:
                        for v2 in right:
                            if v1 > v2:
                                result.add(0)
                            else:
                                result.add(v2)


            return frozenset(result)



        return bool(bool(parse_S(0, n-1)))








class Parser_OPT:
    def __init__(self, string: str):
        self.string = string
        self.n = len(string)


    def check(self) -> bool:
        s = self.string
        n = self.n


        @lru_cache(maxsize=None)
        def parse_T(i: int, j: int) -> frozenset:



            if j - i < 1:
                return frozenset()

            if s[i:i+2] == "ba" or s[j] == 'a':
                return frozenset()

            result = set()

            if j - i == 1 and s[i:j+1] == "ab":
                result.add(1)

            for k in range(i + 1, j):
                if s[k + 1] == 'a':

                    left = parse_S(i, k)
                    right = parse_T(k + 2, j)
                    for v1 in left:
                        for v2 in right:
                            result.add(v1 + v2 + 1)

            return frozenset(result)

        @lru_cache(maxsize=None)
        def parse_S(i: int, j: int) -> frozenset:


            if j - i < 1:
                return frozenset()

            if s[i:i+2] == "ba" or s[j] == 'a':
                return frozenset()

            result = set()
            s_sub = s[i:j+1]


            if j - i == 1 and s_sub == "bb":
                result.add(0)


            if s[i] == 'a' and j - i > 1:
                t = parse_T(i+1, j)
                for v in t:
                    result.add(1+v)



            for k in range(i + 1, j):

                left = parse_T(i, k)
                right = parse_T(k + 1, j)
                for v1 in left:
                    for v2 in right:
                        if v1 == v2:
                            result.add(v1 + v2)

            for k in range(i + 1, j):
                if s[k + 1:k + 3] == "ab":

                    left = parse_S(i, k)
                    right = parse_S(k + 3, j)
                    for v1 in left:
                        for v2 in right:
                            if v1 > v2:
                                result.add(0)
                            else:
                                result.add(v2)


            return frozenset(result)



        return bool(bool(parse_S(0, n-1)))



def generate(size):
    s = ""
    for i in range(size):
        s=s+ chr(ord('a')+random.getrandbits(1))
    return s





def test_parser():
    test_cases = [
        ("bb", True),
        ("babbbbbbbb", False),
        ("abab", True),
        ("bbaabaaaabaabaababaaabaabaab", True),
        ("bbaabaaabaababaaabaabaab", False),
        ("ababababab", True),
        ("abababababab", False),


    ]

    for test, expected in test_cases:
        parser1= Parser(test)

        parser2 = Parser_OPT(test)

        start_time1 = time.time()
        result1 = parser1.check()
        end_time1 = time.time()

        start_time2 = time.time()
        result2 = parser2.check()
        end_time2 = time.time()

        time_taken1 = (end_time1 - start_time1) * 1000
        time_taken2 = (end_time2 - start_time2) * 1000
        print(f"Строка длиной {len(test)} с результатом: {expected}: Результат обычный:{result1}, Время обычное: {time_taken1:.6f} мс, Результат оптимизированный:{result2},Время оптимизированное: {time_taken2:.6f} мс")


def generate_only_true():
    def T(n):
        if n > 2:
            l = random.randint(0, n)
            t1 = S(l)
            t2 = T(n-l)
            return [t1[0] + "a" + t2[0], 1 + t1[1] + t2[1]]
        else:
            return ["ab", 1]

    def S(n):
        if n < 3:
            return ["bb", 0]

        p = random.randint(0, 2)

        if p == 0:
            l = random.randint(0, n)
            t1 = S(l)
            t2 = S(n - l)
            if t1[1] > t2[1]:
                return [t1[0] + "ab" + t2[0], 0]
            else:
                return [t1[0] + "ab" + t2[0], t2[1]]
        elif p == 1:
            t = T(n-1)
            return ["a"+ t[0], 1 + t[1]]
        else:
            l = random.randint(0, n)
            t1 = T(l)
            t2 = T(n - l)
            if t1[1] == t2[1]:
                return [t1[0] + t2[0], 2*t1[1]]
            else:
                t = T(n - 1)
                return ["a" + t[0], 1 + t[1]]

    return S(random.randint(2, 100))[0]

def generate_only_false():
    if random.getrandbits(1) == 1:
        s= "ba"
        for i in range(random.randint(1, 40)):
            s = s + chr(ord('a') + random.getrandbits(1))
        return s
    else:
        s = ""
        for i in range(random.randint(1, 40)):
            s = s + chr(ord('a') + random.getrandbits(1))
        s = s + "a"

        return s



def fuzz():
    Parser_EQ = True
    for i in range(10):
        test = generate(random.randint(10, 100))
        parser1 = Parser(test)

        parser2 = Parser_OPT(test)

        start_time1 = time.time()
        result1 = parser1.check()
        end_time1 = time.time()

        start_time2 = time.time()
        result2 = parser2.check()
        end_time2 = time.time()

        time_taken1 = (end_time1 - start_time1) * 1000
        time_taken2 = (end_time2 - start_time2) * 1000
        if result1 != result2:
            Parser_EQ=False
            break
        print(
            f"Строка длиной {len(test)}: Результат обычный:{result1}, Время обычное: {time_taken1:.6f} мс, Результат оптимизированный:{result2},Время оптимизированное: {time_taken2:.6f} мс")


    print(f"Парсеры эквивалентны:{Parser_EQ}")

    x = []
    y1 = []
    y2 = []

    for i in range(100):
        test = generate_only_true()
        parser1 = Parser(test)

        parser2 = Parser_OPT(test)

        start_time1 = time.time()
        result1 = parser1.check()
        end_time1 = time.time()

        start_time2 = time.time()
        result2 = parser2.check()
        end_time2 = time.time()

        time_taken1 = (end_time1 - start_time1) * 1000
        time_taken2 = (end_time2 - start_time2) * 1000
        x.append(len(test))
        y1.append(time_taken1)
        y2.append(time_taken2)
        print(f"Строка длиной {len(test)}: Результат обычный:{result1}, Время обычное: {time_taken1:.6f} мс, Результат оптимизированный:{result2},Время оптимизированное: {time_taken2:.6f} мс")

    combined_true = sorted(zip(x, y1, y2), key=lambda t: t[0])
    x_true_sorted, y1_true_sorted, y2_true_sorted = zip(*combined_true)

    x = list(x_true_sorted)
    y1 = list(y1_true_sorted)
    y2 = list(y2_true_sorted)

    plt.figure(figsize=(10, 6))

    plt.plot(x, y1,
             label='Обычный парсер',
             marker='o',
             linestyle='-',
             linewidth=2,
             color='blue',
             )

    plt.plot(x, y2,
             label='Оптимизированный',
             marker='s',
             linestyle='--',
             linewidth=2,
             color='red')

    plt.title('True', fontsize=14)
    plt.xlabel('Длинна слова', fontsize=12)
    plt.ylabel('Время', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()

    plt.savefig('C:/Users/juga/Desktop/my_graph.png')

    x = []
    y1 = []
    y2 = []

    for i in range(100):
        test = generate_only_false()
        parser1 = Parser(test)

        parser2 = Parser_OPT(test)

        start_time1 = time.time()
        result1 = parser1.check()
        end_time1 = time.time()

        start_time2 = time.time()
        result2 = parser2.check()
        end_time2 = time.time()

        time_taken1 = (end_time1 - start_time1) * 1000
        time_taken2 = (end_time2 - start_time2) * 1000
        x.append(len(test))
        y1.append(time_taken1)
        y2.append(time_taken2)
        print(f"Строка длиной {len(test)}: Результат обычный:{result1}, Время обычное: {time_taken1:.6f} мс, Результат оптимизированный:{result2},Время оптимизированное: {time_taken2:.6f} мс")

    combined_false = sorted(zip(x, y1, y2), key=lambda t: t[0])
    x_true_sorted, y1_true_sorted, y2_true_sorted = zip(*combined_false)

    x = list(x_true_sorted)
    y1 = list(y1_true_sorted)
    y2 = list(y2_true_sorted)


    plt.figure(figsize=(10, 6))



    plt.plot(x, y1,
             label='Обычный парсер',
             marker='o',
             linestyle='-',
             linewidth=2,
             color='blue')

    plt.plot(x, y2,
             label='Оптимизированный',
             marker='s',
             linestyle='--',
             linewidth=2,
             color='red')

    plt.title('False', fontsize=14)
    plt.xlabel('Длинна слова', fontsize=12)
    plt.ylabel('Время', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()

    plt.savefig('C:/Users/juga/Desktop/my_graph2.png')

if __name__ == "__main__":
    #test_parser()
    fuzz()
