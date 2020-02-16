##Robert frost poem read

import numpy as np
import string

#probability distributions of start of a phrase
initial = {}
#distributions of second word of a sentence
second_word = {}
#dictionary of 2nd order transition
transitions = {}

#remove all punctuations
def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))

#dictionary , key , value order
def add2dict(d, k, v):
    if k not in d:
        d[k] = []
    d[k].append(v)

#looping through the poem
for line in open("robert_frost.txt", 'rt', encoding='UTF8'):
    #read the entire poem and split into tokens
    tokens = remove_punctuation(line.rstrip().lower()).split()


    T = len(tokens)
    for i in range(T):
        t = tokens[i]
        if i == 0:# first work
            # keeping counts of the loop
            initial[t] = initial.get(t, 0.) + 1
        else:
            # we get the previous work
            t_1 = tokens[i-1]
            if i == T - 1:
                # it means it is the last work. the end of a line
                add2dict(transitions, (t_1, t), 'END')
            if i == 1:
                # 2nd word of a sentence
                add2dict(second_word, t_1, t)
            else:
                t_2 = tokens[i-2]
                add2dict(transitions, (t_2,t_1), t)

# normalize the distribution
initial_total = sum(initial.values())
for t, c in initial.items():
    initial[t] = c / initial_total

#take a list and turn it into dictionary
def list2pdict(ts):
    d={}
    n = len(ts)
    for t in ts:
        d[t] = d.get(t, 0.) + 1
    for t, c in d.items():
        d[t] = c/n
    return d

for t_1, ts in second_word.items():
    second_word[t_1] = list2pdict(ts)

for k, ts in transitions.items():
    transitions[k] = list2pdict(ts)

#sample a word from a dictionary of probabilitoies
def sample_word(d):
    p0 = np.random.random()
    cumulative = 0
    for t, p in d.items():
        cumulative += p
        if p0 < cumulative:
            return t

    assert(False)

#it generate a poem
def generate():
    for i in range(4):
        sentence = []

        # initial word
        w0 = sample_word(initial)
        sentence.append(w0)

        # sample second word
        w1 = sample_word(second_word[w0])
        sentence.append(w1)

        # second-order transitions until END
        while True:
            w2 = sample_word(transitions[(w0, w1)])
            if w2 == 'END':
                break
            sentence.append(w2)
            w0 = w1
            w1 = w2
        print(' '.join(sentence))


generate()
