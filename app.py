import os
import sys
import json
import aiml
import re

import requests
from flask import Flask, request

app = Flask(__name__)

graph_url = 'https://graph.facebook.com/v2.6'
counter = 0


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        global counter
        counter = 0
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200



@app.route('/', methods=['POST'])
def webhook():
    
    # endpoint for processing incoming messaging events
    global counter
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text

                    except KeyError:
                        message_text = "smile"

                    kernel = aiml.Kernel()


                    if os.path.isfile("bot_brain.brn"):
                        kernel.bootstrap(brainFile = "bot_brain.brn")
                    else:
                        kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"))#, commands = "load aiml b"

                        kernel.setBotPredicate("name", "Pikachu")
                        kernel.setBotPredicate('master', 'Mina')
                        kernel.setBotPredicate("age","0")
                        kernel.setBotPredicate("birthday","March 8, 2017")
                        kernel.setBotPredicate("birthplace","Paris")
                        kernel.setBotPredicate("botmaster", "botmaster")
                        kernel.setBotPredicate("boyfriend","I am single")
                        kernel.setBotPredicate("build","PyAIML")
                        kernel.setBotPredicate("celebrities","Oprah, Steve Carell, John Stewart, Lady Gaga")
                        kernel.setBotPredicate("celebrity","Jina")
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

                        kernel.saveBrain("bot_brain.brn")

                    if counter == 0:
                        user_info = get_user_info(sender_id)
                        if user_info:
                            username = user_info['first_name']
                            language = user_info['locale']

                    # kernel now ready for use
                            bot_response = "Hi "+username+", nice to meet you!"
                            counter += 1
                            log("counter = {counte}".format(counte=counter))
                        send_template_message(sender_id, bot_response)
                    
                    bot_response = kernel.respond(message_text)
                    keywords = re.sub(' ', '+', message_text)
                    url = "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/?s="+keywords 

                    bot_response += " Maybe you can try this link: "+ url 
                    send_message(sender_id, bot_response)
                    

                if messaging_event.get("delivery"):  # delivery confirmation
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    user_info = get_user_info(sender_id)
                    if user_info:
                        username = user_info['first_name']
                        language = user_info['locale']
                        bot_response = "Hi "+username+", nice to meet you!"
                    send_template_message(sender_id, " ")

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    #print "postback", messaging_event
                    received_postback(messaging_event)

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
        
def send_template_message(recipient_id, message_text):

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
        "message":{
            "attachment":{
            "type":"template",
            "payload":{
            "template_type":"generic",
            "elements": [{
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
          }, {
            "title": "Investo",
            "item_url": "http://investo.bnpparibas/",               
            #"image_url": "https://www.google.fr/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjbsZO-tMLSAhWJuBQKHQSADPgQjRwIBw&url=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Finvesto-par-bnp-paribas%2Fid1189529445%3Fmt%3D8&psig=AFQjCNHkkFs7ZrfJGrDcKqVwNaDesChYyw&ust=1488907950510928",
            "buttons": [{
              "type": "web_url",
              "url": "http://investo.bnpparibas/",
              "title": "Download Investo"
            # }, {
            #   "type": "postback",
            #   "title": "Call Postback",
            #   "payload": "Payload for second bubble",
            # }]
            # "text":message_text,
            # "buttons":[
            # {
            #     "type":"web_url",
            #     "url":"http://www.bnpparibas-ip.fr/investisseur-prive-particulier/fundsheet",
            #     "title":"Show fundsheet Website"
            # },
            # {
            # "type":"postback",
            # "title":"English",
            # "payload":"English"
            }
            ]
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
    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

    # The 'payload' param is a developer-defined field which is set in a postback button for Structured Messages. 
    payload = messaging_event["postback"]["payload"] 

    log("Received postback for {user} and page {recipient}: {text}".format(user=sender_id, recipient=recipient_id, text=payload))
    #log("Received postback for user %d and page %d with payload '%s' ", sender_id, recipient_id, payload)

    # When a postback is called, we'll send a message back to the sender to let them know it was successful
    send_message(sender_id, payload)

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
    counter = 0
    app.run(debug=True)
