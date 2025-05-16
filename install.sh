#!/bin/bash
# Script d'installation pour LogLens

echo "
╭───────────────────────────────────────────╮
│                                           │
│            🧿  LogLens v1.0.0             │
│        Auditeur intelligent de logs       │
│                                           │
╰───────────────────────────────────────────╯
"

echo "[*] Installation de LogLens..."

# Vérifier si Python 3 est installé
if command -v python3 &>/dev/null; then
    echo "[✓] Python 3 trouvé."
else
    echo "[!] Python 3 non trouvé. Installation..."
    
    # Détection du gestionnaire de paquets
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v yum &>/dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -S python python-pip
    elif command -v brew &>/dev/null; then
        brew install python
    else
        echo "[!] Impossible d'installer Python automatiquement."
        echo "    Veuillez l'installer manuellement: https://www.python.org/downloads/"
        exit 1
    fi
fi

# Vérifier la version de Python
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "[*] Version Python: $python_version"

# Installer les dépendances
echo "[*] Installation des dépendances..."

# Vérifier si pip est installé
if command -v pip3 &>/dev/null; then
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[!] Erreur lors de l'installation des dépendances."
        exit 1
    fi
else
    echo "[!] pip3 non trouvé. Installation..."
    
    # Détection du gestionnaire de paquets
    if command -v apt &>/dev/null; then
        sudo apt install -y python3-pip
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3-pip
    elif command -v yum &>/dev/null; then
        sudo yum install -y python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -S python-pip
    elif command -v brew &>/dev/null; then
        brew install python
    else
        echo "[!] Impossible d'installer pip automatiquement."
        echo "    Veuillez l'installer manuellement: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
    
    pip3 install -r requirements.txt
fi

# Rendre le script principal exécutable
chmod +x loglens.py

echo "[✓] LogLens installé avec succès!"
echo ""
echo "Pour analyser un fichier de log, utilisez la commande suivante:"
echo "  python3 loglens.py --logfile /chemin/vers/fichier.log"
echo ""
echo "Exemples:"
echo "  python3 loglens.py --logfile /var/log/auth.log"
echo "  python3 loglens.py --logfile /var/log/syslog"
echo "  python3 loglens.py --logfile /var/log/secure"
echo ""
echo "Pour plus d'options:"
echo "  python3 loglens.py --help"
