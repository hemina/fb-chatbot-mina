
# coding: utf-8

import json

config = {'PAGE_ACCESS_TOKEN' : 'EAAXIHwFxIAQBAFABjCZCMg4ziZAOMvRXHfb8BvrsEXRy4bYepitQSRTLJKod0NksB14CUCytcVhLrejZCep8aVucxrZB7ve9M1VzrKupitwxfQFw5FzLXNprpICd9PgaiiOyQX4eWuJqBZAEWTnmzLpHcu5ixAdBjpuFYZCCSxJAZDZD',
          'graph_url' : 'https://graph.facebook.com/v2.6',
          'name_fund_search' : "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/?s=",
          'fundsearch_url': "http://bnp-ip-onecms-api.bearstech.com/push/fundsearchv2/PV_FR-IND/FRE",
          "fundsheet_url_base": "http://www.bnpparibas-ip.fr/investisseur-prive-particulier/fundsheet/",
          'param':{'master': 'Mina', "age": "0", "birthday": "March 8, 2017", "birthplace": "Paris", "botmaster": "botmaster", "city": "Paris",
            "country":"France", "email": "mina.he1992@gmail.com", "nationality":"French", "question": "Which funds would you want to invest in?"
            },
          'en':{
        'isin_url_response':" Please find here the fundsheet you are looking for : ", 
        'name_url_response':" Maybe you can try this link: ", 
        'fundsearch_postback': "You can either type the ISIN code such as 'lu1165135440' for a precise search of fundsheet, or type the keywords of the fund name such as 'aqua' for a vague fundsearch.",
        'list_isin_url_response':" Here is the list of fundsheets you are looking for : "},
          
          'fr':{'isin_url_response':" Veuillez trouver ici la fiche de fonds vous cherchez : ", 
                'name_url_response':" Tentez ce lien pour plus d'informations: ", 
                'fundsearch_postback': "Vous pouvez taper le code ISIN comme 'lu1165135440' pour une recherche precise, ou le mot cle de nom du fonds comme 'aqua'.",
                'list_isin_url_response': " Veuillez trouver ici la liste des fiches de fonds vous cherchez : "}
         }
with open('config.json', 'w') as outfile:
    json.dump(config, outfile)


