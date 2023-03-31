# Final Project

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/PurtiS/final_project/main.svg)](https://results.pre-commit.ci/latest/github/PurtiS/final_project/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## EPP Project Submission

- Author- Purti Sadhwani
- Project Name- Final Project

## Project overview

This project was developed using the Pytask Project template with the aim of
investigating the relationship between unemployment and loneliness among the working-age
population.

The project is composed of two main folders: a source folder and a tests folder. The
source folder includes sections for managing data, analyzing data, storing original data
files, and generating plots. The tests folder contains similar subfolders with test
functions for all the functions created in the source files. The project adopts
Propensity Score Matching as the empirical strategy. Once the data is filtered, we apply
matching to generate a matched dataset. This matched dataset is then used to conduct
regression analysis to identify the Average Treatment Effect for both the treated and
control groups. The matching quality and effect sizes of variables are presented in the
figures.

## Theoretical Motivation

To examine the impact of unemployment on loneliness, I utilized the SOEP dataset as the
primary source for data analysis. The dataset includes three distinct measures of
loneliness, namely social isolation, feelings of exclusion, and the absence of company.
These measures were assessed during the years 2013-17, and the analysis is therefore
limited to this period. The measures were combined to form an overall measure of
loneliness in 2017. To isolate the effect of unemployment from other covariates,
Propensity Score Matching was employed, and Average Treatment Effects were subsequently
calculated to determine the impact of unemployment on loneliness.

## Project Structure

#### The SRC Folder contains the folder named final_project with following:

- Data Folder- With compressed Datasets from SOEP used as original datasets. The
  datasets used from SOEP are: pgen, ppathl, pl, hgen and hbrutto. Please find more
  information in usage.
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

- In order to use the datasets from SOEP, one can visit
  https://www.diw.de/en/diw_01.c.601584.en/data_access.html. The datasets can be
  directly used for the data cleaning functions created in the project.
- Variables used are defined in data_info.yaml file in the source folder.
- The environment.yml file contians all the dependencies. Missing dependencies can be
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
