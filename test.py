
from argparse import ArgumentParser
from better_exchook import *


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


def test_syntax_error():
    """
    Test :class:`SyntaxError`.
    """
    from io import StringIO, BytesIO
    if sys.version_info[0] == 2:
        exc_stdout = BytesIO()
    else:
        exc_stdout = StringIO()
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
        f.write("[\n\ndef foo():\n  pass\n")
        f.flush()
        filename = f.name
        try:
            _import_dummy_mod_by_path(filename)
        except SyntaxError:
            better_exchook(*sys.exc_info(), file=exc_stdout, autodebugshell=False)
        else:
            raise Exception("We expected to get a SyntaxError...")
    # The standard exception hook prints sth like this:
    """
      File "/var/tmp/tmpx9twr8i2.py", line 3
        def foo():
          ^
    SyntaxError: invalid syntax
    """
    lines = exc_stdout.getvalue().splitlines()
    line4, line3, line2, line1 = lines[-4:]
    assert "SyntaxError" in line1
    assert "^" in line2
    assert "line:" in line3 and "foo" in line3
    assert os.path.basename(filename) in line4


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
        install()
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
