#!/usr/bin/env python3
"""
Substack to Website Sync (No Dependencies Version)

This script pulls your latest articles from Substack and displays them on your website.
Uses only built-in Python libraries - no external dependencies needed!

Usage:
    python3 sync_substack.py navyanizamkari
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import os
import sys
from datetime import datetime
from html import unescape

def clean_html(html_content):
    """Convert HTML to clean text and preserve basic formatting"""
    # Remove HTML tags but keep basic structure
    text = re.sub(r'<[^>]+>', '', html_content)
    # Unescape HTML entities
    text = unescape(text)
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_excerpt(content, max_length=200):
    """Extract a clean excerpt from content"""
    clean_content = clean_html(content)
    if len(clean_content) <= max_length:
        return clean_content
    return clean_content[:max_length] + "..."

def estimate_read_time(content):
    """Estimate reading time based on word count"""
    clean_content = clean_html(content)
    word_count = len(clean_content.split())
    # Average reading speed is 200-250 words per minute
    minutes = max(1, round(word_count / 225))
    return f"{minutes} min read"

def parse_rss_date(date_str):
    """Parse RSS date string to datetime"""
    try:
        # Try common RSS date formats
        for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%dT%H:%M:%S%z']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # If no format works, just return current time
        return datetime.now()
    except:
        return datetime.now()

def fetch_substack_posts(substack_name):
    """Fetch posts from Substack RSS feed using built-in libraries"""
    rss_url = f"https://{substack_name}.substack.com/feed"
    
    print(f"Fetching posts from: {rss_url}")
    
    try:
        # Fetch the RSS feed
        with urllib.request.urlopen(rss_url) as response:
            rss_data = response.read().decode('utf-8')
        
        # Parse XML
        root = ET.fromstring(rss_data)
        
        posts = []
        
        # Find all item elements
        for item in root.findall('.//item'):
            title_elem = item.find('title')
            link_elem = item.find('link')
            description_elem = item.find('description')
            pub_date_elem = item.find('pubDate')
            guid_elem = item.find('guid')
            
            if title_elem is None or link_elem is None:
                continue
            
            title = title_elem.text or "Untitled"
            link = link_elem.text or ""
            content = description_elem.text or "" if description_elem is not None else ""
            
            # Parse date
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    pub_date = parse_rss_date(pub_date_elem.text)
                    date_str = pub_date.strftime('%Y-%m-%d')
                    formatted_date = pub_date.strftime('%B %d, %Y')
                except:
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    formatted_date = "Recently"
            else:
                date_str = datetime.now().strftime('%Y-%m-%d')
                formatted_date = "Recently"
            
            # Create ID from guid or link
            post_id = ""
            if guid_elem is not None and guid_elem.text:
                post_id = guid_elem.text.split('/')[-1] if '/' in guid_elem.text else guid_elem.text
            else:
                post_id = link.split('/')[-1] if '/' in link else "post"
            
            post = {
                'title': title,
                'link': link,
                'content': content,
                'excerpt': extract_excerpt(content),
                'date': date_str,
                'formatted_date': formatted_date,
                'read_time': estimate_read_time(content),
                'id': post_id
            }
            posts.append(post)
        
        print(f"Found {len(posts)} posts")
        return posts
    
    except Exception as e:
        print(f"Error fetching Substack posts: {e}")
        return []

def create_blog_card_html(post):
    """Create HTML for a single blog post card"""
    return f'''<div class="blog-post-card">
    <div class="post-header">
        <h3><a href="{post['link']}" target="_blank">{post['title']}</a></h3>
        <div class="post-meta">
            <span class="post-date"><i class="fas fa-calendar"></i> {post['formatted_date']}</span>
            <span class="post-category"><i class="fas fa-external-link-alt"></i> Substack</span>
            <span class="read-time"><i class="fas fa-clock"></i> {post['read_time']}</span>
        </div>
    </div>
    <p class="post-excerpt">{post['excerpt']}</p>
    <div class="post-tags">
        <span class="tag">Substack</span>
        <span class="tag">External Link</span>
    </div>
</div>'''

def update_blog_index(posts, substack_name):
    """Update the blog index.html with Substack posts"""
    index_file = 'blog/index.html'
    
    if not os.path.exists(index_file):
        print(f"Error: {index_file} not found!")
        return
    
    # Read current file
    with open(index_file, 'r') as f:
        content = f.read()
    
    # Generate new blog posts HTML
    blog_cards = '\n\n                    '.join([create_blog_card_html(post) for post in posts])
    
    # Create new blog posts section
    new_posts_section = f'''                <!-- Blog Posts from Substack -->
                <div class="blog-posts">
                    {blog_cards}
                </div>

                <!-- Subscribe Section -->
                <div class="subscribe-section">
                    <h3>Subscribe on Substack</h3>
                    <p>Get new posts delivered directly to your inbox!</p>
                    <a href="https://{substack_name}.substack.com" class="btn btn-primary" target="_blank">
                        <i class="fas fa-external-link-alt"></i> Visit My Substack
                    </a>
                </div>'''
    
    # Replace the existing blog content section
    # Look for the blog-content div and replace its content
    pattern = r'(<div class="blog-content">)(.*?)(</div>\s*</div>\s*<!-- Sidebar -->)'
    
    def replace_content(match):
        return f'{match.group(1)}\n{new_posts_section}\n            {match.group(3)}'
    
    updated_content = re.sub(pattern, replace_content, content, flags=re.DOTALL)
    
    # Write updated content
    with open(index_file, 'w') as f:
        f.write(updated_content)
    
    print(f"✓ Updated {index_file} with {len(posts)} Substack posts")

def create_substack_config(substack_name):
    """Create a config file to remember the Substack name"""
    config = {
        'substack_name': substack_name,
        'last_updated': datetime.now().isoformat()
    }
    
    with open('substack_config.json', 'w') as f:
        json.dump(config, f, indent=2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 sync_substack.py your-substack-name")
        print("Example: python3 sync_substack.py navyanizamkari")
        return
    
    substack_name = sys.argv[1]
    
    print(f"Syncing posts from {substack_name}.substack.com...")
    
    # Fetch posts
    posts = fetch_substack_posts(substack_name)
    
    if not posts:
        print("No posts found or error occurred.")
        return
    
    # Update blog index
    update_blog_index(posts, substack_name)
    
    # Save config
    create_substack_config(substack_name)
    
    print(f"""
🎉 Substack sync complete!

Synced {len(posts)} posts from {substack_name}.substack.com

Next steps:
1. git add .
2. git commit -m "Sync latest Substack posts"  
3. git push

Your blog will show your Substack posts at:
https://navyanizamkari.github.io/blog/

To sync again after publishing new Substack posts:
python3 sync_substack.py {substack_name}
""")

if __name__ == "__main__":
    main()