import re
import pytest
from utils import replace_old_team_name
import pandas as pd

# Test qui leve une erreur à l'éxcution


@pytest.mark.parametrize(
    'param, erreur, message',
    [
        (
            {"data": [1, 2, 3],
             'column': 10,
             'nba_franchises_old_names': {'cle': "valeur"}},
            TypeError,
            "L'argument data doit être un pd.DataFrame"
        ),
        (
            {"data": "Hello",
             'column': 10,
             'nba_franchises_old_names': {'cle': "valeur"}},
            TypeError,
            "L'argument data doit être un pd.DataFrame"
        ),
        (
            {"data": pd.DataFrame(data=[{'col1': "1", 'col2': "2",
                                         'col3': "3", 'col4': "4"}]),
             'column': 10,
             'nba_franchises_old_names': {'cle': "valeur"}},
            TypeError,
            "L'argument column doit être de type str"
        ),
        (
            {"data": pd.DataFrame(data=[{'col1': "1", 'col2': "2",
                                         'col3': "3", 'col4': "4"}]),
             'column': ["col1"],
             'nba_franchises_old_names': {'cle': "valeur"}},
            TypeError,
            "L'argument column doit être de type str"
        ),
        (
            {"data": pd.DataFrame(data=[{'col1': "1", 'col2': "2",
                                         'col3': "3", 'col4': "4"}]),
             'column': "col5",
             'nba_franchises_old_names': {'cle': "valeur"}},
            ValueError,
            "La colonne spécifiée n'existe pas dans la table"
        ),
        (
            {"data": pd.DataFrame(data=[{'col1': "1", 'col2': "2",
                                         'col3': "3", 'col4': "4"}]),
             'column': "col2",
             'nba_franchises_old_names': ['cle', "valeur"]},
            TypeError,
            "L'argument nba_franchises_old_names doit être un dictionnaire"
        ),
        (
            {"data": pd.DataFrame(data=[{'col1': "1", 'col2': "2",
                                         'col3': "3", 'col4': "4"}]),
             'column': "col5",
             'nba_franchises_old_names': [{'cle': "valeur"}]},
            TypeError,
            "L'argument nba_franchises_old_names doit être un dictionnaire"
        )

    ]
)
def test_erreur_replane_team_name(param, erreur, message):
    with pytest.raises(
        erreur, match=re.escape(message)
    ):
        # Le test passe lorsque la réponse attendu est une erreur
        replace_old_team_name(**param)


# test succes
@pytest.mark.parametrize(
    'param, expected_result',
    [
        (
            {"data": pd.DataFrame({
                'team': ["Kings", "Nets", "Jazz", "Warriors"],
                'year': [2015, 2016, 2017, 2018]}),
             'column': "team",
             'nba_franchises_old_names': {
                 "Sacramento Kings": ["Kings"],
                 "Golden State Warriors": ["Warriors"]
             }},
            pd.DataFrame({
                'team': ["Sacramento Kings", "Nets", "Jazz", "Golden State Warriors"],
                'year': [2015, 2016, 2017, 2018]}),
        ),
        (
            {"data": pd.DataFrame({
                'team': ["Lakers", "Bulls", "Knicks", "Celtics"],
                'year': [2000, 2001, 2002, 2003]}),
             'column': "team",
             'nba_franchises_old_names': {
                 "Los Angeles Lakers": ["Lakers"],
                 "Chicago Bulls": ["Bulls"]
             }},
            pd.DataFrame({
                'team': ["Los Angeles Lakers", "Chicago Bulls", "Knicks", "Celtics"],
                'year': [2000, 2001, 2002, 2003]}),
        ),
        (
            {"data": pd.DataFrame({
                'team': ["Hornets", "Spurs", "Heat", "Cavs"],
                'year': [2010, 2011, 2012, 2013]}),
             'column': "team",
             'nba_franchises_old_names': {
                 "Charlotte Hornets": ["Hornets"],
                 "Miami Heat": ["Heat"]
             }},
            pd.DataFrame({
                'team': ["Charlotte Hornets", "Spurs", "Miami Heat", "Cavs"],
                'year': [2010, 2011, 2012, 2013]}),
        ),
        (
            {"data": pd.DataFrame({
                'team': ["Hawks", "Celtics", "Lakers", "Mavericks"],
                'year': [2016, 2017, 2018, 2019]}),
             'column': "team",
             'nba_franchises_old_names': {
                 "Atlanta Hawks": ["Hawks"],
                 "Dallas Mavericks": ["Mavericks"]
             }},
            pd.DataFrame({
                'team': ["Atlanta Hawks", "Celtics", "Lakers", "Dallas Mavericks"],
                'year': [2016, 2017, 2018, 2019]}),
        ),
        (
            {"data": pd.DataFrame({
                'team': ["Clippers", "Bucks", "Cavs", "Heat"],
                'year': [2015, 2016, 2017, 2018]}),
             'column': "team",
             'nba_franchises_old_names': {
                 "Los Angeles Clippers": ["Clippers"],
                 "Milwaukee Bucks": ["Bucks"]
             }},
            pd.DataFrame({
                'team': ["Los Angeles Clippers", "Milwaukee Bucks", "Cavs", "Heat"],
                'year': [2015, 2016, 2017, 2018]}),
        )
    ]
)
def test_success_replace_old_team_name(param, expected_result):
    result = replace_old_team_name(**param)
    # vérifie que le DataFrame résultant est égal au DataFrame attendu
    pd.testing.assert_frame_equal(result, expected_result)
