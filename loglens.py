#!/usr/bin/env python3
"""
LogLens - Auditeur intelligent de logs système

Analyse les fichiers de logs pour détecter des anomalies
et génère un résumé en langage naturel des événements critiques.
"""

import sys
import os
from core import parser, detector, summarizer
import argparse

def banner():
    """Affiche une bannière stylisée de LogLens"""
    print("\n")
    print("╭───────────────────────────────────────────╮")
    print("│                                           │")
    print("│            🧿  LogLens v1.0.0             │")
    print("│        Auditeur intelligent de logs       │")
    print("│                                           │")
    print("╰───────────────────────────────────────────╯")
    print("\n")

def main():
    """Fonction principale du programme"""
    # Afficher la bannière
    banner()
    
    # Configurer les arguments de la ligne de commande
    parser_cli = argparse.ArgumentParser(description="LogLens - Auditeur IA de logs")
    parser_cli.add_argument("--logfile", required=True, help="Fichier de log à analyser")
    parser_cli.add_argument("--verbose", action="store_true", help="Mode verbeux avec plus de détails")
    parser_cli.add_argument("--output", help="Fichier de sortie pour le rapport (optionnel)")
    args = parser_cli.parse_args()

    # Vérifier si le fichier de log existe
    if not os.path.exists(args.logfile):
        print(f"[❌] Erreur: Le fichier {args.logfile} n'existe pas.")
        sys.exit(1)

    print(f"[🔍] Analyse du fichier: {args.logfile}")
    
    # Analyser le fichier de log
    entries = parser.parse_log(args.logfile)
    print(f"[✓] {len(entries)} entrées pertinentes extraites.")
    
    # Détecter les anomalies
    anomalies = detector.detect_anomalies(entries)
    print(f"[✓] {len(anomalies)} anomalies détectées.")
    
    # Générer un résumé
    report = summarizer.generate_summary(anomalies)
    
    # Afficher les résultats
    if anomalies:
        print("\n[🧿] Anomalies détectées :")
        for a in anomalies:
            print(f" - {a['type']} | {a['entry'][:100]}")
    else:
        print("\n[🧿] Aucune anomalie détectée.")

    print("\n[🧠] Résumé automatique :")
    print(report)
    
    # Sauvegarder le rapport si demandé
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write("# Rapport LogLens\n\n")
                f.write("## Anomalies détectées\n\n")
                for a in anomalies:
                    f.write(f"- **{a['type']}**: {a['entry']}\n")
                f.write("\n## Résumé automatique\n\n")
                f.write(report)
            print(f"\n[✓] Rapport enregistré dans {args.output}")
        except Exception as e:
            print(f"[❌] Erreur lors de l'enregistrement du rapport: {str(e)}")

if __name__ == "__main__":
    main()
