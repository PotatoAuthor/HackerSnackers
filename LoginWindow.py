import pygame
from pygame import MOUSEBUTTONDOWN
import LoginActivity


def main():
    """Main function of the Amitee program. Creates a window that prompts users to login"""
    pygame.init()

    # width and height of window
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # button positions
    button_x, button_y = 30, 80

    # pygame.key.set_repeat(300, 30)
    screen = pygame.display.set_mode((width // 4, height // 4))
    screen.fill((255, 255, 255))

    # set icon and window title
    logo = pygame.image.load("Assets/Amitee_Logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Amitee")

    # collision rectangle for button
    rect = pygame.Rect(button_x, button_y, 412, 96)

    # button image
    login_box = pygame.image.load("Assets/btn_google_sign-in.png")
    screen.blit(login_box, (button_x, button_y))

    pygame.display.flip()

    clock = pygame.time.Clock()
    playing_game = True
    while playing_game:
        clock.tick(45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                playing_game = False
                break
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rect.collidepoint(mouse_pos):
                    LoginActivity.get_oauth2_token()
                    pygame.quit()
                    playing_game = False
                    break


if __name__ == '__main__':
    main()
