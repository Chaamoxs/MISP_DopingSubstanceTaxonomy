from pytaxonomies import Taxonomy
from pytaxonomies import Entry
from pytaxonomies import Predicate
import requests
from bs4 import BeautifulSoup
import json

#attention au sauf
#dernier prédicat -> faut changer ça met des noms de sports parce que c'est dans des <li>


def listePredicats(article):
    liste={}
    for art in article:
        titre = art.find('p', attrs={"class":"h3 panel-title"})
        pred = Predicate()
        pred.predicate = titre.text
        pred.expanded = titre.text
        div = art.find('div', attrs={"class":"layout-wysiwyg"})
        #print(div.text)
        descrip = div.find('p')
        print(descrip.text)
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
    #categorie = art.find('div', attrs={"class":"list-img"})
    #print(categorie.text.lstrip().strip())
    titre = art.find('p', attrs={"class":"h3 panel-title"})
    #print(titre.text)
    produits = art.findAll('li')
    listeProduits={}
    for prod in produits:
        entree = Entry()
        entree.value=prod.text
        entree.expanded=prod.text
        listeProduits.update({entree.value : entree})
    
    new_taxonomy.predicates[titre.text].entries=listeProduits

#print(new_taxonomy.to_json())
with open('../../machinetag.json', 'wt', encoding='utf-8') as f:
    json.dump(new_taxonomy.to_dict(), f, indent=2, ensure_ascii=False)