#!/bin/bash

URL_cellier="https://www.saq.com/content/SAQ/fr/produits/nouveautes/nouvel-arrivage-cellier.html"

#URL_cellier="https://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?pageSize=5000&searchTerm=*&catalogId=50000&showOnly=product&beginIndex=0&langId=-2&storeId=20002&facet=ads_f23_ntk_cs%3A%2522Nouvel%2Barrivage%2BCellier%2522&orderBy=1"
Fichier_cellier_out="nouvel-arrivage-cellier.html"

URL_signature="https://www.saq.com/content/SAQ/fr/produits/nouveautes/nouvel-arrivage-saq-signature.html"


curl -L $URL_cellier -o $Fichier_cellier_out

#sleep 5
#wget $URL_signature
