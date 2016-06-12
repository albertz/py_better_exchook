==============
better_exchook
==============

A nicer drop-in-replacement for Python ``sys.excepthook``.
It will add some useful information for each frame,
like printing the relevant variables (relevant = referenced in the code line).
Also see `Python source and comments <https://github.com/albertz/py_better_exchook/blob/master/better_exchook.py>`_ for further details.

Example output:

.. code::

  $ python better_exchook.py
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
  EXCEPTION
  Traceback (most recent call last):
    File "better_exchook.py", line 484, in <module>
      line: f(x, y)
      locals:
        f = <local> <function <lambda> at 0x107f1df50>
        x = <local> {'a': 'b', 1: 2}
        y = <not found>
  NameError: name 'y' is not defined
  EXCEPTION
  Traceback (most recent call last):
    File "better_exchook.py", line 490, in <module>
      line: (lambda x: None)(__name__,
                             42)  # multiline
      locals:
        x = <local> {'a': 'b', 1: 2}
        __name__ = <local> '__main__', len = 8
  TypeError: <lambda>() takes exactly 1 argument (2 given)
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


-- Albert Zeyer, <http://www.az2000.de>
