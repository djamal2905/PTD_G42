import os
import pandas as pd
import numpy as np

# Dans ce module, nous allons lire chacun des jeux de données et réaliser
#  un premier
#  traitement


def import_data(path):
    """
    Lecture des fichier CSV nécessaire au traitement

    path : str
        le chemin vers qui mène au répertoire contenant vos
        différents fichiers.
        NB. Ne pas mettre de back-slash à la fin du chemin
    """

    if path == "" or not isinstance(path, str):
        raise ValueError("Entrez un chemin valide")

    # listons l'ensemble des fichiers
    paths = os.listdir(path)
    # tables = [file.replace(".csv", "") for file in paths]

    # Lecture des fichier
    data = {}
    for file in paths:
        if file.endswith(".csv"):
            try:
                data[file.replace(".csv", "")] = pd.read_csv(f"{path}/{file}")
            except Exception(f"Erreur de lecture du fichier {file}") as e:
                print(e)
    # print("Fin de lecture des fichiers.\n")
    # print(f'Les jeux de donnees disponible sont : {tables}')

    return data


def inch_to_cm(x):
    """
    Cette méthode va permettre de convertir des valeurs de inch en cm

    Parameters
    ------------
        x : str
            la quantité en inch au format : a-b
            avec a le nombre de 'pied' et b le nombre de 'pouce'

    Returns
    --------
        int
            la quantité en cm
    """

    # Tester le paramètre en entré
    if x is not np.nan:
        if not isinstance(x, str):
            raise ValueError("L'argument n'est pas un str")

    # Traitement
    if x is np.nan:
        return x
    else:
        # format: '7-11'
        mesure = x.split("-")
        pied = float(mesure[0])
        pouce = float(mesure[1])
        return 30.48 * pied + pouce * 2.54


def replace_old_team_name(
    data: pd.DataFrame, column: str, nba_franchises_old_names: dict
) -> pd.DataFrame:
    """
    Remplace les anciens noms des franchises NBA par leurs
    nouveaux noms dans une colonne spécifique d'un DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        Le DataFrame contenant les données à traiter.
    column : str
        Le nom de la colonne dans laquelle les anciens noms
        de franchises doivent être remplacés.
    nba_franchises_old_names : dict
        Un dictionnaire où les clés sont les nouveaux noms
        des franchises et les valeurs sont des listes des anciens noms.

    Returns
    -------
    pd.DataFrame
        Le DataFrame avec les anciens noms remplacés par
        les nouveaux noms dans la colonne spécifiée.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("L'argument data doit être un pd.DataFrame")

    if not isinstance(column, str):
        raise TypeError("L'argument column doit être de type str")
    if not isinstance(nba_franchises_old_names, dict):
        raise TypeError("L'argument nba_franchises_old_names doit être un dictionnaire")
    if column not in data.columns:
        raise ValueError("La colonne spécifiée n'existe pas dans la table")

    for key, old_names in nba_franchises_old_names.items():
        if old_names:
            data.loc[data[column].isin(old_names), column] = key

    return data
