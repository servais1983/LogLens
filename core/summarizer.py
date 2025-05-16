"""
Module de génération de résumés en langage naturel.

Contient des fonctions pour analyser les anomalies détectées
et générer des résumés compréhensibles en langage naturel.
"""

from collections import Counter
import re
from datetime import datetime
from .utils import log_info

def generate_summary(anomalies):
    """
    Génère un résumé en langage naturel des anomalies détectées.
    
    Args:
        anomalies (list): Liste des anomalies détectées
        
    Returns:
        str: Résumé formaté des anomalies
    """
    log_info(f"Génération d'un résumé pour {len(anomalies)} anomalies")
    
    if not anomalies:
        return "Aucune anomalie critique détectée dans la période analysée."

    # Début du résumé
    summary = "Résumé des événements critiques :\n\n"
    
    # Compter les types d'anomalies
    types = {}
    for a in anomalies:
        t = a["type"]
        types[t] = types.get(t, 0) + 1
    
    # Ajouter les statistiques par type
    for k, v in types.items():
        summary += f"- {v} événement(s) de type '{k}' détecté(s).\n"
    
    # Ajouter des sections plus détaillées pour certains types d'anomalies
    if "Attaque Brute Force" in types:
        summary += "\nDétail des attaques brute force :\n"
        for a in anomalies:
            if a["type"] == "Attaque Brute Force":
                summary += f"- {a['entry']}\n"
    
    # Ajouter une section sur les IPs suspectes
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = []
    
    for a in anomalies:
        entry = a.get("entry", "")
        ip_matches = re.findall(ip_pattern, entry)
        ips.extend(ip_matches)
    
    if ips:
        # Compter les occurrences de chaque IP
        ip_counter = Counter(ips)
        
        # Ajouter les IPs avec le plus d'occurrences
        summary += "\nAdresses IP suspectes :\n"
        for ip, count in ip_counter.most_common(5):
            summary += f"- {ip} : impliquée dans {count} événement(s)\n"
    
    # Ajouter une conclusion
    if len(anomalies) > 10:
        summary += "\nConclusion : Activité suspecte significative détectée, une investigation approfondie est recommandée.\n"
    elif len(anomalies) > 0:
        summary += "\nConclusion : Activité suspecte détectée, une surveillance accrue est recommandée.\n"
    
    return summary

def generate_advanced_summary(anomalies):
    """
    Génère un résumé avancé avec analyse temporelle et identification de schémas.
    Version améliorée qui serait implémentée avec des bibliothèques NLP comme spaCy.
    
    Args:
        anomalies (list): Liste des anomalies détectées
        
    Returns:
        str: Résumé avancé formaté des anomalies
    """
    # Cette fonction serait implémentée dans une version future
    # avec l'intégration de bibliothèques NLP
    
    # Pour l'instant, utiliser la version simple
    return generate_summary(anomalies)

def extract_timestamp(log_entry):
    """
    Tente d'extraire un timestamp d'une entrée de log.
    
    Args:
        log_entry (str): Entrée de log
        
    Returns:
        datetime or None: Objet datetime si un timestamp est trouvé, None sinon
    """
    # Formats de timestamp courants dans les logs
    timestamp_patterns = [
        # May 16 14:32:41
        r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
        # 2023-05-16 14:32:41
        r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
        # 16/May/2023:14:32:41
        r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'
    ]
    
    for pattern in timestamp_patterns:
        match = re.search(pattern, log_entry)
        if match:
            timestamp_str = match.group(1)
            # Tenter de convertir en datetime
            try:
                # Format dépend du pattern trouvé
                if 'May' in timestamp_str and ':' not in timestamp_str.split()[1]:
                    # May 16 14:32:41
                    return datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
                elif '-' in timestamp_str:
                    # 2023-05-16 14:32:41
                    return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                elif '/' in timestamp_str:
                    # 16/May/2023:14:32:41
                    return datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')
            except ValueError:
                continue
    
    return None

def format_time_summary(anomalies):
    """
    Génère un résumé basé sur la distribution temporelle des anomalies.
    
    Args:
        anomalies (list): Liste des anomalies détectées
        
    Returns:
        str: Résumé de la distribution temporelle
    """
    # Cette fonction serait implémentée dans une version future
    return ""
