5Minutes
========

5Minutes is a simple work queue management system. Manage your time and what you are working on - quickly and easily.

Launch Development Version
--------------------------

To run with settings in settings.cfg.template, run:

```
$ ./runserver.py
```

The app will be up on port 5000 (Flask default).

Launch with Environment Variable Configuration
--------------------------------------------------

To start the app, copy `settings.cfg.template` to a file and edit
it to your liking. Then, run:
```
$ CONFIG=~/5Minutes/settings.cfg ./runserver.py -p 8001
```

Note that the `CONFIG` environment variable has to be an absolute path!
