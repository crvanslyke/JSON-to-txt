# 1. Paste your messy text here
raw_text = r"""
PASTE_YOUR_TEXT_HERE
"""

def simple_clean(text):
    # Step A: Convert the literal "\n" strings into actual line breaks
    # We use .replace instead of json.loads to prevent any hanging
    clean_text = text.replace("\\n", "\n")
    
    final_lines = []
    
    # Step B: Process line by line to strip Markdown symbols
    for line in clean_text.splitlines():
        # Remove table dashes (e.g., |---|)
        if set(line.strip()) <= {"-", "|", " "}:
            continue
            
        # Strip Markdown characters: #, *, _, and |
        # We use a simple translation table for speed
        chars_to_remove = "#*_|"
        for char in chars_to_remove:
            line = line.replace(char, "")
        
        final_lines.append(line.rstrip())

    # Join lines back together with a single newline
    return "\n".join(final_lines)

print(simple_clean(raw_text))