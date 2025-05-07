import pytest
import pandas as pd
from logic_for_application import HomeFunction
from application.shared import data
import re


@pytest.fixture
def home():
    return HomeFunction(data_=data)


def test_return_nb_players(home):
    assert isinstance(home.return_nb_players(), int)
    assert home.return_nb_players() > 0


def test_return_nb_teams(home):
    assert isinstance(home.return_nb_teams(), int)
    assert home.return_nb_teams() > 0


# test erreur de return_greatest_players
@pytest.mark.parametrize(
    "params, erreurs, message_erreur",
    [
        (
            {
                'year_range': (2022, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        ),
        (
            {
                'year_range': (1991, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        ),
        (
            {
                'year_range': (2021, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        )
    ]
)
def test_erreur_return_greatest_players(home, params, erreurs, message_erreur):
    with pytest.raises(erreurs, match=re.escape(message_erreur)):
        home.return_greatest_players(**params)


@pytest.mark.parametrize("year_range", [
        None,
        (2000, 2020)
    ])
def test_return_greatest_players(home, year_range):
    players = home.return_greatest_players(year_range=year_range)
    assert isinstance(players[1], int)
    assert isinstance(players[0], pd.DataFrame)
    assert 'Prénom' in players[0].columns
    assert 'Nom' in players[0].columns
    assert len(players[0]) >= 0  # peut être vide pour certaines années


# test erreur de create_line_chart_nb_match
@pytest.mark.parametrize(
    "params, erreurs, message_erreur",
    [
        (
            {
                'year_range': (2022, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        ),
        (
            {
                'year_range': (1991, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        ),
        (
            {
                'year_range': (2021, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        )
    ]
)
def test_erreur_create_line_chart_nb_match(home, params, erreurs, message_erreur):
    with pytest.raises(erreurs, match=re.escape(message_erreur)):
        home.create_line_chart_nb_match(**params)


@pytest.mark.parametrize("year_range", [
        None,
        (2000, 2020)
])
def test_create_line_chart_nb_match(home, year_range):
    fig = home.create_line_chart_nb_match(year_range)
    assert fig is not None


# test erreur de test_create_donut_chart
@pytest.mark.parametrize(
    "params, erreurs, message_erreur",
    [
        (
            {
                'year_range': (2022, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        ),
        (
            {
                'year_range': (1991, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        ),
        (
            {
                'year_range': (2021, 1900)
            },
            ValueError,
            "La date de début ne peut pas être après la date de fin"
        )
    ]
)
def test_erreur_create_donut_chart(home, params, erreurs, message_erreur):
    with pytest.raises(erreurs, match=re.escape(message_erreur)):
        home.create_dunut_chart_of_position_distribution(**params)


@pytest.mark.parametrize("year_range", [None, (2000, 2020)])
def test_create_donut_chart(home, year_range):
    fig = home.create_dunut_chart_of_position_distribution(year_range=year_range)
    assert fig is not None
    assert hasattr(fig, 'axes')
