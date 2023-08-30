const pygame = require("pygame");
const math = require("mathjs");

// Initialize Pygame and OpenGL
pygame.init();
pygame.mixer.init(); // Initialize the mixer module for sound
const display = [1920, 1080];
pygame.display.set_mode(display, [pygame.DOUBLEBUF, pygame.OPENGL, pygame.RESIZABLE]);
pygame.glu.gluPerspective(30, (display[0] / display[1]), 1, 50.0);
pygame.gl.glTranslatef(0.0, 0.0, -10);

// Apply tilt
const tilt = 30;
pygame.gl.glPushMatrix();
pygame.gl.glRotatef(tilt, 10, 0, 0);
// pygame.gl.glPopMatrix();

// Global Variables
let player_x = 0;
let player_y = -1.5;
const obstacles = [];
const collided_ids = new Set();
let collision_count = 0;
let obstacle_id = 0;

// Function to draw a cube
function draw_cube(x, y, z, size, color = [1, 1, 1]) {
  const vertices = [
    [size + x, -size + y, -size + z],
    [size + x, size + y, -size + z],
    [-size + x, size + y, -size + z],
    [-size + x, -size + y, -size + z],
    [size + x, -size + y, size + z],
    [size + x, size + y, size + z],
    [-size + x, size + y, size + z],
    [-size + x, -size + y, size + z]
  ];
  const edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
  ];
  pygame.gl.glBegin(pygame.GL_LINES);
  pygame.gl.glColor3f(color[0], color[1], color[2]);
  for (const edge of edges) {
    for (const vertex of edge) {
      pygame.gl.glVertex3fv(vertices[vertex]);
    }
  }
  pygame.gl.glEnd();
}

// Function to detect collision between player and obstacle
function is_collision(player_x, player_y, player_z, obstacle_x, obstacle_y, obstacle_z, threshold = 0.4) {
  return math.abs(player_x - obstacle_x) < threshold && math.abs(player_y - obstacle_y) < threshold && math.abs(player_z - obstacle_z) < threshold;
}

function draw_text(text, x, y, color = [0, 0, 0]) {
  const font = pygame.font.SysFont("Arial", 12);
  const text_surface = font.render(text, true, color);
  const text_rect = text_surface.get_rect();
  text_rect.topright = [x, y];
  // pygame.display.get_active().blit(text_surface, text_rect)
}

// Main Function
function main() {
  global player_x, player_y, obstacles, collision_count, obstacle_id;
  const clock = pygame.time.Clock();
  while (true) {
    for (const event of pygame.event.get()) {
      if (event.type === pygame.QUIT) {
        pygame.quit();
        process.exit();
      }
    }

    const keys = pygame.key.get_pressed();
    if (keys[pygame.K_a]) {
      player_x -= 0.1;
    }
    if (keys[pygame.K_d]) {
      player_x += 0.1;
    }
    if (keys[pygame.K_w]) {
      player_y += 0.1;
    }
    if (keys[pygame.K_s]) {
      player_y -= 0.1;
    }

    if (Math.random() > 0.5) {
      obstacles.push([obstacle_id, Math.random() * 4 - 2, -1.5, -30, 0.2, [0, 1, 0]]);
      obstacle_id += 1; // Increment the obstacle ID
    }

    const new_obstacles = [];
    for (const [obs_id, x, y, z, s, color] of obstacles) {
      z += 0.1;
      if (z < 5) {

        if (is_collision(player_x, player_y, 0, x, y, z)) {
          if (obs_id not in collided_ids) {
            color = [0.5, 0.5, 0.5]; // Change color to grey upon collision
            pygame.mixer.music.play();
            collision_count += 1;
          }
          collided_ids.add(obs_id); // Add the collided obstacle ID to the set
          // Draw the collision count
          draw_text("Collisions: " + collision_count, display[0] - 30, 10);
        }
        new_obstacles.push([obs_id, x, y, z, s, color]); // Update with the new color
      }
    }
    obstacles = new_obstacles;

    pygame.gl.glClear(pygame.GL_COLOR_BUFFER_BIT | pygame.GL_DEPTH_BUFFER_BIT);
    draw_cube(player_x, player_y, 0, 0.2, [1, 1, 1]); // Player cube is white

    // Draw Obstacles and their IDs
    for (const [id, x, y, z, s, color] of obstacles) {
      draw_cube(x, y, z, s, color);
    }

    // Update the display
    pygame.display.flip();
    clock.tick(30);
  }
}

main();
