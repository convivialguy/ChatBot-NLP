#
# """
# import re
# import random
# import numpy as np
# pairs = [
#     ["Core Values",
#          ["our core values are Client impact, Leadership, Openness, Creativity, People growth, Relationships . For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values" ,
#           "Core values help us to align culturally, This helps us to perform and collaborate better, Our people can form efficient, passionate, and productive teams because they share a set of values that are core to their individual and collective working identities "\
#            ",Core values help us to attract, retain and grow the best people. Core values help prospective colleagues understand what we’re about and what is expected of them from the outset. People who share our core values know that this will be a great place for them to grow over time "\
#            ",Core values differentiate us for our clients. Our values serve as a promise to our clients that we are committed to focusing our energies towards their best interests, Our clients consistently report that our commitment and passion surpasses their expectations. When we live our values and are aligned culturally, we amaze our clients.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
#           ]
#     ],
#     [
#         "Client Impact",
#         ["Our clients engage us to bring the best ideas and deliver, To figure out what their business really needs, and plan to deliver it on time, Get to know the client’s business—and their competition’s—better than they know it . For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values",
#          "Engage them in conversations about growing the bottom line, Let your passion show. Focus on success for your direct client and the company as a whole "\
#          "Try a new view • Keep an eye on the big picture • Manage—then exceed—expectations.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
#          ]
#     ],
#     [
#         "what is your name ?",
#         ["My name is Chatty and I'm a chatbot ?", ]
#     ],
#     [
#         "Creativity",
#         ["Creativity is the foundation of good ideas and good execution, There’s never a set path to a great solution —you have to take a new perspective, find a new angle, make something up to make it happen, Sometimes you have to take risks, Be curious and seek inspiration from unexpected places. Always have your eyes open to new ideas.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values",
#         "Challenge assumptions and consider new possibilities, Cultivate collaboration,Seek creative impact. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values" ]
#     ],
#     [
#         "Leadership",
#         ["Leadership isn’t a title, it’s a mentality, It’s about having a point of view, sharing your experience and energizing our people and our clients around a shared vision, sometimes it’s about making tough decisions—all in the name of reaching a common goal,Model the way Learn to coach Confront missed expectations.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
#         ]
#     ],
#     [
#         "Openness",
#         ["Honest communication is the cornerstone of any good relationship, It’s also a form of respect, And when you’re not listening or sharing, you’re not learning or teaching, Be open to changing your viewpoint, but exercise your obligation to dissent when it’s the right thing to do, Enlist many heads—they’re better than one, Listen up, Always be curious,Share information and feedback.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
#         ]
#     ],
#     [
#         "People Growth",
#         ["People Growth is about more than promotions, It’s a mindset that there is room to grow and learn in every interaction, So teach those around you as both a consumer and producer of knowledge","Earn whatever you can, whenever you can, Seize the opportunities that are in front of you; create the ones that are not, Take the initiative to achieve more"\
#          "• Own your growth• Get comfortable with being uncomfortable• Look back to move forward. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
#         ]
#     ],
#     [
#         "Relationships",
#         ["Strong relationships and trusted partnerships make it exciting for us to come to work, fun for our clients to hire us and smart for people to do business with us. So put in the time to understand your coworkers and clients. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values",\
#          "Find out what’s important to them and care about it. Become a trusted advisor. Do your part to put the delight into our day. Do the right thing • Communicate• Collaborate. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"]
#     ],
#     [
#         "Hi sup greetings are you?",["Hi !", "I am good thank you"]
#     ],
# ]
# for (pattern, response) in pairs:
#     # match = pattern.match(str)
#     # match = re.search(str,pattern)
#     # did the pattern match?
#     # if match:
#     print(type(pairs))
#     if re.search(" leader ", str(pattern)):
#         print("Matching Patter Found")
#         print(str(response))
#         resp = random.choice(response)  # pick a random response
#         print(resp)
#
#
# word_index_map = {}
# word_index_map = {"Hello",0}
# word_index_map = {"are",1}
# word_index_map = {"you",2}
#
# x = np.zeros(len(word_index_map))
# for word in word_index_map:
#     i = word_index_map[word]
#     x[i] +=1
# x=x/x.sum()
# print (x)
# """
# import random
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd
# corpus = [
#  "This is values just a testing excersise","core values are leadership, growth, culture","core growth is important for me values",
#          "core client growth in your hand",]
#
# corpus.append("testing excersise hand is good growth core")
# vectorizer = TfidfVectorizer(stop_words="english")
# tfidf= vectorizer.fit_transform(corpus)
#
# # print(vectorizer.get_feature_names())
# #print(tfidf)
# #print(tfidf[-1])
#
# vals = cosine_similarity(tfidf[-1], tfidf)
# print(vals)
# print(vals.argsort())
# idx = vals.argsort()[0][-2]
# print(idx)
# flat = vals.flatten()
# flat.sort()
# print(flat)
# req_tfidf = flat[-2]
#
# if (req_tfidf == 0):
#     print("no record found")
# else:
#     print(corpus[idx])
#
# tfidf = tfidf.todense()
# df = pd.DataFrame(tfidf,
#                   columns=vectorizer.get_feature_names(),
#                   index=['0', '1', '2','3','4'])
# df.to_excel("output.xlsx")
#
#
# # import requests
# # import json
# # import random
# #
# # question=[
# #     "what's your Creativity","tell me about core values","what is there in growth","why is leadership important","tell me more about core values","why is it important to learn", "what is culture",
# # ]
# #
# # while True:
# #     question1 = random.choice(question)
# #     print(question1)
# #     r = requests.get("http://127.0.0.1:5000/Rule/" + question1)
# #     print(r.text)
#
# from spellchecker import SpellChecker
#
#
# # find those words that may be misspelled
#
# newword = []
#
# def MySpellCheker(Sent):
#     spell = SpellChecker()
#     SentSplit = Sent.split()
#     for word in SentSplit:
#         newword.append(spell.correction(word))
#     return ' ' .join(newword)
#     # print(SentSplit)
#     # misspelled = spell.unknown(SentSplit)
#     # print(misspelled)
#     # newword1=''
#     # try:
#     #     for word in misspelled:
#     #         newword.append(spell.correction(word))
#     #     newword1 = ' '.join(newword)
#     #     if not misspelled:
#     #         newword1=''
#     #         return newword1
#     #     return newword1
#     # except Exception:
#     #     traceback.print_exc()
#
#
# print(MySpellCheker("tell me more about creativvity "))
#
#
# # newwordtosend=[]
# # for word in Text1:
# #     newword=MySpellCheker(word)
# #     if newword == '':
# #         newwordtosend.append(word)
# #     else:
# #         newwordtosend.append(newword)
# # newwordtosend=' '.join(newwordtosend)
# #print (newwordtosend)
#
# """
# maintags = [
#     ["Core Values",
#         {"Leadership":"http://Viedeo.com",
#          "Growth":"what is people growth",
#          "Open":"what is Openess",
#          "Client impact":"what is client impact",
#          "Creativity":"what is creativity",
#          "Relationships":"what is relationship",
#          "People":"what is people growth"
#         }
#     ]
# ]
# duppairs=[]
# duppairs = maintags
# for (pattern, response) in duppairs:
#     for key in response:
#         print(key + "->" + response[key])
#

import random
import re
import string

def replace(t):

    inner_word = list(t.group(2))
    #print(str(inner_word) + " " + str(len(inner_word)))
    print(t.group(2))
    #3print(t.group(3))
    random.shuffle(inner_word)
    return t.group(1) + "".join(inner_word) + t.group(3)

text = "Hello, You should reach the finish line."

re.sub(r"(\w)(\w+)(\w)", replace, text)

for punct in string.punctuation:
    print (punct)
#print (re.sub(r"(\w)(\w+)(\w)", replace, text))
#print (re.sub(r"(\w)(\w+)(\w)", replace, text))