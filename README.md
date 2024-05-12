# s28330
# Project Snake

*A web-based implementation of the classic Snake game built with Python.*

## Project Requirements and Goals

**Target Audience**

* Casual players seeking a nostalgic gaming experience.
* Players familiar with the classic Snake game.
* Individuals looking for a simple yet engaging challenge.

**Core Gameplay**

* Intuitive directional controls (arrow keys or WASD).
* Food items randomly placed on the game board.
* Snake grows in length upon consuming food.
* Game over upon collision with walls or the snake's body.
* Real-time score display.

**Success Criteria**

* A playable Snake game with core mechanics implemented.
* User-friendly interface with clear visual or text-based gameplay.
* Database integration for storing player names and scores.

**Stretch Goals**
* **Multiplayer Mode:**  Enable collaborative play where multiple players contribute to controlling the snake's movements, fostering teamwork and coordination.
* **Dynamic Obstacles:** Introduce obstacles within the playing field that increase in complexity or frequency over time, requiring strategic navigation and adaptation.

## Installation and Setup

### Prerequisites
- Python 3.10 or later
- Docker (optional for containerization)

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/project-snake.git
   cd project-snake
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Run the application:**
   ```bash
   python app.py
This will start the Flask server on http://localhost:5000.

### Using Docker
1. **Build the Docker image**
   ```bash
   docker build -t snake-game .

3. **Run the Docker container:**
   ```bash
   docker run -p 5000:5000 snake-game
Access the game at http://localhost:5000.

### How to Play
* Navigate to http://localhost:5000 in your web browser.
* Use the mouse for clicking the direction buttons to control the direction of the snake.
* Try to eat as much food as possible without colliding with the walls or the snake's body.


