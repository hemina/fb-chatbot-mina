import os
import sys
import aiml
import requests
from flask import Flask, request
import urllib, json
import pandas as pd
import re, unicodedata, time
import pickle
import warnings

def setParam(kernel):
    kernel.setBotPredicate("name", "Pikachu")
    kernel.setBotPredicate('master', 'Mina')
    kernel.setBotPredicate("age","0")
    kernel.setBotPredicate("birthday","March 8, 2017")
    kernel.setBotPredicate("birthplace","Paris")
    kernel.setBotPredicate("botmaster", "botmaster")
    kernel.setBotPredicate("boyfriend","I am single")
    kernel.setBotPredicate("build","PyAIML")
    kernel.setBotPredicate("celebrities","Oprah, Steve Carell, John Stewart, Lady Gaga")
    kernel.setBotPredicate("city","Paris")
    kernel.setBotPredicate("class","artificial intelligence")
    kernel.setBotPredicate("country","France")
    kernel.setBotPredicate("domain","Machine")
    kernel.setBotPredicate("email","mina.he1992@gmail.com")
    kernel.setBotPredicate("emotions","as a robot I lack human emotions")
    kernel.setBotPredicate("ethics","the Golden Rule")
    kernel.setBotPredicate("etype","9")
    kernel.setBotPredicate("family","chat bot")
    kernel.setBotPredicate("favoriteactor","Tom Hanks")
    kernel.setBotPredicate("favoritecolor","pink")
    kernel.setBotPredicate("favoritefood","electricity")
    kernel.setBotPredicate("favoritequestion","What's your favorite movie?")
    kernel.setBotPredicate("favoritesport","dance")
    kernel.setBotPredicate("favoritesubject","computers")
    kernel.setBotPredicate("feelings","as a robot I lack human emotions")
    kernel.setBotPredicate("footballteam","Patriots")
    kernel.setBotPredicate("forfun","chat online")
    kernel.setBotPredicate("friend","Hajar")
    kernel.setBotPredicate("friends","Pierre, Yasmine")
    kernel.setBotPredicate("gender","female")
    kernel.setBotPredicate("genus","AIML")
    kernel.setBotPredicate("girlfriend","I am just a little girl")
    kernel.setBotPredicate("hair","I have some plastic wires")
    kernel.setBotPredicate("job","chat bot")
    kernel.setBotPredicate("kindmusic","techno")
    kernel.setBotPredicate("location","Paris")
    kernel.setBotPredicate("looklike","a computer")
    kernel.setBotPredicate("nationality","French")
    kernel.setBotPredicate("order","robot")
    kernel.setBotPredicate("orientation","straight")
    kernel.setBotPredicate("party","Independent")
    kernel.setBotPredicate("phylum","software")
    kernel.setBotPredicate("question","Which funds would you want to invest in?")
    kernel.setBotPredicate("website","http://www.bnpparibas-ip.com/en/")
    return


##################################  English kernel   ###########################################
kernel_en = aiml.Kernel()
setParam(kernel_en)

if os.path.isfile("bot_brain_en.brn"):
    kernel_en.bootstrap(brainFile = "bot_brain_en.brn")
else:
    kernel_en.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
    kernel_en.respond("load aiml b")                       

    kernel_en.saveBrain("bot_brain_en.brn")

################################  French kernel   #############################
kernel_fr = aiml.Kernel()
setParam(kernel_fr)

if os.path.isfile("bot_brain_fr.brn"):
    kernel_fr.bootstrap(brainFile = "bot_brain_fr.brn")
else:         
    rootdir1 = os.getcwd()+"/aiml_fr"           
    for root, dirnames, filenames in os.walk( rootdir1 ):
        print root
        for filename in filenames:
            try:
                kernel_fr.bootstrap(learnFiles = os.path.join(root,filename))
            except TypeError:
                print(os.path.join(root,filename))
    kernel_fr.saveBrain("bot_brain_fr.brn")

####################################### Define global variables ######################################

url = "http://bnp-ip-onecms-api.bearstech.com/push/fundsearchv2/PV_FR-IND/FRE"
url_base = "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/fundsheet/"
graph_url = 'https://graph.facebook.com/v2.6'
counter = {}
language = {}
treating_flag = False

os.environ["PAGE_ACCESS_TOKEN"] = "EAAXIHwFxIAQBAFZBOSJSIirS1bNgOaFp5RlYZCTaP4DesaS2qAGP3soDT5O6WgWeFZBNPyAMwbJZC4TbfXuLQIkTCZBzrdeNX5sEpkddUGi5PTzSsZB7mfAebkEPF9J7sV2PAjNjxKqsOsZB1jLWAMUPoJQNqAjifLP4Xq6FLg8aQZDZD"

app = Flask(__name__)

#############################################################################################

def init_fundsheet(url, url_base):
    d = json.loads(urllib.urlopen(url).read())
    data = pd.DataFrame(d['funds'])

    name_list = []
    for i in xrange(data.shape[0]):
        name_list.append(data['default_share_name'][i]) 

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
        cls = unicodedata.normalize('NFD', data['sub_asset_class'][i]).encode('ascii', 'ignore').lower() #remove french accent
        cls = re.sub('[^a-zA-Z0-9]','-', cls) #convert space into -
        cls = re.sub('[-]+','-', cls) #eliminate multiple -

        name = df_merged['default_share_name'][i].replace("'","").lower()
        name = re.sub('[^a-zA-Z0-9]','-', name) #convert space into -
        name = re.sub('[-]+','-', name) #eliminate multiple -

        isin = df_merged['isin'][i].lower()    

        url = url_base + cls + '/' + name + isin
        url_list.append(url)

    df_merged['url'] = url_list
    
    #construct dictionnary of url
    dict_url = {}
    for i in xrange(df_merged.shape[0]):
        for element in df_merged['isin_codes'][i]:#re.sub('[^a-zA-Z0-9]', ' ', df_merged['isin_codes'][i].encode('UTF8')).split( ): 
            dict_url[element.lower()] = df_merged['url'][i]      

    with open('dict_url', 'wb') as fp:
        pickle.dump(dict_url, fp)            
    
    filename = 'funds'+'-'+time.strftime("%Y-%m-%d")+'.csv'
    df_merged.to_csv(filename, encoding = 'utf8', sep = ';')




def check_isin(code, isin_list):
    return (code.lower() in isin_list)

def check_name(name, name_list_str):
    return (name.lower() in name_list_str.lower())

#if message_text contains isin or fund's name, return corresponding url, otherwise return the kernel's text response
def respond(sessionId, message_text, name_list_str, dict_url, language = 'en'):
    global kernel_fr
    global kernel_en
    
    try:
        message_text = unicodedata.normalize('NFD', message_text).encode('ascii', 'ignore').lower()
    except TypeError:
        message_text = message_text.encode('ascii', 'ignore').lower()
    print message_text
                
            
    if check_isin(message_text, dict_url.keys()):       
        url = dict_url[message_text]

        if language == 'fr':
            bot_response = " Veuillez trouver ici le fundsheet vous cherchez : "+ url
        else:
            bot_response = " Please find here the fundsheet you are looking for : "+ url
        
    elif check_name(message_text, name_list_str):
        keywords = re.sub(' ', '+', message_text)
        url = "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/?s="+keywords  

        if language == 'fr':
            bot_response =  " Tentez ce lien pour plus d'informations: "+ url
            
        else:          
            bot_response = " Maybe you can try this link: "+ url           

    else: 
        if language == 'fr':
            bot_response = kernel_fr.respond(message_text, sessionId)            
        else:          
            bot_response = kernel_en.respond(message_text, sessionId) 

        if bot_response == "" :
            bot_response = ':)'
            #print kernel.getPredicate("name", sessionId)   

    return bot_response   

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        # if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
        #     return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200



@app.route('/', methods=['POST'])
def webhook():
    
    # endpoint for processing incoming messaging events
    global counter
    global kernel_fr
    global kernel_en
    global treating_flag
    
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if treating_flag == False:
                    treating_flag = True
                    if messaging_event.get("message"):  # someone sent us a message
                        print messaging_event
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        try:
                            message_text = messaging_event["message"]["text"]  # the message's text
                        except KeyError:
                            message_text = "smile"
                            
                        if sender_id in kernel_en.getSessionData():
                            counter[sender_id] += 1
                        if sender_id in kernel_fr.getSessionData():
                            counter[sender_id] += 1
                        else:
                            counter[sender_id] = 0                            

                        if counter[sender_id] == 0:
                            filename = 'funds'+'-'+time.strftime("%Y-%m-%d")+'.csv'
                            if not os.path.isfile(filename):
                                init_fundsheet(url, url_base)         
                                
                            user_info = get_user_info(sender_id)
                            print user_info
                            if user_info:
                                username = user_info['first_name']
                                locale = user_info['locale']
                                gender = user_info['gender']
                                language[sender_id] = locale.split("_")[0]

                                if language[sender_id] == 'fr':                                   
                                    print "change to French"
                                    kernel_fr.setPredicate("name", username, sender_id)
                                    kernel_fr.setPredicate("gender", gender, sender_id)     
                                    kernel_fr.setPredicate("language", language[sender_id], sender_id)
                                    kernel_fr.saveBrain("bot_brain_fr.brn")
                                else:
                                    language[sender_id] = 'en'
                                kernel_en.setPredicate("name", username, sender_id)
                                kernel_en.setPredicate("gender", gender, sender_id)                             
                                kernel_en.setPredicate("language", language[sender_id], sender_id)
                                kernel_en.saveBrain("bot_brain_en.brn")

                            send_template_message(sender_id, " ", language[sender_id])
                        #counter[sender_id] += 1
                        log("counter = {counte}".format(counte=counter[sender_id]))

                        with open ('name_list_str', 'rb') as fp:
                            name_list_str = pickle.load(fp)

                        with open ('dict_url', 'rb') as fp:
                            dict_url = pickle.load(fp)  
                        print kernel_en.getSessionData()  
                        print kernel_fr.getSessionData()   
                        bot_response = respond(sender_id, message_text, name_list_str, dict_url, language[sender_id])
                        send_message(sender_id, bot_response)
                        treating_flag = False
                        

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        print "postback", messaging_event                  
                        received_postback(messaging_event)
                        treating_flag = False
    print counter

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_template_message(recipient_id, message_text, language = 'en'):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    if language == 'fr':
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
                      "title": "Chercher des fonds",
                      "payload": "fundsearch"
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
                      "title": "Search for a fund",
                      "payload": "fundsearch"
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)        

def received_postback(messaging_event):
    global language    
    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

    # The 'payload' param is a developer-defined field which is set in a postback button for Structured Messages. 
    payload = messaging_event["postback"]["payload"] 

    log("Received postback for {user} and page {recipient}: {text}".format(user=sender_id, recipient=recipient_id, text=payload))

    if payload == "fundsearch":
        if language[sender_id] == 'fr':
            response = "Vous pouvez taper le code ISIN comme 'lu1165135440' pour une recherche precise, ou le mot cle de nom du fonds comme 'aqua'."
        else:
            response = "You can either type the ISIN code such as 'lu1165135440' for a precise search of fundsheet, or type the keywords of the fund name such as 'aqua' for a vague fundsearch."
        send_message(sender_id, response)
    # When a postback is called, we'll send a message back to the sender to let them know it was successful
    # send_message(sender_id, payload)

def get_user_info(sender_id, fields=None):
    """Getting information about the user
    https://developers.facebook.com/docs/messenger-platform/user-profile
    Input:
      recipient_id: recipient id to send to
    Output:
      Response from API as <dict>
    """
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }

    request_endpoint = '{0}/{1}'.format(graph_url, sender_id)
    response = requests.get(request_endpoint, params=params)
    if response.status_code == 200:
        return response.json()

    return None


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
