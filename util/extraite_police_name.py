import os

dossier = "polices"
liste_de_polices = os.listdir(dossier)

temp = []
for police in liste_de_polices:
    if 'ttf' in police:
        temp.append(police)
        
print(temp)

import json

file = open(r"polices\polices.json", 'w')
json.dump(temp, file, indent=4)
file.close()