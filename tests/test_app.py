import pytest
from pycli import Application
from . import templates as t


def test_empty_app():
    app = t.create_test_app()
    assert app.root_cmd.name == "test app"
    assert app.root_cmd.long == None
    rc = app.run([])
    assert rc == 0
    rc = app.run(["not-existing-command"])
    assert rc == 1


def test_app_with_commands():
    app = t.create_test_app().with_commands(t.cmds.TestCommand())
    assert isinstance(app.root_cmd.children[0], t.cmds.TestCommand)
    rc = app.run(["test"])
    assert rc == 0
    rc = app.run(["rest"])
    assert rc == 1
    rc = app.run("test and rest".split(" "))
    assert rc == 1


def test_app_with_opts():
    app = t.create_test_app().with_commands(t.cmds.TestCommandWithCustomRC())
    rc = app.run(["test"])
    assert rc == 0
    rc = app.run("test --rc 42".split(" "))
    assert rc == 42
    rc = app.run("test --idk".split(" "))
    assert rc == 1
    rc = app.run("test --idk --rc 42".split(" "))
    assert rc == 1


def test_app_with_subcommands():
    app = t.create_test_app().with_commands(t.cmds.TestCommandWithSubcommand())
    assert app.root_cmd.children[0].children is not None
    rc = app.run(["test"])
    assert rc == 0
    rc = app.run("test subtest".split(" "))
    assert rc == 0
    rc = app.run("test subrest".split(" "))
    assert rc == 1