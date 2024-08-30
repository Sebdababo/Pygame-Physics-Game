# Pygame Physics Game Collection

Welcome to the Pygame Physics Game Collection! This repository contains two fun and interactive games developed using the Pygame library. Each game has its own unique gameplay mechanics and features. Below you'll find detailed instructions for setting up and playing both games.

## Game 1: Bouncy Ball

In Bouncy Ball, you control a ball that bounces around the screen, collecting points and avoiding obstacles. The goal is to accumulate the highest score possible.

### Features

- Bouncing ball with user-controlled movement
- Randomly placed obstacles
- Randomly placed points to collect
- Invincibility power-ups
- Score tracking

### Controls

- Arrow Keys: Move the ball
- Invincibility: Collect green power-ups
- Quit: Close the game window

### How to Play

1. **Setup and Installation**
   - Ensure you have Python and Pygame installed.
   - Run the following command to install Pygame if you don't have it already:
     ```bash
     pip install -r requirements.txt
     ```

2. **Running the Game**
   - Navigate to the directory containing `main.py`.
   - Run the game using the following command:
     ```bash
     python main.py
     ```

3. **Gameplay**
   - Use the arrow keys to move the ball.
   - Avoid blue obstacles.
   - Collect yellow points to increase your score.
   - Collect green power-ups to become invincible for a short period.
   - The game keeps running until you close the window.

### Example Gameplay
![Physics Game 1 output](https://github.com/user-attachments/assets/38e70683-2e45-4fb9-a558-62b58dba7b56)

## Game 2: Enhanced Chaos Pendulum Simulation

In this simulation, you can create and manipulate a chaos pendulum. The pendulum consists of joints connected by lines, and you can control gravity, damping, and colors.

### Features

- Interactive pendulum creation and manipulation
- Adjustable gravity and damping
- Trail color changing
- Real-time physics simulation

### Controls

- Left Click: Add a joint
- Right Click: Remove the last joint
- Mouse Drag: Move a selected joint
- Space: Pause/Resume the simulation
- C: Change the trail color
- Arrow Up/Down: Increase/Decrease gravity
- Arrow Left/Right: Increase/Decrease damping
- R: Reset the simulation

### How to Play

1. **Setup and Installation**
   - Ensure you have Python and Pygame installed.
   - Run the following command to install Pygame if you don't have it already:
     ```bash
     pip install pygame
     ```

2. **Running the Game**
   - Navigate to the directory containing `game.py`.
   - Run the game using the following command:
     ```bash
     python game.py
     ```

3. **Gameplay**
   - Left-click to add joints to the pendulum.
   - Right-click to remove the last joint.
   - Drag with the left mouse button to move a joint.
   - Press Space to pause or resume the simulation.
   - Press C to change the color of the pendulum trail.
   - Use the arrow keys to adjust gravity and damping.
   - Press R to reset the simulation.

### Example Simulation
![Physics Game 2 output](https://github.com/user-attachments/assets/00dc9260-0622-4867-aaa3-77c406fadd74)

