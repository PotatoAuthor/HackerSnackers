import thorpy
calendar_list = {'main': 12984789372, 'utat': 120947908, 'canada holidays': 1092347820188}
ans = set()
cal = []
for c in calendar_list:
    cal.append(c)

def main():
    title_element = thorpy.make_text("Chose calendar to use", 22, (0, 0, 0))
    elements = [title_element]
    element1 = thorpy.make_button(cal[0], func=a)
    elements.append(element1)
    element2 = thorpy.make_button(cal[1], func=b)
    elements.append(element2)
    element3 = thorpy.make_button(cal[2], func=c)
    elements.append(element3)
    e_quit = thorpy.make_button("Done", func=done)
    e_quit.set_size((300, 100))
    elements.append(e_quit)
    background = thorpy.Background(color=(200, 200, 200), elements=elements)
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()

def a():
    ans.add(cal[0])
    print('a')

def b():
    ans.add(cal[1])

def c():
    ans.add(cal[2])

def done():
    print(ans)
    thorpy.functions.quit_menu_func()
    thorpy.functions.quit_menu_func()


application = thorpy.Application(size=(1000, 800), caption="Amitee")


e_title = thorpy.make_text("Amitee", font_size=40, font_color=(10, 10, 10))
e_title.center()
e_title.set_topleft((None, 20))

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
