import nltk
import requests
from bs4 import BeautifulSoup

myword=""
corpus=""

# my word will be randomly selected later...
"""
(not implemented)
think_subject function will be get the random quiz word
"""
def think_animal():
    global myword
    myword="jaguar"
def think_greats():
    global myword
    myword="Einstein"
def think_hi():
    global myword
    myword="hi"

"""
subject_corpus function gets the imformation of quiz word from website.
The website will be different to have appropriate informations.
ex) I  select the national geographic site to get the features of specific animals.
"""
def animal_corpus(word):
    corpus=""
    web=requests.get('https://www.nationalgeographic.com/animals/mammals/'+word[0]+'/'+word+'/')
    soup=BeautifulSoup(web.content, 'html.parser')
    feature_list= soup.findAll('div',class_='smartbody')
    for sent in feature_list:
        untag=sent.get_text()
        corpus += untag + " "
    return corpus

"""
(not completed)
Select the subject with user interation &
select quiz word + get information from web (make corpus to answer the user questions)
"""
def choose_subect():    
    while (1):
        print("If you want to exit, give me the number 0")
        print("Choose the subject.")
        sub=input("1. animals "+"2.greats "+"3. hi "+"\n")
        if(sub=='0'):
            break
        if(sub=='1'):
            global corpus
            think_animal()
            corpus=animal_corpus(myword)
        elif(sub=='2'):
            think_greats()
            #corpus=greates_corpus(myword)
            break
        elif(sub=="3"):
            think_hi()
            #corpus=
            break
        else:
            print("There is no option about that. Choose number.\n")

def get_questions():

#(not completed)
#main function part
            
print("Hello, this is 20 questions program.\n"+"I will think the word about subjects  you chose.\n")
choose_subject()
#get_questions (get user question + check the answer)
#answer_questions (with some tricks)
#
