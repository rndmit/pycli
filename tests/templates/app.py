from pycli import Application


def create_test_app(name = "test app", descr = None, global_opts = None):
    return Application(name, descr, global_opts)