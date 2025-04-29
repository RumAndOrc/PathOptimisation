
# Path Optimisation

## MapMaker

This will be a node editor to represent junctions on a map 

### Key features:
* Distances between nodes will be to scale
* Lines will be colour coded (these will be changeable in the settings later)
  * Black for distance is to-scale
  * Red for some hindrance making the path more difficult than the default distance
  * Blue for an easier than default distance
* Distances will be rounded to integers for simplicity

### Usage
* Middle mouse button to create a new node, or delete an existing one
* left click and drag to
  * create a leg between two nodes, or
  * move a node
* right click to clear the legs from a node


## Optimiser

Initially this will implement Dijkstra's algorithm, but I have some ideas to modify it. Given that this project is mainly for learning git and for the love of coding I will probably end up at some other well known algorithm without realising. Fun either way. 
