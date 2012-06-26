# What is wson-sim

`wson-sim` is a simple event driven simulator for studying the impact of interference in Wavelength Switched Optical Networks. The simulator is written in Python. The code is straightforward and can be easily adapated for any kind of simulation targeting a WSON.

For more information about the experiment take a look at the `docs` directory. 

# Requirements

We strongly suggest to use PyPy for launching the simulations, due to its tracing JIT. On the other hand for running extracting graphs you have to use Python. All the graphs are indeed generated thanks to matplotlib, which on its side is based on numpy, which is currently not supported on PyPy.

# Installation

We strongly suggest to use virtualenv to not clobber the python system installation. First of all you have to create a pypy virtual environment. Here we assume that you already have pypy and virtualenv installed on your system.

## Setting up a virtual environment for running simulations

That's what you should do to get an environment capable of carrying out intensive simulations:

	$ virtualenv -p /usr/bin/pypy venv-pypy
	Running virtualenv with interpreter /usr/bin/pypy
	New pypy executable in venv-pypy/bin/pypy
	Installing setuptools............done.
	Installing pip...............done.
	$ . venv-pypy/bin/activate
	(venv-pypy)$ pip install networkx
	Downloading/unpacking networkx
	  Downloading networkx-1.7rc1.tar.gz (724Kb): 724Kb downloaded
	  Running setup.py egg_info for package networkx
	  ...

Now you should be ready to run the simulations.

## Setting up a virtual environment for rendering graphs

In this case we have to use the classic Python implementation, namely CPython. We then need to create an isolated virtual environment and on top of it install `numpy` and `matplotlib` which is the package responsible for graph rendering. Please be aware that you need gcc, gcc-f77 and several other packages to build `numpy` from sources. Take also in consideration that some of the plot scripts require a working latex environment to run properly.

	$ virtualenv venv-graph
	New python executable in venv-graph/bin/python2
	Also creating executable in venv-graph/bin/python
	Installing setuptools............done.
	Installing pip...............done.
	$ . venv-graph/bin/activate
	(venv-graph)$ pip install numpy
	...
	(venv-graph)$ pip install matplotlib
	...


## Evaluating the Average Blocking Probability

For evaluating the average blocking probability you have to execute the `plot.py` script passing as its first argument the keyworkd `blocking`.

	(venv-pypy)$ pypy plot-scripts/plot.py blocking
	...

After the execution, the file `graph-block.py` should have been generated. Just run it through the `venv-graph` environment, and you will get the `graph-block.eps` file.

	(venv-graph)$ python graph-block.py

## Evaluating the Average Interference Level

For evaluating the interference level you have to execute the `plot.py` script passing as its first argument the keyworkd `interference`.

	(venv-pypy)$ pypy plot-scripts/plot.py interference
	[ Classic]   80 rate, 2.036167 interference,   4939 blocks, 102501 arrivals [0.0482]
	[      FF]   80 rate, 2.124782 interference,    206 blocks, 100144 arrivals [0.0021]
	[   FF/LF]   80 rate, 1.893770 interference,    206 blocks, 100144 arrivals [0.0021]
	[ FF/LF/2]   80 rate, 1.845894 interference,    214 blocks, 100146 arrivals [0.0021]
	[ MinCost]   80 rate, 1.730013 interference,    203 blocks, 100141 arrivals [0.0020]
	...

The script automatically generates the script `graph.py`. You can run it through the `venv-graph` environment as usual and get the `graph.eps` file as output.

	(venv-graph)$ python graph.py


## Evaluating the PDF of the Distance/Interference

In order to get a graph showing the PDF of the distance in hops, or the graph of the Average interference level in function of the number of hops you first have to collect several statistics. To do this just run the `plot.py` script passing as first argument the keyword `pdf`:

	(venv-pypy)$ pypy plot-scripts/plot.py pdf
	[ Classic]   80 rate,   2574 blocks,  51326 arrivals [0.0502]
	[      FF]   80 rate,     73 blocks,  50082 arrivals [0.0015]
	[   FF/LF]   80 rate,    117 blocks,  50093 arrivals [0.0023]
	[ FF/LF/2]   80 rate,    106 blocks,  50083 arrivals [0.0021]
	[ MinCost]   80 rate,    148 blocks,  50111 arrivals [0.0030]
	...

The command will generate a file `pdf-all.txt` cotnaining all the needed statistics to extract the two graphs.

Now to extract the PDF of the distance just issue:

	(venv-graph)$ python plot-scripts/distance-all.py
	...

The command will generate the file `pdf-distance.eps`. Instead, to get the graph representing the Average interference level in function of the number of hops you have to use:

	(venv-graph)$ python plot-scripts/pdf-all.py
	...

The script will then generate the file `pdf.eps`.

## Other Graphs

The `plot-scripts` directory also contains two other scripts generating two different graphs:

 - `central-vs-side.py`: Shows the difference between the central and side allocation in terms of average interference level. It generates the `generic.eps` file.
 - `precompute.py`: For each possible combination it computes the best slot that produces the minimum interference. The result is then shown as an histogram.