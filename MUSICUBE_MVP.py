import random
import requests
import pygame
import threading

from datetime import datetime
from gradio_client import Client
from itertools import cycle
from moviepy.editor import AudioFileClip

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Initialize the Gradio server
server_url = "https://facebook-musicgen--hg8nj.hf.space/"
MUSICUBE = "MUSICUBE"
print(f"Initializing...")

# Check if the server is available
try:
    response = requests.get(server_url)
    if response.status_code == 200:
        client = Client(server_url)
        print("Server is available: ", server_url)
        print("Loading MUSICUBE.")
    else:
        print("Server is not available. Status Code:", response.status_code)
except requests.RequestException as e:
    print("An error occurred while checking the server:", e)

# Initialize Pygame and OpenGL
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.mixer.music.load("loop.wav")
pygame.mixer.music.play(loops=-1)
pong_sound = pygame.mixer.Sound("pong.wav")  # Green Cube
ping_sound = pygame.mixer.Sound('ping.wav')  # Dark Green Cube
surf_sound = pygame.mixer.Sound('surf.wav')  # Cyan Cube
drop_sound = pygame.mixer.Sound('drop.wav')  # Smash Cube
oof_sound = pygame.mixer.Sound('oof.wav')  # Game Over
display = (1920, 1080)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.RESIZABLE)

# Function to load keywords from a file
def load_keywords_from_file(filename='keywords.txt'):
    keywords = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                # Remove quotation marks, split the line by commas, and strip whitespace
                cleaned_line = line.replace('"', '').replace("'", "")
                keywords.extend([word.strip() for word in cleaned_line.split(",")])
    return keywords

# Load the keywords from the file
musical_keywords = load_keywords_from_file()

# Initialize the cycle of musical keywords
keyword_cycle = cycle(musical_keywords)

# Initialize OpenGL
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Rotate the camera
tilt = 45
glPushMatrix()
glRotatef(tilt, 10, 0, 0)

# 3D Cube
global z, y, x

# Player Cube
global player_x, player_y, player_z, player_flashing
player_x = 0
player_y = -1.5
player_z = 0
player_flashing = False

# Obstacles
obstacles = []
collided_ids = set()
last_collisions = []  # To store the IDs of the last obstacle collisions

# Revised Reset Logic to keep special IDs intact
special_ids = {"Cyan", "Dark Green"}
collided_ids = collided_ids.intersection(special_ids)
# last_collisions = [id for id in last_collisions if id in special_ids]
collision_count = 0  # To store the total number of collisions
obstacle_id = 0  # To store the ID of the obstacle
score = 0  # Initialize the score
lives = 3  # Starting with 3 lives


# Function to draw a cube
def draw_cube(x, y, z, size, color=(1, 1, 1), player_flashing=False):
    vertices = [
        [size + x, -size + y, -size + z],
        [size + x, size + y, -size + z],
        [-size + x, size + y, -size + z],
        [-size + x, -size + y, -size + z],
        [size + x, -size + y, size + z],
        [size + x, size + y, size + z],
        [-size + x, size + y, size + z],
        [-size + x, -size + y, size + z]
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    glBegin(GL_LINES)
    if player_flashing:
        if random.randint(0, 9) == 0:
            glColor3f(1, 1, 1)
        else:
            if random.randint(0, 1) == 1:
                glColor3f(1, 1, 0)
            else:
                glColor3f(1, 0, 0)
    else:
        glColor3f(*color)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


# Function to draw OpenGL text using bitmap rendering
def drawText(position, textString, color=(255, 255, 255, 255)):
    font = pygame.font.Font(None, 64)
    textSurface = font.render(textString, True, color, (0, 0, 0, 128))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


# Function to detect collision between player and obstacle
def is_collision(player_x, player_y, player_z, obstacle_x, obstacle_y, obstacle_z, threshold=0.4):
    return abs(player_x - obstacle_x) < threshold and abs(player_y - obstacle_y) < threshold and abs(player_z - obstacle_z) < threshold

obs_speed = 0.1

# Function to send a prompt to the Gradio server
def send_prompt(prompt):
    global player_flashing
    player_flashing  = True
    MUSICGEN = f"{MUSICUBE}, {prompt}"
    print(f"Sending Prompt: {MUSICGEN}")
    client = Client(server_url)
    result = client.predict(MUSICGEN, "loop.wav", fn_index=0)
    print("MP4 Download:", result)
    track = datetime.now().strftime("%Y%m%d%H%M%S")
    bg_music = f"musicube-{track}.wav"
    AudioFileClip(result).write_audiofile(bg_music)
    pygame.mixer.music.load(bg_music)
    pygame.mixer.music.play(loops=-1)
    collided_ids.clear()
    player_flashing = False
    surf_sound.play()


# Function to send a prompt to the Gradio server asynchronously
def async_send_prompt(prompt):
    threading.Thread(target=send_prompt, args=(prompt,)).start()


# Main Function
def main():
    global player_x, player_y, player_z, obstacles, collision_count, obstacle_id, font
    global score, lives, collided_ids, last_collisions, player_flashing, obs_speed
    font = pygame.font.SysFont('Rajdhani-Bold', 24)
    clock = pygame.time.Clock()
    hud_text = "M U S I C U B E"
    flash_color = (1, 1, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Player Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 0.1 + (obs_speed / 6)
        if keys[pygame.K_RIGHT]:
            player_x += 0.1 + (obs_speed / 6)
        if keys[pygame.K_a]:
            player_x -= 0.1 + (obs_speed / 6)
        if keys[pygame.K_d]:
            player_x += 0.1 + (obs_speed / 6)
        if keys[pygame.K_UP]:
            player_z -= 0.1 + (obs_speed / 6)
        if keys[pygame.K_DOWN]:
            player_z += 0.1 + (obs_speed / 6)
        if keys[pygame.K_w]:
            player_z -= 0.1 + (obs_speed / 6)
        if keys[pygame.K_s]:
            player_z += 0.1 + (obs_speed / 6)
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if random.choice([True, True, False, False, False, False, False, False, False, False]):
            # Get the next musical keyword from the cycle
            keyword = next(keyword_cycle) if obstacle_id % 100 != 0 else "SURF!"

            color = (0, 1, 0)  # Green by default
            if obstacle_id % 100 == 0:  # Check if it's the 100th cube
                color = (0, 1, 1)  # Change to Cyan

            # Use 'keyword' instead of 'obstacle_id' as the ID for the cube
            if player_flashing:
                obstacles.append(['', random.uniform(-4, 4), -1.5, -30, 0.2, color])
            else:
                obstacles.append([keyword, random.uniform(-4, 4), -1.5, -30, 0.2, color])
            obstacle_id += 1  # Increment the obstacle ID

            # DARK CUBES
            obstacles.append([str(obstacle_id), random.uniform(-4, 4), -1.5, -30, 0.2, color])
            obstacle_id += 1  # Increment the obstacle ID

        new_obstacles = []
        for obs_id, x, y, z, s, color in obstacles:
            z += obs_speed

            if z < 5:

                # Check if the obstacle ID is a numerical value
                if obs_id.isdigit():
                    obs_id = ""
                    color = (0, 0.42, 0)  # Change to DARK GREEN

                if is_collision(player_x, player_y, player_z, x, y, z):
                    if player_flashing:
                        # "Destroy" the obstacle and play the special sound
                        obs_id = ""
                        drop_sound.play()
                        color = (0, 0, 0)  # Change color to black
                        score += 100  # Add 100 points
                else:
                    # Existing collision logic here...
                    pass  # This is a placeholder. Replace with your actual code.

                if is_collision(player_x, player_y, player_z, x, y, z):
                    if color == (0, 0.42, 0):  # Assuming dark green is represented this way
                        print("Oof ...")
                        if lives == 0:
                            # Play the different sound
                            oof_sound.play()
                            print("End Score: ", score)
                            # Pause Game
                            pygame.mixer.music.pause()
                            # restart the game after nine second timer that refills lives
                            pygame.time.wait(9000)
                            # Reset the game
                            pygame.mixer.music.unpause()
                            lives = 3
                            score = 0
                            collision_count = 0
                            obstacles = []
                            collided_ids = set()
                            collided_ids.clear()
                            last_collisions = []
                            obstacle_id = 0
                            player_x = 0
                            player_y = -1.5
                            player_z = 0
                            pygame.mixer.music.load("loop.wav")
                            pygame.mixer.music.play(loops=-1)
                            # Reset the HUD text
                            hud_text = "PRESS START"
                            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                if is_collision(player_x, player_y, player_z, x, y, z):


                    if obs_id not in collided_ids:
                        # Check if the color of the obstacle is red
                        if color == (0, 0.42, 0):
                            # Play the different sound
                            ping_sound.play()
                            lives -= 1
                            # Clear the prompt list
                            last_collisions.clear()
                            print("You hit a dark green cube!")
                            collided_ids.clear()
                        # Check if the color of the obstacle is cyan
                        if color == (0, 1, 1):
                            # Play the different sound
                            surf_sound.play()
                            async_send_prompt(last_collisions)
                            obs_speed += 0.1
                            # Add 1000 points for each keyword in the list
                            score += len(last_collisions) * 1000
                            # Clear the prompt list
                            last_collisions.clear()
                            print("You hit a cyan cube!")
                            collided_ids.clear()
                        else:
                            # Play the regular sound
                            pong_sound.play()
                            color = (0.5, 0.5, 0.5)  # Change color to grey upon collision
                            score += 10
                            collision_count += 1

                        # Update the list of last collision IDs
                        if obs_id != "SURF!":
                            if obs_id != "  ":
                                print("You collected:", obs_id)
                                last_collisions.append(obs_id)
                        if len(last_collisions) > 8:
                            last_collisions.pop(0)

                    collided_ids.add(obs_id)  # Add the collided obstacle ID to the set

                new_obstacles.append([obs_id, x, y, z, s, color])  # Update with the new color

        obstacles = new_obstacles


        if player_flashing:
            if color != (1,0,0):
                if random.randint(0, 1) == 0:  # 10% chance to clear the screen
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                else:
                    if random.randint(0, 9) == 0:
                        flash_color = (0.42, 0.42, 0.42)
                    else:
                        if random.randint(0, 1) == 1:
                            flash_color = (1, 1, 0)
                        else:
                            flash_color = (1, 0, 0)
            draw_cube(player_x, player_y, player_z, 0.2, color=(flash_color))
        else:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw_cube(player_x, player_y, player_z, 0.2, color=(1, 1, 1))  # Player cube is white



        # Draw Obstacles and their IDs
        for id, x, y, z, s, color in obstacles:
            draw_cube(x, y, z, s, color)
            drawText((x-.2, y, z), str(id), color=(0, 255, 0, 255))  # Draw the obstacle ID

        drawText((-2.35, 1.8, 0), f'Score: {score}', color=(255, 255, 255, 255))
        drawText((-4.5, -3, 0), f'{hud_text}', color=(255, 255, 255, 255))
        drawText((2.2, 1.8, 0), f'{lives}', color=(255, 255, 255, 255))

        # Update the display
        pygame.display.flip()

        # Switch to 2D rendering for score display
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, display[0], display[1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw the 2D text for score
        screen = pygame.display.get_surface()  # Get the current screen surface
        text_surface = font.render(f'SCORE: {collision_count}', True, (255, 255, 255))
        screen.blit(text_surface, (display[0] - 100, 10))

        # Display the last collision IDs on the HUD
        prompt = f"{' '.join(map(str, last_collisions))}"
        hud_text = f"{prompt}"
        screen.blit(text_surface, (display[0] - 100, 10))

        # Switch back to 3D rendering
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        clock.tick(15)


main()
# EOF
