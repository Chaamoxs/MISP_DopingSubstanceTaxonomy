from pytaxonomies import Taxonomy
from pytaxonomies import Entry
from pytaxonomies import Predicate
import requests
from bs4 import BeautifulSoup
import json

#attention au sauf

#ignore = liste des catégories qu'on veut pas 

ignore = []
ignore = ['BÊTABLOQUANTS', 'SUBSTANCES NON APPROUVÉES']
#Betabloquant = pas interdit pour tous les sports
#Substance non appouvées = pas interressant

def listePredicats(article):
    liste={}
    for art in article:
        titre = art.find('p', attrs={"class":"h3 panel-title"})
        presenceIgnore = False
        for i in ignore:
            if titre.text == i:
                presenceIgnore = True
                #print("on ignore pas" + titre.text)
            #else:
                #print("pasla")

        if not presenceIgnore:
            pred = Predicate()
            pred.predicate = titre.text
            pred.expanded = titre.text
            div = art.find('div', attrs={"class":"layout-wysiwyg"})
            descrip = div.find('p')
            pred.description = descrip.find_next_sibling().text
            liste.update({titre.text : pred})
    return liste

new_taxonomy = Taxonomy()

new_taxonomy.name = "doping-substances"
new_taxonomy.description = "This taxonomy aims to list doping-substance"
new_taxonomy.version = 1
new_taxonomy.expanded = "Doping-substance"

response = requests.get("https://www.wada-ama.org/fr/liste-des-interdictions?")

soup = BeautifulSoup(response.text, 'html.parser')

article = soup.findAll('article', attrs={"class":"panel hide-reader"})

new_taxonomy.predicates = listePredicats(article)

for art in article:

    titre = art.find('p', attrs={"class":"h3 panel-title"})
    presenceIgnore = False
    for i in ignore:
        if titre.text == i:
            presenceIgnore = True

    if not presenceIgnore:
        produits = art.findAll('li')
        listeProduits={}
        for prod in produits:
            entree = Entry()
            entree.value=prod.text
            entree.expanded=prod.text
            listeProduits.update({entree.value : entree})
            
            new_taxonomy.predicates[titre.text].entries=listeProduits
    

#print(new_taxonomy.to_json())

#création du JSON
with open('machinetag.json', 'wt', encoding='utf-8') as f:
    json.dump(new_taxonomy.to_dict(), f, indent=2, ensure_ascii=False)