import pycli

EXTTEXT_OPT = pycli.Option[list[str]]("extra", help="Add extra text", default="", nargs="+")


class Bar(pycli.Command):
    short = "Prints 'bar'"
    long = "Prints 'bar' to stdout"

    opts = [
        # defining predefined option
        # it's value will be available from get method
        EXTTEXT_OPT,
        # defining name-referenced opt
        # it's value will be available from get_by_name method
        pycli.Option[int]("rc", help="Return code"),
    ]

    def exec(self, vals: pycli.Values) -> int:
        
        extra = vals.get(EXTTEXT_OPT)
        if extra is None:
            extra = []
        print(f"bar {' '.join(extra)}")
        
        rc = vals.get_by_name("rc", True)
        if rc:
            return rc
        return 0


class Foo(pycli.Command):
    short = "Prints 'foo'"
    long = "Prints 'foo' to stdout"

   # All attributes named like _opt_* are interpreted like local options
    _opt_verbose = pycli.Option[bool](
            "verbose", ["-v", "--verbose"], "Print more information", is_flag=True
        )
    opts = [
        EXTTEXT_OPT
    ]

    children = [Bar()]

    def exec(self, vals: pycli.Values) -> int:
        verbose = vals.get(self._opt_verbose)
        if verbose:
            print("Printing 'foo'")
        print("foo")
        return 0


if __name__ == "__main__":
    rc = (
        pycli.Application("example", "Example application made with PyCLI")
        .with_commands(Foo(), Bar())
        .run()
    )
    if rc != 0:
        print(f"non-zero return code: {rc}")
    exit(rc)
