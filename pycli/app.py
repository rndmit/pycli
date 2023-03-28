from typing import Tuple
import sys
import jinja2
from .command import Command
from .option import Option
from .output import Messager


class Application(object):
    """Application is a first class entity which holds \
    root command of your CLI app. It handles all CLI application \
    lifecycle.
    """
    class RootCommand(Command):
        opts = [
            Option[bool]("help", flags=["-h", "--help"], help="Get help for commands", is_flag=True)
        ]
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

    def __init__(self, name: str, descr: str = None, global_opts: Tuple[Option] = None):
        """
        Args:
            name: application name (actually root command name)
            descr: discription of your application (e.g. "tool for doing something"
            global_opts: Options which will be parsed with all commands
        """
        self.__messager = Messager(jinja2.FileSystemLoader("pycli/templates"))
        self.root_cmd = self.RootCommand(name, descr)

    def register(self, *cmds: Command):
        """Registers Command within application's root command

        Args:
            *cmds: one or more Command(-s) which should be registered
        """
        for cmd in cmds:
            self.root_cmd.children.append(cmd)

    def run(self) -> int:
        """Runs Application lifecycle

        Returns:
            Numeric result code
        """
        inputl = sys.argv[1:]
        ret = self.root_cmd.process(inputl, set())
        resolved_opts = {}
        inputlf = [x for x in inputl if x not in ret[2]]
        for i in ret[1]:
            r = i.process(inputlf)
            if r is None:
                continue
            if r[1] is not None:
                inputlf = r[1]
            if r is not None:
                resolved_opts[i.name] = r[0]
        if len(inputlf) != 0:
            self.__messager.show_error(ret[0], f"unrecognized command or option: {inputlf}")
            return 1
        if resolved_opts['help']:
            self.__messager.show_help(ret[0])
            return 0
        rc = ret[0].exec(resolved_opts)
        return rc