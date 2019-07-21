try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
import enchant
import time

d = enchant.Dict("en_US")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def caesar(message, shift):
    answer = ""
    for elem in message:
        shifted_ans = ord(elem) + shift
        if shifted_ans >= 123:
            shifted_ans -= 26
        answer += chr(shifted_ans)
    return answer

def decode(message):
    for i in range(len(alphabet)):
        yield caesar(message, i)


class Guess:
    def __init__(self, past, curr, upcoming):
        self.past = past
        self.curr = curr
        self.upcoming = upcoming

    def __lt__(self, other):
        if not self.past and not other.past:
            return other.curr < self.curr
        if not self.past:
            return True
        if not other.past:
            return False
        tie = max(self.past, key = len) == max(other.past, key = len)
        if not tie:
            return len(max(self.past, key = len)) - len(max(other.past, key = len))
        if len(self.past) == len(other.past):
            return other.curr < self.curr
        else:
            return len(other.past) < len(self.past)

def parse(word):
    fringe = Q.PriorityQueue()
    #fringe.put(Guess([], "", word))
    fringe = [Guess([], "", word)]
    count = 0
    while fringe:
        count += 1
        guess = fringe.pop()
        if not guess.upcoming:
            if not guess.curr:
                yield guess.past
            continue
        word = guess.curr + guess.upcoming[0]
        if d.check(word) and len(word) >= 2:
            fringe.append(Guess(guess.past[:] + [word], "", guess.upcoming[1:]))
        guess.curr += guess.upcoming[0]
        guess.upcoming = guess.upcoming[1:]
        fringe.append(guess)

def determine_longest(encoded):
    for x in decode(encoded):
        answers = list(parse(x))
        if answers:
            return min(answers, key = len)

def determine_fastest(encoded):
    for x in decode(encoded):
        answers = parse(x)
        try:
            return next(answers)
        except:
            continue

inp = input("enter the string to be encoded: ").lower()
num = int(input("enter how much you want to shift: "))
encoded = caesar(inp, num % 26)
print("This is your encoded message: " + encoded)
see_ans = input("Shall I break the encoded message? ")
answer = determine_longest(encoded)
print(answer)
