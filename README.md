# pacman
Computer-played simplified pacman with maze generation and pathfinding.

## Features
- [X] Randomized DFS maze generation
- [X] A* pathfinding
- [X] Greedy algorithm pathfinding

You may also play the generated maze yourself. Use arrow keys to move the player (green square) in order to reach the goal (red square).
Once you've reached the goal, a program will close and the maze image will be saved to ``./media/maze.png``.


## Installation
Install `tkinter`:

- GNU/Linux based systems:
  - Debian based (Debian, Ubuntu, Pop\_OS!):
    
    ```
    apt-get install python3-tk
    ```
  - Arch based (Arch, Manjaro):
    
    ```
    pacman -S tk
    ```
  - Fedora based:
    
    ```
    dnf install python3-tkinter
    ```
    
  - RHEL, CentOS, Oracle Linux:

    ```
    yum install -y tkinter tk-devel
    ```

Install required libraries:

```
pip install -r requirements.txt
```


## Launching
Launch:
```
python main.py
```


# Examples
Maze `40 x 60`:

![maze](https://user-images.githubusercontent.com/28676554/158453045-26450675-2ee6-415a-979d-d63f2934f2fe.png)

Solved maze `40 x 60`:

![maze](https://user-images.githubusercontent.com/28676554/158602954-64d3e254-cc79-4cf1-a087-50466bd3f1a8.png)


## Configuration
Change maze's width and height: `constants.py > ROWS, COLUMNS`

