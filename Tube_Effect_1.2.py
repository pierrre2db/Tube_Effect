# =============================================================================
# --- Importations des bibliothèques nécessaires ---
# =============================================================================
# last edit 13/06/25 14:05
import sys
import cv2
import numpy as np
import math
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QFileDialog, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QProgressDialog,
    QGraphicsLineItem, QGroupBox, QComboBox, QGraphicsRectItem, QGraphicsObject, QGraphicsItem,
    QColorDialog, QDialog, QDialogButtonBox, QFormLayout, QStatusBar, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF, QRectF, QRect
from PyQt6.QtGui import QPixmap, QImage, QPen, QBrush, QColor, QIcon, QPainterPath, QPainter

class PathEditor:
    """
    Classe pour gérer l'édition avancée des tracés avec support des courbes de Bézier.
    Permet de créer et modifier des chemins lisses avec des points de contrôle interactifs.
    """
    def __init__(self, scene):
        """
        Initialise l'éditeur de chemin.
        
        Args:
            scene: La scène QGraphicsScene où le chemin sera affiché
        """
        self.scene = scene           # Scène graphique parente
        self.points = []             # Liste des points de contrôle du chemin
        self.bezier_handles = []     # Poignées de Bézier pour les courbes
        self.smoothing = 0.5         # Niveau de lissage (0.0 à 1.0)
        self.show_handles = True     # Afficher les poignées de contrôle
        
    def add_point(self, pos, size):
        """
        Ajoute un nouveau point de contrôle au chemin.
        
        Args:
            pos: Position QPointF du nouveau point
            size: Taille du point (pour le rendu)
            
        Returns:
            int: Index du point ajouté
        """
        point = {"x": pos.x(), "y": pos.y(), "size": size}
        self.points.append(point)
        self.update_bezier_handles()  # Met à jour les poignées de Bézier
        self.redraw()  # Redessine le chemin
        return len(self.points) - 1  # Retourne l'index du point
    
    def update_bezier_handles(self):
        """
        Calcule et met à jour les poignées de Bézier pour tous les points de contrôle.
        Les poignées déterminent la courbure du chemin entre les points.
        """
        self.bezier_handles = []  # Réinitialise les poignées existantes
        
        # Parcourt tous les points sauf le premier et le dernier
        for i in range(len(self.points)):
            # Pas de poignées pour les extrémités
            if i == 0 or i == len(self.points) - 1:
                self.bezier_handles.append({"in": None, "out": None})
                continue
                
            # Points adjacents pour calculer la tangente
            prev = self.points[i-1]
            curr = self.points[i]
            next_pt = self.points[i+1]
            
            # Calcul du vecteur tangent (direction du chemin)
            # Le facteur 0.2 et le smoothing déterminent l'intensité de la courbure
            dx = (next_pt["x"] - prev["x"]) * 0.2 * self.smoothing
            dy = (next_pt["y"] - prev["y"]) * 0.2 * self.smoothing
            
            # Création des poignées d'entrée et de sortie
            # Ces points contrôlent la courbe avant et après le point de contrôle
            handle_in = {
                "x": curr["x"] - dx,  # Poignée d'entrée (côté point précédent)
                "y": curr["y"] - dy
            }
            
            handle_out = {
                "x": curr["x"] + dx,  # Poignée de sortie (côté point suivant)
                "y": curr["y"] + dy
            }
            
            # Stockage des poignées pour ce point
            self.bezier_handles.append({
                "in": handle_in,
                "out": handle_out
            })
    
    def get_smoothed_path(self):
        """
        Construit et retourne un QPainterPath représentant le chemin lissé.
        
        Returns:
            QPainterPath: Le chemin lissé prêt à être affiché
        """
        path = QPainterPath()
        
        # Pas assez de points pour former un chemin
        if len(self.points) < 2:
            return path
            
        # Positionnement au premier point
        first = self.points[0]
        path.moveTo(QPointF(first["x"], first["y"]))
        
        # Cas particulier : seulement 2 points -> ligne droite
        if len(self.points) == 2:
            second = self.points[1]
            path.lineTo(QPointF(second["x"], second["y"]))
            return path
        
        # Parcours des points pour créer des courbes de Bézier
        for i in range(1, len(self.points)):
            prev = self.points[i-1]
            curr = self.points[i]
            
            # Vérifie si on peut créer une courbe de Bézier cubique
            if (i < len(self.bezier_handles) and 
                self.bezier_handles[i-1]["out"] and 
                self.bezier_handles[i]["in"]):
                
                # Récupération des points de contrôle de Bézier
                handle_out = self.bezier_handles[i-1]["out"]  # Poignée de sortie du point précédent
                handle_in = self.bezier_handles[i]["in"]      # Poignée d'entrée du point courant
                
                # Création d'une courbe de Bézier cubique
                path.cubicTo(
                    QPointF(handle_out["x"], handle_out["y"]),  # Point de contrôle de départ
                    QPointF(handle_in["x"], handle_in["y"]),    # Point de contrôle d'arrivée
                    QPointF(curr["x"], curr["y"])               # Point d'arrivée
                )
            else:
                # Si pas de poignées, on trace une ligne droite
                path.lineTo(QPointF(curr["x"], curr["y"]))
                
        return path
    
    def redraw(self):
        """
        Redessine l'ensemble du chemin et ses éléments de contrôle dans la scène.
        Cette méthode est appelée à chaque modification du chemin.
        """
        # Supprime tous les éléments graphiques précédents du chemin
        for item in self.scene.items():
            if hasattr(item, 'is_path_element') and item.is_path_element:
                self.scene.removeItem(item)
        
        # Vérifie s'il y a assez de points pour former un chemin
        if len(self.points) >= 2:
            # Création du style pour le chemin principal
            pen = QPen(QColor("#4f46e5"), 2, Qt.PenStyle.SolidLine)
            
            # Obtention du chemin lissé
            path = self.get_smoothed_path()
            
            # Ajout du chemin à la scène
            path_item = self.scene.addPath(path, pen)
            path_item.is_path_element = True  # Marque l'élément pour une suppression facile
            
            # Dessin des points de contrôle
            for i, point in enumerate(self.points):
                # Dessin du point principal
                point_size = 8
                point_item = self.scene.addEllipse(
                    point["x"] - point_size/2,
                    point["y"] - point_size/2,
                    point_size, point_size,
                    QPen(Qt.GlobalColor.white, 1.5),  # Contour blanc
                    QBrush(QColor("#4f46e5"))          # Remplissage bleu
                )
                point_item.is_path_element = True
                point_item.setZValue(15)  # S'assure que les points sont au-dessus du chemin
                
                # Dessin des poignées de Bézier si activé et pour les points intermédiaires
                if (self.show_handles and 
                    0 < i < len(self.points) - 1 and 
                    i-1 < len(self.bezier_handles)):
                    
                    self._draw_bezier_handles(i, point)
    
    def _draw_bezier_handles(self, point_index, point):
        """
        Dessine les poignées de Bézier pour un point de contrôle.
        
        Args:
            point_index: Index du point de contrôle
            point: Dictionnaire contenant les coordonnées du point
        """
        handle_in = self.bezier_handles[point_index-1]["in"]
        handle_out = self.bezier_handles[point_index-1]["out"]
        
        if not handle_in or not handle_out:
            return
        
        # Style des lignes de guidage
        line_pen = QPen(QColor("#6b7280"), 1, Qt.PenStyle.DotLine)
        
        # Ligne point de contrôle -> poignée d'entrée
        line_in = self.scene.addLine(
            point["x"], point["y"],
            handle_in["x"], handle_in["y"],
            line_pen
        )
        line_in.is_path_element = True
        
        # Ligne point de contrôle -> poignée de sortie
        line_out = self.scene.addLine(
            point["x"], point["y"],
            handle_out["x"], handle_out["y"],
            line_pen
        )
        line_out.is_path_element = True
        
        # Style des poignées
        handle_size = 6
        handle_brush = QBrush(QColor("#ef4444"))  # Couleur rouge pour les poignées
        
        # Dessin de la poignée d'entrée
        handle_in_item = self.scene.addEllipse(
            handle_in["x"] - handle_size/2,
            handle_in["y"] - handle_size/2,
            handle_size, handle_size,
            QPen(Qt.GlobalColor.white, 1),
            handle_brush
        )
        handle_in_item.is_path_element = True
        handle_in_item.setZValue(15)
        
        # Dessin de la poignée de sortie
        handle_out_item = self.scene.addEllipse(
            handle_out["x"] - handle_size/2,
            handle_out["y"] - handle_size/2,
            handle_size, handle_size,
            QPen(Qt.GlobalColor.white, 1),
            handle_brush
        )
        handle_out_item.is_path_element = True
        handle_out_item.setZValue(15)
    
    def set_smoothing(self, value):
        """
        Définit le niveau de lissage du chemin.
        
        Args:
            value: Niveau de lissage entre 0 (pas de lissage) et 100 (lissage maximal)
        """
        self.smoothing = value / 100.0  # Conversion en 0.0-1.0
        self.update_bezier_handles()  # Met à jour les poignées
        self.redraw()  # Redessine le chemin
    
    def get_points(self):
        """
        Retourne la liste des points de contrôle du chemin.
        
        Returns:
            list: Liste des points de contrôle avec leurs coordonnées et tailles
        """
        return self.points
    
    def clear(self):
        """
        Réinitialise l'éditeur en supprimant tous les points de contrôle.
        """
        self.points = []
        self.bezier_handles = []
        self.redraw()  # Met à jour l'affichage

# =============================================================================
# --- Constantes globales de l'application ---
# =============================================================================
PROFILES = {
    "HD 720p": (1280, 720),
    "Full HD 1080p": (1920, 1080),
    "4K UHD": (3840, 2160)
}
DEFAULT_SETTINGS = {
    "speed": 500,
    "size": 250,
    "brightness": 50,
    "fps": 50,
    "shape": "Cercle",
    "trace_color": "#FFFF00",
    "shape_color": "#00FFFF"
}

# =============================================================================
# --- Classe Point de Contrôle ---
# =============================================================================
class ControlPoint(QGraphicsObject):
    pointMoved = pyqtSignal(int, QPointF)

    def __init__(self, x, y, handle_size, index):
        super().__init__()
        self.handle_size = handle_size
        self.index = index
        self.setPos(x, y)
        self.setZValue(11)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def boundingRect(self):
        return QRectF(-self.handle_size, -self.handle_size, self.handle_size * 2, self.handle_size * 2)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.setBrush(QBrush(QColor("#4f46e5")))
        painter.drawEllipse(self.boundingRect())

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self.pointMoved.emit(self.index, value)
        return super().itemChange(change, value)

# =============================================================================
# --- Classe Worker pour l'Animation ---
# =============================================================================
class AnimationWorker(QThread):
    progress_update = pyqtSignal(int)
    frame_ready_for_preview = pyqtSignal(np.ndarray)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)  # Signal pour les erreurs

    def __init__(self, path_points, settings, image, resolution, output_path=None):
        super().__init__()
        self.path_points = path_points
        self.settings = settings
        self.image = image.copy()
        self.target_resolution = resolution
        self.output_path = output_path
        self.is_running = True

    def run(self):
        """
        Méthode principale exécutée dans un thread séparé pour générer l'animation.
        Gère la création des frames et l'exportation vidéo si nécessaire.
        """
        try:
            # Récupération des dimensions de l'image et des paramètres
            height, width, _ = self.image.shape
            speed = self.settings['speed']  # en pixels par seconde
            fps = self.settings['fps']      # images par seconde
            
            # Calcul du facteur d'assombrissement de l'arrière-plan (0.0 à 1.0)
            bg_brightness_factor = self.settings['brightness'] / 100.0
            
            # Calcul de la distance totale du trajet
            total_distance = sum(
                self.calculate_distance(self.path_points[i], self.path_points[i+1]) 
                for i in range(len(self.path_points) - 1)
            )
            
            # Calcul du nombre total de frames pour la barre de progression
            if speed > 0 and fps > 0:
                total_frames = int((total_distance / speed) * fps)
            else:
                total_frames = 0

            # Initialisation du writer vidéo si nécessaire
            video_writer = None
            if self.output_path:
                out_w, out_h = self.target_resolution if self.target_resolution else (width, height)
                # Utilisation de l'encodeur H.264 (X264) pour une meilleure qualité
                fourcc = cv2.VideoWriter_fourcc(*'X264')
                video_writer = cv2.VideoWriter(self.output_path, fourcc, fps, (out_w, out_h))
                if not video_writer.isOpened():
                    raise RuntimeError(f"Impossible d'initialiser le fichier vidéo: {self.output_path}")

            # Vérification des paramètres valides
            if speed <= 0 or fps <= 0:
                if video_writer:
                    video_writer.release()
                self.finished.emit()
                return
                
            # Calcul du nombre de pixels à parcourir par frame
            pixels_per_frame = speed / fps
            
            # Initialisation des variables de suivi de l'animation
            current_segment = 0
            progress_in_segment = 0.0
            frame_count = 0
            
            # Création de l'image d'arrière-plan assombrie
            dark_image = (self.image * bg_brightness_factor).astype(np.uint8)

            # Boucle principale de génération des frames
            while current_segment < len(self.path_points) - 1 and self.is_running:
                # Récupération des points de début et de fin du segment actuel
                start_point = self.path_points[current_segment]
                end_point = self.path_points[current_segment + 1]
                
                # Calcul de la position et de la taille actuelles par interpolation linéaire
                current_x = start_point["x"] + (end_point["x"] - start_point["x"]) * progress_in_segment
                current_y = start_point["y"] + (end_point["y"] - start_point["y"]) * progress_in_segment
                current_size = start_point["size"] + (end_point["size"] - start_point["size"]) * progress_in_segment
                
                # Création de la frame avec la zone mise en évidence
                frame = self.create_highlight_frame(dark_image, current_x, current_y, current_size)
                
                # Gestion de l'exportation ou de la prévisualisation
                if video_writer:
                    # Redimensionnement si nécessaire pour l'exportation
                    if self.target_resolution:
                        frame = cv2.resize(frame, self.target_resolution, interpolation=cv2.INTER_AREA)
                    video_writer.write(frame)
                else:
                    # Envoi de la frame pour prévisualisation
                    self.frame_ready_for_preview.emit(frame)
                    self.msleep(int(1000/fps))  # Contrôle de la vitesse de lecture
                
                # Mise à jour de la progression
                frame_count += 1
                if total_frames > 0:
                    progress_percent = int((frame_count / total_frames) * 100)
                    self.progress_update.emit(progress_percent)
                
                # Calcul de la progression dans le segment actuel
                segment_length = self.calculate_distance(start_point, end_point)
                if segment_length > 0:
                    progress_in_segment += pixels_per_frame / segment_length
                else:
                    progress_in_segment = 1.0
                
                # Passage au segment suivant si nécessaire
                if progress_in_segment >= 1.0:
                    progress_in_segment = 0.0
                    current_segment += 1

            # Nettoyage final
            if video_writer:
                video_writer.release()
                
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()

    def create_highlight_frame(self, dark_image, x, y, size):
        """
        Crée une frame avec une zone mise en évidence.
        
        Args:
            dark_image: Image de fond assombrie
            x, y: Position du centre de la zone
            size: Taille de la zone
            
        Returns:
            Image avec la zone mise en évidence
        """
        # Création d'un masque pour la zone éclairée
        mask = np.zeros(self.image.shape[:2], dtype="uint8")
        
        # Dessin de la forme sélectionnée dans le masque
        if self.settings['shape'] == "Cercle":
            cv2.circle(mask, (int(x), int(y)), int(size / 2), 255, -1)
        elif self.settings['shape'] == "Carré":
            half_size = int(size / 2)
            cv2.rectangle(
                mask, 
                (int(x - half_size), int(y - half_size)), 
                (int(x + half_size), int(y + half_size)), 
                255, 
                -1
            )
        
        # Application du masque pour combiner les images
        mask_3d = mask[:, :, np.newaxis] > 0
        return np.where(mask_3d, self.image, dark_image)
        
    def calculate_distance(self, p1, p2):
        """
        Calcule la distance euclidienne entre deux points.
        
        Args:
            p1, p2: Dictionnaires avec les clés 'x' et 'y'
            
        Returns:
            Distance entre les deux points
        """
        return math.sqrt((p2["x"] - p1["x"])**2 + (p2["y"] - p1["y"])**2)

    def stop(self):
        """Arrête le rendu de l'animation en cours."""
        self.is_running = False

class PreferencesDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Préférences")
        self.settings = settings.copy()
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.trace_color_btn = QPushButton()
        self.trace_color_btn.clicked.connect(lambda: self.pick_color('trace_color'))
        self.shape_color_btn = QPushButton()
        self.shape_color_btn.clicked.connect(lambda: self.pick_color('shape_color'))
        form_layout.addRow("Couleur de la Trajectoire:", self.trace_color_btn)
        form_layout.addRow("Couleur de la Forme:", self.shape_color_btn)
        layout.addLayout(form_layout)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.update_color_buttons()

    def pick_color(self, key):
        color = QColorDialog.getColor(QColor(self.settings[key]), self)
        if color.isValid():
            self.settings[key] = color.name(); self.update_color_buttons()

    def update_color_buttons(self):
        self.trace_color_btn.setStyleSheet(f"background-color: {self.settings['trace_color']};")
        self.shape_color_btn.setStyleSheet(f"background-color: {self.settings['shape_color']};")

    def get_settings(self): return self.settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créateur d'Animation Vidéo v1.9")
        self.setGeometry(100, 100, 1400, 900)
        
        self.settings = DEFAULT_SETTINGS.copy()
        self.image_path, self.cv_image = None, None
        self.path_points = []
        self.graphic_items = {'points': [], 'lines': [], 'shapes': []}
        self.preview_worker, self.export_worker = None, None
        self.dragged_point = None
        self.overlay_item = None
        self.hovered_point_index = None
        self.path_editor = None
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        # Configuration de la fenêtre principale
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Barre d'outils supérieure
        top_bar = QHBoxLayout()
        
        # Boutons de contrôle
        self.btn_load = QPushButton("Charger une image")
        self.btn_save_path = QPushButton("Sauvegarder le tracé")
        self.btn_load_path = QPushButton("Charger un tracé")
        self.btn_prefs = QPushButton("Préférences")
        
        # Ajout des boutons à la barre supérieure
        top_bar.addWidget(self.btn_load)
        top_bar.addWidget(self.btn_save_path)
        top_bar.addWidget(self.btn_load_path)
        top_bar.addWidget(self.btn_prefs)
        top_bar.addStretch()
        
        # Zone de visualisation
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        self.view.mousePressEvent = self.view_mouse_press
        self.view.mouseMoveEvent = self.view_mouse_move
        self.view.mouseReleaseEvent = self.view_mouse_release
        
        # Contrôles de l'application
        controls_layout = QHBoxLayout()
        
        # Groupe pour la forme
        shape_group = QGroupBox("Forme")
        shape_layout = QVBoxLayout()
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Cercle", "Carré"])
        shape_layout.addWidget(self.shape_combo)
        shape_group.setLayout(shape_layout)
        
        # Groupe pour la taille
        size_group = QGroupBox("Taille")
        size_layout = QVBoxLayout()
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_label = QLabel(f"Taille ({self.settings['size']}px):")
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_slider)
        size_group.setLayout(size_layout)
        
        # Groupe pour la luminosité
        bg_group = QGroupBox("Luminosité")
        bg_layout = QVBoxLayout()
        self.bg_slider = QSlider(Qt.Orientation.Horizontal)
        self.bg_label = QLabel(f"Luminosité ({self.settings['brightness']}%):")
        bg_layout.addWidget(self.bg_label)
        bg_layout.addWidget(self.bg_slider)
        bg_group.setLayout(bg_layout)
        
        # Groupe pour la vitesse
        speed_group = QGroupBox("Vitesse")
        speed_layout = QVBoxLayout()
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_label = QLabel(f"Vitesse ({self.settings['speed']} px/s):")
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)
        speed_group.setLayout(speed_layout)
        
        # Groupe pour les FPS
        fps_group = QGroupBox("FPS")
        fps_layout = QVBoxLayout()
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["15", "24", "25", "30", "50", "60"])
        self.fps_combo.setCurrentText(str(self.settings['fps']))
        fps_layout.addWidget(self.fps_combo)
        fps_group.setLayout(fps_layout)
        
        # Groupe pour le lissage
        self.smoothing_group = QGroupBox("Lissage")
        smoothing_layout = QHBoxLayout()
        self.smoothing_slider = QSlider(Qt.Orientation.Horizontal)
        self.smoothing_slider.setRange(0, 100)
        self.smoothing_slider.setValue(50)
        self.smoothing_label = QLabel("50%")
        smoothing_layout.addWidget(QLabel("Lissage:"))
        smoothing_layout.addWidget(self.smoothing_slider)
        smoothing_layout.addWidget(self.smoothing_label)
        self.smoothing_group.setLayout(smoothing_layout)
        
        # Groupe pour les options d'exportation
        export_group = QGroupBox("Exportation")
        export_layout = QVBoxLayout()
        
        # Sélection du profil d'exportation
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Profil:"))
        self.export_profile_combo = QComboBox()
        self.export_profile_combo.addItems(["HD 720p", "Full HD 1080p", "4K UHD"])
        profile_layout.addWidget(self.export_profile_combo)
        export_layout.addLayout(profile_layout)
        
        # Boutons d'action
        action_layout = QVBoxLayout()
        self.btn_preview = QPushButton("Prévisualiser")
        self.btn_export = QPushButton("Exporter")
        self.btn_reset = QPushButton("Réinitialiser")
        action_layout.addWidget(self.btn_preview)
        action_layout.addWidget(self.btn_export)
        action_layout.addWidget(self.btn_reset)
        
        export_layout.addLayout(action_layout)
        export_group.setLayout(export_layout)
        
        # Ajout des groupes aux contrôles
        controls_layout.addWidget(shape_group)
        controls_layout.addWidget(size_group)
        controls_layout.addWidget(bg_group)
        controls_layout.addWidget(speed_group)
        controls_layout.addWidget(fps_group)
        controls_layout.addWidget(self.smoothing_group)
        controls_layout.addWidget(export_group)
        
        # Barre d'état
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.status_label = QLabel("Prêt")
        self.duration_label = QLabel("Durée: 00:00:00")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_bar.addPermanentWidget(self.status_label)
        status_bar.addPermanentWidget(self.duration_label)
        status_bar.addPermanentWidget(self.progress_bar, 1)
        
        # Assemblage du layout principal
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.view, 1)  # Le 1 indique que la vue prendra tout l'espace disponible
        main_layout.addLayout(controls_layout)
        
        # Connexion des signaux
        self.connect_signals()
        
        # Initialisation des contrôles
        self.init_controls()
        self.update_button_states()
    def connect_signals(self):
        self.btn_load.clicked.connect(self.load_image)
        self.btn_export.clicked.connect(self.export_video)
        self.btn_save_path.clicked.connect(self.save_path)
        self.btn_load_path.clicked.connect(self.load_path)
        self.btn_prefs.clicked.connect(self.open_preferences)
        self.btn_preview.clicked.connect(self.toggle_preview_animation)
        self.btn_reset.clicked.connect(self.reset_path)
        
        # Connexion des contrôles
        self.size_slider.valueChanged.connect(lambda v: self.update_setting("size", v))
        self.speed_slider.valueChanged.connect(lambda v: self.update_setting("speed", v))
        self.bg_slider.valueChanged.connect(lambda v: self.update_setting("brightness", v))
        self.shape_combo.currentTextChanged.connect(lambda t: self.update_setting("shape", t))
        self.fps_combo.currentTextChanged.connect(lambda t: self.update_setting("fps", int(t)))
        
        # Connexion du slider de lissage
        self.smoothing_slider.valueChanged.connect(self.update_smoothing)

    def init_controls(self):
        self.size_slider.setRange(20, 500)
        self.bg_slider.setRange(0, 100)
        self.speed_slider.setRange(20, 1000)
        self.size_slider.setValue(self.settings['size'])
        self.bg_slider.setValue(self.settings['brightness'])
        self.speed_slider.setValue(self.settings['speed'])
        self.update_all_labels()
        self.fps_combo.setCurrentText(str(self.settings['fps']))
        self.shape_combo.setCurrentText(self.settings.get('shape', 'Cercle'))

    def update_setting(self, key, value):
        self.settings[key] = value
        self.update_all_labels()
        if key == "shape": self.sync_scene_from_data()
        if key == "brightness": self.update_brightness_overlay()
        self.calculate_and_display_duration()

    def update_all_labels(self):
        self.size_label.setText(f"Taille ({self.settings['size']}px):")
        self.bg_label.setText(f"Luminosité ({self.settings['brightness']}%):")
        self.speed_label.setText(f"Vitesse ({self.settings['speed']} px/s):")
    
    def open_preferences(self):
        dialog = PreferencesDialog(self.settings, self)
        if dialog.exec():
            self.settings.update(dialog.get_settings())
            self.sync_scene_from_data()

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Ouvrir une image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.image_path, self.cv_image = path, cv2.imread(path)
            pixmap = QPixmap(self.image_path)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            height = self.cv_image.shape[0]
            self.size_slider.setMaximum(height)
            self.settings['size'] = int(height / 4)
            self.size_slider.setValue(self.settings['size'])
            self.overlay_item = QGraphicsRectItem(QRectF(pixmap.rect()))
            self.overlay_item.setZValue(5)
            self.scene.addItem(self.overlay_item)
            self.view.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            
            # Initialisation de l'éditeur de chemin
            self.path_editor = PathEditor(self.scene)
            self.reset_path()
            self.update_brightness_overlay()

    def update_brightness_overlay(self):
        if self.overlay_item:
            alpha = int(255 * (1 - self.settings['brightness'] / 100.0))
            self.overlay_item.setBrush(QColor(0, 0, 0, alpha))

    def save_path(self):
        if not self.path_points: return
        path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le projet", "", "Projet Vidéo (*.json)")
        if path:
            with open(path, 'w') as f: json.dump({"settings": self.settings, "path_points": self.path_points}, f, indent=4)

    def load_path(self):
        if self.cv_image is None: return
        path, _ = QFileDialog.getOpenFileName(self, "Charger un projet", "", "Projet Vidéo (*.json)")
        if path:
            try:
                with open(path, 'r') as f: project_data = json.load(f)
                self.settings = project_data.get("settings", DEFAULT_SETTINGS.copy())
                self.path_points = project_data.get("path_points", [])
                self.init_controls()
                self.sync_scene_from_data()
            except Exception as e:
                print(f"Erreur lors du chargement du fichier projet : {e}")

    def update_smoothing(self, value):
        """Met à jour le niveau de lissage du chemin"""
        self.smoothing_label.setText(f"{value}%")
        if self.path_editor:
            self.path_editor.set_smoothing(value / 100.0)
    
    def view_mouse_press(self, event):
        if not self.path_editor:
            return
            
        scene_pos = self.view.mapToScene(event.pos())
        
        # Vérifier si on est en mode édition (Maj enfoncé)
        shift_pressed = (QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier) == Qt.KeyboardModifier.ShiftModifier
        
        if shift_pressed:
            # Mode édition - on laisse gérer le déplacement des points par Qt
            item = self.scene.itemAt(scene_pos, self.view.transform())
            if isinstance(item, ControlPoint):
                self.dragged_point = item
                return
        else:
            # Mode ajout de point
            if self.cv_image is None:
                return
                
            # Ajout d'un point avec l'éditeur de chemin
            self.path_editor.add_point(scene_pos, self.settings['size'])
            self.sync_path_from_editor()

    def view_mouse_move(self, event):
        if self.dragged_point:
            new_pos = self.view.mapToScene(event.pos())
            index = self.dragged_point.index
            self.dragged_point.setPos(new_pos)
            if index < len(self.path_points):
                self.path_points[index]['x'], self.path_points[index]['y'] = new_pos.x(), new_pos.y()
                self.redraw_dependent_graphics()
                self.calculate_and_display_duration()
            return
            
        shift_pressed = (QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier) == Qt.KeyboardModifier.ShiftModifier
        new_hover_index = None
        if shift_pressed:
            scene_pos = self.view.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.view.transform())
            if isinstance(item, ControlPoint):
                new_hover_index = item.index
        if new_hover_index != self.hovered_point_index:
            if self.hovered_point_index is not None: self.highlight_shape(self.hovered_point_index, False)
            if new_hover_index is not None: self.highlight_shape(new_hover_index, True)
            self.hovered_point_index = new_hover_index

    def view_mouse_release(self, event): self.dragged_point = None

    def highlight_shape(self, index, highlight_on):
        if index < len(self.graphic_items['shapes']):
            shape_item = self.graphic_items['shapes'][index]
            if highlight_on:
                pen = QPen(QColor("#FF00FF"), 4, Qt.PenStyle.SolidLine)
            else:
                pen = QPen(QColor(self.settings['shape_color']), 3, Qt.PenStyle.SolidLine)
            shape_item.setPen(pen)

    def sync_path_from_editor(self):
        """Synchronise path_points à partir de l'éditeur de chemin"""
        if not self.path_editor:
            return
            
        self.path_points = self.path_editor.get_points().copy()
        self.redraw_dependent_graphics()
        self.calculate_and_display_duration()
        self.update_button_states()
    
    def sync_scene_from_data(self):
        # Nettoyage de la scène
        for item_list in self.graphic_items.values():
            for item in item_list: 
                if item.scene() == self.scene:
                    self.scene.removeItem(item)
            item_list.clear()
            
        # Si on a un éditeur de chemin, on le laisse gérer l'affichage
        if self.path_editor:
            self.path_editor.redraw()
        else:
            # Mode de rendu par défaut (sans lissage)
            for i, point_data in enumerate(self.path_points):
                point_item = ControlPoint(point_data["x"], point_data["y"], 5, i)
                point_item.pointMoved.connect(self.handle_point_move)
                self.scene.addItem(point_item)
                self.graphic_items['points'].append(point_item)
            self.redraw_dependent_graphics()
            
        self.calculate_and_display_duration()
        self.update_button_states()

    def handle_point_move(self, index, pos):
        if not self.dragged_point: return
        self.path_points[index]['x'], self.path_points[index]['y'] = pos.x(), pos.y()
        self.redraw_dependent_graphics()
        self.calculate_and_display_duration()

    def redraw_dependent_graphics(self):
        # Nettoyage des anciens éléments graphiques
        for item in self.graphic_items['lines'] + self.graphic_items['shapes']: 
            if item.scene() == self.scene:
                self.scene.removeItem(item)
        self.graphic_items['lines'].clear()
        self.graphic_items['shapes'].clear()
        
        # Si on a un éditeur de chemin, on utilise son rendu
        if self.path_editor and len(self.path_points) >= 2:
            # On laisse l'éditeur gérer le rendu du chemin
            pass
        # Sinon, on utilise le rendu par défaut
        elif len(self.path_points) >= 2:
            pen_line = QPen(QColor(self.settings['trace_color']), 2, Qt.PenStyle.DashLine)
            for i in range(len(self.path_points) - 1):
                p1, p2 = self.path_points[i], self.path_points[i+1]
                line = self.scene.addLine(p1["x"], p1["y"], p2["x"], p2["y"], pen_line)
                self.graphic_items['lines'].append(line)
        
        # Dessin des formes (cercles ou carrés) pour chaque point
        pen_shape = QPen(QColor(self.settings['shape_color']), 3, Qt.PenStyle.SolidLine)
        for point_data in self.path_points:
            size, x, y = point_data["size"], point_data["x"], point_data["y"]
            if self.settings.get("shape", "Cercle") == "Cercle":
                shape = self.scene.addEllipse(x - size/2, y - size/2, size, size, pen_shape)
            else:
                shape = self.scene.addRect(x - size/2, y - size/2, size, size, pen_shape)
            if shape:
                shape.setZValue(10)
                self.graphic_items['shapes'].append(shape)

    def calculate_and_display_duration(self):
        fps = self.settings['fps']
        speed = self.settings['speed']
        if len(self.path_points) < 2 or speed <= 0 or fps <= 0:
            self.duration_label.setText("Durée: 00:00:00"); return
        
        total_distance = self.calculate_total_distance()
        total_seconds = total_distance / speed
        
        total_frames = int(total_seconds * fps)
        total_seconds_from_frames = total_frames // fps
        remaining_frames = total_frames % fps
        minutes = total_seconds_from_frames // 60
        seconds = total_seconds_from_frames % 60
        
        self.duration_label.setText(f"Durée: {minutes:02d}:{seconds:02d}:{remaining_frames:02d}")

    def calculate_total_distance(self):
        return sum(math.sqrt((self.path_points[i+1]["x"] - self.path_points[i]["x"])**2 + (self.path_points[i+1]["y"] - self.path_points[i]["y"])**2) for i in range(len(self.path_points) - 1))

    def update_button_states(self, is_previewing=False):
        has_image = self.cv_image is not None
        has_path = len(self.path_points) >= 2
        for widget in [self.btn_load, self.btn_export, self.btn_reset, self.size_slider, self.speed_slider, self.shape_combo, self.bg_slider, self.btn_save_path, self.btn_load_path, self.btn_prefs, self.export_profile_combo, self.fps_combo]:
            widget.setEnabled(not is_previewing)
        if not is_previewing:
            self.btn_export.setEnabled(has_image and has_path)
            self.btn_preview.setEnabled(has_image and has_path)
            self.btn_reset.setEnabled(has_image and len(self.path_points) > 0)
            self.btn_save_path.setEnabled(has_image and len(self.path_points) > 0)
            self.btn_load_path.setEnabled(has_image)
        else: self.btn_preview.setEnabled(True)
    
    def reset_path(self):
        if self.path_editor:
            self.path_editor.clear()
        self.path_points = []
        self.sync_scene_from_data()

    def toggle_preview_animation(self):
        if self.preview_worker and self.preview_worker.isRunning(): self.preview_worker.stop()
        else:
            if not (self.cv_image is not None and len(self.path_points) >= 2): return
            self.btn_preview.setText("Arrêter")
            self.update_button_states(is_previewing=True)
            self.preview_worker = AnimationWorker(self.path_points, self.settings, self.cv_image, None)
            self.preview_worker.frame_ready_for_preview.connect(self.update_preview_frame)
            self.preview_worker.finished.connect(self.animation_finished)
            self.preview_worker.start()

    def update_preview_frame(self, frame_np):
        rgb_image = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        q_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        current_pixmap_item = next((item for item in self.scene.items() if isinstance(item, QGraphicsPixmapItem)), None)
        if current_pixmap_item: current_pixmap_item.setPixmap(pixmap)
        else: self.scene.addPixmap(pixmap)

    def export_video(self):
        try:
            # Vérifier qu'une image est chargée
            if self.cv_image is None:
                QMessageBox.warning(self, "Erreur", "Veuillez d'abord charger une image.")
                return
                
            # Vérifier qu'il y a des points de tracé
            if not self.path_points or len(self.path_points) < 2:
                QMessageBox.warning(self, "Erreur", "Veuillez dessiner un tracé avec au moins 2 points.")
                return
                
            # Obtenir la résolution sélectionnée
            profile = self.export_profile_combo.currentText()
            if profile not in PROFILES:
                QMessageBox.critical(self, "Erreur", f"Profil non reconnu: {profile}")
                return
                
            resolution = PROFILES[profile]
            
            # Demander où enregistrer la vidéo
            output_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Enregistrer la vidéo", 
                "", 
                "MPEG-4 (*.mp4);;Tous les fichiers (*)",
                options=QFileDialog.Option.DontUseNativeDialog
            )
            
            if not output_path:
                return  # L'utilisateur a annulé
                
            # S'assurer que l'extension est .mp4
            if not output_path.lower().endswith('.mp4'):
                output_path += '.mp4'
                
            # Créer et configurer le worker d'exportation
            self.export_worker = AnimationWorker(
                self.path_points, 
                self.settings, 
                self.cv_image, 
                resolution, 
                output_path
            )
            
            # Configurer la boîte de dialogue de progression
            self.progress_dialog = QProgressDialog("Rendu de la vidéo...", "Annuler", 0, 100, self)
            self.progress_dialog.setWindowTitle("Exportation en cours")
            self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.canceled.connect(self.export_worker.stop)
            
            # Connecter les signaux
            self.export_worker.progress_update.connect(self.progress_dialog.setValue)
            self.export_worker.finished.connect(self.animation_finished)
            self.export_worker.finished.connect(self.progress_dialog.close)
            self.export_worker.error_occurred.connect(self.handle_export_error)
            
            # Démarrer l'exportation
            self.export_worker.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'exportation :\n{str(e)}")
    
    def handle_export_error(self, error_message):
        """Gère les erreurs d'exportation"""
        if self.progress_dialog:
            self.progress_dialog.close()
        QMessageBox.critical(self, "Erreur d'exportation", error_message)
        
    def animation_finished(self):
        sender = self.sender()
        if sender == self.preview_worker: self.preview_worker = None
        elif sender == self.export_worker: self.export_worker = None
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            current_pixmap_item = next((item for item in self.scene.items() if isinstance(item, QGraphicsPixmapItem)), None)
            if current_pixmap_item: current_pixmap_item.setPixmap(pixmap)
            else: self.scene.addPixmap(pixmap)
            self.update_brightness_overlay()
            self.sync_scene_from_data()
        self.btn_preview.setText("Animer")
        self.update_button_states()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


