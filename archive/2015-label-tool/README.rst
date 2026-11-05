====================================================
Github Organization Information and Management Tools
====================================================

Use with care!

Setup
=====

Follow the standard buildout process::

    virtualenv .
    ./bin/pip install zc.buildout
    ./bin/buildout

Source Code
===========

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

If you want to help with the development (reporting, improvement, update, bug-fixing, ...) of ``plone.github`` this is a great idea!

Please file any issues or ideas for enhancement at the `issue tracker <https://github.com/plone/plone.github/issues>`_.

The code is located in `github <https://github.com/plone/plone.github>`_.

Documentation for the used Labels is in `Google Sheets - Github Plone Organisation Labels <https://docs.google.com/spreadsheets/d/1IQ73bSQ10b0pwoUFn0u8SE4epDdvwjhTiYTDyPAhx7A/edit#gid=0>`_.

Maintainer is Jens Klein and the Plone Foundation Core Developer team.
We appreciate any contribution!

Usage
=====

.. code:: sh

    usage: manage_labels [-h] -t TOKEN [-c CONFIGURATION] [-s]
                         [--debug-limit DEBUG_LIMIT]
                         [repos [repos ...]]

    positional arguments:
    repos                 Repositories to match

    optional arguments:
    -h, --help            show this help message and exit
    -t TOKEN, --token TOKEN
                        Github token
    -c CONFIGURATION, --configuration CONFIGURATION
                        configuration file (json) to be used.
    -s, --summary         Show summary of labels with used repos and colors
    --debug-limit DEBUG_LIMIT
                        Limit the number of repos fetched, for debugging


Apply Labels
============

To apply new Labels or Apply it to new Repositories adjust the definitions.json file.

You need a Github Token with owner permission on the organisatzion level.
You could generate a Github Token on `Personal access tokens <https://github.com/settings/tokens>`

To execute, run:

.. code:: sh

    ./bin/manage_labels -t <github token>


Contributors
============

- Jens W. Klein <jens@bluedynamics.com> - development
- Alexander Loechel <Alexander.Loechel@lmu.de> - development
