import time
import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData,TransportType

# CHARGEMENT DES VARIABLES 
load_dotenv()

# CONNEXION EVENT HUB 
CHAINE_CONNEXION = os.getenv("EVENT_HUB_CONNECTION_STR")
NOM_HUB = "commandes"


# VRAIES DONNÉES 
vrais_clients = ["Martin_Sophie", "Bernard_Lucas", "Dubois_Emma"]

vrais_titres = {
    "Devotion": 12.99,
    "Scary Godmother: Halloween Spooktakular": 5.99,
    "The Matrix": 9.99
}
liste_titres = list(vrais_titres.keys())

# DEMARRAGE DU PRODUCTEUR ET CONNEXION SUR LE PORT 443 (WebSockets)
producer = EventHubProducerClient.from_connection_string(
    conn_str=CHAINE_CONNEXION, 
    eventhub_name=NOM_HUB,
    transport_type=TransportType.AmqpOverWebsocket 
)

print("Connexion établie sur le port 443. Début de l'envoi...")

# BOUCLE D'ENVOI 
for y in range(0, 20):
    event_data_batch = producer.create_batch() 
    titre_choisi = random.choice(liste_titres)
    
    commande = {
        "id_commande": f"CMD-{int(time.time())}",
        "client_id": random.choice(vrais_clients),
        "titre": titre_choisi,
        "prix": vrais_titres[titre_choisi],
        "date_commande": str(datetime.utcnow())
    }
    
    event_data_batch.add(EventData(json.dumps(commande)))
    producer.send_batch(event_data_batch)
    
    print(f"Commande {y+1}/20 expédiée : {commande}")
    time.sleep(3)

producer.close()
print("Transmission terminée et connexion fermée.")
