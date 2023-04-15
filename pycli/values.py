"""Values module
"""
from typing import Self, TypeVar, Tuple
from .option import Option


class ValueNotExistsErr(Exception):
    pass


class OptionNotExistsErr(Exception):
    pass


T = TypeVar("T")


class Values(object):
    """Values object holds all options for current Command"""

    __values: dict[Option, any] = dict()

    def __init__(self, opts: list[Option]) -> None:
        for opt in opts:
            self.__values[opt] = opt.default

    def get(self, opt: Option[T], strict: bool = False) -> T:
        try:
            return self.__values[opt]
        except KeyError:
            raise OptionNotExistsErr(
                f"option {opt.name} doesnt exist in this command context")

    def get_by_name(self, name: str, strict: bool = False) -> any:
        for opt, val in self.__values.items():
            if opt.name != name:
                continue
            return val
        if strict:
            raise ValueNotExistsErr(f"no option with name {name}")
        return None

    def resolve_opts(self, args: list[str]) -> Tuple[list[str]]:
        retargs = []
        opts = list(self.__values.keys())
        opts.sort(
            key=lambda x:
            (x.is_flag, x.nargs == "+", isinstance(x.nargs, int)),
            reverse=True,
        )
        for opt in opts:
            result, retargs = opt.process(args)
            if result is None:
                continue
            if retargs is None:
                break
            args = retargs
            self.__values[opt] = result
        return retargs

    @staticmethod
    def from_opts_args(opts: dict[str, any],
                       args: list[str]) -> Tuple[Self, list[str]]:
        v = Values(opts)
        retargs = v.resolve_opts(args)
        return v, retargs
