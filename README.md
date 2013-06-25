romancalckata
=============

This is an implementation of the
[Roman Numeral Calculator kata](http://codingdojo.org/cgi-bin/wiki.pl?KataRomanCalculator)
from [codingdojo.org](http://codingdojo.org) in Python.  This is one
of the first programs of more than a few lines that I wrote in Python.
It doesn't do anything really exciting, but it's a good example of
what I believe good Python style to be---straightforward,
well-factored, and, most of all, *elegant* without being too tricky.

All the action is in `class RNum`, which some people may object to as
being too big (certainly more than one screen!).  My take on that is
that all the functionality belongs in that class---additional helper
classes would only compromise good cohesion and add unnecessary
coupling, the bane of overtricky OO systems.  The rest of the file is
a unit- and integration-test harness developed side-by-side with
`RNum`, [TDD](http://www.agiledata.org/essays/tdd.html)-style, using
the standard Python `unittest` module.

