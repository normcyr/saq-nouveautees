#!/bin/usr/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
from datetime import datetime


def extraire_donnees(fichier_nouv_cellier, parser):

    # création de la soupe à partir du fichier de résultats téléchargé
    with open(fichier_nouv_cellier, 'r') as requete:
        soupe = BeautifulSoup(requete, parser)

    return(soupe)


def trouver_resultats(soupe):

    # trouver section liste des resultats
    soupe_resultats_info = soupe.find_all('div', attrs={'class': 'mev-product-content'})
    soupe_resultats_prix = soupe.find_all('div', attrs={'class': 'product-price'})

    return(soupe_resultats_info, soupe_resultats_prix)


def extraire_info(resultat_info):

    # extraction des résultats en utilisant BeautifulSoup
    titre = resultat_info.find('div', attrs={'class': 'mev-product-title '}).find('a')['title'].replace('\xa0',' ')
    identite = resultat_info.find('span', attrs={'class': 'dprod-identite'}).text.strip()
    pays = resultat_info.find('span', attrs={'class': 'dprod-pays'}).text.strip()
    volume = resultat_info.find('div', attrs={'class': 'dprod-format'}).text.strip().replace('\xa0',' ')
    code_saq = resultat_info.find('div', attrs={'class': 'dprod-codesaq'}).text.replace('Code SAQ :\xa0', '')
    url = resultat_info.find('div', attrs={'class': 'mev-product-title '}).find('a')['href']

    # certains champs sont optionels alors éviter les erreurs si c'est vide
    appelation = resultat_info.find('span', attrs={'class': 'dprod-appellation'})
    if appelation != None:
        appelation = appelation.text.strip()

    cepage = resultat_info.find('div', attrs={'class': 'dprod-cepage'})
    if cepage != None:
        cepage = cepage.text.strip()

    region = resultat_info.find('span', attrs={'class': 'dprod-region'})
    if region != None:
        region = region.text.strip()

    #prix = resultat_prix.find('td', attrs={'class': 'price'}).text.strip()

    # construction du dictionaire
    info_produit = {'titre': titre,
                    'appelation': appelation,
                    'cépage': cepage,
                    'identité': identite,
                    'pays': pays,
                    'région': region,
                    'volume': volume,
                    #'prix': prix,
                    'code SAQ': code_saq,
                    'URL': url}

    # construction de la ligne CSV
    info_produit_csv = [titre, appelation, cepage, identite, pays, region, volume, code_saq, url]

    return(info_produit, info_produit_csv)


def faire_html(ajd):

    # lire le fichier CSV, le convertir en data frame puis l'écrire en HTML
    with open('sortie.csv', 'r') as fichier_csv:
        df = pd.read_csv(fichier_csv)

    with open('sortie.html', 'w') as fichier_html:
        fichier_html.write('Données récoltées le {}'.format(ajd))
        fichier_html.write(df.to_html())


def main():

    parser = 'html.parser'
    fichier_nouv_cellier = 'nouvel-arrivage-cellier.html'
    ajd = datetime.now().strftime("%Y-%m-%d")

    soupe = extraire_donnees(fichier_nouv_cellier, parser)
    soupe_resultats_info, soupe_resultats_prix = trouver_resultats(soupe)

    # créer la ligne de titre dans le fichier CSV
    with open('sortie.csv', 'w') as fichier_csv:
        fichier_csv.write('titre,appelation,cépage,identité,pays,région,volume,code SAQ,url\n')

    # créer les fichiers JSON et CSV
    for resultat_info in soupe_resultats_info:
        info_produit, info_produit_csv = extraire_info(resultat_info)

        with open('sortie.json', 'a') as fichier_json:
            fichier_json.write(json.dumps(info_produit, indent = 4)+ '\n')

        with open('sortie.csv', 'a') as fichier_csv:
            csvwriter = csv.writer(fichier_csv)
            csvwriter.writerow(info_produit_csv)

    # créer fichier HTML à partir du CSV
    faire_html(ajd)
    

if __name__ == '__main__':
    main()
