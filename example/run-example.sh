#!/bin/sh
echo 'Running a clean Docker instance with just Python on it'
echo 'To get a feel for dotrunner and dotlinker, run this inside the container'
echo ''
echo '$ pip install dotrunner dotlinker'
echo '$ dotrunner /dotfiles/dotfiles-demo'
echo '$ dotlinker /dotfiles/dotfiles-demo ~'
echo ''
echo 'Have fun!'
docker run -it -v `pwd`:/dotfiles python:alpine sh
