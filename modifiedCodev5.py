import re
import os
import html
from bs4 import BeautifulSoup
import itertools

def convert_markdown_to_latex(markdown_text):
    """
    Convert Markdown text to LaTeX format with special handling for the specified formats.
    
    Args:
        markdown_text (str): The Markdown text to be converted.
        
    Returns:
        str: The converted LaTeX text.
    """
    # Initialization
    latex_output = ""
    lines = split_lines(markdown_text)
    list_stack = []  # Track nested list levels
    in_code_block = False
    code_block_language = ""
    html_block = []
    in_html_block = False
    i = 0
    
    # Extract and convert title
    title_match = re.match(r'^#\s+(.+)$', lines[0])
    if title_match:
        title = title_match.group(1).strip()
        latex_output += f"\\title{{{title}}}\n"
        i += 1
    
    # Extract and convert author details
    author_details = []
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'^#\s+Abstract$', line, re.IGNORECASE):
            break
        author_details.append(line)
        i += 1
    if author_details:
        latex_output += "\\author{" + " \\\\ ".join(author_details) + "}\n"
    
    # Extract and convert abstract
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'^#\s+Abstract$', line, re.IGNORECASE):
            latex_output += "\\begin{abstract}\n"
            i += 1
            while i < len(lines) and not re.match(r'^#\s+', lines[i]):
                latex_output += lines[i].strip() + " "
                i += 1
            latex_output += "\n\\end{abstract}\n"
            break
        i += 1

    # i = 0  # Reset index to process the rest of the document
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            latex_output += "\n"
            i += 1
            continue
        
        # Step 1: Convert Code Blocks
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                if code_block_language:
                    latex_output += "\\end{lstlisting}\n"
                else:
                    latex_output += "\\end{verbatim}\n"
                code_block_language = ""
            else:
                in_code_block = True
                code_block_language = extract_language(line)
                if code_block_language:
                    latex_output += f"\\begin{{lstlisting}}[language={code_block_language}]\n"
                else:
                    latex_output += "\\begin{verbatim}\n"
            i += 1
            continue

        if in_code_block:
            latex_output += line + "\n"
            i += 1
            continue

        # Step 2: Handle Math Equations in the specific format - case 1
        if line == "$$":
            # Start of equation block
            latex_output += "\\begin{equation}\n"
            i += 1
            equation_content = []
            
            # Collect all lines until the closing $$
            while i < len(lines) and lines[i].strip() != "$$":
                equation_content.append(lines[i])
                i += 1
                
            # Join and add the equation content
            if equation_content:
                equation_text = "\n".join(equation_content)
                latex_output += equation_text + "\n"
                
            # Add closing tag and skip the closing $$
            latex_output += "\\end{equation}\n"
            if i < len(lines):
                i += 1
            continue
            

        # Step 3: Convert Headers based upon dots upto 3 dots
        # Match headers like "# 3 header" "# 3.2 header2" "#3.3.3 header 3"
        # header_match = re.match(r'^#+\s+(\d+)(?:\.(\d+))?(?:\.(\d+))?\s+(.+)$', line)
        # if header_match:
        #     # Extract section numbers and title
        #     section = header_match.group(1)
        #     subsection = header_match.group(2)
        #     subsubsection = header_match.group(3)
        #     header_text = header_match.group(4).strip()
            
        #     # Determine header level based on dots
        #     if subsubsection:
        #         # This is a subsubsection (###)
        #         latex_output += f"\\subsubsection{{{header_text}}}\n"
        #     elif subsection:
        #         # This is a subsection (##)
        #         latex_output += f"\\subsection{{{header_text}}}\n"
        #     else:
        #         latex_output += f"\\section{{{header_text}}}"
        #     i += 1
        #     continue

        header_match = re.match(r'^#+\s+(\d+(?:\.\d+)*\.?)\s+(.+)$', line)
        if header_match:
            # Extract section numbers and title
            section = header_match.group(1).rstrip('.')  # Remove trailing dot if present
            header_text = header_match.group(2).strip()
            
            # Count how many dots are in the section number to determine level
            dot_count = section.count('.')

            # Convert to LaTeX sectioning
            if dot_count == 2:
                latex_output += f"\\subsubsection{{{header_text}}}\n"
            elif dot_count == 1:
                latex_output += f"\\subsection{{{header_text}}}\n"
            else:
                latex_output += f"\\section{{{header_text}}}\n"

            i += 1
            continue
        
        # Handle regular headers
        regular_header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if regular_header_match and not header_match:
            level = len(regular_header_match.group(1))
            header_text = regular_header_match.group(2).strip()
            
            # Remove any leading numbers from the header text (like '3.2 Title' -> 'Title')
            header_text = re.sub(r'^\d+(\.\d+)*\s+', '', header_text)
            
            if level == 1:
                latex_output += f"\\section{{{header_text}}}\n"
            elif level == 2:
                latex_output += f"\\subsection{{{header_text}}}\n"
            elif level == 3:
                latex_output += f"\\subsubsection{{{header_text}}}\n"
            elif level == 4:
                latex_output += f"\\paragraph{{{header_text}}}\n"
            elif level == 5:
                latex_output += f"\\subparagraph{{{header_text}}}\n"
            else:
                latex_output += f"\\textbf{{{header_text}}}\n"
            i += 1
            continue
        
        # Step 4: Handle captions before images
        # image_caption_match = re.match(r'^Fig\.?\s+(\d+)\.?\s+(.*)', line)
        image_caption_match = re.match(r'^(?:Fig\.?|Figure)\s+(\d+)[\.:]?\s+(.*)', line)
        
        if image_caption_match and i + 1 < len(lines):
            # Found a caption before an image
            caption_number = image_caption_match.group(1)
            caption_text = image_caption_match.group(2)
            is_image_found = False

            # Find the next line which might contain the image, if not then attach the caption only 
            while(i+1 < len(lines)):
                line = lines[i+1].strip()
                image_match = re.search(r'!\[\]\((.*?)\)', line)
                if line and (not image_match):
                    #image not found but there is a line
                    break
                elif line and image_match:
                    #found the image line
                    is_image_found = True
                    break

                i += 1

            i += 1
            
            if is_image_found:
                line = lines[i].strip()
                image_match = re.search(r'!\[\]\((.*?)\)', line)
                image_path = image_match.group(1)
                
                # Create figure environment
                latex_output += "\\begin{figure}[htbp]\n\\centering\n"
                latex_output += f"\\includegraphics[width=0.8\\linewidth]{{{image_path}}}\n"
                latex_output += f"\\caption{{{caption_text}}}\n"
                latex_output += f"\\label{{fig:{caption_number}}}\n"
                latex_output += "\\end{figure}\n\n"
                
                i += 1
                continue
            
            
        # Step 6: Handle Images Post Figure captions (after image captions)
        image_match = re.search(r'!\[\]\((.*?)\)', line)
        if image_match:
            image_path = image_match.group(1)
            # Look ahead for a caption line starting with "Fig."
            caption_found = False
            caption_number = ""
            caption_text = ""
            
            # Check next line for caption
            while i + 1 < len(lines):
                line = lines[i+1].strip()
                # image_caption_match = re.match(r'^Fig\.?\s+(\d+)\.?\s+(.*)', line)
                image_caption_match = re.match(r'^(?:Fig\.?|Figure)\s+(\d+)[\.:]?\s+(.*)', line)

                if line and not image_caption_match:
                    #found a line that is not caption
                    break
                elif line and image_caption_match:
                    caption_number = image_caption_match.group(1)
                    caption_text = image_caption_match.group(2)
                    caption_found = True
                    break  # Skip the caption line in next iteration
                i += 1
            
            i += 1

            if caption_found:
                # Found Image and Caption next to it
                latex_output += "\\begin{figure}[htbp]\n\\centering\n"
                latex_output += f"\\includegraphics[width=0.8\\linewidth]{{{image_path}}}\n"
                
                if caption_text:
                    latex_output += f"\\caption{{{caption_text}}}\n"
                    
                if caption_number:
                    latex_output += f"\\label{{fig:{caption_number}}}\n"
                    
                latex_output += "\\end{figure}\n\n"
                i += 1 
            
            else:
                #found the image but not any caption belongs to it
                latex_output += "\\begin{figure}[htbp]\n\\centering\n"
                latex_output += f"\\includegraphics[width=0.8\\linewidth]{{{image_path}}}\n"
                latex_output += "\\end{figure}\n\n"
                
                

            continue
            # # Replace the image tag in the line
            # line = line.replace(image_match.group(0), "")
            
            # # If line is now empty, move to next line
            # if not line.strip():
            #     i += 1
            #     continue
        
        
        # Step 7: Handle captions before Table
        table_caption_match = re.match(r'^Table\.?\s+(\d+)\.?\s+(.*)', line)
        if table_caption_match and i + 1 < len(lines):
            table_output = "" #table preamble
            table_content = "" #store actual table
            # Found a caption before a table
            caption_number = table_caption_match.group(1)
            caption_text = table_caption_match.group(2)

            # Move to the next line
            i += 1

            # Skip empty lines before encountering the table
            while i < len(lines) and lines[i].strip() == "":
                i += 1

            # Handle HTML table
            if i < len(lines) and "<table" in lines[i]:
                html_table = []

                # Check if </table> is in the same line as <table>
                if "</table>" in lines[i]:
                    html_table.append(lines[i])
                    i += 1  # Move to the next line
                else:
                    # Collect the entire table content
                    while i < len(lines):
                        html_table.append(lines[i])
                        if "</table>" in lines[i]:
                            i += 1  # Move next the closing tag
                            break
                        i += 1

                html_content = "".join(html_table)
                try:
                    # Convert HTML table to LaTeX
                    table_content = convert_html_table_to_latex(html_content)
                except Exception as e:
                    # Fallback to verbatim if conversion fails
                    table_content += f"\\begin{{verbatim}}\n{html_content}\n\\end{{verbatim}}\n"

            # Handle markdown table
            elif i < len(lines) and "|" in lines[i]:
                markdown_table = []
                while i < len(lines) and "|" in lines[i]:
                    markdown_table.append(lines[i])
                    i += 1

                # Convert markdown table to LaTeX tabular
                table_output += convert_markdown_table_to_latex(markdown_table)

            
            # Start the table environment
            table_output += "\\begin{table}[htbp]\n\\centering\n"
            table_output += f"\\caption{{{caption_text}}}\n"
            table_output += f"\\label{{tab:{caption_number}}}\n"
            table_output += table_content
            table_output += "\\end{table}\n\n"
            
            if table_content:
                #found the table and caption both
                latex_output += table_output
            
            else:
                #only caption found
                latex_output += f"Table {caption_number} {caption_text}\n"

            continue

        # 
        # Step 8: Handle table before the Table caption
        if "<table" in line:
            table_output = "" #table preamble
            table_content = "" #store actual table
            html_table = []

            # Check if </table> is in the same line as <table>
            if "</table>" in line:
                html_table.append(line)
            else:
                # Collect the entire table content
                while i < len(lines):
                    html_table.append(lines[i])
                    if "</table>" in lines[i]:
                        break
                    i += 1

            html_content = "".join(html_table)
            try:
                # Convert HTML table to LaTeX
                table_content = convert_html_table_to_latex(html_content)
            except Exception as e:
                # Fallback to verbatim if conversion fails
                table_content += f"\\begin{{verbatim}}\n{html_content}\n\\end{{verbatim}}\n"


            # After the table, search for a caption
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1  # Skip empty lines

            table_output = "\\begin{table}[htbp]\n\\centering\n"
            if i < len(lines):
                table_caption_match = re.match(r'^Table\.?\s+(\d+)\.?\s+(.*)', lines[i])

                if table_caption_match:
                    caption_number = table_caption_match.group(1)
                    caption_text = table_caption_match.group(2)

                    table_output += f"\\caption{{{caption_text}}}\n"
                    table_output += f"\\label{{tab:{caption_number}}}\n"
                    i += 1

            table_output += table_content
            table_output += "\\end{table}\n\n"
            latex_output += table_output
            continue



        # Step 1: Extract and preserve math expressions
        line, math_placeholders = extract_math_expressions(line)

        # Step 2: Convert Markdown bold/italics formatting
        line = convert_markdown_formatting(line)

        # Step 3: Escape LaTeX special characters (outside math mode)
        line = escape_latex_chars(line)

        # Step 4: Reinsert math expressions
        line = reinsert_math_expressions(line, math_placeholders)
    

        # Step 8: Convert Blockquotes
        if line.startswith(">"):
            if not list_stack or list_stack[-1] != "quote":
                latex_output += "\\begin{quote}\n"
                list_stack.append("quote")
            latex_output += line[1:].strip() + "\n"
            i += 1
            continue

        if list_stack and list_stack[-1] == "quote" and not line.startswith(">"):
            latex_output += "\\end{quote}\n"
            list_stack.pop()
        
        # Step 4: Convert Lists
        list_match = re.match(r'^(\s*)([*+-]|\d+\.)\s+(.+)$', line)
        if list_match:
            indent = list_match.group(1)
            list_marker = list_match.group(2)
            list_item = list_match.group(3)
            
            # Determine list type and level
            is_ordered = re.match(r'\d+\.', list_marker) is not None
            level = len(indent) // 2  # Assuming 2 spaces per level
            
            # Adjust list stack as needed
            while len(list_stack) > level + 1:
                list_type_end = list_stack.pop()
                if list_type_end in ["itemize", "enumerate"]:
                    latex_output += f"\\end{{{list_type_end}}}\n"
            
            # Start new list if needed
            if len(list_stack) <= level:
                if is_ordered:
                    latex_output += "\\begin{enumerate}\n"
                    list_stack.append("enumerate")
                else:
                    latex_output += "\\begin{itemize}\n"
                    list_stack.append("itemize")
            
            # Output list item
            latex_output += f"\\item {list_item}\n"
            i += 1
            continue
        
        # Close lists if we're no longer in a list
        if not re.match(r'^\s*([*+-]|\d+\.)\s+', line) and any(item in ["itemize", "enumerate"] for item in list_stack):
            while list_stack and list_stack[-1] in ["itemize", "enumerate"]:
                list_type_end = list_stack.pop()
                latex_output += f"\\end{{{list_type_end}}}\n"
        

        # Step 10: Convert Horizontal Rules
        if re.match(r'^(\*\*\*+|\-\-\-+|___+)\s*$', line):
            latex_output += "\\hrulefill\n\n"
            i += 1
            continue
        
        # Step 5: Convert Links
        line = convert_links(line)
        
        # Handle line breaks
        if line.endswith("  "):
            latex_output += line.strip() + "\\\\\n"
        else:
            # Skip empty lines (they'll be preserved in output)
            if line.strip() or (i > 0 and i < len(lines)-1 and lines[i-1].strip() and lines[i+1].strip()):
                latex_output += line + "\n"
        
        i += 1
    
    # Close any remaining environments
    while list_stack:
        list_type_end = list_stack.pop()
        if list_type_end in ["itemize", "enumerate", "quote"]:
            latex_output += f"\\end{{{list_type_end}}}\n"
    
    return latex_output

def html_table_to_2d_array(html):
    """
    Convert an HTML table to a 2D array with handling for rowspan and colspan.
    Merged cells are marked with "up" for row-wise merges and "left" for column-wise merges.
    
    Args:
        html (str): HTML content containing a table
        
    Returns:
        list: 2D array representation of the table
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
                
                if r > 0:
                    grid[new_row][new_col] = "up"
                else:
                    grid[new_row][new_col] = "left"
                
            col_idx += colspan
    
    return grid

def array_to_latex(grid):
    """
    Convert a 2D array to LaTeX tabular format with support for merged cells using \\multicolumn and \\multirow.
    Ensures that \\hline does not pass through multirow cells.
    
    Args:
        grid (list): 2D array representation of a table
        
    Returns:
        str: LaTeX tabular environment
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
                if col_idx==0:
                    ch="|"
                else:
                    ch=""
                
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

def convert_html_table_to_latex(html):
    """
    Convert an HTML table to LaTeX tabular environment.
    
    Args:
        html (str): HTML content containing a table
        
    Returns:
        str: LaTeX tabular environment
    """
    try:
        array = html_table_to_2d_array(html)
        return array_to_latex(array)
    except Exception as e:
        # Fallback to verbatim
        return f"\\begin{{verbatim}}\n{html}\n\\end{{verbatim}}"


def convert_markdown_table_to_latex(table_lines):
    """Convert Markdown table to LaTeX tabular environment."""
    if not table_lines:
        return ""
    
    # Process the header row to determine number of columns
    header_row = table_lines[0]
    columns = [col.strip() for col in header_row.split('|') if col.strip()]
    num_columns = len(columns)
    
    # Create the tabular environment
    latex_table = f"\\begin{{tabular}}{{{'|c' * num_columns}|}}\n\\hline\n"
    
    # Add the header row
    latex_table += " & ".join(columns) + " \\\\ \\hline\n"
    
    # Skip the separator row (line 1) and process data rows
    for row in table_lines[2:]:
        if row.strip():
            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
            if cells:
                latex_table += " & ".join(cells) + " \\\\ \\hline\n"
    
    latex_table += "\\end{tabular}\n"
    return latex_table

def split_lines(text):
    """Split text into lines."""
    return text.splitlines()


def extract_math_expressions(text):
    """
    Extracts inline math expressions ($...$) and replaces them with placeholders.
    """
    math_patterns = re.findall(r'(?<!\\)(?<!\$)\$(.*?)(?<!\\)\$', text)
    placeholder_map = {}

    for i, math_expr in enumerate(math_patterns):
        placeholder = f"@@MATH{i}@@"
        placeholder_map[placeholder] = math_expr
        text = text.replace(math_expr, placeholder, 1)

    return text, placeholder_map

def convert_markdown_formatting(text):
    """
    Converts Markdown bold (**bold**) and italics (*italic*) to LaTeX format.
    """
    # Convert bold (**bold**) -> \textbf{}
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)

    # Convert italics (*italic*) -> \textit{}
    text = re.sub(r'(?<!\*)\*(.*?)\*(?!\*)', r'\\textit{\1}', text)

    return text


def escape_latex_chars(text):
    """
    Escapes LaTeX special characters except in math placeholders and math mode.
    """
    replacements = {
        '\\': r'\\',  # Backslash
        '_': r'\_',    # Underscore
        '^': r'\^{}',  # Caret
        '%': r'\%',    # Percent
        '#': r'\#',    # Hash
        '&': r'\&',    # Ampersand
        '{': r'\{',    # Curly brace
        '}': r'\}',    # Curly brace
        '~': r'\textasciitilde{}',  # Tilde
    }

    # Escape special characters (except $)
    for char, escaped in replacements.items():
        text = re.sub(rf'(?<!@)({re.escape(char)})(?!MATH\d+@@)', escaped, text)

    # Ensure $ is not escaped inside math mode ($@@MATH0@@$ should remain unchanged)
    text = re.sub(r'(?<![@\$])\$(?!@@MATH\d+@@)', r'\$', text)


    return text

def reinsert_math_expressions(text, placeholder_map):
    """
    Restores math expressions from placeholders.
    """
    for placeholder, math_expr in placeholder_map.items():
        text = text.replace(placeholder, math_expr)

    return text



def convert_links(text):
    """Convert Markdown links to LaTeX hyperlinks."""
    # Regular links: [text](url)
    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        return f"\\href{{{link_url}}}{{{link_text}}}"
    
    text = re.sub(r'\[(.*?)\]\((.*?)\)', replace_link, text)
    
    return text

def extract_language(line):
    """Extract the language specifier from a code block opening."""
    match = re.match(r'^```(\w+)\s*$', line)
    if match:
        return match.group(1)
    return ""

def main():
    """Main function to convert a Markdown file to LaTeX."""
    import argparse
    
    # parser = argparse.ArgumentParser(description='Convert Markdown to LaTeX')
    # parser.add_argument('input_file', help='Input Markdown file')
    # parser.add_argument('-o', '--output', help='Output LaTeX file')
    # parser.add_argument('--preamble', help='LaTeX preamble file to include')
    
    # args = parser.parse_args()
    input_file = 'test.md'
    # input_file = 'placeholder.md'
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return 1
    
    # Convert to LaTeX
    latex_text = convert_markdown_to_latex(markdown_text)
    
    # Determine output file
    # output_file = args.output if args.output else os.path.splitext(args.input_file)[0] + '.tex'
    output_file = os.path.splitext(input_file)[0] + '.tex'
    
    # Write output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_text)
        print(f"Successfully converted '{input_file}' to '{output_file}'")
    except Exception as e:
        print(f"Error writing output file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())



