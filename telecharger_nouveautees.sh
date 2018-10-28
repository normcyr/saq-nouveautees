#!/bin/bash

URL_cellier="https://www.saq.com/content/SAQ/fr/produits/nouveautes/nouvel-arrivage-cellier.html"
URL_signature="https://www.saq.com/content/SAQ/fr/produits/nouveautes/nouvel-arrivage-saq-signature.html"

wget $URL_cellier
sleep 5

wget $URL_signature
