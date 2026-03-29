# Exercício 3 — Face Tracking → Realidade Virtual

Projeto da disciplina de **Visão Computacional / Realidade Aumentada e Virtual**.

O sistema captura rostos em tempo real pela câmera, detecta e identifica cada pessoa via OpenCV, e renderiza avatares 3D correspondentes dentro de uma cena de Realidade Virtual com A-Frame — tudo sincronizado via WebSocket.

## O que o sistema faz

- Captura o feed da câmera (celular ou PC) em tempo real
- Detecta rostos usando **Haar Cascade** (OpenCV) no servidor Python
- Extrai as coordenadas X, Y e o tamanho de cada rosto detectado
- Mapeia essas coordenadas 2D para posições 3D no espaço A-Frame (VR)
- Renderiza um avatar (esfera + corpo) para cada pessoa detectada
- Atualiza as posições em tempo real conforme as pessoas se movem
- Exibe o ID de cada pessoa (`Pessoa 1`, `Pessoa 2`...) como label no mundo virtual
- Permite que múltiplos dispositivos se conectem: uns com câmera, outros só visualizando a cena VR

## Mapeamento de coordenadas 2D → 3D

| Câmera (2D)                        | Mundo VR (3D)                                |
| ---------------------------------- | -------------------------------------------- |
| Rosto à esquerda da imagem         | Avatar à esquerda no VR (X negativo)         |
| Rosto à direita da imagem          | Avatar à direita no VR (X positivo)          |
| Bounding box grande (rosto perto)  | Avatar mais próximo no VR (Z menos negativo) |
| Bounding box pequena (rosto longe) | Avatar mais afastado no VR (Z mais negativo) |
| Altura                             | Fixo em 1.5m (nível dos olhos)               |

Fórmulas usadas em `server.py`:

```
vr_x = (centro_x / largura_frame - 0.5) * 10   → intervalo [-5, +5] metros
vr_z = -2.0 a -8.0                               → baseado no tamanho da bbox
```

## Tecnologias

| Camada              | Tecnologia                                    |
| ------------------- | --------------------------------------------- |
| Backend             | Python 3.10+, Flask, Flask-SocketIO, Eventlet |
| Visão Computacional | OpenCV (Haar Cascade), NumPy                  |
| Pose / Mãos         | MediaPipe Tasks API                           |
| Frontend            | HTML5, CSS3, JavaScript (ES6+)                |
| Realidade Virtual   | A-Frame 1.6 (WebXR)                           |
| 3D alternativo      | Three.js r160                                 |
| WebSocket           | Socket.IO v4                                  |
| IA (opcional)       | OpenAI API (gpt-4o-mini, gpt-4o)              |

## Estrutura do projeto

```
Exercicio-3/
├── server.py               # Servidor Flask + Socket.IO + pipelines de CV
├── requirements.txt        # Dependências Python
├── models/                 # Modelos MediaPipe (baixados automaticamente, ignorados pelo git)
├── static/
│   ├── css/style.css       # Estilos globais
│   ├── js/
│   │   ├── arvr.js         # Cliente AR/VR (Socket.IO + A-Frame)
│   │   ├── cv.js           # Cliente Visão Computacional
│   │   ├── cv3d.js         # Cliente CV → 3D (Three.js)
│   │   └── worldgen.js     # Cliente AI World Generator
│   └── vendor/             # Bibliotecas JS locais (aframe, socket.io, three.js)
└── templates/
    ├── index.html          # Página inicial com links para todas as interfaces
    ├── arvr.html           # Cena 3D interativa com painel de controle
    ├── cv.html             # Interface de Visão Computacional
    ├── cv3d.html           # Ponte CV → Three.js 3D
    ├── worldgen.html       # Gerador de mundos via OpenAI
    └── face_vr.html        # Face Tracking → Realidade Virtual (novo)
```

## Como rodar

### Windows

```bash
# Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar o servidor
python server.py
```

### Linux / macOS / WSL

```bash
# Instalar dependências nativas do OpenCV/MediaPipe
sudo apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libgles2 libegl1

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt

# Rodar o servidor
python server.py
```

Acesse **http://localhost:5000**

Na primeira execução, os modelos do MediaPipe são baixados automaticamente para a pasta `models/`.

> **Windows:** o MediaPipe não consegue abrir arquivos em caminhos com acentos. Os modelos são salvos em `C:\Users\<usuario>\mediapipe_models\` automaticamente.

## Interfaces disponíveis

### 👤 Face Tracking → VR (`/face_vr`) — principal deste exercício

Página que integra câmera em tempo real com cena de Realidade Virtual:

- **Painel esquerdo:** feed da câmera ao vivo + frame anotado com os bounding boxes e coordenadas VR de cada rosto + lista de pessoas detectadas
- **Painel direito:** cena A-Frame com avatares 3D, um por rosto detectado, com label "Pessoa N" flutuante, animação de pulsação e indicador de profundidade
- Suporte a câmera frontal e traseira (celular)
- FPS de envio configurável (5, 10, 15, 20)
- Múltiplos dispositivos podem se conectar simultaneamente: câmeras enviam frames, visualizadores veem os avatares

### 🏠 Página Principal (`/`)

Links para todas as interfaces com resumo do projeto.

### 🥽 AR/VR (`/arvr`)

Cena 3D interativa com A-Frame:

- Adicionar objetos (cubo, esfera, cilindro, cone, torus, dodecaedro)
- Alterar cor, mover, animar e remover objetos
- Presets de cor do céu (dia, noite, pôr do sol, nublado)
- Sincronização em tempo real entre todos os clientes conectados

### 👁 Visão Computacional (`/cv`)

Pipelines de processamento de imagem via OpenCV:

| Pipeline    | Descrição                                              |
| ----------- | ------------------------------------------------------ |
| `edges`     | Detecção de bordas com Canny                           |
| `contours`  | Detecção e contagem de contornos                       |
| `faces`     | Detecção de rostos com Haar Cascade                    |
| `color`     | Segmentação por cor (tons de verde no HSV)             |
| `blur`      | Desfoque Gaussiano                                     |
| `threshold` | Limiarização binária                                   |
| `hands`     | Detecção de mãos e contagem de dedos (MediaPipe)       |
| `pose`      | Detecção de pose corporal com articulações (MediaPipe) |

### 🔬 CV → 3D Bridge (`/cv3d`)

Ponte entre Visão Computacional e Three.js:

- 3 painéis: feed original, resultado CV e cena 3D
- Rostos detectados viram esferas; contornos viram formas extrudadas; bordas viram nuvem de pontos

### 🤖 AI World Gen (`/worldgen`)

Gerador de mundos 3D via OpenAI (requer `OPENAI_API_KEY`):

- Digite um prompt em linguagem natural (ex.: "floresta à noite com vagalumes")
- A IA gera uma cena completa em A-Frame ou Three.js

## Conectar outro dispositivo na mesma rede

Descubra seu IP local e acesse pelo outro dispositivo:

```bash
# Windows
ipconfig

# Linux/macOS
hostname -I
```

No celular ou PC do professor:

```
http://SEU_IP:5000/face_vr
```

> O servidor já aceita conexões externas (`host="0.0.0.0"`). Se necessário, libere a porta 5000 no firewall do Windows:
>
> ```bash
> netsh advfirewall firewall add rule name="Flask 5000" dir=in action=allow protocol=TCP localport=5000
> ```

> **HTTPS:** navegadores móveis bloqueiam acesso à câmera via HTTP. Para usar a câmera em outro dispositivo, utilize **ngrok** para criar um túnel HTTPS: `ngrok http 5000`.

## API WebSocket — Sala `face_vr`

| Evento (cliente → servidor) | Payload           | Descrição                                |
| --------------------------- | ----------------- | ---------------------------------------- |
| `join_face_vr`              | —                 | Entra na sala e recebe confirmação       |
| `face_vr_frame`             | `{image: base64}` | Envia frame JPEG para detecção de rostos |

| Evento (servidor → cliente) | Payload                   | Descrição                         |
| --------------------------- | ------------------------- | --------------------------------- |
| `face_vr_ready`             | `{message}`               | Servidor pronto                   |
| `face_vr_update`            | `{faces[], count, image}` | Rostos detectados + frame anotado |

Estrutura de cada objeto em `faces[]`:

```json
{
  "id": 1,
  "label": "Pessoa 1",
  "vr": { "x": 2.1, "y": 1.5, "z": -4.3, "scale": 0.65 },
  "bbox": { "x": 120, "y": 80, "w": 90, "h": 90 }
}
```

```bash
# Linux/macOS
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."
```
