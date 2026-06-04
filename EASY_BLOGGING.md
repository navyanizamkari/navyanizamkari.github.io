# Super Easy Blog Posting! 🚀

Adding new blog posts is now **incredibly simple**!

## Quick Start (3 steps!)

### 1. Write your article in markdown
Create a file anywhere (like `my-post.md`) with this format:

```markdown
# My Amazing Article Title

*Published: 2024-03-20 | Category: Machine Learning | Read time: 5 min*

## Introduction

Your content here with **bold text** and `code snippets`.

### Code Examples

```python
def hello():
    return "Hello World!"
```

## Conclusion

Your conclusion here.

---

*Questions? Email me at [navyasritech@gmail.com](mailto:navyasritech@gmail.com)*
```

### 2. Run the magic script
```bash
python3 add_post.py my-post.md
```

### 3. Commit and push
```bash
git add .
git commit -m "Add new blog post"
git push
```

**That's it!** Your blog post is live! 🎉

## What the script does automatically:

✅ **Copies** your markdown to the right folder  
✅ **Generates** HTML version with proper styling  
✅ **Updates** articles.json with metadata  
✅ **Extracts** title, date, and tags automatically  
✅ **Creates** excerpt from your content  
✅ **Tells you** exactly what to commit  

## Examples:

```bash
# Add a new ML article
python3 add_post.py neural-networks-guide.md

# Add a career post  
python3 add_post.py my-journey-to-apple.md

# Add a technical tutorial
python3 add_post.py building-apis-python.md
```

## Pro Tips:

- **Title**: Use `# Your Title` as the first line
- **Date**: Include `*Published: YYYY-MM-DD | Category: YourCategory | Read time: X min*` 
- **Tags**: Script auto-detects tags from your content (LLMs, Production, Mobile, etc.)
- **Code**: Use triple backticks for code blocks
- **Links**: Normal markdown links work: `[text](url)`

**Your blog is now super easy to update! Just write markdown and run one command.** 📝✨