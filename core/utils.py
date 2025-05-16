"""
Module d'utilitaires pour LogLens.

Contient des fonctions de support utilisées par les différents modules.
"""

import os
import sys
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('LogLens')

# Couleurs pour les messages de console (ANSI)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_info(message):
    """
    Log un message d'information.
    
    Args:
        message (str): Message à logger
    """
    logger.info(message)

def log_warning(message):
    """
    Log un message d'avertissement.
    
    Args:
        message (str): Message à logger
    """
    logger.warning(message)

def log_error(message):
    """
    Log un message d'erreur.
    
    Args:
        message (str): Message à logger
    """
    logger.error(message)

def get_timestamp():
    """
    Retourne l'horodatage actuel au format ISO.
    
    Returns:
        str: Horodatage au format ISO
    """
    return datetime.now().isoformat()

def ensure_dir(directory):
    """
    S'assure qu'un répertoire existe, le crée si nécessaire.
    
    Args:
        directory (str): Chemin du répertoire
    
    Returns:
        bool: True si le répertoire existe ou a été créé, False sinon
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            return True
        except Exception as e:
            log_error(f"Erreur lors de la création du répertoire {directory}: {str(e)}")
            return False
    return True

def format_bytes(size):
    """
    Formate un nombre d'octets en une chaîne lisible par l'homme (KB, MB, etc.).
    
    Args:
        size (int): Taille en octets
    
    Returns:
        str: Taille formatée
    """
    power = 2 ** 10  # 1024
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    
    while size > power and n < 4:
        size /= power
        n += 1
    
    return f"{size:.2f} {power_labels[n]}B"

def print_colored(message, color=Colors.BLUE):
    """
    Affiche un message coloré dans la console.
    
    Args:
        message (str): Message à afficher
        color (str): Code de couleur ANSI
    """
    print(f"{color}{message}{Colors.ENDC}")

def print_success(message):
    """
    Affiche un message de succès dans la console.
    
    Args:
        message (str): Message à afficher
    """
    print_colored(message, Colors.GREEN)

def print_error(message):
    """
    Affiche un message d'erreur dans la console.
    
    Args:
        message (str): Message à afficher
    """
    print_colored(message, Colors.RED)

def print_warning(message):
    """
    Affiche un message d'avertissement dans la console.
    
    Args:
        message (str): Message à afficher
    """
    print_colored(message, Colors.WARNING)

def count_lines(file_path):
    """
    Compte le nombre de lignes dans un fichier.
    
    Args:
        file_path (str): Chemin du fichier
    
    Returns:
        int: Nombre de lignes
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception as e:
        log_error(f"Erreur lors du comptage des lignes de {file_path}: {str(e)}")
        return 0

def get_file_info(file_path):
    """
    Obtient des informations sur un fichier.
    
    Args:
        file_path (str): Chemin du fichier
    
    Returns:
        dict: Informations sur le fichier
    """
    try:
        stats = os.stat(file_path)
        return {
            'size': stats.st_size,
            'size_human': format_bytes(stats.st_size),
            'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
            'lines': count_lines(file_path)
        }
    except Exception as e:
        log_error(f"Erreur lors de l'obtention des informations sur {file_path}: {str(e)}")
        return {}
