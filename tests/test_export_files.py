import os
from utils import ExportFiles
import pytest
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


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


@pytest.fixture
def basic_plot():
    def _plot():
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        ax.set_title("Exemple")
        return fig
    return _plot


# test erreur export_to_csv_format
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "table": [2, "Pique"],
                "path": '../Exportations/tables/table.csv',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame ou"
            "  pd.Series peuvent être exportées",
        ),
        (
            {
                "table": {2, "Pique"},
                "path": '../Exportations/tables/table.csv',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame ou"
            "  pd.Series peuvent être exportées",
        ),
        (
            {
                "table": 10,
                "path": '../Exportations/tables/table.csv',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame ou"
            "  pd.Series peuvent être exportées",
        ),
        (
            {
                "table": (2, "Pique"),
                "path": '../Exportations/tables/table.csv',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame ou"
            "  pd.Series peuvent être exportées",
        ),
        (
            {
                "table": "",
                "path": '../Exportations/tables/table.csv',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame ou"
            "  pd.Series peuvent être exportées",
        ),
        (
            {
                "table": None,
                "path": '../Exportations/tables/table.csv',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame ou"
            "  pd.Series peuvent être exportées",
        ),
        (
            {
                "table": pd.DataFrame({}),
                "path": 10,
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str)."
        ),
        (
            {
                "table": pd.DataFrame({}),
                "path": [10],
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str)."
        ),
        (
            {
                "table": pd.DataFrame({}),
                "path": pd.DataFrame({}),
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str)."
        ),
    ],
)
# fonction pour tester les erreurs en fonction de
# la paramétrisation ci-dessus
def test_export_to_csv_format_echec(params, erreur, message_erreur):
    export_files = ExportFiles()
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        export_files.export_to_csv_format(**params)


# test succès export_to_csv_format
@pytest.mark.parametrize(
    "params, resultat_attendu",
    [
        (
            {
                "table": None,
                "path": f'{os.getcwd()}/Exportations/tables/table.csv',
            },
            True,
        ),
        (
            {
                "table": None,
                "path": f'{os.getcwd()}/Exportations/tables/table.csv',
            },
            True,
        ),
    ],
)
def test_succes_export_to_csv_format(simple_df, params, resultat_attendu):
    if params['table'] is None:
        params['table'] = simple_df
    export_files = ExportFiles()
    print("Répertoire courant :", os.getcwd())
    res = export_files.export_to_csv_format(**params)
    assert res == resultat_attendu


# test erreur export_to_xlsx_format
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "table": [2, "Pique"],
                "path": '../Exportations/tables/table.xlsx',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame"
            " ou pd.Series peuvent être exportées"
        ),
        (
            {
                "table": {2, "Pique"},
                "path": '../Exportations/tables/table.xlsx',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame"
            " ou pd.Series peuvent être exportées",
        ),
        (
            {
                "table": 10,
                "path": '../Exportations/tables/table.xlsx',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame"
            " ou pd.Series peuvent être exportées",
        ),
        (
            {
                "table": (2, "Pique"),
                "path": '../Exportations/tables/table.xlsx',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame"
            " ou pd.Series peuvent être exportées",
        ),
        (
            {
                "table": "",
                "path": '../Exportations/tables/table.xlsx',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame"
            " ou pd.Series peuvent être exportées",
        ),
        (
            {
                "table": None,
                "path": '../Exportations/tables/table.xlsx',
            },
            TypeError,
            "Seules les tables de types pd.DataFrame"
            " ou pd.Series peuvent être exportées",
        ),
        (
            {
                "table": pd.DataFrame({}),
                "path": 10,
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str)."
        ),
        (
            {
                "table": pd.DataFrame({}),
                "path": [10],
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str)."
        ),
        (
            {
                "table": pd.DataFrame({}),
                "path": pd.DataFrame({}),
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str)."
        ),
    ],
)
# fonction pour tester les erreurs en fonction de
# la paramétrisation ci-dessus
def test_export_to_xlsx_format_echec(params, erreur, message_erreur):
    export_files = ExportFiles()
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        export_files.export_to_xlsx_format(**params)


# test succès export_to_xlsx_format
@pytest.mark.parametrize(
    "params, resultat_attendu",
    [
        (
            {
                "table": None,
                "path": f'{os.getcwd()}/Exportations/tables/table.xlsx',
            },
            True,
        ),
        (
            {
                "table": None,
                "path": f'{os.getcwd()}/Exportations/tables/table.xlsx',
            },
            True,
        ),
    ],
)
def test_succes_export_to_xlsx_format(simple_df, params, resultat_attendu):
    if params['table'] is None:
        params['table'] = simple_df
    export_files = ExportFiles()
    print("Répertoire courant :", os.getcwd())
    res = export_files.export_to_xlsx_format(**params)
    assert res == resultat_attendu


# Tests d’erreurs : export_to_png
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "img": None,
                "path": "figures/plot.png",
            },
            TypeError,
            "Seules les graphiques faits"
            " avec matplotlib peuvent être exportés",
        ),
        (
            {
                "img": [1, 2, 3],
                "path": "figures/plot.png",
            },
            TypeError,
            "Seules les graphiques faits"
            " avec matplotlib peuvent être exportés",
        ),
        (
            {
                "img": plt.figure(),
                "path": 123,
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str).",
        ),
    ],
)
def test_export_to_png_format_erreur(params, erreur, message_erreur):
    export_files = ExportFiles()
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        export_files.export_to_png(**params)


# Tests de succès : export_to_jpg
@pytest.mark.parametrize(
    "params, resultat_attendu",
    [
        (
            {
                "img": None,
                "path": f"{os.getcwd()}/Exportations/images/plot.png",
            },
            True,
        ),
        (
            {
                "img": None,
                "path": f"{os.getcwd()}/Exportations/images/plot.png",
            },
            True,
        ),
    ],
)
def test_export_to_png_format_succes(basic_plot, params, resultat_attendu):
    if params["img"] is None:
        params["img"] = basic_plot()
    export_files = ExportFiles()
    res = export_files.export_to_png(**params)
    assert res == resultat_attendu


# Tests d’erreurs : export_to_jpg
@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {
                "img": None,
                "path": "figures/plot.jpg",
            },
            TypeError,
            "Seules les graphiques faits"
            " avec matplotlib peuvent être exportés",
        ),
        (
            {
                "img": [1, 2, 3],
                "path": "figures/plot.jpg",
            },
            TypeError,
            "Seules les graphiques faits"
            " avec matplotlib peuvent être exportés",
        ),
        (
            {
                "img": plt.figure(),
                "path": 123,
            },
            TypeError,
            "Le chemin de sauvegarde (path)"
            " doit être une chaîne de caractères (str).",
        ),
    ],
)
def test_export_to_jpg_erreur(params, erreur, message_erreur):
    export_files = ExportFiles()
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        export_files.export_to_jpg(**params)


# Tests de succès : export_to_jpg
@pytest.mark.parametrize(
    "params, resultat_attendu",
    [
        (
            {
                "img": None,
                "path": f"{os.getcwd()}/Exportations/images/plot.jpg",
            },
            True,
        ),
        (
            {
                "img": None,
                "path": f"{os.getcwd()}/Exportations/images/plot.jpg",
            },
            True,
        ),
    ],
)
def test_export_to_jpg_format_succes(basic_plot, params, resultat_attendu):
    if params["img"] is None:
        params["img"] = basic_plot()
    export_files = ExportFiles()
    res = export_files.export_to_png(**params)
    assert res == resultat_attendu
