import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotation of a Point")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Function to rotate a point (px, py) around a center point (cx, cy) by angle theta
def rotate_point(px, py, cx, cy, theta):
    # Convert angle to radians
    theta = math.radians(theta)
    
    # Translate the point to the origin
    px_translated = px - cx
    py_translated = py - cy
    
    # Apply rotation using the 2D rotation matrix
    px_rot = px_translated * math.cos(theta) - py_translated * math.sin(theta)
    py_rot = px_translated * math.sin(theta) + py_translated * math.cos(theta)
    
    # Translate the point back
    px_rot += cx
    py_rot += cy
    
    return px_rot, py_rot

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    
    # Define the original point and center of rotation
    px, py = 300, 200  # Point to rotate
    cx, cy = 300, 300  # Center of rotation
    angle = 0  # Initial angle
    
    while running:
        screen.fill(WHITE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Rotate the point by `angle` degrees
        px_rot, py_rot = rotate_point(px, py, cx, cy, angle)
        
        # Draw the center of rotation (red)
        pygame.draw.circle(screen, RED, (int(cx), int(cy)), 5)
        
        # Draw the original point (blue)
        pygame.draw.circle(screen, BLUE, (int(px), int(py)), 5)
        
        # Draw the rotated point (green)
        pygame.draw.circle(screen, GREEN, (int(px_rot), int(py_rot)), 5)
        
        # Draw lines from center to the points
        pygame.draw.line(screen, BLUE, (cx, cy), (px, py), 2)
        pygame.draw.line(screen, GREEN, (cx, cy), (px_rot, py_rot), 2)
        
        # Increase the angle for the next frame
        angle += 1
        if angle >= 360:
            angle = 0  # Reset angle after a full rotation
        
        # Update the screen
        pygame.display.flip()
        
        # Control the frame rate
        clock.tick(60)

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
