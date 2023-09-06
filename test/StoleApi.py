import csv
import requests

url = "https://www.blagues-api.fr/api/random"
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTY2NjYwNjQyMTQwOTc5MjAwIiwibGltaXQiOjEwMCwia2V5IjoiampiQ3lXNkh4Q245a3ViVEFkaGhLbHpWT3dRZDFQRGpWb2RoUm1RbUF2WkFSc05QT2siLCJjcmVhdGVkX2F0IjoiMjAyMy0wOC0yNVQwODoyODozOSswMDowMCIsImlhdCI6MTY5Mjk1MjExOX0.Mo_gQ_sn-izhysIhjG1npu5vOmfsugmrELnFuDh-SYY "}

# Enregistrer les informations dans un fichier CSV
with open("blague.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["type", "Blague", "Reponse"])

    # Utiliser un ensemble pour stocker les blagues uniques
    blagues_uniques = set()
    nombre_total_de_blagues = 2462

    while len(blagues_uniques) < nombre_total_de_blagues:
        response = requests.get(url, headers=headers)
        donnee = response.json()

        # Créer une chaîne unique pour la blague et la réponse
        blague = f"{donnee['joke']} - {donnee['answer']}"

        # Vérifier si la blague est déjà dans l'ensemble
        if blague not in blagues_uniques:
            blagues_uniques.add(blague)
            writer.writerow([donnee['type'], donnee['joke'], donnee['answer']])
            print(f"Blague {len(blagues_uniques)} ajoutée")
        else:
            print("Blague déjà présente, en cherchant une autre...")
