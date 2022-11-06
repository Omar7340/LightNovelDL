# LightNovelDL

## Purpose

Create epub file from lightnovel taken from the web

## Supported source

- https://lightnovelfr.com/

## Python package used

- requests
- Beautiful Soup 4
- pypub (version Python 3 compatible from https://github.com/imgurbot12/pypub.git )
- unidecode (have to remove all of the accented characters in title of the chapters because they are not supported only
  in the table of content and i dont know why)