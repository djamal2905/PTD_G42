from application import shared
from pypalettes import load_cmap
import matplotlib.pyplot as plt
from copy import deepcopy
import matplotlib
import pandas as pd


class HomeFunction:
    def __init__(self, data_: dict[pd.DataFrame] = shared.data):
        self.data = deepcopy(data_)
        self.palettes = load_cmap("Abbott")

    def create_line_chart_nb_match(self,
                                   year_range: (str, str) = None
                                   ) -> matplotlib.figure.Figure:
        """
        Retourne un graphique de l'évolution du nombre de rencontres NBA par saison,
        avec une option de filtrage par plage d'années.

        Cette méthode regroupe les données par saison, compte le nombre de rencontres,
        puis trace un graphique en ligne avec Matplotlib, filtré par année si spécifié.

        Parameters
        ----------
        self : object
            Instance de la classe contenant les attributs `self.data['game']` et
            `self.data['game_summary']`, qui doivent être des DataFrames pandas.

        year_range : tuple, optional
            Un tuple (année_début, année_fin) pour filtrer les données. Si non spécifié,
            toutes les données sont utilisées.

        Returns
        -------
        fig : matplotlib.figure.Figure
            L'objet figure représentant le graphique, sans affichage automatique.
        """
        # Si une plage d'années est donnée, filtrer les données
        filtered_data = self.data["game"]
        filtered_data["all_seasons_combined"] = filtered_data["season_id"].apply(
            lambda x: int(str(x)[-4:])
        )
        if year_range:
            start_year, end_year = year_range
            if start_year > end_year:
                raise ValueError(
                    "La date de début ne peut pas être après la date de fin"
                )

            # Filtrer les matchs en fonction des années
            filtered_data = filtered_data[
                (filtered_data["all_seasons_combined"] >= start_year)
                & (filtered_data["all_seasons_combined"] <= end_year)
            ]
        else:
            # Si aucune plage d'années n'est donnée, utiliser toutes les données
            pass

        # Agrégation des données pour compter les matchs par saison
        nb_match_par_saison = (
            filtered_data.groupby(["all_seasons_combined"])  # Groupement par saison
            .agg({"game_id": "count"})  # Comptage des matchs
            .reset_index()
        )

        # Renommage des colonnes pour plus de clarté
        nb_match_par_saison.rename(
            columns={"all_seasons_combined": "Saisons", "game_id": "Nombre de matchs"},
            inplace=True,
        )

        # Création du graphique
        fig, ax = plt.subplots(figsize=(10, 5))

        # Tracé du graphique en ligne
        ax.plot(
            nb_match_par_saison["Saisons"],  # Axe des X : saisons
            nb_match_par_saison["Nombre de matchs"],  # Axe des Y : nombre de matchs
            marker="o",  # Ajouter un marqueur pour chaque point
            color="limegreen",  # Couleur des points
        )

        # Titres et labels
        ax.set_title("Évolution du nombre de matchs par saison")
        ax.set_xlabel("Saison")
        ax.set_ylabel("Nombre de matchs")
        ax.grid(True)  # Affichage de la grille
        plt.xticks(rotation=45)  # Rotation des labels de l'axe X
        plt.tight_layout()  # Ajustement du layout pour éviter les chevauchements

        return fig

    def create_dunut_chart_of_position_distribution(self,
                                                    year_range: (str, str) = None
                                                    ) -> matplotlib.figure.Figure:
        """
        Crée un graphique donut de la répartition des positions,
        filtré par année si spécifiée.

        Parameters
        ----------
        year_range : tuple, optional
            (année_début, année_fin) pour filtrer les données.

        Returns
        -------
        fig : matplotlib.figure.Figure
        """
        if year_range:
            # print("YEIKBDD : =================================", year_range)
            start_year, end_year = year_range
            if start_year > end_year:
                raise ValueError(
                    "La date de début ne peut pas être après la date de fin"
                )
            filtered_data = self.data["common_player_info"][
                (self.data["common_player_info"]["from_year"] >= start_year)
                & (self.data["common_player_info"]["to_year"] <= end_year)
            ].dropna(subset=["position"])
        else:
            filtered_data = self.data["common_player_info"].dropna(subset=["position"])

        result = filtered_data.groupby("position").size()
        labels = result.index.tolist()
        values = result.values.tolist()
        colors = self.palettes.colors[: len(labels)]

        fig, ax = plt.subplots()
        ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.4),
            labeldistance=0.95,
        )
        if year_range:
            ax.set_title(f"Répartition des common players par position {year_range}")
        else:
            ax.set_title("Répartition des common players par position")
        ax.axis("equal")

        return fig

    # def stats_non_basket_fan(self) -> int:
    #     nombre_de_ville = len(self.data["team_details"].loc[:, "city"].unique())
    #     return nombre_de_ville

    def nombre_univ(self) -> int:
        data_draft = self.data["draft_history"][
            (self.data["draft_history"]["draft_type"] == 'Draft') &
            (self.data["draft_history"]["organization_type"] == 'College/University') &
            (self.data["draft_history"]["overall_pick"] != 0)]

        nombre_univ = len(data_draft["organization"].unique())
        return nombre_univ

    def return_greatest_players(self,
                                year_range: (str, str) = None
                                ) -> (pd.DataFrame, int):
        """
        Retourne les meilleurs joueurs (flag Y), filtrés selon une plage d'années.

        Parameters
        ----------
        year_range : tuple, optional
            (année_début, année_fin) pour filtrer les données.

        Returns
        -------
        tuple (pd.DataFrame, int)
        """
        if year_range:
            start_year, end_year = year_range
            if start_year > end_year:
                raise ValueError(
                    "La date de début ne peut pas être après la date de fin"
                )
            data_filtered = (
                self.data["common_player_info"]
                .loc[
                    (self.data["common_player_info"]["to_year"] >= start_year)
                    & (self.data["common_player_info"]["from_year"] <= end_year)
                    & (self.data["common_player_info"]["greatest_75_flag"] == "Y"),
                    ["first_name", "last_name"],
                ]
                .rename(columns={"first_name": "Prénom", "last_name": "Nom"})
            )
            return data_filtered, data_filtered.shape[0]

        else:
            data_filtered = (
                self.data["common_player_info"]
                .loc[
                    self.data["common_player_info"]["greatest_75_flag"] == "Y",
                    ["first_name", "last_name"],
                ]
                .rename(columns={"first_name": "Prénom", "last_name": "Nom"})
            )
            return data_filtered, data_filtered.shape[0]

    def return_nb_players(self) -> int:
        return self.data["player"].shape[0]

    def return_nb_teams(self) -> int:
        return self.data["team"].shape[0]

    def return_data_home(self) -> dict[pd.DataFrame]:
        return self.data
