from pycli import Command
from .opts import custom_rc


class TestCommand(Command):
    name = "test"
    short = "command for usage with tests"
    long = "Empty command for usage with tests"

    def exec(self, vals):
        return 0
    
class TestCommandWithCustomRC(TestCommand):
    _opt_custom_rc = custom_rc

    def exec(self, vals):
        rc = vals.get(custom_rc)
        if rc:
            return rc
        return 0
    
class TestCommandWithSubcommand(TestCommand):
    class Subcommand(Command):
        name = "subtest"

        def exec(self, vals):
            return 0
        
    children = [Subcommand()]

    def exec(self, vals):
        return 0