"""
Module core du projet LogLens.

Contient les fonctionnalités principales pour:
- Analyse de fichiers de logs
- Détection d'anomalies
- Génération de résumés en langage naturel
"""

__version__ = '1.0.0'

# Importer les modules pour faciliter leur utilisation
from . import parser
from . import detector
from . import summarizer
from . import utils
