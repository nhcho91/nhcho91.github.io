#!/bin/sh
# explicit setting of script execution directory
cd -- "$(dirname -- "$BASH_SOURCE")"

# BibTeX -> jemdoc, LaTeX
echo "\nBibTeX ----> jemdoc"
python3 format_bibtex.py jemdoc pub_nhcho publications "" 0
# To boldify main author: python format_bibtex.py jemdoc pub_nhcho publications Namhoon 0

echo "\nBibTeX ----> LaTeX"
python3 format_bibtex.py tex pub_nhcho publications Namhoon 0
mv ~/Dropbox/Personal\ Homepage/nhcho91.github.io/publications.tex ~/Dropbox/Research/Documents/Curriculum\ Vitae/publications.tex

# jemdoc -> html
echo "\njemdoc ----> html"
./jemdoc -c mathjax.conf *.jemdoc

# local -> git repo
echo "\nlocal dir ----> git repo"
git add --all
git commit -m "housekeeping shell script"
git push origin master
git status
