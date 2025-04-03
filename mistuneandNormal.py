import mistune
import sys
import re
from mistune import HTMLRenderer
from bs4 import BeautifulSoup
import itertools

class LaTeXRenderer(HTMLRenderer):
    """
    A Mistune renderer that converts Markdown to LaTeX with enhanced support
    for equations, tables, and other elements.
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
        self.math_placeholders = {}
        self.math_counter = 0
        
    def text(self, text):
        """
        Escape LaTeX special characters in text and handle math expressions.
        """
        # Extract and preserve math expressions
        text, self.math_placeholders = self.extract_math_expressions(text)
        
        # Escape LaTeX special characters
        for char, escaped in self.escape_chars.items():
            text = text.replace(char, escaped)
            
        # Reinsert math expressions
        text = self.reinsert_math_expressions(text)
        return text
    
    def extract_math_expressions(self, text):
        """
        Extracts inline math expressions ($...$) and replaces them with placeholders.
        """
        math_patterns = re.findall(r'(?<!\\)(?<!\$)\$(.*?)(?<!\\)\$', text)
        placeholder_map = {}

        for math_expr in math_patterns:
            placeholder = f"@@MATH{self.math_counter}@@"
            self.math_counter += 1
            placeholder_map[placeholder] = math_expr
            text = text.replace(f"${math_expr}$", placeholder, 1)

        return text, placeholder_map
    
    def reinsert_math_expressions(self, text):
        """
        Restores math expressions from placeholders.
        """
        for placeholder, math_expr in self.math_placeholders.items():
            text = text.replace(placeholder, f"${math_expr}$")
        
        # Clear placeholders after using them
        self.math_placeholders = {}
        return text
    
    def paragraph(self, text):
        """Convert a paragraph"""
        return f"{text}\n\n"
    
    def heading(self, text, level):
        """Convert headings"""
        # Handle numbered headings like "3.2 Header Text"
        header_match = re.match(r'^(\d+(?:\.\d+)*\.?)\s+(.+)$', text)
        if header_match:
            section = header_match.group(1).rstrip('.')
            header_text = header_match.group(2).strip()
            
            # Count dots to determine section level
            dot_count = section.count('.')
            
            # Adjust level based on dot count
            if dot_count >= 2:
                level = 3
            elif dot_count == 1:
                level = 2
            else:
                level = 1
        
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
        """Convert code blocks with language specification"""
        if info and info.strip():
            # Using listings package for syntax highlighting
            return f"\\begin{{lstlisting}}[language={info.strip()}]\n{code}\n\\end{{lstlisting}}\n\n"
        else:
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
    
    # def image(self, url=None, src=None, alt="", title=None):
    #     """
    #     Convert images with advanced handling for figures and captions.
    #     Detects if the image has a caption (Fig. X) before or after.
    #     """
    #     # Use either url or src, whichever is provided
    #     image_source = url if url is not None else src
    #     caption = alt if alt else (title if title else "")
    #     image_output = ""
        
    #     # Check if there's a figure caption pattern in the alt or title
    #     caption_match = re.match(r'^(?:Fig\.?|Figure)\s+(\d+)[\.:]?\s+(.*)', caption)
    #     if caption_match:
    #         caption_number = caption_match.group(1)
    #         caption_text = caption_match.group(2)
            
    #         image_output = f"""\\begin{{figure}}[htbp]
    # \\centering
    # \\includegraphics[width=0.8\\linewidth]{{{image_source}}}
    # \\caption{{{caption_text}}}
    # \\label{{fig:{caption_number}}}
    # \\end{{figure}}
    # """
    #     else:
    #         image_output = f"""\\begin{{figure}}[htbp]
    # \\centering
    # \\includegraphics[width=0.8\\linewidth]{{{image_source}}}
    # """
    #         if caption:
    #             image_output += f"\\caption{{{caption}}}\n"
            
    #         image_output += "\\end{figure}\n"
        
    #     return image_output

    def table(self, header, body):
        """
        Convert tables with improved handling for complex table structures.
        """
        # Count columns based on header
        columns = len(header.split('&')) if header else 1
        col_spec = '|' + 'c|' * columns
        
        table_output = f"""\\begin{{table}}[htbp]
\\centering
\\begin{{tabular}}{{{col_spec}}}
\\hline
{header}\\hline
{body}\\end{{tabular}}
\\end{{table}}
"""
        return table_output
    
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
        """Process math expressions"""
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
    
    def process_block_equation(self, text):
        """
        Process a block equation ($$...$$) and convert it to LaTeX equation environment.
        """
        return f"\\begin{{equation}}\n{text}\n\\end{{equation}}\n\n"
    
    def process_html_table(self, html):
        """
        Process an HTML table and convert it to LaTeX tabular environment.
        """
        try:
            return self.html_table_to_latex(html)
        except Exception as e:
            # Fallback to verbatim if conversion fails
            return f"\\begin{{verbatim}}\n{html}\n\\end{{verbatim}}\n"
    
    def html_table_to_latex(self, html):
        """
        Convert an HTML table to LaTeX tabular format with support for merged cells.
        """
        try:
            array = self.html_table_to_2d_array(html)
            return self.array_to_latex(array)
        except Exception as e:
            # Fallback to verbatim
            return f"\\begin{{verbatim}}\n{html}\n\\end{{verbatim}}"
    
    def html_table_to_2d_array(self, html):
        """
        Convert an HTML table to a 2D array with handling for rowspan and colspan.
        """
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        
        max_cols = 0
        structured_rows = []
        
        # First pass: determine the number of columns
        for row in rows:
            cells = row.find_all(["td", "th"])
            col_count = sum(int(cell.get("colspan", 1)) for cell in cells)
            max_cols = max(max_cols, col_count)
            structured_rows.append(cells)
        
        # Initialize empty grid
        grid = [[None] * max_cols for _ in range(len(rows))]
        
        # Second pass: fill the grid
        for row_idx, cells in enumerate(structured_rows):
            col_idx = 0
            for cell in cells:
                # Skip over already occupied cells
                while col_idx < max_cols and grid[row_idx][col_idx] is not None:
                    col_idx += 1
                    
                rowspan = int(cell.get("rowspan", 1))
                colspan = int(cell.get("colspan", 1))
                
                # Insert main value
                grid[row_idx][col_idx] = cell.get_text(strip=True)
                
                # Mark spanning cells
                for r, c in itertools.product(range(rowspan), range(colspan)):
                    if r == 0 and c == 0:
                        continue
                    
                    new_row = row_idx + r
                    new_col = col_idx + c
                    
                    # Ensure row exists
                    if new_row >= len(grid):
                        grid.extend([[None] * max_cols for _ in range(new_row - len(grid) + 1)])
                    
                    if new_col < len(grid[new_row]):
                        if r > 0:
                            grid[new_row][new_col] = "up"
                        else:
                            grid[new_row][new_col] = "left"
                    
                col_idx += colspan
        
        return grid
    
    def array_to_latex(self, grid):
        """
        Convert a 2D array to LaTeX tabular format with multirow and multicolumn support.
        """
        if not grid or not grid[0]:
            return "\\begin{tabular}{|c|}\\hline\nEmpty Table\\\\\\hline\n\\end{tabular}"
        
        num_cols = len(grid[0])
        latex = "\\begin{tabular}{|" + "|".join(["c"] * num_cols) + "|}\\hline\n"
        
        for row_idx, row in enumerate(grid):
            cells = []
            col_idx = 0
            skip_hline = any(cell == "up" for cell in row)  # Skip \hline if row contains \multirow
            
            while col_idx < num_cols:
                cell = row[col_idx]
                if cell is None:
                    cells.append("")
                    col_idx += 1
                    continue
                elif cell == "up":
                    cells.append(" ")  # Ensure empty space for row merging
                    col_idx += 1
                    continue
                elif cell == "left":
                    col_idx += 1
                    continue
                else:
                    # Count colspan
                    colspan = 1
                    while col_idx + colspan < num_cols and row[col_idx + colspan] == "left":
                        colspan += 1
                    
                    # Count rowspan
                    rowspan = 1
                    while row_idx + rowspan < len(grid) and grid[row_idx + rowspan][col_idx] == "up":
                        rowspan += 1
                    
                    # Apply LaTeX multirow and multicolumn
                    if col_idx == 0:
                        ch = "|"
                    else:
                        ch = ""
                    
                    if rowspan > 1 and colspan > 1:
                        cell_text = f"\\multicolumn{{{colspan}}}{{{ch}c|}}{{\\multirow{{{rowspan}}}{{*}}{{{cell}}}}}"
                    elif rowspan > 1:
                        cell_text = f"\\multirow{{{rowspan}}}{{*}}{{{cell}}}"
                    elif colspan > 1:
                        cell_text = f"\\multicolumn{{{colspan}}}{{{ch}c|}}{{{cell}}}"
                    else:
                        cell_text = cell
                    
                    cells.append(cell_text)
                    col_idx += colspan
            
            latex += " & ".join(cells) + " \\\\ "
            
            # Add \hline only if the next row doesn't contain "up" (multirow continuation)
            if row_idx + 1 < len(grid) and "up" not in grid[row_idx + 1]:
                latex += "\\hline\n"
            elif row_idx + 1 == len(grid):
                latex += "\\hline\n"
            else:
                # Determine the valid range for \cline
                start_col, last_col = 0, num_cols - 1
                while start_col < num_cols and grid[row_idx + 1][start_col] == "up":
                    start_col += 1
                while last_col > 0 and grid[row_idx + 1][last_col] == "up":
                    last_col -= 1
                
                if start_col <= last_col:
                    latex += f"\\cline{{{start_col + 1}-{last_col + 1}}}\n"
        
        latex += "\\end{tabular}"
        return latex


class MarkdownProcessor:
    """
    A class to preprocess Markdown content before passing it to Mistune.
    This allows us to handle certain elements that Mistune doesn't natively support.
    """
    
    def __init__(self):
        self.block_equations = []
        self.equation_counter = 0
        self.html_tables = []
        self.table_counter = 0
    
    def preprocess(self, markdown_text):
        """
        Preprocess markdown text to handle block equations and complex tables.
        Returns the processed text and collected special elements.
        """
        lines = markdown_text.splitlines()
        processed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Handle block equations
            if line.strip() == "$$":
                i += 1
                equation_content = []
                
                # Collect equation content until closing $$
                while i < len(lines) and lines[i].strip() != "$$":
                    equation_content.append(lines[i])
                    i += 1
                
                # Skip the closing $$ if found
                if i < len(lines):
                    i += 1
                
                # Store the equation and add placeholder
                equation_text = "\n".join(equation_content)
                placeholder = f"@EQ{self.equation_counter}@"
                self.block_equations.append((placeholder, equation_text))
                self.equation_counter += 1
                processed_lines.append(placeholder)
                continue
            
            # Handle HTML tables
            if "<table" in line:
                html_table = []
                html_table.append(line)
                
                # If the closing tag is on the same line
                if "</table>" in line:
                    i += 1
                else:
                    i += 1
                    # Collect all table content until closing tag
                    while i < len(lines) and "</table>" not in lines[i]:
                        html_table.append(lines[i])
                        i += 1
                    
                    # Add closing tag line if found
                    if i < len(lines):
                        html_table.append(lines[i])
                        i += 1
                
                # Store the table and add placeholder
                table_html = "\n".join(html_table)
                placeholder = f"@TABLE{self.table_counter}@"
                self.html_tables.append((placeholder, table_html))
                self.table_counter += 1
                processed_lines.append(placeholder)
                continue
            
            # Add regular line
            processed_lines.append(line)
            i += 1
        
        return "\n".join(processed_lines)
    
    def postprocess(self, latex_text, latex_renderer):
        """
        Process the generated LaTeX to replace placeholders with properly formatted elements.
        """
        # Replace equation placeholders
        for placeholder, equation in self.block_equations:
            latex_text = latex_text.replace(placeholder, latex_renderer.process_block_equation(equation))
        
        # Replace table placeholders
        for placeholder, table_html in self.html_tables:
            latex_text = latex_text.replace(placeholder, latex_renderer.process_html_table(table_html))
        
        return latex_text


def markdown_to_latex(markdown_text):
    """
    Convert markdown text to LaTeX using enhanced Mistune renderer with
    preprocessing for complex elements.
    
    Args:
        markdown_text (str): The markdown text to convert
        
    Returns:
        str: The converted LaTeX text
    """
    # Create the preprocessor, renderer and parser
    processor = MarkdownProcessor()
    processed_markdown = processor.preprocess(markdown_text)
    
    renderer = LaTeXRenderer()
    markdown_parser = mistune.create_markdown(renderer=renderer)
    
    # Parse and convert the markdown
    latex_content = markdown_parser(processed_markdown)
    
    # Post-process to handle special elements
    latex_content = processor.postprocess(latex_content, renderer)
    
    # Add LaTeX document structure with necessary packages
    latex_preamble = "\\documentclass{article}\n" \
                     "\\usepackage{hyperref}\n" \
                     "\\usepackage{graphicx}\n" \
                     "\\usepackage{amsmath}\n" \
                     "\\usepackage{amssymb}\n" \
                     "\\usepackage{ulem}  % For strikethrough\n" \
                     "\\usepackage{multirow}  % For multirow tables\n" \
                     "\\usepackage{listings}  % For code listings\n" \
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
    #     print("Usage: python md_to_latex.py input.md output.tex")
    #     sys.exit(1)
    
    input_file = 'test.md'
    output_file = 'output2.tex'
    
    if not process_file(input_file, output_file):
        sys.exit(1)