import json
import os
import sys

def simple_clean(text):
    """
    Cleans the input text by:
    1. Converting literal "\\n" to actual newlines.
    2. Removing Markdown table separator lines.
    3. Stripping Markdown characters (#, *, _, |).
    """
    if not text:
        return ""
        
    # Step A: Convert the literal "\n" strings into actual line breaks
    clean_text = text.replace("\\n", "\n")
    
    final_lines = []
    
    # Step B: Process line by line to strip Markdown symbols
    for line in clean_text.splitlines():
        # Remove table dashes (e.g., |---|)
        if set(line.strip()) <= {"-", "|", " "}:
            continue
            
        # Strip Markdown characters: #, *, _, and |
        chars_to_remove = "#*_|"
        for char in chars_to_remove:
            line = line.replace(char, "")
        
        final_lines.append(line.rstrip())

    # Join lines back together with a single newline
    return "\n".join(final_lines)

def process_directory(directory_path):
    """
    Iterates through all JSON files in the given directory,
    extracts 'generated_content', cleans it, and saves as TXT.
    """
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return

    # List all files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract content
                content = data.get("generated_content")
                
                if content:
                    cleaned_content = simple_clean(content)
                    
                    # Create output filename (replace .json with .txt)
                    output_filename = os.path.splitext(filename)[0] + ".txt"
                    output_path = os.path.join(directory_path, output_filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(cleaned_content)
                    
                    print(f"Successfully converted: {filename} -> {output_filename}")
                else:
                    print(f"Skipping {filename}: 'generated_content' key not found or empty.")
            
            except json.JSONDecodeError:
                print(f"Skipping {filename}: Invalid JSON format.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Default to current directory if no argument provided
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print(f"Processing JSON files in: {os.path.abspath(target_dir)}")
    process_directory(target_dir)
