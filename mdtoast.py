import mistune
import json

# Read Markdown text from a file
with open("test.md", "r", encoding="utf-8") as file:
    markdown_text = file.read()

# Create a Markdown parser with AST renderer
parser = mistune.create_markdown(renderer="ast")

# Convert Markdown to AST
ast = parser(markdown_text)

with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(ast, json_file, indent=2)

print("AST has been saved to output.json")



# import mistune
# import json
# import re

# class MathMarkdown(mistune.Markdown):
#     def __init__(self):
#         super().__init__(renderer="ast", plugins=[self.math_plugin])

#     def math_plugin(self, md):
#         md.inline.register("math_inline", self.parse_inline_math, before="text")
#         md.block.register("math_block", self.parse_block_math, before="paragraph")

#     def parse_inline_math(self, inline, m, state):
#         text = m.group(1)
#         return "math_inline", {"text": text}

#     def parse_block_math(self, block, m, state):
#         text = m.group(1)
#         return "math_block", {"text": text}

# # Define regex patterns for detecting equations
# INLINE_MATH_PATTERN = re.compile(r"\$(.+?)\$")
# BLOCK_MATH_PATTERN = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)

# # Register the regex patterns with Mistune
# mistune.inline_math_rule = INLINE_MATH_PATTERN
# mistune.block_math_rule = BLOCK_MATH_PATTERN

# # Create the Markdown parser with math detection
# parser = MathMarkdown()

# # Example Markdown with Math
# with open("testingFilesWithMdFiles/org-mdfiles/Hybrid-modified/2.md", "r", encoding="utf-8") as file:
#     markdown_text = file.read()

# # Convert Markdown to AST
# ast = parser(markdown_text)

# # Save AST to JSON
# with open("output.json", "w", encoding="utf-8") as json_file:
#     json.dump(ast, json_file, indent=2)

# print(json.dumps(ast, indent=2))
