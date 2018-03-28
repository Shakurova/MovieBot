# -*- coding: utf-8 -*-

import ujson

dictionary = {}
from normalization import normalize, movie_cleaner


def create_dict(arr):
    global dictionary
    # print('!!!!!!!!', len(arr))
    # print('????', len(dictionary.keys()))
    for i in '#'.join(arr).split('BREAK'):
        a = [a for a in i.split('#') if a != '']
        if len(a) > 3:
            name = a[0].replace("'", "")
            # score = a[2].replace("'", "")
            # helpfulness = a[1].replace("'", "")
            if name not in dictionary:
                dictionary[name] = {}
                dictionary[name]['review'] = []
                dictionary[name]['review'].append((a[1], a[2], a[3]))
            else:
                dictionary[name]['review'].append((a[1], a[2], a[3]))

    # # for i in dictionary:
    # #     print(i, dictionary[i])

    with open('amazon2.json', 'w') as w:
        ujson.dump(dictionary, w)
    # return dictionary


def amazon_parser(filename='amazon_movies.txt'):

    with open(filename, 'rb') as f:
        count = 0
        arr = []

        for line in f:
            # print(line)
            # line = str(line, 'utf-8')
            count += 1
            if count < 80000000:
                # if count / 10 == 0:
                #     print(count)
                # print(str(line).split(':')[0])
                # print(str(line).split(':')[0][2::])
                if line != b"\n":
                    if str(line).split(':')[0][2::] == 'product/productId':
                        arr.append(str(line).replace('\\n', '').split(': ')[1])
                    if str(line).split(':')[0][2::] == 'review/text':
                        arr.append(str(line).replace('\\n', '').split('review/text: ')[1])
                    if str(line).split(':')[0][2::] == 'review/helpfulness':
                        arr.append(str(line).replace('\\n', '').split(': ')[1])
                    if str(line).split(':')[0][2::] == 'review/score':
                        arr.append(str(line).replace('\\n', '').split(': ')[1])

                elif line == b"\n" or len(line) < 3:
                    arr.append('BREAK')
                    if count % 1000 == 0:
                        print(count)
                        # print('here')
                        create_dict(arr)
            else:
                break

    return arr


if __name__ == '__main__':
    # # arr = amazon_parser()
    #
    # # Transform crawled data into a normal format
    # results = ujson.load(open('results2.json'))
    #
    # lookup_dictionary = {}
    # for l in results:
    #     lookup_dictionary[l['event_url'].split('/')[-1]] = l['event_title'][0].split(': ')[2]
    #
    # with open('lookup_dictionary2.json', 'w') as w:
    #     ujson.dump(lookup_dictionary, w)
    #
    # print('start with amazon')
    # # transform amazon keys
    # amazon = ujson.load(open('amazon2.json'))
    # print(len(amazon.keys()))
    #
    # nice_amazon = {}
    #
    # for k in amazon:
    #     if k in lookup_dictionary:
    #         nice_amazon[lookup_dictionary[k]] = amazon[k]
    #     else:
    #         print(k)
    #
    # with open('nice_amazon2.json', 'w') as w:
    #     ujson.dump(nice_amazon, w)
    #
    # nice_amazon2 = ujson.load(open('./intent/nice_amazon2.json'))
    # print(len(nice_amazon2.keys()))
    #
    # # To lower case and clean movie names from () and []
    # nice_amazon2_lower = {}
    # for k in nice_amazon2:
    #     # print(k, movie_cleaner(k).lower())
    #     nice_amazon2_lower[movie_cleaner(k).lower()] = nice_amazon2[k]
    #
    # with open('nice_amazon2_lower.json', 'w') as w:
    #     ujson.dump(nice_amazon2_lower, w)
    #
    # nice_amazon2_lower = ujson.load(open('nice_amazon2_lower.json'))
    # for k in nice_amazon2_lower:
    #     print(k)

    movie_names = open('./intent/movie_names.txt', 'r')
    with open('movie_names_lower.txt', 'w') as w:
        for line in movie_names:
            w.write(movie_cleaner(line).lower())





