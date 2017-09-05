* Guess a Number

This is a tiny project to proove a setup of python and scratch. The goal of this project is to introduce basics of computer science to pupils of primary school.
But not only theoretical aspects of computer science should be teached, it should also introduce the everyday problems of developers working in a team.

Therefore this project provides a part in python to be implemented by those with pre knowledge and a gui part in scratch to be implemented by complete newbies.

Guess a Number provides a small game to guess a number, that will be asked by a scratch gui, but the "business logic" of comparing the number with entries
of the user are implemented in a python backend.

For the Backend install [Python 2.x](https://www.python.org/downloads/)

Then install virtualenv by
pip install virtualenv

After cloning this repo by
git clone https://github.com/fonzerelly/guess_a_number.git

and running setup.sh

you should have setup a virtual python enviroment with all necessary dependencies.

Run
source Scripts/activate

to to activate the virtual environment.

Now you can run
nosetests -s

to run all python tests.

On the scratch site you need to install scratch 1.x from [https://scratch.de.uptodown.com/windows](https://scratch.de.uptodown.com/windows)

