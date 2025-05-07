import pandas as pd
from answers_class import LinearRegression
import matplotlib.pyplot as plt
from copy import deepcopy


class CareerPrediction:
    """
    Classe pour prédire la durée de carrière (season_exp) d'un joueur.
    Elle traite les colonnes pertinentes, puis applique une régression linéaire.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        use_ridge: bool = False,
        x_vars: list = [],
        alpha: float = 1.0,
        k: int = 5,
    ):
        """
        Initialise la classe CareerPrediction.

        Parameters
        ----------
        data : pd.DataFrame
            Jeu de données des joueurs.
        use_ridge : bool, optional
            Utiliser Ridge Regression si True (default: False).
        alpha : float, optional
            Paramètre de régularisation Ridge (default: 1.0).
        k : int, optional
            Nombre de folds pour la validation croisée (default: 3).
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Le paramètre data doit être un pd.DataFrame")

        self.data = deepcopy(data)
        self.use_ridge = use_ridge  # Ajouter le paramètre use_ridge
        self.alpha = alpha  # Paramètre de régularisation Ridge
        self.model = None
        self.X = None
        self.y = None
        self.y_var = ["season_exp"]
        self.x_vars = x_vars
        self.X_clean = None
        self.k = k

        self.prepare_data()

    def prepare_data(self):
        """
        Prépare les données en nettoyant et en traitant les colonnes pertinentes.
        """
        # Traiter les variables catégorielles et les variables numériques
        self.data["draft_year"] = pd.to_numeric(
            self.data["draft_year"], errors="coerce"
        )  # Convertir en numérique
        self.data["draft_year"] = self.data["draft_year"].fillna(
            0
        )  # 'undrafted' -> NaN -> 0

        self.data = self.data[self.data["to_year"] <= 2022]

        self.data["birth_year"] = pd.to_numeric(
            self.data["birthdate"].apply(lambda x: x[:4])
        )

        self.data["draft_year"] = pd.to_numeric(
            self.data["draft_year"], errors="coerce"
        )

        self.data["age_at_draft"] = (
            self.data["draft_year"] - self.data["birth_year"]
        )  # Âge au moment du draft

        self.data = self.data[
            self.data["age_at_draft"] > 0
        ]  # Filtrer les joueurs avec un âge valide au moment du draft

        # Sélectionner les variables explicatives
        self.x_vars = ["age_at_draft", "position"]  # Âge au moment du draft  # Position

        # Créer une instance de modèle de régression linéaire
        self.model = LinearRegression(
            df=self.data,
            y_var=self.y_var,
            x_vars=self.x_vars,
            seuil=0.05,
            fit_intercept=True,
        )

    def run_regression(self):
        """
        Applique la régression linéaire et retourne les résultats.

        Parameters
        ----------
        y_var : list of str
            La variable cible à prédire.
        x_vars : list of str
            Les variables explicatives à utiliser pour la régression.

        Returns
        -------
        dict
            Les résultats de la régression (coefficients, RMSE, etc.).
        """

        x_vars = ["age_at_draft", "position"]
        # Créer une instance du modèle de régression
        self.model = LinearRegression(
            df=self.data,
            y_var=self.y_var,
            x_vars=x_vars,
            seuil=0.05,
            fit_intercept=True,
        )

        # Effectuer la régression en fonction de use_ridge
        if self.use_ridge:
            results = self.model.perfom_linear_reg(use_ridge=True, alpha=self.alpha)
        else:
            results = self.model.perfom_linear_reg(use_ridge=False)

        return results

    def plot_k_fold(self):
        """
        Génère et retourne un graphique de la performance (RMSE)
        en fonction des folds dans une validation croisée k-fold.
        """
        # Effectuer la validation croisée k-fold pour obtenir les valeurs de RMSE
        list_rmse = self.model.k_fold(k=self.k)

        # Créer les valeurs pour l'axe X (les valeurs de k)
        k_values = range(1, self.k + 1)

        # Créer un objet figure
        fig, ax = plt.subplots(figsize=(8, 6))

        # Tracer la courbe avec les valeurs de k et les RMSE
        ax.plot(k_values, list_rmse, marker="o", linestyle="-", color="b", label="RMSE")

        # Ajouter un titre et des labels
        ax.set_title(f"Validation Croisée k-fold (k={self.k})", fontsize=16)
        ax.set_xlabel("Fold (k)", fontsize=12)
        ax.set_ylabel("RMSE", fontsize=12)

        # Ajouter une grille et une légende
        ax.grid(True)
        ax.legend(loc="upper right")

        # Retourner l'objet figure (au lieu d'afficher directement)
        return fig

    def predict_career_duration(
        self,
        birthdate="2022-01-01",
        draft_year="2022-01-01",
        position="Center",
        coef_df="",
    ):
        """
        Prédit la durée de la carrière d'un joueur en fonction de ses caractéristiques.

        Parameters
        ----------
        birthdate : str
            La date de naissance du joueur (format 'YYYY-MM-DD').
        draft_year : int
            L'année du draft du joueur.
        position : str
            La position du joueur (ex: 'Guard', 'Forward', etc.).
        coef_df : pd.DataFrame
            Le DataFrame contenant les coefficients et les bornes de
            confiance pour chaque variable.

        Returns
        -------
        dict
            La durée de carrière prédite et l'intervalle de confiance.
        """
        # Transformation des données
        birth_year = int(str(birthdate)[:4])
        draft_year = int(str(draft_year)[:4])
        age_at_draft = draft_year - birth_year

        if age_at_draft <= 0:
            raise ValueError("Âge au moment de la draft invalide.")

        # Initialisation des features
        features = {
            "birth_year": birth_year,
            "draft_year": draft_year,
            "age_at_draft": age_at_draft,
            "position": position
        }

        # Ajouter les variables de position sauf 'Center' (référence)
        for var in coef_df["Variable"]:
            if var.startswith("position_"):
                expected_position = var.replace("position_", "")
                features[var] = 1.0 if position == expected_position else 0.0

        # Ajout de l'intercept
        intercept_row = coef_df[coef_df["Variable"] == "intercept"]
        y_pred = (
            float(intercept_row["Estimation"].iloc[0])
            if not intercept_row.empty
            else 0.0
        )
        lower = (
            float(intercept_row["Borne inférieure"].iloc[0])
            if not intercept_row.empty
            else 0.0
        )
        upper = (
            float(intercept_row["Borne supérieure"].iloc[0])
            if not intercept_row.empty
            else 0.0
        )

        # Contribution des autres variables
        for _, row in coef_df.iterrows():
            var = row["Variable"]
            if var == "intercept":
                continue  # intercept déjà pris en compte
            coef = row["Estimation"]
            ci_low = row["Borne inférieure"]
            ci_high = row["Borne supérieure"]
            x = features.get(var, 0.0)
            y_pred += coef * x
            lower += ci_low * x
            upper += ci_high * x

        return {"duree_predite": y_pred, "intervalle_confiance": (lower, upper)}
