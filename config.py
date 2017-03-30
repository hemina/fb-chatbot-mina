
# coding: utf-8

import json
import pandas as pd

# We have to use internal internet to download these files 
question_file1 = 'other_project' #https://api-int.ip.dev.echonet.net.intra/investment-advisor/question?project_type=project
question_file2 = 'just_invest' #https://api-int.ip.dev.echonet.net.intra/investment-advisor/question?project_type=just_invest
question_file3 = 'retirement' #https://api-int.ip.dev.echonet.net.intra/investment-advisor/question?project_type=retirement

def load_questions(question_file, language = 'en'):  
  questions = {}
  with open('data/'+question_file+'.json') as json_data_file:
      data = json.load(json_data_file)   
  df = pd.DataFrame(data['questions'])    
  tmp = df[['titles']]['titles']
  if language == 'fr':
    for i in xrange(len(tmp)):
      questions[i] = tmp[i]['fr_FR']
  else:
    for i in xrange(len(tmp)):
      questions[i] = tmp[i]['en_GB']    
  return questions

ANSWERS = {
           '0':[{
              "content_type":"text",
              "title":"1000 euros",
              "payload":"invest_amount"
            },
            {
              "content_type":"text",
              "title":"5000 euros",
              "payload": "invest_amount"
            },
            {
              "content_type":"text",
              "title":"10000 euros",
              "payload": "invest_amount"
            },
            {
              "content_type":"text",
              "title":"50000 euros",
              "payload": "invest_amount"
            }],
           '1':[{
              "content_type":"text",
              "title":"1 year",
              "payload":"horizon"
            },
            {
              "content_type":"text",
              "title":"5 years",
              "payload": "horizon"
            },
            {
              "content_type":"text",
              "title":"10 years",
              "payload": "horizon"
            },
            {
              "content_type":"text",
              "title":"20 years",
              "payload": "horizon"
            },
            {
              "content_type":"text",
              "title":"30 years",
              "payload": "horizon"
            }],
           '2':[{
              "content_type":"text",
              "title":"Very low",
              "payload":"risks"
            },
            {
              "content_type":"text",
              "title":"Low",
              "payload": "risks"
            },
            {
              "content_type":"text",
              "title":"Moderate",
              "payload": "risks"
            },
            {
              "content_type":"text",
              "title":"High",
              "payload": "risks"
            },
            {
              "content_type":"text",
              "title":"Very high",
              "payload": "risks"
            }],    
           '3':[{
              "content_type":"text",
              "title":"No",
              "payload":"investment_options"
            },
            {
              "content_type":"text",
              "title":"Social and responsible invest",
              "payload": "investment_options"
            },
            {
              "content_type":"text",
              "title":"Small caps funds",
              "payload": "investment_options"
            },
            {
              "content_type":"text",
              "title":"Only ETF",
              "payload": "investment_options"
            }]
          }    

ANSWERS_FR = {
           '0':[{
              "content_type":"text",
              "title":"1000 euros",
              "payload":"invest_amount"
            },
            {
              "content_type":"text",
              "title":"5000 euros",
              "payload": "invest_amount"
            },
            {
              "content_type":"text",
              "title":"10000 euros",
              "payload": "invest_amount"
            },
            {
              "content_type":"text",
              "title":"50000 euros",
              "payload": "invest_amount"
            }],
           '1':[{
              "content_type":"text",
              "title":"1 an",
              "payload":"horizon"
            },
            {
              "content_type":"text",
              "title":"5 ans",
              "payload": "horizon"
            },
            {
              "content_type":"text",
              "title":"10 ans",
              "payload": "horizon"
            },
            {
              "content_type":"text",
              "title":"20 ans",
              "payload": "horizon"
            },
            {
              "content_type":"text",
              "title":"30 ans",
              "payload": "horizon"
            }],
           '2':[{
              "content_type":"text",
              "title":"Très bas",
              "payload":"risks"
            },
            {
              "content_type":"text",
              "title":"Bas",
              "payload": "risks"
            },
            {
              "content_type":"text",
              "title":"Moyen",
              "payload": "risks"
            },
            {
              "content_type":"text",
              "title":"Haut",
              "payload": "risks"
            },
            {
              "content_type":"text",
              "title":"Très haut",
              "payload": "risks"
            }],    
           '3':[{
              "content_type":"text",
              "title":"None",
              "payload":"investment_options"
            },
            {
              "content_type":"text",
              "title":"Fonds responsables",
              "payload": "investment_options"
            },
            {
              "content_type":"text",
              "title":"Fonds PME",
              "payload": "investment_options"
            },
            {
              "content_type":"text",
              "title":"ETF",
              "payload": "investment_options"
            }]
          }    

config = {'PAGE_ACCESS_TOKEN' : 'EAAXIHwFxIAQBAK3Kad8eujNr8FZBZCnXbfbP2L5WjKVIA4FshgyqvVqzDs1pRjwdjn2iLZCwx9uzzWZAADhppRs8K1BfZBynPeJwaSZBnGDGQTeTEueiGZA3ZBQGLFDdmWZAV88oOFRT5jU6MN0Cs3nZAZBovT0UvlYkPo1trOWXlN3PwZDZD',
          'graph_url' : 'https://graph.facebook.com/v2.6',
          'name_fund_search' : "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/?s=",
          'fundsearch_url': "http://bnp-ip-onecms-api.bearstech.com/push/fundsearchv2/PV_FR-IND/FRE",
          "fundsheet_url_base": "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/fundsheet/",
          'param':
            {'master': 'Mina', "age": "0", "birthday": "March 8, 2017", "birthplace": "Paris", "botmaster": "botmaster", "city": "Paris",
            "country":"France", "email": "mina.he1992@gmail.com", "nationality":"French", "question": "Which funds would you want to invest in?"
            },
          'en':
            {
            'isin_url_response':" Please find here the fundsheet you are looking for : ", 
            'name_url_response':" Maybe you can try this link: ", 
            'fundsearch_postback': "You can either type the ISIN code such as 'lu1165135440' for a precise search of fundsheet, or type the keywords of the fund name such as 'aqua' for a vague fundsearch.",
            'list_isin_url_response':" Here is the list of fundsheets you are looking for : ",
            'roboAdvisor':
              {
                'ask_invest_type':"What is your project ?", 
                'just_invest': 
                {
                'title':"Just invest", 
                'questions':load_questions('just_invest'),
                'answers': ANSWERS          
                },
                'retirement':
                {
                'title':"Retirement", 
                'questions':load_questions('retirement'),
                'answers': ANSWERS 
                },
                'other_project':{
                'title':"I have other projet.", 
                'questions':load_questions('other_project'),
                'answers': ANSWERS 
                }               
              }
            },
          
          'fr':
            {
            'isin_url_response':" Veuillez trouver ici la fiche de fonds vous cherchez : ", 
            'name_url_response':" Tentez ce lien pour plus d'informations: ", 
            'fundsearch_postback': "Vous pouvez taper le code ISIN comme 'lu1165135440' pour une recherche precise, ou le mot cle de nom du fonds comme 'aqua'.",
            'list_isin_url_response': " Veuillez trouver ici la liste des fiches de fonds vous cherchez : ",
            'roboAdvisor':
              {
                'ask_invest_type':"What is your project ?", 
                'just_invest': 
                {
                'title':"Just invest", 
                'questions':load_questions('just_invest', 'fr'),
                'answers': ANSWERS_FR          
                },
                'retirement':
                {
                'title':"Retirement", 
                'questions':load_questions('retirement', 'fr'),
                'answers': ANSWERS_FR 
                },
                'other_project':{
                'title':"I have other projet.", 
                'questions':load_questions('other_project', 'fr'),
                'answers': ANSWERS_FR 
                }               
              }            
            }
         }
with open('config.json', 'w') as outfile:
    json.dump(config, outfile)


