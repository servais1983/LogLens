"""
Module de parsing des fichiers de logs.

Contient des fonctions pour lire et extraire les entrées pertinentes
de différents types de fichiers de logs.
"""

import os
import re
from datetime import datetime
from .utils import log_info, log_error

# Mots-clés importants à identifier dans les logs
KEYWORDS = [
    "failed", "failure", "denied", "error", "refused", "invalid", 
    "unauthorized", "warning", "rejected", "suspicious", "attack",
    "violation", "intrusion", "malware", "exploit", "breach",
    "brute force", "connection", "authentication"
]

def parse_log(filepath):
    """
    Parse un fichier de log et extrait les entrées pertinentes.
    
    Args:
        filepath (str): Chemin vers le fichier de log à analyser
        
    Returns:
        list: Liste des entrées de log pertinentes
    """
    log_info(f"Analyse du fichier: {filepath}")
    
    # Déterminer le type de log en fonction de l'extension ou du nom
    log_type = detect_log_type(filepath)
    log_info(f"Type de log détecté: {log_type}")
    
    # Utiliser le parser approprié
    if log_type == "syslog":
        return parse_syslog(filepath)
    elif log_type == "auth":
        return parse_auth_log(filepath)
    elif log_type == "windows":
        return parse_windows_event(filepath)
    else:
        return parse_generic_log(filepath)

def detect_log_type(filepath):
    """
    Détecte le type de log en fonction du nom du fichier.
    
    Args:
        filepath (str): Chemin vers le fichier de log
        
    Returns:
        str: Type de log détecté ('syslog', 'auth', 'windows', 'generic')
    """
    filename = os.path.basename(filepath).lower()
    
    if "syslog" in filename or "system" in filename:
        return "syslog"
    elif "auth" in filename or "secure" in filename:
        return "auth"
    elif "windows" in filename or "event" in filename or ".evt" in filename:
        return "windows"
    else:
        # Tenter de détecter par inspection du contenu
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                first_lines = [f.readline() for _ in range(5) if f.readline()]
                content = "".join(first_lines)
                
                if re.search(r"\bssh[d]?\b", content) or re.search(r"\bauthentication\b", content):
                    return "auth"
                elif re.search(r"\bEvent ID\b", content) or re.search(r"\bWindows\b", content):
                    return "windows"
                elif re.search(r"\bsystemd\b", content) or re.search(r"\bkernel\b", content):
                    return "syslog"
        except Exception as e:
            log_error(f"Erreur lors de la détection du type de log: {str(e)}")
        
        return "generic"

def parse_generic_log(filepath):
    """
    Parser générique pour tout type de fichier de log.
    
    Args:
        filepath (str): Chemin vers le fichier de log
        
    Returns:
        list: Liste des entrées pertinentes
    """
    entries = []
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if any(keyword in line.lower() for keyword in KEYWORDS):
                    entries.append(line)
    except Exception as e:
        log_error(f"Erreur lors du parsing du fichier {filepath}: {str(e)}")
    
    return entries

def parse_syslog(filepath):
    """
    Parser spécifique pour les logs syslog.
    
    Args:
        filepath (str): Chemin vers le fichier syslog
        
    Returns:
        list: Liste des entrées pertinentes
    """
    return parse_generic_log(filepath)  # Utilise le parser générique pour l'instant

def parse_auth_log(filepath):
    """
    Parser spécifique pour les logs d'authentification.
    
    Args:
        filepath (str): Chemin vers le fichier auth.log
        
    Returns:
        list: Liste des entrées pertinentes
    """
    return parse_generic_log(filepath)  # Utilise le parser générique pour l'instant

def parse_windows_event(filepath):
    """
    Parser spécifique pour les logs d'événements Windows.
    
    Args:
        filepath (str): Chemin vers le fichier d'événements Windows
        
    Returns:
        list: Liste des entrées pertinentes
    """
    return parse_generic_log(filepath)  # Utilise le parser générique pour l'instant
