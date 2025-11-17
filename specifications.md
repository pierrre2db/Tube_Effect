# Document de Spécifications Produit Développeur - Créateur d'Animation
## Version : 2.0
## Date : 13/06/2025
## Auteur : Cascade (basé sur la spécification originale de Gemini)
## Statut : Implémentation en cours

---

## 1. Introduction

### 1.1. Objectif du Document
Ce document définit les spécifications techniques et fonctionnelles du logiciel "Tube Effect", une application de création d'animations vidéo avec effet de projecteur. Il sert de référence pour le développement et la maintenance de l'application.

### 1.2. État d'Avancement
- [x] Gestion de projet (FP-01)
- [x] Édition de trajet (FP-02)
- [x] Paramétrage de l'animation (FP-03)
- [x] Exportation vidéo (FP-05)
- [x] Effets visuels multiples (FP-07)
- [x] Effet de lentille/loupe (FP-08)
- [ ] Prévisualisation en temps réel (FP-04)
- [ ] Gestion des préférences utilisateur (FP-06)

### 1.3. Glossaire
- **Point de Contrôle** : Point éditable sur la scène (position x,y + taille)
- **Effet Projecteur** : Zone éclairée se déplaçant sur un fond assombri
- **Effet Lentille** : Zone avec effet de loupe/zoom magnifiant le contenu
- **Scène** : Zone d'affichage principale de l'image et du tracé
- **Profil d'Export** : Paramètres prédéfinis pour la résolution vidéo
- **Facteur de Zoom** : Intensité de l'agrandissement pour l'effet lentille (100-300%)

---

## 2. Architecture Technique

### 2.1. Pile Technologique
- **Langage** : Python 3.10+
- **Bibliothèques Principales** :
  - Interface : PyQt6
  - Traitement d'image : OpenCV 4.8+

### 2.2. Structure du Code
```
Tube_Effect/
├── main.py                  # Point d'entrée
├── core/
│   ├── path_editor.py      # Gestion des tracés
│   ├── animation_worker.py # Rendu vidéo
│   └── models.py           # Modèles de données
├── ui/
│   ├── main_window.py      # Interface principale
│   └── dialogs.py          # Boîtes de dialogue
└── utils/
    ├── file_handlers.py    # Gestion des fichiers
    └── video_export.py     # Exportation vidéo
```

---

## 3. Spécifications Techniques Détail

### 3.1. Gestion des Trajectoires
- **Implémentation** : Classe `PathEditor`
- **Fonctionnalités** :
  - Ajout/suppression de points
  - Déplacement par glisser-déposer
  - Lissage des courbes de Bézier
  - Gestion des poignées de contrôle

### 3.2. Moteur de Rendu
- **Classe** : `AnimationWorker(QThread)`
- **Caractéristiques** :
  - Traitement asynchrone
  - Gestion de la progression
  - Support de l'annulation
  - Calcul optimisé des frames

### 3.3. Formats Supportés
- **Images** : PNG, JPG, BMP
- **Vidéo** : MP4 (H.264)
- **Projets** : JSON

---

## 4. Interface Utilisateur

### 4.1. Barre d'Outils
- Charger/Enregistrer projet
- Préférences
- Aide

### 4.2. Panneau de Contrôle
- **Forme** : Cercle/Carré
- **Effet** : Projecteur/Lentille/Projecteur + Lentille
- **Zoom Lentille** : 100-300%
- **Taille** : 20-500px
- **Vitesse** : 20-1000 px/s
- **Luminosité** : 0-100%
- **Lissage** : 0-100%
- **FPS** : 15/24/25/30/50/60

### 4.3. Zone de Visualisation
- Affichage de l'image
- Édition des points
- Aperçu en temps réel

---

## 5. Flux de Travail

1. Charger une image
2. Définir les points de contrôle
3. Ajuster les paramètres
4. Prévisualiser
5. Exporter la vidéo

---

## 6. Tests et Validation

### 6.1. Tests Unitaires
- Gestion des points
- Calcul des trajectoires
- Export vidéo

### 6.2. Tests d'Intégration
- Flux complet d'exportation
- Gestion des erreurs
- Performance

---

## 7. Dépendances

```python
# requirements.txt
PyQt6>=6.4.0
opencv-python>=4.8.0
numpy>=1.24.0
```

---

## 8. Notes d'Implémentation

### 8.1. Points Clés
- Architecture modulaire
- Gestion asynchrone
- Gestion des erreurs

### 8.2. Améliorations Futures
- Support des calques
- Effets supplémentaires (flou, distorsion, etc.)
- Export GIF
- Effet de lentille avec distorsion fisheye
- Prévisualisation temps réel optimisée

---

## 9. Journal des Modifications

| Version | Date       | Description                     |
|---------|------------|---------------------------------|
| 1.0     | 10/06/2025 | Version initiale                |
| 1.1     | 12/06/2025 | Ajout du lissage des courbes    |
| 2.0     | 13/06/2025 | Refonte complète de l'interface |
| 2.1     | 17/11/2025 | Ajout des effets de lentille/loupe avec zoom configurable (100-300%) |

---

*Document généré automatiquement - Dernière mise à jour : 13/06/2025 12:42*
