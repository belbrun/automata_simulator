
---Automaton simulator---

Uses a definition to create an automaton and an input sequence to simulate the behaviour of the defined automaton.
Prints out a console line output that describes events happening during the simulation.


Pushdown automaton:

run with: python simulator.py -dpda -test_num 1
(while positioned in the root directory of this project)

- there are 25 test cases that can be run seperately of as a group

- to run a test case use: python simulator.py -dpda -test X,
	where X is the number of the test case you want to run

- to run all test cases use : python simulator -dpda --all 

Epsilon NF automaton

run with: python simulator.py -enfa -test_num 1

- there are 24 test cases that can be run seperately or as a group

- to run a test case use: python simulator.py -enfa -test X,
	where X is the number of the test case you want to run

- to run all test cases use : python simulator -enfa --all 
