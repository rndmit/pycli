"""Option module
"""
from typing import ClassVar, Self, Generic, TypeVar, Type, Optional, Tuple, cast
from typing import get_args as get_type_args
from collections.abc import Iterable
import re


class IncompatibleTypingErr(Exception):
    """Raised when Option's type conflicts with attributes"""

    pass


class MissingRequiredOptionErr(Exception):
    """Raised when option marked as required but not presented in input"""

    pass


class UnableToParseErr(Exception):
    """Raised when input cannot be casted to Option's type"""

    pass


class NotEnoughOptValuesErr(Exception):
    """Raised when input has more or less option values than required"""

    pass


T = TypeVar("T")


class Option(Generic[T]):
    """Option represents an Option for your Command"""

    name: ClassVar[str]
    flags: ClassVar[list[str]]
    help: ClassVar[str]
    default: ClassVar[T]
    nargs: ClassVar[int | str]
    is_flag: ClassVar[bool]
    required: ClassVar[bool]

    def __init__(
        self,
        name: str,
        flags: list[str] = None,
        help: str = "",
        default: T = None,
        nargs: int | str = 1,
        is_flag: bool = False,
        required: bool = False,
    ):
        """
        Args:
            name: option name
            flags: list of option's flags
            help: help string for option
            default: default value for option
            nargs: number of expected args or "+" (one or more)
            is_flag: indicates if option is flag (don't accept any values)
            required: indicates if option is required
        """
        self.name = name
        if flags is None:
            self.flags = [f"--{self.name}"]
        else:
            self.flags = flags
        self.help = help
        self.default = default
        self.nargs = nargs
        self.is_flag = is_flag
        if self.is_flag:
            self.nargs = 0
        self.required = required

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def process(self, inputl: list[str]) -> Tuple[Optional[T], list[str]]:
        """Search Option's flag in inputl"""
        ret_t = get_type_args(self.__orig_class__)[0]
        if self.is_flag and not (ret_t == bool):
            raise IncompatibleTypingErr("flag option couldn't be other type than bool")
        if isinstance(self.nargs, int) and self.nargs > 1 and not isinstance(ret_t, Iterable):
            raise IncompatibleTypingErr(
                f"option {self.name} has {self.nargs} nargs property but it's type not iterable"
            )
        if isinstance(self.nargs, str) and self.nargs == "+" and not isinstance(ret_t, Iterable):
            raise IncompatibleTypingErr(
                f"option {self.name} has {self.nargs} nargs property but it's type not iterable"
            )
        for flag in self.flags:
            try:
                pos = inputl.index(flag)
                return self.extract_value(pos, inputl)
            except ValueError:
                continue
        if self.required:
            raise MissingRequiredOptionErr(self.name)
        if self.is_flag:
            return False, inputl
        if self.default:
            return self.default, inputl
        return None, inputl

    def extract_value(self, idx: int, inputl: list[str]) -> Tuple[T, list[str]]:
        """Extract option value(-s) after given index

        Arguments:
            idx: index of Option's flag
            inputl: list of input
        """

        def remove(l: list, idx: int, count=0):
            del l[idx : idx + count + 1]
            return l

        ret_t = get_type_args(self.__orig_class__)[0]
        if self.is_flag:
            return True, remove(inputl, idx)
        if self.nargs == 1:
            return ret_t(inputl[idx + 1]), remove(inputl, idx, 1)
        valoffset = self.nargs
        if isinstance(self.nargs, str) and self.nargs == "+":
            valoffset = 0
            for pos in inputl[idx + 1:]:
                if re.match(r"-.*", pos):
                    break
                valoffset += 1 
        result, result_t = ret_t(), ret_t.__args__[0]
        for pos in range(idx + 1, idx + valoffset + 1):
            try:
                val = inputl[pos]
            except IndexError:
                raise NotEnoughOptValuesErr(f"excepting {self.nargs} values")
            if result_t == bool:
                result.append(self.extract_boolean(val))
                continue
            try:
                r = result_t(val)
            except:
                raise UnableToParseErr(f"unable to convert {val} to {result_t}")
            result.append(r)
        return result, remove(inputl, idx, valoffset)

    def extract_boolean(val: bool | str) -> bool:
        """Extract bool value"""
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            val = val.lower()
            if val == "true" or val == "yes":
                return True
            elif val == "false" or val == "no":
                return False
        raise Exception(f"unable to convert {val} to bool")
