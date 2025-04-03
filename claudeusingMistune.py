import mistune
import sys
import re
from html.parser import HTMLParser

class HTMLTableParser(HTMLParser):
    """HTML Parser specifically for tables to convert them to LaTeX format"""
    
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_thead = False
        self.in_tbody = False
        self.in_tr = False
        self.in_th = False
        self.in_td = False
        
        self.current_cell_content = []
        self.current_row = []
        self.header_rows = []
        self.body_rows = []
        
        self.column_count = 0
        
    def handle_starttag(self, tag, attrs):
        """Handle HTML start tags"""
        tag = tag.lower()
        
        if tag == 'table':
            self.in_table = True
        elif tag == 'thead':
            self.in_thead = True
        elif tag == 'tbody':
            self.in_tbody = True
        elif tag == 'tr':
            self.in_tr = True
            self.current_row = []
        elif tag == 'th':
            self.in_th = True
            self.current_cell_content = []
        elif tag == 'td':
            self.in_td = True
            self.current_cell_content = []
    
    def handle_endtag(self, tag):
        """Handle HTML end tags"""
        tag = tag.lower()
        
        if tag == 'table':
            self.in_table = False
        elif tag == 'thead':
            self.in_thead = False
        elif tag == 'tbody':
            self.in_tbody = False
        elif tag == 'tr':
            self.in_tr = False
            if self.in_thead:
                self.header_rows.append(self.current_row)
            else:
                self.body_rows.append(self.current_row)
            
            # Track the maximum column count
            self.column_count = max(self.column_count, len(self.current_row))
            
        elif tag == 'th':
            self.in_th = False
            self.current_row.append(''.join(self.current_cell_content).strip())
        elif tag == 'td':
            self.in_td = False
            self.current_row.append(''.join(self.current_cell_content).strip())
    
    def handle_data(self, data):
        """Handle text content"""
        if self.in_th or self.in_td:
            self.current_cell_content.append(data)
    
    def to_latex(self):
        """Convert the parsed HTML table to LaTeX format"""
        if not self.header_rows and not self.body_rows:
            return ""
            
        # Create column specification
        col_spec = '|' + 'c|' * self.column_count
        
        latex_table = f"\\begin{{table}}\n\\centering\n\\begin{{tabular}}{{{col_spec}}}\n\\hline\n"
        
        # Add header rows
        for row in self.header_rows:
            padded_row = row + [''] * (self.column_count - len(row))
            formatted_cells = [f"\\textbf{{{cell}}}" for cell in padded_row]
            latex_table += ' & '.join(formatted_cells) + " \\\\ \\hline\n"
        
        # Add body rows
        for row in self.body_rows:
            padded_row = row + [''] * (self.column_count - len(row))
            latex_table += ' & '.join(padded_row) + " \\\\ \\hline\n"
        
        latex_table += "\\end{tabular}\n\\end{table}\n\n"
        return latex_table


class LaTeXRenderer(mistune.HTMLRenderer):
    """
    A Mistune renderer that converts Markdown to LaTeX.
    """
    
    def __init__(self):
        super().__init__()
        self.escape_chars = {
            '&': '\\&', 
            '%': '\\%', 
            '$': '\\$', 
            '#': '\\#', 
            '_': '\\_', 
            '{': '\\{', 
            '}': '\\}', 
            '~': '\\textasciitilde{}',
            '^': '\\textasciicircum{}',
            '\\': '\\textbackslash{}',
        }
        
    def text(self, token, state):
        """Escape LaTeX special characters in text"""
        print(f"Rendering text: {token.content}")
        text = token["content"]
        for char, escaped in self.escape_chars.items():
            text = text.replace(char, escaped)
        return text
    
    def paragraph(self, token, state):
        """Convert a paragraph"""
        print("hello");
        text = self.render_children(token, state)
        # Check if the paragraph contains an HTML table
        if text.strip().startswith('<table') and text.strip().endswith('</table>'):
            parser = HTMLTableParser()
            parser.feed(text)
            return parser.to_latex()
        return f"{text}\n\n"
    
    def heading(self, token, state):
        """Convert headings"""
        text = self.render_children(token, state)
        level = token.attrs.get('level')
        if level == 1:
            return f"\\section{{{text}}}\n\n"
        elif level == 2:
            return f"\\subsection{{{text}}}\n\n"
        elif level == 3:
            return f"\\subsubsection{{{text}}}\n\n"
        elif level == 4:
            return f"\\paragraph{{{text}}}\n\n"
        else:  # level == 5 or 6
            return f"\\subparagraph{{{text}}}\n\n"
    
    def thematic_break(self, token, state):
        """Convert horizontal rule"""
        return "\\rule{\\textwidth}{0.4pt}\n\n"
    
    def block_text(self, token, state):
        """Generic block text handler"""
        return self.render_children(token, state)
    
    def block_code(self, token, state):
        """Convert code blocks"""
        code = token.attrs.get('code', '')
        info = token.attrs.get('info', '')
        return f"\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}\n\n"
    
    def block_quote(self, token, state):
        """Convert block quotes"""
        text = self.render_children(token, state)
        return f"\\begin{{quotation}}\n{text}\\end{{quotation}}\n\n"
    
    def list(self, token, state):
        """Convert lists"""
        text = self.render_children(token, state)
        ordered = token.attrs.get('ordered', False)
        env = "enumerate" if ordered else "itemize"
        return f"\\begin{{{env}}}\n{text}\\end{{{env}}}\n\n"
    
    def list_item(self, token, state):
        """Convert list items"""
        text = self.render_children(token, state)
        return f"\\item {text}\n"
    
    def strong(self, token, state):
        """Convert bold text"""
        text = self.render_children(token, state)
        return f"\\textbf{{{text}}}"
    
    def emphasis(self, token, state):
        """Convert italics"""
        text = self.render_children(token, state)
        return f"\\textit{{{text}}}"
    
    def codespan(self, token, state):
        """Alternative method for inline code"""
        code = token.content
        # Remove special characters from code
        for char, escaped in self.escape_chars.items():
            code = code.replace(char, escaped)
        return f"\\texttt{{{code}}}"
    
    def link(self, token, state):
        """Convert links"""
        url = token.attrs.get('url', '')
        title = token.attrs.get('title', '')
        text = self.render_children(token, state)
        
        if title:
            return f"\\href{{{url}}}{{{text}}} ({title})"
        return f"\\href{{{url}}}{{{text}}}"
    
    def image(self, token, state):
        """Convert images"""
        url = token.attrs.get('url', '')
        alt = token.attrs.get('alt', '')
        title = token.attrs.get('title', '')
        
        caption = alt if alt else (title if title else "")
        return f"""\\begin{{figure}}
\\centering
\\includegraphics[width=0.8\\textwidth]{{{url}}}
\\caption{{{caption}}}
\\end{{figure}}
"""
    
    def table(self, token, state):
        """Convert standard Markdown tables"""
        header = self.render_children(token.children[0], state)
        body = ''
        for child in token.children[1:]:
            body += self.render(child, state)
            
        # Count columns based on header
        columns = len(header.split('&')) if header else 1
        col_spec = '|' + 'c|' * columns
        
        return f"""\\begin{{table}}
\\centering
\\begin{{tabular}}{{{col_spec}}}
\\hline
{header}\\hline
{body}\\end{{tabular}}
\\end{{table}}
"""
    
    def table_row(self, token, state):
        """Convert table rows"""
        content = self.render_children(token, state)
        return f"{content} \\\\ \\hline\n"
    
    def table_cell(self, token, state):
        """Convert table cells"""
        content = self.render_children(token, state)
        is_head = token.attrs.get('head', False)
        if is_head:
            content = f"\\textbf{{{content}}}"
        return f"{content} & "
        
    def strikethrough(self, token, state):
        """Convert strikethrough text"""
        text = self.render_children(token, state)
        return f"\\sout{{{text}}}"
    
    def linebreak(self, token, state):
        """Convert line breaks"""
        return "\\\\\n"

    def newline(self, token, state):
        """Handle newlines"""
        return "\n"

    def html_block(self, token, state):
        """Handle HTML blocks - particularly useful for tables"""
        html = token.content
        # Check if the HTML block is a table
        if html.strip().startswith('<table') and html.strip().endswith('</table>'):
            parser = HTMLTableParser()
            parser.feed(html)
            return parser.to_latex()
        # For other HTML, just pass it through (or optionally handle it differently)
        return f"% HTML content (not converted): {html.strip()}\n\n"
        
    def inline_html(self, token, state):
        """Handle inline HTML"""
        return token.content


def preprocess_markdown(markdown_text):
    """
    Preprocess markdown text to handle HTML tables that might be broken across multiple lines.
    This ensures that the entire table is treated as a single block.
    """
    # Use regex to find all HTML tables and their contents (even across multiple lines)
    table_pattern = re.compile(r'<table.*?</table>', re.DOTALL)
    
    # Process the document to combine table elements
    processed_text = markdown_text
    
    return processed_text


def markdown_to_latex(markdown_text):
    """
    Convert markdown text to LaTeX using Mistune.
    
    Args:
        markdown_text (str): The markdown text to convert
        
    Returns:
        str: The converted LaTeX text
    """
    # Preprocess markdown to handle HTML tables
    preprocessed_markdown = preprocess_markdown(markdown_text)
    
    # Create the renderer and parser
    renderer = LaTeXRenderer()
    markdown = mistune.create_markdown(renderer=renderer)
    
    # Parse and convert the markdown
    latex_content = markdown(preprocessed_markdown)
    
    # Add LaTeX document structure
    latex_preamble = "\\documentclass{article}\n" \
                     "\\usepackage{hyperref}\n" \
                     "\\usepackage{graphicx}\n" \
                     "\\usepackage{amsmath}\n" \
                     "\\usepackage{amssymb}\n" \
                     "\\usepackage{ulem}  % For strikethrough\n" \
                     "\\begin{document}\n\n"
    
    latex_ending = "\n\\end{document}"
    
    return latex_preamble + latex_content + latex_ending


def process_file(input_file, output_file):
    """Process a markdown file and output LaTeX"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        latex_content = markdown_to_latex(markdown_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    # print(len(sys.argv))
    # if len(sys.argv) != 3:
    #     print("Usage: python mistune_md_to_latex.py input.md output.tex")
    #     sys.exit(1)
    
    input_file = 'testingFilesWithMdFiles/org-mdfiles/Hybrid-modified/2.md'
    output_file = 'output2.tex'
    
    if not process_file(input_file, output_file):
        sys.exit(1)