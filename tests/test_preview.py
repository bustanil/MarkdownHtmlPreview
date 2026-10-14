import importlib.util
from pathlib import Path
import re
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_plugin():
    sublime = types.ModuleType("sublime")
    sublime.version = lambda: "4180"
    sublime.Region = lambda start, end: (start, end)
    sublime.error_message = lambda message: (_ for _ in ()).throw(AssertionError(message))
    sublime_plugin = types.ModuleType("sublime_plugin")
    sublime_plugin.TextCommand = object
    spec = importlib.util.spec_from_file_location("preview_under_test", ROOT / "MarkdownHtmlPreview.py")
    plugin = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"sublime": sublime, "sublime_plugin": sublime_plugin}):
        spec.loader.exec_module(plugin)
    return plugin


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.plugin = load_plugin()

    def test_bundled_html_matches_source_assets(self):
        expected = (ROOT / "src/index.html").read_text(encoding="utf-8")
        expected = expected.replace("%%%CSS%%%", (ROOT / "dist/md.css").read_text(encoding="utf-8"))
        expected = expected.replace("%%%JS%%%", (ROOT / "dist/md.js").read_text(encoding="utf-8"))
        self.assertEqual(self.plugin.html, expected)
        self.assertEqual((ROOT / "dist/index.html").read_text(encoding="utf-8"), expected)

    def test_style_does_not_modify_the_renderer_script(self):
        document = self.plugin.generate_preview("# Reading preview")
        scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", document, re.S)
        self.assertEqual(scripts, [(ROOT / "dist/md.js").read_text(encoding="utf-8")])
        styles = re.findall(r"<style>(.*?)</style>", document, re.S)
        self.assertEqual(styles, [(ROOT / "dist/md.css").read_text(encoding="utf-8")])

    def test_markdown_unicode_and_angle_brackets_reach_the_page(self):
        document = self.plugin.generate_preview("# Café\n\n`<tag>`")
        self.assertIn("<pre># Café\n\n`&lt;tag&gt;`</pre>", document)
        self.assertNotIn("%%%CONTENT%%%", document)

    def test_command_writes_html_and_opens_external_browser(self):
        markdown = "# Browser preview\n\nCafé"
        view = types.SimpleNamespace(size=lambda: len(markdown), substr=lambda region: markdown)
        command = self.plugin.markdown_html_preview_command()
        command.view = view
        with tempfile.TemporaryDirectory() as directory:
            original = self.plugin.tempfile.NamedTemporaryFile
            with patch.object(self.plugin.tempfile, "NamedTemporaryFile", side_effect=lambda **kw: original(dir=directory, **kw)):
                with patch.object(self.plugin.webbrowser, "open") as open_browser:
                    command.run(None)
            page = next(Path(directory).glob("*.html"))
            self.assertEqual(page.read_text(encoding="utf-8"), self.plugin.generate_preview(markdown))
            open_browser.assert_called_once_with("file://" + str(page))


if __name__ == "__main__":
    unittest.main()
