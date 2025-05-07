import pandas as pd
import numpy as np
from scipy.stats import norm
import warnings
from copy import deepcopy


class LinearRegression:
    """
    Régression linéaire multiple manuelle avec prise en charge des variables
    catégorielles, détection de multicolinéarité,
    validation croisée et régularisation Ridge.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        y_var: list,
        x_vars: list,
        seuil: float = 0.05,
        fit_intercept: bool = True,
    ):
        """
        Initialise la classe LinearRegression.

        Parameters
        ----------
        df : pd.DataFrame
            Jeu de données initial.
        y_var : list of str
            Liste contenant le nom de la variable cible.
        x_vars : list of str
            Liste des noms des variables explicatives.
        seuil : float, optional
            Niveau alpha pour les intervalles de confiance (default: 0.05).
        fit_intercept : bool, optional
            Indique si un terme d'intercept est ajouté (default: True).
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "La base de données fournie en paramètre doit être de type pd.DataFrame"
            )

        if not isinstance(y_var, list) or not isinstance(x_vars, list):
            raise TypeError("y_var et x_vars doivent être des listes")

        if any(not isinstance(x_var, str) for x_var in x_vars):
            raise TypeError("x_vars doit contenir des élements de types str")
        if len(x_vars) <= 0:
            raise ValueError("x_vars doit contenir au moins un élement")

        if any(not isinstance(x_var, str) for x_var in x_vars):
            raise TypeError("x_vars doit contenir des élements de types str")

        if len(y_var) != 1:
            raise ValueError("y_var doit contenir exactement un élement")

        if not isinstance(y_var[0], str):
            raise TypeError("y_var doit contenir un élement de type str")

        if any(var not in df.columns for var in y_var + x_vars):
            raise ValueError("x_vars et y_var doivent être parmis les colonnes de df")

        if not isinstance(seuil, float):
            raise TypeError("Le seuil doit être un nombre réel")

        if not isinstance(fit_intercept, bool):
            raise TypeError("fit_intercept doit être un bool")

        self.df = deepcopy(df).dropna(subset=y_var + x_vars).reset_index(drop=True)
        self.y_var = y_var
        self.x_vars = x_vars
        self.seuil = seuil
        self.fit_intercept = fit_intercept
        self.X, self.y = self.create_x_y()

    def create_x_y(self):
        """
        Crée les matrices X et y avec gestion des NA,
        des variables catégorielles et de l'intercept.

        Returns
        -------
        X : pd.DataFrame
            Matrice des variables explicatives.
        y : np.ndarray
            Vecteur cible.
        """
        df = self.df[self.y_var + self.x_vars].dropna().reset_index(drop=True)
        dummies = pd.DataFrame()
        x_vars_clean = []

        for x in self.x_vars:
            if df[x].dtype in ["object", "category"]:
                dummies_x = self.get_dummies(
                    df, variable=x, delete_var=True, drop_first=True
                )
                dummies = pd.concat([dummies, dummies_x], axis=1)
            else:
                x_vars_clean.append(x)

        var = pd.concat([df.loc[:, x_vars_clean], dummies], axis=1)

        if self.fit_intercept:
            intercept = pd.DataFrame(np.ones((df.shape[0], 1)), columns=["intercept"])
            X_ = pd.concat([intercept, var], axis=1)
        else:
            X_ = var

        y = df[self.y_var].values.reshape((-1, 1))

        return X_, y

    def get_dummies(
        self,
        df: pd.DataFrame,
        variable: str,
        delete_var: bool = False,
        drop_first: bool = False,
    ):
        """
        Effectue le one-hot encoding d'une variable catégorielle.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame source.
        variable : str
            Nom de la variable catégorielle.
        delete_var : bool
            Si True, supprime la variable d'origine.
        drop_first : bool
            Si True, ignore la première modalité (pour éviter la colinéarité).

        Returns
        -------
        pd.DataFrame
            DataFrame contenant les colonnes dummies.
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "La base de données fournie en paramètre doit être de type pd.DataFrame"
            )

        if not isinstance(variable, str):
            raise TypeError("L'argument variable doit être de type str")

        if not isinstance(delete_var, bool):
            raise TypeError("L'argument delete_var doit être un booléen")

        if not isinstance(drop_first, bool):
            raise TypeError("L'argument drop_first doit être un booléen")

        if variable not in df.columns:
            raise ValueError(
                "La variable spécifiée n'existe pas dans la base de données"
            )

        df = self.df.dropna(subset=[variable])
        modalities = sorted(df[variable].unique())

        if drop_first:
            modalities = modalities[1:]

        for mod in modalities:
            df[f"{variable}_{mod}"] = (df[variable] == mod).astype(int)

        if delete_var:
            df.drop(columns=[variable], inplace=True)
            return df[[col for col in df.columns if col.startswith(f"{variable}_")]]

        return pd.concat(
            [
                df[variable],
                df[[col for col in df.columns if col.startswith(f"{variable}_")]],
            ],
            axis=1,
        )

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Estime les coefficients de régression par OLS.

        Parameters
        ----------
        X : np.ndarray
            Matrice des prédicteurs.
        y : np.ndarray
            Vecteur cible.

        Returns
        -------
        np.ndarray
            Coefficients estimés.
        """
        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            raise TypeError("X et Y doivent-être de type np.ndarray")

        cond_number = np.linalg.cond(X.T @ X)
        if cond_number > 1e10:
            warnings.warn(
                "Matrice X.T @ X mal conditionnée (cond > 1e10)."
                "Risque de multicolinéarité."
            )

        X_X_inv = np.linalg.pinv(X.T @ X)
        Beta = X_X_inv @ X.T @ y
        return Beta

    def fit_ridge(self, X: np.ndarray, y: np.ndarray, alpha: float = 1.0):
        """
        Estime les coefficients via la régression Ridge.

        Parameters
        ----------
        X : np.ndarray
            Matrice des prédicteurs.
        y : np.ndarray
            Vecteur cible.
        alpha : float
            Paramètre de régularisation.

        Returns
        -------
        np.ndarray
            Coefficients estimés.
        """

        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            raise TypeError("X et Y doivent-être de type np.ndarray")

        n_variables = X.shape[1]
        I_ = np.eye(n_variables)
        if self.fit_intercept:
            I_[0, 0] = 0

        Beta = np.linalg.inv(X.T @ X + alpha * I_) @ X.T @ y
        return Beta

    def compute_confidence_interval(
        self, X: np.ndarray, Y: np.ndarray, Y_hat: np.ndarray, Beta: np.ndarray
    ):
        """
        Calcule les intervalles de confiance des coefficients.

        Parameters
        ----------
        X : np.ndarray
        Y : np.ndarray
        Y_hat : np.ndarray
        Beta : np.ndarray

        Returns
        -------
        pd.DataFrame
            DataFrame avec estimations et bornes d'intervalles.
        """
        if (
            not isinstance(X, np.ndarray)
            or not isinstance(Y, np.ndarray)
            or not isinstance(Y_hat, np.ndarray)
            or not isinstance(Beta, np.ndarray)
        ):
            raise TypeError("X, Y, Y_hat et Beta doivent-être de type np.ndarray")

        epsilon = Y - Y_hat
        n, p = X.shape
        var_epsilon = ((epsilon.T @ epsilon) / (n - p))[0][0]
        beta_var_matrix = var_epsilon * np.linalg.pinv(X.T @ X)
        ecart_type_beta = np.sqrt(np.diag(beta_var_matrix)).reshape(-1, 1)
        quantile = norm.ppf(1 - self.seuil / 2)

        borne_inf = Beta - quantile * ecart_type_beta
        borne_sup = Beta + quantile * ecart_type_beta

        return pd.DataFrame(
            {
                "Estimation": Beta.flatten(),
                "Borne inférieure": borne_inf.flatten(),
                "Borne supérieure": borne_sup.flatten(),
            }
        )

    def compute_rmse(self, y_true, y_pred):
        """
        Calcule la racine de l'erreur quadratique moyenne (RMSE).

        Parameters
        ----------
        y_true : np.ndarray
        y_pred : np.ndarray

        Returns
        -------
        float
            RMSE
        """
        if not isinstance(y_true, np.ndarray) or not isinstance(y_pred, np.ndarray):
            raise TypeError("y_true et y_pred doivent-être de type np.ndarray")

        return np.sqrt(np.mean((y_true - y_pred) ** 2))

    def predict(self, X, Beta):
        """
        Prédit la variable cible.

        Parameters
        ----------
        X : np.ndarray
        Beta : np.ndarray

        Returns
        -------
        np.ndarray
            Prédictions
        """
        if not isinstance(X, np.ndarray):
            raise TypeError("X doit être un np.ndarray")
        return X @ Beta

    def perfom_linear_reg(self, use_ridge=False, alpha=1.0):
        """
        Réalise la régression complète avec ou sans Ridge.

        Parameters
        ----------
        use_ridge : bool, optional
            Utiliser Ridge Regression si True (default: False).
        alpha : float, optional
            Paramètre de pénalisation Ridge (default: 1.0).

        Returns
        -------
        dict
            Résultats incluant : estimation, prédictions, RMSE.
        """
        if not isinstance(use_ridge, bool):
            raise TypeError("use_ridge doit être de type booléen")
        if not isinstance(alpha, float):
            raise TypeError("use_ridge doit être de type float")

        X_matrix = self.X.values if isinstance(self.X, pd.DataFrame) else self.X
        y_vector = self.y

        if use_ridge:
            Beta = self.fit_ridge(X_matrix, y_vector, alpha=alpha)
        else:
            Beta = self.fit(X_matrix, y_vector)

        y_hat = self.predict(X_matrix, Beta)
        estimation = self.compute_confidence_interval(X_matrix, y_vector, y_hat, Beta)
        epsilon = y_vector - y_hat
        estimation = pd.concat(
            [pd.DataFrame({"Variable": self.X.columns}), estimation], axis=1
        )

        return {
            "estimation_results": estimation,
            "y_pred": y_hat,
            "epsilon": epsilon,
            "rmse": self.compute_rmse(y_vector, y_hat),
        }

    def create_k_fold(self, k):
        """
        Crée les k sous-échantillons pour validation croisée.

        Parameters
        ----------
        k : int
            Nombre de folds.

        Returns
        -------
        list of np.ndarray
            Liste de folds contenant les données.
        """

        if not isinstance(k, int):
            raise TypeError("k doit être un entier")

        df_clean = (
            self.df[self.y_var + self.x_vars].dropna().reset_index(drop=True)
        )
        indices = np.random.permutation(len(df_clean))
        fold_size = len(df_clean) // k

        folds = []
        for i in range(k):
            start = i * fold_size
            end = None if i == k - 1 else (i + 1) * fold_size
            fold_idx = indices[start:end]
            fold_x = self.X.iloc[fold_idx, :]
            fold_y = self.y[fold_idx]
            folds.append(np.column_stack((fold_x, fold_y)))
        return folds

    def k_fold(self, k):
        """
        Effectue une validation croisée k-fold avec RMSE.

        Parameters
        ----------
        k : int
            Nombre de folds.

        Returns
        -------
        list of float
            Liste des RMSE pour chaque fold.
        """

        if not isinstance(k, int):
            raise TypeError("k doit être un entier")

        folds = self.create_k_fold(k)
        rmse_scores = []

        for i in range(k):
            test_fold = folds[i]
            train_folds = [folds[j] for j in range(k) if j != i]
            train_data = np.vstack(train_folds)

            X_train, y_train = train_data[:, :-1], train_data[:, -1].reshape(-1, 1)
            X_test, y_test = test_fold[:, :-1], test_fold[:, -1].reshape(-1, 1)

            Beta = self.fit(X_train, y_train)
            y_hat = self.predict(X_test, Beta)
            rmse = self.compute_rmse(y_test, y_hat)
            rmse_scores.append(rmse)

        return rmse_scores
