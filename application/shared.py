from pathlib import Path
from utils import import_data, replace_old_team_name
import copy

app_dir = Path(__file__).parent
data = import_data(f"{app_dir.parent}/donnees_basketball")

# --------------------- Harmonisation de la base de données ---------------------

# Dictionnaire avec les noms actuelles et passés des franchises

nba_franchises_old_names = {
    "Atlanta Hawks": ["Buffalo Bisons", "Tri-Cities Blackhawks", "Milwaukee Hawks",
                      "St. Louis Hawks"],
    "Boston Celtics": [],  # Aucun ancien nom officiel
    "Brooklyn Nets": ["New Jersey Americans", "New York Nets", "New Jersey Nets"],
    "Charlotte Hornets": ["Charlotte Bobcats"],
    "Chicago Bulls": [],  # Aucun ancien nom
    "Cleveland Cavaliers": [],  # Aucun ancien nom
    "Dallas Mavericks": [],  # Aucun ancien nom
    "Denver Nuggets": ["Denver Larks", "Denver Rockets"],
    "Detroit Pistons": ["Fort Wayne Zollner Pistons", "Fort Wayne Pistons"],
    "Golden State Warriors": ["Philadelphia Warriors", "San Francisco Warriors"],
    "Houston Rockets": ["San Diego Rockets"],
    "Indiana Pacers": [],  # Aucun ancien nom
    "Los Angeles Clippers": ["Buffalo Braves", "San Diego Clippers"],
    "Los Angeles Lakers": ["Detroit Gems", "Minneapolis Lakers"],
    "Memphis Grizzlies": ["Vancouver Grizzlies"],
    "Miami Heat": [],  # Aucun ancien nom
    "Milwaukee Bucks": [],  # Aucun ancien nom
    "Minnesota Timberwolves": [],  # Aucun ancien nom
    "New Orleans Pelicans": ["New Orleans Hornets",
                             "New Orleans/Oklahoma City Hornets"],
    "New York Knicks": [],  # Aucun ancien nom
    "Oklahoma City Thunder": ["Seattle SuperSonics"],
    "Orlando Magic": [],  # Aucun ancien nom
    "Philadelphia 76ers": ["Syracuse Nationals"],
    "Phoenix Suns": [],  # Aucun ancien nom
    "Portland Trail Blazers": [],  # Aucun ancien nom
    "Sacramento Kings": ["Rochester Royals", "Cincinnati Royals",
                         "Kansas City-Omaha Kings", "Kansas City Kings"],
    "San Antonio Spurs": ["Dallas Chaparrals", "Texas Chaparrals"],
    "Toronto Raptors": [],  # Aucun ancien nom
    "Utah Jazz": ["New Orleans Jazz"],
    "Washington Wizards": ["Chicago Packers", "Chicago Zephyrs", "Baltimore Bullets",
                           "Capital Bullets", "Washington Bullets"]
}

df = copy.deepcopy(data["game"])

# Modification de la colonne des équipes à domicile
df = replace_old_team_name(data=df,
                           column="team_name_home",
                           nba_franchises_old_names=nba_franchises_old_names)

# Modification de la colonne des équipes à extérieur
df = replace_old_team_name(data=df,
                           column="team_name_away",
                           nba_franchises_old_names=nba_franchises_old_names)

# Actualisation
data["game"] = df
