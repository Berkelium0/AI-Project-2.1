# Repository for ws2324.2.1/team689

**Topic:** WS2324 Assignment 2.1: Compute Blood Types

### Libraries Used:

- pgmpy : a python library for working with Probabilistic Graphical Models. To install :
$ pip install pgmpy
- networkx : a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of 
complex networks. To install : $ pip install networkx
- matplotlib : a comprehensive library for creating static, animated, and interactive visualizations in Python. 
To install : $ pip install matplotlib

### How To Run:

In our project we should have 2 folders. One of them must have the problems we want to solve and the
other one for us to create solution json files into. 

'path_to_json' variable holds the name of the folder for problems and 'path_to_solution' variable holds
the name of the folder for solutions. The files should be created beforehand and their names should be 
assigned to those variables. When we run the script, solutions to every json problem in problems folder will
be created as a json file in the solution folder.

### How The Script Works:

The script takes every json file from the problems folder. It loops through all and calls the guess_blood
function for each. Every time it returns a result and then the script writes the results into a new json file
which will be stored in the solutions folder.

Inside the guess_blood function, first we create our network. We divided each person into two alleles X and Y.
So we have variables such as subX and subY for the subject and objX and objY for the object. We also created
a blood-type variable for both subject and object as subBT and objBT. While subBT is directly depended on subX and subY alleles,
objBT is depended on objX and objY alleles. Also, object's X is depended on the mother's alleles while object's Y is 
depended on the father's alleles. In case they don't have both parents, they get the allele probabilities of the country
allele probabilities for the missing parent. Then we added the state names and the values they can get. Since subX, subY, objX,
objY are alleles, they can get A, B or 0 while subBT and objBT can get A, B, AB or 0. According to this logic, we added the nodes and edges.


