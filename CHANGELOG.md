# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [2.1.0] - 2026-06-12

### 🐛 Corrections de Bugs Critiques

- **Correction indexation poignées Bézier** : Affichage correct des courbes de contrôle - bug majeur corrigé dans `_draw_bezier_handles()`
- **Validation chargement image** : Détection des fichiers corrompus ou invalides avec message d'erreur approprié
- **Gestion robuste des codecs vidéo** : Fallback automatique entre X264, avc1, mp4v, XVID si codec préféré indisponible
- **Arrêt propre des threads** : Ajout de `wait()` pour éviter les fuites mémoire lors de l'annulation d'animations
- **Validation données projet** : Vérification complète de la structure JSON lors du chargement de fichiers

### ✨ Nouvelles Fonctionnalités

- **Suppression de points individuels** : Supprimer un point du tracé avec la touche Delete ou Backspace (survol le point et appuyer sur Delete)
- **Raccourcis clavier** : Ctrl+S (sauvegarder projet), Ctrl+O (ouvrir projet)
- **Messages de feedback améliorés** : Confirmation après sauvegarde et export réussis, messages d'erreur plus clairs
- **Tooltips complets** : Aide contextuelle sur tous les contrôles de l'interface
- **Status bar active** : Affichage de l'état actuel et des actions en cours

### 🎨 Améliorations de l'Interface

- **Format de durée amélioré** : Affichage MM:SS.CS au lieu de MM:SS:FF (centisecondes plus lisibles)
- **Messages d'erreur détaillés** : Erreurs plus claires et informatives avec détails spécifiques
- **Gestion erreurs sauvegarde** : Validation et messages d'erreur lors de la sauvegarde de projets

### ⚡ Optimisations

- **Rendu PathEditor optimisé** : Utilisation d'une liste `path_items` pour suppression rapide des éléments graphiques au lieu de parcourir toute la scène
- **Validation des entrées** : Prévention des valeurs invalides lors du chargement de données
- **Gestion mémoire améliorée** : Nettoyage approprié des ressources graphiques

### 🔧 Corrections Mineures

- **Correction du double division** : Bug dans `update_smoothing()` causant un lissage incorrect
- **Mise à jour numéro de version** : Titre de la fenêtre affiche correctement "Tube Effect v2.1.0"
- **Extension fichiers automatique** : Ajout automatique de `.json` et `.mp4` si omis lors de la sauvegarde

---

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
