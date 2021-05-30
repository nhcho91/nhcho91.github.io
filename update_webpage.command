#!/bin/sh
# explicit setting of script execution directory
cd -- "$(dirname -- "$BASH_SOURCE")"


# BibTeX -> jemdoc, LaTeX
echo "\nBibTeX ----> jemdoc"
python format_bibtex.py jemdoc pub_nhcho publications "" 0
echo "\nBibTeX ----> LaTeX"
python format_bibtex.py tex pub_nhcho publications Namhoon 0

# jemdoc -> html
echo "\njemdoc ----> html"
./jemdoc -c mathjax.conf *.jemdoc

# local -> git repo
echo "\nlocal dir ----> git repo"
git add --all
git commit -m "housekeeping shell script"
git push origin master
git status
