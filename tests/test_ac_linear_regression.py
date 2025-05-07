from answers_class import LinearRegression
import pandas as pd
import numpy as np

# from sklearn import linear_model.LinearRegression
import pytest
import re
import utils.chargement_data as chargement_data


@pytest.fixture
def get_data():
    # Lecture des fichier
    data = chargement_data.import_data(path="donnees_basketball")
    return data["common_player_info"]


# simple_df ressemble traits pour trait à data['common_player_info']
# dans l'optique de faciliter les tests et de voir facilement ce qui
# la gestion des ereurs et de test des succes des autres fonctions


@pytest.fixture
def simple_df():
    return pd.DataFrame(
        {
            "weight": [70, 80, 90, 70, 80, 90],
            "position": ["Guard", "Forward", "Center", "Guard", "Forward", "Center"],
            "season_exp": [
                3,
                5,
                7,
                4,
                6,
                8,
            ],  # relation approx linéaire avec poids et position
        }
    )


# Paramétrisation pour tester les erreurs levées lors de l'appel du constructeur
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": [2, "Pique"],
                "y_var": ["11"],
                "x_vars": ["55"],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            TypeError,
            "La base de données fournie en paramètre doit être de type pd.DataFrame",
        ),
        (
            {
                "df": None,
                "y_var": 10,
                "x_vars": ["55"],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            TypeError,
            "y_var et x_vars doivent être des listes",
        ),
        (
            {
                "df": None,
                "y_var": ['10'],
                "x_vars": [],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            ValueError,
            "x_vars doit contenir au moins un élement",
        ),
        (
            {
                "df": None,
                "y_var": ['10'],
                "x_vars": ['10', 2],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            TypeError,
            "x_vars doit contenir des élements de types str",
        ),
        (
            {
                "df": None,
                "y_var": 10,
                "x_vars": "55",
                "seuil": 0.05,
                "fit_intercept": True,
            },
            TypeError,
            "y_var et x_vars doivent être des listes",
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["school", "birthdate"],
                "seuil": "0.05",
                "fit_intercept": True,
            },
            TypeError,
            "Le seuil doit être un nombre réel",
        ),
        (
            {
                "df": None,
                "y_var": [10],
                "x_vars": ["55"],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            TypeError,
            "y_var doit contenir un élement de type str",
        ),
        (
            {
                "df": None,
                "y_var": ["A", "B"],
                "x_vars": ["55"],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            ValueError,
            "y_var doit contenir exactement un élement",
        ),
        (
            {
                "df": None,
                "y_var": ["A"],
                "x_vars": [10, "55"],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            TypeError,
            "x_vars doit contenir des élements de types str",
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["school", "birthdate"],
                "seuil": 0.05,
                "fit_intercept": "True",
            },
            TypeError,
            "fit_intercept doit être un bool",
        ),
        (
            {
                "df": None,
                "y_var": ["A"],
                "x_vars": ["10", "55"],
                "seuil": 0.05,
                "fit_intercept": True,
            },
            ValueError,
            "x_vars et y_var doivent être parmis les colonnes de df",
        ),
    ],
)
# fonction pour tester les erreurs en fonction de
# la paramétrisation ci-dessus
def test_linerar_reg_init_echec(get_data, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = get_data
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        LinearRegression(**params)


# test es erreur  la méthode get_dummies
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": "pas_un_dataframe",
                "variable": "position",
                "delete_var": False,
                "drop_first": False,
            },
            TypeError,
            "La base de données fournie en paramètre doit être de type pd.DataFrame",
        ),
        (
            {
                "df": None,
                "variable": 123,
                "delete_var": False,
                "drop_first": False,
            },
            TypeError,
            "L'argument variable doit être de type str",
        ),
        (
            {
                "df": None,
                "variable": "position",
                "delete_var": "faux",
                "drop_first": False,
            },
            TypeError,
            "L'argument delete_var doit être un booléen",
        ),
        (
            {
                "df": None,
                "variable": "position",
                "delete_var": False,
                "drop_first": "non",
            },
            TypeError,
            "L'argument drop_first doit être un booléen",
        ),
        (
            {
                "df": None,
                "variable": "inexistante",
                "delete_var": False,
                "drop_first": False,
            },
            ValueError,
            "La variable spécifiée n'existe pas dans la base de données",
        ),
    ],
)
def test_get_dummies_erreurs(get_data, params, erreur, message_erreur):
    model = LinearRegression(
        df=get_data,
        y_var=["season_exp"],
        x_vars=["height", "weight"],
        seuil=0.05,
        fit_intercept=True,
    )
    if params["df"] is None:
        params["df"] = get_data
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.get_dummies(**params)


# test du succes
# Paramétrisation pour tester les cas de succès de la méthode get_dummies
@pytest.mark.parametrize(
    "params, resultat_attendu",
    [
        (
            {
                "df": None,
                "variable": "position",
                "delete_var": False,
                "drop_first": False,
            },
            [
                "position_Center",
                "position_Center-Forward",
                "position_Forward",
                "position_Forward-Center",
                "position_Forward-Guard",
                "position_Guard",
                "position_Guard-Forward",
            ],
        ),
        (
            {
                "df": None,
                "variable": "position",
                "delete_var": False,
                "drop_first": True,
            },
            [
                "position",
                "position_Center-Forward",
                "position_Forward",
                "position_Forward-Center",
                "position_Forward-Guard",
                "position_Guard",
                "position_Guard-Forward",
            ],  # 'position_Center' est ignorée car en premier alphabétiquement
        ),
        (
            {
                "df": None,
                "variable": "position",
                "delete_var": True,
                "drop_first": False,
            },
            [
                "position_Center",
                "position_Center-Forward",
                "position_Forward",
                "position_Forward-Center",
                "position_Forward-Guard",
                "position_Guard",
                "position_Guard-Forward",
            ],
        ),
        (
            {
                "df": None,
                "variable": "position",
                "delete_var": True,
                "drop_first": True,
            },
            [
                "position_Guard-Forward",
                "position_Center-Forward",
                "position_Forward",
                "position_Forward-Center",
                "position_Forward-Guard",
                "position_Guard",
            ],
        ),
    ],
)
def test_get_dummies_succes(get_data, params, resultat_attendu):
    model = LinearRegression(
        df=get_data,
        y_var=["season_exp"],
        x_vars=["height", "weight"],
        seuil=0.05,
        fit_intercept=True,
    )
    if params["df"] is None:
        params["df"] = get_data

    df_resultat = model.get_dummies(**params)
    # Vérifie que toutes les colonnes attendues sont présentes
    for col in resultat_attendu:
        assert col in df_resultat.columns

    # Si delete_var est True, on vérifie que la variable d'origine a disparu
    if params["delete_var"]:
        assert params["variable"] not in df_resultat.columns
    else:
        assert params["variable"] in df_resultat.columns

    # Vérification que la somme des dummies par ligne est égale à 1
    for i, row in df_resultat.iterrows():
        dummies_columns = [
            col
            for col in df_resultat.columns
            if col.startswith(f"{params['variable']}_")
        ]
        sum_dummies = row[dummies_columns].sum()
        assert sum_dummies == 1 or sum_dummies == 0


# te=ter create_x_Y
@pytest.mark.parametrize(
    "params, expected_columns_X, expected_columns_y",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
            },
            [
                "intercept",
                "weight",
                "position_Center-Forward",
                "position_Forward",
                "position_Forward-Center",
                "position_Forward-Guard",
                "position_Guard",
                "position_Guard-Forward",
            ],
            ["season_exp"],
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": False,
            },
            [
                "weight",
                "position_Center-Forward",
                "position_Forward",
                "position_Forward-Center",
                "position_Forward-Guard",
                "position_Guard",
                "position_Guard-Forward",
            ],
            ["season_exp"],
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["position"],
                "fit_intercept": True,
            },
            ["intercept", "position_Center-Forward", "position_Forward"],
            ["season_exp"],
        ),
    ],
)
def test_create_x_y(get_data, params, expected_columns_X, expected_columns_y):
    # Préparation de la donnée si df est None
    if params["df"] is None:
        params["df"] = get_data

    # Création du modèle LinearRegression
    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        seuil=0.05,
        fit_intercept=params["fit_intercept"],
    )

    # Appel de la méthode create_x_y
    X, y = model.create_x_y()
    # print(X.columns, y.columns)
    # Vérification des colonnes de X
    for col in expected_columns_X:
        assert col in X.columns

    # Vérification des colonnes de y
    assert isinstance(y, np.ndarray)
    assert y.shape == (y.shape[0], len(expected_columns_y))


#  tester les erreurs de la methode fit et fit_ridge
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "X": [2, "Pique"],
                "y": ["11"],
            },
            TypeError,
            "X et Y doivent-être de type np.ndarray",
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "X": 15,
                "y": ["11"],
            },
            TypeError,
            "X et Y doivent-être de type np.ndarray",
        ),
    ],
)
# fonction pour tester les erreurs des méthodes fit
# et fit ridge
# la paramétrisation ci-dessus
def test_fit_echec(simple_df, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = simple_df

    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        seuil=0.05,
        fit_intercept=params["fit_intercept"],
    )

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.fit(params["X"], params["y"])


# test fit_ridge echec
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "use_ridge": "yes",  # Mauvais type
                "alpha": 1.0,
            },
            TypeError,
            "use_ridge doit être de type booléen",
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "use_ridge": True,
                "alpha": "1",  # Mauvais type
            },
            TypeError,
            "use_ridge doit être de type float",
        ),
    ],
)
def test_perfom_linear_reg_echec(simple_df, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = simple_df

    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        fit_intercept=params["fit_intercept"],
        seuil=0.05,
    )

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.perfom_linear_reg(
            use_ridge=params["use_ridge"],
            alpha=params["alpha"]
        )


# tester succès de la méthode fit
def test_fit_ols(simple_df):
    model = LinearRegression(
        df=simple_df, y_var=["season_exp"], x_vars=["weight"], seuil=0.05
    )
    X, y = model.create_x_y()
    Beta = model.fit(X.values, y)

    assert isinstance(Beta, np.ndarray)
    y_hat = model.predict(X.values, Beta)
    rmse = model.compute_rmse(y, y_hat)
    assert rmse < 1.0  # bonne approximation si données linéaires
    assert isinstance(Beta, np.ndarray)  # verifie que Beta est un df pandas
    assert Beta.shape[0] == 2


# tester le succès de la méthode fit_ridge
def test_fit_ridge(simple_df):
    model = LinearRegression(
        df=simple_df, y_var=["season_exp"], x_vars=["weight"], seuil=0.05
    )
    X, y = model.create_x_y()
    Beta_ridge = model.fit_ridge(X.values, y, alpha=0.1)

    assert isinstance(Beta_ridge, np.ndarray)
    y_hat_ridge = model.predict(X.values, Beta_ridge)
    rmse_ridge = model.compute_rmse(y, y_hat_ridge)
    assert rmse_ridge > 0
    assert isinstance(Beta_ridge, np.ndarray)


# tester echec de la methode predict
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "X": [2, "Pique"],
                "y": ["11"],
            },
            TypeError,
            "X doit être un np.ndarray",
        )
    ],
)
def test_predict_echec(simple_df, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = simple_df

    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        seuil=0.05,
        fit_intercept=params["fit_intercept"],
    )
    X, y = model.create_x_y()
    Beta = model.fit(X.values, y)

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.predict(params["X"], Beta)


# tester succees de la methode predict
def test_predict(simple_df):
    model = LinearRegression(
        df=simple_df, y_var=["season_exp"], x_vars=["weight"], seuil=0.05
    )
    X, y = model.create_x_y()
    Beta = model.fit(X.values, y)
    y_pred = model.predict(X.values, Beta)

    assert isinstance(y_pred, np.ndarray)
    assert y_pred.shape == y.shape


# test echec compute rmse
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "y_true": [1, 2, 3],
                "y_pred": np.array([1, 2, 3]),
            },
            TypeError,
            "y_true et y_pred doivent-être de type np.ndarray",
        ),
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "y_true": np.array([1, 2, 3]),
                "y_pred": "not an array",
            },
            TypeError,
            "y_true et y_pred doivent-être de type np.ndarray",
        ),
    ],
)
def test_compute_rmse_echec(simple_df, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = simple_df

    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        fit_intercept=params["fit_intercept"],
        seuil=0.05,
    )

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.compute_rmse(params["y_true"], params["y_pred"])


# test de la méthode compute_rmse
def test_compute_rmse(simple_df):
    y_true = np.array([[1], [2], [3]])
    y_pred = np.array([[1.1], [1.9], [3.2]])
    model = LinearRegression(
        df=simple_df, y_var=["season_exp"], x_vars=["weight"], seuil=0.05
    )
    rmse = model.compute_rmse(y_true, y_pred)

    assert isinstance(rmse, float)
    assert np.isclose(rmse, np.sqrt(np.mean((y_true - y_pred) ** 2)))


# test erreur de compute_confidence_interval
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "X": [[1, 2], [3, 4]],  # X pas un np.ndarray
                "Y": np.array([[1], [2]]),
                "Y_hat": np.array([[1], [2]]),
                "Beta": np.array([[0.5], [1]]),
            },
            TypeError,
            "X, Y, Y_hat et Beta doivent-être de type np.ndarray",
        ),
        (
            {
                "X": np.array([[1, 2], [3, 4]]),
                "Y": [[1], [2]],  # Y pas un np.ndarray
                "Y_hat": np.array([[1], [2]]),
                "Beta": np.array([[0.5], [1]]),
            },
            TypeError,
            "X, Y, Y_hat et Beta doivent-être de type np.ndarray",
        ),
        (
            {
                "X": np.array([[1, 2], [3, 4]]),
                "Y": np.array([[1], [2]]),
                "Y_hat": [[1], [2]],  # Y_hat pas un np.ndarray
                "Beta": np.array([[0.5], [1]]),
            },
            TypeError,
            "X, Y, Y_hat et Beta doivent-être de type np.ndarray",
        ),
        (
            {
                "X": np.array([[1, 2], [3, 4]]),
                "Y": np.array([[1], [2]]),
                "Y_hat": np.array([[1], [2]]),
                "Beta": [[0.5], [1]],  # Beta pas un np.ndarray
            },
            TypeError,
            "X, Y, Y_hat et Beta doivent-être de type np.ndarray",
        ),
    ]
)
def test_erreur_compute_confidence_interval(simple_df, params, erreur, message_erreur):
    model = LinearRegression(
        df=simple_df,
        y_var=['season_exp'],
        x_vars=['position', 'weight'],
        seuil=0.05,
        fit_intercept=True,
    )

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.compute_confidence_interval(
            params["X"], params["Y"], params["Y_hat"], params["Beta"]
        )


# test de la methode compute_confidence_interval
def test_compute_confidence_interval(simple_df):
    model = LinearRegression(
        df=simple_df, y_var=["season_exp"], x_vars=["weight"], seuil=0.05
    )
    X, y = model.create_x_y()
    Beta = model.fit(X.values, y)
    y_hat = model.predict(X.values, Beta)
    ci_df = model.compute_confidence_interval(X.values, y, y_hat, Beta)

    assert isinstance(ci_df, pd.DataFrame)
    assert "Estimation" in ci_df.columns
    assert "Borne inférieure" in ci_df.columns
    assert "Borne supérieure" in ci_df.columns
    assert len(ci_df) == X.shape[1]


# test de la methode perfom_linear_re
def test_perfom_linear_reg(simple_df):
    model = LinearRegression(
        df=simple_df, y_var=["season_exp"], x_vars=["weight", "position"], seuil=0.05
    )
    model.X, model.y = model.create_x_y()

    results = model.perfom_linear_reg(use_ridge=True, alpha=0.1)

    assert "estimation_results" in results
    assert "rmse" in results
    assert "y_pred" in results
    assert "epsilon" in results
    assert isinstance(results["estimation_results"], pd.DataFrame)
    assert results["rmse"] > 0


# tester echec des methodes create_k_fold et k_fold
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "X": [2, "Pique"],
                "y": ["11"],
                "k": "4",
            },
            TypeError,
            "k doit être un entier",
        )
    ],
)
def test_create_kfold_echec(simple_df, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = simple_df

    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        seuil=0.05,
        fit_intercept=params["fit_intercept"],
    )
    X, y = model.create_x_y()

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.create_k_fold(params["k"])


# test echec k_fold
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "df": None,
                "y_var": ["season_exp"],
                "x_vars": ["weight", "position"],
                "fit_intercept": True,
                "X": [2, "Pique"],
                "y": ["11"],
                "k": "4",
            },
            TypeError,
            "k doit être un entier",
        )
    ],
)
def test_kfold_echec(simple_df, params, erreur, message_erreur):
    if params["df"] is None:
        params["df"] = simple_df

    model = LinearRegression(
        df=params["df"],
        y_var=params["y_var"],
        x_vars=params["x_vars"],
        seuil=0.05,
        fit_intercept=params["fit_intercept"],
    )
    X, y = model.create_x_y()

    with pytest.raises(erreur, match=re.escape(message_erreur)):
        model.k_fold(params["k"])


# tester le succès de la methode create_k_fold
def test_create_k_fold(simple_df):
    model = LinearRegression(
        df=simple_df,
        y_var=["season_exp"],
        x_vars=["weight", "position"],
        fit_intercept=True,
        seuil=0.05,
    )
    model.X, model.y = model.create_x_y()
    folds = model.create_k_fold(k=3)

    assert isinstance(folds, list)
    assert len(folds) == 3
    for fold in folds:
        assert isinstance(fold, np.ndarray)
        assert fold.shape[1] == model.X.shape[1] + 1  # X + y


# tester le succès de la methode k_fold
def test_k_fold(simple_df):
    model = LinearRegression(
        df=simple_df,
        y_var=["season_exp"],
        x_vars=["weight", "position"],
        fit_intercept=True,
        seuil=0.05,
    )
    model.X, model.y = model.create_x_y()
    rmse_scores = model.k_fold(k=4)

    assert isinstance(rmse_scores, list)
    assert len(rmse_scores) == 4
    assert all(isinstance(score, float) for score in rmse_scores)
    assert all(score > 0 for score in rmse_scores)
