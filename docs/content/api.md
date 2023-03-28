# pycli.app

## Application Objects

```python
class Application(object)
```

Application is a first class entity which holds     root command of your CLI app. It handles all CLI application     lifecycle.

#### \_\_init\_\_

```python
def __init__(name: str, descr: str = None, global_opts: Tuple[Option] = None)
```

**Arguments**:

- `name` - application name (actually root command name)
- `descr` - discription of your application (e.g. "tool for doing something"
- `global_opts` - Options which will be parsed with all commands

#### register

```python
def register(*cmds: Command)
```

Registers Command within application's root command

**Arguments**:

- `*cmds` - one or more Command(-s) which should be registered

#### run

```python
def run() -> int
```

Runs Application lifecycle

**Returns**:

  Numeric result code

# pycli.command

## Command Objects

```python
class Command(ABC)
```

Command represents one command in your CLI app.

# pycli.option

## Option Objects

```python
class Option(Generic[T])
```

Option represents an Option for your Command

