import pandas as pd
import pytest
import re
from logic_for_application import CareerPrediction


@pytest.fixture
def dummy_data():
    return pd.DataFrame({
        "draft_year": ["2000", "2001", "2002"],
        "birthdate": ["1980-01-01", "1981-01-01", "1982-01-01"],
        "height": ["6'5\"", "6'7\"", "6'6\""],
        "weight": [200, 210, 190],
        "position": ["Guard", "Forward", "Center"],
        "to_year": [2020, 2020, 2020],
        "season_exp": [10, 12, 8]
    })


@pytest.fixture
def dummy_coef_df():
    return pd.DataFrame({
        "Variable": ["intercept", "age_at_draft", "position_Forward", "position_Guard"],
        "Estimation": [2.0, 0.5, 1.0, -1.0],
        "Borne inférieure": [1.5, 0.3, 0.5, -1.5],
        "Borne supérieure": [2.5, 0.7, 1.5, -0.5],
    })


# test erreur init
@pytest.mark.parametrize(
    "data, message_erreur",
    [
        (
            ['1', '2'],
            "Le paramètre data doit être un pd.DataFrame"
        ),
        (
            {'1': '2'},
            "Le paramètre data doit être un pd.DataFrame"
        ),

    ]
)
def test_erreur_init(data, message_erreur):
    with pytest.raises(TypeError, match=re.escape(message_erreur)):
        CareerPrediction(data=data)


# tester succès de l'initialisation
def test_initialization(dummy_data):
    model = CareerPrediction(dummy_data)
    assert isinstance(model.data, pd.DataFrame)


def test_predict_valid(dummy_coef_df, dummy_data):
    model = CareerPrediction(dummy_data, x_vars=["age_at_draft", "position"])
    result = model.predict_career_duration(
        birthdate="1980-01-01",
        draft_year="2000-01-01",
        position="Forward",
        coef_df=dummy_coef_df,
    )
    assert isinstance(result, dict)
    assert "duree_predite" in result
    assert "intervalle_confiance" in result


def test_invalid_age_prediction(dummy_coef_df, dummy_data):
    model = CareerPrediction(dummy_data, x_vars=["age_at_draft", "position"])
    with pytest.raises(ValueError):
        model.predict_career_duration(
            birthdate="2001-01-01",
            draft_year="2000-01-01",
            position="Guard",
            coef_df=dummy_coef_df,
        )
