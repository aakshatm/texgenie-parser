import json
from bs4 import BeautifulSoup
import itertools
import re

def json_to_latex(json_file, output_file):
    """
    Convert a JSON representation of a Markdown AST to LaTeX code.
    
    Args:
        json_file (str): Path to the input JSON file.
        output_file (str): Path to the output LaTeX file.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        ast = json.load(f)
    
    latex_output = []
    first_heading_processed = False
    
    def process_node(node):
        """Recursively process each node in the AST."""
        nonlocal first_heading_processed  # Allow modification of the outer variable
        node_type = node.get("type")
        
        if node_type == "heading":
            # Extract the heading level
            level = node["attrs"]["level"]

            # Process the heading text and remove leading digits, periods, and whitespace
            raw_text = process_children(node)
            clean_text = re.sub(r"^\d+(\.\d+)*\.?\s*", "", raw_text)  # Remove leading digits, periods, and spaces

            # If it's the first heading, make it the title
            if not first_heading_processed:
                first_heading_processed = True
                return f"\\title{{{clean_text}}}\n\\maketitle\n\n"

            # Convert to LaTeX heading based on the level
            if level == 1:
                return f"\\section{{{clean_text}}}\n\n"
            elif level == 2:
                return f"\\section{{{clean_text}}}\n\n"
            elif level == 3:
                return f"\\subsection{{{clean_text}}}\n\n"
            elif level == 4:
                return f"\\subsubsection{{{clean_text}}}\n\n"
            elif level == 5:
                return f"\\paragraph{{{clean_text}}}\n\n"
            else: 
                return f"\\subparagraph{{{clean_text}}}\n\n"
        
        elif node_type == "paragraph":
            # Check if the paragraph contains an equation (delimited by $$)
            raw_text = "".join(
                child["raw"] for child in node.get("children", []) if "raw" in child
            ).strip()
            if raw_text.startswith("$$") and raw_text.endswith("$$"):
                # Extract the equation content (remove the $$ delimiters)
                equation = raw_text[2:-2].strip()
                return f"\\[\n{equation}\n\\]\n\n"
                
            # Check if the paragraph contains an image
            if any(child.get("type") == "image" for child in node.get("children", [])):
                # Extract the image node and its attributes
                image_node = next(child for child in node["children"] if child["type"] == "image")
                src = image_node["attrs"]["url"]

                # Merge all raw text nodes in the paragraph for the caption
                caption = " ".join(
                    child["raw"] for child in node["children"] if child["type"] == "text"
                ).strip()

                # Return the LaTeX figure environment
                return f"""\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{src}}}
\\caption{{{caption}}}
\\end{{figure}}\n\n"""
            else:
                # Process as a normal paragraph
                text = process_children(node)
                return f"{text}\n\n"
        
        elif node_type == "list":
            ordered = node.get("ordered", False)
            items = process_children(node)
            env = "enumerate" if ordered else "itemize"
            return f"\\begin{{{env}}}\n{items}\\end{{{env}}}\n\n"
        
        elif node_type == "list_item":
            text = process_children(node)
            return f"\\item {text}\n"
        
        elif node_type == "table":
            header = process_children(node["header"])
            body = process_children(node["body"])
            columns = len(header.split("&"))
            col_spec = "|" + "c|" * columns
            return f"""\\begin{{table}}[htbp]
\\centering
\\begin{{tabular}}{{{col_spec}}}
\\hline
{header} \\\\ \\hline
{body}
\\end{{tabular}}
\\end{{table}}\n\n"""
        
        elif node_type == "table_row":
            return f"{process_children(node)} \\\\ \\hline\n"
        
        elif node_type == "table_cell":
            content = process_children(node)
            return f"{content} & "
        
        elif node_type == "math":
            return f"${node['raw']}$"
        
        elif node_type == "inline_code":
            return f"\\texttt{{{node['raw']}}}"
        
        elif node_type == "strong":
            text = process_children(node)
            return f"\\textbf{{{text}}}"
        
        elif node_type == "emphasis":
            text = process_children(node)
            return f"\\textit{{{text}}}"
        
        elif node_type == "link":
            text = process_children(node)
            url = node["attrs"]["href"]
            return f"\\href{{{url}}}{{{text}}}"
        
        elif node_type == "image":
            src = node["attrs"]["url"]
            alt = node.get("attrs", {}).get("alt", "")
            caption = alt if alt else "Image"
            return f"""\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{src}}}
\\caption{{{caption}}}
\\end{{figure}}\n\n"""
        
        elif node_type == "block_html":
            # Handle HTML tables or other block HTML elements
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
                            if rowspan > 1 and colspan > 1:
                                cell_text = f"\\multicolumn{{{colspan}}}{{|c|}}{{\\multirow{{{rowspan}}}{{*}}{{{cell}}}}}"
                            elif rowspan > 1:
                                cell_text = f"\\multirow{{{rowspan}}}{{*}}{{{cell}}}"
                            elif colspan > 1:
                                cell_text = f"\\multicolumn{{{colspan}}}{{|c|}}{{{cell}}}"
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

            # Use the convert_html_table_to_latex function to handle HTML tables
            html_content = node["raw"]
            return convert_html_table_to_latex(html_content)
            return f"% HTML block skipped: {node['raw']}\n"
        
        elif node_type == "blank_line":
            return "\n"
        
        elif node_type == "text":
            return node["raw"]
        
        elif node_type == "softbreak":
            return " "
        
        elif node_type == "linebreak":
            return "\\\\\n"
        
        else:
            return f"% Unknown node type: {node_type}\n"
    
    def process_children(node):
        """Process all children of a node."""
        if "children" in node:
            return "".join(process_node(child) for child in node["children"])
        return node.get("raw", "")
    
    # Process the root AST
    for node in ast:
        latex_output.append(process_node(node))
    
    # Add LaTeX document structure
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
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_preamble)
        f.write("".join(latex_output))
        f.write(latex_ending)
    
    print(f"LaTeX has been saved to {output_file}")

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


# Example usage
if __name__ == "__main__":
    input_json = "output.json"  # Replace with your JSON file
    output_tex = "outputJson.tex"  # Replace with your desired LaTeX output file
    json_to_latex(input_json, output_tex)