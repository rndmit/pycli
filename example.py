import pycli

EXTTEXT_OPT = pycli.Option[str]("extra", help="Add extra text", default="")


class Bar(pycli.Command):
    short = "Prints 'bar'"
    long = "Prints 'bar' to stdout"
    opts = [
        pycli.Option[bool](
            "verbose", ["-v", "--verbose"], "Print more information", is_flag=True
        ),
        pycli.Option[int]("rc", help="Return code"),
        EXTTEXT_OPT,
    ]

    def exec(self, opts: dict) -> int:
        if opts["verbose"]:
            print("Printing 'bar'")
        try:
            extra = opts["extra"]
        except:
            extra = ""
        print(f"bar {extra}")
        try:
            return opts["rc"]
        except:
            return 0


class Foo(pycli.Command):
    short = "Prints 'foo'"
    long = "Prints 'foo' to stdout"
    opts = [
        pycli.Option[bool](
            "verbose", ["-v", "--verbose"], "Print more information", is_flag=True
        )
    ]
    children = [Bar()]

    def exec(self, opts: dict) -> int:
        if opts["verbose"]:
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
