# Workshop data-sciences

This website is the main support of a two-days datasciences workshop taking place in Fribourg on October 2017. It covers the basics of big data analytics using HADOOP and related technologies.

It is powered by the exascale institute of the UNIFR and the DAPLAB institute of the HEIA-FR.

## Setup and run

(1) clone this repo:

```shell
git@github.com:derlin/workshop-data-sciences.git
```

(2) install dependencies:

```shell
pip install -r requirements.txt
```

(3) start a local server (default to [http://localhost:8000/](http://localhost:8000/)):

```shell
cd workshop-data-sciences
mkdocs serve
```

(4) modify the site and add content

(5) deploy the changes by (a) updating the master branch on github and (b) updating the gh-pages branch:

```shell
# update master branch
git commit -a -m "do some changes"
git push origin master
# updatet the gh-pages branch, i.e. the website
mkdocs gh-deploy
```

## Editing rules and tips

External links should always open into a new tab. For that, add `{: target="_blank"}` after any markdown link, for example

```
[some link](http://example.com){: target="_blank"}
```

The theme is mkdocs-material, which has a [great documentation](http://squidfunk.github.io/mkdocs-material). We also use a lot of extensions, most of which are explained in the docs. The most interesting one is the [Admonition](http://squidfunk.github.io/mkdocs-material/extensions/admonition/) one, so have a look at it !
