from answers_class import Reponse
from application import shared
from pypalettes import load_cmap
import pandas as pd
import matplotlib

# Dans ce dossier, nous allons implémenter les fonction qui vont servir à la
# réalisation des visualisations de l'interface


class ReponseFunction:
    def __init__(self, data_: dict[pd.DataFrame] = shared.data):  # (donnéesHarmonisées)
        self.reponses = Reponse(data_)
        self.palettes = load_cmap("Abbott")

    def prop_university(self, top_N: int, debut: int,
                        fin: int) -> matplotlib.figure.Figure:
        """
        Illustrer un graphique avec la distribution des joueurs NBA selon
        l'université de formation
        """
        # Traitement par rapport aux entrés
        if debut == fin:
            periode = None
            annee_draft = debut
        else:
            periode = str(debut)+'-'+str(fin)
            annee_draft = None

        # récupération des données
        tab, fig = self.reponses.prop_joueurs_en_nba_selon_universite_de_formation(
            top_N=top_N,
            annee_draft=annee_draft,
            periode=periode,
            graph=True)

        return fig

    def statistique_taille_poids(self, stat: str) -> pd.DataFrame:
        """
        Réaliser une statistique souhaité sur la taille et le poids selon
        le poste des joueurs en NBA
        """
        associer = {"Minimum": "Min", 'Maximum': "Max",
                    "Médiane": "Median", "Moyenne": "Mean"
                    }

        resultat = self.reponses.stat_sur_taille_et_poids_par_poste(
            statistique=associer[stat])
        return resultat

    def au_moins_N_fois_le_titre(self, nb_min: int,
                                 debut: int, fin: int) -> pd.DataFrame:
        resultat = self.reponses.equipe_remporte_au_moins_N_fois_le_titre(
            debut_periode=debut,
            fin_periode=fin,
            nb_victoire_min=nb_min)

        return resultat

    def remporter_titre(self, debut: int, fin: int) -> pd.DataFrame:
        resultat = self.reponses.vainqueur_titre_NBA_saisons(
            debut_periode=debut,
            fin_periode=fin)

        return resultat

    def nombre_victoires_defaites(self, debut: int,
                                  fin: int, issu_match: str) -> pd.DataFrame:
        issu = {'Victoire': False,
                'Défaite': True}

        resultat = self.reponses.\
            nombre_victoires_ou_defaites_equipe_les_N_dernieres_saisons(
                debut_periode=debut,
                fin_periode=fin,
                defaite=issu[issu_match])

        return resultat

    def numero_1_draft(self, nb: int) -> pd.DataFrame:
        return self.reponses.premiers_choix_draft_N_derniere_saison(N_saison=nb)

    def distribution_pays(self, top_N) -> (matplotlib.figure.Figure, pd.DataFrame):
        result, fig = self.reponses.top_N_nb_joueurs_par_pays(top=top_N, graph=True)
        return fig, result

    def recup_min_max_date(self, season: str) -> (str, str):

        # Selection du mix et du max
        game_regular_season = self.reponses.data["game"][
            self.reponses.data['game']['season_id'].astype(str).str.startswith("2")
        ].copy()
        game_regular_season["season_years"] = game_regular_season['season_id'].\
            astype(str).str[-4:].astype(int).\
            apply(lambda x: f"{x}-{x + 1}")
        game_regular_season["game_date"] = pd.to_datetime(
            game_regular_season["game_date"])

        # Vérifie que les dates entrées sont bien dans la saison
        game_regular_season = game_regular_season[
            game_regular_season["season_years"] == season
            ]
        min_periode = game_regular_season["game_date"].min()
        max_periode = game_regular_season["game_date"].max()

        return (min_periode.date(), max_periode.date())

    def display_conference(self, season: str, end: str) -> dict[pd.DataFrame]:
        return self.reponses.classement_conferences(season=season,
                                                    end=end)
