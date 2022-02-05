import thorpy
#change the dictionary below to the dict of the input dictionary
calendar_list = {'main': 12984789372, 'utat': 120947908, 'canada holidays': 1092347820188}
calendar_length = len(calendar_list)
ans = set()
cal = []
for c in calendar_list:
    cal.append(c)

def main():
    title_element = thorpy.make_text("Chose calendar to use", 22, (0, 0, 0))
    elements = [title_element]
    if calendar_length >= 1:
        element1 = thorpy.make_button(cal[0], func=a)
        elements.append(element1)
    if calendar_length >= 2:
        element2 = thorpy.make_button(cal[1], func=b)
        elements.append(element2)
    if calendar_length >= 3:
        element3 = thorpy.make_button(cal[2], func=c)
        elements.append(element3)
    if calendar_length >= 4:
        element4 = thorpy.make_button(cal[3], func=d)
        elements.append(element4)
    if calendar_length >= 5:
        element5 = thorpy.make_button(cal[4], func=e)
        elements.append(element5)
    e_quit = thorpy.make_button("Done", func=done)
    e_quit.set_size((300, 100))
    elements.append(e_quit)
    sub_title = thorpy.make_text("You have selected" + str(ans), 15, (0, 0, 0))
    elements.append(sub_title)
    background = thorpy.Background(color=(200, 200, 200), elements=elements)
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()

def a():
    ans.add(cal[0])

def b():
    ans.add(cal[1])

def c():
    ans.add(cal[2])

def d():
    ans.add(cal[3])

def e():
    ans.add(cal[4])

def done():
    #the set of keys to the dictionary that is selected
    print(ans)
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
