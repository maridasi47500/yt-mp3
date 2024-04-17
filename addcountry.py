import json
from fichier import Fichier
from country import Country
dbPays=Country()
x=json.loads(Fichier("./","temp2.json").lire())
for pays in x["pays"]:
    phone=""
    name=""
    unicode=""
    
    try:
        phone=pays["phone"]
    except:
        phone=""
    try:
        name=pays["country"]
    except:
        name=""
    try:
        unicode=pays["unicode"]
    except:
        unicode=""
    dbPays.create({"name":name,"unicode":unicode,"phone":phone})
