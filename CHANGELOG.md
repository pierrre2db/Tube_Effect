# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [2.0.0] - 2025-11-05

### 🎉 Système d'Effets Multiples

Cette version majeure introduit un système complet d'effets multiples et améliore considérablement l'expérience utilisateur.

### ✨ Nouvelles Fonctionnalités

- **Système d'effets multiples** : Support de plusieurs types d'effets visuels sur vos animations
- **Éditeur de tracé amélioré** : Interface intuitive avec support complet des courbes de Bézier
- **Gestion avancée des points de contrôle** : Ajout, suppression et modification des points avec prévisualisation en temps réel
- **Poignées de contrôle interactives** : Manipulation précise des courbes avec des poignées visuelles
- **Paramètres personnalisables** :
  - Forme du projecteur (Cercle/Carré)
  - Taille ajustable (20-500px)
  - Contrôle de la vitesse (20-1000 px/s)
  - Réglage de la luminosité du fond (0-100%)
  - Options de FPS (15/24/25/30/50/60)

### 🎨 Améliorations de l'Interface

- **Interface PyQt6 moderne** : Refonte complète avec une meilleure ergonomie
- **Zone de visualisation interactive** : Édition directe sur l'image avec retour visuel immédiat
- **Barre de progression** : Suivi détaillé de l'export vidéo
- **Gestion des projets** : Sauvegarde et chargement de vos projets au format JSON

### 🎥 Export Vidéo

- **Qualité professionnelle** : Export jusqu'à 4K
- **Format optimisé** : MP4 avec codec H.264
- **Rendu asynchrone** : Export en arrière-plan sans bloquer l'interface
- **Profils d'export prédéfinis** : Résolutions standards pour tous les usages

### 🔧 Améliorations Techniques

- **Architecture modulaire** : Code restructuré pour une meilleure maintenabilité
- **Classe PathEditor** : Gestion professionnelle des trajectoires
- **AnimationWorker** : Traitement asynchrone des rendus
- **Calcul optimisé** : Performances améliorées pour les animations complexes

### 📦 Formats Supportés

- **Images** : PNG, JPG, BMP
- **Vidéo** : MP4 (H.264)
- **Projets** : JSON

### 🐛 Corrections de Bugs

- Amélioration de la stabilité générale de l'application
- Optimisation de la mémoire lors du traitement de grandes images
- Correction des problèmes de synchronisation lors de l'export

---

## [1.2] - 2025-06-13

### Ajouté
- Support des courbes de Bézier
- Lissage automatique des trajectoires

## [1.1] - 2025-06-12

### Ajouté
- Lissage basique des courbes
- Amélioration de la prévisualisation

## [1.0] - 2025-06-10

### Première Version
- Fonctionnalité de base de l'effet tube
- Export vidéo simple
- Interface utilisateur minimale
