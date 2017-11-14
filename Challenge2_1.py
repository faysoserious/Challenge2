# -*- coding: utf-8 -*-
#import nltk
#nltk.download()
import itertools
import sqlite3
import re
from operator import itemgetter
import time
#from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
# function copied form https://gist.github.com/utdiscant/7e03cab4b6763be1fdda0e8815aed6ba
#
def utdiscant_words(string):
    symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

    s=string    
    s = s.lower()
    for sym in symbols:
    	s = s.replace(sym, " ")
    
    words = set()
    for w in s.split(" "):
    	if len(w.replace(" ","")) > 0:
    		words.add(w)
    
    return words   

#def get_unique_words(string):
#     wordnet_lemmatizer=WordNetLemmatizer()

#     symbols = ['\n','/r/']
#     comment_text = BeautifulSoup(string,"lxml").get_text()
#    yield [unique_word.union(set(letters_only.lower().split()))for letters_only in get_clean_words(subnames)]
#     for sym in symbols:
#         letters_only = comment_text.replace(sym," ")
#     letters_only= letters_only.replace("'","")
#     letters_only= letters_only.replace("/r/","")
#     letters_only = re.sub("[^a-zA-Z]"," ", comment_text)
     
#     meanings=[wordnet_lemmatizer.lemmatize(word) for word in letters_only.lower().split()]
#     return set(meanings)
    

    
with sqlite3.connect('reddit.db') as conn:
    start = time.clock()
    #Solve the Error "'gbk' codec can't encode character '\xc2' in position 147: illegal multibyte sequence"
    conn.text_factory = lambda x:str(x,'latin1')
#    conn.text_factory = bytes
    size_dict = dict()
    for i in range(10):
        size_dict.update({i+1:0})
    turns=0
    
        #create a Cursor object and call its execute() method to perform SQL commands
    c = conn.cursor()
    
#        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
#        table_names = c.fetchall()
#        c.execute("""SELECT * FROM comments""")
#        comments_names = [d[0] for d in c.description]
    #    c.execute("""SELECT * FROM authors""")
    #    authors_names = [d[0] for d in c.description]
    #    c.execute("""SELECT * FROM subreddits""")
    #    subreddits_names = [d[0] for d in c.description]    
#    c.execute("""SELECT name From Subreddits Order by name""")
#    names = c.fetchall()
    #    for subreddit_name in names:
        
#        names=c.fetchall()
    c.execute("""SELECT name From subreddits Order by name""")
    subreddit_name=c.fetchall()
    
#    for subreddit_name in [" ".join(name) for name in c.fetchall()]:
        
    #        start = time.clock()
    for name in subreddit_name:
        turns=turns+1

#        vectorizer= CountVectorizer()
        print('[{}]{}'.format(turns,name[0]))
#        subname= (subreddit_name,)
        c.execute("""SELECT comments.body
                                      FROM subreddits 
                                      join comments on subreddits.id = comments.subreddit_id
                                      WHERE subreddits.name=?
                                      """, name)
        comments= [" ".join(row) for row in c.fetchall()]
        string= " ".join(comments)
        unique_length = len(utdiscant_words(string))
        
#        for comment in [" ".join(row) for row in c.fetchall()]:
#        X = vectorizer.fit_transform(comments)
#            temp.union(word_set)

#            temp = temp.union(get_unique_words(comment))
    #        print('get the size of the subreddit')

#            temp= temp.union(unique)
#            unique_length = len(temp)
    #        print('create a dictionary store the size of each subreddit')
        size_dict.update({name[0]:unique_length})
        size_sorted = sorted(size_dict.items(),key = itemgetter(1), reverse = True)[:10]
        size_dict = dict(size_sorted)     
        
        elapsed =  (time.clock()-start)
        print("Time used: ",elapsed)

        
        
    result= sorted(size_dict.items(),key = itemgetter(1), reverse = True)[:10]

           
    #    print('find the first 10')
    with open('challenge2_1.txt', 'wt') as f:
        for key,value in result:
            print("subreddit:'{}'\n total number of distinct words:{}".format(key,size_dict[key]),file=f)
            print('\n')
    
