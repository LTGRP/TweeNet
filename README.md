# TweeNet

Let's visualize your Twitter Friendship Network!

## Installation

### [pip](https://pip.pypa.io/en/stable/)
```
pip install requirements.txt
```

### [pipenv](https://pipenv.kennethreitz.org/en/latest/#) 
Use pipenv to manage and install the Python packages.

```bash
pipenv install
```

## Usage
To use data_scraper.py

```
Usage: data_scraper.py [OPTIONS] TARGET

Options:
  -f, --filename TEXT  filename of output data  [default: data.json]
  --help               Show this message and exit.
```
To show visualization, please make sure the file /measures/network_measure_data.csv is in your local file system, and run visual_dirg_gephi.py.

## Preview
![Example](/graphs/spacex-visual.gif)
