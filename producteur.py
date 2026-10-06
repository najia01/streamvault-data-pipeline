import time
import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData, TransportType
from azure.storage.blob import BlobServiceClient

# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
load_dotenv()
CHAINE_CONNEXION_EH = os.getenv("EVENT_HUB_CONNECTION_STR")
NOM_COMPTE = os.getenv("STORAGE_ACCOUNT")
CLE_COMPTE = os.getenv("ACCOUNT_KEY")

NOM_HUB = "commandes"
NOM_CONTENEUR = "clean"
PREFIXE_DOSSIER = "clients_enrichis/"

# RÉCUPÉRATION DIRECTE DES CLIENTS ENRICHIS DEPUIS LE DATA LAKE
print("Connexion au Data Lake en cours pour récupérer les clients...")
vrais_clients = []

try:
    blob_service_client = BlobServiceClient(
        account_url=f"https://{NOM_COMPTE}.blob.core.windows.net", 
        credential=CLE_COMPTE
    )
    container_client = blob_service_client.get_container_client(NOM_CONTENEUR)
    blobs_list = container_client.list_blobs(name_starts_with=PREFIXE_DOSSIER)
    
    for blob in blobs_list:
        if blob.name.endswith(".json"):
            blob_client = container_client.get_blob_client(blob)
            donnees_json_lines = blob_client.download_blob().readall().decode('utf-8')
            
            for ligne in donnees_json_lines.strip().split('\n'):
                if ligne.strip():
                    client_dict = json.loads(ligne)
                    vrais_clients.append(client_dict["_id"])
                    
    print(f"Succès : {len(vrais_clients)} clients chargés directement depuis Azure !")

except Exception as e:
    print(f"Erreur lors de la lecture sur Azure : {e}")
    vrais_clients = ["Martin_Sophie", "Bernard_Lucas", "Dubois_Emma"]

# GESTION DU CATALOGUE
vrais_titres = {
    "Devotion": 12.99,
    "Scary Godmother: Halloween Spooktakular": 5.99,
    "The Matrix": 9.99,
    "Inception": 14.99,
    "Dune": 15.99
}
liste_titres = list(vrais_titres.keys())

# DEMARRAGE DU PRODUCTEUR EVENT HUB SUR LE PORT 443
producer = EventHubProducerClient.from_connection_string(
    conn_str=CHAINE_CONNEXION_EH, 
    eventhub_name=NOM_HUB,
    transport_type=TransportType.AmqpOverWebsocket 
)

print("Connexion à l'Event Hub établie sur le port 443. Début de l'envoi des commandes...")

# BOUCLE D'ENVOI EN CONTINU
# On extrait 20 clients uniques au hasard 
clients_uniques = random.sample(vrais_clients, 20)

for y in range(0, 20):
    event_data_batch = producer.create_batch() 
    titre_choisi = random.choice(liste_titres)
    
    commande = {
        "id_commande": f"CMD-{int(time.time())}",
        # Utilise un client différent à chaque tour
        "client_id": clients_uniques[y], 
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