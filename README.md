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
(Precompute)
- compute next second's kill zones (3D BFS)
- and also zones if a bomb is placed this turn (duplicate state, 3D BFS)
- or our bombs are accelerated (duplicate state, 3D BFS)
- also check which moves are legal (not hitting indesctructible wall, have to have bomb for accelerate, simple checks)

SURVIVE
- Escape blast (mark moves that will cause death)
- If all moves will cause death, undo mark moves; then if dying in next turn, place bomb

KILL
- If has bomb and placing bomb will kill enemy, do so
- If accelerating will cause enemy to get caught in blast, do so

GET_POWERUP
- Try to get powerup, if present. Plan route through destructible walls, but increasing cost by 3x.
- If has bomb and wall is blocking, place bomb. Else mark as waiting for bomb.

STAY_SAFE
- Escape blast radius even if it is still safe, just in case the enemy accelerates the timer.

TRACK
- Home in to nearest undestroyed wall or enemy
- If near wall and has bomb, place bomb. Else mark for waiting for bomb.

WAITING
- If no immediate action is needed and still waiting for bomb, accelerate

ANY
- Do any available action left, starting from moves, up to staying still if there's really nothing else
```
