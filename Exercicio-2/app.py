import cv2

# Carrega o classificador Haar Cascade treinado para detectar rostos frontais.
# O arquivo XML contém milhares de exemplos de rostos e não-rostos usados no treinamento.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Abre a webcam (0 = primeira câmera disponível no sistema)
cap = cv2.VideoCapture(0)

while True:
    # Lê um frame da webcam
    # ret: True se a leitura foi bem-sucedida | frame: a imagem capturada
    ret, frame = cap.read()
    if not ret:
        break  # Encerra se a câmera falhar

    # Converte o frame colorido (BGR) para escala de cinza.
    # O Haar Cascade analisa contraste de luz/sombra, não cor, então cinza é suficiente e mais rápido.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta rostos na imagem em escala de cinza.
    # scaleFactor=1.1 : reduz a imagem 10% a cada varredura para encontrar rostos de tamanhos diferentes
    # minNeighbors=5  : número mínimo de detecções vizinhas para confirmar um rosto (evita falsos positivos)
    # minSize=(30,30) : tamanho mínimo em pixels para considerar algo um rosto
    # Retorna uma lista de (x, y, largura, altura) para cada rosto encontrado
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Para cada rosto detectado, desenha um retângulo verde ao redor dele
    for (x, y, w, h) in faces:
        # (x, y) = canto superior esquerdo | (x+w, y+h) = canto inferior direito
        # (0, 255, 0) = cor verde em BGR | 2 = espessura da borda em pixels
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Exibe o texto "Rosto Detectado" apenas quando pelo menos um rosto for encontrado
    if len(faces) > 0:
        # Parâmetros: imagem, texto, posição (x,y), fonte, tamanho, cor, espessura
        cv2.putText(frame, 'Rosto Detectado', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exibe o frame processado (com retângulos e texto) em uma janela
    cv2.imshow('Deteccao de Rostos', frame)

    # Aguarda 1ms por uma tecla. Se for 'q', encerra o loop.
    # & 0xFF garante compatibilidade em sistemas de 64 bits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha todas as janelas abertas pelo OpenCV
cap.release()
cv2.destroyAllWindows()
