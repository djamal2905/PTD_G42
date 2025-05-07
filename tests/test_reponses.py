from answers_class import Reponse
import pytest
import re
import pandas as pd
import matplotlib

# ------------- Création de la fixture --------------------------


@pytest.fixture
def get_data():
    val_df = pd.DataFrame([
        # Saison régulière pour A
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},

        # Saison pré-saison pour A
        {"season_id": "12022", "season_type": "Pre Season", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "12022", "season_type": "Pre Season", "wl_home": "L",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "12022", "season_type": "Pre Season", "wl_home": "L",
         "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        {"season_id": "12022", "season_type": "Pre Season", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        {"season_id": "12022", "season_type": "Pre Season", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "12022", "season_type": "Pre Season", "wl_home": "W",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},

        # Saison Playoffs pour A (Pas de rencontres ici)
        {"season_id": "42022", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "42022", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "42022", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        {"season_id": "42022", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        {"season_id": "42022", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "42022", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},

        # Playoffs saison 2021
        {"season_id": "42021", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "42021", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "42021", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        {"season_id": "42021", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        {"season_id": "42021", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "42021", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},

        # Playoffs saison 2020
        {"season_id": "42020", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "42020", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "42020", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        {"season_id": "42020", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        {"season_id": "42020", "season_type": "Playoffs", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "42020", "season_type": "Playoffs", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},

        # Saison tous types pour B
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "22022", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},

        # Saison régulière pour 2021
        {"season_id": "22021", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe B", "team_name_away": "Equipe A"},
        {"season_id": "22021", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe C"},
        {"season_id": "22021", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe A"},
        {"season_id": "22021", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe A", "team_name_away": "Equipe B"},
        {"season_id": "22021", "season_type": "Regular Season", "wl_home": "W",
         "team_name_home": "Equipe B", "team_name_away": "Equipe C"},
        {"season_id": "22021", "season_type": "Regular Season", "wl_home": "L",
         "team_name_home": "Equipe C", "team_name_away": "Equipe B"},
     ])

    player_info = pd.DataFrame([
        {"person_id": 10001, "display_first_last": "Joueur1", "school": "UCLA",
         "country": "USA", "height": "6-7", "weight": 210.0, "position": "Guard"},
        {"person_id": 10002, "display_first_last": "Joueur2", "school": "Duke",
         "country": "USA", "height": "6-9", "weight": 230.0, "position": "Forward"},
        {"person_id": 10003, "display_first_last": "Joueur3", "school": "UCLA",
         "country": "USA", "height": "7-0", "weight": 245.0, "position": "Center"},
        {"person_id": 10004, "display_first_last": "Joueur4", "school": "Michigan",
         "country": "USA", "height": "6-5", "weight": 200.0, "position": "Guard"},
        {"person_id": 10005, "display_first_last": "Joueur5", "school": "Duke",
         "country": "USA", "height": "6-11", "weight": 240.0,
         "position": "Forward-Center"},
        {"person_id": 10006, "display_first_last": "Joueur6", "school": "UCLA",
         "country": "USA", "height": "6-10", "weight": 235.0, "position": "Forward"},
        {"person_id": 10007, "display_first_last": "Joueur7",
         "school": "North Carolina",
         "country": "USA", "height": "6-6", "weight": 215.0,
         "position": "Guard-Forward"},
        {"person_id": 10008, "display_first_last": "Joueur8", "school": "Duke",
         "country": "Canada", "height": "6-8", "weight": 225.0, "position": "Forward"},
        {"person_id": 10009, "display_first_last": "Joueur9", "school": "Michigan",
         "country": "USA", "height": "7-1", "weight": 250.0, "position": "Center"},
        {"person_id": 10010, "display_first_last": "Joueur10",
         "school": "Florida State",
         "country": "USA", "height": "6-4", "weight": 190.0, "position": "Guard"},
    ])

    draft = pd.DataFrame([{
        'person_id': 10001,
        'player_name': 'Joueur1',
        'season': 2022,
        'round_number': 1,
        'round_pick': 5,
        'overall_pick': 5,
        'draft_type': 'Draft',
        'team_id': 1610612737,
        'team_city': 'Atlanta',
        'team_name': 'Hawks',
        'team_abbreviation': 'ATL',
        'organization': 'UCLA',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10002,
        'player_name': 'Joueur2',
        'season': 2021,
        'round_number': 1,
        'round_pick': 3,
        'overall_pick': 3,
        'draft_type': 'Draft',
        'team_id': 1610612744,
        'team_city': 'Golden State',
        'team_name': 'Warriors',
        'team_abbreviation': 'GSW',
        'organization': 'Duke',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10003,
        'player_name': 'Joueur3',
        'season': 2020,
        'round_number': 1,
        'round_pick': 8,
        'overall_pick': 8,
        'draft_type': 'Draft',
        'team_id': 1610612755,
        'team_city': 'Philadelphia',
        'team_name': '76ers',
        'team_abbreviation': 'PHI',
        'organization': 'UCLA',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10004,
        'player_name': 'Joueur4',
        'season': 2023,
        'round_number': 2,
        'round_pick': 4,
        'overall_pick': 34,
        'draft_type': 'Draft',
        'team_id': 1610612740,
        'team_city': 'New Orleans',
        'team_name': 'Pelicans',
        'team_abbreviation': 'NOP',
        'organization': 'Michigan',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10005,
        'player_name': 'Joueur5',
        'season': 2019,
        'round_number': 1,
        'round_pick': 2,
        'overall_pick': 2,
        'draft_type': 'Draft',
        'team_id': 1610612757,
        'team_city': 'Portland',
        'team_name': 'Trail Blazers',
        'team_abbreviation': 'POR',
        'organization': 'Duke',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10006,
        'player_name': 'Joueur6',
        'season': 2022,
        'round_number': 1,
        'round_pick': 7,
        'overall_pick': 7,
        'draft_type': 'Draft',
        'team_id': 1610612761,
        'team_city': 'Toronto',
        'team_name': 'Raptors',
        'team_abbreviation': 'TOR',
        'organization': 'UCLA',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10007,
        'player_name': 'Joueur7',
        'season': 2021,
        'round_number': 2,
        'round_pick': 12,
        'overall_pick': 42,
        'draft_type': 'Draft',
        'team_id': 1610612739,
        'team_city': 'Cleveland',
        'team_name': 'Cavaliers',
        'team_abbreviation': 'CLE',
        'organization': 'North Carolina',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10008,
        'player_name': 'Joueur8',
        'season': 2020,
        'round_number': 1,
        'round_pick': 10,
        'overall_pick': 10,
        'draft_type': 'Draft',
        'team_id': 1610612747,
        'team_city': 'Los Angeles',
        'team_name': 'Lakers',
        'team_abbreviation': 'LAL',
        'organization': 'Duke',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10009,
        'player_name': 'Joueur9',
        'season': 2023,
        'round_number': 1,
        'round_pick': 1,
        'overall_pick': 1,
        'draft_type': 'Draft',
        'team_id': 1610612763,
        'team_city': 'Memphis',
        'team_name': 'Grizzlies',
        'team_abbreviation': 'MEM',
        'organization': 'Michigan',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }, {
        'person_id': 10010,
        'player_name': 'Joueur10',
        'season': 2019,
        'round_number': 2,
        'round_pick': 20,
        'overall_pick': 50,
        'draft_type': 'Draft',
        'team_id': 1610612752,
        'team_city': 'New York',
        'team_name': 'Knicks',
        'team_abbreviation': 'NYK',
        'organization': 'Florida State',
        'organization_type': 'College/University',
        'player_profile_flag': 1
    }])

    dict_of_df = {
        "game": val_df,
        'common_player_info': player_info,
        'draft_history': draft
    }

    return dict_of_df

# ------------- Test qui créés une erreur à la création de l'instance -------


@pytest.mark.parametrize(
    'df, erreur, message',
    [
        ([1, 2, 3], TypeError, "L'argument data doit être un dictionnaire."),
        ("Data", TypeError, "L'argument data doit être un dictionnaire."),
        ({1, 2, 3}, TypeError, "L'argument data doit être un dictionnaire."),
        ({1: [2, 3]}, TypeError, "Toutes les valeurs des clés doivents être des "
                                 "pandas.DataFrame."),
        ({1: [2, 3], "a": pd.DataFrame([{'cle': 'val'}])}, TypeError,
         "Toutes les valeurs des clés doivents être des pandas.DataFrame."),
        (
            {1: [2, 3],
             "a": pd.DataFrame([{'cle': 'val'}])},
            TypeError,
            "Toutes les valeurs des clés doivents être des pandas.DataFrame."
        ),
        (
            {1: pd.DataFrame([{'cle': 'val'}]),
             "a": pd.DataFrame([{'cle': 'val'}])},
            KeyError, "La clé 'draft_history' ne fait pas parti du dictionnaire"
        ),
        (
            {'draft_history': pd.DataFrame([{'cle': 'val'}]),
             "a": pd.DataFrame([{'cle': 'val'}])},
            KeyError, "La clé 'common_player_info' ne fait pas parti du dictionnaire"
        ),
        (
            {'draft_history': pd.DataFrame([{'cle': 'val'}]),
             "common_player_info": pd.DataFrame([{'cle': 'val'}])},
            KeyError, "La clé 'game' ne fait pas parti du dictionnaire"
        ),
    ]
)
def test_erreur_creation_instance(df, erreur, message):
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        Reponse(df)

# ------------- Test qui soulève pas d'erreur à la création de l'instance -------


@pytest.mark.parametrize(
    'df, resultat',
    [
        (None, True),
        (None, True)
    ]
)
def test_creation_instance(get_data, df, resultat):
    df = get_data
    reponses = Reponse(df)
    assert all(val in reponses.data.keys() for val in ["game", 'common_player_info',
                                                       'draft_history']) == resultat


# -------------- Test sur les méthodes en vérifiant les erreurs ---------------


@pytest.mark.parametrize(
    "param, erreur, message",
    [(
        {"annee_debut": 2022,
         "annee_fin": '2023'},
        TypeError,
        "Les dates de début et de fin doivent être des entiers."
    ), (
        {"annee_debut": '2022',
            "annee_fin": 2023},
        TypeError,
        "Les dates de début et de fin doivent être des entiers."
    ), (
        {"annee_debut": 1903,
            "annee_fin": 2010},
        ValueError,
        "La période sélectionnée doit être comprise entre 1946 inclu"
        " et 2023 inclu."
    ), (
        {"annee_debut": 1950,
         "annee_fin": 2025},
        ValueError,
        "La période sélectionnée doit être comprise entre 1946 inclu"
        " et 2023 inclu."
    ), (
        {"annee_debut": 2010,
         "annee_fin": 2009},
        ValueError,
        "La date de début ne peut pas excéder ou être égale à "
        "la date de fin."
    ), (
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "season_type": "Autre saison"},
        ValueError,
        "Le type de saison sélectionné doit être une des valeurs "
        "suivantes : Regular Season, Pre Season, All-Star, Playoffs"
    ), (
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "season_type": "Playoffs",
         "defaite": 10},
        TypeError,
        "L'argument defaite doit être de type booléen (True or False)"
    )]
)
def test_erreur_equip_victoires_defaites_saison(get_data, param, erreur, message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.equip_victoires_defaites_saison(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'top_N': 'ababa'}, ValueError,
            "L'argument top_N doit etre un entier strictement positif"
        ),
        (
            {'top_N': -10}, ValueError,
            "L'argument top_N doit etre un entier strictement positif"
            ),
        (
            {'top_N': 5,
             'annee_draft': 2020,
             'periode': '2019-2022'}, ValueError,
            (
                "Entrez soit une année soit une période. Donc mettre soit"
                " le paramètre annee_draft à None soit le paramètre période à None"
            )
        ),
        (
            {'top_N': 5,
             'annee_draft': '2020'}, ValueError,
            (
                "L'année de la draft est un entier compris entre 1947 et 2023"
            )
        ),
        (
            {'top_N': 5,
             'periode': '2019/2025'}, ValueError,
            (
                "L'argument periode est incorrecte. Un exemple de "
                "valeur possible est '2012-2015'"
            )
        ),
        (
            {'top_N': 5,
             'periode': '2aa9-2bb5'}, ValueError,
            (
                "Les années de début et de fin de la période doivent"
                " être des entiers."
            )
        ),
        (
            {'top_N': 5,
             'periode': '2022-2025'}, ValueError,
            (
                "La période considéré n'est pas existante. Choisir une"
                " période entre 1947 et 2023 inclu"
            )
        ),
        (
            {'top_N': 5,
             'periode': '2000-2003',
             'graph': "vrai"}, ValueError,
            (
                "L'argument graph doit être un boolean"
            )
        )
    ]
)
def test_erreur_prop_joueurs_en_nba_selon_universite_de_formation(get_data, param,
                                                                  erreur, message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.prop_joueurs_en_nba_selon_universite_de_formation(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'statistique': 'ababa'}, ValueError,
            ("L'argument statistique doit prendre une des valeurs"
             " suivantes : Mean, Max, Min, Median")
        ),
        (
            {'statistique': 'moyenne'}, ValueError,
            ("L'argument statistique doit prendre une des valeurs"
             " suivantes : Mean, Max, Min, Median")
        ),
        (
            {'poste': 'autreposte'}, ValueError,
            ("L'argument poste est incorrecte. Veuillez choisir "
             "une valeur existante : Pivot, Pivot/Ailier fort,"
             " Ailier, Ailier fort/Pivot, Ailier/Meneur,"
             " Arrière/Meneur, Arrière/Ailier")
        ),
        (
            {'poste': 'pivot'}, ValueError,
            ("L'argument poste est incorrecte. Veuillez choisir "
             "une valeur existante : Pivot, Pivot/Ailier fort,"
             " Ailier, Ailier fort/Pivot, Ailier/Meneur,"
             " Arrière/Meneur, Arrière/Ailier")
        )
    ]
)
def test_erreur_stat_sur_taille_et_poids_par_poste(get_data, param, erreur, message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.stat_sur_taille_et_poids_par_poste(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'nb_victoire_min': 'ababa'}, ValueError,
            ("L'argument nb_victoire_min doit etre un entier "
             "strictement positif")
        ),
        (
            {'nb_victoire_min': -5}, ValueError,
            ("L'argument nb_victoire_min doit etre un entier "
             "strictement positif")
        ),
        (
            {'nb_victoire_min': [1, 2]}, ValueError,
            ("L'argument nb_victoire_min doit etre un entier "
             "strictement positif")
        ),
        (
            {'nb_victoire_min': 5, 'debut_periode': "2006"}, TypeError,
            ("Les dates de début et de fin doivent être des entiers.")
        ),
        (
            {'nb_victoire_min': 5, 'debut_periode': 2006,
             'fin_periode': "2022"}, TypeError,
            ("Les dates de début et de fin doivent être des entiers.")
        ),
        (
            {'nb_victoire_min': 5, 'debut_periode': 1900,
             'fin_periode': 2022}, ValueError,
            ("La période sélectionnée doit être comprise entre 1946 inclu "
             "et 2023 inclu.")
        ),
        (
            {'nb_victoire_min': 5, 'debut_periode': 2012,
             'fin_periode': 2000}, ValueError,
            ("La date de début ne peut pas excéder ou être égale à la date de fin.")
        )
    ]  # Les test sur les quantité debut_période et fin_periode sont tester dirrectement
    # dans la sous  fonction
)
def test_erreur_equipe_remporte_au_moins_N_fois_le_titre(get_data, param, erreur,
                                                         message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.equipe_remporte_au_moins_N_fois_le_titre(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'N_saison': 'ababa'}, ValueError,
            ("L'argument N_saison doit etre un entier "
             "strictement positif")
        ),
        (
            {'N_saison': -5}, ValueError,
            ("L'argument N_saison doit etre un entier "
             "strictement positif")
        ),
        (
            {'N_saison': [1, 2]}, ValueError,
            ("L'argument N_saison doit etre un entier "
             "strictement positif")
        )
    ]
)
def test_erreur_premiers_choix_draft_N_derniere_saison(get_data, param, erreur,
                                                       message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.premiers_choix_draft_N_derniere_saison(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'debut_periode': "2006"}, TypeError,
            ("Les dates de début et de fin doivent être des entiers.")
        ),
        (
            {'debut_periode': 2006,
             'fin_periode': "2022"}, TypeError,
            ("Les dates de début et de fin doivent être des entiers.")
        ),
        (
            {'debut_periode': 1900,
             'fin_periode': 2022}, ValueError,
            ("La période sélectionnée doit être comprise entre 1946 inclu "
             "et 2023 inclu.")
        ),
        (
            {'debut_periode': 2012,
             'fin_periode': 2000}, ValueError,
            ("La date de début ne peut pas excéder ou être égale à la date de fin.")
        )
    ]
)
def test_erreur_vainqueur_titre_NBA_saisons(get_data, param, erreur,
                                            message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.vainqueur_titre_NBA_saisons(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [

        (
            {'N': 'hello'}, ValueError,
            ("L'argument N doit etre un entier "
             "strictement positif")
        ),
        (
            {'N': -5}, ValueError,
            ("L'argument N doit etre un entier "
             "strictement positif")
        ),
        (
            {'N': [1, 2]}, ValueError,
            ("L'argument N doit etre un entier "
             "strictement positif")
        ),
        # De meme les test sur les quantité defaite et fin_periode sont tester
        # directement dans la sous fonction equip_victoires_defaites_saison
        (
            {'N': 3, 'debut_periode': 2006,
             'fin_periode': "2022"}, TypeError,
            ("Les dates de début et de fin doivent être des entiers.")
        )
    ]
)
def test_erreur_equipe_qui_remporte_N_fois_daffile_le_titre(get_data, param, erreur,
                                                            message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.equipe_qui_remporte_N_fois_daffile_le_titre(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        # De meme les test sur les quantités debut_periode, fin_periode,
        # defaite et season_type sont testées
        # directement dans la sous fonction equip_victoires_defaites_saison
        (
            {'debut_periode': 2020,
             'fin_periode': 2023, 'season_type': "Autre texte"}, ValueError,
            ("Le type de saison sélectionné doit être une des valeurs "
             "suivantes : Regular Season, Pre Season, All-Star, Playoffs")
        ),
        (
            {'debut_periode': 2020,
             'fin_periode': 2023, 'season_type': ['Regular Season']}, ValueError,
            ("Le type de saison sélectionné doit être une des valeurs "
             "suivantes : Regular Season, Pre Season, All-Star, Playoffs")
        ),
        (
            {'debut_periode': 2020,
             'fin_periode': 2023, 'defaite': 1900}, TypeError,
            ("L'argument defaite doit être de type booléen (True or False)")
        )
    ]
)
def test_erreur_nombre_victoires_ou_defaites_equipe_les_N_dernieres_saisons(
        get_data, param, erreur, message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.nombre_victoires_ou_defaites_equipe_les_N_dernieres_saisons(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'top': 'ababa'}, TypeError,
            "le nombre de pays doit etre un entier strictement positif."
        ),
        (
            {'top': -10}, TypeError,
            "le nombre de pays doit etre un entier strictement positif."
        ),
        (
            {'top': 0}, TypeError,
            "le nombre de pays doit etre un entier strictement positif."
        ),
        (
            {'top': 10,
             'graph': "Ok"}, ValueError,
            "L'argument graph doit être un boolean"
        ),
        (
            {'top': 5,
             'graph': 2}, ValueError,
            "L'argument graph doit être un boolean"
        ),
    ]
)
def test_erreur_top_N_nb_joueurs_par_pays(get_data, param,
                                          erreur, message):
    df = get_data
    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.top_N_nb_joueurs_par_pays(**param)


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {'season': '202-2021'}, ValueError,
            "Choisir une saison valide entre 1946-1947 et 2022-2023."
        ),
        (
            {'season': '2023-2024'}, ValueError,
            "Choisir une saison valide entre 1946-1947 et 2022-2023."
        ),
        (
            {'season': '2022-2023', 'end': '2023-06-09'},
            ValueError,
            "La plage de date sélectionné est incorrecte. Choisir une date entre "
            "2022-10-30 exclu et 2023-04-18 pour le classement des équipes sur la "
            "saison régulière 2022-2023."
        ),
        (
            {'season': '2022-2023', 'end': '2022-10-30'},
            ValueError,
            "La plage de date sélectionné est incorrecte. Choisir une date entre "
            "2022-10-30 exclu et 2023-04-18 pour le classement des équipes sur la "
            "saison régulière 2022-2023."
        ),
        (
            {'season': '2020-2021', 'end': '2023/01/16'},
            TypeError,
            "La date doit être une chaîne de caractères au format aaaa-mm-dd"
        ),
        (
            {'season': '2020-2021', 'end': '202-05-160'},
            TypeError,
            "La date doit être une chaîne de caractères au format aaaa-mm-dd"
        ),
        (
            {'season': '2020-2021', 'end': '2021-05-aa'},
            ValueError,
            "Erreur de format pour la date."
        ),
        (
            {'season': '2020-2021', 'end': 'aaaa-mm-dd'},
            ValueError,
            "Erreur de format pour la date."
        )
    ]
)
def test_erreur_classement_conferences(get_data, param,
                                       erreur, message):

    df = get_data
    # Pour ce test, il faut que la table game se présente autrement que celle uilisée
    # pour les tests précédent. En effet, on va rajouter de nouvelle information
    df["game"] = pd.DataFrame([
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-10-30",
         "team_name_home": "Boston Celtics", "team_name_away": "Miami Heat",
         "wl_home": "W", "pts_home": 110, "pts_away": 102},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-11-18",
         "team_name_home": "Chicago Bulls", "team_name_away": "Toronto Raptors",
         "wl_home": "L", "pts_home": 95, "pts_away": 100},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-18",
         "team_name_home": "New York Knicks", "team_name_away": "Brooklyn Nets",
         "wl_home": "W", "pts_home": 120, "pts_away": 115},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-01",
         "team_name_home": "Milwaukee Bucks", "team_name_away": "Indiana Pacers",
         "wl_home": "W", "pts_home": 108, "pts_away": 97},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-02",
         "team_name_home": "Philadelphia 76ers", "team_name_away": "Detroit Pistons",
         "wl_home": "L", "pts_home": 90, "pts_away": 98},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-18",
         "team_name_home": "Denver Nuggets", "team_name_away": "Utah Jazz",
         "wl_home": "W", "pts_home": 113, "pts_away": 101},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-11-01",
         "team_name_home": "Phoenix Suns", "team_name_away": "LA Clippers",
         "wl_home": "W", "pts_home": 105, "pts_away": 103},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-11-09",
         "team_name_home": "Dallas Mavericks",
         "team_name_away": "Golden State Warriors",
         "wl_home": "L", "pts_home": 98, "pts_away": 106},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-18",
         "team_name_home": "Los Angeles Lakers", "team_name_away": "Sacramento Kings",
         "wl_home": "W", "pts_home": 115, "pts_away": 110},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-03-18",
         "team_name_home": "Houston Rockets", "team_name_away": "Memphis Grizzlies",
         "wl_home": "L", "pts_home": 89, "pts_away": 97},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-04-18",
         "team_name_home": "Atlanta Hawks", "team_name_away": "Orlando Magic",
         "wl_home": "W", "pts_home": 100, "pts_away": 96},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-05",
         "team_name_home": "Charlotte Hornets", "team_name_away": "Washington Wizards",
         "wl_home": "L", "pts_home": 91, "pts_away": 95},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-20",
         "team_name_home": "New Orleans Pelicans",
         "team_name_away": "San Antonio Spurs",
         "wl_home": "W", "pts_home": 112, "pts_away": 109},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-07",
         "team_name_home": "Portland Trail Blazers",
         "team_name_away": "Minnesota Timberwolves",
         "wl_home": "L", "pts_home": 96, "pts_away": 102},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-09",
         "team_name_home": "Cleveland Cavaliers", "team_name_away": "Toronto Raptors",
         "wl_home": "W", "pts_home": 103, "pts_away": 99},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-08",
         "team_name_home": "Oklahoma City Thunder",
         "team_name_away": "Golden State Warriors",
         "wl_home": "L", "pts_home": 87, "pts_away": 101},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-11",
         "team_name_home": "Detroit Pistons", "team_name_away": "Brooklyn Nets",
         "wl_home": "W", "pts_home": 99, "pts_away": 93},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-05",
         "team_name_home": "Sacramento Kings", "team_name_away": "San Antonio Spurs",
         "wl_home": "L", "pts_home": 94, "pts_away": 104},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-22",
         "team_name_home": "Orlando Magic", "team_name_away": "Boston Celtics",
         "wl_home": "L", "pts_home": 88, "pts_away": 96},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-03-04",
         "team_name_home": "Utah Jazz", "team_name_away": "Phoenix Suns",
         "wl_home": "W", "pts_home": 101, "pts_away": 95},
    ])

    reponses = Reponse(df)
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        reponses.classement_conferences(**param)

# ------------ Test sur les méthodes en vérifiant les résultats renvoyés -------------


@pytest.mark.parametrize(
    "param, attendu",
    [(
        {"annee_debut": 2022,
         "annee_fin": 2023},
        [("Equipe A", 4), ("Equipe B", 6)]
    ), (
        {"annee_debut": 2021,
         "annee_fin": 2022},
        [("Equipe A", 4), ("Equipe B", 2)]
    ), (
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "season_type": "Playoffs"},
        [("Equipe A", 4), ("Equipe B", 1), ("Equipe C", 1)]
    ), (
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "season_type": "Pre Season"},
        [("Equipe A", 3), ("Equipe B", 1), ("Equipe C", 2)]
    )]
)
def test_traitement_correct_victoires(get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    resultat = reponses.equip_victoires_defaites_saison(**param)
    for element in attendu:
        verif = resultat[
            resultat['Equipes'] == element[0]]['Nombre de victoires'] == element[1]
        assert verif.values[0]


@pytest.mark.parametrize(
    "param, attendu",
    [(
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "defaite": True},
        [("Equipe A", 2), ("Equipe B", 2), ("Equipe C", 6)]
    ), (
        {"annee_debut": 2021,
         "annee_fin": 2022,
         "defaite": True},
        [("Equipe B", 2), ("Equipe C", 4)]
    ), (
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "season_type": "Playoffs",
         "defaite": True},
        [("Equipe B", 3), ("Equipe B", 3)]
    ), (
        {"annee_debut": 2022,
         "annee_fin": 2023,
         "season_type": "Pre Season",
         "defaite": True},
        [("Equipe A", 1), ("Equipe B", 3), ("Equipe C", 2)]
    )]
)
def test_traitement_correct_defaites(get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    resultat = reponses.equip_victoires_defaites_saison(**param)
    for element in attendu:
        verif = resultat[
            resultat['Equipes'] == element[0]]['Nombre de défaites'] == element[1]
        assert verif.values[0]


@pytest.mark.parametrize(
    'param, attendu',
    [

        (
            {'top_N': 3, "periode": '2019-2023', "graph": False},
            [("UCLA", 3), ("Duke", 3), ("Michigan", 2)]
        ),
        (
            {'top_N': 3, "graph": False},
            [("UCLA", 3), ("Duke", 3), ("Michigan", 2)]
        ),
        (
            {'top_N': 1, "periode": '2019-2021', "graph": False},
            [("Duke", 3)]
        ),
        (
            {'top_N': 1, "annee_draft": 2021, "graph": False},
            [("Duke", 1)]
        ),
        (
            {'top_N': 1, "periode": '2019-2021', "graph": True},
            [("Duke", 3)]
        ),
    ]
)
def test_prop_joueurs_en_nba_selon_universite_de_formation(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    if param["graph"]:
        resultat, fig = reponses.prop_joueurs_en_nba_selon_universite_de_formation(
            **param)
    else:
        resultat = reponses.prop_joueurs_en_nba_selon_universite_de_formation(**param)
    for element in attendu:
        verif = resultat[
            resultat['Université'] == element[0]]['Effectif'] == element[1]
        assert verif.values[0]
    if param["graph"]:
        assert isinstance(fig, matplotlib.figure.Figure)


@pytest.mark.parametrize(
    'param, attendu',
    [

        (
            {'statistique': 'Mean'},
            [("Pivot", 214.63, 112.26), ("Ailier", 205.74, 104.33),
             ("Ailier fort/Pivot", 210.82, 108.86),
             ("Arrière/Meneur", 196.43, 90.72), ("Arrière/Ailier", 198.12, 97.52)]
        ),
        (
            {'statistique': 'Max', 'poste': "Pivot"},
            [("Pivot", 215.90, 113.40)]
        ),
        (
            {'statistique': 'Min', 'poste': "Arrière/Meneur"},
            [("Arrière/Meneur", 193.04, 86.18)]
        )
    ]
)
def test_stat_sur_taille_et_poids_par_poste(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    resultat = reponses.stat_sur_taille_et_poids_par_poste(**param)
    for element in attendu:
        verif_taille = resultat[
            resultat['position'] == element[0]]['Taille cm'] == element[1]
        verif_poids = resultat[
            resultat['position'] == element[0]]['Poids Kg'] == element[2]
        assert verif_taille.values[0] and verif_poids.values[0]


@pytest.mark.parametrize(
    'param, attendu',
    [

        (
            {'nb_victoire_min': 1},
            [("Equipe A", 2), ("Equipe B", 1)]
        ),
        (
            {'nb_victoire_min': 2},
            [("Equipe A", 2)]
        )
    ]
)
def test_equipe_remporte_au_moins_N_fois_le_titre(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    resultat = reponses.equipe_remporte_au_moins_N_fois_le_titre(**param)
    for element in attendu:
        verif = resultat[
            resultat['Equipe'] == element[0]]['Nombre de titre NBA'] == element[1]
        # print(verif)
        assert verif.values[0]


@pytest.mark.parametrize(
    'param, attendu',
    [
        (
            {'N_saison': 3},
            [(2023, "Joueur9", "Memphis")]
        )
        # Les données que nous avons simuler ne contient qu'un seul 1 choix
        # de draft
    ]
)
def test_premiers_choix_draft_N_derniere_saison(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    resultat = reponses.premiers_choix_draft_N_derniere_saison(**param)
    for element in attendu:
        verif_nom = resultat[
            resultat['Saison'] == element[0]]['Nom'] == element[1]
        verif_team = resultat[
            resultat['Saison'] == element[0]]['Equipe'] == element[2]
        assert verif_nom.values[0] and verif_team.values[0]


@pytest.mark.parametrize(
    'param, attendu',
    [
        (
            {'debut_periode': 2020, "fin_periode": 2023},
            [("2022-2023", "Equipe A"), ("2021-2022", "Equipe A"),
             ("2020-2021", "Equipe B")]
        ),
        (
            {'debut_periode': 2020, "fin_periode": 2021},
            [("2020-2021", "Equipe B")]
        )
    ]
)
def test_vainqueur_titre_NBA_saisons(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    resultat = reponses.vainqueur_titre_NBA_saisons(**param)
    for element in attendu:
        verif = resultat[
            resultat['Saison'] == element[0]]['Equipes'] == element[1]
        assert verif.values[0]


# Pour le test suivant, on prend la période 2020-2023 car ces uniquement sur cette
# période que nous avons généré nos données.
# En effet, si je prend la période par defaut 1946-2023, la taille ne peut pas être
# vérifié car dans la fonction on enrichi la réponse à l'aide des données collectées
# sur internet sur les saisons où ne retrouvons pas le vaiceur du titre à l'aide des
# données initiales


@pytest.mark.parametrize(
    'param, attendu',
    [
        (
            {'N': 2, 'debut_periode': 2020,
             "fin_periode": 2023},
            ["Equipe A"]
        ),
        (
            {'N': 2, 'debut_periode': 2020,
             "fin_periode": 2023},
            ["Equipe A"]
        ),
        (
            {'N': 1, 'debut_periode': 2020,
             "fin_periode": 2023},
            ["Equipe A", "Equipe B"]
        )

    ]
)
def test_equipe_qui_remporte_N_fois_daffile_le_titre(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    resultat = reponses.equipe_qui_remporte_N_fois_daffile_le_titre(**param)
    assert all(val in attendu for val in resultat) and (len(resultat) == len(attendu))


@pytest.mark.parametrize(
    'param, attendu',
    [
        (
            {'debut_periode': 2022,
             'fin_periode': 2023, "defaite": False},
            [("2022-2023", "Equipe B", 6)]
        ),
        (
            {'debut_periode': 2021,
             'fin_periode': 2023, "defaite": False},
            [("2021-2022", "Equipe A", 4),
             ("2022-2023", "Equipe B", 6)]
        ),
        (
            {'debut_periode': 2022,
             'fin_periode': 2023, "defaite": True},
            [("2022-2023", "Equipe C", 6)]
        ),
        (
            {'debut_periode': 2021,
             'fin_periode': 2023, "defaite": True},
            [("2021-2022", "Equipe C", 4),
             ("2022-2023", "Equipe C", 6)]
        ),
    ]
)
def test_nombre_victoires_ou_defaites_equipe_les_N_dernieres_saisons(
        get_data, param, attendu):
    df = get_data
    reponses = Reponse(df)
    # Le test passe lorsque la réponse attendu est une erreur
    resultat = reponses.nombre_victoires_ou_defaites_equipe_les_N_dernieres_saisons(
        **param)
    # récupérons le bon libele de la colonne
    status = ("Nombre de " +
              'victoires'*(1-param['defaite']) +
              'défaites'*param['defaite'])
    for element in attendu:
        verif_nom = resultat[
            resultat['Saison'] == element[0]]['Equipes'] == element[1]
        verif_point = resultat[
            resultat['Saison'] == element[0]][status] == element[2]
        assert verif_point.values[0] and verif_nom.values[0]


@pytest.mark.parametrize(
    'param, attendu',
    [
        (
            {'top': 5, 'graph': False},
            [('Canada', 7), ("France", 4), ("Germany", 2), ("Spain", 2), ("Brazil", 1)]
        ),
        (
            {'top': 2, 'graph': True},
            [('Canada', 7), ("France", 4)]
        )
    ]
)
def test_top_N_nb_joueurs_par_pays(get_data, param, attendu):
    df = get_data

    # Les données simulé au départ portant uniquement sur les pays des USA.
    # Pour faire ce test on va donc proposer d'autres données pour faire intervenir
    # différents pays
    df["common_player_info"] = pd.DataFrame([
        {"person_id": 999001, "country": "USA"},
        {"person_id": 999002, "country": "Canada"},
        {"person_id": 999003, "country": "Canada"},
        {"person_id": 999004, "country": "Spain"},
        {"person_id": 999005, "country": "Canada"},
        {"person_id": 999006, "country": "USA"},
        {"person_id": 999007, "country": "France"},
        {"person_id": 999008, "country": "Germany"},
        {"person_id": 999009, "country": "USA"},
        {"person_id": 999010, "country": "Brazil"},
        {"person_id": 999011, "country": "Canada"},
        {"person_id": 999012, "country": "France"},
        {"person_id": 999013, "country": "Spain"},
        {"person_id": 999014, "country": "Canada"},
        {"person_id": 999015, "country": "Canada"},
        {"person_id": 999016, "country": "Japan"},
        {"person_id": 999017, "country": "Germany"},
        {"person_id": 999018, "country": "France"},
        {"person_id": 999019, "country": "Canada"},
        {"person_id": 999020, "country": "France"},
    ])

    reponses = Reponse(df)

    if param["graph"]:
        resultat, fig = reponses.top_N_nb_joueurs_par_pays(**param)
    else:
        resultat = reponses.top_N_nb_joueurs_par_pays(**param)
    for element in attendu:
        verif = resultat[
            resultat['Pays'] == element[0]]['Effectif'] == element[1]
        assert verif.values[0]
    if param["graph"]:
        assert isinstance(fig, matplotlib.figure.Figure)


@pytest.mark.parametrize(
    'param, conference, attendu',
    [  # On va tester pour valeurs des 5 premiers
        (
            {'season': '2022-2023'},
            "Conférence Est",
            [("Boston Celtics", 2.0, 206.0), ("Detroit Pistons", 2.0, 197.0),
             ("Milwaukee Bucks", 1.0, 108.0), ("Toronto Raptors", 1.0, 199.0),
             ("New York Knicks", 1.0, 120.0)]
        ),
        (
            {'season': '2022-2023'},
            "Conférence Ouest",
            [("Phoenix Suns", 1.0, 200.0), ("San Antonio Spurs", 1.0, 213.0),
             ("Golden State Warriors", 2.0, 207.0), ("Utah Jazz", 1.0, 202.0),
             ('Los Angeles Lakers', 1.0, 115.0)]
        ),
    ]
)
def test_classement_conferences(get_data, param,
                                conference, attendu):

    df = get_data
    # Pour ce test, il faut que la table game se présente autrement que celle uilisée
    # pour les tests précédent. En effet, on va rajouter de nouvelle information
    df["game"] = pd.DataFrame([
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-10-30",
         "team_name_home": "Boston Celtics", "team_name_away": "Miami Heat",
         "wl_home": "W", "pts_home": 110, "pts_away": 102},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-11-18",
         "team_name_home": "Chicago Bulls", "team_name_away": "Toronto Raptors",
         "wl_home": "L", "pts_home": 95, "pts_away": 100},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-18",
         "team_name_home": "New York Knicks", "team_name_away": "Brooklyn Nets",
         "wl_home": "W", "pts_home": 120, "pts_away": 115},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-01",
         "team_name_home": "Milwaukee Bucks", "team_name_away": "Indiana Pacers",
         "wl_home": "W", "pts_home": 108, "pts_away": 97},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-02",
         "team_name_home": "Philadelphia 76ers", "team_name_away": "Detroit Pistons",
         "wl_home": "L", "pts_home": 90, "pts_away": 98},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-12-18",
         "team_name_home": "Denver Nuggets", "team_name_away": "Utah Jazz",
         "wl_home": "W", "pts_home": 113, "pts_away": 101},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-11-01",
         "team_name_home": "Phoenix Suns", "team_name_away": "LA Clippers",
         "wl_home": "W", "pts_home": 105, "pts_away": 103},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2022-11-09",
         "team_name_home": "Dallas Mavericks",
         "team_name_away": "Golden State Warriors",
         "wl_home": "L", "pts_home": 98, "pts_away": 106},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-18",
         "team_name_home": "Los Angeles Lakers", "team_name_away": "Sacramento Kings",
         "wl_home": "W", "pts_home": 115, "pts_away": 110},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-03-18",
         "team_name_home": "Houston Rockets", "team_name_away": "Memphis Grizzlies",
         "wl_home": "L", "pts_home": 89, "pts_away": 97},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-04-18",
         "team_name_home": "Atlanta Hawks", "team_name_away": "Orlando Magic",
         "wl_home": "W", "pts_home": 100, "pts_away": 96},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-05",
         "team_name_home": "Charlotte Hornets", "team_name_away": "Washington Wizards",
         "wl_home": "L", "pts_home": 91, "pts_away": 95},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-20",
         "team_name_home": "New Orleans Pelicans",
         "team_name_away": "San Antonio Spurs",
         "wl_home": "W", "pts_home": 112, "pts_away": 109},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-07",
         "team_name_home": "Portland Trail Blazers",
         "team_name_away": "Minnesota Timberwolves",
         "wl_home": "L", "pts_home": 96, "pts_away": 102},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-09",
         "team_name_home": "Cleveland Cavaliers", "team_name_away": "Toronto Raptors",
         "wl_home": "W", "pts_home": 103, "pts_away": 99},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-08",
         "team_name_home": "Oklahoma City Thunder",
         "team_name_away": "Golden State Warriors",
         "wl_home": "L", "pts_home": 87, "pts_away": 101},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-01-11",
         "team_name_home": "Detroit Pistons", "team_name_away": "Brooklyn Nets",
         "wl_home": "W", "pts_home": 99, "pts_away": 93},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-05",
         "team_name_home": "Sacramento Kings", "team_name_away": "San Antonio Spurs",
         "wl_home": "L", "pts_home": 94, "pts_away": 104},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-02-22",
         "team_name_home": "Orlando Magic", "team_name_away": "Boston Celtics",
         "wl_home": "L", "pts_home": 88, "pts_away": 96},
        {"season_id": 22022, "season_type": "Regular Season", "game_date": "2023-03-04",
         "team_name_home": "Utah Jazz", "team_name_away": "Phoenix Suns",
         "wl_home": "W", "pts_home": 101, "pts_away": 95},
    ])

    reponses = Reponse(df)
    resultat = reponses.classement_conferences(**param)
    resultat = resultat[conference].iloc[:5, :]
    print(resultat)
    for element in attendu:
        verif_vic = resultat[
            resultat['Équipe'] == element[0]]["Victoires"] == element[1]
        verif_point = resultat[
            resultat['Équipe'] == element[0]]["Points"] == element[2]
        assert verif_point.values[0] and verif_vic.values[0]
