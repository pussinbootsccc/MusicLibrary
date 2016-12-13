# MusicLibrary

## How to Run

The codes can be executed in two modes:

To enter the interactive command line interface, run
```
python MusicLibrary.py
```

To test the program using an external file of user commands, run
```
python MusicLibrary.py sample_in.txt
```

## Answers to Questions

1. How have you gained confidence in your code?

The program has been tested using the external files of simulated user commands. In addition, all the functionalities in the program has been unit-tested throughout the implementation. Special attention has been paid to address possible errors, including invalid user commands and logic faults.

2. One of the things we'll be evaluating is how your code is organized. Why did you choose the structure that you did? What principles were important to you as you organized this code?

The program is organized in a hierarchical structure, where we have 4 entities with descending granularity: the library, artists, albums, and tracks, with their relations indexed by hash tables. Such a hierarchical design pattern offers us a separation of concern at different levels, hence helps us to focus on implementing key attributes/functionalities of each entity type within its own domain. We also tried to make the code as modularized as possible. To give a concrete example, the action of adding a new track to the library is realized by calling the submodule of adding a new track to the album of the corresponding artist.

3. What are the performance characteristics of your implementation? Does it perform some operations faster than others? Explain any tradeoffs you made in architecting your solution.

The program is designed to be efficient in terms of handling large number of input.

i) We use hash tables to enable fast O(1) access to the artist/album/track based on their relationship mappings.

ii) We use min heap to allow fast response with respect to rank queries (finding Top N tracks/artists). The heap scales at O(Mlog(N)) where M is the total number of entities, while a naive sorting algorithm will be O(Mlog(M)) where M >> N. Meanwhile, we are aware that there are other data structures which can scale at O(Nlog(M)), such as the Order-statistic Tree or the Skip List. However, those data structures can be more expensive to update and we therefore choose to stay with our current design in favor of its relative simplicity.

iii) As a further enhancement, a cache has been implemented on top of the min-heap, allowing O(1) retrieval for the rank-statistics in many cases. The intuition is that rank queries can be highly repetitive, and queries for the top K' items can be subsumed by queries for top K items when K'<=K. The presence of the cache should lead to substantial speed improvement in expectation.

## Other Features

1. I wrote code to format the output of the program as pretty-looking tables. 

2. Help instructions can be accessed by typing `help`, or when an invalid input is encountered.

