# pycli.app

App module

## Application Objects

```python
class Application(object)
```

Application is a first class entity which holds     root command of your CLI app. It handles all CLI application     lifecycle.

#### \_\_init\_\_

```python
def __init__(name: str = "",
             descr: str = None,
             global_opts: Tuple[Option] = None)
```

**Arguments**:

- `name` - application name (actually root command name)
- `descr` - discription of your application
- `global_opts` - Options which will be parsed with all commands

#### with\_commands

```python
def with_commands(*cmds: Command) -> Self
```

Registers Command within application's root command

**Arguments**:

- `*cmds` - one or more Command(-s) which should be registered

#### run

```python
def run(argv: list[str] = None) -> int
```

Runs Application lifecycle

**Returns**:

  Numeric result code

# pycli.command

Command module

## Command Objects

```python
class Command(ABC)
```

Command represents one command in your CLI app.

**Attributes**:

- `name` - name of command
- `short` - short description which shown in subcommands section
- `long` - long description which shown if help called directly
- `opts` - list of Options which Command supports
- `children` - subcommands of this Command

#### exec

```python
@abstractmethod
def exec(vals: Values) -> int
```

Command body

Accepts dict with options values

Should return result code (returned within application exit)

#### find\_child

```python
def find_child(name: str) -> Optional[Self]
```

Finds if subcommand with given name exists

**Arguments**:

- `name` - name of subcommand

#### process

```python
def process(inputl: Tuple[str],
            collected_opts: set[Option],
            cmd_path: list[str] = []) -> Tuple[Self, set[Option], Tuple[str]]
```

Process inputl recursively above this command and it's subcommands

**Arguments**:

- `inputl` - tuple of inputed strings
- `collected_opts` - set of Options which already found from Commands
- `cmd_path` - list of Commands before this

# pycli.option

Option module

## IncompatibleTypingErr Objects

```python
class IncompatibleTypingErr(Exception)
```

Raised when Option's type conflicts with attributes

## MissingRequiredOptionErr Objects

```python
class MissingRequiredOptionErr(Exception)
```

Raised when option marked as required but not presented in input

## UnableToParseErr Objects

```python
class UnableToParseErr(Exception)
```

Raised when input cannot be casted to Option's type

## NotEnoughOptValuesErr Objects

```python
class NotEnoughOptValuesErr(Exception)
```

Raised when input has more or less option values than required

## Option Objects

```python
class Option(Generic[T])
```

Option represents an Option for your Command

#### \_\_init\_\_

```python
def __init__(name: str,
             flags: list[str] = None,
             help: str = "",
             default: T = None,
             nargs: int | str = 1,
             is_flag: bool = False,
             required: bool = False,
             local: bool = False)
```

**Arguments**:

- `name` - option name
- `flags` - list of option's flags
- `help` - help string for option
- `default` - default value for option
- `nargs` - number of expected args or "+" (one or more)
- `is_flag` - indicates if option is flag (don't accept any values)
- `required` - indicates if option is required

#### process

```python
def process(inputl: list[str]) -> Tuple[Optional[T], list[str]]
```

Search Option's flag in inputl

#### extract\_value

```python
def extract_value(idx: int, inputl: list[str]) -> Tuple[T, list[str]]
```

Extract option value(-s) after given index

**Arguments**:

- `idx` - index of Option's flag
- `inputl` - list of input

#### extract\_boolean

```python
def extract_boolean(val: bool | str) -> bool
```

Extract bool value

# pycli.values

Values module

## Values Objects

```python
class Values(object)
```

Values object holds all options for current Command

