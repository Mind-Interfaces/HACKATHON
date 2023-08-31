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
level_name = "Minimal Loop"
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
ping_sound = pygame.mixer.Sound('pong.wav')
display = (1920, 1080)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.RESIZABLE)

# Initialize OpenGL
#gluPerspective(30, (display[0] / display[1]), 1, 50.0)
#glTranslatef(0.0, 0.0, -10)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Apply tilt
tilt = 45
glPushMatrix()
glRotatef(tilt, 10, 0, 0)

player_x = 0
player_y = -1.5
player_z = 0
obstacles = []

collided_ids = set()
last_collisions =[]  # To store the IDs of the last bstacle collisions
collision_count = 0 # To store the total number of collisions
obstacle_id = 0  # To store the ID of the obstacle

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

# Send Prompt to API OMG WE NEED HELP HERE <<UNDER CONSTRUCTION>>
def send_prompt(prompt):
        result = client.predict(
            	True,	# bool in 'Enable' Checkbox component
				128,	# int | float in 'BPM' Number component
                "A",	# str (Option from: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']) in 'Key' Dropdown component
				"Minor",	# str (Option from: ['Major', 'Minor']) in 'Scale' Dropdown component
				level_name,	# str in 'Global Prompt' Textbox component
				prompt,	# str in 'Input Text' Textbox component
				1337,	# int | float in 'Seed' Number component
				fn_index=14
        )

        return result

# TURN THE RETURNED DATA INTO A WAV AND LOAD IT INTO PYGAME
def load_wav(data):
     pygame.mixer.music.load(data)
     pygame.mixer.music.play(loops=-1)

# Loop conductor to send prompt and load wav
def loop_conductor():
    while True:
        prompt = last_collisions
        result = send_prompt(prompt)
        load_wav(result)

# Main Function
def main():
    global player_x, player_y, player_z, obstacles, collision_count, obstacle_id
    clock = pygame.time.Clock()
    # hud_text= set("A","U","D","I","O","S","U","R","F","3D")
    hud_text = ("A U D I O S U R F 3D")
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
        if keys[pygame.K_UP]:
            player_y += 0.1
        if keys[pygame.K_DOWN]:
            player_y -= 0.1
        if keys[pygame.K_w]:
            player_z -= 0.1
        if keys[pygame.K_s]:
            player_z += 0.1
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if random.choice([True, False, False, False]):
            color = (0, 1, 0)  # Green by default
            if obstacle_id % 100 == 0:  # Check if it's the 100th cube
                color = (0, 1, 1)  # Change to Cyan
            obstacles.append([str(obstacle_id), random.uniform(-4, 4), -1.5, -30, 0.2, color])
            obstacle_id += 1  # Increment the obstacle ID

        new_obstacles = []
        for obs_id, x, y, z, s, color in obstacles:
            z += 0.1
            if z < 5:

                if is_collision(player_x, player_y, player_z, x, y, z):
                    if obs_id not in collided_ids:
                        color = (0.5, 0.5, 0.5)  # Change color to grey upon collision

                        # Check if the color of the obstacle is cyan
                        if color == (0, 1, 1):
                            # Play the different sound
                            ping_sound.play()
                        else:
                            # Play the regular sound
                            pong_sound.play()

                        collision_count += 1
                        # Update the list of last collision IDs
                        last_collisions.append(obs_id)
                        if len(last_collisions) > 8:
                            last_collisions.pop(0)
                    collided_ids.add(obs_id)  # Add the collided obstacle ID to the set
                new_obstacles.append([obs_id, x, y, z, s, color])  # Update with the new color



        obstacles = new_obstacles

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_cube(player_x, player_y, player_z, 0.2, color=(1, 1, 1))  # Player cube is white

        # Draw Obstacles and their IDs
        for id, x, y, z, s, color in obstacles:
            draw_cube(x, y, z, s, color)
            drawText((x, y, z), str(id))  # Draw the obstacle ID

        drawText((-2, 1.5, 0), f'Score: {collision_count}')
        drawText((-3, -3, 0), f'{hud_text}')

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
        font = pygame.font.Font("Hack-Regular.ttf", 24)
        text_surface = font.render(f'SCORE: {collision_count}', True, (255, 255, 255))
        screen.blit(text_surface, (display[0] - 100, 10))
        # Display the last collision IDs on the HUD
        prompt = f"{' '.join(map(str, last_collisions))}"
        hud_text = f"PROMPT: {prompt}"
        screen.blit(text_surface, (display[0] - 100, 10))

        # Add code here to render the HUD text

        # Switch back to 3D rendering
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        clock.tick(30)

main()
