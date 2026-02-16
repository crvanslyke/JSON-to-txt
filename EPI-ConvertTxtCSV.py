#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import csv
import re

current_dir = os.getcwd()
output_file = os.path.join(current_dir, 'ncoder_LINE_BY_LINE.csv')

def split_by_every_line():
    all_rows = []
    row_id = 1

    # Matches filenames like: climate_adaptation_deepseek...iter01.txt
    file_pattern = re.compile(r"climate_adaptation_(.*)_\d{8}_\d{6}_(iter\d+)\.txt")
    files = [f for f in os.listdir(current_dir) if f.endswith('.txt')]

    for filename in files:
        match = file_pattern.match(filename)
        model = match.group(1) if match else filename
        iteration = match.group(2) if match else "N/A"

        with open(os.path.join(current_dir, filename), 'r', encoding='utf-8') as f:
            # 1. Read everything and strip the AI's internal 'think' blocks
            content = f.read()
            clean_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)

            # 2. SPLIT BY EVERY SINGLE NEWLINE (\n)
            # This ensures headers and bullet points get their own rows
            lines = clean_content.splitlines()

            for line in lines:
                clean_line = line.strip()
                if clean_line:  # Only save rows that aren't empty
                    all_rows.append({
                        'ID': row_id,
                        'Model': model,
                        'Iteration': iteration,
                        'Text': clean_line
                    })
                    row_id += 1

    # 3. Write to CSV with strict quoting to prevent text from leaking into other columns
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Model', 'Iteration', 'Text'], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Success! Created {row_id - 1} individual rows.")

if __name__ == "__main__":
    split_by_every_line()


# In[ ]:




