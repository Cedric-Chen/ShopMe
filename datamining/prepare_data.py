import os
def loadData(filePath, inv = False):
    '''
    Load data from a input file into memory with dictionary format.
    * Input file format: itemID \t userID \t rating \n
    * Output data format: {userID: {itemID: rating, ...}, ...}
    '''
    data = {}
    try:
        with open(filePath) as file:
            for line in file:
                line = line.replace("\n", "")
                tokens = line.split("\t")

                if len(tokens) < 2:
                    continue
                elif len(tokens) == 2:
                    item = tokens[0]
                    user = tokens[1]
                    rating = 1
                else:
                    item = tokens[0]
                    user = tokens[1]
                    rating = tokens[2]

                # Store data
                if inv == False:
                    data.setdefault(user, {})
                    data[user][item] = float(rating)
                else:
                    data.setdefault(item, {})
                    data[item][user] = float(rating)
            file.close()
    except IOError as e:
        print(e)
    return data

def to_reconstructed_file(data):
    with open('user_like.txt','w') as f:
        for key in data.keys():
            d = data[key]
            l = []
            for b in d.keys():
                if(d[b] >= 4):
                    l.append(b)
            if(l != []):
                f.write(','.join(l) + '\n')
