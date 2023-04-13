from abc import ABC, abstractmethod
from typing import ClassVar, Self, Tuple, Optional
from .option import Option


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
    def exec(self, opts: dict) -> int: 
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

    """Finds if subcommand with given name exists

    Arguments:
        name: name of subcommand
    """
    def find_child(self, name: str) -> Optional[Self]:
        if not hasattr(self, "children"):
            return None
        for child in self.children:
            if child.name == name:
                return child
        return None

    """Process inputl recursively above this command and it's subcommands

    Arguments:
        inputl: tuple of inputed strings
        collected_opts: set of Options which already found from Commands
        cmd_path: list of Commands before this
    """
    def process(self, inputl: Tuple[str], collected_opts: set[Option], cmd_path: list[str] = []) -> Tuple[Self, set[Option], Tuple[str]]:
        if hasattr(self, "opts") and self.opts:
            collected_opts.update(self.opts)
        if len(inputl) == 0:
            return self, collected_opts, cmd_path
        else:
            token = inputl[0]
            pc = self.find_child(token)
            if pc is None or token.startswith('"'):
                return self.process(inputl[1:], collected_opts)
            else:
                cmd_path.append(pc.name)
                return pc.process(inputl[1:], collected_opts)
