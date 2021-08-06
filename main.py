from gra import Gra

g = Gra()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()