[![DOI](https://zenodo.org/badge/139702936.svg)](https://zenodo.org/badge/latestdoi/139702936)

# LSMO Synthesis Condition Finder

Optimize your synthesis conditions

 1. Generate a maximally diverse set of conditions
 1. Evolve the set of conditions based on experimentally determined fitness (using a genetic algorithm)
 1. Determine importance of synthesis variables

[Try it live](https://www.materialscloud.org/work/tools/sycofinder)

## Run locally

```
pip install -e .
python run.py
# open http://0.0.0.0:8050/
```

## Run inside docker container

```
./build-docker.sh
./run-docker.sh
# open http://localhost:8050
```
