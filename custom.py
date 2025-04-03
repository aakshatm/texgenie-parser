import mistune
from rich.tree import Tree

def build_tree_mistune(tokens, parent):
    for token in tokens:
        if isinstance(token, dict) and "type" in token:
            node = parent.add(f"[bold]{token['type']}[/bold]")
            if "children" in token:
                build_tree_mistune(token["children"], node)

def markdown_to_tree_mistune(md_text):
    parser = mistune.create_markdown(renderer=mistune.AstRenderer())
    tokens = parser(md_text)
    root = Tree("Markdown Document")
    build_tree_mistune(tokens, root)
    return root

md_text = """# Title
## Subtitle
- Item 1
- Item 2
  - Subitem 2.1
"""
print(markdown_to_tree_mistune(md_text))
