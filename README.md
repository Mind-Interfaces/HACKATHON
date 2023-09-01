# MusiCube: Interactive Pygame Music Generator

MusiCube is an innovative pygame project that utilizes the powerful musicgen model from the audiocraft library to create unique musical compositions based on user interactions within a captivating 3D environment. This project offers an engaging musical experience where users can actively participate in the music generation process.

## Project Overview

The core of MusiCube lies in its ability to generate music by analyzing the user's interactions with a dynamic 3D interface. The interface consists of various cubes, each serving a distinct purpose:

- **Controller Cube (White)**: This cube serves as the user's avatar within the 3D space. Users can navigate it using the arrow keys.

- **Collision Cubes (Green and Cyan)**: The environment is adorned with green and cyan cubes. Colliding with these cubes triggers different musical effects.


## About Musicube

🎶 Musicube: Where Creativity and Music Converge! 🎮🎵 Embark on a journey beyond traditional gaming with Musicube, an innovative 3D cube-based game that redefines the boundaries of creativity and music production. Designed to captivate both gaming enthusiasts and music aficionados, Musicube offers an unparalleled experience where players don't just play the game, but actively participate in crafting unique musical compositions.

🚀 Real-time Music Generation 🎶💡 What sets Musicube apart is its seamless integration of gaming and music generation. The instant you intersect cubes, your commands are sent to our cutting-edge MusicGen engine. This AI-powered technology transforms your actions into real-time musical output, providing an enchanting auditory experience that mirrors your gaming journey. Witness the magic unfold as your gameplay shapes the very music that accompanies it.

🌈 Limitless Exploration and Discovery 🔍🎮 Step into a universe where creativity knows no bounds. With a multitude of cube types, each representing distinct musical elements, Musicube encourages you to explore, experiment, and uncover hidden synergies. Delve into the world of harmonics, percussion, melodies, and more. Whether you're creating serene soundscapes or energetic compositions, every moment in Musicube is an opportunity to push the boundaries of your artistic expression.

🎉 Experience Musicube Today! 🌍🎮 Are you ready to embark on an unforgettable journey where your gaming skills fuel your musical prowess? Musicube invites you to explore, play, and compose your way to a symphonic adventure like no other. Elevate your gaming experience, unlock your inner composer, and witness the harmony of Musicube – where the cubes dance to your gaming, and the music sings to your soul.
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


## Demo

Experience MusiCube in action! Watch our demo video [here](https://www.youtube.com/watch?v=NUnyDEqjWBg).
## Installation and Usage

To enjoy the MusiCube experience and even contribute to its development, follow these steps:

1. Clone the repository using `git clone https://github.com/Mind-Interfaces/HACKATHON.git` or download the project source code.

Set up a virtual environment using `python -m venv env` and activate it with `env\Scripts\activate` (Windows) or `source env/bin/activate` (Linux/MacOS).

2. Install the necessary packages from requirements.txt using `pip install -r requirements.txt`.

3. Launch the project by running the script with `python AudioCraft-3D-POC.py`.

Alternatively, for a hassle-free experience, you can directly download and run the executable file from [here](LINK_TO_EXECUTABLE).

## Licensing

MusiCube operates under the MIT License. For comprehensive licensing details, refer to the [LICENSE](LINK_TO_LICENSE) file.

## Acknowledgments

We extend our gratitude to the following sources for their contributions and inspiration:

- The audiocraft library for providing the remarkable musicgen model capable of converting text prompts into musical compositions. Learn more about it [here](https://github.com/facebookresearch/audiocraft).

- The pygame library for equipping us with the tools to construct the immersive 3D interface and manage user input.

- The pyopengl library for furnishing the essential functions to render intricate 3D graphics seamlessly within the pygame framework.

Indulge in the captivating world of MusiCube, where music and interaction harmoniously blend, leading to a novel musical journey for all.


## Technical Details

Details about the technical implementation, algorithms, and design choices can be added here.
## Team Members

- ![MIND](PROFILE_IMAGE_LINK) **MIND INTERFACES**: Life Science Research (AI)
- ![KP](PROFILE_IMAGE_LINK) **KP Kshitij Parashar**: Technical Product Manager
- ![Joseph](PROFILE_IMAGE_LINK) **Joseph Pollack**: CIO
- ![Muhammad Umar](PROFILE_IMAGE_LINK) **Muhammad Umar Nawaz**: Full stack developer
