import enchant
from random import randint

"""
FUTURE NOTES
Does not support punctuation
Does not work efficiently on long inserts for the subsitution decoder (nor does it return the correct answer on small ones)
Caesar cipher works perfectly fine

GOALS
connect to a web app
"""
class Answers():
    def __init__(self, c, default = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'], o = False):
        self.code = c.lower()
        self.alphabet = default
        self.has_spaces = False
        self.dictionary = self.create_dict()

    def create_dict(self):
            """Return a list that has each alphabet letter in code ordered by frequency """
            d = {}
            for char in self.code:
                if char.isspace():
                    self.has_spaces = True
                    continue
                elif char not in d:
                    d[char] = 1
                else:
                    d[char] += 1
            return d

    def next(self):
            """ Spit's out next most likely guess """
            try:
                return next(self.spitter)
            except:
                return False

class Substution(Answers):
    def __init__(self, c, default = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'], o = False):
        Answers.__init__(self, c, default)
        if o == False:
            self.ordered = self.sort_dict()
        else:
            self.ordered = o
        self.spitter = self.spit()

    def all_but(self, i, lst):
        return lst[:i] + lst[i + 1:]

    def sort_dict(self):
        sorted_items = sorted(self.dictionary.items(), key = lambda a: a[1], reverse = True)
        return [item[0] for item in sorted_items]

    def which_changed(self, code_pop, alpha_pop):
        def f(char):
            if (char == code_pop):
                return True
            else:
                return False
        return [f(i) for i in self.code]

    def final_ans(self, changed_bools, changed_answer, alpha_pop):
        def f(i):
            if changed_bools[i]:
                return alpha_pop
            else:
                return changed_answer[i]
        new_ans = [f(i) for i in range(len(changed_answer))]
        return "".join(new_ans)

    def all_outputs(self, i):
        one = self.all_but(i, self.alphabet)
        two = self.alphabet[i]
        three = self.ordered[1:]
        four = self.ordered[0]
        return one, two, three, four

    def spit(self):
        """ Generator that yields all possible interpretations """
        if not self.code:
            return
        if not self.ordered:
            yield self.code
            return
        for i in range(len(self.alphabet)):
            new_alphabet, alpha_pop, new_ordered, code_pop = self.all_outputs(i)
            next_ans = Substution(self.code, new_alphabet, new_ordered)
            for changed_answer in next_ans.spit():
                changed_bools = self.which_changed(code_pop, alpha_pop)
                yield self.final_ans(changed_bools, changed_answer, alpha_pop)

class Caesar(Answers):
    def __init__(self, c):
        Answers.__init__(self, c)
        self.spitter = self.spit()

    def spit(self):
        """ Spits out the 26 potential answers in order of most likely """
        max_elem = ord(max(self.dictionary.items(), key = lambda a: a[1])[0])
        for index in range(26):
            shift = ord(self.alphabet[index]) - max_elem  #check if the most popular was this one
            yield self.shifted_by(shift)

    def shifted_by(self, diff):
        ans = []
        for char in self.code:
            if char.isspace():
                ans.append(char)
            else:
                letter = ord(char) + diff
                if letter < 97:
                    letter = 123 - (97 - letter)
                elif letter > 122:
                    letter = letter % 123 + 97
                ans.append(chr(letter))
        return "".join(ans)

class Decoder:
    def __init__(self, instance, num = None):
        self.webster = enchant.Dict('en_US')
        self.instance = instance # Needs to be some Answers instance
        if num == None:
            self.num_words = len(self.instance.code)
        else:
            self.num_words = num
        self.answer_gen = self.answers()

    def next(self):
            """ Spit's out next most likely guess """
            try:
                return next(self.answer_gen)
            except:
                return False

    def answers(self):
        return self.get_answers(self.num_words)

    def get_answers(self, num_words):
        """ A Generator that yields all potential answers """
        word = ""
        while word is not False:
            word = self.instance.next()
            if self.instance.has_spaces:
                yield from self.dissect_spaces(word)
            else:
                yield from self.dissect(word, num_words)

    def dissect(self, word, num):
        """ We want to see if any words can be constructed from this string """
        if not num or not word or len(word) < 2:
            return
        if self.webster.check(word):
            yield word
        for i in range(1, len(word)):
            first, rest = word[:i], word[i:]
            if len(first) >= 2 or first == 'i' or first == 'a':
                if self.webster.check(first):
                    for answer in self.dissect(rest, num - 1):
                        yield first + " " + answer

    def dissect_spaces(self, word):
        """ Check if the given string is a sentence """
        if not word:
            return
        text = word.split()
        for w in text:
            if not self.webster.check(w):
                return
        yield word

class Encode_Caesar():
    def __init__(self, word):
        self.alphabet = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']
        self.word = word.lower()
        self.shift = randint(0, len(self.alphabet) - 1)
        self.encoded = self.encode()

    def encode(self):
        ans = []
        for char in self.word:
            if char.isspace():
                ans.append(char)
            else:
                letter = ord(char) + self.shift
                if letter < 97:
                    letter = 123 - (97 - letter)
                elif letter > 122:
                    letter = letter % 123 + 97
                ans.append(chr(letter))
        return "".join(ans)

class Encode_Substution():
    def __init__(self, word):
        self.alphabet = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']
        self.word = word
        self.d = self.dictionize()
        self.encoded = self.encode()

    def dictionize(self):
        d = {}
        for char in self.word:
            if char not in d:
                d[char] = self.random_char()
        return d

    def encode(self):
        return "".join([self.d[char] for char in self.word])

    def random_char(self):
        return self.alphabet.pop(randint(0, len(self.alphabet) - 1))

def test(word):
    e = Encode_Caesar(word)
    print(e.encoded)
    s = Caesar(e.encoded)
    d = Decoder(s, 1)
    print(list(d.answer_gen))

test("butterfly")
