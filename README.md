![image](https://github.com/user-attachments/assets/06259356-d2e7-4860-b44d-cee1cc05e3d0)


# 🧿 LogLens – Analyse IA de logs système

LogLens est un outil de ligne de commande conçu pour analyser intelligemment les fichiers de logs système, détecter des anomalies et générer des résumés en langage naturel.

## ⚙️ Fonctionnalités

- **Analyse polyvalente** : Traitement des logs systèmes Linux, journaux Active Directory et fichiers texte génériques
- **Détection d'anomalies** : Identification automatique des échecs d'authentification, tentatives d'accès RDP, requêtes DNS suspectes
- **Résumé intelligent** : Synthèse des événements critiques en langage clair (NLP léger)
- **Interface simple** : Utilisation facile via la ligne de commande

## 📋 Prérequis

- Python 3.6 ou supérieur
- Accès aux fichiers de logs (permissions suffisantes)

## 📥 Installation

```bash
# Cloner le dépôt
git clone https://github.com/servais1983/LogLens.git
cd LogLens

# Rendre le script d'installation exécutable
chmod +x install.sh

# Lancer l'installation
./install.sh
```

## 🚀 Exemple d'utilisation

```bash
# Analyser un fichier de logs d'authentification
python3 loglens.py --logfile /var/log/auth.log

# Analyser un journal d'événements Windows exporté
python3 loglens.py --logfile event_logs.txt 
```

## 📁 Structure du projet

```
loglens/
├── core/
│   ├── parser.py             # Parsing des logs (journalctl, Syslog, etc.)
│   ├── detector.py           # Détection d'anomalies
│   ├── summarizer.py         # Résumé NLP des événements critiques
│   ├── utils.py              # Fonctions de support
├── loglens.py                # Point d'entrée CLI
├── requirements.txt
├── install.sh
└── README.md
```

## 🧠 Prochaines améliorations

* **Intégration Syslog/Journalctl live** : Surveillance en temps réel
* **NLP avancé** : Intégration de spaCy ou modèles GPT pour des analyses plus précises
* **Dashboard web** : Interface graphique avec Streamlit ou FastAPI
* **Corrélation d'événements** : Détection de schémas complexes d'attaques
* **Alertes** : Notification par email ou Slack lors de détection d'anomalies critiques

## 🔍 Exemple de sortie

```
[🧿] Anomalies détectées :
 - Échec Auth | May 16 14:32:41 server sshd[12345]: Failed password for invalid user admin from 192.168.1.100 port 43200
 - Échec Auth | May 16 14:34:22 server sshd[12346]: Failed password for invalid user root from 192.168.1.100 port 43212

[🧠] Résumé automatique :
Résumé des événements critiques :

- 2 événement(s) de type 'Échec Auth' détecté(s).
```

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request pour améliorer l'outil.
