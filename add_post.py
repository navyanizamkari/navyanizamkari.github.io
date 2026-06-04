#!/usr/bin/env python3
"""
Simple Blog Post Generator for Navya's Portfolio Website

Usage:
    python3 add_post.py path/to/your-article.md

This script will:
1. Read your markdown file
2. Extract metadata from the content
3. Generate HTML version automatically
4. Update articles.json
5. Update blog index.html
6. Tell you what to commit

Just write your markdown file and run this script!
"""

import json
import re
import os
import sys
from datetime import datetime

def extract_metadata(content):
    """Extract metadata from markdown content"""
    lines = content.split('\n')
    
    # Get title (first # heading)
    title = "New Blog Post"
    for line in lines:
        if line.strip().startswith('# '):
            title = line.strip()[2:]
            break
    
    # Extract metadata from second line (if exists)
    date = datetime.now().strftime('%Y-%m-%d')
    category = "Technology"
    read_time = "5 min"
    
    for line in lines[:10]:  # Check first 10 lines
        if line.startswith('*Published:'):
            # Parse: *Published: YYYY-MM-DD | Category: Machine Learning | Read time: 8 min*
            parts = line.split('|')
            if len(parts) >= 3:
                date_part = parts[0].split(':')[1].strip()
                category = parts[1].split(':')[1].strip()
                read_time = parts[2].split(':')[1].strip().replace('*', '')
            break
    
    # Extract first paragraph as excerpt
    excerpt = ""
    in_content = False
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('*Published:') and not line.startswith('---'):
            # Clean up markdown formatting for excerpt
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Remove bold
            clean_line = re.sub(r'`(.*?)`', r'\1', clean_line)   # Remove code
            clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)  # Remove links
            if len(clean_line) > 20:  # Good enough for excerpt
                excerpt = clean_line[:200] + "..." if len(clean_line) > 200 else clean_line
                break
    
    # Generate tags from title and category
    tags = []
    if "LLM" in title or "language model" in title.lower():
        tags.extend(["LLMs", "AI"])
    if "production" in title.lower():
        tags.append("Production")
    if "optimization" in title.lower() or "performance" in title.lower():
        tags.append("Optimization")
    if "mobile" in title.lower() or "edge" in title.lower():
        tags.extend(["Mobile", "Edge Computing"])
    if "machine learning" in title.lower() or "ML" in title:
        tags.append("Machine Learning")
    
    # Default tags if none found
    if not tags:
        tags = ["Technology", "AI"]
    
    return {
        'title': title,
        'date': date,
        'category': category,
        'read_time': read_time,
        'excerpt': excerpt,
        'tags': tags[:3]  # Limit to 3 tags
    }

def markdown_to_html(content, metadata):
    """Convert markdown content to HTML"""
    # Simple markdown to HTML conversion
    html_content = content
    
    # Headers
    html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # Bold and italic
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # Code
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # Links
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # Lists
    html_content = re.sub(r'^- (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
    
    # Paragraphs (simple version)
    paragraphs = []
    for line in html_content.split('\n'):
        line = line.strip()
        if line and not line.startswith('<') and not line.startswith('*Published:'):
            if line.startswith('---'):
                paragraphs.append('<hr>')
            else:
                paragraphs.append(f'<p>{line}</p>')
        elif line.startswith('<'):
            paragraphs.append(line)
    
    return '\n'.join(paragraphs)

def create_html_file(filename, metadata, content_html):
    """Create the full HTML file"""
    file_id = filename.replace('.md', '')
    tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in metadata['tags']])
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']} - Navya Sri Nizamkari</title>
    <meta name="description" content="{metadata['excerpt'][:150]}">
    
    <link rel="icon" type="image/x-icon" href="../../favicon.ico">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="stylesheet" href="../../css/blog.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <a href="../../index.html">Navya Sri Nizamkari</a>
            </div>
            <div class="nav-menu">
                <a href="../../index.html" class="nav-link">Home</a>
                <a href="../index.html" class="nav-link">Blog</a>
            </div>
        </div>
    </nav>

    <article class="article-content">
        <div class="container">
            <header class="article-header">
                <h1>{metadata['title']}</h1>
                <div class="article-meta">
                    <span class="article-date"><i class="fas fa-calendar"></i> {metadata['date']}</span>
                    <span class="article-category"><i class="fas fa-tag"></i> {metadata['category']}</span>
                    <span class="article-read-time"><i class="fas fa-clock"></i> {metadata['read_time']}</span>
                </div>
                <div class="article-tags">
                    {tags_html}
                </div>
            </header>

            <div class="article-body">
                {content_html}
            </div>

            <div class="article-navigation">
                <a href="../index.html" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Back to Blog
                </a>
            </div>
        </div>
    </article>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Navya Sri Nizamkari. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
    
    return html_template

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_post.py your-article.md")
        print("Example: python3 add_post.py my-new-post.md")
        return
    
    markdown_file = sys.argv[1]
    
    if not os.path.exists(markdown_file):
        print(f"Error: File {markdown_file} not found!")
        return
    
    # Read markdown file
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Extract metadata
    metadata = extract_metadata(content)
    filename = os.path.basename(markdown_file)
    file_id = filename.replace('.md', '')
    
    print(f"Processing: {filename}")
    print(f"Title: {metadata['title']}")
    print(f"Category: {metadata['category']}")
    print(f"Tags: {', '.join(metadata['tags'])}")
    
    # Create directories if needed
    os.makedirs('blog/articles', exist_ok=True)
    
    # Copy markdown to articles directory
    target_md = f'blog/articles/{filename}'
    if not os.path.exists(target_md):
        with open(target_md, 'w') as f:
            f.write(content)
        print(f"✓ Created {target_md}")
    
    # Generate HTML
    content_html = markdown_to_html(content, metadata)
    html_content = create_html_file(filename, metadata, content_html)
    
    html_file = f'blog/articles/{file_id}.html'
    with open(html_file, 'w') as f:
        f.write(html_content)
    print(f"✓ Created {html_file}")
    
    # Update articles.json
    articles_json = 'blog/articles.json'
    if os.path.exists(articles_json):
        with open(articles_json, 'r') as f:
            articles = json.load(f)
    else:
        articles = []
    
    # Add new article (check if not already exists)
    existing = [a for a in articles if a.get('id') == file_id]
    if not existing:
        new_article = {
            "id": file_id,
            "title": metadata['title'],
            "excerpt": metadata['excerpt'],
            "date": metadata['date'],
            "category": metadata['category'],
            "tags": metadata['tags'],
            "readTime": metadata['read_time'],
            "filename": filename
        }
        articles.insert(0, new_article)  # Add to beginning
        
        with open(articles_json, 'w') as f:
            json.dump(articles, f, indent=2)
        print(f"✓ Updated {articles_json}")
    
    print(f"""
🎉 Blog post ready!

Next steps:
1. git add .
2. git commit -m "Add blog post: {metadata['title']}"
3. git push

Your post will be live at:
https://navyanizamkari.github.io/blog/articles/{file_id}.html
""")

if __name__ == "__main__":
    main()