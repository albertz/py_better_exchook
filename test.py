from argparse import ArgumentParser
import tempfile
from better_exchook import *
import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from io import BytesIO as StringIO
else:
    from io import StringIO

_IsGithubEnv = os.environ.get("GITHUB_ACTIONS") == "true"


def _fold_open(txt):
    if _IsGithubEnv:
        print("::group::%s" % txt)


def _fold_close():
    if _IsGithubEnv:
        print("::endgroup::")


def test_is_source_code_missing_open_brackets():
    """
    Test :func:`is_source_code_missing_open_brackets`.
    """
    assert is_source_code_missing_open_brackets("a") is False
    assert is_source_code_missing_open_brackets("a)") is True
    assert is_source_code_missing_open_brackets("fn()") is False
    assert is_source_code_missing_open_brackets("fn().b()") is False
    assert is_source_code_missing_open_brackets("fn().b()[0]") is False
    assert is_source_code_missing_open_brackets("fn({a[0]: 'b'}).b()[0]") is False
    assert is_source_code_missing_open_brackets("a[0]: 'b'}).b()[0]") is True


def test_add_indent_lines():
    """
    Test :func:`add_indent_lines`.
    """
    assert add_indent_lines("foo ", " bar") == "foo  bar"
    assert add_indent_lines("foo ", " bar\n baz") == "foo  bar\n     baz"


def test_get_same_indent_prefix():
    """
    Test :func:`get_same_indent_prefix`.
    """
    assert get_same_indent_prefix(["a", "b"]) == ""
    assert get_same_indent_prefix([" a"]) == " "
    assert get_same_indent_prefix([" a", "  b"]) == " "


def test_remove_indent_lines():
    """
    Test :func:`remove_indent_lines`.
    """
    assert remove_indent_lines(" a\n  b") == "a\n b"
    assert remove_indent_lines("  a\n b") == "a\nb"
    assert remove_indent_lines("\ta\n\t b") == "a\n b"


def _import_dummy_mod_by_path(filename):
    """
    :param str filename:
    """
    dummy_mod_name = "_dummy_mod_name"
    if sys.version_info[0] == 2:
        # noinspection PyDeprecation
        import imp
        # noinspection PyDeprecation
        imp.load_source(dummy_mod_name, filename)
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(dummy_mod_name, filename)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # noqa


def _run_code_format_exc(txt, expected_exception, except_hook=better_exchook):
    """
    :param str txt:
    :param type[Exception] expected_exception: exception class
    :return: stdout of better_exchook
    :rtype: str
    """
    exc_stdout = StringIO()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
        f.write(txt)
        f.flush()
        filename = f.name
        try:
            _import_dummy_mod_by_path(filename)
        except expected_exception:
            except_hook(*sys.exc_info(), file=exc_stdout)
        except Exception:  # some other exception
            # Note: Any exception which falls through would miss the source code
            # in the exception handler output because the file got deleted.
            # So handle it now.
            sys.excepthook(*sys.exc_info())
            print("-" * 40)
            raise Exception("Got unexpected exception.")
        else:
            raise Exception("We expected to get a %s..." % expected_exception.__name__)
    return exc_stdout.getvalue()


def test_syntax_error():
    """
    Test :class:`SyntaxError`.
    """
    exc_stdout = _run_code_format_exc("[\n\ndef foo():\n  pass\n", expected_exception=SyntaxError)
    # The standard exception hook prints sth like this:
    """
      File "/var/tmp/tmpx9twr8i2.py", line 3
        def foo():
          ^
    SyntaxError: invalid syntax
    """
    lines = exc_stdout.splitlines()
    line4, line3, line2, line1 = lines[-4:]
    assert "SyntaxError" in line1
    assert "^" in line2
    assert "line:" in line3 and "foo" in line3
    assert ".py" in line4


def test_get_source_code_multi_line():
    dummy_fn = "<_test_multi_line_src>"
    source_code = "(lambda _x: None)("
    source_code += "__name__,\n" + len(source_code) * " " + "42)\n"
    set_linecache(filename=dummy_fn, source=source_code)

    src = get_source_code(filename=dummy_fn, lineno=2)
    assert src == source_code

    src = get_source_code(filename=dummy_fn, lineno=1)
    assert src == source_code


def test_parse_py_statement_prefixed_str():
    # Our parser just ignores the prefix. But that is fine.
    code = "b'f(1,'"
    statements = (list(parse_py_statement(code)))
    assert statements == [("str", "f(1,")]


def test_exception_chaining():
    if PY2:
        return  # not supported in Python 2
    exc_stdout = _run_code_format_exc("""
try:
    {}['a']
except KeyError as exc:
    raise ValueError('failed') from exc
""", ValueError)
    assert "The above exception was the direct cause of the following exception" in exc_stdout
    assert "KeyError" in exc_stdout
    assert "ValueError" in exc_stdout


def test_exception_chaining_implicit():
    exc_stdout = _run_code_format_exc("""
try:
    {}['a']
except KeyError:
    raise ValueError('failed')
""", ValueError)
    if not PY2:  # Python 2 does not support this
        assert "During handling of the above exception, another exception occurred" in exc_stdout
        assert "KeyError" in exc_stdout
    assert "ValueError" in exc_stdout


def test():
    for k, v in sorted(globals().items()):
        if not k.startswith("test_"):
            continue
        _fold_open(k)
        print("running: %s()" % k)
        v()
        _fold_close()

    print("All ok.")


def main():
    """
    Main entry point. Either calls the function, or just calls the demo.
    """
    arg_parser = ArgumentParser()
    arg_parser.add_argument("command", default=None, help="test, ...", nargs="?")
    args = arg_parser.parse_args()
    if args.command:
        if "test_%s" % args.command in globals():
            func_name = "test_%s" % args.command
        elif args.command in globals():
            func_name = args.command
        else:
            print("Error: Function (test_)%s not found." % args.command)
            sys.exit(1)
        print("Run %s()." % func_name)
        func = globals()[func_name]
        func()
        sys.exit()

    # Run all tests.
    test()


if __name__ == "__main__":
    main()
