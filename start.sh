#!/bin/bash

# Script de lancement de Tube Effect
# Usage: ./start.sh

echo "================================="
echo "   🎬 Tube Effect - Lancement   "
echo "================================="
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null
then
    echo "❌ Erreur: Python n'est pas installé"
    echo "Installez Python 3.8+ depuis https://www.python.org/"
    exit 1
fi

# Utiliser python3 si disponible, sinon python
if command -v python3 &> /dev/null
then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "✓ Python détecté: $($PYTHON_CMD --version)"
echo ""

# Vérifier si les dépendances sont installées
echo "📦 Vérification des dépendances..."
if ! $PYTHON_CMD -c "import PyQt6" 2>/dev/null
then
    echo "⚠️  Dépendances manquantes détectées"
    echo "📥 Installation des dépendances..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'installation des dépendances"
        exit 1
    fi
    echo "✓ Dépendances installées avec succès"
else
    echo "✓ Toutes les dépendances sont installées"
fi

echo ""
echo "🚀 Démarrage de Tube Effect..."
echo ""

# Lancer l'application
$PYTHON_CMD Tube_Effect_1.2.py

# Vérifier le code de sortie
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ L'application s'est terminée avec une erreur"
    exit 1
fi

echo ""
echo "✓ Application fermée normalement"
