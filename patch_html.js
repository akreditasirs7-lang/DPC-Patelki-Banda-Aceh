const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// Replace inner <style>...</style> blocks with <link rel="stylesheet" href="styles.css">
// Note: there are two style blocks in head.
html = html.replace(/<style>[\s\S]*?<\/style>/g, '');
html = html.replace(/<head>/, `<head>\n    <link rel="stylesheet" href="styles.css">\n`);

// Replace the script blocks at the end
// Let's remove everything from the first <script> after </div> up to </body>
html = html.replace(/<script>[\s\S]*?<\/body>/, '<script src="script.js"></script>\n</body>');

fs.writeFileSync('index.html', html);
console.log('index.html patched successfuly');
