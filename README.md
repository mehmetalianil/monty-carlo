# Monty Carlo

***RIGHT NOW THE CODE IS FAR FROM BEING USABLE.
IN THIS STAGE, IT IS STILL IN THE BRAINSTORMING PHASE, WITH MANY CLASSES AND FUNCTIONS SCATTERED AROUND.***

Monty Carlo is a modular Monte Carlo engine, suitable for statistical systems. The subgroup of all  Monte Carlo algorithms that Monty Carlo will be affiliated with will be the ones that have the structure of a energy minimizing (or fitness maximizing) randomized repetitive process.

In a clearer context, Monty Carlo will need,

* a definition of the “state” that is in question.
* an initial state, in the type of the state that was presented.
* a set of parameters that are defined with reference to the objects of the state
* an energy (or fitness) definition in which the randomized process depends on
* an operation to the system if the random process returns active

as an addition to this chronological list of inputs, the algorithm may be customized with,

* the nature of the random number generator.
* a set of widely used systems, and a library built upon the definitions needed for those systems.
 * 2D and 3D Ising spin systems
 * 3D crystal spin systems
 * gaseous systems

![Lattice Initialization](https://github.com/monty-carlo/monty-carlo/blob/master/src/atomic/ex_atomic_lattice_fig.png?raw=true)


Monty Carlo gets the initial state as an input, then starts a randomized process. It takes a predefined change in the system, and calculates the energy difference for that change to occur for that condition. Then, it takes a random number, and checks the qualification criterion. If the process qualifies, this process is executed. Then it takes the next change, until all units of the state has undergone the same process. 
