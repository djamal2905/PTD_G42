from utils import inch_to_cm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import copy


class Reponse:
    def __init__(self, data: dict[pd.DataFrame]):
        # Réalisons les tests nécessaire sur l'objet data

        if (
            not isinstance(data, dict)
        ):
            raise TypeError("L'argument data doit être un dictionnaire.")

        if (
            any(not isinstance(data[key], pd.DataFrame) for key in data.keys())
        ):
            raise TypeError("Toutes les valeurs des clés doivents être des "
                            "pandas.DataFrame.")

        # Testons qu'on a bien la clé common_player_info dans le dictionnaire
        if ("draft_history" not in data.keys()):
            raise KeyError("La clé 'draft_history' ne fait pas parti du dictionnaire")
        if ("common_player_info" not in data.keys()):
            raise KeyError("La clé 'common_player_info' ne fait pas parti du "
                           "dictionnaire")
        if ("game" not in data.keys()):
            raise KeyError("La clé 'game' ne fait pas parti du dictionnaire")

        self.data = copy.deepcopy(data)

    def equip_victoires_defaites_saison(self, annee_debut: int, annee_fin: int,
                                        season_type: str = 'Regular Season',
                                        defaite: bool = False) -> pd.DataFrame:
        """
        Calcule le nombre de victoires ou de défaites par équipe pour un
        type de saison NBA donné, entre deux années spécifiques.
        On obtient la réponse grâce a la table 'game'

        Parameters
        ----------
        annee_debut : int
            année de début de saison
            La date de début de la période à considérer.
        annee_fin : int
            année de fin de saison
            La date de fin de  la période à considérer.
        season_type : str, optional
            Le type de saison à considérer : 'Regular Season', 'Pre Season',
            'All-Star' ou 'Playoffs' (default is 'Regular Season').
        defaite : bool, optional
            Si True, retourne le nombre de défaites ; sinon,
            retourne le nombre de victoires (default is False).

        Returns
        -------
        pd.DataFrame
            Un DataFrame contenant pour chaque équipe et
            chaque saison le nombre de victoires ou de défaites, avec les colonnes :
            ['Saison', 'Equipes', 'Nombre de victoires'] ou
            ['Saison', 'Equipes', 'Nombre de défaites'].

        Raises
        ------
        TypeError
            Si data n'est pas un dictionnaire ou si defaite n'est pas un booléen,
            ou si les dates ne sont pas du type int.
        ValueError
            Si annee_debut est postérieure à annee_fin,
            ou si les années sont hors de l'intervalle [1946, 2023].
        KeyError
            Si la clé d'intérêt game n'est pas dans le dictionnaire

        Examples
        ---------
        >>> val_df = pd.DataFrame([
        ...    # Saison régulière pour A
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe B"},
        ...    # Saison pré-saison pour A
        ...    {"season_id": "12022", "season_type": "Pre Season", "wl_home": "W",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        ...    {"season_id": "12022", "season_type": "Pre Season", "wl_home": "L",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        ...    {"season_id": "12022", "season_type": "Pre Season", "wl_home": "W",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        ...    {"season_id": "12022", "season_type": "Pre Season", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        ...    {"season_id": "12022", "season_type": "Pre Season", "wl_home": "W",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        ...    {"season_id": "12022", "season_type": "Pre Season", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe B"},
        ...    # Saison All-Star pour A (Pas de rencontres ici)
        ...    {"season_id": "32022", "season_type": "All-Star", "wl_home": "W",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        ...    {"season_id": "32022", "season_type": "All-Star", "wl_home": "L",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        ...    {"season_id": "32022", "season_type": "All-Star", "wl_home": "W",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        ...    {"season_id": "32022", "season_type": "All-Star", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        ...    {"season_id": "32022", "season_type": "All-Star", "wl_home": "W",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        ...    {"season_id": "32022", "season_type": "All-Star", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe B"},
        ...    # Saison tous types pour B
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
        ... "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
        ... "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        ...    {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
        ... "team_name_home": "Equipe C", "team_name_away": "Equipe B"},
        ... ])

        >>> dict_of_df = {
        ...    "game": val_df
        ...    "common_player_info": val_df
        ...    "draft_history": val_df
        ... }

        >>> reponses = Reponse(dict_of_df)
        >>> resultat = reponses.equip_victoires_defaites_saison(annee_debut=2022,
        ... annee_fin=2023)
        >>> verif = resultat[
        ... resultat['Equipes'] == 'Equipe A']['Nombre de victoires'] == 4
        >>> verif.values[0]
        True
        >>> verif = resultat[
        ... resultat['Equipes'] == 'Equipe B']['Nombre de victoires'] == 6
        >>> verif.values[0]
        True

        >>> reponses = Reponse(dict_of_df)
        >>> resultat = reponses.equip_victoires_defaites_saison(annee_debut=2022,
        ... annee_fin=2023, defaite=True)
        >>> verif = resultat[
        ... resultat['Equipes'] == 'Equipe C']['Nombre de défaites'] == 6
        >>> verif.values[0]
        True
        >>> verif = resultat[
        ... resultat['Equipes'] == 'Equipe A']['Nombre de défaites'] == 2
        >>> verif.values[0]
        True
        >>> verif = resultat[
        ... resultat['Equipes'] == 'Equipe B']['Nombre de défaites'] == 2
        >>> verif.values[0]
        True
        """

        # ------------- Réalisons les tests -------------

        # Les tests qui vérifie la validité de l'objet data est réalisé dans le
        # constructeur. On vérifie donc qu'on a un dictionnaire et que toutes les
        # tables sont des pd.dataFrame

        # testons si la periode est correctement renseignée
        if not (isinstance(annee_debut, int) and isinstance(annee_fin, int)):
            raise TypeError("Les dates de début et de fin doivent être des entiers.")

        if not (annee_debut >= 1946 and annee_fin <= 2023):
            raise ValueError("La période sélectionnée doit être comprise entre 1946 "
                             "inclu et 2023 inclu.")

        if not (annee_debut < annee_fin):
            raise ValueError("La date de début ne peut pas excéder ou être égale à "
                             "la date de fin.")

        # Testons le type de saison choisi
        choix = ['Regular Season', 'Pre Season', 'All-Star', 'Playoffs']
        if season_type not in choix:
            raise ValueError("Le type de saison sélectionné doit être une des valeurs "
                             "suivantes : Regular Season, Pre Season, All-Star,"
                             " Playoffs")

        # Testons la valeur entré pour le paramètre defaite
        if not isinstance(defaite, bool):
            raise TypeError("L'argument defaite doit être de type booléen (True "
                            "or False)")

        # ------------- Réalisons le traitement -------------
        name_var = "Nombre de victoires" if not defaite else "Nombre de défaites"

        # Déterminer le code de la saison selon le type
        season_code = '2'  # Regular Season
        if season_type == 'Pre Season':
            season_code = '1'
        elif season_type == 'All-Star':
            season_code = '3'
        elif season_type == 'Playoffs':
            season_code = '4'

        # Filtrage par type de saison
        game_chosen_season = self.data["game"][
            self.data['game']['season_id'].astype(str).str.startswith(season_code)
        ].copy()

        # Extraire l'année de la saison
        game_chosen_season['season_years'] = game_chosen_season['season_id']\
            .astype(str).str[-4:].astype(int)

        # Filtrage des saisons dans la plage définie
        game_chosen_season = game_chosen_season[
            game_chosen_season['season_years'].isin(range(annee_debut, annee_fin))
        ]

        # Mise en forme de la saison pour affichage
        game_chosen_season['season_years'] = game_chosen_season['season_years']\
            .apply(lambda x: f"{x}-{x + 1}")

        # Détermination des équipes en fonction du résultat souhaité
        game_chosen_season['Equipes'] = np.where(
            ((game_chosen_season['wl_home'] == "W") & (not defaite)) |
            ((game_chosen_season['wl_home'] == "L") & defaite),
            game_chosen_season['team_name_home'],
            game_chosen_season['team_name_away']
        )

        # Agrégation des résultats
        results = game_chosen_season.groupby(["season_years", "Equipes"]).aggregate({
            'wl_home': 'count',
            'Equipes': 'first',
            'season_years': 'first'
        }).reset_index(drop=True)

        # Renommage final des colonnes
        results.rename(columns={
            'wl_home': name_var,
            'Equipes': "Equipes",
            'season_years': "Saison"
        }, inplace=True)

        return results

    # Aujout des méthodes de la classe pour répondre aux différentes questions
    def prop_joueurs_en_nba_selon_universite_de_formation(self, top_N: int = 10,
                                                          annee_draft: int = None,
                                                          periode: str = None,
                                                          graph: bool = False
                                                          ) -> pd.DataFrame:
        """Renvoie un pandas.series donnant la proportion de joueurs qu'on retrouve
        en NBA de 1947 à 2023 selon l'université de formation.
        Il est possible de choisir une année en particulier ou une période bien précise.
        On obtient la réponse grâce a la table 'draft_history'

                Parameters
                ----------
                top_N : int
                    permet de ne représenter que le top N des universités selon le
                    nombre de joueurs formé par l'université
                annee_draft : int = None
                    correspond à l'année d'une draft en particulier
                periode : str = None
                    correspond la période d'étude. Elle est renseigné sous le format :
                    annee_debut-annee_fin
                graph : bool = False
                    permet de préciser si on veut afficher en sortie le graphique à
                    barres ou non

                Returns
                -------
                    result : pandas.DataFrame
                        Les effectifs pour chaque université faisant parti du top N
        """

        # Testons les autres quantités
        if (not (isinstance(top_N, int) and top_N > 0)):
            raise ValueError("L'argument top_N doit etre un entier strictement positif")

        # test sur l'année de draft uniquement quand l'utilisateur précise une année
        if annee_draft is not None and periode is not None:
            raise ValueError("Entrez soit une année soit une période. Donc mettre soit"
                             " le paramètre annee_draft à None soit le paramètre "
                             "période à None")
        if annee_draft is not None:
            if not (
                    isinstance(annee_draft, int) and
                    annee_draft >= 1947 and annee_draft <= 2023
            ):
                raise ValueError("L'année de la draft est un entier compris"
                                 " entre 1947 et 2023")
        # testons si la periode est correctement renseignée
        if periode is not None:
            if not (isinstance(periode, str) and
                    "-" in periode and
                    len(periode.split("-")[0]) == 4 and
                    len(periode.split("-")[1]) == 4
                    ):
                raise ValueError("L'argument periode est incorrecte. Un exemple de "
                                 "valeur possible est '2012-2015'")
            try:
                debut = int(periode.split("-")[0])
                fin = int(periode.split("-")[1])
            except Exception:
                raise ValueError("Les années de début et de fin de la période doivent"
                                 " être des entiers.")

            if not (debut >= 1947 and fin <= 2023 and debut < fin):
                raise ValueError("La période considéré n'est pas existante. Choisir une"
                                 " période entre 1947 et 2023 inclu")

        # testons le fait que le parametre graph est soit True soit False
        if not (isinstance(graph, bool)):
            raise ValueError("L'argument graph doit être un boolean")

        # Réalisons le traitement
        # Filtrons pour ce concenttrer sur les joueurs draftés en
        # provenance d'université/college
        data_draft = self.data["draft_history"][
            (self.data["draft_history"]["draft_type"] == 'Draft') &
            (self.data["draft_history"]["organization_type"] == 'College/University') &
            (self.data["draft_history"]["overall_pick"] != 0)]

        # Filtre les données selon les entrées de l'utilisateur
        if annee_draft is not None:
            name = str(annee_draft)
            result = data_draft[(data_draft["season"] == annee_draft)].\
                groupby("organization")["person_id"].count().\
                sort_values(ascending=False).\
                iloc[:top_N]
        elif periode is not None:
            name = periode
            result = data_draft[
                data_draft["season"].isin(list(range(debut, (fin+1))))].\
                groupby("organization")["person_id"].count().\
                sort_values(ascending=False).\
                iloc[:top_N]
        else:
            name = '1947-2023'
            result = data_draft.groupby("organization")["person_id"].count().\
                sort_values(ascending=False).iloc[:top_N]

        result = pd.DataFrame(data=result.values, index=result.index).\
            rename(columns={0: "Effectif"}).reset_index().\
            rename(columns={'organization': "Université"})

        if graph:
            fig, ax = plt.subplots(figsize=(13, 6))  # Crée une figure + axe avec taille
            # plt.grid(True)
            # Création du bar plot
            graph = ax.bar(result["Université"], height=result["Effectif"])

            # Ajout des labels sur les barres
            ax.bar_label(graph, fmt='%.0f', padding=3)

            # Définir les limites de l'axe Y
            ax.set_ylim(0, max(result["Effectif"].values) + 40)

            # Polices
            font1 = {'family': 'serif', 'color': 'black', 'size': 9}
            font2 = {'family': 'serif', 'color': 'black', 'size': 12}

            # Ajout des éléments de mise en forme
            ax.set_xlabel("Universités", fontdict=font1)
            ax.set_title("Les " + str(top_N) + " universités avec le plus "
                         "de \njoueurs évoluant en NBA", fontdict=font2)
            if annee_draft is not None:
                ax.set_ylabel("Effectif en " + name, fontdict=font1)
            else:
                ax.set_ylabel("Effectif sur la période " + name, fontdict=font1)
            ax.set_xticklabels(result["Université"], rotation=80)

            return result, fig

        return result

    def stat_sur_taille_et_poids_par_poste(self, statistique: str = "Median",
                                           poste: str = None) -> pd.DataFrame:
        """Renvoie un pandas.dataFrame avec la taille et le poids calculé selon la
        statistique souhaité pour chacun des postes. Si un poste est précisé, seul les
        statistiques calculé pour
        ce poste sont retournées.
        On obtient la réponse grâce a la table 'common_player_info'

                Parameters
                ----------
                statistique : str
                    La statistique souhaitée pour la taille et le poids. Les valeurs
                    possibles sont : Max, Min, Median, Mean
                poste : str
                    correspond au poste pour le quel on souhaite particulièrement
                    calculer les statistiques. Les valeurs possibles sont :
                    "Pivot", "Pivot/Ailier fort", "Ailier", "Ailier fort/Pivot",
                    "Ailier/Meneur", "Arrière/Meneur", "Arrière/Ailier"

                Returns
                -------
                    result : pandas.DataFrame
                        les statistiques sur le poids et la taille
        """

        # Testons la statistique souhaité
        if not (isinstance(statistique, str) and
                statistique.capitalize() in ["Mean", "Max", "Min", "Median"]):
            raise ValueError("L'argument statistique doit prendre une des valeurs"
                             " suivantes : Mean, Max, Min, Median")

        # testons si le poste est correctement renseigné
        if poste is not None:
            if not (isinstance(poste, str) and
                    poste in ["Pivot", "Pivot/Ailier fort", "Ailier",
                              "Ailier fort/Pivot", "Ailier/Meneur",
                              "Arrière/Meneur", "Arrière/Ailier"]):
                raise ValueError("L'argument poste est incorrecte. Veuillez choisir "
                                 "une valeur existante : Pivot, Pivot/Ailier fort,"
                                 " Ailier, Ailier fort/Pivot, Ailier/Meneur,"
                                 " Arrière/Meneur, Arrière/Ailier")

        # Traitement des données
        taille_poids = self.data["common_player_info"].\
            loc[:, ["position", "weight", "height"]]

        # Convsersion de la taille en cm
        taille_poids["height"] = taille_poids["height"].apply(lambda x: inch_to_cm(x))
        # Convsersion du poids en kg. On sait que une 1 lb = 0.453592370kg
        taille_poids["weight"] = taille_poids["weight"].\
            apply(lambda x: round(x*0.453592370, 2))

        # Calcule de la statistique souhaité par poste
        if statistique == "Median":
            result = taille_poids.groupby("position").median().round(2)
        elif statistique == "Mean":
            result = taille_poids.groupby("position").mean().round(2)
        elif statistique == "Max":
            result = taille_poids.groupby("position").max().round(2)
        else:  # Soit le Min
            result = taille_poids.groupby("position").min().round(2)

        result = result.reset_index()

        french_label = pd.DataFrame(data={'French': ["Pivot", "Pivot/Ailier fort",
                                                     "Ailier", "Ailier fort/Pivot",
                                                     "Ailier/Meneur", "Arrière/Meneur",
                                                     "Arrière/Ailier"],
                                          'position': ["Center", "Center-Forward",
                                                       "Forward",
                                                       "Forward-Center",
                                                       "Forward-Guard",
                                                       "Guard", "Guard-Forward"]})

        result = result.merge(french_label, on='position')
        result = result.iloc[:, [3, 2, 1]].rename(columns={'French': 'position'})

        result = result.rename(columns={"weight": "Poids Kg",
                                        "height": "Taille cm"})

        if poste is None:
            return result
        else:
            return result.loc[result['position'] == poste, :]

    def equipe_remporte_au_moins_N_fois_le_titre(self, nb_victoire_min: int = 3,
                                                 debut_periode: int = 1946,
                                                 fin_periode: int = 2023
                                                 ) -> pd.DataFrame:
        """Renvoie un pandas.DataFrame avec les équipes ayant remporté plus de N fois
        le titre NBA sur la période considéré ainsi que le nombre de titres emportés.
        On obtient la réponse grâce a la table 'game'

        Parameters
        ----------
            nb_victoire_min : int
                le nombre de victoire minimal du titre NBA sur la période considéré
            debut_periode : int
                l'année de debut de la première saison sur la période considéré
            fin_periode : int
                l'année de fin de la dernière saison sur la période considéré

        Returns
        -------
            result : pandas.DataFrame
                les équipes et le nombre de titre NBA
        """

        # Les tests sur la validité de l'objet data sont réalisés dans la fonction
        # equip_victoires_defaites_saison

        # Les tests sur les paramètres debut_periode et fin_periode sont réalisé dans la
        # fonction equip_victoires_defaites_saison

        # Testons les autres quantités
        if (not (isinstance(nb_victoire_min, int) and nb_victoire_min > 0)):
            raise ValueError("L'argument nb_victoire_min doit etre un entier "
                             "strictement positif")

        # Traitement des données
        resultat = self.equip_victoires_defaites_saison(annee_debut=debut_periode,
                                                        annee_fin=fin_periode,
                                                        season_type='Playoffs')
        # récupération des gagnant pour chaque saison
        # En effet, on sait que celui qui gagne le plus de match durant la phase des
        # playoff est forcement champion NBA car il est parti jusqu'a la final.
        # Aujourd'huit pour être champion NBA, il faut gagner exatement au total
        # 16 matchs dont 4 series (les 4 phases) de 4 victoires.
        max_saison = resultat.groupby("Saison").max("Nombre de victoires")
        max_saison = max_saison.reset_index()
        resultat = resultat.merge(right=max_saison, on="Saison")

        # Récupération du gagnant par saison
        resultat = resultat.loc[
            resultat["Nombre de victoires_x"] == resultat["Nombre de victoires_y"],
            ["Saison", "Equipes"]]

        # Comptons le nombre de victoire par équipe
        resultat = resultat.groupby("Equipes").count()

        # On se ramene a un dictionnaire pour facilité le traitement
        # # Initialisation d'un dictionnaire
        equipe = resultat.to_dict()["Saison"]

        # Nous allons également rajouter les informations dont on ne dispose pas à
        # partir des résultats trouvés sur internet sur les précédents champion NBA
        nba_champions_manquant = {
            "1957-1958": "Atlanta Hawks",
            "1958-1959": "Boston Celtics",
            "1960-1961": "Boston Celtics",
            "1964-1965": "Boston Celtics",
            "1968-1969": "Boston Celtics",
            "1993-1994": "Houston Rockets",
            "1995-1996": "Chicago Bulls",
            "1999-2000": "Los Angeles Lakers",
            "2001-2002": "Los Angeles Lakers",
            "2005-2006": "Miami Heat"
        }

        for val in nba_champions_manquant.items():
            # On Vérifions qu'on est dans la bonne période
            if (
                int(val[0].split("-")[0]) >= debut_periode and
                int(val[0].split("-")[1]) <= fin_periode
            ):
                if val[1] not in equipe.keys():
                    equipe[val[1]] = 1
                else:
                    equipe[val[1]] += 1

        # Préparation de la table retournée
        table = pd.DataFrame(equipe, index=[0]).T
        table = table.reset_index()
        table = table.rename(columns={"index": "Equipe", 0: "Nombre de titre NBA"}).\
            sort_values(by="Nombre de titre NBA", ascending=False)

        # Affichange en fonction du nombre de victoire minimale
        result = table[table["Nombre de titre NBA"] >= nb_victoire_min]
        result.index = list(range(len(result)))

        return result

    def premiers_choix_draft_N_derniere_saison(self, N_saison: int = 3) -> pd.DataFrame:
        """
        Affiche les informations sur les premiers choix de la Draft NBA
        pour les N dernières saisons (par défaut 3).
        On obtient la réponse grâce aux tables 'draft_history' et 'common_player_info'

        Paramètres
        ----------
        N_saison : int = 3
            Le nombre de saisons à prendre en compte en partant de 2023 vers le passé.
            Par défaut, N_saison=3 pour afficher le n°1 des saisons 2021, 2022 et 2023.

        Returns
        -------
            result : pandas.DataFrame
                qui sont les informations des joueurs pour chaque saison :
                identifiant du joueur, saison de la draft, nom du joueur, ville de
                l'équipe ou part le joueur et pays d'origine du joueur
        """

        # Testons la quantité N_saison
        if (not (isinstance(N_saison, int) and N_saison > 0)):
            raise ValueError("L'argument N_saison doit etre un entier "
                             "strictement positif")

        dh = copy.copy(self.data["draft_history"])
        players = copy.copy(self.data["common_player_info"])

        premiers = dh[(dh["overall_pick"] == 1) & (dh["draft_type"] == "Draft")]
        premiers = premiers.merge(players[["person_id", "country"]],
                                  on="person_id", how="left")
        saisons = premiers[(premiers["season"] >= (2023 - N_saison + 1)) &
                           (premiers["season"] <= 2023)]

        result = saisons[["person_id", "season", "player_name", "team_city", "country"]]
        result = result.rename(columns={"person_id": 'Identifiant',
                                        "season": 'Saison',
                                        "player_name": 'Nom',
                                        "team_city": "Equipe",
                                        "country": 'Pays'})

        # Rajoutons le pays de Victor Wembanyama car n'est pas dans le jeu de données
        # 'common_player_info'
        result.loc[result["Identifiant"] == 1641705, "Pays"] = "France"

        return result

    def vainqueur_titre_NBA_saisons(self, debut_periode: int = 2022,
                                    fin_periode: int = 2023) -> pd.DataFrame:
        """
        Retourne l'équipe ayant remporté le le titre NBA pour une saison particulière.
        Il est également possible de préciser plus d'une saison et donc avoir le
        champion sur chaque saison.
        On obtient la réponse grâce a la table 'game'

        Parameters
        ----------
            data : dict
                    dictionnaire des tables dont la table d'intérêt est la valeur de la
                    clé 'game'
            debut_periode : int = 2022
                correspond à l'année de début de la première saison
                de la période considérée
            fin_periode : int = 2022
                correspond à l'année de fin de la dernière saison
                de la période considérée

        Returns
        --------
            pandas.DataFrame
                Un tableau contenant les équipes ayant remporté le titre NBA.
        """

        # Traitement des données
        # La fonction 'equip_victoires_defaites_saison' réalise les test sur le jeu de
        # données, la validité des année de début et de fin
        resultat = self.equip_victoires_defaites_saison(annee_debut=debut_periode,
                                                        annee_fin=fin_periode,
                                                        season_type='Playoffs')

        # Déterminons désormais les vainceurs de chaque saison
        # récupération des gagnant pour chaque saison
        max_saison = resultat.groupby("Saison").max("Nombre de victoires")
        max_saison = max_saison.reset_index()
        resultat = resultat.merge(right=max_saison, on="Saison")

        # Récupération du gagnant par saison
        resultat = resultat.loc[
            resultat["Nombre de victoires_x"] == resultat["Nombre de victoires_y"],
            ["Saison", "Equipes"]]

        # Ajoutons des champions NBA des saisons inconnu
        nba_champions_manquant = {
            "1957-1958": "Atlanta Hawks",
            "1958-1959": "Boston Celtics",
            "1960-1961": "Boston Celtics",
            "1964-1965": "Boston Celtics",
            "1968-1969": "Boston Celtics",
            "1993-1994": "Houston Rockets",
            "1995-1996": "Chicago Bulls",
            "1999-2000": "Los Angeles Lakers",
            "2001-2002": "Los Angeles Lakers",
            "2005-2006": "Miami Heat"
        }
        for saison, champion in nba_champions_manquant.items():
            ligne = pd.DataFrame([{"Saison": saison, "Equipes": champion}])
            resultat = pd.concat([resultat, ligne], ignore_index=True)

        # Récupération des saisons souhaités
        saisons = [f"{x}-{x+1}" for x in range(debut_periode, fin_periode)]
        resultat = resultat.loc[resultat["Saison"].isin(saisons)]

        resultat = resultat.sort_values("Saison")
        resultat.index = list(range(len(resultat)))

        return resultat

    def equipe_qui_remporte_N_fois_daffile_le_titre(self, N: int = 2,
                                                    debut_periode: int = 1946,
                                                    fin_periode: int = 2023
                                                    ) -> pd.DataFrame:
        """
        Retourne une liste des équipes ayant remporté au moins 2 fois d'affilé le titre
        NBA sur une période particulière.
        On obtient la réponse grâce a la table 'game'

        Parameters
        ----------
            N : int = 2
                le nombre de fois d'affilé
            debut_periode : int = 1946
                correspond à l'année de début de la première saison
                de la période considérée
            fin_periode : int = 2023
                correspond à l'année de fin de la dernière saison
                de la période considérée

        Returns
        --------
            equipe : list
                Les équipes ayant remporté au moins N fois d'affilé le titre NBA.
        """

        # Usage de la fonction 'vainqueur_titre_NBA_saisons' pour nous retourner un
        # tableau avec les vainceurs de chaque saison sur une période

        # Cette fonction réalise déja les tests sur l'objet 'data' et 'debut_période' et
        # 'fin_periode'.
        # Réalisons donc les tests sur le 'N'
        if (not (isinstance(N, int) and N > 0)):
            raise ValueError("L'argument N doit etre un entier "
                             "strictement positif")

        # Traitement
        resultat = self.vainqueur_titre_NBA_saisons(debut_periode=debut_periode,
                                                    fin_periode=fin_periode)

        # Procedons à la modification des noms de lakers et de golden state warrios
        resultat = resultat.set_index("Saison").to_dict()["Equipes"]

        # Récupération des équipes qui vérifient la conditions
        equipe = []

        best_team_last = ''
        count = 0

        for key in sorted(resultat.keys()):
            if resultat[key] == best_team_last:
                count += 1
            else:
                count = 1
                best_team_last = resultat[key]

            if count == N and resultat[key] not in equipe:
                equipe.append(resultat[key])

        return equipe

    def nombre_victoires_ou_defaites_equipe_les_N_dernieres_saisons(
            self, debut_periode: int = 2020,
            fin_periode: int = 2023, season_type: str = 'Regular Season',
            defaite: bool = False) -> pd.DataFrame:
        """
            Retourne pour les saisons de la période, les équipes ayant remporté/perdu le
            plus de match durant la saison régulière si defaite vaut False/True.
            On obtient la réponse grâce à la table 'game'

            Parameters
            ----------
                debut_periode : int = 1946
                    correspond à l'année de début de la première saison
                    de la période considérée
                fin_periode : int = 2023
                    correspond à l'année de fin de la dernière saison
                    de la période considérée
                defaite : bool = False
                    permet de préciser si nous voulons les défaites ou les victoires.
                    Si defaite = False, on obtient l'équipe avec le plus de victoires
                    et inversement

            Returns
            --------
                pandas.DataFrame
                    Un tableau contenant les équipes et le nombre de match perdu/gagné.
        """

        # Traitement des données
        # La fonction 'equip_victoires_defaites_saison' réalise les test sur le jeu de
        # données, la validité des année de début et de fin
        resultat = self.equip_victoires_defaites_saison(annee_debut=debut_periode,
                                                        annee_fin=fin_periode,
                                                        season_type=season_type,
                                                        defaite=defaite)

        # Identifions s'il s'agit de défaite ou victoire
        issu_match = 'victoires'*(1-defaite) + 'défaites'*defaite

        # Déterminons désormais l'équipe avec le plus de victoire/defaite par saison
        max_saison = resultat.groupby("Saison").max("Nombre de "+issu_match)
        max_saison = max_saison.reset_index()
        resultat = resultat.merge(right=max_saison, on="Saison", how="left")

        # Récupération du gagnant par saison
        resultat = resultat.loc[
            resultat["Nombre de "+issu_match+"_x"] == resultat[
                "Nombre de "+issu_match+"_y"],
            ["Saison", "Equipes", "Nombre de "+issu_match+"_x"]]
        resultat = resultat.rename(
            columns={"Nombre de "+issu_match+"_x": "Nombre de "+issu_match})

        resultat.index = list(range(len(resultat)))

        return resultat

    def top_N_nb_joueurs_par_pays(self, top: int = 10,
                                  graph: bool = False) -> pd.DataFrame:
        """Renvoie un tableau donnant le nombre de joueurs participant
        au championnat pour chaque pays hors USA.
        Le diagramme à barre correspondant est aussi affiché si graph=True.
        Celui-ci n'affiche que les top premiers pays, en termes de nombre
        de joueurs participant.
        On obtient la réponse grâce à la table 'common_player_info'


                Parameters
                ----------
                top : int = 10
                    permet faire un top des pays qui ont le
                    plus de joueurs participant au championnat.

                graph : bool
                    affiche le diagramme à barre s'il vaut True.

                Returns
                -------
                Dataframe
                    affiche la distibution.
        """
        if not (isinstance(top, int) and top > 0):
            raise TypeError("le nombre de pays doit etre un entier"
                            " strictement positif.")

        # testons le fait que le parametre graph est soit True soit False
        if not (isinstance(graph, bool)):
            raise ValueError("L'argument graph doit être un boolean")

        # enlever les USA
        common_player_without_usa = self.data["common_player_info"][
            self.data["common_player_info"]["country"] != 'USA']

        # nombre de joueurs pour chaque pays mentionné
        nb_joueurs_pays = common_player_without_usa["country"].value_counts()
        nb_joueurs_pays.name = 'Effectif'
        nb_joueurs_pays = nb_joueurs_pays.reset_index()
        nb_joueurs_pays.columns.values[0] = 'Pays'

        # on ne garde que le top des pays choisi par l'utilisateur
        nb_joueurs_pays_preponderant = nb_joueurs_pays[:top]
        # print(nb_joueurs_pays_preponderant.columns)
        # diagramme
        if graph:
            fig, ax = plt.subplots(figsize=(13, 6))  # Crée une figure + axe avec taille
            # plt.grid(True)
            # Création du bar plot
            ax.bar(nb_joueurs_pays_preponderant["Pays"],
                   height=nb_joueurs_pays_preponderant["Effectif"])

            # Définir les limites de l'axe Y
            ax.set_ylim(0, max(nb_joueurs_pays_preponderant["Effectif"].values) + 8)

            # Polices
            font1 = {'family': 'serif', 'color': 'black', 'size': 9}
            font2 = {'family': 'serif', 'color': 'black', 'size': 12}

            # Ajout des éléments de mise en forme
            ax.set_xlabel("Pays", fontdict=font1)
            ax.set_title("Les " + str(top) + " pays les plus représentés en NBA",
                         fontdict=font2)
            ax.set_ylabel("Effectif", fontdict=font1)
            ax.set_xticklabels(nb_joueurs_pays_preponderant["Pays"], rotation=45)

            return nb_joueurs_pays_preponderant, fig

        return nb_joueurs_pays_preponderant

    def classement_conferences(self, season: str = '2022-2023',
                               end: str = None) -> dict[pd.DataFrame]:
        """Renvoie le classement des conférences ouest et est en saison régulière.
            Il est aussi possible d'avoir le classe à une instant précis de la saison.
            On affiche par défaut la fin de la saison régulière 2022-2023 et le rang
            de toutes les équipes.
            On obtient la réponse grâce à la table 'game'

            Parameters
            ----------
                end : str = None
                    date de fin de la période
                season : str = '2022-2023'
                    la saison pour laquelle on veut un classement

            Returns
            -------
                dict(pandas.Dataframe)
                    classement de chaque conférence Est et Ouest.
        """

        if end is not None:
            if not (
                isinstance(end, str) and
                len(end) == 10 and
                len(end.split('-')) == 3 and
                len(end.split('-')[0]) == 4
            ):
                raise TypeError("La date doit être une chaîne de caractères"
                                " au format aaaa-mm-dd")

            try:
                end_date = datetime.strptime(end, "%Y-%m-%d")
            except Exception:
                raise ValueError("Erreur de format pour la date.")

        # Test sur la saison entré par l'utilisateur
        if season not in [f"{x}-{x + 1}" for x in range(1946, 2023)]:
            raise ValueError("Choisir une saison valide entre 1946-1947 et 2022-2023.")

        # Rajoutons une colonne pour la saison
        data = copy.deepcopy(self.data)
        data['game']['season_years'] = data['game']['season_id'].\
            astype(str).str[-4:].astype(int)
        data['game']['season_years'] = data['game']['season_years'].\
            apply(lambda x: f"{x}-{x + 1}")

        # Filtrons la table pour ne garder que les matchs en saison régululière
        game_regular_season = data["game"][
            data['game']['season_id'].astype(str).str.startswith("2")
        ].copy()
        # Conversion des dates
        game_regular_season["game_date"] = pd.to_datetime(
            game_regular_season["game_date"])

        # Vérifie que les dates entrées sont bien dans la saison
        game_regular_season = game_regular_season[
            game_regular_season["season_years"] == season
            ]
        min_periode = game_regular_season["game_date"].min()
        max_periode = game_regular_season["game_date"].max()

        # Vérification de la plage de dates est bien comprise dans la saison choisi
        if end is not None:
            # On va donc tester si les dates sont bonne et filter les données
            if not (
                end_date > min_periode and
                end_date <= max_periode
            ):
                raise ValueError("La plage de date sélectionné est incorrecte."
                                 f" Choisir une date entre {min_periode.date()}"
                                 f" exclu et {max_periode.date()}"
                                 " pour le classement des équipes sur la saison "
                                 f"régulière {season}.")
            else:
                # Parmis les matchs de la saison, on choisi ceux de la plage de date
                game_regular_season = game_regular_season[
                    game_regular_season["game_date"].apply(lambda x: x <= end_date)]

        # Si on a pas de date de fin, on prend tous les games de toute la saison.
        # Donc les game de 'min_periode' à 'max_periode'

        # Indiquer le vainqueur de chaque match
        game_regular_season["winner"] = np.where(
            game_regular_season["wl_home"] == "W",
            game_regular_season["team_name_home"],
            game_regular_season["team_name_away"])

        # Calcul des points

        # Equipes à domicile
        pts_home = game_regular_season.groupby("team_name_home")["pts_home"].\
            sum().reset_index()
        pts_home.columns = ["Équipe", "total_pts_home"]   # renommer

        # Equipes à l'extérieur
        pts_away = game_regular_season.groupby("team_name_away")["pts_away"].\
            sum().reset_index()
        pts_away.columns = ["Équipe", "total_pts_away"]  # renommer

        # Fusion
        total_points = pd.merge(pts_home, pts_away, on="Équipe", how="outer").fillna(0)

        # Calcul des points totaux
        total_points["Points"] = (total_points["total_pts_home"] +
                                  total_points["total_pts_away"])

        # on ne garde que les points totaux
        total_points = total_points[["Équipe", "Points"]]

        # nombre de victoires de chaque équipe
        victoires = game_regular_season["winner"].value_counts().reset_index()
        victoires.columns = ["Équipe", "Victoires"]   # renommer

        # Fusion des résultats
        resultats = pd.merge(victoires, total_points, on="Équipe", how="right").\
            fillna(0)

        # ------------- Tri par conférence --------------

        # colonne qui indique la conférence de l'équipe
        equipes_conf_est = ["Boston Celtics", "Brooklyn Nets", "New York Knicks",
                            "Philadelphia 76ers", "Toronto Raptors", "Chicago Bulls",
                            "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers",
                            "Milwaukee Bucks", "Atlanta Hawks", "Charlotte Hornets",
                            "Miami Heat", "Orlando Magic", "Washington Wizards"]

        resultats["Conférence"] = np.where(resultats["Équipe"].isin(equipes_conf_est),
                                           'Conférence est',
                                           'Conférence ouest')

        # classement conférence est
        conf_est = resultats[resultats["Conférence"] == "Conférence est"]
        conf_est = conf_est[["Équipe", "Victoires", "Points"]]
        classement_est = conf_est.sort_values(by=["Victoires", "Points"],
                                              ascending=[False, False])
        classement_est.index = range(len(classement_est))

        # classement conférence ouest
        conf_ouest = resultats[resultats["Conférence"] == "Conférence ouest"]
        conf_ouest = conf_ouest[["Équipe", "Victoires", "Points"]]
        classement_ouest = conf_ouest.sort_values(by=["Victoires", "Points"],
                                                  ascending=[False, False])
        classement_ouest.index = range(len(classement_ouest))

        classement = {"Conférence Est": classement_est,
                      "Conférence Ouest": classement_ouest}

        return classement
