# Markdown HTML Preview

Render the current Markdown buffer as HTML and open it in your default browser.

This fork of [zeyon/MarkdownHtmlPreview](https://github.com/zeyon/MarkdownHtmlPreview) includes a reading layout:

- A centered column with a maximum width of 760 px.
- An 18 px system font with a line height of 1.75.
- A dim, warm gray background (`#eeede9`).
- Muted backgrounds for code blocks and tables.
- Horizontal scrolling for wide code blocks and tables.
- A layout that fits small screens.
- A white background for printing.

The style is embedded in the generated HTML. It does not need a separate installed stylesheet or network requests.

## Install the fork

1. In Sublime Text, select **Preferences > Browse Packages**.
2. Quit Sublime Text.
3. If that folder already contains `Markdown HTML Preview`, move it outside the Packages folder as a backup. This includes any local style overrides you installed previously.
4. Clone this fork into a folder named `Markdown HTML Preview` inside Packages:

   ```sh
   git clone https://github.com/bustanil/MarkdownHtmlPreview.git "Markdown HTML Preview"
   ```

5. Start Sublime Text.

Loose package files take priority over the original installed package archive. Keep the Git checkout to update the fork with `git pull`. Package Control updates to the original archive do not update this fork.

## Use the preview

Open a Markdown file. Open the command palette and run **Markdown HTML Preview**. The default shortcut is **Ctrl+Shift+M**.

Each command creates a new temporary HTML file and opens your default browser. Regenerate the preview after editing Markdown or changing the style. Refreshing an existing HTML page does not rebuild it.

## Change the style

Edit the reading layout in `src/main.css`. Change `--reading-width` to adjust the column width and `--reading-background` to adjust the page color.

Rebuild the bundled preview with Python 3:

```sh
python3 scripts/build_reading_style.py
```

This command updates:

- `dist/md.css`
- `dist/index.html`
- `MarkdownHtmlPreview.py`

The script preserves the existing bundled GitHub Markdown CSS and JavaScript renderer. It does not rebuild JavaScript from `src/main.js`. The upstream Gulp/Bower build files remain available for renderer changes.

Run the checks with:

```sh
python3 -m unittest discover -s tests
```

## Compatibility

The upstream plugin targets Sublime Text 2/3. The approved reading style was verified through a local override in Sublime Text 4 on macOS and in Firefox. This fork's generated files pass local rendering-command and build-consistency checks. A fresh installation of the fork, Sublime Text 2, and other operating systems have not been verified.

Relative links and images still use the temporary HTML file's directory. This fork changes the reading style and retains the upstream rendering behavior.

## License

The upstream MIT license applies. See `LICENSE`.

Copyright (c) 2014 Peter-Christoph Haider.
