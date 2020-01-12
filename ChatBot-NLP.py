
from flask import Flask, jsonify,session , request,redirect, url_for, render_template,Response,json

from flask_restful import Resource, Api
import random
import string  # to process standard python strings
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.chat.util import Chat, reflections
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from spellchecker import SpellChecker


debug = False
app = Flask(__name__)
app.secret_key = "debashishdey"
api = Api(app)



reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}
maintags = [
    ["Core Values",
        {"Leadership":"http://Viedeo.com",
         "Growth":"what is people growth",
         "Open":"what is Openess",
         "Client impact":"what is client impact",
         "Creativity":"what is creativity",
         "Relationships":"what is relationship",
         "People":"what is people growth",
         "clients":"what do clients want"
        }
    ],
    ["Impact",
         {"competition":"what do Client Impact",
         }
    ]
]
pairs = [
    ["Core Values",
         ["our core values are Client impact, Leadership, Openness, Creativity, People growth, Relationships . For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values" ,
          "Core values help us to align culturally, This helps us to perform and collaborate better, Our people can form efficient, passionate, and productive teams because they share a set of values that are core to their individual and collective working identities "\
           ",Core values help us to attract, retain and grow the best people. Core values help prospective colleagues understand what we’re about and what is expected of them from the outset. People who share our core values know that this will be a great place for them to grow over time "\
           ",Core values differentiate us for our clients. Our values serve as a promise to our clients that we are committed to focusing our energies towards their best interests, Our clients consistently report that our commitment and passion surpasses their expectations. When we live our values and are aligned culturally, we amaze our clients.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
          ]
    ],
    [
        "Client Impact",
        ["Our clients engage us to bring the best ideas and deliver, To figure out what their business really needs, and plan to deliver it on time, Get to know the client’s business—and their competition’s—better than they know it . For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values",
         "Engage them in conversations about growing the bottom line, Let your passion show. Focus on success for your direct client and the company as a whole "\
         "Try a new view • Keep an eye on the big picture • Manage—then exceed—expectations.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
         ]
    ],
    [
        "what is your name ?",
        ["My name is Chatty and I'm a chatbot ?", ]
    ],
    [
        "Creativity",
        ["Creativity is the foundation of good ideas and good execution, There’s never a set path to a great solution —you have to take a new perspective, find a new angle, make something up to make it happen, Sometimes you have to take risks, Be curious and seek inspiration from unexpected places. Always have your eyes open to new ideas.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values",
        "Challenge assumptions and consider new possibilities, Cultivate collaboration,Seek creative impact. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values" ]
    ],
    [
        "Leadership",
        ["Leadership isn’t a title, it’s a mentality, It’s about having a point of view, sharing your experience and energizing our people and our clients around a shared vision, sometimes it’s about making tough decisions—all in the name of reaching a common goal,Model the way Learn to coach Confront missed expectations.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
        ]
    ],
    [
        "Openness",
        ["Honest communication is the cornerstone of any good relationship, It’s also a form of respect, And when you’re not listening or sharing, you’re not learning or teaching, Be open to changing your viewpoint, but exercise your obligation to dissent when it’s the right thing to do, Enlist many heads—they’re better than one, Listen up, Always be curious,Share information and feedback.. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
        ]
    ],
    [
        "People Growth",
        ["People Growth is about more than promotions, It’s a mindset that there is room to grow and learn in every interaction, So teach those around you as both a consumer and producer of knowledge","Earn whatever you can, whenever you can, Seize the opportunities that are in front of you; create the ones that are not, Take the initiative to achieve more"\
         "• Own your growth• Get comfortable with being uncomfortable• Look back to move forward. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"
        ]
    ],
    [
        "Relationships",
        ["Strong relationships and trusted partnerships make it exciting for us to come to work, fun for our clients to hire us and smart for people to do business with us. So put in the time to understand your coworkers and clients. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values",\
         "Find out what’s important to them and care about it. Become a trusted advisor. Do your part to put the delight into our day. Do the right thing • Communicate• Collaborate. For More information go to https://tools.publicis.sapient.com/confluence/display/MEARO/Core+Values"]
    ],
    [
        "Hi sup greetings are you ?",["Hi !", "I am good thank you"]
    ],
    [
      "bye good day",["Bye!"]
    ],
]

warnings.filterwarnings('ignore')

nltk.download('popular', quiet=True)  # for downloading packages
nltk.download('all', quiet=True)  # for downloading packages

equestion=''
answer=''

# uncomment the following only the first time
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only
stopwords_str = stopwords.words('english')

# Reading in the corpus
with open(r'C:\Users\debdey\PycharmProjects\NLP-ChatBot\chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()


class Chat(object):
    def __init__(self, pairs, reflections={}):
        """

        """

        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find('%')
        return response

    def RuleRespond(self, strq,flag=1):
        duppairs=[]

        try:
            if flag==2:
                duppairs = maintags
            if flag==1:
                duppairs=pairs
            # check each pattern
            for (pattern, response) in duppairs:
                #match = pattern.match(str)
                #match = re.search(str,pattern)
                # did the pattern match?
                #if match:
                cleanstr1 = []
                resp = "Sorry I did not undertsand"
                cleanstr = [c for c in strq if c not in string.punctuation]
                cleanstr = ''.join(cleanstr)

                cleanstr = cleanstr.lower().split()
                #print(cleanstr)
                cleanstr1 = [word for word in cleanstr if word not in stopwords_str]
                # for word in cleanstr:
                #     if word not in stopwords_str:
                #         print (word)
                #         cleanstr1.append(word)

                cleanstr = ' '.join(cleanstr1)
                #print('after stopwords ' + cleanstr)

                cleanstr = cleanstr.split()
                #print("before loop")
                for term in cleanstr:
                    print("match->" + term + '->' + str(pattern) + '->' + str(response))
                    if re.search(' ' + str(term) + ' ' , ' ' + str(pattern) + ' ' ,re.IGNORECASE):
                        print("In IF SEARCH->" + str(term) + '->' + str(pattern) + '->' + str(response))
                        if debug:
                            print("lenght of list is " + str(len(pairs)))
                            print("Trying to Match->" + str(strq) + ' ' + str(pattern))
                            print(str(re.search(' ' + str(strq) + ' ' , ' ' + str(pattern) + ' ' ,re.IGNORECASE)))
                    #if re.search(' ' + str(term) + ' ' , ' ' + str(pattern) + ' ' ,re.IGNORECASE):
                        if debug:
                            print("Matching Patter Found")
                        resp = response

                        if flag == 1:
                            resp = random.choice(response)  # pick a random response
                            #resp = self._wildcards(resp, match)  # process wildcards
                            # fix munged punctuation at the end
                            if resp[-2:] == '?.':
                                resp = resp[:-2] + '.'
                            if resp[-2:] == '??':
                                resp = resp[:-2] + '?'
                        return resp
                    #else:
                        #resp = "Sorry I did not undertsand"
            return resp
        except:
            #print("In Rule Respond exception block")
            return 'I do not understand, seems like I need more training'

# TOkenisation
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    if debug:
        print(text)
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey", "how are you","how r u")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


spell = SpellChecker()
def MySpellCheker(Sent):
    newword = []
    SentSplit = Sent.split()
    for word in SentSplit:
        newword.append(spell.correction(word))
    return ' ' .join(newword)

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def MLresponse(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        if debug:
            print("In the Resoponse block ->" + robo_response)
            print("In the sent token block ->" + sent_tokens[idx])
        robo_response = robo_response + sent_tokens[idx]
        global answer
        answer = robo_response
        return robo_response

# ###########Using ChatterBot API#######################################################################################
my_bot = ChatBot(name='CoreValueBot', read_only=False,logic_adapters=['chatterbot.logic.MathematicalEvaluation',{'import_path':'chatterbot.logic.BestMatch','default_response': 'I am sorry, but I do not understand.','maximum_similarity_threshold': 0.90},'chatterbot.logic.TimeLogicAdapter'])

trainer = ListTrainer(my_bot)
trainer.train([
    "How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You are welcome.",
])
corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english','chatterbot.corpus.english.conversations','chatterbot.corpus.english.greetings')#,'C:/Users/debdey/PycharmProjects/NLP-ChatBot/chatbot.txt')


chat = Chat(pairs, reflections)
globalanswer = ''
questionanswer={}
response_dict={}
###################################################################################################################

@app.route('/',methods=['GET','POST'])
def index():
    if (request.method == 'POST'):
        some_json = request.get_json()
        #return jsonify({"data:":'use rule or request'}),201
        return render_template("home.html",setvalue='')
        #return jsonify({"data:":some_json}),201
    else:
        #return jsonify({"data:":'use rule or request'})
        return render_template("home.html")


@app.route('/Rule/<string:question>',methods=['GET'])
def getChatAnswerRule(question):

    while question[-1] in "!.":
        question = question[:-1]
    if debug:
        print("Earlier ->" + question)
    newquestion = MySpellCheker(question)
    if debug:
        print("After ->" + newquestion)
    globalanswer=str(chat.RuleRespond(newquestion))
    return jsonify({'result': 'ROBO: ' + str(chat.RuleRespond(newquestion))})

@app.route('/Demo',methods=['POST', 'GET'])
def Demo():

    try:
        if request.method == 'POST':
            question = request.form['messageText']
            question=question.strip()
            if len(question) == 0:
                return ''
            global equestion
            question = MySpellCheker(question)
            if question == equestion:  # in same question
                globalanswer= jsonify({'result': 'ROBO: ' + answer})
            else:
                equestion = question
            if (question != 'bye'):
                if (question == 'thanks' or question == 'thank you'):
                    flag = False
                    globalanswer = 'You are welcome..'
                    questionanswer[question]=globalanswer
                    return render_template('home.html', result=globalanswer)
                else:
                    if (greeting(question) != None):
                        tosend = greeting(question)
                        if debug:
                            print(tosend)
                        globalanswer = tosend
                        questionanswer[question] = globalanswer
                        return render_template('home.html', result=globalanswer)
                    else:
                        tosend = MLresponse(question)
                        # tosend1 = my_bot.get_response(question) ot working check more taking more time

                        sent_tokens.remove(question)
                        print('Print the globalanswer->' + str(tosend))
                        questionanswer[question] = tosend
                        return render_template('home.html', result=tosend)
            else:
                questionanswer[question] = "Bye! take care.."
                return render_template('home.html', result="Bye! take care..")
    except:
        globalanswer= ""
        jsonify({'result': 'ROBO: I do not understand, seems like I need more training'})

@app.route('/request/<string:question>',methods=['POST', 'GET'])
def getChatAnswer(question):
    try:
        global equestion
        question = MySpellCheker(question)
        if question == equestion: # in same question
            return jsonify({'result': 'ROBO: ' + answer})
        else:
            equestion = question
        if (question != 'bye'):
            if (question == 'thanks' or question == 'thank you'):
                flag = False
                globalanswer='You are welcome..'
                return jsonify({'result':'ROBO: You are welcome..'})
            else:
                if (greeting(question) != None):
                    tosend = greeting(question)
                    if debug:
                        print(tosend)
                    globalanswer = tosend
                    return jsonify({'result':'ROBO: ' + tosend})
                else:
                    tosend = MLresponse(question)
                    #tosend1 = my_bot.get_response(question) ot working check more taking more time
                    sent_tokens.remove(question)
                    globalanswer = tosend
                    response_dict["response"] = tosend
                    response_dict["tags"] = chat.RuleRespond(question,2)
                    print(json.dumps(response_dict))
                    return Response(json.dumps(response_dict), status = 200, mimetype = 'application/json')
                    #return jsonify({'result':'ROBO: ' + tosend}) # + ' ' + str(tosend1)})
        else:
            flag = False
            return jsonify({'result': 'ROBO: Bye! take care..'})
    except:
        return jsonify({'result': 'ROBO: I do not understand, seems like I need more training'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)