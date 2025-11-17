@echo off
REM Script de lancement de Tube Effect pour Windows
REM Usage: start.bat

echo =================================
echo    🎬 Tube Effect - Lancement
echo =================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Python n'est pas installé
    echo Installez Python 3.8+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python détecté
python --version
echo.

REM Vérifier si les dépendances sont installées
echo 📦 Vérification des dépendances...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dépendances manquantes détectées
    echo 📥 Installation des dépendances...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
    echo ✓ Dépendances installées avec succès
) else (
    echo ✓ Toutes les dépendances sont installées
)

echo.
echo 🚀 Démarrage de Tube Effect...
echo.

REM Lancer l'application
python Tube_Effect_1.2.py

if errorlevel 1 (
    echo.
    echo ❌ L'application s'est terminée avec une erreur
    pause
    exit /b 1
)

echo.
echo ✓ Application fermée normalement
pause
