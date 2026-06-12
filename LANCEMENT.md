# 🚀 Guide de Lancement - Tube Effect v2.1.0

## Installation et Lancement

### Option 1 : Script Automatique (Recommandé)

```bash
./run.sh
```

### Option 2 : Manuel

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Lancer l'application** :
```bash
python3 Tube_Effect_1.2.py
```

## Utilisation Rapide

### 1️⃣ Charger une Image
- Cliquez sur **"Charger une image"**
- Sélectionnez une image (PNG, JPG, BMP)

### 2️⃣ Créer un Tracé
- **Cliquez** sur l'image pour ajouter des points
- **Maj + Clic** pour déplacer un point existant
- **Survol + Delete** pour supprimer un point

### 3️⃣ Ajuster les Paramètres
- **Forme** : Cercle ou Carré
- **Taille** : Taille du projecteur (20-500px)
- **Vitesse** : Vitesse de déplacement (20-1000 px/s)
- **Luminosité** : Luminosité du fond (0-100%)
- **FPS** : Images par seconde (15-60)
- **Lissage** : Intensité des courbes de Bézier (0-100%)

### 4️⃣ Prévisualiser et Exporter
- **Prévisualiser** : Voir l'animation en temps réel
- **Exporter** : Créer la vidéo MP4 (HD, Full HD, ou 4K)

## 🎹 Raccourcis Clavier (NOUVEAU v2.1.0)

| Touche | Action |
|--------|--------|
| **Ctrl+S** | Sauvegarder le projet |
| **Ctrl+O** | Ouvrir un projet |
| **Delete** | Supprimer le point survolé |

## ✨ Nouveautés v2.1.0

### Corrections de Bugs
- ✅ Courbes de Bézier corrigées
- ✅ Validation des images chargées
- ✅ Fallback automatique des codecs vidéo
- ✅ Meilleure gestion de la mémoire

### Nouvelles Fonctionnalités
- 🆕 Suppression de points individuels (touche Delete)
- 🆕 Raccourcis clavier (Ctrl+S, Ctrl+O)
- 🆕 Tooltips d'aide sur tous les contrôles
- 🆕 Messages de succès après sauvegarde/export

### Améliorations
- ⚡ Interface plus réactive
- ⚡ Messages d'erreur plus clairs
- ⚡ Validation robuste des données

## 🧪 Tests

Pour vérifier l'intégrité de la version :

```bash
python3 test_static.py
```

Ce test vérifie :
- ✅ Syntaxe du code
- ✅ Corrections de bugs
- ✅ Nouvelles fonctionnalités
- ✅ Optimisations

## 🐛 Résolution de Problèmes

### Erreur : "libEGL.so.1: cannot open shared object file"
**Solution** : Installer les bibliothèques graphiques manquantes
```bash
# Ubuntu/Debian
sudo apt-get install libegl1 libxkbcommon-x11-0

# Fedora
sudo dnf install mesa-libEGL
```

### Erreur : "No module named 'PyQt6'"
**Solution** : Installer PyQt6
```bash
pip3 install PyQt6
```

### L'export vidéo échoue
**Solution** : Le codec X264 n'est pas disponible
- L'application essaie automatiquement d'autres codecs (avc1, mp4v, XVID)
- Si tous échouent, installer ffmpeg :
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

## 📞 Support

Pour signaler un bug ou demander une fonctionnalité :
- GitHub Issues : https://github.com/pierrre2db/Tube_Effect/issues

## 📄 Documentation

- [CHANGELOG.md](CHANGELOG.md) : Historique des versions
- [specifications.md](specifications.md) : Spécifications techniques

---

**Tube Effect v2.1.0** - Créé avec ❤️ par Pierre 2DB
