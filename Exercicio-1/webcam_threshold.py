import cv2          # Importa a biblioteca OpenCV para processamento de imagens
import numpy as np  # Importa o NumPy para operacoes com arrays (usado para empilhar imagens)

# Define o nome da janela principal como uma constante reutilizavel
WINDOW_NAME = "Webcam - Threshold em Tempo Real"

# Largura de cada imagem apos redimensionamento (3 imagens lado a lado cabem na tela)
IMG_WIDTH = 426   # 426 * 3 = 1278 pixels de largura total (cabe em telas 1280+)
IMG_HEIGHT = 320  # Altura proporcional para cada imagem

def main():
    # Inicializa a captura de video usando a webcam padrao (indice 0)
    cap = cv2.VideoCapture(0)

    # Verifica se a webcam foi aberta corretamente; encerra o programa se falhar
    if not cap.isOpened():
        print("Erro: nao foi possivel acessar a webcam.")
        return

    # Cria a janela principal em modo normal (redimensionavel)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    # Cria uma trackbar chamada "Threshold" na janela principal
    # Valor inicial: 127 | Valor maximo: 255 | Callback vazio pois lemos o valor manualmente
    cv2.createTrackbar("Threshold", WINDOW_NAME, 127, 255, lambda x: None)

    # Instrucoes exibidas no terminal
    print("Pressione 'q' para sair.")
    print("Teste os valores de threshold: 50, 127 e 200 usando a trackbar.")

    # Loop principal: executa continuamente ate o usuario pressionar 'q'
    while True:
        # Captura um frame da webcam; ret indica sucesso (True/False), frame e a imagem capturada
        ret, frame = cap.read()

        # Se a captura falhar (ex: webcam desconectada), exibe erro e encerra o loop
        if not ret:
            print("Erro: nao foi possivel capturar o frame.")
            break

        # Le o valor atual da trackbar (0 a 255) para usar como limite do threshold
        threshold_value = cv2.getTrackbarPos("Threshold", WINDOW_NAME)

        # Redimensiona o frame original para o tamanho definido (cabe na tela ao lado das outras)
        frame_resized = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))

        # Converte o frame redimensionado para escala de cinza (1 canal)
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

        # Aplica o threshold binario: pixels acima do limite viram branco (255), abaixo viram preto (0)
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

        # Converte a imagem cinza para BGR (3 canais) para poder empilhar com as outras
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # Converte a imagem threshold para BGR (3 canais) pelo mesmo motivo
        thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        # Define a fonte usada para os textos sobrepostos nas imagens
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Escreve o texto "Original" no canto superior esquerdo da imagem original
        cv2.putText(frame_resized, "Original", (10, 30), font, 0.8, (0, 255, 0), 2)

        # Escreve o texto "Escala de Cinza" na imagem em cinza
        cv2.putText(gray_bgr, "Escala de Cinza", (10, 30), font, 0.8, (0, 255, 0), 2)

        # Escreve o valor atual do threshold na imagem binarizada (atualiza em tempo real)
        cv2.putText(thresh_bgr, f"Threshold: {threshold_value}", (10, 30), font, 0.8, (0, 255, 0), 2)

        # Empilha as tres imagens horizontalmente em uma unica imagem para exibicao conjunta
        combined = np.hstack((frame_resized, gray_bgr, thresh_bgr))

        # Exibe a imagem combinada na janela unica
        cv2.imshow(WINDOW_NAME, combined)

        # Aguarda 1ms por uma tecla pressionada; aplica mascara para compatibilidade com 64 bits
        key = cv2.waitKey(1) & 0xFF

        # Se a tecla 'q' for pressionada, encerra o loop
        if key == ord('q'):
            break

    # Libera o recurso da webcam apos o encerramento do loop
    cap.release()

    # Fecha todas as janelas abertas pelo OpenCV
    cv2.destroyAllWindows()

# Ponto de entrada do programa: chama a funcao main() apenas quando executado diretamente
if __name__ == "__main__":
    main()
