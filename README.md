# MusiCube: Interactive Pygame Music Generator

MusiCube is an innovative pygame project that utilizes the powerful musicgen model from the audiocraft library to create unique musical compositions based on user interactions within a captivating 3D environment. This project offers an engaging musical experience where users can actively participate in the music generation process.

## Project Overview

The core of MusiCube lies in its ability to generate music by analyzing the user's interactions with a dynamic 3D interface. The interface consists of various cubes, each serving a distinct purpose:

- **Controller Cube (White)**: This cube serves as the user's avatar within the 3D space. Users can navigate it using the arrow keys.

- **Collision Cubes (Green and Cyan)**: The environment is adorned with green and cyan cubes. Colliding with these cubes triggers different musical effects.

## User Interactions

MusiCube leverages user interactions to influence the music generation process:

- **Green Cube Collisions**: Upon colliding with a green cube, the musicgen model generates a music genre token such as soothing, guitar, rock, pop, and more. These tokens are collected in a prompt list that serves as the basis for music generation. For example, colliding with green cubes that generate tokens like soothing, guitar, and rock results in the prompt list [soothing, guitar, rock].

- **Cyan Cube Collisions**: Colliding with a cyan cube removes the last token from the prompt list. This interaction allows users to fine-tune their music prompt.

## Scoring System

MusiCube incorporates a scoring system to gamify the experience:

- Green cube collisions add points to the user's score, incentivizing interactions.
- Cyan cube collisions subtract points, encouraging strategic decisions.

## Music Generation and Playback

The accumulated prompt list is sent to the musicgen model after a series of collisions. The model then generates music based on the provided prompts. The resulting composition is played in a loop until a new prompt is constructed through further interactions.

## Example

Here's a sneak peek of the MusiCube experience:

![MusiCube Example](link_to_your_gif_or_screenshot.gif)

## Installation and Usage

To enjoy the MusiCube experience and even contribute to its development, follow these steps:

1. Set up a virtual environment using `python -m venv env` and activate it with `env\Scripts\activate` (Windows) or `source env/bin/activate` (Linux/MacOS).

2. Install the necessary packages from requirements.txt using `pip install -r requirements.txt`.

3. Launch the project by running the script with `python AudioCraft-3D-POC.py`.

Alternatively, for a hassle-free experience, you can directly download and run the executable file from [here].

## Licensing

MusiCube operates under the MIT License. For comprehensive licensing details, refer to the [LICENSE] file.

## Acknowledgments

We extend our gratitude to the following sources for their contributions and inspiration:

- The audiocraft library for providing the remarkable musicgen model capable of converting text prompts into musical compositions. Learn more about it [here](https://github.com/facebookresearch/audiocraft).

- The pygame library for equipping us with the tools to construct the immersive 3D interface and manage user input.

- The pyopengl library for furnishing the essential functions to render intricate 3D graphics seamlessly within the pygame framework.

Indulge in the captivating world of MusiCube, where music and interaction harmoniously blend, leading to a novel musical journey for all.
