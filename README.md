[![Build Status](https://travis-ci.org/ltalirz/sycofinder.svg?branch=master)](https://travis-ci.org/ltalirz/sycofinder)
[![DOI](https://zenodo.org/badge/139702936.svg)](https://zenodo.org/badge/latestdoi/139702936)

# LSMO Synthesis Condition Finder

Optimize your synthesis conditions

 1. Generate a maximally diverse set of conditions
 1. Evolve the set of conditions based on experimentally determined fitness (using a genetic algorithm)
 1. Determine importance of synthesis variables

## Use SyCoFinder

 * [Watch the youtube tutorial](https://youtu.be/i8i4HmEEw4Y)
 * [Try it live](https://www.materialscloud.org/work/tools/sycofinder)

## Run SyCoFinder locally (for development)

```
pip install -e .
python run.py
# open http://0.0.0.0:8050/
```

## Run inside docker container (for deployment)

```
./build-docker.sh
./run-docker.sh
# open http://localhost:8050
```

## Citing SyCoFinder

If your scientific work has benefited from the use of SyCoFinder,
please consider an acknowledgement through the following citation

 * Seyed Mohamad Moosavi, Arunraj Chidambaram, Leopold Talirz, Maciej Haranczyk, Kyriakos C. Stylianou, Berend Smit. _Nat. Commun._ doi: [10.1038/s41467-019-08483-9](https://dx.doi.org/10.1038/s41467-019-08483-9)
 * Talirz, L., Moosavi, S. M.  SyCoFinder (2019). [![DOI](https://zenodo.org/badge/139702936.svg)](https://zenodo.org/badge/latestdoi/139702936)

## Contact

For information concerning SyCoFinder, please contact
[leopold.talirz@gmail.com](mailto:leopold.talirz@gmail.com)
or [open an issue](https://github.com/ltalirz/sycofinder/issues/new).
