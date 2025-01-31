# Interpreter Project for Compilation Theory

### About the project:

The aim of the project was constructing a language offering binary operations on numeric data types, booleans, strings and matrices, in addition to printing, if-else statements and loops. The syntax is a little reminiscent of a mix between Python and C, with Python-like dynamic typing and C-like semi colons and if/loop syntax.

The language also handles errors such as attempting to perform operations for data of types for which the operator has not been overloaded (e.g. adding string to a matrix of floats).

The whole interpreter was written in Python, with use of the sly and numpy libraries. The files written in the created language are of type .m.


### Contents of the folders:

[Lab1](Lab1) - scanner
[Lab2](Lab2) - parser
[Lab3](Lab3) - tree printer
[Lab4](Lab4) - type checker
[Lab5](Lab5) - interpreter

Caution: a scanner (and also parser and so on) from one directory may not be the same as a scanner from another and so swapping them may lead to unexpected behaviour. The finished project resides within Lab5 directory, containing an interpreter and all other neccessary files.

### Running the project:

If you happen not to have sly and numpy already installed, run the following command in the terminal:

`pip install numpy sly`

Upon doing that from within the selected directory run:

`python ./main.py <relative .m file path>`

