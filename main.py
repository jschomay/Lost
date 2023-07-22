from game import Game

game = Game()

while True:
    game.init()
    game.run()
    game.clean_up()

game.quit()
quit()
