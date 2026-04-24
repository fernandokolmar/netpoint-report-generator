"""Writes HTML reports to disk and opens them in the default browser."""


def export_html(html_content: str, output_path: str) -> str:
    """Writes HTML to file. Returns output_path."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_path


def open_in_browser(html_path: str) -> None:
    """Opens the HTML file in the default browser."""
    import webbrowser
    webbrowser.open(f'file:///{html_path.replace(chr(92), "/")}')
