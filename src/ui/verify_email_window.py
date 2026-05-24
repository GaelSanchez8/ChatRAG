from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                                QPushButton, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal
from database.database_manager import verificar_codigo, reenviar_codigo, obtener_id_por_correo


class VerifyEmailWindow(QWidget):
    verificacion_exitosa = Signal(int, str)  # Emite (id_usuario, correo)
    volver_a_login = Signal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.correo_usuario = None
        
        # Layout maestro
        self.layout_maestro = QVBoxLayout(self)
        self.layout_maestro.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tarjeta de verificación
        self.tarjeta_verificacion = QFrame()
        self.tarjeta_verificacion.setObjectName("tarjetaVerificacion")
        self.tarjeta_verificacion.setFixedWidth(400)
        
        layout = QVBoxLayout(self.tarjeta_verificacion)
        layout.setContentsMargins(35, 40, 35, 40)
        layout.setSpacing(15)

        # Icono
        self.lbl_icono = QLabel("✉️")
        self.lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_icono.setStyleSheet("font-size: 50px; margin-bottom: 5px;")
        layout.addWidget(self.lbl_icono)

        # Título
        self.lbl_title = QLabel("Verifica tu Email")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #f5f5f5;")
        layout.addWidget(self.lbl_title)

        # Subtítulo
        self.lbl_subtitle = QLabel("Hemos enviado un código de 6 dígitos a tu correo.\nEl código expira en 20 minutos.")
        self.lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_subtitle.setStyleSheet("font-size: 13px; color: #a19f9d; margin-bottom: 20px;")
        layout.addWidget(self.lbl_subtitle)

        # Campo de código
        self.lbl_codigo = QLabel("Código de Verificación")
        self.lbl_codigo.setStyleSheet("color: #f5f5f5; font-weight: bold; font-size: 13px;")
        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Ingresa los 6 dígitos")
        self.input_codigo.setObjectName("inputCustom")
        self.input_codigo.setMaxLength(6)
        self.input_codigo.returnPressed.connect(self.procesar_verificacion)  # Agregar Enter
        layout.addWidget(self.lbl_codigo)
        layout.addWidget(self.input_codigo)

        # Botón verificar
        self.btn_verificar = QPushButton("Verificar")
        self.btn_verificar.setObjectName("btnPrimario")
        self.btn_verificar.setFixedHeight(40)
        self.btn_verificar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_verificar.clicked.connect(self.procesar_verificacion)
        layout.addWidget(self.btn_verificar)

        # Botón reenviar código
        self.btn_reenviar = QPushButton("¿No recibiste el código? Reenviar")
        self.btn_reenviar.setObjectName("btnSecundario")
        self.btn_reenviar.setFixedHeight(36)
        self.btn_reenviar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reenviar.clicked.connect(self.reenviar_codigo_accion)
        layout.addWidget(self.btn_reenviar)

        # Botón volver al login
        self.btn_volver = QPushButton("Volver al Login")
        self.btn_volver.setObjectName("btnSecundario")
        self.btn_volver.setFixedHeight(36)
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.clicked.connect(self.volver_login)
        layout.addWidget(self.btn_volver)

        self.layout_maestro.addWidget(self.tarjeta_verificacion)

        # Aplicar estilos
        self.aplicar_estilos()

    def aplicar_estilos(self):
        """Aplica estilos de la tarjeta de verificación"""
        estilos = """
            VerifyEmailWindow {
                background-color: #1e1e1e;
            }
            QFrame#tarjetaVerificacion {
                background-color: #252526;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
            }
            QLineEdit#inputCustom {
                background-color: #3c3c3c;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit#inputCustom:focus {
                border: 1px solid #0078d4;
                background-color: #2d2d2e;
            }
            QPushButton#btnPrimario {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#btnPrimario:hover {
                background-color: #106ebe;
            }
            QPushButton#btnSecundario {
                background-color: #3c3c3c;
                color: #a19f9d;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton#btnSecundario:hover {
                background-color: #454547;
                color: #f5f5f5;
            }
        """
        self.setStyleSheet(estilos)

    def set_correo(self, correo):
        """Establece el correo del usuario para verificación"""
        self.correo_usuario = correo
        self.lbl_subtitle.setText(f"Hemos enviado un código de 6 dígitos a:\n{correo}\nEl código expira en 20 minutos.")

    def procesar_verificacion(self):
        """Procesa la verificación del código"""
        codigo = self.input_codigo.text().strip()
        
        if not codigo:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingresa el código de verificación.")
            return
        
        if len(codigo) != 6 or not codigo.isdigit():
            QMessageBox.warning(self, "Código Inválido", "El código debe contener exactamente 6 dígitos.")
            return
        
        # Verificar código en BD
        exito, mensaje = verificar_codigo(self.correo_usuario, codigo)
        
        if exito:
            QMessageBox.information(self, "¡Éxito!", mensaje)
            # Obtener el id del usuario
            id_usuario = obtener_id_por_correo(self.correo_usuario)
            if id_usuario:
                self.verificacion_exitosa.emit(id_usuario, self.correo_usuario)
            self.input_codigo.clear()
        else:
            QMessageBox.warning(self, "Error de Verificación", mensaje)
            self.input_codigo.clear()

    def reenviar_codigo_accion(self):
        """Reenvía un nuevo código de verificación"""
        if not self.correo_usuario:
            QMessageBox.warning(self, "Error", "No se encontró el correo del usuario.")
            return
        
        exito, mensaje = reenviar_codigo(self.correo_usuario)
        
        if exito:
            QMessageBox.information(self, "Código Reenviado", mensaje)
            self.input_codigo.clear()
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def volver_login(self):
        """Vuelve a la ventana de login"""
        self.input_codigo.clear()
        self.correo_usuario = None
        self.volver_a_login.emit()
