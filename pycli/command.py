from abc import ABC, abstractmethod
from typing import ClassVar, Self, Tuple, Optional
import re
from .option import Option


class Command(ABC):
    """Command represents one command in your CLI app.
    """
    name: ClassVar[str]
    short: ClassVar[str]
    long: ClassVar[str]
    opts: ClassVar[list[Option]]
    children: ClassVar[dict[str, Self]]

    @abstractmethod
    def exec(self, opts: dict) -> int: ...

    def __init_subclass__(cls):
        if not hasattr(cls, "name"):
            cls.name = cls.__name__.lower()
        if not hasattr(cls, "short"):
            cls.short = ""
        if not hasattr(cls, "long"):
            cls.long = ""

    def find_child(self, name: str) -> Optional[Self]:
        if not hasattr(self, "children"):
            return None
        for child in self.children:
            if child.name == name:
                return child

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
