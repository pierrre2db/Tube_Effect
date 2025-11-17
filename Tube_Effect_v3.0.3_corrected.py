import sys
import cv2
import numpy as np
import math
import json
import os
import threading
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QFileDialog, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QProgressDialog,
    QGroupBox, QComboBox, QGraphicsRectItem, QGraphicsObject,
    QMessageBox, QAction, QColorDialog, QDialog, QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QUrl, QPointF
from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor, QKeySequence, QDesktopServices, QImage
from PyQt6.QtWidgets import QGraphicsItem

# Logging
logging.basicConfig(level=logging.INFO)

# Constants
PROFILES = {
    "Original": None,
    "Full HD (1080p)": (1920, 1080),
    "HD (720p)": (1280, 720),
    "Mobile (Vertical HD)": (720, 1280),
    "SD (480p)": (640, 480)
}
DEFAULT_SETTINGS = {
    "effect": "Highlight",
    "speed": 200,
    "size": 250,
    "brightness": 50,
    "distortion": 20,
    "fps": 50,
    "shape": "Cercle",
    "sharpen": False,
    "trace_color": "#00FF00",
    "shape_color": "#FF00FF"
}

class Command:
    def execute(self): pass
    def undo(self): pass

class AddPointCommand(Command):
    def __init__(self, main, point_data):
        self.main, self.point_data = main, point_data
    def execute(self):
        self.main.path_points.append(self.point_data)
        self.main.sync_scene_from_data()
    def undo(self):
        self.main.path_points.pop()
        self.main.sync_scene_from_data()

class MovePointCommand(Command):
    def __init__(self, main, index, old_pos, new_pos):
        self.main, self.index, self.old_pos, self.new_pos = main, index, old_pos, new_pos
    def execute(self):
        p = self.main.path_points[self.index]
        p['x'], p['y'] = self.new_pos.x(), self.new_pos.y()
        self.main.sync_scene_from_data()
    def undo(self):
        p = self.main.path_points[self.index]
        p['x'], p['y'] = self.old_pos.x(), self.old_pos.y()
        self.main.sync_scene_from_data()

class ControlPoint(QGraphicsObject):
    pointMoved = pyqtSignal(int, QPointF)

    def __init__(self, x, y, handle_size, index):
        super().__init__()
        self.handle_size, self.index = handle_size, index
        self.setPos(x, y)
        self.setZValue(11)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def boundingRect(self):
        return QRectF(-self.handle_size, -self.handle_size,
                      self.handle_size*2, self.handle_size*2)
    def paint(self, painter, option, widget):
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.setBrush(QBrush(QColor("#4f46e5")))
        painter.drawEllipse(self.boundingRect())

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self.pointMoved.emit(self.index, value)
        return super().itemChange(change, value)

class AnimationWorker(QThread):
    progress_update = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, path_points, settings, image, resolution, output_path=None):
        super().__init__()
        self.path_points = path_points
        self.settings = settings.copy()
        self.image = image.copy()
        self.target_resolution = resolution
        self.output_path = output_path
        self.is_running = True
        self._lock = threading.Lock()

    def run(self):
        speed = self.settings.get('speed', 0)
        fps = self.settings.get('fps', 0)
        if speed <= 0 or fps <= 0:
            logging.warning("Invalid speed/fps: %s/%s", speed, fps)
            self.finished.emit()
            return

        h, w = self.image.shape[:2]
        base = (cv2.addWeighted(self.image, 1.5,
                  cv2.GaussianBlur(self.image, (0,0), 3), -0.5, 0)
                if self.settings.get('sharpen') else self.image)

        dist = sum(math.hypot(p2['x']-p1['x'], p2['y']-p1['y'])
                   for p1, p2 in zip(self.path_points, self.path_points[1:]))
        total_frames = int((dist/speed)*fps)
        pix_pf = speed/fps

        writer = None
        if self.output_path:
            out_w, out_h = self.target_resolution or (w, h)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            try:
                writer = cv2.VideoWriter(self.output_path, fourcc, fps, (out_w, out_h))
                if not writer.isOpened():
                    raise IOError("VideoWriter failed")
            except Exception as e:
                logging.error(e)
                self.finished.emit()
                return

        seg, prog, fc = 0, 0.0, 0
        try:
            while True:
                with self._lock:
                    if not self.is_running:
                        break
                if seg >= len(self.path_points)-1:
                    break
                p1, p2 = self.path_points[seg], self.path_points[seg+1]
                length = math.hypot(p2['x']-p1['x'], p2['y']-p1['y']) or 1
                prog = min(prog + pix_pf/length, 1.0)
                x = p1['x']+(p2['x']-p1['x'])*prog
                y = p1['y']+(p2['y']-p1['y'])*prog
                size = p1['size']+(p2['size']-p1['size'])*prog
                frame = self._frame(base, x, y, size,
                                    (out_w, out_h) if writer else (w, h))
                if writer:
                    writer.write(frame)
                else:
                    self.msleep(int(1000/fps))
                fc += 1
                if total_frames:
                    self.progress_update.emit(int(fc/total_frames*100))
                if prog>=1.0:
                    seg+=1
                    prog=0.0
        finally:
            if writer:
                writer.release()
        self.finished.emit()

    def _frame(self, base, x, y, size, res):
        if "TuboVision" in self.settings.get('effect',''):
            return self._tubo(base, x, y, size, res, 'Déformé' in self.settings['effect'])
        return self._high(base, x, y, size)

    def _high(self, base, x, y, size):
        b = self.settings['brightness']/100.0
        dark = (self.image*b).astype(np.uint8)
        mask = np.zeros(self.image.shape[:2], np.uint8)
        c = (int(x), int(y))
        r=int(size/2)
        if self.settings['shape']=='Cercle':
            cv2.circle(mask,c,r,255,-1)
        else:
            cv2.rectangle(mask,(c[0]-r,c[1]-r),(c[0]+r,c[1]+r),255,-1)
        return np.where(mask[:,:,None]>0, base, dark)

    def _tubo(self, base, x, y, size, res, dist):
        ow, oh = res
        frame=np.zeros((oh,ow,3),np.uint8)
        hlf=int(size)//2
        x1,y1=int(x-hlf),int(y-hlf)
        src=base[max(0,y1):y1+int(size),max(0,x1):x1+int(size)]
        if src.size==0:
            logging.warning("Empty ROI")
            return frame
        roi=src
        if dist and self.settings['distortion']>0:
            k=-self.settings['distortion']/200.0
            hh,ww=roi.shape[:2]
            cam=np.array([[ww,0,ww/2],[0,hh,hh/2],[0,0,1]],np.float32)
            roi=cv2.undistort(roi,cam,np.array([k,0,0,0],np.float32))
        d=min(ow,oh)
        rz=cv2.resize(roi,(d,d),interpolation=cv2.INTER_LINEAR)
        m=np.zeros((d,d),np.uint8)
        if self.settings['shape']=='Cercle':
            cv2.circle(m,(d//2,d//2),d//2,255,-1)
        else:
            cv2.rectangle(m,(0,0),(d,d),255,-1)
        msk=cv2.bitwise_and(rz,rz,mask=m)
        xo,yo=(ow-d)//2,(oh-d)//2
        frame[yo:yo+d,xo:xo+d]=msk
        return frame

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
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.update_color_buttons()

    def pick_color(self, key):
        color = QColorDialog.getColor(QColor(self.settings[key]), self)
        if color.isValid():
            self.settings[key] = color.name()
            self.update_color_buttons()

    def update_color_buttons(self):
        self.trace_color_btn.setStyleSheet(f"background-color: {self.settings['trace_color']};")
        self.shape_color_btn.setStyleSheet(f"background-color: {self.settings['shape_color']};")

    def get_settings(self):
        return self.settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créateur d'Animation Vidéo v3.0.3")
        self.setGeometry(100,100,1600,900)
        self.settings=DEFAULT_SETTINGS.copy()
        self.image_path=self.cv_image=None
        self.project_path=None
        self.path_points=[]
        self.items={'points':[],'lines':[],'shapes':[]}
        self.preview_worker=self.export_worker=None
        self.undo_stack=[]
        self.redo_stack=[]
        self.dragged_point = None
        self.init_ui()

    def init_ui(self):
        cw=QWidget()
        self.setCentralWidget(cw)
        ml=QHBoxLayout(cw)
        ml.setContentsMargins(0,0,0,0)
        left=QWidget()
        left.setFixedWidth(300)
        ll=QVBoxLayout(left)
        right=QWidget()
        rl=QVBoxLayout(right)
        self.scene=QGraphicsScene()
        self.view=QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        self.view.mousePressEvent = self.view_mouse_press
        self.view.mouseMoveEvent = self.view_mouse_move
        self.view.mouseReleaseEvent = self.view_mouse_release
        bottom=QHBoxLayout()

        # File group
        fg=QGroupBox("Fichier")
        fg.setLayout(QVBoxLayout())
        self.btn_load=QPushButton("Charger Image")
        self.btn_export=QPushButton("Exporter Vidéo")
        self.btn_about=QPushButton("À propos")
        fg.layout().addWidget(self.btn_load)
        fg.layout().addWidget(self.btn_export)
        fg.layout().addWidget(self.btn_about)
        ll.addWidget(fg)

        # Params group
        pg=QGroupBox("Paramètres")
        pl=QVBoxLayout(pg)
        self.effect_cb=QComboBox()
        self.effect_cb.addItems(["Highlight","TuboVision (Zoom)","TuboVision (Déformé)"])
        self.shape_cb=QComboBox()
        self.shape_cb.addItems(["Cercle","Carré"])
        self.profile_cb=QComboBox()
        self.profile_cb.addItems(PROFILES.keys())
        self.fps_cb=QComboBox()
        self.fps_cb.addItems(['24','25','30','50','60'])
        pl.addWidget(QLabel("Effet:"))
        pl.addWidget(self.effect_cb)
        pl.addWidget(QLabel("Forme:"))
        pl.addWidget(self.shape_cb)
        pl.addWidget(QLabel("Profil:"))
        pl.addWidget(self.profile_cb)
        pl.addWidget(QLabel("FPS:"))
        pl.addWidget(self.fps_cb)
        ll.addWidget(pg)

        # Sliders
        sg=QGroupBox("Réglages")
        sl=QVBoxLayout(sg)
        self.size_sl=QSlider(Qt.Orientation.Horizontal)
        self.speed_sl=QSlider(Qt.Orientation.Horizontal)
        self.bright_sl=QSlider(Qt.Orientation.Horizontal)
        self.dist_sl=QSlider(Qt.Orientation.Horizontal)
        self.size_lbl=QLabel("Taille:")
        self.speed_lbl=QLabel("Vitesse:")
        self.bright_lbl=QLabel("Luminosité:")
        self.dist_lbl=QLabel("Distorsion:")
        sl.addWidget(self.size_lbl)
        sl.addWidget(self.size_sl)
        sl.addWidget(self.speed_lbl)
        sl.addWidget(self.speed_sl)
        sl.addWidget(self.bright_lbl)
        sl.addWidget(self.bright_sl)
        sl.addWidget(self.dist_lbl)
        sl.addWidget(self.dist_sl)
        ll.addWidget(sg)
        ll.addStretch()
        ml.addWidget(left)
        ml.addWidget(right)
        rl.addWidget(self.view)
        rl.addLayout(bottom)

        # Bottom bar
        self.duration_lbl=QLabel("Durée: 00:00:00")
        self.frames_lbl=QLabel("Images: 0")
        self.btn_anim=QPushButton("Animer")
        self.btn_reset=QPushButton("Effacer Trajet")
        bottom.addStretch()
        bottom.addWidget(self.duration_lbl)
        bottom.addWidget(self.frames_lbl)
        bottom.addStretch()
        bottom.addWidget(self.btn_anim)
        bottom.addWidget(self.btn_reset)

        # Actions & signals
        self._make_actions()
        self._connect()
        self._init_ctrls()
        self._update_states()

    def _make_actions(self):
        mb=self.menuBar()
        fm=mb.addMenu("&Fichier")
        self.save_act=QAction("Sauvegarder",self)
        self.save_act.setShortcut(QKeySequence.StandardKey.Save)
        self.save_as=QAction("Sauvegarder sous...",self)
        self.save_as.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.load_proj=QAction("Charger Projet...",self)
        self.pref=QAction("Préférences...",self)
        self.pref.setShortcut(QKeySequence.StandardKey.Preferences)
        self.quit=QAction("Quitter",self)
        self.quit.setShortcut(QKeySequence.StandardKey.Quit)
        for a in [self.save_act,self.save_as,self.load_proj,self.pref,self.quit]:
            fm.addAction(a)
        em=mb.addMenu("&Édition")
        self.undo_act=QAction("Annuler",self)
        self.undo_act.setShortcut(QKeySequence.StandardKey.Undo)
        self.redo_act=QAction("Rétablir",self)
        self.redo_act.setShortcut(QKeySequence.StandardKey.Redo)
        em.addAction(self.undo_act)
        em.addAction(self.redo_act)

    def _connect(self):
        self.btn_load.clicked.connect(self.load_image)
        self.btn_export.clicked.connect(self.export_video)
        self.btn_about.clicked.connect(self.show_about)
        self.save_act.triggered.connect(lambda:self.save_project(False))
        self.save_as.triggered.connect(lambda:self.save_project(True))
        self.load_proj.triggered.connect(self.load_project)
        self.pref.triggered.connect(self.open_preferences)
        self.quit.triggered.connect(self.close)
        self.undo_act.triggered.connect(self.undo)
        self.redo_act.triggered.connect(self.redo)
        self.size_sl.valueChanged.connect(lambda v:self._update('size',v))
        self.speed_sl.valueChanged.connect(lambda v:self._update('speed',v))
        self.bright_sl.valueChanged.connect(lambda v:self._update('brightness',v))
        self.dist_sl.valueChanged.connect(lambda v:self._update('distortion',v))
        self.shape_cb.currentTextChanged.connect(lambda t:self._update('shape',t))
        self.effect_cb.currentTextChanged.connect(lambda t:self._update('effect',t))
        self.fps_cb.currentTextChanged.connect(lambda t:self._update('fps',int(t)))
        self.profile_cb.currentTextChanged.connect(lambda t:self._update_states())
        self.btn_anim.clicked.connect(self.toggle_anim)
        self.btn_reset.clicked.connect(self.reset_path)

    def _init_ctrls(self):
        self.size_sl.setRange(20,500)
        self.speed_sl.setRange(20,1000)
        self.bright_sl.setRange(0,100)
        self.dist_sl.setRange(0,100)
        self.size_sl.setValue(self.settings['size'])
        self.speed_sl.setValue(self.settings['speed'])
        self.bright_sl.setValue(self.settings['brightness'])
        self.dist_sl.setValue(self.settings['distortion'])
        self.fps_cb.setCurrentText(str(self.settings['fps']))
        self.shape_cb.setCurrentText(self.settings['shape'])
        self.effect_cb.setCurrentText(self.settings['effect'])
        self._update_labels()

    def _update(self,key,val):
        self.settings[key]=val
        self._update_labels()
        self._update_states()
        self._calc_duration()
        if key == 'shape':
            self.sync_scene_from_data()

    def _update_labels(self):
        self.size_lbl.setText(f"Taille: {self.settings['size']}px")
        self.speed_lbl.setText(f"Vitesse: {self.settings['speed']}px/s")
        self.bright_lbl.setText(f"Luminosité: {self.settings['brightness']}%")
        self.dist_lbl.setText(f"Distorsion: {self.settings['distortion']}%")

    def _update_states(self):
        is_pre=bool(self.preview_worker)
        for w in [self.btn_load,self.btn_export,self.btn_reset,self.size_sl,
                  self.speed_sl,self.bright_sl,self.dist_sl,
                  self.shape_cb,self.effect_cb,self.fps_cb,self.profile_cb]:
            w.setEnabled(not is_pre)
        self.update_controls(is_pre)

    def update_controls(self,is_pre):
        eff=self.settings['effect']=='Highlight'
        self.bright_sl.setEnabled(eff and not is_pre)
        self.dist_sl.setEnabled('Déformé' in self.settings['effect'] and not is_pre)

    def _calc_duration(self):
        if len(self.path_points)<2 or self.settings['speed']<=0:
            self.duration_lbl.setText("Durée: 00:00:00")
            self.frames_lbl.setText("Images: 0")
            return
        dist=sum(math.hypot(self.path_points[i+1]['x']-p['x'],self.path_points[i+1]['y']-p['y'])
                 for i,p in enumerate(self.path_points[:-1]))
        total=dist/self.settings['speed']
        fps=self.settings['fps']
        m,s=divmod(total,60)
        frac=s-int(s)
        frames=int(total*fps)
        self.duration_lbl.setText(f"Durée: {int(m):02d}:{int(s):02d}:{int(frac*fps):02d}")
        self.frames_lbl.setText(f"Images: {frames}")

    def load_image(self):
        path,_=QFileDialog.getOpenFileName(self,"Charger une image","","Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        img=cv2.imread(path)
        if img is None:
            QMessageBox.critical(self,"Erreur","Image invalide")
            return
        self.cv_image=img
        self.image_path=path
        pix=QPixmap(path)
        self.scene.clear()
        self.scene.addPixmap(pix)
        h=img.shape[0]
        self.size_sl.setMaximum(h)
        self.size_sl.setValue(h//4)
        self.reset_path()
        self.view.fitInView(self.scene.sceneRect(),Qt.AspectRatioMode.KeepAspectRatio)

    def save_project(self,dlg):
        if not self.path_points:
            return False
        if dlg or not self.project_path:
            fn,_=QFileDialog.getSaveFileName(self,"Sauvegarder le projet","","Projet (*.json)")
            if not fn:
                return False
            self.project_path=fn
        data={'settings':self.settings,'path_points':self.path_points}
        with open(self.project_path,'w') as f:
            json.dump(data,f,indent=4)
        QMessageBox.information(self,"Succès","Projet sauvegardé avec succès")
        return True

    def load_project(self):
        if not self.cv_image:
            QMessageBox.warning(self,"Attention","Charger une image d'abord")
            return
        fn,_=QFileDialog.getOpenFileName(self,"Charger un projet","","Projet (*.json)")
        if not fn:
            return
        try:
            with open(fn) as f:
                d=json.load(f)
            self.settings=d.get('settings',self.settings)
            self.path_points=d.get('path_points',[])
            self.project_path=fn
            self._init_ctrls()
            self.sync_scene_from_data()
            QMessageBox.information(self,"Succès","Projet chargé avec succès")
        except Exception as e:
            QMessageBox.critical(self,"Erreur",f"Projet invalide: {str(e)}")

    def open_preferences(self):
        dialog = PreferencesDialog(self.settings, self)
        if dialog.exec():
            self.settings.update(dialog.get_settings())
            self.sync_scene_from_data()

    def show_about(self):
        QMessageBox.about(self, "À propos",
            "Créateur d'Animation Vidéo v3.0.3\n\n"
            "Application pour créer des animations vidéo avec effets de mise en évidence.\n\n"
            "Utilisation:\n"
            "- Cliquez sur la vue pour ajouter des points de contrôle\n"
            "- Maintenez Maj et faites glisser pour déplacer un point\n"
            "- Utilisez les contrôles pour ajuster les paramètres\n\n"
            "Développé avec PyQt6 et OpenCV")

    def view_mouse_press(self, event):
        scene_pos = self.view.mapToScene(event.pos())

        # Vérifier si on est en mode édition (Maj enfoncé)
        shift_pressed = (QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier)

        if shift_pressed:
            # Mode édition - déplacement de point
            item = self.scene.itemAt(scene_pos, self.view.transform())
            if isinstance(item, ControlPoint):
                self.dragged_point = item
                return
        else:
            # Mode ajout de point
            if self.cv_image is None:
                return

            # Ajouter un nouveau point
            point_data = {
                'x': scene_pos.x(),
                'y': scene_pos.y(),
                'size': self.settings['size']
            }
            cmd = AddPointCommand(self, point_data)
            cmd.execute()
            self.undo_stack.append(cmd)
            self.redo_stack.clear()

    def view_mouse_move(self, event):
        if self.dragged_point:
            scene_pos = self.view.mapToScene(event.pos())
            index = self.dragged_point.index
            if index < len(self.path_points):
                self.path_points[index]['x'] = scene_pos.x()
                self.path_points[index]['y'] = scene_pos.y()
                self.sync_scene_from_data()
                self._calc_duration()

    def view_mouse_release(self, event):
        self.dragged_point = None

    def sync_scene_from_data(self):
        # Nettoyer la scène
        for li in self.items.values():
            for it in li:
                if it.scene() == self.scene:
                    self.scene.removeItem(it)
        self.items={k:[] for k in self.items}

        # Redessiner les points
        for i,p in enumerate(self.path_points):
            cp=ControlPoint(p['x'],p['y'],5,i)
            cp.pointMoved.connect(self.handle_point_move)
            self.scene.addItem(cp)
            self.items['points'].append(cp)

        self._draw_paths()
        self._calc_duration()

    def handle_point_move(self, index, pos):
        if index < len(self.path_points):
            self.path_points[index]['x'] = pos.x()
            self.path_points[index]['y'] = pos.y()
            self._draw_paths()
            self._calc_duration()

    def _draw_paths(self):
        # Nettoyer les lignes et formes
        for it in self.items['lines'] + self.items['shapes']:
            if it.scene() == self.scene:
                self.scene.removeItem(it)
        self.items['lines'].clear()
        self.items['shapes'].clear()

        # Lignes
        pen=QPen(QColor(self.settings['trace_color']),2,Qt.PenStyle.DashLine)
        for i in range(len(self.path_points)-1):
            p1,p2=self.path_points[i],self.path_points[i+1]
            line=self.scene.addLine(p1['x'],p1['y'],p2['x'],p2['y'],pen)
            self.items['lines'].append(line)

        # Formes
        pen2=QPen(QColor(self.settings['shape_color']),3)
        for p in self.path_points:
            x,y,s=p['x'],p['y'],p['size']
            if self.settings['shape']=='Cercle':
                shp=self.scene.addEllipse(x-s/2,y-s/2,s,s,pen2)
            else:
                shp=self.scene.addRect(x-s/2,y-s/2,s,s,pen2)
            shp.setZValue(10)
            self.items['shapes'].append(shp)

    def undo(self):
        if not self.undo_stack:
            return
        cmd=self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)

    def redo(self):
        if not self.redo_stack:
            return
        cmd=self.redo_stack.pop()
        cmd.execute()
        self.undo_stack.append(cmd)

    def reset_path(self):
        self.path_points = []
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.sync_scene_from_data()

    def toggle_anim(self):
        if self.preview_worker:
            with self.preview_worker._lock:
                self.preview_worker.is_running=False
            self.btn_anim.setText("Animer")
        else:
            if not self.cv_image or len(self.path_points)<2:
                QMessageBox.warning(self,"Attention","Veuillez charger une image et créer un trajet")
                return
            self.btn_anim.setText("Arrêter")
            self.btn_anim.setEnabled(True)
            self.preview_worker=AnimationWorker(self.path_points,self.settings,
                                                self.cv_image,None)
            self.preview_worker.finished.connect(self._anim_done)
            self.preview_worker.start()

    def _anim_done(self):
        self.preview_worker=None
        self.btn_anim.setText("Animer")
        self.btn_anim.setEnabled(True)
        # Restaurer l'image originale
        if self.image_path:
            pix=QPixmap(self.image_path)
            self.scene.clear()
            self.scene.addPixmap(pix)
            self.sync_scene_from_data()

    def export_video(self):
        if not self.cv_image:
            QMessageBox.warning(self,"Erreur","Veuillez charger une image d'abord")
            return
        if len(self.path_points)<2:
            QMessageBox.warning(self,"Erreur","Veuillez créer un trajet avec au moins 2 points")
            return

        if not self.save_project(False):
            return

        path,_=QFileDialog.getSaveFileName(self,"Enregistrer Vidéo","","MPEG-4 (*.mp4)")
        if not path:
            return

        if not path.endswith('.mp4'):
            path += '.mp4'

        # Obtenir la résolution
        profile_name = self.profile_cb.currentText()
        resolution = PROFILES.get(profile_name)

        self.btn_export.setEnabled(False)
        self.export_worker=AnimationWorker(self.path_points,self.settings,
                                           self.cv_image,resolution,path)
        pd=QProgressDialog("Rendu de la vidéo...","Annuler",0,100,self)
        pd.setWindowModality(Qt.WindowModality.WindowModal)
        pd.canceled.connect(lambda: setattr(self.export_worker,'is_running',False))
        self.export_worker.progress_update.connect(pd.setValue)
        self.export_worker.finished.connect(lambda: self._export_done(path,pd))
        pd.show()
        self.export_worker.start()

    def _export_done(self,path,pd):
        pd.close()
        QMessageBox.information(self,"Terminé","Vidéo exportée avec succès!")
        QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path)))
        self.btn_export.setEnabled(True)
        self.export_worker = None

if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=MainWindow()
    w.showMaximized()
    sys.exit(app.exec())
