
# coding: utf-8

# In[126]:

import os, requests, json, sys
import random, string
import urllib, pickle, unicodedata, re, time
import pandas as pd
import aiml
from flask import Flask, render_template, request, jsonify

CONFIG_FILE = "config.json"

class User(object):

    with open(CONFIG_FILE) as json_data_file:
        config = json.load(json_data_file)   

    users = {}
    
    @classmethod
    def add_user_facebook(cls, userId, user):
        cls.users[userId] = user
        return  
    
    def __init__(self, userId):
        self.userId = userId
        if not User.users.get(userId):
            try:
                user = get_user_info(userId) 
                user['language'] = user['locale'].split("_")[0]
                if user['language'] != 'fr':
                    user['language'] = 'en'
                user['counter'] = 0
                self.add_user_facebook(userId, user) 
            except: # when can't get user profil
                user = {}
                user['language'] = 'en'
                user['counter'] = 0               
                self.add_user_facebook(userId, user)
        else:
            pass #user already in the list
                  


class Bot(object):
    def __init__(self, name, config, language = 'en'):
        self.name = name
        self.config = config
        self.payload = "just_invest"
        self.language = language
        self.kernel = aiml.Kernel()
        self.kernel.setBotPredicate('name', self.name)
        
        for element in self.config['param'] :
            self.kernel.setBotPredicate(element ,self.config['param'][element])        
                
        brain_name = "bot_brain_"+self.language+".brn"        
        if os.path.isfile(brain_name):
            self.kernel.bootstrap(brainFile = brain_name)
            
        else:
            #no matter which language the user use, we load english aiml files all the time    
            self.kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
            self.kernel.respond("load aiml b")                       
            self.kernel.saveBrain(brain_name)
                    
            if self.language == 'fr': #french kernel        
                rootdir1 = os.getcwd()+"/aiml_fr"           
                for root, dirnames, filenames in os.walk( rootdir1 ):
                    print root
                    for filename in filenames:
                        try:
                            self.kernel.bootstrap(learnFiles = os.path.join(root,filename))
                        except TypeError:
                            print(os.path.join(root,filename))
                self.kernel.saveBrain(brain_name)

        with open ('name_list_str', 'rb') as fp:
            self.name_list_str = pickle.load(fp)

        with open ('dict_url', 'rb') as fp:
            self.dict_url = pickle.load(fp)                 
            
    def send_message(self, recipient_id, message_text):
        log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {
            "access_token": self.config["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
        r = requests.post(self.config['graph_url']+"/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)

    def send_template_message(self, recipient_id):

        log("sending template message to {recipient}".format(recipient=recipient_id))

        params = {
            "access_token": self.config["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        if self.language == 'fr':
            data = json.dumps({
                "recipient": {
                    "id": recipient_id
                },
                "message":{
                    "attachment":{
                    "type":"template",
                    "payload":{
                    "template_type":"generic",
                    "elements": [
                    {
                    "title": "Bonjour, qu'est-ce que je peux vous aider?",
                        "buttons": [{
                          "type": "postback",
                          "title": "Plan d'investissement",
                          "payload":"roboAdvisor"
                        }],
                    },
                    {
                    "title": "Vous voulez chercher des fonds avec le code ISIN ou le nom?",
                        "buttons": [{
                          "type": "postback",
                          "title": "Chercher des fonds",
                          "payload":"fundsearch"
                        }],
                    },                    
                    {
                    "title": "BNP Paribas Investment Partners",
                    #"subtitle": "Next-generation virtual reality",
                    "item_url": "http://www.bnpparibas-ip.fr",               
                    #"image_url": "./img/bnpip.jpg",
                        "buttons": [{
                          "type": "web_url",
                          "url": "http://www.bnpparibas-ip.fr",
                          "title": "Site en FRANCAIS"
                        }, {
                          "type": "web_url",
                          "url": "http://www.bnpparibas-ip.com/en/",
                          "title": "Site en ANGLAIS",
                        }],
                    }, 
                    {
                    "title": "Investo",
                    "item_url": "http://investo.bnpparibas/",               
                    #"image_url": "https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjbsZO-tMLSAhWJuBQKHQSADPgQjRwIBw&url=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Finvesto-par-bnp-paribas%2Fid1189529445%3Fmt%3D8&psig=AFQjCNHkkFs7ZrfJGrDcKqVwNaDesChYyw&ust=1488907950510928",
                        "buttons": [{
                          "type": "web_url",
                          "url": "http://investo.bnpparibas/",
                          "title": "TELECHARGER Investo"
                        }]
                    },
                    {
                    "title": "Nous contacter",

                    # "item_url": "http://investo.bnpparibas/",               
                    #"image_url": "https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjbsZO-tMLSAhWJuBQKHQSADPgQjRwIBw&url=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Finvesto-par-bnp-paribas%2Fid1189529445%3Fmt%3D8&psig=AFQjCNHkkFs7ZrfJGrDcKqVwNaDesChYyw&ust=1488907950510928",
                        "buttons": [{
                          "type": "web_url",
                          "url": "https://mabanque.bnpparibas/fr/nous-contacter/nous-contacter",
                          "title": "Nous contacter"
                        }]
                    }
                    ]
                    }
                }
                }
            })        

        else:
            data = json.dumps({
                "recipient": {
                    "id": recipient_id
                },
                "message":{
                    "attachment":{
                    "type":"template",
                    "payload":{
                    "template_type":"generic",
                    "elements": [
                    {
                    "title": "Hello, how could I help you?",
                        "buttons": [{
                          "type": "postback",
                          "title": "Investment Planning",
                          "payload": "roboAdvisor"
                        }],
                    },                    
                    {
                    "title": "Would you like to search for a fund by the isin code or the name?",
                        "buttons": [{
                          "type": "postback",
                          "title": "Search for a fund",
                          "payload":"fundsearch"
                        }],
                    },
                    {
                    "title": "BNP Paribas Investment Partners",
                    "item_url": "http://www.bnpparibas-ip.fr",               
                        "buttons": [{
                          "type": "web_url",
                          "url": "http://www.bnpparibas-ip.fr",
                          "title": "Website in French"
                        }, {
                          "type": "web_url",
                          "url": "http://www.bnpparibas-ip.com/en/",
                          "title": "Website in English",
                        }],
                    }, 
                    {
                    "title": "Investo",
                    "item_url": "http://investo.bnpparibas/",               
                    #"image_url": "https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjbsZO-tMLSAhWJuBQKHQSADPgQjRwIBw&url=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Finvesto-par-bnp-paribas%2Fid1189529445%3Fmt%3D8&psig=AFQjCNHkkFs7ZrfJGrDcKqVwNaDesChYyw&ust=1488907950510928",
                        "buttons": [{
                          "type": "web_url",
                          "url": "http://investo.bnpparibas/",
                          "title": "Download Investo"
                        }]
                    },
                    {
                    "title": "Contact us",

                    # "item_url": "http://investo.bnpparibas/",               
                    #"image_url": "https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjbsZO-tMLSAhWJuBQKHQSADPgQjRwIBw&url=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Finvesto-par-bnp-paribas%2Fid1189529445%3Fmt%3D8&psig=AFQjCNHkkFs7ZrfJGrDcKqVwNaDesChYyw&ust=1488907950510928",
                        "buttons": [{
                          "type": "web_url",
                          "url": "https://mabanque.bnpparibas/fr/nous-contacter/nous-contacter",
                          "title": "Contact us"
                        }]
                    }
                    ]
                    }
                }
                }
            })
        r = requests.post(self.config['graph_url']+"/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)               

    def ask_invest_type(self, recipient_id):

        log("ask_invest_type to {recipient}".format(recipient=recipient_id))

        params = {
            "access_token": self.config["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message":
            {
                "attachment":
                {
                    "type":"template",
                    "payload":
                    {
                        "template_type":"generic",
                        "elements": 
                        [{
                        "title": self.config[self.language]['roboAdvisor']['ask_invest_type'],
                            "buttons": 
                            [{
                              "type": "postback",
                              "title": self.config[self.language]['roboAdvisor']['just_invest']['title'],
                              "payload": "just_invest"
                            },
                            {
                              "type": "postback",
                              "title": self.config[self.language]['roboAdvisor']['retirement']['title'],
                              "payload": "retirement"
                            },
                            {
                              "type": "postback",
                              "title": self.config[self.language]['roboAdvisor']['other_project']['title'],
                              "payload": "other_project"
                            }]
                        }]                              
                    }
                }
            }
        })
        r = requests.post(self.config['graph_url']+"/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text) 

    def send_questions(self, sender_id, invest_type, i=0):
        log("send_question_{i} to {sender_id}".format(i = i, sender_id=sender_id))

        params = {
            "access_token": self.config["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "recipient": {
                "id": sender_id
            },
            "message":{
            "text": self.config[self.language]['roboAdvisor'][invest_type]['questions'][str(i)],
            "quick_replies": self.config[self.language]['roboAdvisor'][invest_type]['answers'][str(i)]
            }                        
        })
        r = requests.post(self.config['graph_url']+"/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)        
             

    def received_postback(self, sender_id, payload):
        print payload
        self.payload = payload
        log("Received postback for {user}: {text}".format(user=sender_id, text=payload))
        if payload == "fundsearch":
            response = self.config[self.language]['fundsearch_postback']
            self.send_message(sender_id, response) 
        elif payload == "roboAdvisor":
            self.ask_invest_type(sender_id)           
        else:
            self.send_questions(sender_id, payload)
        return 
            
    def check_isin(self, message_text):
        msg_isin_list = re.findall(r'[a-zA-Z]{2}[0-9]{10}', message_text)

        url = []
        isin_list = self.dict_url.keys()

        for element in msg_isin_list:
            if element in isin_list:
                url.append(self.dict_url[message_text])
                
        if len(url) == 1:
            response = config[self.language]['isin_url_response'] + url[0]
            
        elif len(url) == 0:
            return ''

        else:
            url_list_str = ' \n '.join(url)
            response = config[self.language]['list_isin_url_response'] + url_list_str

        return response

    def check_name(self, message_text):
        keywords = re.split('[^a-zA-Z0-9]', message_text)
        for k in keywords:
            if k.lower() not in self.name_list_str.lower():
                return ''
        response = config[self.language]['name_url_response']+self.config['name_fund_search']+'-'.join(keywords)
        return response         

    def respond(self, sessionId, message_text):
        try:
            message_text = unicodedata.normalize('NFD', message_text).encode('ascii', 'ignore').lower()

        except TypeError:
            message_text = message_text.encode('ascii', 'ignore').lower()
        #print message_text
        text = self.check_isin(message_text)
        if text != '':
            bot_response = text
            return bot_response

        text = self.check_name(message_text)
        if text != '':
            bot_response = text
            return bot_response        

        else:
            bot_response = self.kernel.respond(message_text, sessionId)
             
        if bot_response == '' :
            bot_response = ':)' 

        return bot_response   
        
    def savebrain(self):
        self.kernel.saveBrain("bot_brain_"+self.language+".brn")


def init_fundsheet(fundsearch_url, fundsheet_url_base):
    log('initializing fundsheet......')
    d = json.loads(urllib.urlopen(fundsearch_url).read())
    data = pd.DataFrame(d['funds'])

    name_list = []
    for i in xrange(data.shape[0]):
        # replace other characters by space
        name = re.sub(r'[^a-zA-Z0-9\'\ ]+', ' ', data['default_share_name'][i])
        name = re.sub(r'[\ ]+', ' ', name)
        name_list.append(name) 

    #name_list  
    name_list_str = ' ,'.join(name_list)
        
    with open('name_list_str', 'wb') as fp:
        pickle.dump(name_list_str, fp)

    #find destinated isin code
    codes_list = data[['codes']].T.to_dict().values()
    new_codes_list = []

    for item in codes_list:
        item = item['codes']
        new_codes_list.append(item)

    #new_codes_list[1].keys()
    codes_df = pd.DataFrame(new_codes_list)

    df_merged = pd.merge(data, codes_df, left_index = True, right_index = True)

    #compose url
    url_list = []

    for i in xrange(df_merged.shape[0]):
        cl = unicodedata.normalize('NFD', data['sub_asset_class'][i]).encode('ascii', 'ignore').lower() #remove french accent
        cl = re.sub('[^a-zA-Z0-9]','-', cl) #convert space into -
        cl = re.sub('[-]+','-', cl) #eliminate multiple -

        name = df_merged['default_share_name'][i].replace("'","").lower()
        name = re.sub('[^a-zA-Z0-9]','-', name) #convert space into -
        name = re.sub('[-]+','-', name) #eliminate multiple -

        isin = df_merged['isin'][i].lower()    

        url = fundsheet_url_base + cl + '/' + name + isin
        url_list.append(url)

    df_merged['url'] = url_list
    
    #construct dictionnary of url
    dict_url = {}
    for i in xrange(df_merged.shape[0]):
        for element in df_merged['isin_codes'][i]:#re.sub('[^a-zA-Z0-9]', ' ', df_merged['isin_codes'][i].encode('UTF8')).split( ): 
            dict_url[element.lower()] = df_merged['url'][i]      

    with open('dict_url', 'wb') as fp:
        pickle.dump(dict_url, fp)            
    
    filename = 'funds'+'-'+time.strftime("%Y-%m-%d")+'.json'
    #df_merged.to_csv(filename, encoding = 'utf8', sep = ';')
    
    with open(filename, 'w') as outfile:
        json.dump(df_merged.reset_index().to_json(orient='records'), outfile)

def get_user_info(userId):

    global config
    """Getting information about the user
    https://developers.facebook.com/docs/messenger-platform/user-profile
    Input:
      recipient_id: recipient id to send to
    Output:
      Response from API as <dict>
    """
    params = {
        "access_token": config["PAGE_ACCESS_TOKEN"]
    }
    request_endpoint = '{0}/{1}'.format(config['graph_url'], userId)
    response = requests.get(request_endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    log("response status is {code}: {text}".format(code=response.status_code, text=response.text))
    return  

   
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush() 


app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "Mina":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "hello world", 200

@app.route('/', methods=['POST'])
def webhook():    
    # endpoint for processing incoming messaging events
    global bot_en
    global bot_fr
    treat_flag = {}

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            if entry['id'] not in treat_flag:
                treat_flag[entry['id']] = False
            if treat_flag[entry['id']] == False:
                treat_flag[entry['id']] = True

                for messaging_event in entry["messaging"]:
                    userId = messaging_event["sender"]["id"] 
                    usr = User(userId)   

                    if User.users[userId]['language'] == 'fr':
                        bot = bot_fr
                    else:
                        bot = bot_en
                    
                    if messaging_event.get("message"):    # someone sent us a message                      
                        if User.users[userId]['counter']==0:
                            print User.users[userId]
                            try:
                                bot.kernel.setPredicate("name", User.users[userId]['first_name'], userId)
                                bot.kernel.setPredicate("gender", User.users[userId]['gender'], userId)
                            except:
                                pass
                            bot.savebrain()
                            bot.send_template_message(userId) # send the new user our introduction page
                        try:
                            message_text = messaging_event["message"]["text"]  # the message's text
                        except KeyError:
                            message_text = "smile"          
                        if messaging_event["message"].get("quick_reply"):
                            question_type = messaging_event["message"]["quick_reply"]["payload"] 
                            print bot.payload    
                            print question_type
                            if question_type == "invest_amount":                               
                                bot.send_questions(userId, bot.payload, 1)
                            elif question_type == "horizon":                               
                                bot.send_questions(userId, bot.payload, 2)
                            elif question_type == "risks":                               
                                bot.send_questions(userId, bot.payload, 3)
                            elif question_type == "investment_options":  
                                pass     # rendre result page                        
                                #bot.send_questions(userId, bot.payload, 4)                                                                                                
                        else:             
                            bot.send_message(userId, bot.respond(userId, message_text))
                        
                    if messaging_event.get("postback"):  
                        bot.received_postback(userId, messaging_event["postback"]["payload"])
                        
                    if messaging_event.get("delivery"): 
                        pass
                    
                    if messaging_event.get("optin"): 
                        pass
                    
                    User.users[userId]['counter'] += 1

    return "ok", 200


with open(CONFIG_FILE) as json_data_file:
    config = json.load(json_data_file)   
print  
# try:
#     with open(configfile) as json_data_file:
#         config = json.load(json_data_file)
#         print config
# except:
#     print("cannot load configuration file.")    

filename = 'funds'+'-'+time.strftime("%Y-%m-%d")+'.csv'

if not os.path.isfile(filename):
    init_fundsheet(config['fundsearch_url'], config['fundsheet_url_base'])    #to rename url...
log("bot_en")
bot_en = Bot("Pikachu", config, language = 'en')
bot_fr = Bot("Pikachu", config, language = 'fr')


if __name__ == '__main__':
    #configure...
    log("main function.............")
    app.run(debug=True)




