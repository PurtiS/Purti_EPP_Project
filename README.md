# Final Project

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/PurtiS/final_project/main.svg)](https://results.pre-commit.ci/latest/github/PurtiS/final_project/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## EPP Project Submission

- Author- Purti Sadhwani
- Project Name- Final Project

## Project overview

This is a project created from Pytask Project template. The objective of the paper is to
find the effect of unemployment on loneliness among working age population.

The project mainly contains a source folder and a tests folder, the former further
contains sections for Data Management, Analysis, Original Data files and Plots. The
tests folder comprises of a similar distribution with test functions for all the
functions created in source files. The project uses Propensity score matching as the
empirical strategy. After we get the filtered data, we implement matching in the
Modeling and predict a Matched Dataset. This matched dataset is then used to run a
regression and find Avergae Treatment Effect on the treated and Average Treatment
Effect. The matching quality and the effect size of the variables is shown in the
figures.

## Theoretical Motivation

In order to analyse the effect of Unemployment on Loneliness, I have used SOEP Dataset
for the original Datasets. There are three Loneliness measures, socially isolated,
feeling left out and missing company of others. These were measured for the years
2013-17 and therfore the analysis focuses on the mentioned time frame. These measure are
combined as aggregate loneliness as an outcome in the year 2017. We look at the impact
on loneliness for those who went unemployed in this period isloating the effect of other
covariates using Propensity Score Matching and further conclude with Average Treatment
effects.

## Project Structure

#### The SRC Folder contains the folder named final_project with following:

- Data Folder- With compressed Datasets from SOEP used as original datasets
- Data Management Folder - Contains data cleaning functions and produces a filtered
  dataset from the task executed inside it.
- Analysis Folder - Contains models and predictions. We execute PSM, regression in the
  task file and predict matched dataset and regression results.
- Final Folder - Contains Plotting functions and executes the task in order to produce 8
  plots subsequently in the build folder.

#### The Folder named Paper has:

- The tex files for presentation and the pdf compiled with the task file

#### The Tests Folder has:

- Data Management folder with tests pertaining to data cleaning functions.
- Analysis Folder with tests pertainign to the modeling and predictions functions.

#### When pytest and pytask modules are used, we find the results in the BLD Folder under specific subsections.

## Usage

- The environment.yml file contians all the dependencies. Missinf dependencies can be
  installed.

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

## Acknowledgments

I would like to express my sincere gratitude to Professor Hans-Martin von Gaudecker and
Janos Gabler for their invaluable guidance and support throughout this project. Their
mentorship has been instrumental in my journey as a beginner in Python, VSCode, and
GitHub. This project has been an amazing roller coaster like learning experience for me.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
