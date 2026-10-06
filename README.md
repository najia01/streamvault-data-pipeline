# StreamVault - Pipeline Cloud Data Engineering

## Contexte du Projet

StreamVault est une plateforme de streaming vidéo souhaitant diversifier son catalogue avec des livres numériques et mieux analyser géographiquement sa base d'abonnés.

Ce projet consiste à construire un pipeline cloud de bout en bout capable de gérer :

1. L'ingestion automatisée du catalogue et des abonnés (batch).
2. L'enrichissement et le stockage des données.
3. L'absorption d'un flux de commandes en temps réel (streaming).
4. L'alerte en cas d'incident et la restitution visuelle/sémantique.

## Architecture Technique

Le projet repose sur une architecture hybride Cloud (Azure) / Local, séparant distinctement les flux Batch et Streaming :

- **Orchestration :** Azure Data Factory (ADF).

- **Stockage Cloud :** Azure Data Lake Storage Gen2 (ADLS - conteneurs `raw/` et `clean/`).

- **Transformation :** Databricks (Apache Spark / PySpark).

- **Messagerie Temps Réel :** Azure Event Hubs.

- **Base de Données Finale :** MongoDB (local) connecté via un Self-hosted Integration Runtime (SHIR).

- **Alerting :** Azure Logic Apps.

- **Restitution :** Power BI (Dashboard) et WebProtégé/WebVOWL (Ontologie OWL/RDF).

- **Architecture réelle :** Architecture réelle réalisée avec Mermaid.

## Fonctionnalités Principales

### 1. Ingestion et traitement batch

- **Sources :** `movies.json`, `book1-100k.csv`, et `clients.csv`.
- **Enrichissement API :** Déduplication des codes postaux clients via Databricks et enrichissement avec l'API `geo.api.gouv.fr` via une boucle native ADF.
- **Chargement MongoDB :** Stockage sécurisé et idempotent (garantie de non-duplication) dans des collections distinctes pour le catalogue mixte (films/livres) et les clients.

### 2. Flux Temps Réel (Streaming)

- **Producteur Python :** Script générant une commande toutes les 3 secondes en croisant de vrais clients et de vrais médias du catalogue.
- **Consommateur Databricks :** Lecture en continu (Structured Streaming) depuis Azure Event Hubs et écriture par micro-lots dans MongoDB.
- **Sécurité :** Transport chiffré (AMQP sur WebSockets via le port 443).

### 3. Automatisation et Alerting

- **Planification :** Déclenchement automatique (Trigger) du pipeline Batch quotidien à 10h00.
- **Alerting :** Envoi d'un email d'alerte via Azure Logic Apps en cas d'échec d'une activité du pipeline.

### 4. Restitution et Modélisation

- **Dashboard Power BI :** Visualisation des KPI du catalogue et croisement géographique des commandes clients.
- **Ontologie Sémantique :** Modélisation RDF/OWL sur WebProtégé définissant les relations entre les classes `Film`, `Livre`, `Client` et `Commande`.

## Installation & Prérequis

1. **Environnement Azure :**

- Souscription Azure active avec les ressources provisionnées (ADF, Databricks, Event Hubs niveau Basic, ADLS Gen2, Logic App).

2. **Environnement Local :**

- **MongoDB** et **MongoDB Compass** installés.
- **Self-hosted Integration Runtime (SHIR)** installé et configuré sur la machine hébergeant MongoDB.
- **Python 3.x** avec la librairie `azure-eventhub` et `websocket-client` pour le script producteur.
