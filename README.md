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

## Pré-requis

```bash
pip install pandas firebase-admin
```

## `FIRESTORE TO POSTGRESQL (STREAM)`




