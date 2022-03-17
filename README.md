# pacman
Computer-played simplified pacman with maze generation and pathfinding.

- [X] Randomized DFS maze generation
- [X] A* pathfinding
- [X] Greedy algorithm pathfinding

You may also play the generated maze yourself. Use arrow keys to move the player (green square) in order to reach the goal (red square).
Once you've reached the goal, a program will close and the maze image will be saved to ``./media/maze.png``.

Install required libraries: ``pip install -r requirements.txt``

Launch: ``main.py``

Change maze's width and height: ``constants.py`` > ``ROWS, COLUMNS``

Example maze (40 rows, 60 columns):

![maze](https://user-images.githubusercontent.com/28676554/158453045-26450675-2ee6-415a-979d-d63f2934f2fe.png)

Example solved maze (40 rows, 60 columns):

![maze](https://user-images.githubusercontent.com/28676554/158602954-64d3e254-cc79-4cf1-a087-50466bd3f1a8.png)
