#!/bin/sh
# explicit setting of script execution directory
cd -- "$(dirname -- "$BASH_SOURCE")"

# BibTeX -> jemdoc

# jemdoc -> html
echo "\njemdoc ----> html"
./jemdoc -c mathjax.conf *.jemdoc


# local -> git repo
echo "\nlocal dir ----> git repo"
git add --all
git commit -m "housekeeping shell script"
git push origin master
git status
