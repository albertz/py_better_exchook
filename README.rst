==============
better_exchook
==============

A nicer drop-in-replacement for Python ``sys.excepthook``,
i.e. it prints stack traces with extended information.
It will add some useful information for each frame,
like printing the relevant variables (relevant = referenced in the code line).

Features
--------
* Shows locals/globals per frame, but only those used in the current statement.
  It does this by a simple Python code parser.
  By default, we exclude builtins, undefined names,
  bound methods (when accessed via the original attribute),
  modules, top-level module functions.
* Multi-line Python statements in the stack trace output,
  in case the statement goes over multiple lines.
* Shows full function qualified name (not just ``co_name``).
* Colored/formatted output of each frame.
* Syntax highlighting for the Python source code.
* Support for `DomTerm <https://github.com/PerBothner/DomTerm>`__ text folding
  (`see more <https://stackoverflow.com/a/54019993/133374>`__),
  where it folds all the details of each stack frame away by default,
  and thus provides a much more comprehensive overview,
  while still providing all the details when needed.

.. image:: https://github.com/albertz/py_better_exchook/workflows/CI/badge.svg
    :target: https://github.com/albertz/py_better_exchook/actions


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

Or:

.. code:: python

  import better_exchook
  better_exchook.setup_all()

API:

* **setup_all()**
    - ``install()`` + ``replace_traceback_format_tb()`` + ``replace_traceback_print_tb()``
* **install()**:
    - ``sys.excepthook = better_exchook``
* **replace_traceback_format_tb()**:
    - ``traceback.format_tb = format_tb``
    - ``traceback.StackSummary.format = format_tb``
    - ``traceback.StackSummary.extract = _StackSummary_extract``
* **replace_traceback_print_tb()**:
    - ``traceback.print_tb = print_tb``
    - ``traceback.print_exception = print_exception``
    - ``traceback.print_exc = print_exc``
* **better_exchook(exc_type, exc_value, tb, ...)** / **print_exception(exc_type, exc_value, tb, ...)**:
    - Prints the exception and its traceback with extended information.
* **format_tb(tb, ...) -> list[str]**:
    - Formats the traceback with extended information, returning a string for every frame.
      The string per frame includes a newline at the end.


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
      File "/Users/az/Programmierung/py_better_exchook/demo.py", line 23, in demo
        line: f()
        locals:
          f = <local> <function demo.<locals>.f at 0x10328f740>
      File "/Users/az/Programmierung/py_better_exchook/demo.py", line 21, in demo.<locals>.f
        line: x, 42, sys.stdin.__class__, sys.exc_info, y, z  # noqa: F821
        locals:
          x = <local> {1: 2, 'a': 'b'}
          sys.stdin = <global> <_io.TextIOWrapper name='<stdin>' mode='r' encoding='utf-8'>
          sys.stdin.__class__ = <global> <class '_io.TextIOWrapper'>
          y = <local> 'foo'
    NameError: name 'z' is not defined

Python example code:

.. code:: python

    try:
        (lambda _x: None)(
            __name__,
            42,
        )  # multiline
    except Exception:
        better_exchook(*sys.exc_info())

Output:

.. code::

    EXCEPTION
    Traceback (most recent call last):
      File "/Users/az/Programmierung/py_better_exchook/demo.py", line 29, in demo
        line: (lambda _x: None)(
                  __name__,
                  42,
              )  # multiline
        locals:
          __name__ = <global> '__main__', len = 8
    TypeError: demo.<locals>.<lambda>() takes 1 positional argument but 2 were given

Python example code:

.. code:: python

    # use this to overwrite the global exception handler
    sys.excepthook = better_exchook.better_exchook
    # and fail
    raise ValueError("final failure: %s" % ((sys, f1, 123),))

Output:

.. code::

    EXCEPTION
    Traceback (most recent call last):
      File "/Users/az/Programmierung/py_better_exchook/demo.py", line 106, in <module>
        line: main()
        locals:
          main = <local> <function main at 0x103071c60>
      File "/Users/az/Programmierung/py_better_exchook/demo.py", line 102, in main
        line: demo()
      File "/Users/az/Programmierung/py_better_exchook/demo.py", line 69, in demo
        line: raise ValueError("final failure: %s" % ((sys, f1, 123),))
        locals:
          f1 = <local> <function demo.<locals>.f1 at 0x1030d1da0>
    ValueError: final failure: (<module 'sys' (built-in)>, <function demo.<locals>.f1 at 0x1030d1da0>, 123)

Screenshot:

.. image:: https://gist.githubusercontent.com/albertz/a4ce78e5ccd037041638777f10b10327/raw/2cda70f8c5c0478e545640369ebf58d49bf0001c/screenshot2.png

.. _domterm:

Screencast with `DomTerm <http://domterm.org>`__ using text folding (`see more <https://stackoverflow.com/a/54019993/133374>`__):

.. image:: https://gist.githubusercontent.com/albertz/a4ce78e5ccd037041638777f10b10327/raw/7ec2bb7079dbd56119d498f20905404cb2d812c0/screencast-domterm.gif


Status
------

This has been used in production for many years (since 2011)
and should be fairly stable (and has a save fallback mode).


Details
-------

Also see `Python source and comments <https://github.com/albertz/py_better_exchook/blob/master/better_exchook.py>`_ for further details.



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
* `patrys / great-justice <https://github.com/patrys/great-justice>`__
* `Qix- / better-exceptions <https://github.com/Qix-/better-exceptions>`__.
  Pretty-print Python exceptions and their tracebacks.
  Adds content of relevant variables from the current source line,
  but only top-level names, not attributes of objects
  (for ``a.b``, only print ``a``).
  Also does not support multi-line statements,
  and no full function qualified names.
  Also currently (2025-06) broken for Python 3.13.
* `onelivesleft / PrettyErrors <https://github.com/onelivesleft/PrettyErrors>`__
* `friendly-traceback <https://friendly-traceback.github.io/>`__.
  Prints tracebacks with added explanations,
  intended for Python beginners.
* `skorokithakis / tbvaccine <https://github.com/skorokithakis/tbvaccine>`__.
  Pretty-print Python tracebacks.
  Automatically highlights lines you care about.
  Can print all locals of a frame
  (but no selection of only relevant ones, no globals).
* `alexmojaki / stack_data <https://github.com/alexmojaki/stack_data>`__.
  Extracts data from stack frames.
* See `this <http://stackoverflow.com/questions/1308607/python-assert-improved-introspection-of-failure>`__
  related StackOverflow question.


-- Albert Zeyer, <http://www.az2000.de>
