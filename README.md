# Tube Effect

![Tube Effect Banner](https://via.placeholder.com/1200x400/2d2d2d/ffffff?text=Tube+Effect)

Une application Python pour créer des animations vidéo avec un effet de projecteur qui suit un tracé personnalisé sur vos images.

## ✨ Nouveautés v1.3 - Interface Modernisée !

- 🎨 **Design sombre moderne** : Interface élégante avec palette de couleurs professionnelle
- 💡 **Tooltips informatifs** : Chaque contrôle dispose d'une aide contextuelle
- 🎯 **Messages améliorés** : Notifications claires avec icônes pour chaque action
- ⚡ **Feedback visuel** : Effets hover et états interactifs sur tous les boutons
- 📊 **Barre d'état enrichie** : Informations en temps réel sur vos actions

## 🚀 Fonctionnalités

- 🖼️ Chargement d'images (PNG, JPG, BMP)
- ✏️ Édition intuitive du tracé avec support des courbes de Bézier
- 🎚️ Paramètres personnalisables :
  - Forme (Cercle/Carré)
  - Taille du projecteur
  - Vitesse de déplacement
  - Luminosité du fond
  - Lissage des courbes
- 🎥 Export vidéo en haute qualité (jusqu'à 4K)
- ⚡ Prévisualisation en temps réel
- 💾 Sauvegarde et chargement de projets

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

### 🚀 Démarrage rapide

**Linux / Mac :**
```bash
./start.sh
```

**Windows :**
```batch
start.bat
```

**Ou manuellement :**
```bash
python Tube_Effect_1.2.py
```

Les scripts de lancement vérifient automatiquement :
- ✓ Présence de Python
- ✓ Installation des dépendances
- ✓ Démarrage de l'application

2. **Chargez une image** : Cliquez sur "📁 Charger Image"
   - Un message d'aide s'affichera automatiquement au premier lancement

3. **Créez votre tracé** :
   - Cliquez sur l'image pour ajouter des points
   - Maintenez **Maj** et glissez un point pour le déplacer
   - Les courbes sont automatiquement lissées

4. **Ajustez les paramètres** :
   - 📏 **Taille** : Dimension du projecteur (20-500px)
   - 💡 **Luminosité** : Obscurité de l'arrière-plan (0-100%)
   - ⚡ **Vitesse** : Rapidité du déplacement (20-1000 px/s)
   - ✨ **Lissage** : Douceur des courbes (0-100%)
   - 🎬 **FPS** : Fluidité de l'animation (15-60)

5. **Prévisualisez** : Cliquez sur "▶️ Prévisualiser" pour voir le résultat

6. **Exportez** : Cliquez sur "📤 Exporter Vidéo"
   - Choisissez la résolution (HD, Full HD, ou 4K)
   - Sélectionnez l'emplacement de sauvegarde
   - Une notification vous confirmera le succès

### 💡 Astuces

- **Survolez** les contrôles pour voir des explications détaillées
- **Sauvegardez** vos projets pour les reprendre plus tard
- Les valeurs des paramètres s'affichent en temps réel
- La durée estimée de l'animation est visible dans la barre d'état

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Documentation

- [Spécifications techniques](specifications.md) - Documentation technique détaillée
- [Journal des modifications](CHANGELOG.md) - Historique complet des améliorations de l'interface

## 📞 Contact

Pierre 2DB - [@votre_twitter](https://twitter.com/votre_twitter)

Lien du projet : [https://github.com/pierrre2db/Tube_Effect](https://github.com/pierrre2db/Tube_Effect)

---

<div align="center">
  <sub>Créé avec ❤️ par Pierre 2DB</sub>
</div>
