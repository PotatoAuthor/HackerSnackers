import thorpy

def main():
    application = thorpy.Application((1000, 800), "Chose calendar")
    element = thorpy.Checker("Checker")
    title_element = thorpy.make_text("Chose calendar to use", 22, (0, 0, 0))
    background = thorpy.Background(color=(200, 200, 200), elements=[title_element, element])
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()
    application.quit()



application = thorpy.Application(size=(1000, 800), caption="Amitee")


e_title = thorpy.make_text("Amitee", font_size=40, font_color=(10, 10, 10))
e_title.center() #center the title on the screen
e_title.set_topleft((None, 20)) #set the y-coord at 10

e_subtitle = thorpy.make_text("Restoration of Friendship", font_size=15, font_color=(10, 10, 10))
e_subtitle.move((400, 80))


e_options = thorpy.make_button('start', func=main)
e_options.set_size((300, 100))

e_quit = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)
e_quit.set_size((300, 100))



e_background = thorpy.Background(color=(170, 170, 170),
                                 elements=[e_title, e_subtitle, e_options, e_quit])
thorpy.store(e_background, [e_options, e_quit])

menu = thorpy.Menu(e_background)
menu.play()

application.quit()