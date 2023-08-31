from gradio_client import Client
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import requests

# The URL to the Gradio server
server_url = "https://47180b0fc10d536932.gradio.live"

# Check if the AudioCraft server is available
try:
    response = requests.get(server_url)
    if response.status_code == 200:
        # The server is available; proceed to create the client and predict
        client = Client(server_url)
        result = client.predict(fn_index=0)
        print("Prediction result:", result)
    else:
        print("Server is not available. Status Code:", response.status_code)
except requests.RequestException as e:
    print("An error occurred while checking the server:", e)


# Initialize Pygame and OpenGL
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("loop.wav")
pygame.mixer.music.play(loops=-1)
pong_sound = pygame.mixer.Sound("pong.wav")

display = (1920, 1080)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.RESIZABLE)
gluPerspective(30, (display[0] / display[1]), 1, 50.0)
glTranslatef(0.0, 0.0, -10)

# Apply tilt
tilt = 30
glPushMatrix()
glRotatef(tilt, 10, 0, 0)

# Global Variables
player_x = 0
player_y = -1.5
obstacles = []
collided_ids = set()
collision_count = 0
obstacle_id = 0

# Function to draw a cube
def draw_cube(x, y, z, size, color=(1, 1, 1)):
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
    glColor3f(*color)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw OpenGL text using bitmap rendering
def drawText(position, textString):
    font = pygame.font.Font(None, 64)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

# Function to detect collision between player and obstacle
def is_collision(player_x, player_y, player_z, obstacle_x, obstacle_y, obstacle_z, threshold=0.4):
    return abs(player_x - obstacle_x) < threshold and abs(player_y - obstacle_y) < threshold and abs(player_z - obstacle_z) < threshold

# def draw_text(text, x, y, color=(0, 0, 0)):
#    font = pygame.font.SysFont("Arial", 10)
#    text_surface = font.render(text, True, color)
#    text_rect = text_surface.get_rect()
#    text_rect.topright = (x, y)
#    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text)

# Main Function
def main():
    global player_x, player_y, obstacles, collision_count, obstacle_id
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= 0.1
        if keys[pygame.K_d]:
            player_x += 0.1
        if keys[pygame.K_w]:
            player_y += 0.1
        if keys[pygame.K_s]:
            player_y -= 0.1

        if random.choice([True, False]):
            obstacles.append([str(obstacle_id), random.uniform(-4, 4), -1.5, -30, 0.2, (0, 1, 0)])
            obstacle_id += 1  # Increment the obstacle ID

        new_obstacles = []
        for obs_id, x, y, z, s, color in obstacles:
            z += 0.1
            if z < 5:

                if is_collision(player_x, player_y, 0, x, y, z):
                    if obs_id not in collided_ids:
                        color = (0.5, 0.5, 0.5)  # Change color to grey upon collision
                        #pygame.mixer.music.play()
                        pong_sound.play()
                        collision_count += 1
                    collided_ids.add(obs_id)  # Add the collided obstacle ID to the set
                    # Draw the collision count
                    # draw_text("Collisions: " + str(collision_count), display[0] - 30, 10)
                new_obstacles.append([obs_id, x, y, z, s, color])  # Update with the new color

        obstacles = new_obstacles

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_cube(player_x, player_y, 0, 0.2, color=(1, 1, 1))  # Player cube is white

        # Draw Obstacles and their IDs
        for id, x, y, z, s, color in obstacles:
            draw_cube(x, y, z, s, color)
            drawText((x, y, z), str(id))  # Draw the obstacle ID

        # Update the display
        pygame.display.flip()
        clock.tick(30)

main()
