# Final Project

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/PurtiS/final_project/main.svg)](https://results.pre-commit.ci/latest/github/PurtiS/final_project/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## EPP Project Submission

This is a project created from Pytask Project template. The objective of the paper is to
find the effect of unemployment on loneliness among working age population.

## Project overview

## Project Structure

My project mainly contains a source folder and a tests folder, the former further
contains sections for Data Management, Analysis, Original Data files and Plots. The
tests folder comprises of a similar distribution with test functions for all the
functions created in source files. The project uses Propensity score matching as the
empirical strategy. After we get the filtered data, we implement matching in the
Modeling and predict a Matched Dataset. This matched dataset is then used to run a
regression and find Avergae Treatment Effect on the treated and Average Treatment
Effect. The matching quality and the effect size of the variables is shown in the
figures.

## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate final_project
```

If you encounter any issues with dependencies, make sure to install the required
libraries using pip:

```
$ pip install PsmPy
```

To build the project, type

```console
$ pytask
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
