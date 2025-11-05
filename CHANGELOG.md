# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [2.0.0] - 2025-11-05

### 🎉 Version Majeure - Système d'Effets Multiples

### Ajouté

#### Système d'Effets
- **Spotlight Classic** : Effet de projecteur original (cercle/carré)
- **Spotlight avec Glow** : Projecteur avec halo lumineux progressif et contrôle d'intensité
- **Vignette Animée** : Effet d'assombrissement radial inversé suivant le tracé
- **Color Grading** : Application d'une teinte de couleur personnalisable sur le spotlight
- **Zoom/Lens** : Effet de loupe/grossissement avec contrôle d'intensité (0-200%)
- **Blur Focus** : Flou gaussien sur l'arrière-plan, zone nette sur le spotlight
- Système d'effets modulaire avec classe de base `Effect`
- Registre d'effets (`EFFECTS_REGISTRY`) pour faciliter l'ajout de nouveaux effets

#### Interface Utilisateur
- Sélecteur d'effets : Menu déroulant pour choisir parmi les 6 effets disponibles
- Paramètres d'effets dynamiques : L'interface s'adapte automatiquement à l'effet sélectionné
- Contrôles spécifiques par effet :
  - Slider d'intensité du glow (0-100%)
  - Slider de rayon de vignette (50-1000px)
  - Sélecteur de couleur pour le color grading
  - Slider d'intensité de couleur (0-100%)
  - Slider d'intensité de zoom (0-200%)
  - Slider d'intensité de flou (0-100%)
- Fenêtre agrandie (1600x900) pour meilleure ergonomie

#### Édition de Tracé Avancée
- **Undo/Redo** : Historique d'actions avec support de 50 niveaux
- **Suppression de points** :
  - Clic droit sur un point pour le supprimer
  - Touche `Suppr` pour supprimer le point sélectionné
- **Numérotation des points** : Affichage du numéro d'ordre avec fond semi-transparent
- **Gestion de l'historique** : Sauvegarde automatique de l'état à chaque modification
- Méthodes `PathEditor.undo()` et `PathEditor.redo()`
- Méthode `PathEditor.delete_point(index)` pour suppression programmatique
- Méthode `PathEditor.find_point_at(pos, tolerance)` pour détection de points

#### Raccourcis Clavier
- `Ctrl+Z` : Annuler la dernière action
- `Ctrl+Y` : Rétablir l'action annulée
- `Suppr` : Supprimer le point sélectionné
- `Espace` : Lancer/Arrêter la prévisualisation
- `Maj+Clic` : Mode édition (déjà existant, maintenant documenté)

#### Feedback Utilisateur
- Messages dans la barre d'état pour chaque action (undo, redo, suppression)
- Indicateurs visuels améliorés
- Numérotation visible des points du tracé

### Modifié

- Architecture du code refactorisée pour supporter le système d'effets
- `AnimationWorker.create_highlight_frame()` utilise maintenant le système d'effets
- Titre de la fenêtre mis à jour : "Tube Effect - Créateur d'Animation Vidéo v2.0"
- Taille de la fenêtre principale : 1400x900 → 1600x900
- Classe `PathEditor` étendue avec gestion d'historique
- Amélioration de la documentation du code avec docstrings détaillés
- `DEFAULT_SETTINGS` étendu avec les nouveaux paramètres d'effets

### Technique

- Ajout de la classe abstraite `Effect` comme base pour tous les effets
- 6 classes d'effets dérivées : `SpotlightEffect`, `SpotlightGlowEffect`, `VignetteEffect`, `ColorGradingEffect`, `ZoomEffect`, `BlurFocusEffect`
- Utilisation de NumPy pour les calculs de masques et dégradés optimisés
- Gestion de la mémoire améliorée avec `copy.deepcopy` pour l'historique
- Architecture modulaire facilitant l'ajout de nouveaux effets

### Performances

- Optimisation des calculs de masques avec NumPy vectorisé
- Pré-calcul des dégradés pour les effets de glow
- Cache des positions de points pour recherche rapide

---

## [1.9.0] - 2025-06-13

### Ajouté
- Support initial des courbes de Bézier
- Classe `PathEditor` pour l'édition avancée des tracés
- Lissage ajustable du tracé (0-100%)
- Prévisualisation en temps réel de l'animation

### Modifié
- Interface utilisateur améliorée avec groupes de contrôles
- Système de rendu asynchrone avec `AnimationWorker`

---

## [1.0.0] - 2025-06-01

### Ajouté
- Version initiale de Tube Effect
- Effet spotlight basique (cercle/carré)
- Édition de tracé par points
- Export vidéo en HD, Full HD et 4K
- Contrôles de base : taille, vitesse, luminosité, FPS
- Sauvegarde/chargement de projets au format JSON
- Support d'images PNG, JPG, BMP

---

## Types de Changements

- **Ajouté** : Nouvelles fonctionnalités
- **Modifié** : Changements dans les fonctionnalités existantes
- **Déprécié** : Fonctionnalités bientôt supprimées
- **Supprimé** : Fonctionnalités retirées
- **Corrigé** : Corrections de bugs
- **Sécurité** : Corrections de vulnérabilités

---

## Liens

- [2.0.0] : https://github.com/pierrre2db/Tube_Effect/releases/tag/v2.0.0
- [1.9.0] : https://github.com/pierrre2db/Tube_Effect/releases/tag/v1.9.0
- [1.0.0] : https://github.com/pierrre2db/Tube_Effect/releases/tag/v1.0.0
