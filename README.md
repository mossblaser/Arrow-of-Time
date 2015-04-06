Arrow of Time
=============

[![Build Status](https://travis-ci.org/mossblaser/Arrow-of-Time.svg?branch=master)](https://travis-ci.org/mossblaser/Arrow-of-Time)

An implementation of Andrew Webb's universe model in which entopy (number of
non-A particles) increases no matter which direction time advances except
following a small number of starting states.

Currently not working!


Development
-----------

To setup in a virtualenv:

    $ virtualenv arrow_of_time_env
    $ cd arrow_of_time_env
    $ . bin/activate
    $ git clone git@github.com:mossblaser/Arrow-of-Time.git arrow_of_time
    $ cd arrow_of_time

To run tests:

    $ pip install -r requirements-test.txt
    $ py.test arrow_of_time
