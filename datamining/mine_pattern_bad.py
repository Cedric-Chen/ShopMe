import sys
from collections import Counter

def mine_pattern(filename, min_sup):
    data = open(filename,'r')
    dict_word = {}
    index=0
    for line in data:
        for word in line.strip().split('\t'):
            if frozenset([word]) not in dict_word:
                dict_word[frozenset([word])] = {index}
            else:
                dict_word[frozenset([word])] = dict_word[frozenset([word])] | {index}
        index += 1

    unfitword = []
    for word, value in dict_word.items():
        if len(value) < min_sup:
            unfitword.append(word)
    for word in unfitword:
        del dict_word[word]

    tag = 2
    get_out = True
    while(True):
        candidate = {}
        new_dict = dict(dict_word) 
        for word1, value1 in dict_word.items():
            if len(word1) != tag-1:
                continue
#            print(word1)
            for word2, value2 in dict_word.items():
                if len(word2) != tag-1:
                    continue
                new_word = word1 | word2
                if len(new_word) == tag:
                    if new_word not in candidate:
                        candidate[new_word] = 0
                    candidate[new_word] += 1
                else:
                    continue

                if candidate[new_word] == tag * (tag-1):
                    new_set = value1 & value2
                    if len(new_set) >= min_sup:
                        new_dict[new_word] = new_set
                        get_out = False

        if get_out:
            break
        get_out = True
        tag += 1
        dict_word = dict(new_dict)

    return dict_word

if __name__ == '__main__':
    patterns = mine_pattern(sys.argv[1], int(sys.argv[2]))
    with open('result.txt', 'w') as f:
        for key, value in patterns.items():
            f.write(', '.join(list(key)) )
            f.write('\n')
