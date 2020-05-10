import nltk
import requests
from bs4 import BeautifulSoup
import browncorpus as br
import random

book_list = nltk.corpus.brown.categories()
wrong_list=["Nope.","Wrong answer.","Try again...", "Your answer is maybe not correct"]
hint_list=[]
myword=""
corpus=""

# my word will be randomly selected later...
"""
(not implemented)
think_subject function will be get the random quiz word
"""
def think_animal():
    global myword
    animals_type=['mammals','amphibians','birds'] #'fish' 'invertebrates' 'reptiles' will be added
    animals_dict={"mammals":['african elemphant','horse','red fox','cheetah','giraffe','koala','jaguar','arctic fox','bengal tiger','giant panda', 'polar bear'],
                  "amphibians":['green eyed tree frog','cane toad','spotted salamander'],
                  "fish":[],
                  "birds": ['bald eagle','house sparrow','america crow','rock pigeon'],
                  "invertebrates":[],
                  "reptiles":[]}
    rand_type=animals_type[random.randint(0,len(animals_type)-1)]
    rand_list=animals_dict[rand_type]
    myword=rand_list[random.randint(0,len(rand_list)-1)]
    return (rand_type, myword)
def think_greats():
    global myword
    myword="Einstein"
def think_book():
    global myword
    myword=book_list[random.randint(0,len(book_list)-1)]
    return myword

"""
subject_corpus function gets the imformation of quiz word from website.
The website will be different to have appropriate informations.
ex) I  select the national geographic site to get the features of specific animals.
"""
def animal_corpus(animal_type, word):
    corpus=""
    web=requests.get('https://www.nationalgeographic.com/animals/'+animal_type+'/'+word[0]+'/'+"-".join(word.split())+'/')
    soup=BeautifulSoup(web.content, 'html.parser')
    feature_list= soup.findAll('div',class_='smartbody')
    for sent in feature_list:
        untag=sent.get_text()
        corpus += untag + " "
        corpus = corpus.replace('\n','')
        corpus = corpus.replace("'","")
    return corpus

"""
(not completed)
Select the subject with user interation &
select quiz word + get information from web (make corpus to answer the user questions)
"""
def choose_subject():    
    while (1):
        print("If you want to exit, give me the number 0")
        print("Choose the subject.")
        sub=input("1. animals "+"2.greats "+"3. book categories "+"\n")
        if(sub=='0'):
            return 0
        if(sub=='1'):
            global corpus
            (animal_type, animal)=think_animal()
            corpus=animal_corpus(animal_type,animal)
            return 1
        elif(sub=='2'):
            think_greats()
            #corpus=greates_corpus(myword)
            return 2
        elif(sub=="3"):
            global hintlist
            print("I'm working...")
            rand_category=think_book()
            category_word_list=br.Brown_hintlist(book_list)
            for (category, word_list) in category_word_list:
                if (rand_category==category):
                    hintlist=word_list
                    break
            return 3
        else:
            print("There is no option about that. Choose number.\n")

def get_questions():
    for i in range(20):
        print("This is "+str(i+1)+"th question")
        quest=input("What's your question? Please use question mark \'?\' in the end. \n You can give me the answer also.\n")
        if (quest==myword):
            print("You correct! Congratulation. The answer was "+myword+"!")
            return
        if (quest[-1]!='?'):
            print(wrong_list[random.randint(0,len(wrong_list)-1)])
            continue
        print("I'm thinking about your question...")
        sentence=""
        #sentence=dealing_question(quest)
        print("My answer: "+sentence+"\n")
    print("20 questions over... I win zz. The answer was "+myword+"!")

def give_hint():
    print("I will give hints to you rather than I get the questions from you.")
    for i in range(20):
        print("This is "+str(i+1)+"th hints")
        quest=input("Give me the answer or give me \'?\' to get hints.\n")
        if (quest==myword):
            print("You correct! Congratulation.")
            return
        elif (quest[-1]=='?'):
            global hintlist
            print("My hint word is : "+ hintlist[0])
            hintlist= hintlist[1:]
            continue
        print(wrong_list[random.randint(0,len(wrong_list)-1)])
    print("20 questions over... I win zz. The answer was "+myword+"!")
    
def dealing_question(quest):
    pass

#(not completed)
#main function part            
print("Hello, this is 20 questions program.\n"+"I will think the word about subject  you chose.\n")
exit_code=choose_subject()
if (exit_code == 3):
    give_hint()
elif (exit_code!=0):
    get_questions()
    #dealing_question
print("Good bye.\n")


