import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# remove styles
html = re.sub(r'<style>[\s\S]*?</style>', '', html)
html = html.replace('<head>', '<head>\n    <link rel="stylesheet" href="styles.css">\n')

# remove scripts at the end
html = re.sub(r'<script>[\s\S]*?</body>', '<script src="script.js"></script>\n</body>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done')
