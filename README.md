# MusiCube (Pygame Music Generator)

This is a pygame project that uses the musicgen model from the audiocraft library to generate music based on the user's interactions with a 3D interface. The game consists of a controller cube of white color and collision cubes of green and cyan color. The user can move the controller cube with the arrow keys and collide with the other cubes. Each collision has a different effect on the music generation:

- When the user collides with a green cube, it generates a token of music genre such as soothing, guitar, rock, pop, etc. The token is added to a list of tokens that represents the current musical prompt. For example, if the user collides with three green cubes that generate soothing, guitar, and rock tokens, the prompt will be [soothing, guitar, rock].
- When the user collides with a cyan cube, it removes the last token from the list of tokens. For example, if the prompt is [soothing, guitar, rock], after colliding with a cyan cube, it will be [soothing, guitar].
- The user can see their score on the top left corner of the screen. The score is calculated based on the number and type of collisions. Green collisions add points, while cyan collisions subtract points.
- After some collisions, when the prompt has enough tokens, it is sent to the musicgen model to generate music based on the prompt. The music is played in a loop until a new prompt is generated.
- The game continues until the user presses the escape key to quit.

## Installation and Usage

To set up this project locally and run or make contributions, follow these steps:

1. Create a virtual environment using `python -m venv env` and activate it using `env\Scripts\activate` on Windows or `source env/bin/activate` on Linux/MacOS.
2. Install the required packages from requirements.txt using `pip install -r requirements.txt`.
3. Run the script using `python AudioCraft-3D-POC.py`.

Alternatively, you can download and run the executable file of our game from [here].

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.

## Acknowledgements

We would like to thank the following sources for their help and inspiration:

- The audiocraft library for providing the musicgen model that can generate music from text prompts. You can find more information about it [here].
- The pygame library for providing the tools to create a 3D interface and handle user input. You can find more information about it [here].
- The pyopengl library for providing the functions to render 3D graphics in pygame. You can find more information about it [here].
