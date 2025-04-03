#!/usr/bin/env python3
"""
Generate README.md from structured JSON data
"""
import json
import os
import sys

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'resources.json')
README_FILE = os.path.join(ROOT_DIR, 'README.md')
README_TEMPLATE = os.path.join(ROOT_DIR, 'scripts', 'readme_template.md')

def generate_readme():
    """Generate README.md from the resources.json file"""
    
    # Load the data
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        sys.exit(1)
    
    # Load the template
    try:
        with open(README_TEMPLATE, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        # Create a default template if it doesn't exist
        template = """# Awesome NZ Tech

A curated list of awesome tech resources, projects, and communities in Aotearoa New Zealand.

## Table of Contents

{toc}

{content}

## Contributing

Contributions are welcome! Please see the [Contributing Guidelines](./CONTRIBUTING.md) for more details.
"""
    
    # Generate Table of Contents
    toc_items = []
    for key, category in sorted(data.get('categories', {}).items()):
        toc_items.append(f"- [{category['name']}](#{key})")
    
    toc = "\n".join(toc_items)
    
    # Generate Content
    content_sections = []
    for key, category in sorted(data.get('categories', {}).items()):
        section = f"## {category['name']}\n\n{category['description']}\n"
        
        entries = category.get('entries', [])
        if entries:
            for entry in entries:
                section += f"\n- [{entry['name']}]({entry['url']}) - {entry['description']}"
        else:
            section += "\n- *No entries yet*"
        
        content_sections.append(section)
    
    content = "\n\n".join(content_sections)
    
    # Replace placeholders
    readme_content = template.format(toc=toc, content=content)
    
    # Write the README
    with open(README_FILE, 'w') as f:
        f.write(readme_content)
    
    print(f"Generated README.md successfully!")

if __name__ == "__main__":
    generate_readme()
