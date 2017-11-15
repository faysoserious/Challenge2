# -*- coding: utf-8 -*-


import itertools
import sqlite3
import re
from operator import itemgetter
import time

# Create your engine.
#engine = create_engine('sqlite:///reddit.db')
#with engine.connect() as conn, conn.begin():
#    table_comments = pd.read_sql_query("SELECT * FROM comments WHERE subreddit_id = '%s'"%subid, engine)

#    subreddit_ids = pd.read_sql_query("SELECT subreddits.id FROM subreddits", engine)
#    for subid in subreddit_ids['id']:
#    	  df = pd.read_sql_query("SELECT author_id FROM comments WHERE subreddit_id = '%s'"%subid, engine)

#Define the function to compare the numbers of common authors of a pair
def find_most_common(map_key):
    each_key=map_key
    temp1= each_key[0]
    temp2= each_key[1]
    aurthor_set1=sub_author_dict[temp1]
    author_common=len(aurthor_set1.union(sub_author_dict[temp2]))
    new_key= temp1+ " + " +temp2
    return {new_key:author_common}


    
with sqlite3.connect('reddit.db') as conn:
    size_dict = dict()
    for i in range(10):
        size_dict.update({i+1:0})
    start = time.clock()
    #Solve the Error "'gbk' codec can't encode character '\xc2' in position 147: illegal multibyte sequence"
    conn.text_factory = lambda x:str(x,'latin1')
    sub_author_dict = {'0':0}
#    size_dict.update({0:})
#    for i in range(10):
#        size_dict.update({i+1:0})
    turns=0
    #create a Cursor object and call its execute() method to perform SQL commands
    c = conn.cursor()
    c.execute("""SELECT id From subreddits Order by name""")
    id_table_subreddits=[" ".join(row) for row in c.fetchall()]


    for subrebbitid in id_table_subreddits:
        turns=turns+1

#        vectorizer= CountVectorizer()
        print('[{}]{}'.format(turns,subrebbitid))
        
#        subname= (subreddit_name,)
        c.execute("""SELECT comments.author_id
                                      FROM subreddits 
                                      join comments on subreddits.id = comments.subreddit_id
                                      WHERE subreddits.id=?
                                      """, (subrebbitid,))
        authorids= [" ".join(row) for row in c.fetchall()]
        
        sub_author_dict.update({subrebbitid:set(authorids)})
        
        elapsed =  (time.clock()-start)
        print("Time used: ",elapsed)
        
# As we have already get the dictionary with key=subreddit_id and value = set(list of author_id)
# To find the pairs of subreddit with most common authors 
# we need to compare each key=subreddit with all the rest subreddits
# eg: suppose [key = a, key = b, key=c] need to compare pairs (a,b) (a,c) (b,a)(b,c)(c,a)(c,b)
# also same result but with smaller number of pairs to only compare pairs(a,b)(a,c)(b,c)
# Use itertools.permutations() OR itertools.combination() to generate the compare list
# Apply all these list with map() to get the number of same authors

#    for mostcommon in map(find_most_common,itertools.permutations(id_table_subreddits,2)):
    for mostcommon in map(find_most_common,itertools.combinations(id_table_subreddits,2)):
       
        print(mostcommon)
        size_dict.update(mostcommon)
        size_sorted = sorted(size_dict.items(),key = itemgetter(1), reverse = True)[:10]
        size_dict = dict(size_sorted)   
         
        
        
    result= sorted(size_dict.items(),key = itemgetter(1), reverse = True)[:10]
    elapsed =  (time.clock()-start)
    print("Time used: ",elapsed)
           
    #    print('find the first 10')
    with open('challenge2_2.txt', 'wt') as f:
        for key,value in result:
            print("subreddit pairs:'{}'\n total number of common authors:{}".format(key,size_dict[key]),file=f)
            print('\n')
