import pygame
from pygame import MOUSEBUTTONDOWN

pygame.init()

# width and height of window
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

# text and button positions
text_x, text_y = 10, 10
button_x, button_y = 30, 80

# pygame.key.set_repeat(300, 30)
screen = pygame.display.set_mode((width//4, height//4))
screen.fill((255, 255, 255))

# set icon and window title
logo = pygame.image.load("Assets/Amitee_Logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Amitee")

# collision rectangle for button
rect = pygame.Rect(button_x, button_y, 412, 96)

# button image
loginBox = pygame.image.load("Assets/btn_google_sign-in.png")
screen.blit(loginBox, (button_x, button_y))

# buttonSurface = pygame.display.set_mode(())

# pygame.draw.rect(screen, (255,0,0), rect)

pygame.display.flip()

# #when left arrow is pressed, the red rect goes to the left

clock = pygame.time.Clock()
playing_game = True
while playing_game:
    clock.tick(45)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = False
            break
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 pygame.draw.rect(screen, (255,255,255), rect)
#                 pygame.display.update(rect)
#                 rect.move_ip((-5,0))
#                 pygame.draw.rect(screen, (255,0,0), rect)
#                 pygame.display.update(rect)
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Now it will have the coordinates of click point.
            if rect.collidepoint(mouse_pos):
                print('hi')

pygame.quit()
