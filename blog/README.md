# Blog System - Adding New Articles

This directory contains your blog system with a simple structure for adding new articles.

## Directory Structure

```
blog/
├── index.html              # Main blog page
├── articles.json          # Article metadata
├── articles/              # Article files
│   ├── *.md              # Markdown source files
│   └── *.html            # HTML versions for web display
└── README.md             # This file
```

## Adding New Articles

### 1. Create Your Article

Create a new markdown file in `blog/articles/` with a descriptive filename:

```bash
# Example filename
blog/articles/my-new-article.md
```

### 2. Article Format

Use this template for your markdown file:

```markdown
# Article Title Here

*Published: YYYY-MM-DD | Category: Your Category | Read time: X min*

## Introduction

Your introduction here...

## Main Content

Your main content with:

- **Bold text** for emphasis
- `code snippets` for technical terms
- Links to [external resources](https://example.com)

### Code Examples

```python
# Python code example
def example_function():
    return "Hello, World!"
```

## Conclusion

Your conclusion here...

---

*Have questions? Reach out via [email](mailto:navyasritech@gmail.com) or [LinkedIn](https://linkedin.com/in/navyanizamkari).*
```

### 3. Update Article Metadata

Add your article to `blog/articles.json`:

```json
{
  "id": "my-new-article",
  "title": "My Article Title",
  "excerpt": "Brief description of your article...",
  "date": "2024-MM-DD",
  "category": "Your Category",
  "tags": ["tag1", "tag2", "tag3"],
  "readTime": "X min",
  "filename": "my-new-article.md"
}
```

### 4. Create HTML Version

Create an HTML file with the same name in `blog/articles/`:
- Copy the structure from existing HTML files
- Replace content with your article content
- Update title, meta tags, and navigation

### 5. Update Blog Index

Add your article to the main blog page (`blog/index.html`):
- Add a new `blog-post-card` div with your article details
- Update the link to point to your HTML file

## Quick Steps for New Articles

1. **Write** your article in markdown format
2. **Add** metadata to `articles.json`  
3. **Create** HTML version using existing templates
4. **Update** the blog index page
5. **Commit** and push your changes

## Categories

Current categories:
- Machine Learning
- AI Systems
- Technology
- Career
- Open Source

## Tags

Use relevant tags to help readers find related content:
- LLMs, Production, Optimization
- Edge Computing, Mobile ML
- Privacy, Security
- Infrastructure, Scaling

## Tips

- Keep filenames lowercase with hyphens (kebab-case)
- Use descriptive titles and excerpts
- Include estimated read time
- Add relevant tags for discoverability
- Test your HTML files before committing