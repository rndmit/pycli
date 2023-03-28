from typing import ClassVar, Self, Generic, TypeVar, Type, Optional, Tuple, cast
from typing import get_args as get_type_args
from collections.abc import Iterable


T = TypeVar("T")


class IncompatibleTypingErr(Exception):
    pass


class MissingRequiredOptionErr(Exception):
    pass


class UnableToParseErr(Exception):
    pass


class NotEnoughOptValuesErr(Exception):
    pass


class Option(Generic[T]):
    """Option represents an Option for your Command
    """
    name: ClassVar[str]
    flags: ClassVar[list[str]]
    help: ClassVar[str]
    default: ClassVar[T]
    nargs: ClassVar[str | int]
    is_flag: ClassVar[bool]
    required: ClassVar[bool]

    def __init__(
        self,
        name: str,
        flags: list[str] = None,
        help: str = "",
        default: T = None,
        nargs: str | int = 1,
        is_flag: bool = False,
        required: bool = False,
    ):
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
        ret_t = get_type_args(self.__orig_class__)[0]
        if self.is_flag and not (ret_t == bool):
            raise IncompatibleTypingErr("flag option couldn't be other type than bool")
        if self.nargs > 1 and not isinstance(ret_t, Iterable):
            raise IncompatibleTypingErr(
                "option takes more than 1 arg but it's type not iterable"
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

    def extract_value(self, idx: int, inputl: list[str]) -> Tuple[T, list[str]]:
        def remove(l: list, idx: int):
            return l[:idx] + l[idx+1 :]

        ret_t = get_type_args(self.__orig_class__)[0]
        if self.is_flag:
            return True, remove(inputl, idx)
        if self.nargs == 1:
            return ret_t(inputl[idx + 1]), remove(inputl, idx)
        # TODO: Add support for +/?
        if type(self.nargs) == str:
            raise Exception("Not implemented yet")
        result, result_t = ret_t(), ret_t.__args__[0]
        for pos in range(idx + 1, idx + self.nargs + 1):
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
        del inputl[idx:idx + self.nargs + 1]
        return result, inputl

    @staticmethod
    def extract_boolean(val) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            val = val.lower()
            if val == "true" or val == "yes":
                return True
            elif val == "false" or val =="no":
                return False
        raise Exception(f"unable to convert {val} to bool")
        