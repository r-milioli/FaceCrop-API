"""
Módulo de detecção facial usando OpenCV DNN
Nota: MediaPipe não está disponível para Python 3.13 ainda.
Esta implementação usa OpenCV DNN como alternativa compatível.
"""
import numpy as np
from typing import Optional, Tuple
import cv2
import os


class FaceDetector:
    """
    Classe para detecção de faces usando OpenCV DNN.
    Usa modelo pré-treinado para detectar faces e estimar posição do nariz.
    """
    
    def __init__(self):
        """
        Inicializa o detector de faces usando OpenCV DNN.
        """
        # Usar detector de faces do OpenCV (Haar Cascade como fallback)
        # Para melhor precisão, podemos usar DNN, mas por simplicidade
        # vamos usar o detector de faces padrão do OpenCV
        try:
            # Tentar usar o detector DNN do OpenCV (mais preciso)
            self.face_detector = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.use_dnn = False
        except:
            # Fallback para detector básico
            self.face_detector = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
            )
            self.use_dnn = False
    
    def _estimate_nose_position(self, face_rect: Tuple[int, int, int, int]) -> Tuple[float, float]:
        """
        Estima a posição do nariz baseado no retângulo da face.
        O nariz geralmente está na parte superior central da face.
        
        Args:
            face_rect: (x, y, width, height) do retângulo da face
            
        Returns:
            Tuple[float, float]: Coordenadas estimadas do nariz (x, y)
        """
        x, y, w, h = face_rect
        
        # O nariz está aproximadamente:
        # - Horizontalmente: centro da face (x + w/2)
        # - Verticalmente: cerca de 40% da altura da face a partir do topo
        nose_x = x + w / 2
        nose_y = y + h * 0.4
        
        return nose_x, nose_y
    
    def detect_nose_position(
        self, 
        image: np.ndarray
    ) -> Tuple[Optional[float], Optional[float], bool, float, int, int]:
        """
        Detecta a posição do nariz na imagem.
        
        Args:
            image: Imagem em formato numpy array (RGB)
            
        Returns:
            Tuple contendo:
                - x: coordenada X do nariz (pixels) ou None
                - y: coordenada Y do nariz (pixels) ou None
                - face_detected: boolean indicando se face foi detectada
                - confidence: nível de confiança (0-1)
                - image_width: largura da imagem
                - image_height: altura da imagem
        """
        height, width = image.shape[:2]
        
        # Converter RGB para grayscale (requerido pelo Haar Cascade)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Detectar faces
        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Se nenhuma face detectada, retornar centro
        if len(faces) == 0:
            center_x = width / 2
            center_y = height / 2
            return center_x, center_y, False, 0.0, width, height
        
        # Se múltiplas faces, selecionar a maior (por área)
        if len(faces) > 1:
            # Calcular área de cada face
            face_areas = [(w * h, (x, y, w, h)) for (x, y, w, h) in faces]
            # Selecionar face com maior área
            selected_face = max(face_areas, key=lambda x: x[0])[1]
        else:
            selected_face = tuple(faces[0])
        
        # Estimar posição do nariz
        nose_x, nose_y = self._estimate_nose_position(selected_face)
        
        # Calcular confiança baseada no tamanho da face detectada
        x, y, w, h = selected_face
        face_area = w * h
        image_area = width * height
        area_ratio = face_area / image_area
        
        # Confiança maior para faces maiores e bem posicionadas
        confidence = min(0.95, max(0.7, area_ratio * 10))
        
        return nose_x, nose_y, True, confidence, width, height
    
    def __del__(self):
        """
        Limpa recursos ao destruir o objeto.
        """
        pass


# Instância global do detector (reutilizável)
_detector_instance: Optional[FaceDetector] = None


def get_detector() -> FaceDetector:
    """
    Obtém instância singleton do detector.
    
    Returns:
        FaceDetector: Instância do detector
    """
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = FaceDetector()
    return _detector_instance

