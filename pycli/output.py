"""Output module
"""
from rich.console import Console
import jinja2
from .command import Command


class Messager(object):
    console: Console
    template_engine: jinja2.Environment

    def __init__(self, templates: jinja2.BaseLoader) -> None:
        self.console = Console()
        self.template_engine = jinja2.Environment(loader=templates)

    def show_help(self, cmd: Command, cpath: list[str]):
        self.console.print(
            self.template_engine.get_template("help.j2").render(cmd=cmd, cpath=cpath)
        )

    def show_error(self, cmd: Command, cpath: list[str], errmsg: str):
        self.console.print(
            self.template_engine.get_template("error.j2").render(
                cmd=cmd, errmsg=errmsg, cpath=cpath
            )
        )
