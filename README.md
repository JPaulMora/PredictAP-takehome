# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Usage

To run this application you need to have python installed, the recommended way to install it is to create a virtual environment. Within your preferred environment you must install the dependencies and run the project. Below are specific instructions on how to do this.

```bash
python -m venv venv # Create a virtual environment
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install requirements
python indexer-pygui.py # run the program
```

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

## Further expansion

* To scale this project, consider converting it to a web based project. Web servers are designed to handle multiple concurrent requests and users.
* The limiting factor for performance is the selected indexing backend, SQLite will beat `fopen` but it will be slow at scale compared to MySQL or PostgreSQL.
* The scaling answer _might not_ be SQL at all. There are many different indexing and searching backends such as Solr and Elasticsearch which will have better full text search implementations among other scaling benefits.