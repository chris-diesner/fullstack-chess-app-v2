# Projektbeschreibung

## Projektname
Fullstack ChessApp v2

English below

---

## Projektziel
Das Ziel ist die Entwicklung eines Schachspiels mit vollständiger Spiellogik, das sowohl die grundlegenden als auch die komplexeren Regeln des Spiels abbildet. Es soll bewusst auf die Verwendung von bestehenden Bibliotheken verzichtet werden, die Schachregeln und -abläufe bereits vorgeben. Entgegen meiner vorherigen Schach App, habe ich dieses Projekt gleich als Fullstack Projekt konzeptioniert.

---

## Entwicklungsschritte

### Konzeptionierung 
Da nun in diesem Projekt nicht nur die Entwicklung der Programmlogik im Vordergrund stand, sondern auch wesentliche End-to-End-Funktionalitäten implementiert werden sollen, wurden zu Beginn klare Entwicklungsabschnitte nach dem Konzept des **Vertical Slicing** definiert. Diese Strukturierung ermöglicht eine fokussierte und iterative Entwicklung:

1. **Grundlegendes Spielfeld**
    - Aufbau des Schachbretts.
    - Initialisierung der Figurenpositionen.
    - Darstellung des Schachbretts 
    - Erstellen der Figurenklassen mit ihren spezifischen Bewegungsregeln

2. **Bewegungslogik**
    - Implementierung der Bewegungslogiken für alle Figuren.
    - Überprüfung der Gültigkeit eines Zugs.
    - Erkennung von Schach, Schachmatt oder Remis.
    - Implementierung spezieller Regeln wie „Rochade“, "Bauernumwandlung" und „En Passant“.

3. **Benutzerverwaltung**
    - Datenbankverknüfung für Userverwaltung und Game Sessions.
    - Speicherung und Anzeige der Zughistorie.


Von Beginn an wurde überwiegend **testgetrieben entwickelt**. Dies erleichtert die Implementierung der Methoden gemäß der Schachregeln und stellt sicher, dass jede Erweiterung präzise und robust bleibt. Die Entwicklung wurde auf verschiedene Branches aufgeteilt, um parallele Arbeiten zu ermöglichen. Zusätzlich wurde **Continuous Integration (CI)** eingerichtet, um alle Tests automatisch auszuführen und sicherzustellen, dass nur funktionierende Branches in den Hauptzweig gemergt werden.

Ebenfalls wurde **Continuous Deployment** für das Fullstack Projekt eingerichtet, um auch die vollen Funktionalitäten in einer Serverumgebung zu testen.

Außerdem wurde sich bereits im Vorfeld eines jeden Entwicklungsschritts Gedanken über Struktur und Methodik gemacht und dieses in ERD bzw. UML-Diagrammen skizziert. Es sei dazu gesagt, dass es dabei zu gewisse Inkonsistenzen bei der Benennung von Methoden und Atributen kam. ;) 

**ERD Konzept**

![{0DA5029C-E033-4E30-90E0-975E136EBE3D}](https://github.com/user-attachments/assets/c3316a1d-befe-4233-bc3b-a5b2a3787108)

---

### Implementierungsschritte

#### **1. Grundlegendes Spielfeld**
Der erste Entwicklungsabschnitt konzentrierte sich auf die grundlegende Logik des Schachbretts:
- **Modellierung des Spielfelds:** 
    - Das Schachbrett wurde als 2-dimensionales Array implementiert, in dem jedes Feld durch seine Koordinaten (`[Zeile][Spalte]`) referenziert wird.
    - Jedes Feld kann entweder leer sein oder eine Schachfigur enthalten.
- **Initialisierung der Startaufstellung:**
    - Figuren wie Bauern, Läufer und Türme (etc.) wurden als Objekte erstellt und auf den entsprechenden Startfeldern des Bretts positioniert.
    - Jedes Figurenobjekt enthält Attribute wie Farbe (weiß oder schwarz), aktuelle Position und spezifische Bewegungsregeln.
    - Jede Figur erhielt ihre spezifischen Bewegungsregeln:
        - Der **pawn** kann sich nach vorne bewegen und diagonal schlagen.
        - Der **bishop** bewegt sich nur diagonal, ohne Figuren zu überspringen.
        - Der **rook** bewegt sich orthogonal, ebenfalls ohne Hindernisse zu überspringen.
        - Die **queen** kombiniert die Bewegungsregeln von rook und bishop.
        - Der **king** kann sich nur ein Feld in jede Richtung bewegen.
        - Der **knight** kann sich im L-Muster bewegen und darf Gegner überspringen.
    - Die Bewegungsregeln wurden durch eigene Methoden wie `is_move_valid` in den jeweiligen Figurenklassen umgesetzt.
    - Alle Bewegungsregeln wurden mit unittests abgesichert.
- **API Schnittstellen definieren:**
    - Unter Verwendung von FastAPI wurde eine erste API Schnittstelle (GET) eingerichten, um den aktuellen Brettzustand abrufbar zu machen.
    - Die Funktionalität wurde mit einem Integration Test abgesichert.
- **Darstellung des Schachbretts:**
    - Eine einfache Darstellung des Schachbretts im Frontend mit dem Framework react und der Abruf des aktuellen Brettzustands vom Backend.
 
- **vereinfachte UML-Darstellung**

![grafik](https://github.com/user-attachments/assets/9106faac-a809-4a1d-8851-d888122ded15)


#### **2. Bewegungslogik**
Die zweite Phase umfasste die Implementierung der Bewegungslogiken und die Validierung von Zügen:
- **Figurenbewegungen:**
    - Die Bewegungslogiken stellt sicher, dass die Figuren sich gemäß ihrer vorher definierten Regeln bewegen können, sich das Brett nach dem Zug aktualisiert und ein Spielerwechsel vollzugen wird.
- **Validierung der Züge:**
    - Vor jedem Zug wird überprüft:
        - **Spielfeldgrenzen:** Der Zug darf das Schachbrett nicht verlassen.
        - **Blockaden:** Figuren dürfen keine anderen Figuren überspringen (außer knight).
        - **Zielposition:** Das Zielfeld muss entweder leer sein oder eine gegnerische Figur enthalten.
     
          ![grafik](https://github.com/user-attachments/assets/b3764f78-09a1-4ca8-bb3b-67c3a5931607)


- **Schach- und Schachmatt-Erkennung:**
    - Die Spiellogik wurde erweitert, um Situationen zu erkennen, in denen der king bedroht ist.
    - „Schachmatt“ wird erkannt, wenn keine gültigen Züge mehr verfügbar sind, um die Bedrohung zu beseitigen.
 
        ![grafik](https://github.com/user-attachments/assets/6d9e58d9-9c55-491e-8b3c-4919603a9539)


- **Spezialregeln:**
    - **Rochade:**
        - Die Rochade wurde implementiert, sodass der König und ein Turm gleichzeitig bewegt werden können, wenn:
            - Weder der König noch der Turm zuvor bewegt wurden.
            - Keine Figuren zwischen ihnen stehen.
            - Der König nicht im Schach steht oder durch die Rochade ins Schach gerät.
    - **Bauernumwandlung:**
        - Wenn ein Bauer die letzte Reihe erreicht, wird der Spieler aufgefordert, ihn in eine beliebige andere Figur umzuwandeln.
    - **En Passant:**
        - Diese Regel erlaubt es einem Bauern, einen gegnerischen Bauern zu schlagen, der im vorherigen Zug zwei Felder vorgerückt ist. Um dies umzusetzen:
            - Die Zughistorie wurde erweitert, um den letzten Zug eines Bauern zu speichern.
            - Vor jedem Zug wird überprüft, ob „En Passant“ möglich ist.

          ![grafik](https://github.com/user-attachments/assets/45971df2-1b95-4320-8210-13b627c4e519)


- **Testszenarien:**
    - Für jede Figur wurden Unit Tests erstellt, die typische und komplexe Spielsituationen abdecken, um die Einhaltung der Bewegungsregeln sicherzustellen.


#### **3. Benutzerverwaltung und Datanbankanbindung**
Die dritte Phase konzentrierte sich auf die Implementierung und Validierung von Spezialregeln:
- **WIP:**
    - 
     


- **Testszenarien:**
    - WIP

---

### ChangeLog:

# 🚀 Fullstack Chess App - Changelog

## **Version 1.0.0 – Initial Backend and Frontend Integration**

**Date:** 2025-02-06  
**Status:** ✅ Stable  

---

### **🔹 Backend (FastAPI, Python)**

#### **API Structure & Modular Design**
- Introduced a structured **FastAPI** architecture with separate routers.
- `router/game_api.py` handles retrieving the current board state.
- **Central API (`app.py`)** manages all routes and middleware.

#### **Chessboard Logic (`chess_board.py`)**
- Implemented game logic with complete piece positioning.
- JSON-based board representation for seamless API integration.

#### **Dynamic API Endpoints**
- **`GET /game/board`** → Returns the current chessboard state in JSON format.

#### **Testing & CI/CD**
- Introduced **`pytest`-based unit testing for the backend**.
- Integrated **unit tests for piece movement & board logic**.
- **API integration tests (`test_api.py`)** implemented.

---

### **🔹 Frontend (React, TypeScript)**

#### **Fetching Board State from API**
- Implemented a **`useEffect` hook** for periodic API calls.
- Used **`fetch()`** for backend communication.

#### **Rendering the Chessboard**
- Created a **`ChessBoard` component**, processing JSON data from the backend.
- Positioned pieces dynamically based on **API response (`/game/board`)**.

#### **Error Handling & Loading States**
- Displayed a **loading animation** while fetching the API response.
- **Error messages** appear when the backend is unreachable or returns an incorrect response.

---

## **🐞 Fixes & Improvements**
- **Removed unnecessary duplication in `figure.py` and replaced it with inheritance**.
- **Optimized test structure:** Used `@pytest.fixture` for consistent test data.


----


## Project goal
The aim is to develop a chess game with complete game logic that maps both the basic and the more complex rules of the game. The aim is to deliberately avoid using existing libraries that already contain chess rules and sequences. In contrast to my previous chess app, I designed this project as a full-stack project.

---

## Development steps

### Conceptualization 
As the focus of this project was not only on developing the program logic, but also on implementing key end-to-end functionalities, clear development phases were defined at the beginning according to the concept of **vertical slicing**. This structure enables focused and iterative development:

1. **Basic playing field**
 - Setting up the chessboard.
 - Initialization of the piece positions.
 - Representation of the chessboard.
 - Creation of the piece classes with their specific movement rules.

2. **Movement logic**
    - implementation of the movement logics for all pieces.
    - Checking the validity of a move.
    - Recognition of check, checkmate or draw.
    - Implementation of special rules such as "castling", "pawn conversion" and "en passant".

3. **User administration**
    - database linking for user administration and game sessions.
    - Storage and display of move history.

As no input/output for user interaction has been implemented to date, the development can only be traced via the unit tests.

Right from the start, development was predominantly **test-driven**. This facilitates the implementation of the methods according to the chess rules and ensures that each extension remains precise and robust. The development was split across different branches to enable parallel work. In addition, **Continuous Integration (CI)** was set up to run all tests automatically and ensure that only working branches are merged into the main branch.

Furthermore, the structure and methodology of each development step was considered in advance and outlined in ERD and UML diagrams. It should be noted that there were certain inconsistencies in the naming of methods and attributes ;) 

---

### Implementation steps

#### **1. Basic board**
The first stage of development focused on the basic logic of the chessboard:
- **Modeling the board:** 
 - The chessboard was implemented as a 2-dimensional array in which each square is referenced by its coordinates (`[row][column]`).
    - Each field can either be empty or contain a chess piece.
- **Initialization of the starting position:**
 - Pieces such as pawns, bishops and rooks (etc.) have been created as objects and positioned on the corresponding starting squares of the board.
    - Each piece object contains attributes such as color (white or black), current position and specific movement rules.
    - Each figure was given its own specific movement rules:
        - The **pawn** can move forward and strike diagonally.
        - The **bishop** only moves diagonally without jumping over figures.
        - The **rook** moves orthogonally, also without jumping over obstacles.
        - The **queen** combines the movement rules of rook and bishop.
        - The **king** can only move one square in each direction.
        - The **knight** can move in an L-pattern and may jump over opponents.
    - The movement rules were implemented in the respective figure classes using custom methods such as `is_move_valid`.
    - All movement rules were secured with unittests.
-  Define API interfaces:**
 - Using FastAPI, a first API interface (GET) was set up to make the current board status available.
    - The functionality was validated with an integration test.
- **Display of the chessboard:**
 - A simple display of the chessboard in the frontend with the framework react and the retrieval of the current board status from the backend.
 
#### **2. Movement logic**
The second phase comprised the implementation of the movement logic and the validation of moves:
- **Movement  of pieces:**
 - The movement logic ensures that the pieces can move according to their previously defined rules, that the board updates after the move and that a player change is completed.
- **Move validation:**
 - A check is made before each move:
        - **Playing area limits:** The move must not leave the chessboard.
        - **Blockades:** Pieces may not jump over other pieces (except knight).
        - **Target position:** The target square must either be empty or contain an opponent's piece.
- **Rochade:**
    - Castling was implemented so that the king and a rook can be moved simultaneously if:
        - Neither the king nor the rook have been moved before.
        - There are no pieces between them.
        - The king is not in check or is put in check by castling.
- **Pawn conversion:**
    - When a pawn reaches the last rank, the player is asked to convert it to any other piece (by default to a queen).
- **En Passant:**
    - This rule allows a pawn to capture an opponent's pawn that has advanced two squares in the previous move. To implement this:
        - The move history has been extended to store the last move of a pawn.
        - Before each move, a check is made to see whether “En Passant” is possible.

- **Test scenarios:**
    - Each scenario, including valid and invalid applications of these rules, has been validated by testing.

- **Check and checkmate detection:**
 - The game logic has been enhanced to recognize situations where the king is threatened.
    - “Checkmate” is recognized when there are no more valid moves available to eliminate the threat.

#### **3. User administration and database connection**
The third phase focused on the implementation and validation of special rules:
- **WIP:**
 - 
 


- **Test scenarios:**
 - WIP