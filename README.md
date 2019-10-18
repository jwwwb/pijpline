## Pijpline

A quickly hacked tool to run bitbucket-pipeline.yml files locally.
As it was developed in amsterdam to run pipes, the name is Pijp.

#### Requirements

* docker
* python3

#### Installation

* `pip install .`

#### Usage

`pijp [--file bitbucket-pipelines.yml] [--branch qa] [--environment envfile]`

###### Arguments

* `--file`: location of the pipeline file, defaults to `bitbucket-pipelines.yml`
* `--branch`: which branch to execute, defaults to `qa`.
* `--environment`: file storing environment variables for the pipeline.
  Can be in yaml or json format, or a sh script containing export statements. By default uses the current shell's env.

