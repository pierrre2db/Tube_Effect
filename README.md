# Tube Effect

![Tube Effect Banner](https://via.placeholder.com/1200x400/2d2d2d/ffffff?text=Tube+Effect)

Une application Python avancée pour créer des animations vidéo avec des effets visuels professionnels qui suivent un tracé personnalisé sur vos images.

## ✨ Nouveautés v2.0

### 🎨 Système d'Effets Multiples
Six effets visuels professionnels au choix :
- **Spotlight Classic** - Effet de projecteur circulaire ou carré
- **Spotlight avec Glow** - Projecteur avec halo lumineux progressif
- **Vignette Animée** - Assombrissement radial élégant
- **Color Grading** - Teinte de couleur personnalisable
- **Zoom/Lens** - Effet de loupe/grossissement
- **Blur Focus** - Flou artistique sur l'arrière-plan

### ✏️ Édition Avancée du Tracé
- **Undo/Redo** : Annulation et rétablissement des actions (Ctrl+Z / Ctrl+Y)
- **Suppression de points** : Clic droit ou touche Suppr
- **Numérotation des points** : Visualisation claire de l'ordre du tracé
- **Historique** : Jusqu'à 50 actions sauvegardées

### ⌨️ Raccourcis Clavier
- `Ctrl+Z` : Annuler
- `Ctrl+Y` : Refaire
- `Suppr` : Supprimer un point
- `Espace` : Lancer/Arrêter la prévisualisation
- `Maj+Clic` : Mode édition (déplacer les points)

## 🚀 Fonctionnalités Complètes

- 🖼️ **Support d'images** : PNG, JPG, BMP
- ✏️ **Édition intuitive** : Courbes de Bézier avec lissage ajustable
- 🎨 **6 effets visuels** : Du spotlight classique au blur artistique
- 🎛️ **Paramètres dynamiques** : Interface qui s'adapte à l'effet choisi
- 🎚️ **Contrôles précis** :
  - Forme (Cercle/Carré)
  - Taille du projecteur (20-500px)
  - Vitesse de déplacement (20-1000 px/s)
  - Luminosité du fond (0-100%)
  - Intensité des effets (glow, zoom, flou, etc.)
  - Sélecteur de couleur pour les effets
- 🎥 **Export professionnel** : HD 720p, Full HD 1080p, 4K UHD
- ⚡ **Prévisualisation temps réel** : Testez avant d'exporter
- 💾 **Sauvegarde de projets** : Format JSON pour réutiliser vos tracés

## 📦 Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/pierrre2db/Tube_Effect.git
   cd Tube_Effect
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Utilisation

### Démarrage Rapide

1. Lancez l'application :
   ```bash
   python Tube_Effect_1.2.py
   ```

2. **Chargez une image** : Cliquez sur "Charger une image"

3. **Créez votre tracé** :
   - Clic simple : Ajouter un point
   - Maj + Glisser : Déplacer un point
   - Clic droit : Supprimer un point
   - Ctrl+Z / Ctrl+Y : Annuler / Refaire

4. **Choisissez un effet** : Sélectionnez dans le menu déroulant "Effet"

5. **Ajustez les paramètres** :
   - Les contrôles s'adaptent automatiquement à l'effet choisi
   - Réglez la taille, vitesse, luminosité
   - Personnalisez les paramètres spécifiques (glow, zoom, couleur, etc.)

6. **Prévisualisez** : Cliquez sur "Prévisualiser" ou appuyez sur `Espace`

7. **Exportez** : Sélectionnez la qualité (720p/1080p/4K) et exportez votre vidéo

### 📖 Guide des Effets

| Effet | Description | Paramètres |
|-------|-------------|------------|
| **Spotlight Classic** | Zone circulaire ou carrée éclairée | Forme, Luminosité |
| **Spotlight Glow** | Projecteur avec halo progressif | Forme, Luminosité, Intensité Glow |
| **Vignette Animée** | Assombrissement radial inversé | Luminosité, Rayon |
| **Color Grading** | Teinte de couleur sur spotlight | Forme, Couleur, Intensité |
| **Zoom/Lens** | Grossissement de la zone | Intensité du Zoom |
| **Blur Focus** | Flou gaussien sur l'arrière-plan | Forme, Intensité Flou |

### 💡 Astuces

- **Lissage du tracé** : Utilisez le slider "Lissage" pour des courbes plus douces
- **Sauvegarde** : Sauvegardez vos projets pour les réutiliser plus tard
- **Performances** : Testez en 720p avant d'exporter en 4K
- **Créativité** : Combinez différents effets entre plusieurs exportations

## 💻 Exigences Système

- **Python** : 3.8 ou supérieur
- **Système d'exploitation** : Windows, macOS, Linux
- **RAM** : 4 GB minimum (8 GB recommandé pour 4K)
- **Espace disque** : 200 MB pour l'application + espace pour les vidéos exportées

### Dépendances

- `PyQt6>=6.4.0` - Interface graphique
- `opencv-python>=4.8.0` - Traitement d'image et vidéo
- `numpy>=1.24.0` - Calculs numériques

## 🏗️ Architecture

Le projet utilise une architecture orientée objet avec :
- **Système d'effets modulaire** : Classe de base `Effect` facilement extensible
- **Éditeur de tracé avancé** : `PathEditor` avec gestion de l'historique
- **Worker asynchrone** : Rendu vidéo en arrière-plan sans bloquer l'UI

## 📈 Changelog

Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique complet des versions.

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Idées de Contributions

- Nouveaux effets visuels
- Support de formats d'image supplémentaires (WEBP, TIFF)
- Export GIF animé
- Effets de transition entre points
- Interface en anglais

## 📄 Documentation

- [Spécifications techniques](specifications.md)
- [Guide de contribution](CONTRIBUTING.md) *(à venir)*
- [Wiki](https://github.com/pierrre2db/Tube_Effect/wiki) *(à venir)*

## 📞 Contact

Pierre 2DB - [@votre_twitter](https://twitter.com/votre_twitter)

Lien du projet : [https://github.com/pierrre2db/Tube_Effect](https://github.com/pierrre2db/Tube_Effect)

## 🙏 Remerciements

- PyQt6 pour le framework GUI
- OpenCV pour le traitement vidéo
- La communauté Python pour les outils exceptionnels

---

<div align="center">
  <sub>Créé avec ❤️ par Pierre 2DB</sub>
  <br>
  <sub>Version 2.0 - Novembre 2025</sub>
</div>
