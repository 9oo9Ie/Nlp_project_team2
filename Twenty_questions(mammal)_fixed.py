import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
import random
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

book_list = nltk.corpus.brown.categories()
wrong_list=["Nope.","Wrong answer.","Try again...", "Your answer is maybe not correct"]
hint_list=[]
myword=""
corpus=""
random_corpus = []
num = 0
animals_type=['mammals','amphibians','birds', 'fish', 'invertebrates', 'reptiles']
animals_dict={"mammals":['african elemphant','gray wolf','horse','red fox','cheetah','giraffe','koala','jaguar','arctic fox','bengal tiger','giant panda', 'polar bear','red panda','African lion'],
                  "amphibians":['cane toad','spotted salamander'],
                  "fish":['European eel','Largetooth sawfish','Sockeye Salmon'],
                  "birds": ['bald eagle','house sparrow','american crow','rock pigeon'],
                  "invertebrates":['Praying mantis','Dragonflies','Banana slug'],
                  "reptiles":['komodo dragon','Burmese python','King cobra','Gopher tortoise','Gharial','Nile Crocodile']}

# my word will be randomly selected later...
"""
(not implemented)
think_subject function will be get the random quiz word
"""
def rmstopwords(token):  #function which exclude stop words from token
    stop_words = set(stopwords.words('english'))
    token=[w for w in token if w not in stop_words]
    return token

def think_animal():
    global myword
    rand_type=animals_type[random.randint(0,len(animals_type)-1)]
    rand_list=animals_dict[rand_type]
    myword=rand_list[random.randint(0,len(rand_list)-1)]
    return (rand_type, myword)

"""
subject_corpus function gets the imformation of quiz word from website.
The website will be different to have appropriate informations.
ex) I  select the national geographic site to get the features of specific animals.
"""
def animal_corpus(word):
    corpus=""
    web=requests.get('https://en.wikipedia.org/wiki/'+word)
    soup=BeautifulSoup(web.content, 'html.parser')
    feature_list= soup.findAll('p')
    for sent in feature_list:
        untag=sent.get_text()
        corpus += untag + " "
        corpus = corpus.replace('\n','')
        corpus = corpus.replace("'","")
    clear_corpus = ""
    get = True
    for k in corpus:
        if k =='[':
            get = False
        elif k == ']':
            get = True
        else:
            if get:
                clear_corpus += k
    return clear_corpus

def animal_random_corpus(animal_type, word):
    corpus=""
    web=requests.get('https://www.nationalgeographic.com/animals/' + animal_type + '/' + word[0] + '/' + '-'.join(word.split()) + '/')
    soup=BeautifulSoup(web.content, 'html.parser')
    feature_list= soup.findAll('div', class_ = 'animalFastFacts section')
    for sent in feature_list:
        untag=sent.get_text()
        corpus += untag + " "
        corpus = corpus.replace('\n','')
        corpus = corpus.replace("'","")
    key_corpus = ""
    inside = False
    for k in corpus:
        if k == '[':
            inside = True
        elif k == ']':
            inside = False
        else:
            if inside:
                key_corpus += k
    remember = ""
    new_corpus = []
    inside = False
    for k in key_corpus:
        if k == '"':
            if inside:
                inside = False
            else:
                inside = True
            if len(remember) != 0:
                new_corpus.append(remember)
                remember = ""
        else:
            if inside:
                remember += k
    hint_raw = []
    l = len(new_corpus)
    for i in range(l):
        if i > 3 and i%2 == 1:
            hint_raw.append(new_corpus[i])
    hint = []
    l = len(hint_raw)
    for i in range(int(l/2)):
        hint.append(hint_raw[2*i] + ' - ' + hint_raw[2*i+1])
    hint.reverse()
    return hint


"""
(not completed)
Select the subject with user interation &
select quiz word + get information from web (make corpus to answer the user questions)
"""
def choose_subject():
    while (1):
        sub=input(" 0. Exit "+"1. play the game "+"\n")
        if(sub=='0'):
            return 0
        elif(sub=='1'):
            global corpus
            global random_corpus
            (animal_type, animal)=think_animal()
            corpus=animal_corpus(animal)
            random_corpus = animal_random_corpus(animal_type, animal)
            return 1
        else:
            print("There is no option about that. Choose number.\n")

def get_questions():
    for i in range(20):
        print("\nThis is "+str(i+1)+"th turn")
        quest=input("What's your question? Please use question mark \'?\' in the end. \nThe question must start with What, When or Where. \n You can give me the answer also.\n")
        if quest == '0': return ()
        mylist = [myword.split()[-1]]
        mylist.append(myword)
        if (quest in mylist):
            print("You correct! Congratulation. The answer was "+myword+"!")
            return
        if dealing_question(quest)=="Maybe not or I don't know about that" and quest!='?':
            print("My answer: Maybe not or I don't know about that")
            print("Instead, I'll give you a basic hint")
            quest='?'
        if quest == '?':
            global num
            global random_corpus
            if num == len(random_corpus):
                print("No more basic hints. Guess a question.")
            else:
                print(random_corpus[num])
                num += 1
            continue
        if (quest[-1]!='?' or quest[:2].lower() != 'wh'):
            print(wrong_list[random.randint(0,len(wrong_list)-1)])
            continue
        print("I'm thinking about your question...")
        sentence=dealing_question(quest)
        hide_sentence=hide_critical_part(sentence)
        print("My answer: "+hide_sentence)
    print("20 questions over... I win zz. The answer was "+myword+"!")

def Find_synonym (list1):
    myset=[]
    for myword in list1:
        myword= myword.lower()
        syn=wordnet.synsets(myword)
        syn_words= sorted(l.name() for s in syn for l in s.lemmas())
        #update thier verb/noun/adjective/adverb forms
        relateform=sorted(rf.name() for s in syn for l in s.lemmas() for rf in l.derivationally_related_forms() )
        syn_words= list(set(syn_words + relateform))
        myset+= syn_words
    return myset

def dealing_question(quest):
    sentences=nltk.tokenize.sent_tokenize(corpus)
    answer_list=[]
    #analysis question
    text=nltk.tokenize.word_tokenize(quest)
    tagged=nltk.pos_tag(text)
    word_list= [word[0] for word in tagged if word[1].startswith('NN') or word[1].startswith('VB')]
    stem_list= [word for word in word_list if word.isalpha() and len(word) > 1 and word not in ['do', 'does']]
    stem_list=rmstopwords(stem_list)
    syn_list=Find_synonym(stem_list)
    if ('name' in stem_list):
        return "I'm not fool, I can't show that"
    answer_list = [sentence for sentence in sentences for stem_word in stem_list if stem_word in sentence]
    new_answer_list = []
    for sentence in answer_list:
        token_sentence = nltk.tokenize.word_tokenize(sentence)
        lemma_sentence = [lemmatizer.lemmatize(w) for w in token_sentence]
        for w in syn_list:
            if w in lemma_sentence:
                new_answer_list.append(sentence)
    if (new_answer_list==[]):
        answer_list = [sentence for sentence in sentences for syn_word in syn_list if syn_word in sentence]
        new_answer_list = []
        for sentence in answer_list:
            token_sentence = nltk.tokenize.word_tokenize(sentence)
            lemma_sentence = [lemmatizer.lemmatize(w) for w in token_sentence]
            for w in syn_list:
                if w in lemma_sentence:
                    new_answer_list.append(sentence)
    if (new_answer_list == []):
        return "Maybe not or I don't know about that"
    return ' '.join(new_answer_list)

def hide_critical_part(sentences):
    token_word=nltk.tokenize.word_tokenize(myword)
    for critical_word in token_word:
        c_critical=critical_word.capitalize()
        critical_set=[critical_word]+[critical_word+"s"]+[critical_word+"es"]+[critical_word+"ies"]+[c_critical]+[c_critical+"s"]+[c_critical+"es"]+[c_critical+"ies"]
        for c in critical_set:
            sentences=sentences.replace(c,'???')
    return sentences
    
#main function part            
print("Hello, this is 20 questions program.\n"+"I will think the word about subject you chose.\n")
exit_code=choose_subject()
if (exit_code!=0):
    get_questions()
print("Good bye.\n")
