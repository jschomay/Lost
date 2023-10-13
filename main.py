from game import Game

game = Game()

while game.play_again:
    game.init()
    game.run()
    game.clean_up()

game.quit()
quit()
