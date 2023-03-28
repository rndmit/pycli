# PyCLI

PyCLI is a library for creating Command-Line Interface Applications. It's inspired by [Cobra](https://github.com/spf13/cobra) and focuses on strictly typing, extensibility and as less magic as possible.

You define your application as child classes of the Command class. After you just instantiate Application class and register your commands in it. After firing ```Application.run``` method PyCLI parses ```sys.argv``` list, determines entered commands and extract values for their options.

## TLDR;
```python
from pycli import Application, Command, Option


class Foo(Command):
    name = "foo"
    short = "Prints \"foo\""
    long = "Prints \"foo\" into console"
    opts = [
        Option[bool](
            name="bar", 
            flags=["-b", "--bar"], 
            help="Prints \"bar\" instead \"foo\"", 
            is_flag=True
        )
    ]
    def exec(self, opts: dict) -> int:
        if opts["bar"]:
            print("bar")
        else:
            print("foo")
        return 0


if __name__ == "__main__":
    app = Application("foo-cli", descr="Awesome Foo Application")
    app.register(Foo())
    exit(app.run())
```