# xxi Bomberman Bot

[Bomberman]("https://github.com/EntelectChallenge/2016-Bomberman") game bot using greedy algorithm, written in Python 2. Created by Jonathan Christopher (13515001), Turfa Auliarachman (13515133) and Jordhy Fernando (13515004) for IF2250 Strategi Algoritma (Algorithms) class.

## How to run

1. Download the [Bomberman game engine]("https://github.com/EntelectChallenge/2016-Bomberman") from its Github repository. Version 1.2.6 is recommended.

2. Extract the `Game Engine` folder and place in in this directory's parent directory.

3. To run a match between bots, use `run-bvb.bat` or `<path to Bomberman.exe> --pretty --debug -b "<Path to bot 1>" "<Path to bot 2>" "<Path to bot 3>" "<Path to bot 4>"`.

4. To run a human-vs-bot match, use `run-pvb.bat` or `<path to Bomberman.exe> --pretty -c 1 -b "<Path to bot>"`.

## Strategy

For each round, the bot will try to execute the following goals, starting from the highest priority to the lowest:

```
Calculate danger, blast and target zones.

If in danger zone, try find a path to nearest safe location.
If not possible (trapped), place bomb, then trigger our bombs.

If an enemy player is in the target zone, trigger our bombs.

If placing a bomb will trap enemy, place bomb.

If next to a destructible wall, place bomb.

Try to find a path to nearest accessible power up.

Try to find a path to the nearest destructible wall.
If there's none, try to find a path to nearest enemy instead.

Else do nothing.
```
