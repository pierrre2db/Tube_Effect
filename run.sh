#!/bin/bash
# Script de lancement pour Tube Effect v2.1.0

echo "🚀 Lancement de Tube Effect v2.1.0"
echo "===================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python 3 trouvé: $(python3 --version)"

# Vérifier les dépendances
echo ""
echo "📦 Vérification des dépendances..."

if python3 -c "import PyQt6" 2>/dev/null; then
    echo "✅ PyQt6 installé"
else
    echo "⚠️  PyQt6 manquant - Installation..."
    pip3 install PyQt6>=6.4.0
fi

if python3 -c "import cv2" 2>/dev/null; then
    echo "✅ OpenCV installé"
else
    echo "⚠️  OpenCV manquant - Installation..."
    pip3 install opencv-python>=4.8.0
fi

if python3 -c "import numpy" 2>/dev/null; then
    echo "✅ NumPy installé"
else
    echo "⚠️  NumPy manquant - Installation..."
    pip3 install numpy>=1.24.0
fi

# Lancer l'application
echo ""
echo "🎬 Lancement de l'application..."
echo ""
python3 Tube_Effect_1.2.py

exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo ""
    echo "❌ L'application s'est terminée avec une erreur (code: $exit_code)"
    exit $exit_code
fi
