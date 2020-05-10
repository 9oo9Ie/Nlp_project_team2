
import nltk, csv

book_list = nltk.corpus.brown.categories()

def Brown_hintlist(book_list):
    
    freq_words = list()
    sumlist = list()
    ans = list()

    for i in range(len(book_list)):
        category=book_list[i]
        book_tagged = nltk.corpus.brown.tagged_words(categories = book_list[i])

        book_word = [word for (word, tag) in book_tagged if tag in ['NN', 'NP']]
        long_word = [word for word in book_word if word.isalpha() and len(word) > 2]
        common_word = nltk.FreqDist(long_word).most_common()
        clear_word = [(word, num/float(len(common_word))) for (word, num) in common_word]
        ans.append(clear_word[:100])
        sumlist = sumlist + clear_word[:100]

    sumlist.sort(key = lambda element : element[0])
    newsum = list()
    newsum.append(sumlist[0])
    i = 0
    for k in range(1, len(sumlist)):
        (word, num) = sumlist[k]
        if(not newsum[i][0] == word):
            newsum[i] = (newsum[i][0], newsum[i][1]/len(book_list))
            i += 1
            if k < len(sumlist)-1: newsum.append(sumlist[k + 1])
        else:
            newsum[i] = (newsum[i][0], newsum[i][1] + num)

    newsum[len(newsum)-1] = (newsum[len(newsum)-1][0], newsum[len(newsum)-1][1]/len(book_list))

    newsum.sort(key = lambda element : element[1])
    newsum.reverse()
    remove = [word for (word, _) in newsum[:150]] # hyper parameter는 조절 가능
    for i in range(len(ans)):
        freq_words.append((book_list[i],[word for (word, _) in ans[i] if word not in remove]))

    freq_words.append([remove,"removing_word"])
    return freq_words
"""
    ans = list()
    raw_sent = nltk.corpus.brown.sents(categories = book_list[i])
    for sent in raw_sent:
        long_word = [word for word in sent if word.isalpha()]
        b = nltk.ngrams(long_word, 10)
        for t in b:
            ans.append(t)
    common = nltk.FreqDist(ans).most_common(50)
    clear = [word for (word, num) in common if num > 2]



f = open('data.csv', 'w', newline ='')
wr = csv.writer(f)
for i in range(len(book_list)+1):
    wr.writerow(freq_words[i])
f.close()

text = nltk.corpus.brown.tagged_words(fileids = ['ck01'])
stopwords = nltk.corpus.stopwords.words('english') # to remove stopwords of English
words = [word for (word, pos) in text if (pos == 'NP' and word.isalpha() and word.lower() not in stopwords)] # check general words
fdist = [word for word in nltk.FreqDist(words).most_common()]
"""
