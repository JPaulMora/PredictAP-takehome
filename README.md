# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Instructions

Fork this repository and implement the above requirements. The result must be an application that implements both the index and search features. Use your best judgement as to the interface that is used to use the index and search features, but remember that this is meant to create a dialog during the interview process, not be something that would be used in production.

Feel free to use the language, libraries, and tools that you are most comfortable in and best reflect your ability to translate requirements into a functional implementation.

Once the project is implemented, remove the `# Instructions` section of this readme and add the section `# Usage` with instructions on how to run the produced application.

The `test_data` directory in this project contains files and directories that can be used to test your implementation.

Good luck.


# Documentation

## Requirements

* The files that are to be indexed are of varying sizes, types and with different filenames. There could also be subfolders of unlimited depth.
* There must be file to store the indexed data.

## Preliminary assumptions

* Indexing the files should be easy for the user.
* Ideally, the indexing process should be quick.
* We can assume there could be 10 or 10 million files indexed, so most importantly searching should be fast.
* The interface should be graphical and not console-based so it's user friendly.
* Implementation should be fast as this is just a test.

## Design and architecture

Based on the previous section, the following design choices were made.

* A database is required, and must be quick to implement, therefore we'll be using SQLite.
* Python is the team's (me) main language so this should be the most efficient language to use.
* For the user interface, something web based could be implemented, or a templating/scaffolding framework such as EasyQT could be used.
* The file indexing process will be made sequentially at first, once it's working further optimizations could be made.