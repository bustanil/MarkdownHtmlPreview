"""Rebuild the preview layout using the existing bundled renderer."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build():
    # The first line contains upstream's bundled GitHub Markdown styles.
    # Keep those styles and the bundled JavaScript at their existing versions.
    base_css = (ROOT / "dist/md.css").read_text(encoding="utf-8").split("\n", 1)[0]
    if not base_css.startswith(".markdown-body"):
        raise ValueError("The bundled base stylesheet changed. Review it before rebuilding.")
    css = base_css + "\n" + (ROOT / "src/main.css").read_text(encoding="utf-8")
    javascript = (ROOT / "dist/md.js").read_text(encoding="utf-8")
    document = (ROOT / "src/index.html").read_text(encoding="utf-8")
    document = document.replace("%%%CSS%%%", css).replace("%%%JS%%%", javascript)
    template = (ROOT / "src/MarkdownHtmlPreview.py").read_text(encoding="utf-8")
    escaped = document.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    module = template.replace("%%%HTML%%%", escaped)
    tree = ast.parse(module)
    embedded = next(
        ast.literal_eval(node.value) for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "html" for target in node.targets)
    )
    if embedded != document:
        raise ValueError("The generated Python template does not preserve the HTML.")
    (ROOT / "dist/md.css").write_text(css, encoding="utf-8")
    (ROOT / "dist/index.html").write_text(document, encoding="utf-8")
    (ROOT / "MarkdownHtmlPreview.py").write_text(module, encoding="utf-8")
    print("Rebuilt dist/md.css, dist/index.html, and MarkdownHtmlPreview.py.")


if __name__ == "__main__":
    build()
