#!/bin/sh

# BibTeX -> jemdoc

# jemdoc -> html
./jemdoc -c mysite.conf *.jemdoc

# local -> git repo
git add --all
git commit -m "housekeeping shell script"
git push origin master