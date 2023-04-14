"""App module
"""
from typing import Tuple, Self
import sys
import jinja2
from .command import Command
from .option import Option
from .values import Values
from .output import Messager


class Application(object):
    """Application is a first class entity which holds \
    root command of your CLI app. It handles all CLI application \
    lifecycle.
    """

    opt_help = Option[bool](
        "help",
        flags=["-h", "--help"],
        help="Get help for commands",
        is_flag=True,
    )

    class RootCommand(Command):
        def __init__(self, name, descr=None, *opts: Option):
            self.name = name
            self.long = descr
            self.children = list[Command]()
            for opt in opts:
                self.opts.append(opt)

        def exec(self, opts):
            return

    __messager: Messager
    root_cmd: Command

    def __init__(
        self, name: str = "", descr: str = None, global_opts: Tuple[Option] = None
    ):
        """
        Args:
            name: application name (actually root command name)
            descr: discription of your application (e.g. "tool for doing something"
            global_opts: Options which will be parsed with all commands
        """
        self.__messager = Messager(jinja2.FileSystemLoader("pycli/templates"))
        self.root_cmd = self.RootCommand(name, descr, self.opt_help)
        if global_opts:
            self.root_cmd.opts += global_opts

    def with_commands(self, *cmds: Command) -> Self:
        """Registers Command within application's root command

        Args:
            *cmds: one or more Command(-s) which should be registered
        """
        for cmd in cmds:
            self.root_cmd.children.append(cmd)
        return self

    def run(self) -> int:
        """Runs Application lifecycle

        Returns:
            Numeric result code
        """
        inputl = sys.argv[1:]
        cmd, opts, cmdpath = self.root_cmd.process(inputl, set())
        args = [x for x in inputl if x not in cmdpath]
        values, args = Values.from_opts_args(list(opts), args)
        cpath = [self.root_cmd.name, *cmdpath]
        if len(args) != 0:
            self.__messager.show_error(
                cmd, cpath, f"unrecognized command or option: {args}"
            )
            return 1
        if values.get(self.opt_help):
            self.__messager.show_help(cmd, cpath)
            return 0
        rc = cmd.exec(values)
        return rc
