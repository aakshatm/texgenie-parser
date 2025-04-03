import re
import sys

def markdown_to_latex(markdown_text):
    """
    Convert markdown text to LaTeX.
    
    Args:
        markdown_text (str): The markdown text to convert
        
    Returns:
        str: The converted LaTeX text
    """
    # Store the result
    latex_text = markdown_text
    
    # Define LaTeX document preamble and ending
    latex_preamble = "\\documentclass{article}\n\\usepackage{hyperref}\n\\usepackage{graphicx}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\begin{document}\n\n"
    latex_ending = "\n\\end{document}"
    
    # Headers
    latex_text = re.sub(r'^# (.*?)$', r'\\section{\1}', latex_text, flags=re.MULTILINE)
    latex_text = re.sub(r'^## (.*?)$', r'\\subsection{\1}', latex_text, flags=re.MULTILINE)
    latex_text = re.sub(r'^### (.*?)$', r'\\subsubsection{\1}', latex_text, flags=re.MULTILINE)
    latex_text = re.sub(r'^#### (.*?)$', r'\\paragraph{\1}', latex_text, flags=re.MULTILINE)
    latex_text = re.sub(r'^##### (.*?)$', r'\\subparagraph{\1}', latex_text, flags=re.MULTILINE)
    
    # Bold and italic
    latex_text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', latex_text)
    latex_text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', latex_text)
    latex_text = re.sub(r'__(.*?)__', r'\\textbf{\1}', latex_text)
    latex_text = re.sub(r'_(.*?)_', r'\\textit{\1}', latex_text)
    
    # Inline code
    latex_text = re.sub(r'`(.*?)`', r'\\texttt{\1}', latex_text)
    
    # Code blocks
    def replace_code_block(match):
        code = match.group(1).strip()
        return f"\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}"
    
    latex_text = re.sub(r'```(?:\w+)?\n(.*?)\n```', replace_code_block, latex_text, flags=re.DOTALL)
    
    # Links
    latex_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', latex_text)
    
    # Images
    latex_text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'\\begin{figure}\n\\centering\n\\includegraphics{"\2"}\n\\caption{\1}\n\\end{figure}', latex_text)
    
    # Lists
    # Unordered lists
    def replace_unordered_list(match):
        items = match.group(0).strip().split('\n')
        latex_list = "\\begin{itemize}\n"
        for item in items:
            if item.strip().startswith('- '):
                latex_list += f"  \\item {item.strip()[2:]}\n"
        latex_list += "\\end{itemize}"
        return latex_list
    
    # Match continuous blocks of unordered list items
    latex_text = re.sub(r'(?:^- .*?$\n?)+', replace_unordered_list, latex_text, flags=re.MULTILINE)
    
    # Ordered lists
    def replace_ordered_list(match):
        items = match.group(0).strip().split('\n')
        latex_list = "\\begin{enumerate}\n"
        for item in items:
            if re.match(r'^\d+\. ', item.strip()):
                content = re.sub(r'^\d+\. ', '', item.strip())
                latex_list += f"  \\item {content}\n"
        latex_list += "\\end{enumerate}"
        return latex_list
    
    # Match continuous blocks of ordered list items
    latex_text = re.sub(r'(?:^\d+\. .*?$\n?)+', replace_ordered_list, latex_text, flags=re.MULTILINE)
    
    # Blockquotes
    def replace_blockquote(match):
        content = match.group(1).strip()
        return f"\\begin{{quotation}}\n{content}\n\\end{{quotation}}"
    
    latex_text = re.sub(r'^> (.*?)$', replace_blockquote, latex_text, flags=re.MULTILINE)
    
    # Horizontal rule
    latex_text = re.sub(r'^---+$', r'\\rule{\\textwidth}{0.4pt}', latex_text, flags=re.MULTILINE)
    
    # Tables - simplified approach
    def replace_table(match):
        table_text = match.group(0)
        rows = table_text.strip().split('\n')
        
        if len(rows) < 3:  # Need at least header, separator, and one data row
            return table_text
            
        # Extract columns from header
        columns = [col.strip() for col in rows[0].split('|')[1:-1]]
        num_cols = len(columns)
        
        # Start table
        latex_table = "\\begin{tabular}{" + "|".join(["c"] * num_cols) + "}\n\\hline\n"
        
        # Add header
        latex_table += " & ".join(columns) + " \\\\ \\hline\n"
        
        # Add data rows
        for row in rows[2:]:  # Skip header and separator
            if row.strip() and '|' in row:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                latex_table += " & ".join(cells) + " \\\\ \\hline\n"
                
        latex_table += "\\end{tabular}"
        return latex_table
        
    # Find and replace markdown tables
    table_pattern = r'^\|.*\|\n\|[-:|]+\|\n(?:\|.*\|\n)+'
    latex_text = re.sub(table_pattern, replace_table, latex_text, flags=re.MULTILINE)
    
    # Math blocks - Keep them as is since LaTeX already handles them
    # Just make sure to properly escape the dollar signs that are not part of math expressions
    
    # Wrap the content in document structure
    return latex_preamble + latex_text + latex_ending

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
    if len(sys.argv) != 3:
        print("Usage: python markdown_to_latex.py input.md output.tex")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not process_file(input_file, output_file):
        sys.exit(1)