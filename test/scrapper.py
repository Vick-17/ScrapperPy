import requests
from bs4 import BeautifulSoup
import csv

url = "https://fr.wikipedia.org/wiki/Courteney_Cox"

response = requests.get(url)

if response.status_code != 200:
    print("Erreur lors de la récupération de la page")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

infobox = soup.find("div", {"class": "infobox_v3 noarchive large"})

# Vérifier si l'infobox a été trouvé
if infobox is None:
    print("Infobox introuvable")
    exit()

# Récupérer les informations de base
nom = infobox.find("th", {"scope": "row"})
if nom is not None:
    nom = nom.text

naissance = infobox.find("time", {"class": "nowrap"})
if naissance is not None:
    naissance = naissance.text

biographie = soup.find("div", {"class": "mw-parser-output"}).find_next("p").text

# Enregistrer les informations dans un fichier CSV
with open("courteney_cox.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Nom", "Date de naissance", "Biographie"])
    writer.writerow([nom, naissance, biographie])
