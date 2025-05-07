# Projet PTD - Traitement de Données NBA

Ce projet a pour objectif d'explorer, traiter et visualiser des données NBA via des notebooks interactifs et une application web simple basée sur **Shiny for Python**.

---

## Installation

Avant toute exécution, il est nécessaire d’installer les dépendances et de configurer l’environnement correctement.

### 1. Cloner le dépôt (si nécessaire)

```bash
git clone <URL_DU_DEPOT>
cd PTD
```

### 2. Installer les dépendances Python

Assurez-vous d'être dans le dossier **racine du projet (PTD)** :

```bash
python -m pip install -r requirements.txt
```

Avant d'installer les packages via la commande ci-avant, il est préférable de créer un environnement virtuel via et de l'activer. La commande pour créer l'environnement virtuel est la suivante :

```bash
python -m venv nom_de_votre_environnement_virtuel
```

Et pour l'activiter, pour les utilisateurs de windows, vous devez faire :

```bash
.\nom_de_votre_environnement_virtuel\Scripts\activate
```

Pour ceux qui utilisent d'autres systèmes d'exploitation, la commande ci-avant devra être ajustée.

### 3. Installation en mode développement

Pour que les sous-dossiers soient reconnus comme des packages Python installables localement, entrer la commande suivante (ne pas oublier le point **.**):

```bash
pip install -e .
```

Cela permet d'importer facilement les modules depuis n'importe quel endroit du projet. Et donc facilitera l'exécution des codes. Cette étape est **importante**.

### 4. Les fichiers *ipynb

Les reponses aux questions se trouvent dans les fichiers ipynb dans le dossier jupyter_files. Une fois les packages et bibliothèques installés, vous pourrez exécuter les chuncks de code de ces fichiers. Un des fichiers portent sur les reponses aux questions et l'autre traite de l'apprentissage automatique.

### 5. Lancer l'application Shiny en local

Vous devrez d'abord avoir **l'extension shiny** installée sur visual studio code. Ensuite vous devrez lancer **app.py** depuis le dossier **application** en cliquant en haut à droite sur le bouton exécuter (ressemble à ça : **|>**), puis **Run Shiny app**.
Si l'appication est lancée via le terminal, vous devrez vous deplacer dans le dossier **application** (`cd application`), puis entrer la commande suivante :

```bash
shiny run app.py --port votre_port_de_4_chiffres
```

On spécifie le port pour eviter d'utiliser un port déjà occupé. Cela empêcherait l'application de démarrer. Pour en savoir plus sur ce que c'est qu'un port [cliquez sur ce lien](https://surfshark.com/fr/blog/quel-est-mon-port).

Si l'application l'application est lancée avec le bouton, un **preview** apparaîtra à droite. Il est possible d'exporter vers un navigateur web. Il est également possible de l'ouvrir dans un navigateur web en cliquant (`Ctrl Entrée`) sur l'**adrresse IP avec le port** (elle ressemble à ça : **127.0.0.1:61567**). Cette dernière possibilité est la seule pour si l'application est lancée depuis le terminal.

### STRUCTURE DU PROJET

```rmd
PTD/
├── answers_class/
|   └── __init__.py
│   └── linear_regression.py
|   └── reponses.py
├── application/
|   └── __init__.py
│   └── app.py
|   └── settings.py
|   └── shared.py
├── donnees_basketball/
|   └── *.csv
├── jupyter_files/
│   ├── reponses_aux_questions.ipynb
│   └── apprentissage_automatique.ipynb
├── logic_for_application/
|   └── __init__.py
│   └── home_func.py
|   └── linear_reg_func.py
|   └── reponses_func.py
├── tests/
│   ├── test_ac_linear_regression.py
│   └── test_application_settings.py
|   └── test_export_files.py
│   └── test_logic_home_func.py
│   └── test_logic_linear_reg_func.py
|   └── test_replace_name.py
│   └── test_reponses.py
├── utils/
│   ├── __init__.py
│   ├── chargement_data.py
│   |── export_files.py
├── requirements.txt
├── setup.py
└── README.md
└── README.html
```
