"""
Module de détection d'anomalies dans les logs.

Contient des fonctions pour analyser les entrées de logs
et identifier les anomalies de sécurité potentielles.
"""

import re
from .utils import log_info

# Définition des patterns d'anomalies
PATTERNS = {
    "Échec Auth": [
        r"failed password",
        r"authentication failure",
        r"login failed",
        r"auth failure",
        r"incorrect password",
        r"unauthorized login",
        r"no matching credentials"
    ],
    "Échec RDP": [
        r"rdp.*failed",
        r"remote desktop.*denied",
        r"terminal service.*error",
        r"rdp.*invalid"
    ],
    "Requête DNS suspecte": [
        r"dns.*suspicious",
        r"unresolved hostname",
        r"dns.*malware",
        r"malicious dns",
        r"unknown dns"
    ],
    "Activité Firewall": [
        r"firewall.*block",
        r"firewall.*deny",
        r"dropped packet",
        r"rejected connection"
    ],
    "Tentative d'Élévation de Privilèges": [
        r"privilege.*escalation",
        r"sudo.*command",
        r"unauthorized.*root",
        r"access denied.*admin"
    ],
    "Scan de Ports": [
        r"port scan",
        r"multiple connection.*attempts",
        r"sequential ports",
        r"rapid connection"
    ],
    "Injection SQL": [
        r"sql injection",
        r"malicious.*query",
        r"injection.*attempt",
        r"invalid sql"
    ]
}

def detect_anomalies(logs):
    """
    Détecte les anomalies dans une liste d'entrées de logs.
    
    Args:
        logs (list): Liste d'entrées de logs à analyser
        
    Returns:
        list: Liste des anomalies détectées avec leur type et l'entrée originale
    """
    log_info(f"Recherche d'anomalies dans {len(logs)} entrées de logs")
    anomalies = []
    
    for entry in logs:
        # Vérifier chaque type d'anomalie
        for anomaly_type, patterns in PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, entry.lower()):
                    anomalies.append({
                        "type": anomaly_type,
                        "entry": entry,
                        "pattern": pattern
                    })
                    # Une fois qu'une anomalie est trouvée pour cette entrée, passer à la suivante
                    break
            else:
                # Continuer à la prochaine anomalie si aucun pattern ne correspond
                continue
            # Sortir de la boucle des types d'anomalies si on a trouvé un match
            break
    
    # Recherche d'anomalies plus spécifiques
    anomalies.extend(detect_brute_force(logs))
    
    return anomalies

def detect_brute_force(logs):
    """
    Détecte les tentatives de brute force en cherchant des échecs d'authentification répétés.
    
    Args:
        logs (list): Liste d'entrées de logs à analyser
        
    Returns:
        list: Liste des anomalies de type brute force détectées
    """
    # Dictionnaire pour compter les tentatives par IP
    ip_attempts = {}
    
    # Regex pour extraire une IP
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    # Chercher les échecs d'authentification et extraire les IPs
    for entry in logs:
        if any(re.search(pattern, entry.lower()) for pattern in PATTERNS["Échec Auth"]):
            ip_match = re.search(ip_pattern, entry)
            if ip_match:
                ip = ip_match.group(0)
                if ip not in ip_attempts:
                    ip_attempts[ip] = []
                ip_attempts[ip].append(entry)
    
    # Identifier les IPs avec plus de 3 tentatives (potentielle attaque de brute force)
    brute_force_anomalies = []
    for ip, attempts in ip_attempts.items():
        if len(attempts) >= 3:
            brute_force_anomalies.append({
                "type": "Attaque Brute Force",
                "entry": f"Multiple tentatives d'authentification depuis {ip} ({len(attempts)} essais)",
                "details": attempts[:3]  # Inclure les 3 premières tentatives comme exemple
            })
    
    return brute_force_anomalies

def detect_unusual_login_times(logs, normal_hours=(8, 18)):
    """
    Détecte les connexions à des heures inhabituelles.
    
    Args:
        logs (list): Liste d'entrées de logs à analyser
        normal_hours (tuple): Plage d'heures de bureau normales (début, fin)
        
    Returns:
        list: Liste des anomalies de connexion à des heures inhabituelles
    """
    # Cette fonctionnalité nécessite une analyse plus avancée des timestamps
    # et sera implémentée dans une version future
    return []
