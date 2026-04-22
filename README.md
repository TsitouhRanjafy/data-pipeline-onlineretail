# Online Retail Data Pipeline

Ce projet implémente un pipeline ETL (Extract - Transform - Load) simple pour traiter le dataset **Online Retail** de UCI/Kaggle. [source](https://www.kaggle.com/datasets/vijayuv/onlineretail)

## Objectif

- Transformer les données brutes de ventes en un format propre et enrichi, prêt à être chargé dans une base de données analytics.

- Migrer les données depuis firestore vers Postgresql afin de faire des requêt complexes pour l'analytics.

## Structure du Pipeline

## `CSV TO FIRESTORE (BATCH)`

Le pipeline est composé de trois étapes principales :

### 1. Extract
- Chargement du fichier CSV `OnlineRetail.csv`
- Utilisation de l'encodage `ISO-8859-1` (nécessaire à cause des caractères £)
- Conversion initiale de la colonne `InvoiceDate` avec `parse_dates`

### 2. Transform

Les transformations appliquées sont les suivantes :

- Suppression des lignes où `Quantity ≤ 0` (retours et annulations)
- Suppression des lignes sans `CustomerID`
- Calcul de la colonne `TotalAmount` = `Quantity × UnitPrice` (arrondi à 2 décimales)
- Nettoyage des colonnes texte (`Description` et `Country`) en supprimant les espaces inutiles
- Conversion de la colonne `InvoiceDate` en `datetime.datetime` natif Python (compatible Firestore)


### 3. Export as CS

- Écriture du DataFrame transformé dans `warehouse/daily_online_retail_YYYY-MM-DD.csv`


### 4. Import to Firestore Emulator

- Chargement par batch via `load_batch_to_firestore()`
- Compatible avec le **Firestore Emulator** (Firebase Local Emulator Suite)
- Les dates sont converties en `datetime.datetime` natif Python avant l'import (requis par le SDK Firestore)


## Code — Fonctions principales

| Fonction | Rôle |
|---|---|
| `extract(filepath)` | Charge le CSV brut en DataFrame |
| `transform(df)` | Nettoie et enrichit les données |
| `load(df, output_path)` | Exporte le résultat en CSV |
| `load_to_firestore(df)` | Charge les données dans Firestore |
| `run()` | Orchestre le pipeline de bout en bout |

---

## `FIRESTORE TO POSTGRESQL (STREAM)`

Ce pipeline secondaire écoute en temps réel les modifications dans Firestore et synchronise les données vers une base PostgreSQL pour permettre des analyses complexes.

### 1. Extract (Streaming)
- Utilisation de `on_snapshot()` du SDK Firestore pour écouter les événements (`ADDED`, `MODIFIED`, `DELETE`, `UPDATE`).
- Validation automatique de l'intégrité des documents avant traitement.
- Connexion configurée pour le **Firestore Emulator**.

### 2. Transform
- Mapping des champs Firestore vers le schéma relationnel PostgreSQL.
- Enrichissement des données avec :
    - `processed_at` : Timestamp du traitement par le pipeline.
    - `change_type` : Type d'événement Firestore (ex: ADDED).
- Conversion des types de données (Decimal, Timestamps).

### 3. Load (PostgreSQL)
- Utilisation d'un **pool de connexions** (`ThreadedConnectionPool`) pour la performance.
- Insertion directe dans la table `orders`.
- Gestion des transactions avec rollback en cas d'erreur.

### 4. Orchestration avec FastAPI
Le pipeline est encapsulé dans une application **FastAPI** :
- Le streaming démarre automatiquement au lancement du serveur via l'événement `lifespan`.
- Un endpoint `/status` permet de vérifier l'état de santé de la connexion.

---

## Code — Fonctions principales (Streaming)

| Fonction | Rôle |
|---|---|
| `start_extract_streaming()` | Initialise l'écouteur (listener) Firestore |
| `on_snapshot(col_snapshot, changes, ...)` | Callback traitant chaque changement de document |
| `transform(doc, change_type)` | Prépare le dictionnaire pour l'insertion SQL |
| `load(record)` | Exécute l'INSERT dans PostgreSQL via le pool |

---

## Pré-requis

```bash
pip install pandas firebase-admin fastapi psycopg2-binary
```

### Configuration PostgreSQL
Le schéma de la table doit être créé au préalable en utilisant le fichier `streaming/firestore_to_postgresql/orders_schema.sql`.

## Lancement

### 1. Démarrer le Batch (CSV -> Firestore)
```bash
cd batch/csv_to_firestore
python main.py
```

### 2. Démarrer le Streaming (Firestore -> Postgres)
```bash
cd streaming/firestore_to_postgresql
fastapi dev main.py
```




