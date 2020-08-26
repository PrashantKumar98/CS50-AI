In this code, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them
We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another (it’s true that a movie could take us to multiple different actors, but that’s okay for this problem). Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another.project’s functionality can be seen here [Link to Youtube!](https://youtu.be/5M9j_P31nt0) 