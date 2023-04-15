"""Command module
"""
from abc import ABC, abstractmethod
from typing import ClassVar, Self, Tuple, Optional
from .option import Option
from .values import Values


class Command(ABC):
    """Command represents one command in your CLI app.

    Attributes:
        name: name of command
        short: short description which shown in subcommands section
        long: long description which shown if help called directly
        opts: list of Options which Command supports
        children: subcommands of this Command
    """

    name: ClassVar[str]
    short: ClassVar[str]
    long: ClassVar[str]
    opts: ClassVar[list[Option]]
    children: ClassVar[list[Self]]

    @abstractmethod
    def exec(self, vals: Values) -> int:
        """Command body

        Accepts dict with options values

        Should return result code (returned within application exit)
        """
        ...

    def __init_subclass__(cls):
        if not hasattr(cls, "name"):
            cls.name = cls.__name__.lower()
        if not hasattr(cls, "short"):
            cls.short = ""
        if not hasattr(cls, "long"):
            cls.long = ""
        if not hasattr(cls, "opts"):
            cls.opts = []
        defined_opts = [
            cls.__dict__[i] for i in cls.__dict__.keys() if i[:5] == "_opt_"
        ]
        for dopt in defined_opts:
            if dopt in cls.opts:
                raise Exception(
                    f"opt {dopt.name} defined both in class and opts list")
            dopt.local = True
            cls.opts.append(dopt)

    def find_child(self, name: str) -> Optional[Self]:
        """Finds if subcommand with given name exists

        Arguments:
            name: name of subcommand
        """
        if not hasattr(self, "children"):
            return None
        for child in self.children:
            if child.name == name:
                return child
        return None

    def process(
            self,
            inputl: Tuple[str],
            collected_opts: set[Option],
            cmd_path: list[str] = []) -> Tuple[Self, set[Option], Tuple[str]]:
        """Process inputl recursively above this command and it's subcommands

        Arguments:
            inputl: tuple of inputed strings
            collected_opts: set of Options which already found from Commands
            cmd_path: list of Commands before this
        """
        if hasattr(self, "opts") and self.opts:
            collected_opts.update(self.opts)
        if len(inputl) == 0:
            self.opts = collected_opts
            return self, collected_opts, cmd_path
        else:
            token = inputl[0]
            pc = self.find_child(token)
            if pc is None or token.startswith('"'):
                return self.process(inputl[1:], collected_opts, cmd_path)
            else:
                cmd_path.append(pc.name)
                return pc.process(
                    inputl[1:],
                    set([o for o in collected_opts if not o.local]),
                    cmd_path,
                )
