from logic_for_application import HomeFunction
from logic_for_application import ReponseFunction

# from answers_class import Reponse
from logic_for_application import CareerPrediction

# from shared import data
from shiny.express import ui, render, input
from shiny.ui import page_navbar
from faicons import icon_svg
from settings import Settings
from datetime import date, timedelta
from shiny import ui as sui
from shiny import reactive
import pandas as pd
from copy import deepcopy


settings = Settings()
bg_value_box = settings.gradients["blue_green"]
ui.page_opts(
    title="Visualisation NBA : Data management",
    page_fn=page_navbar,
    fillable=True,
)

# INTERFACE HOME
with ui.nav_panel("🏠 Accueuil"):
    home = HomeFunction()
    ui.h5(
        "Infomations générales sur les joueurs et matchs NBA",
        style="font-style: italic; font-family: 'Georgia',"
        " 'Times New Roman', serif; color: gray;",
    )

    # Layout en deux colonnes : sidebar + main
    with ui.layout_sidebar():

        # --- Colonne secondaire (sidebar) ---
        with ui.sidebar(position="right", open="always"):
            with ui.value_box(
                showcase=icon_svg("trophy"),
                theme=bg_value_box,
                showcase_layout=settings.vb_showcase_layout,
                full_screen=True,
            ):
                ui.h4("Nombre total de joueurs Greatest")

                @render.text
                def display_nb_players_():
                    # print(year_range_home())
                    return (
                        f"{home.return_greatest_players(year_range_home())[1]} joueurs"
                    )

            # print(home.return_greatest_players())
            with ui.card():
                ui.card_header("Joueurs NBA Greatest")

                @render.data_frame
                def display_greatest():
                    return home.return_greatest_players(year_range_home())[0]

        # --- Colonne principale (main) ---
        # Les value_boxes et cards suivants apparaîtront à gauche
        with ui.layout_column_wrap(width=1 / 3, gap="1rem"):
            # Nombre de joueurs
            with ui.value_box(
                showcase=icon_svg("person-running"),
                theme=bg_value_box,
                showcase_layout=settings.vb_showcase_layout,
                full_screen=True,
            ):
                ui.h4("Nombre de joueurs")

                @render.text
                def display_nb_players():
                    return f"{home.return_nb_players()} joueurs"

            # Nombre d'équipes
            with ui.value_box(
                showcase=icon_svg("users"),
                theme=bg_value_box,
                showcase_layout=settings.vb_showcase_layout,
                full_screen=True,
            ):
                ui.h4("Nombre d'équipes")

                @render.text
                def display_nb_teams():
                    return f"{home.return_nb_teams()} équipes"

            # Meilleur scoreur all time
            with ui.value_box(
                showcase=icon_svg("school"),
                theme=bg_value_box,
                showcase_layout=settings.vb_showcase_layout,
                full_screen=True,
            ):
                ui.h4("Nombre d'universités")

                @render.text
                def display_best_scorer():
                    return home.nombre_univ()

        # Deux cards plein écran sous les boxes
        with ui.card(full_screen=True):
            ui.card_header("Statistiques générales")
            with ui.layout_columns(col_widths=(5, 7)):
                with ui.layout_columns(col_widths=(12, 12)):
                    ui.input_date_range(
                        id="date_plage_",
                        label="Selectionnez une plage de date pour filtrer "
                        "(Seul les années seront considéré)",
                        separator=" à ",
                        start=date(2015, 1, 1),
                        end=date(2022, 12, 31),
                        min=date(1946, 1, 1),
                        max=None,
                    )

                    @render.plot
                    def plt_ev_match():
                        return home.create_line_chart_nb_match(year_range_home())

                @render.plot
                def plt_dist_eff_position():
                    return home.create_dunut_chart_of_position_distribution(
                        year_range_home()
                    )

    @reactive.calc
    def year_range_home():
        start, end = input.date_plage_()
        if start is None or end is None:
            return None
        return (start.year, end.year)


# Reponses aux questions
with ui.nav_panel("📊🧠 Reponses aux questions"):
    reponses = ReponseFunction()  # création de l'instance
    ui.h5(
        "Reponse aux questions de notre sujet",
        style="font-style: italic; font-family: 'Georgia',"
        " 'Times New Roman', serif; color: gray;",
    )  # Titre principale de l'onglet

    with ui.navset_bar(id="selected_window", title="Résultats"):
        with ui.nav_panel(title="Analyse 1 - Joueurs"):
            with ui.layout_columns(col_widths=(3, 5, 4)):
                with ui.card(full_screen=True):
                    ui.card_header("Quelques statisques - Taille/Poids ")
                    ui.input_selectize(
                        id="stat",
                        label="Choisir une statistique",
                        selected="Minimum",
                        choices=["Minimum", "Maximum", "Médiane", "Moyenne"],
                    )

                    @render.data_frame
                    def display_stat():
                        return reponses.statistique_taille_poids(stat=input.stat())

                with ui.card(full_screen=True):
                    ui.card_header(
                        "Classement des universités selon le"
                        " nombre de joueurs évoluant en NBA"
                    )
                    with ui.layout_columns(col_widths=(12, 12)):
                        with ui.layout_columns(col_widths=(3, 3, 3, 3)):
                            # Top
                            ui.input_text(id="top_universite", label="Top N", value=10)
                            # anne_bas
                            ui.input_selectize(
                                id="debut_per_univ",
                                label="Début période",
                                selected=1947,
                                choices=[i for i in range(1947, 2024)],
                            )
                            # anne_haut
                            ui.input_selectize(
                                id="fin_per_univ",
                                label="Fin période",
                                selected=2023,
                                choices=[i for i in range(1947, 2024)],
                            )
                            # Bouton
                            ui.input_action_button(
                                "aff_univ", "Afficher", class_="btn-primary"
                            )

                    # Réalisation d'une vérification des quantités et illustration
                    @render.plot
                    @reactive.event(input.aff_univ)
                    def display_top_university():
                        # vérif top
                        try:
                            top = int(input.top_universite())

                            # vérifie de l'annee
                            if (
                                input.debut_per_univ() == ""
                                or input.fin_per_univ() == ""
                            ):
                                m = ui.modal(
                                    ("Merci de sélectionner une " "année correcte."),
                                    title="Erreur de saisie",
                                    easy_close=True,
                                )
                                ui.modal_show(m)
                            else:
                                debut = int(input.debut_per_univ())
                                fin = int(input.fin_per_univ())
                                try:
                                    resultat = reponses.prop_university(
                                        top_N=top, debut=debut, fin=fin
                                    )
                                    return resultat
                                except Exception as e:
                                    m = ui.modal(
                                        f"{e}",
                                        title="Erreur de saisie",
                                        easy_close=True,
                                    )
                                    ui.modal_show(m)
                        except Exception:
                            m = ui.modal(
                                ("Merci de saisir un entier positif pour Top N."),
                                title="Erreur de saisie",
                                easy_close=True,
                            )
                            ui.modal_show(m)

                with ui.card(full_screen=True):
                    ui.card_header("Numéro 1 de draft selon la saison")

                    with ui.layout_columns(col_widths=(12, 12)):
                        with ui.layout_columns(col_widths=(6, 6)):
                            ui.input_text(id="nb_1_draft",
                                          label=("Choisir le nombre de saison "
                                                 "antérieures"),
                                          value=8)
                            # Bouton
                            ui.input_action_button(
                                "nb_draft", "Afficher", class_="btn-primary"
                            )

                        @render.data_frame
                        @reactive.event(input.nb_draft)
                        def display_1_draft():
                            try:
                                nb = int(input.nb_1_draft())
                                return reponses.numero_1_draft(nb)
                            except Exception:
                                ui.modal_show(
                                    ui.modal(
                                        ("Merci de saisir un entier positif "
                                         "pour le nombre de saisons antérieures."),
                                        title="Erreur de saisie",
                                        easy_close=True,
                                    )
                                )
                                return None

        # Fonction utilitaire pour la vérification des argements
        def verifier_periode():
            try:

                if input.debut_per() == "" or input.fin_per() == "":
                    raise ValueError("Merci de sélectionner une " "année correcte.")

                debut = int(input.debut_per())
                fin = int(input.fin_per())

                if debut > fin:
                    raise ValueError(
                        "La date de début est postérieure à la " "date de fin."
                    )

                return debut, fin
            except Exception as e:
                ui.modal_show(
                    ui.modal(
                        str(e),
                        title="Erreur de saisie",
                        easy_close=True,
                    )
                )
                return None

        def verifier_nb_vic_minimale():
            try:
                try:
                    nb_min = int(input.min_win())
                except Exception:
                    raise ValueError(
                        "Merci de saisir un entier positif le nombre "
                        "de victoire minimale."
                    )

                return nb_min
            except Exception as e:
                ui.modal_show(
                    ui.modal(
                        str(e),
                        title="Erreur de saisie",
                        easy_close=True,
                    )
                )
                return None

        def verifier_issu_match():
            try:
                if input.isssu_match() == "":
                    raise ValueError(
                        "Merci de sélectionner entre Victoire ou " "Défaite."
                    )
                isssu_match = input.isssu_match()

                return isssu_match
            except Exception as e:
                ui.modal_show(
                    ui.modal(
                        str(e),
                        title="Erreur de saisie",
                        easy_close=True,
                    )
                )
                return None

        with ui.nav_panel(title="Analyse 2 - Equipes"):
            with ui.layout_columns(col_widths=(12, 12)):
                # with ui.card(full_screen=False):
                with ui.layout_columns(col_widths=(12, 12)):
                    ui.h5("Choisir une période d'étude")
                    with ui.layout_columns(col_widths=(4, 4, 4)):
                        # anne_bas
                        ui.input_selectize(
                            id="debut_per",
                            label="Début période",
                            selected=2019,
                            choices=[i for i in range(1946, 2024)],
                        )
                        # anne_haut
                        ui.input_selectize(
                            id="fin_per",
                            label="Fin période",
                            selected=2023,
                            choices=[i for i in range(1947, 2024)],
                        )
                        # Bouton
                        ui.input_action_button(
                            "analyse_2", "Afficher", class_="btn-primary"
                        )

                with ui.layout_columns(col_widths=(4, 4, 4)):
                    with ui.card(full_screen=True):
                        ui.card_header(
                            "Equipes qui ont remporter au moins " "N fois le titre."
                        )
                        with ui.layout_columns(col_widths=(12, 12)):
                            ui.input_text(
                                id="min_win",
                                label="Nombre de victoire minimal",
                                value=2,
                            )

                            @render.data_frame
                            @reactive.event(input.analyse_2)
                            def dysplay_min_win():
                                valeurs_periode = verifier_periode()
                                valeurs_vic_min = verifier_nb_vic_minimale()
                                if valeurs_periode is None or valeurs_vic_min is None:
                                    return pd.DataFrame()

                                debut, fin = valeurs_periode
                                nb_min = valeurs_vic_min
                                try:
                                    resultat = reponses.au_moins_N_fois_le_titre(
                                        nb_min=nb_min, debut=debut, fin=fin
                                    )
                                    return resultat
                                except Exception as e:
                                    ui.modal_show(
                                        ui.modal(
                                            str(e), title="Erreur dans les données"
                                        )
                                    )
                                    return pd.DataFrame()

                    with ui.card(full_screen=True):
                        ui.card_header("Vainceur du titre selon la saison")

                        # Si le nombre de victoire minimal fonction, aucune raison
                        # que cette fonction ne fonctionne pas
                        @render.data_frame
                        @reactive.event(input.analyse_2)
                        def dysplay_winner_saison():
                            valeurs_periode = verifier_periode()
                            if valeurs_periode is None:
                                return pd.DataFrame()

                            debut, fin = valeurs_periode
                            try:
                                resultat = reponses.remporter_titre(
                                    debut=debut, fin=fin
                                )
                                return resultat
                            except Exception as e:
                                ui.modal_show(
                                    ui.modal(str(e), title="Erreur dans les données")
                                )
                                return pd.DataFrame()

                    with ui.card(full_screen=True):
                        ui.card_header(
                            "Equipe avec le plus de victoires/défaites "
                            "en saison régulière"
                        )
                        with ui.layout_columns(col_widths=(12, 12)):
                            ui.input_selectize(
                                id="isssu_match",
                                label=("Choisissez l'issu de match " "à évaluer"),
                                selected="Victoire",
                                choices=["Victoire", "Défaite"],
                            )

                            @render.data_frame
                            @reactive.event(input.analyse_2)
                            def display_issu_match_equipe():
                                valeurs_periode = verifier_periode()
                                valeurs_issu_match = verifier_issu_match()
                                if (
                                    valeurs_periode is None
                                    or valeurs_issu_match is None
                                ):
                                    return pd.DataFrame()

                                debut, fin = valeurs_periode
                                isssu_match = valeurs_issu_match
                                try:
                                    resultat = reponses.nombre_victoires_defaites(
                                        issu_match=isssu_match, debut=debut, fin=fin
                                    )
                                    return resultat
                                except Exception as e:
                                    ui.modal_show(
                                        ui.modal(
                                            str(e), title="Erreur dans les données"
                                        )
                                    )
                                    return pd.DataFrame()

        with ui.nav_panel(title="Analyse 3 - Equipes"):
            with ui.layout_columns(col_widths=(12, 12)):
                with ui.card(full_screen=True):
                    ui.card_header(
                            "Répartition des joueurs NBA selon leur pays d'origine"
                        )
                    with ui.layout_columns(col_widths=(9, 3)):
                        with ui.layout_columns(col_widths=(12, 12)):
                            with ui.card(full_screen=True):
                                ui.input_text(id='top_n_pays',
                                              label=('Sélectionner le nombre de pays '
                                                     'à afficher dans le Top N'),
                                              value=10)

                                @render.plot
                                def ditribution_pays():
                                    if isinstance(input.top_n_pays(), str):
                                        if str(input.top_n_pays()).isdigit():
                                            top = int(input.top_n_pays())
                                            fig, _ = reponses.distribution_pays(top)
                                            return fig
                                    elif isinstance(input.top_n_pays(), int):
                                        top = int(input.top_n_pays())
                                        fig, _ = reponses.distribution_pays(top)
                                        return fig
                                    else:
                                        ui.modal_show(
                                            ui.modal(
                                                ("Merci de saisir un entier strictement"
                                                 " positif pour le nombre des "
                                                 "pays à afficher."),
                                                title="Erreur de saisie",
                                                easy_close=True,
                                            ))
                                        return None

                        @render.data_frame
                        def ditribution_pays_tab():
                            try:
                                top = int(input.top_n_pays())
                                _, tab = reponses.distribution_pays(top)
                                return tab
                            except Exception:
                                return None

                # Fonction pour la récupération des date
                @reactive.calc
                def min_max_date():
                    if not input.season_conf() == '':
                        return reponses.recup_min_max_date(input.season_conf())
                    else:
                        ui.modal_show(
                            ui.modal(
                                ("Merci de selectionner une saison."),
                                title="Erreur de saisie",
                                easy_close=True,
                            ))
                        return None

                with ui.card(full_screen=True):
                    ui.card_header(
                            "Classement des conférences est et ouest sur une saison"
                        )
                    with ui.layout_columns(col_widths=(12, 12)):
                        with ui.layout_columns(col_widths=(4, 4, 4)):
                            # season
                            ui.input_selectize(
                                id="season_conf",
                                label="Saison régulière",
                                selected='2020-2023',
                                choices=[f"{i}-{i+1}" for i in range(1946, 2023)],
                            )

                            # Possibilité de choisir une date
                            @render.ui
                            def input_date_classement():
                                if min_max_date() is not None:
                                    min_date, max_date = min_max_date()
                                    min_date = str(min_date + timedelta(days=1))
                                    max_date = str(max_date)
                                else:
                                    min_date, max_date = None, None
                                return ui.input_date(
                                    id='end_date',
                                    label=('Choisir le moment où observer le '
                                           'classement des conférences'),
                                    value=max_date,  # ou n'importe quelle date
                                    min=min_date,
                                    max=max_date)

                            # Bouton
                            ui.input_action_button(
                                "aff_conference", "Afficher", class_="btn-primary"
                            )

                        with ui.layout_columns(col_widths=(6, 6)):
                            with ui.card(full_screen=True):
                                ui.card_header(
                                        "Classement de la conférence est"
                                    )

                                @render.data_frame
                                @reactive.event(input.aff_conference)
                                def display_conf_est():
                                    if not input.season_conf() == '':
                                        resultat = reponses.display_conference(
                                            season=input.season_conf(),
                                            end=str(input.end_date())
                                        )
                                        return resultat["Conférence Est"]
                                    else:
                                        return None

                            with ui.card(full_screen=True):
                                ui.card_header(
                                        "Classement de la conférence ouest"
                                    )

                                @render.data_frame
                                @reactive.event(input.aff_conference)
                                def display_conf_ouest():
                                    if not input.season_conf() == '':
                                        resultat = reponses.display_conference(
                                            season=input.season_conf(),
                                            end=str(input.end_date())
                                        )
                                        return resultat["Conférence Ouest"]
                                    else:
                                        return None

# LINEAR MODEL
with ui.nav_panel("📈⚙️ Machine Learning"):
    career_prediction = CareerPrediction(data=home.data["common_player_info"])
    ui.h5(
        "Prédiction de la durée de carrière des joueurs de basket-ball",
        style="font-style: italic; font-family: 'Georgia',"
        " 'Times New Roman', serif; color: gray;",
    )

    with ui.layout_columns(col_widths=(12, 12)):
        # ligne du resultat du modèle ainsi que de al courbe des RMSE
        with ui.layout_columns(col_widths=(6, 6)):
            with ui.card():
                ui.card_header("Model training results")
                with ui.layout_columns(col_widths=(6, 6)):
                    ui.input_checkbox(
                        id="regression_method",
                        label="Entrainner le modèle avec la régularisation de Ridge",
                    )
                    ui.input_numeric(
                        id="alpha_value",
                        label="Entrer le coefficient de regularisation",
                        value=career_prediction.alpha,
                    )

                @render.data_frame
                def display_model_result():
                    res = fit_model()["results"]["estimation_results"]
                    # afficher les postes en francais
                    poste_mapping = {
                        'position_Center-Forward': 'Pivot-Ailier fort',
                        'position_Forward': 'Ailier',
                        'position_Forward-Center': 'Ailier fort-Pivot',
                        'position_Forward-Guard': 'Ailier-Arrière',
                        'position_Guard': 'Arrière',
                        'position_Guard-Forward': 'Arrière-Ailier'
                    }
                    res['Variable'] = res['Variable'].replace(poste_mapping)
                    return res

            with ui.card():
                ui.card_header("Validation du modèle : Courbe des RMSE (k-fold)")

                @render.plot
                def plot_rmse():
                    fit_model()["new_model"].plot_k_fold()

            @reactive.calc
            def fit_model():
                # import time
                method = input.regression_method()
                alpha = input.alpha_value()
                career_prediction.use_ridge = False

                if method == "Ridge":
                    career_prediction.use_ridge = True
                    career_prediction.alpha = alpha

                results = career_prediction.run_regression()
                return {"results": results, "new_model": career_prediction}

        with ui.layout_columns(col_widths=(6, 6)):  # Deux colonnes (gauche et droite)
            with ui.card():  # Carte pour la section Prédiction
                ui.card_header("Prediction")  # En-tête de la carte

                # Deux colonnes côte à côte : gauche = dates, droite = position + bouton
                with ui.layout_columns(col_widths=(6, 6)):

                    # Colonne gauche : les deux dates
                    with ui.card():
                        ui.input_date(
                            id="birth_date",
                            label="Entrer la date de naissance du joeurs"
                            " drafté (année considérée)",
                            min=date(1900, 1, 1),
                        )
                        ui.input_date(
                            id="draft_date",
                            label="Entrer la date de draft (année considérée)",
                            min=date(1946, 1, 1),
                        )

                    # Colonne droite : position + bouton
                    with ui.card():  # Optionnel : idem pour un encadrement
                        poste_mapping = {
                            'Center': 'Pivot',
                            'Forward': 'Ailier',
                            'Forward-Center': 'Ailier fort-Pivot',
                            'Center-Forward': 'Pivot-Ailier fort',
                            'Forward-Guard': 'Ailier-Arrière',
                            'Guard': 'Arrière',
                            'Guard-Forward': 'Arrière-Ailier'
                        }

                        raw_positions = (
                            deepcopy(home.data["common_player_info"])
                            .dropna(subset=["position"])["position"]
                            .unique()
                        )

                        choices = {
                            pos: poste_mapping.get(pos, pos) for pos in raw_positions
                        }

                        ui.input_select(
                            id="position",
                            label="Selectionner le poste du joeur",
                            selected="Center",
                            choices=choices,
                        )
                        ui.input_action_button("go", "Predire", class_="btn-primary")

            with ui.card():  # Carte pour afficher les résultats (colonne de droite)
                ui.card_header("Résultats de la prédiction")  # En-tête de la carte

                # Affichage des résultats de la prédiction
                sui.output_ui(id="prediction_results_display")

                # update réactive du résultat de la prédiction
                # lors du clic sur le bouton
                @render.ui
                @reactive.event(input.go)  # Déclenchement à partir du bouton 'go'
                def prediction_results_display_():
                    birthdate = input.birth_date()
                    draftdate = input.draft_date()
                    position = str(input.position())
                    if birthdate >= draftdate:
                        m = ui.modal(
                            "La date de naissance ne peut pas"
                            " être après celle de draft",
                            title="Dates invalides",
                            easy_close=True,
                        )
                        ui.modal_show(m)
                    else:
                        results = career_prediction.predict_career_duration(
                            birthdate=str(birthdate),
                            draft_year=str(draftdate),
                            position=position,
                            coef_df=career_prediction.run_regression()[
                                "estimation_results"
                            ],
                        )
                        predicted_duration = results["duree_predite"]
                        lower_bound = results["intervalle_confiance"][0]
                        upper_bound = results["intervalle_confiance"][1]
                        return ui.markdown(
                            f"""
                            ## Résultat de la prédiction

                            - 🏀 **Durée de carrière prédite :
                            {predicted_duration:.1f} ans**
                            - 📉 **Intervalle de confiance : [{lower_bound:.1f}
                            – {upper_bound:.1f}] ans**
                            """
                        )


# DARK OR LIGHT MODE
ui.nav_spacer()
with ui.nav_control():
    ui.input_dark_mode(id="mode")


@reactive.effect
@reactive.event(input.make_light)
def _():
    ui.update_dark_mode("light")


@reactive.effect
@reactive.event(input.make_dark)
def _():
    ui.update_dark_mode("dark")
