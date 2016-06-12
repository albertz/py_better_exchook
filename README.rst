==============
better_exchook
==============

A nicer drop-in-replacement for Python ``sys.excepthook``.
It will add some useful information for each frame,
like printing the relevant variables (relevant = referenced in the code line).
Also see `Python source and comments <https://github.com/albertz/py_better_exchook/blob/master/better_exchook.py>`_ for further details.

You can just copy over the file ``better_exchook.py`` to your project.
Or alternatively, it is also available `on PyPI <https://pypi.python.org/pypi/better_exchook>`_
and can be installed via:

.. code::

  pip install better_exchook

Usage:

.. code:: python

  import better_exchook
  better_exchook.install()  # will just do: sys.excepthook = better_exchook

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


Similar projects:
 - `<https://github.com/patrys/great-justice>`_
 - `Nose does something similar for assertion failures <http://nose.readthedocs.io/en/latest/plugins/failuredetail.html>`_.
 - See `this <http://stackoverflow.com/questions/1308607/python-assert-improved-introspection-of-failure>`_ related StackOverflow question.


-- Albert Zeyer, <http://www.az2000.de>
