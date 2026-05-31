# ♟️ Chess Game — Computer Networks Project

A real-time two-player chess application built with a client-server architecture over TCP sockets.

---
![Python](https://img.shields.io/badge/Language-Python-blue)
![Socket Programming](https://img.shields.io/badge/Networking-TCP%20Sockets-green)
![AWS EC2](https://img.shields.io/badge/Cloud-AWS%20EC2-orange)
![Qt](https://img.shields.io/badge/GUI-Qt-yellow)
---
## 👥 Authors

- **Hakan Kocaman**
- **Ahmet Emin Uğurlu**
  
---

## 🎮 How to Play

The server is hosted on **AWS EC2 (Ubuntu)**. You don't need to set up anything — just download the client and play.

1. Download the latest `chess_game.exe` from the [Releases](../../releases) page
2. Run the executable
3. Enter the server IP (13.61.144.160) and connect
4. Wait for a second player to join and start playing

---

## 🏗️ Project Structure

```
Chess_Game_Computer_Networks/
├── backend/                # Server side
│   ├── server.py           # Main server, connection management
│   ├── gateway.py          # Handles and routes client requests
│   ├── controllers.py      # Request controllers
│   ├── services.py         # Business logic services
│   ├── player.py           # Player object and list
│   ├── socket_manager.py   # Socket configuration
│   ├── global_variables.py # Game state variables
│   └── logger.py           # Logging
│
├── models/                 # Chess piece models
│   ├── ChessPiece.py       # Abstract base class
│   ├── GameBoard.py        # 8x8 game board
│   ├── Pawn.py
│   ├── Rook.py
│   ├── Knight.py
│   ├── Bishop.py
│   ├── Queen.py
│   └── King.py
│
├── dtos/                   # Data Transfer Objects
│   ├── client_requests.py  # Client → Server requests
│   └── server_responses.py # Server → Client responses
│
└── zcilent/                # Client side (PySide6 GUI)
    ├── connectscreen.py    # Connection screen & network thread
    └── frame.py            # Game board UI
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, TCP Socket |
| Frontend | Python 3, PySide6 |
| Communication | Pickle (binary serialization) |
| Server | AWS EC2 (Ubuntu) |
| Concurrency | Python threading |
| Logging | Python logging module |

---

## 🌐 Architecture

```
Client A (Windows .exe)
        |
        |  TCP Socket (pickle)
        |
   [ AWS EC2 Ubuntu Server ]
        |   gateway.py → controllers.py → services.py
        |   models/ (chess logic)
        |
Client B (Windows .exe)
```

- Server listens on port `5050`
- Server Ip: '13.61.144.160'
- Each client runs in a separate thread
- All game state is managed server-side
- Clients send requests, server broadcasts responses


## ♟️ Game Features

- Real-time two-player chess over the network
- Full chess piece movement validation
- Check and checkmate detection
- Capture detection
- Turn management
- In-game chat
- Automatic game reset after match ends
- Connection loss handling

---

## 👥 Authors

- **Hakan Kocaman**
- **Ahmet Emin Uğurlu**
  
---
