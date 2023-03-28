import pytest
from pycli import Application


def test_new_app():
    a = Application("test app")
    assert a.root_cmd.name == "test app"

    with pytest.raises(TypeError) as e:
        a = Application()
    assert "missing 1 required positional argument: 'name'" in str(e.value)