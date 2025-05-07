import os
import pandas as pd
import matplotlib.pyplot as plt


class ExportFiles:
    """
    Classe pour exporter des tableaux de données ou des figures matplotlib
    vers différents formats de fichiers (CSV, Excel, JPG, PNG).
    """

    def __init__(self):
        """Initialise une instance d'ExportFiles (aucun paramètre requis)."""
        pass

    def _normalize_path(self, path: str) -> str:
        """
        Normalise le chemin d'accès en remplaçant
        les backslashes par des slashs.

        Parameters
        ----------
        path : str
            Chemin du fichier à corriger.

        Returns
        -------
        str
            Chemin corrigé compatible avec tous les systèmes d'exploitation.
        """
        return os.path.normpath(path.replace("\\", "/"))

    def export_to_csv_format(self, table, path) -> bool:
        """
        Exporte un DataFrame ou une Series vers un fichier CSV.

        Parameters
        ----------
        table : pandas.DataFrame or pandas.Series
            Table de données à exporter.
        path : str
            Chemin d'accès du fichier CSV à créer.

        Returns
        -------
        bool
            True si l'export a réussi, False sinon.

        Raises
        ------
        TypeError
            Si la table n'est pas un DataFrame ou une Series,
            ou si le path n'est pas une chaîne.
        """
        if not isinstance(table, (pd.DataFrame, pd.Series)):
            raise TypeError(
                "Seules les tables de types pd.DataFrame ou"
                "  pd.Series peuvent être exportées"
            )
        if not isinstance(path, str):
            raise TypeError(
                "Le chemin de sauvegarde (path)"
                " doit être une chaîne de caractères (str)."
            )
        try:
            path = self._normalize_path(path)
            table.to_csv(path, index=False)
            return True
        except Exception as e:
            print(f"Erreur lors de l'export CSV : {e}")
            return False

    def export_to_xlsx_format(self, table, path) -> bool:
        """
        Exporte un DataFrame ou une Series vers un fichier Excel (.xlsx).

        Parameters
        ----------
        table : pandas.DataFrame or pandas.Series
            Table de données à exporter.
        path : str
            Chemin d'accès du fichier Excel à créer.

        Returns
        -------
        bool
            True si l'export a réussi, False sinon.

        Raises
        ------
        TypeError
            Si la table n'est pas un DataFrame ou une Series,
            ou si le path n'est pas une chaîne.
        """
        if not isinstance(table, (pd.DataFrame, pd.Series)):
            raise TypeError(
                "Seules les tables de types pd.DataFrame"
                " ou pd.Series peuvent être exportées"
            )
        if not isinstance(path, str):
            raise TypeError(
                "Le chemin de sauvegarde (path)"
                " doit être une chaîne de caractères (str)."
            )
        try:
            path = self._normalize_path(path)
            if isinstance(table, pd.Series):
                table = table.to_frame()
            table.to_excel(path, index=False)
            return True
        except Exception as e:
            print(f"Erreur lors de l'export Excel : {e}")
            return False

    def export_to_jpg(self, img, path) -> bool:
        """
        Exporte une figure matplotlib vers un fichier JPG.

        Parameters
        ----------
        img : matplotlib.figure.Figure
            Graphique à exporter.
        path : str
            Chemin d'accès du fichier JPG à créer.

        Returns
        -------
        bool
            True si l'export a réussi, False sinon.

        Raises
        ------
        TypeError
            Si l'objet img n'est pas une figure matplotlib,
            ou si le path n'est pas une chaîne.
        """
        if not isinstance(img, plt.Figure):
            raise TypeError(
                "Seules les graphiques faits"
                " avec matplotlib peuvent être exportés"
            )
        if not isinstance(path, str):
            raise TypeError(
                "Le chemin de sauvegarde (path)"
                " doit être une chaîne de caractères (str)."
            )
        try:
            path = self._normalize_path(path)
            img.savefig(path, format='jpg')
            return True
        except Exception as e:
            print(f"Erreur lors de l'export JPG : {e}")
            return False

    def export_to_png(self, img, path) -> bool:
        """
        Exporte une figure matplotlib vers un fichier PNG.

        Parameters
        ----------
        img : matplotlib.figure.Figure
            Graphique à exporter.
        path : str
            Chemin d'accès du fichier PNG à créer.

        Returns
        -------
        bool
            True si l'export a réussi, False sinon.

        Raises
        ------
        TypeError
            Si l'objet img n'est pas une figure matplotlib,
            ou si le path n'est pas une chaîne.
        """
        if not isinstance(img, plt.Figure):
            raise TypeError(
                "Seules les graphiques faits"
                " avec matplotlib peuvent être exportés"
            )
        if not isinstance(path, str):
            raise TypeError(
                "Le chemin de sauvegarde (path)"
                " doit être une chaîne de caractères (str)."
            )
        try:
            path = self._normalize_path(path)
            img.savefig(path, format='png')
            return True
        except Exception as e:
            print(f"Erreur lors de l'export PNG : {e}")
            return False
