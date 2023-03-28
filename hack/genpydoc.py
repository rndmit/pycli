import sys, os
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer

def generate(dest: str, module_names: list[str]):
    pm = PydocMarkdown()
    assert isinstance(pm.loaders[0], PythonLoader)
    assert isinstance(pm.renderer, MarkdownRenderer)

    pm.loaders[0].search_path = ["../pycli"]
    pm.loaders[0].modules = module_names
    pm.renderer.insert_header_anchors = False

    modules = pm.load_modules()
    pm.process(modules)

    with open(os.path.join(dest, os.extsep.join(["api", "md"])), "w+") as result:
        pm.renderer.render_single_page(result, modules) 

if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2:])
