# Exercício 2 — Detecção de Rostos em Tempo Real

Programa de detecção de rostos via webcam usando OpenCV e Haar Cascade.

---

## O que é Detecção de Objetos?

Diferente do Threshold (que olha pixel por pixel), a detecção procura por **padrões**. O computador busca contrastes que lembram a anatomia humana: a sombra dos olhos, a linha do nariz e o brilho da testa.

## O que é o Haar Cascade?

É como um "manual de instruções" que o OpenCV usa. Ele contém milhares de exemplos do que é um rosto e do que não é. O arquivo utilizado é o `haarcascade_frontalface_default.xml`.

---

## Requisitos Técnicos

O programa deve obrigatoriamente:

- Carregar o classificador de face do OpenCV
- Capturar o vídeo da webcam
- Identificar as coordenadas (X, Y, Largura, Altura) do rosto
- Desenhar um retângulo colorido ao redor da face
- Exibir o texto "Rosto Detectado" na tela quando alguém aparecer

---

## Dependências

```bash
pip install opencv-python
```

- Python 3
- OpenCV (`cv2`)

---

## Como Executar

```bash
python app.py
```

Pressione **Q** para encerrar o programa.

---

## Conceitos para a Apresentação

Durante a explicação, demonstrar:

- O que o computador está procurando na imagem para decidir que aquilo é um rosto?
- O que acontece se você cobrir a boca ou os olhos? O algoritmo ainda funciona?
- A diferença entre **detectar** (saber que há um rosto) e **reconhecer** (saber de quem é o rosto).

---

## Investigação Obrigatória

Testar as seguintes situações e anotar os resultados:

| Situação | Resultado |
|---|---|
| **Distância** — até que distância da câmera o rosto ainda é detectado? | |
| **Óculos escuros** — o algoritmo funciona com acessórios? | |
| **Máscara** — e com a boca coberta? | |
| **Perfil** — o que acontece ao virar o rosto de lado? Por quê? | |
| **Múltiplas faces** — o programa consegue detectar 3 pessoas ao mesmo tempo? | |
