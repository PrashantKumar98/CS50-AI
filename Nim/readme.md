This project demonstrate AI that teaches itself to play Nim through reinforcement learning
In the game Nim, we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses.

We’ll use Q-learning for this project.
In Q-learning, we try to learn a reward value (a number) for every (state, action) pair. An action that loses the game will have a reward of -1, an action that results in the other player losing the game will have a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.
The key formula for Q-learning is below. Every time we are in a state s and take an action a, we can update the Q-value Q(s, a) according to:
```
Q(s, a) <- Q(s, a) + alpha * (new value estimate - old value estimate)
```

Project functionality can be seen here :https://youtu.be/cBTxLnl3g0A
