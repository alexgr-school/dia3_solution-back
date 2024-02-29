"""
Nom du fichier: main.py
Auteur: Alexandre GRODENT
Date: 29/02/2024

Description:
Ce script analyse les parcours entre différents nœuds à partir d'un fichier CSV.
Il identifie le chemin le plus long et le plus court en termes de distance parcourue, et calcule des métriques statistiques
pour l'ensemble des chemins trouvés, telles que la moyenne, la médiane, l'écart-type, et l'écart interquartile des distances.

Le fichier CSV doit contenir les colonnes suivantes:
- 'noeud_amont' : Le noeud de départ de l'arête.
- 'noeud_aval' : Le noeud d'arrivée de l'arête.
- 'type_aretes' : Indique le type de l'arête, pouvant être 'depart', 'arrivee' ou 'chemin'.
- 'distance' : La distance entre le noeud amont et le noeud aval.
- 'arete_id' : Un identifiant unique pour chaque arête.

Dépendances: pandas, numpy
"""

import numpy as np
import pandas as pd

# Chargement du fichier CSV
explorer_df = pd.read_csv("./data/parcours_explorateurs.csv")

# Préparation des données
upstream_downstream = explorer_df.set_index(["noeud_amont", "noeud_aval"]).to_dict()[
    "distance"
]

# Points de départ et d'arrivée uniques
start_nodes = set(
    explorer_df.loc[
        explorer_df["type_aretes"] == "depart", "noeud_amont"
    ].drop_duplicates()
)
end_nodes = set(
    explorer_df.loc[
        explorer_df["type_aretes"] == "arrivee", "noeud_aval"
    ].drop_duplicates()
)


# Recherche de tous les chemins et calcul des distances
def find_paths(start_node, visited=[], distance=0):
    if start_node in end_nodes:
        path_distances.append(distance)
        return
    visited.append(start_node)
    for (upstream, downstream), dist in upstream_downstream.items():
        if upstream == start_node and downstream not in visited:
            find_paths(downstream, visited.copy(), distance + dist)


path_distances = []
for start_node in start_nodes:
    find_paths(start_node)

if path_distances:
    metrics = {
        "Longueur du chemin le plus long": max(path_distances),
        "Longueur du chemin le plus court": min(path_distances),
        "Moyenne des longueurs": np.mean(path_distances),
        "Médiane des longueurs": np.median(path_distances),
        "Écart-type des longueurs": np.std(path_distances),
        "Écart interquartile des longueurs": np.percentile(path_distances, 75)
        - np.percentile(path_distances, 25),
    }
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}")
else:
    print("Aucun chemin trouvé.")
