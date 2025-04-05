import mistune
import sys
from mistune import HTMLRenderer

class LaTeXRenderer(HTMLRenderer):
    """
    A Mistune renderer that converts Markdown to LaTeX.
    """
    
    def __init__(self):
        super(LaTeXRenderer, self).__init__()
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
        # Skip escaping for these elements as they're handled in their respective methods
        self.skip_escape = ('math', 'block_code', 'inline_code')
        
    def text(self, text):
        """Escape LaTeX special characters in text"""
        for char, escaped in self.escape_chars.items():
            text = text.replace(char, escaped)
        return text
    
    def paragraph(self, text):
        """Convert a paragraph"""
        return f"{text}\n\n"
    
    def heading(self, text, level):
        """Convert headings"""
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
    
    def thematic_break(self):
        """Convert horizontal rule"""
        return "\\rule{\\textwidth}{0.4pt}\n\n"
    
    def block_text(self, text):
        """Generic block text handler"""
        return text
    
    def block_code(self, code, info=None):
        """Convert code blocks"""
        return f"\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}\n\n"
    
    def block_quote(self, text):
        """Convert block quotes"""
        return f"\\begin{{quotation}}\n{text}\\end{{quotation}}\n\n"
    
    def list(self, text, ordered, level=None):
        """Convert lists"""
        env = "enumerate" if ordered else "itemize"
        return f"\\begin{{{env}}}\n{text}\\end{{{env}}}\n\n"
    
    def list_item(self, text, level=None):
        """Convert list items"""
        return f"\\item {text}\n"
    
    def emphasis(self, text):
        """Convert italics"""
        return f"\\textit{{{text}}}"
    
    def strong(self, text):
        """Convert bold text"""
        return f"\\textbf{{{text}}}"
    
    def inline_code(self, code):
        """Convert inline code"""
        # Remove special characters from code
        for char, escaped in self.escape_chars.items():
            code = code.replace(char, escaped)
        return f"\\texttt{{{code}}}"
    
    def link(self, link, title, text):
        """Convert links"""
        if title:
            return f"\\href{{{link}}}{{{text}}} ({title})"
        return f"\\href{{{link}}}{{{text}}}"
    
    # def image(self, src, alt="", title=None):
    #     """Convert images"""
    #     caption = alt if alt else (title if title else "")
    #     return f"""\\begin{{figure}}
    # \\centering
    # \\includegraphics[width=0.8\\textwidth]{{{src}}}
    # \\caption{{{caption}}}
    # \\end{{figure}}
    # """
    
    def table(self, header, body):
        """Convert tables"""
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
    
    def table_row(self, content):
        """Convert table rows"""
        return f"{content} \\\\ \\hline\n"
    
    def table_cell(self, content, align=None, is_head=False):
        """Convert table cells"""
        if is_head:
            content = f"\\textbf{{{content}}}"
        return f"{content} & "
        
    def strikethrough(self, text):
        """Convert strikethrough text"""
        return f"\\sout{{{text}}}"
    
    def math(self, text):
        """Keep math expressions intact"""
        return f"${text}$"
    
    def codespan(self, text):
        """Alternative method for inline code"""
        return self.inline_code(text)
    
    def linebreak(self):
        """Convert line breaks"""
        return "\\\\\n"

    def newline(self):
        """Handle newlines"""
        return "\n"


def markdown_to_latex(markdown_text):
    """
    Convert markdown text to LaTeX using Mistune.
    
    Args:
        markdown_text (str): The markdown text to convert
        
    Returns:
        str: The converted LaTeX text
    """
    # Create the renderer and parser
    renderer = LaTeXRenderer()
    markdown_parser = mistune.create_markdown(renderer=renderer)
    
    # Parse and convert the markdown
    latex_content = markdown_parser(markdown_text)
    
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
        print(f"Error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python mistune_md_to_latex.py input.md output.tex")
    #     sys.exit(1)
    
    input_file = 'testingFilesWithMdFiles/org-mdfiles/Hybrid-modified/2.md'
    output_file = 'output2.tex'
    
    if not process_file(input_file, output_file):
        sys.exit(1)