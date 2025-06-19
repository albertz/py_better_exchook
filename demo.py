import sys
from argparse import ArgumentParser
import better_exchook


# noinspection PyMissingOrEmptyDocstring,PyBroadException
def demo():
    """
    Some demo.
    """
    # some examples
    # this code produces this output: https://gist.github.com/922622

    try:
        x = {1: 2, "a": "b"}

        # noinspection PyMissingOrEmptyDocstring
        def f():
            y = "foo"
            # noinspection PyUnresolvedReferences,PyStatementEffect
            x, 42, sys.stdin.__class__, sys.exc_info, y, z  # noqa: F821

        f()
    except Exception:
        sys.excepthook(*sys.exc_info())

    try:
        # noinspection PyArgumentList
        (lambda _x: None)(
            __name__,
            42,
        )  # multiline
    except Exception:
        sys.excepthook(*sys.exc_info())

    try:

        class Obj:
            def __repr__(self):
                return "<Obj multi-\n" + "     line repr>"

        obj = Obj()
        assert not obj
    except Exception:
        sys.excepthook(*sys.exc_info())

    # noinspection PyMissingOrEmptyDocstring
    def f1(a):
        f2(a + 1, 2)

    # noinspection PyMissingOrEmptyDocstring
    def f2(a, b):
        f3(a + b)

    # noinspection PyMissingOrEmptyDocstring
    def f3(a):
        b = ("abc" * 100) + "-interesting"  # some long demo str
        a(b)  # error, not callable

    try:
        f1(13)
    except Exception:
        sys.excepthook(*sys.exc_info())

    # final fail
    raise ValueError("final failure: %s" % ((sys, f1, 123),))


def _debug_shell():
    better_exchook.debug_shell(locals(), globals())


def _debug_shell_exception():
    # noinspection PyBroadException
    try:
        raise Exception("demo exception")
    except Exception:
        better_exchook.better_exchook(*sys.exc_info(), debugshell=True)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("command", help="demo, debug_shell, ...", nargs="?")
    arg_parser.add_argument("--excepthook-setup", help="excepthook setup", default="better_exchook.install()")
    args = arg_parser.parse_args()

    exec(args.excepthook_setup, globals(), locals())

    if args.command:
        if "_%s" % args.command in globals():
            func_name = "_%s" % args.command
        elif args.command in globals():
            func_name = args.command
        else:
            print("Error: Function (_)%s not found." % args.command)
            sys.exit(1)
        print("Run %s()." % func_name)
        func = globals()[func_name]
        func()
        sys.exit()

    # Just run the demo.
    demo()


if __name__ == "__main__":
    main()
