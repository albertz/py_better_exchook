==============
better_exchook
==============

A nicer drop-in-replacement for Python ``sys.excepthook``,
i.e. it prints stack traces with extended information.
It will add some useful information for each frame,
like printing the relevant variables (relevant = referenced in the code line).
Also see `Python source and comments <https://github.com/albertz/py_better_exchook/blob/master/better_exchook.py>`_ for further details.

Features
--------
* Shows locals/globals per frame, but only those used in the current statement.
  It does this by a simple Python code parser.
* Multi-line Python statements in the stack trace output,
  in case the statement goes over multiple lines.
* Shows full function qualified name (not just ``co_name``).
* Colored/formatted output of each frame.
* Syntax highlighting for the Python source code.
* Support for `DomTerm <https://github.com/PerBothner/DomTerm>`__,
  where it folds all the details of each stack frame away by default,
  and thus provides a much more comprehensive overview,
  while still providing all the details when needed.


Installation
------------

You can just copy over the single file ``better_exchook.py`` to your project.

Or alternatively, it is also available `on PyPI <https://pypi.python.org/pypi/better_exchook>`_
and can be installed via:

.. code::

  pip install better_exchook


Usage
-----

.. code:: python

  import better_exchook
  better_exchook.install()  # will just do: sys.excepthook = better_exchook


Examples
--------

Python example code:

.. code:: python

    try:
        x = {1:2, "a":"b"}
        def f():
            y = "foo"
            x, 42, sys.stdin.__class__, sys.exc_info, y, z
        f()
    except Exception:
        better_exchook.better_exchook(*sys.exc_info())

Output:

.. code::

  EXCEPTION
  Traceback (most recent call last):
    File "better_exchook.py", line 478, in <module>
      line: f()
      locals:
        f = <local> <function f at 0x107f1de60>
    File "better_exchook.py", line 477, in f
      line: x, 42, sys.stdin.__class__, sys.exc_info, y, z
      locals:
        x = <global> {'a': 'b', 1: 2}
        sys = <global> <module 'sys' (built-in)>
        sys.stdin = <global> <open file '<stdin>', mode 'r' at 0x107d9f0c0>
        sys.stdin.__class__ = <global> <type 'file'>
        sys.exc_info = <global> <built-in function exc_info>
        y = <local> 'foo'
        z = <not found>
  NameError: global name 'z' is not defined

Python example code:

.. code:: python

    try:
        f = lambda x: None
        f(x, y)
    except Exception:
        better_exchook.better_exchook(*sys.exc_info())

Output:

.. code::

  EXCEPTION
  Traceback (most recent call last):
    File "better_exchook.py", line 484, in <module>
      line: f(x, y)
      locals:
        f = <local> <function <lambda> at 0x107f1df50>
        x = <local> {'a': 'b', 1: 2}
        y = <not found>
  NameError: name 'y' is not defined

Python example code:

.. code:: python

    try:
        (lambda x: None)(__name__,
                         42)  # multiline
    except Exception:
        better_exchook.better_exchook(*sys.exc_info())

Output:

.. code::

  EXCEPTION
  Traceback (most recent call last):
    File "better_exchook.py", line 490, in <module>
      line: (lambda x: None)(__name__,
                             42)  # multiline
      locals:
        x = <local> {'a': 'b', 1: 2}
        __name__ = <local> '__main__', len = 8
  TypeError: <lambda>() takes exactly 1 argument (2 given)

Python example code:

.. code:: python

    # use this to overwrite the global exception handler
    sys.excepthook = better_exchook.better_exchook
    # and fail
    finalfail(sys)

Output:

.. code::

  EXCEPTION
  Traceback (most recent call last):
    File "better_exchook.py", line 497, in <module>
      line: finalfail(sys)
      locals:
        finalfail = <not found>
        sys = <local> <module 'sys' (built-in)>
  NameError: name 'finalfail' is not defined

Screenshot:

.. image:: https://gist.githubusercontent.com/albertz/a4ce78e5ccd037041638777f10b10327/raw/7ec2bb7079dbd56119d498f20905404cb2d812c0/screenshot1.png

Screencast with `DomTerm <http://domterm.org>`__:

.. image:: https://gist.githubusercontent.com/albertz/a4ce78e5ccd037041638777f10b10327/raw/7ec2bb7079dbd56119d498f20905404cb2d812c0/screencast-domterm.gif


Similar projects
----------------

* `Nose does something similar for assertion failures <http://nose.readthedocs.io/en/latest/plugins/failuredetail.html>`_.
* IPython has something similar (`ultratb <https://github.com/ipython/ipython/blob/master/IPython/core/ultratb.py>`__).
  Do this: ``from IPython.core import ultratb; sys.excepthook = ultratb.VerboseTB()``.
  Shows more source code context (but not necessarily all relevant parts).
* Ka-Ping Yee's "cgitb.py", which is part of Python,
  `see here <https://docs.python.org/3/library/cgitb.html>`__,
  `code here <https://github.com/python/cpython/blob/3.7/Lib/cgitb.py>`__.
* `Rich Python library <https://github.com/willmcgugan/rich#tracebacks>`__.
  Syntax highlighting but without locals.
* `andy-landy / traceback_with_variables <https://github.com/andy-landy/traceback_with_variables>`__.
  Python Traceback (Error Message) Printing Variables.
  Very similar, but less advanced.
  Only shows locals, not globals, and also just all locals, not only those used in current statement.
  Also does not expand statement if it goes over multiple lines.
* `cknd / stackprinter <https://github.com/cknd/stackprinter>`__.
  Similar as IPython ultratb.
* `patrys / great-justice <https://github.com/patrys/great-justice>`_
* See `this <http://stackoverflow.com/questions/1308607/python-assert-improved-introspection-of-failure>`__
  related StackOverflow question.


-- Albert Zeyer, <http://www.az2000.de>
