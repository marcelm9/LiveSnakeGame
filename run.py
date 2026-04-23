import argparse
from LiveSnakeGame.game import Game

parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="Name of the player")
args = parser.parse_args()

Game(args.name).run()
