#!/usr/bin/env python3
"""
Substack to Website Sync

This script pulls your latest articles from Substack and displays them on your website.
Write in Substack (easy!) and automatically sync to your personal site.

Usage:
    python3 sync_substack.py your-substack-name

Example:
    python3 sync_substack.py navya  # for navya.substack.com
"""

import feedparser
import json
import re
import os
import sys
from datetime import datetime

def clean_html(html_content):
    """Convert HTML to clean text and preserve basic formatting"""
    # Remove HTML tags but keep basic structure
    text = re.sub(r'<[^>]+>', '', html_content)
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

def fetch_substack_posts(substack_name):
    """Fetch posts from Substack RSS feed"""
    rss_url = f"https://{substack_name}.substack.com/feed"
    
    print(f"Fetching posts from: {rss_url}")
    
    try:
        feed = feedparser.parse(rss_url)
        
        if feed.status != 200:
            print(f"Error: Could not fetch feed. Status: {feed.status}")
            return []
        
        posts = []
        for entry in feed.entries:
            # Parse date
            try:
                pub_date = datetime(*entry.published_parsed[:6])
                date_str = pub_date.strftime('%Y-%m-%d')
                formatted_date = pub_date.strftime('%B %d, %Y')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
                formatted_date = "Recently"
            
            # Extract content
            content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
            
            post = {
                'title': entry.title,
                'link': entry.link,
                'content': content,
                'excerpt': extract_excerpt(content),
                'date': date_str,
                'formatted_date': formatted_date,
                'read_time': estimate_read_time(content),
                'id': entry.id.split('/')[-1] if '/' in entry.id else entry.id
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
        print("Example: python3 sync_substack.py navya  # for navya.substack.com")
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