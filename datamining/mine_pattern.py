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
    old_dict = dict_word
    new_dict = {}
    while(True):
        candidate = []
        for word1, value1 in old_dict.items():
            for word2, value2 in old_dict.items():
                if word1 == word2:
                    continue
                new_word = word1 | word2
                if len(new_word) == tag:
                    candidate.append(new_word)

        candidate = Counter(candidate)
        for new_word, count in candidate.items():
            if count != tag * (tag-1):
                continue

            value1 = old_dict[frozenset(list(new_word)[1:])]
            value2 = old_dict[frozenset(list(new_word)[:-1])]
            new_set = value1 & value2
            if len(new_set) >= min_sup:
                new_dict[new_word] = new_set
                get_out = False

        if get_out:
            break
        get_out = True
        dict_word = {**dict_word, **new_dict}
        old_dict = new_dict
        new_dict = {}
        tag += 1
    return dict_word
#    tag = 2
#    get_out = True
#    while(True):
#        new_dict = dict(dict_word)
#        for word1, value1 in dict_word.items():
#            if len(word1) != tag - 1:
#                continue
#
#            for word2, value2 in dict_word.items():
#                if len(word2) != 1:
#                   continue
#                if word1 == word2:
#                    continue
#                if word2.issubset(word1):
#                    continue
#                new_word = word1 | word2
#                if new_word in dict_word:
#                    continue
#
#                new_set = value1 & value2
#                if len(new_set) >= min_sup:
#                    new_dict[new_word] = new_set
#                    get_out = False
#
#        if get_out:
#            break
#        get_out = True
#        dict_word = dict(new_dict)
#        tag += 1
#    return dict_word

if __name__ == '__main__':
    patterns = mine_pattern(sys.argv[1], int(sys.argv[2]))
    with open('result.txt', 'w') as f:
        for key, value in patterns.items():
            f.write(', '.join(list(key)) )
            f.write('\n')
