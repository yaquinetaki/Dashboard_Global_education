import requests
import os

RAW_DATA_DIR = os.path.join('data', 'raw')

# Dictionnaire des URLs des fichiers CSV + simple qu'une liste
URLS = {
    "1-basic-education.csv": "https://raw.githubusercontent.com/Yaquine25/global-education-data/refs/heads/main/1-basic-education.csv",
    "2- lays.csv": "https://raw.githubusercontent.com/Yaquine25/global-education-data/refs/heads/main/2-%20lays.csv",
    "3- nbr_out_school_children.csv": "https://raw.githubusercontent.com/Yaquine25/global-education-data/refs/heads/main/3-%20nbr_out_school_children.csv",    
    "4- gender-gap-educ-levels.csv": "https://raw.githubusercontent.com/Yaquine25/global-education-data/refs/heads/main/4-%20gender-gap-educ-levels.csv"
} #clé: nom du fichier, valeur: URL de GITHUB à POSER

def get_data():
    for file_name, url in URLS.items():
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        
        try:
            response = requests.get(url, timeout=30)
            # Vérifie le code de statut HTTP
            response.raise_for_status() 
            # Écriture du fichier
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_name} from {url} ")
        except requests.exceptions.RequestException as e:
            # Gestion des erreurs de connexion, timeout, ou 404/500
            print(f"Failed to download {file_name} from {url}. Error: {e}")

    print("All files processed.")
    return True


if __name__ == '__main__':
    get_data()
