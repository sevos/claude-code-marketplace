#!/usr/bin/env node
/**
 * Tengwar Rendering Script
 *
 * Converts Latin text to Tengwar and renders it as SVG.
 * Supports multiple output formats for different use cases.
 *
 * Usage:
 *   node render-tengwar.js "mae govannen" --format svg
 *   node render-tengwar.js "elen sila" --format inline
 *   node render-tengwar.js "mellon" --format html --output greeting.html
 *
 * Requirements:
 *   npm install text-to-svg tengwar
 */

const fs = require('fs');
const path = require('path');

// Check for required dependencies
let TextToSVG, tengwar;
try {
  TextToSVG = require('text-to-svg');
} catch (e) {
  console.error('Missing dependency: text-to-svg');
  console.error('Run: npm install text-to-svg');
  process.exit(1);
}

try {
  tengwar = require('tengwar/general-use');
} catch (e) {
  console.error('Missing dependency: tengwar');
  console.error('Run: npm install tengwar');
  process.exit(1);
}

// Configuration
const CONFIG = {
  // Default font path - update this to your font location
  fontPath: process.env.TENGWAR_FONT_PATH || path.join(__dirname, '../fonts/tengwar-annatar.ttf'),

  // Default SVG options
  defaultFontSize: 48,
  defaultFill: 'currentColor',

  // CDN font URL for HTML output
  cdnFontUrl: 'https://fonts.cdnfonts.com/css/tengwar-annatar',
  fontFamily: 'Tengwar Annatar'
};

/**
 * Transcribe Latin text to Tengwar font encoding
 * @param {string} text - Latin text to transcribe
 * @param {string} mode - Transcription mode (general-use, classical, beleriand)
 * @returns {string} - Text encoded for Tengwar font
 */
function transcribeToTengwar(text, mode = 'general-use') {
  try {
    let transcriber;
    switch (mode) {
      case 'classical':
        transcriber = require('tengwar/classical');
        break;
      case 'beleriand':
        transcriber = require('tengwar/beleriand');
        break;
      default:
        transcriber = tengwar;
    }
    return transcriber.transcribe(text);
  } catch (e) {
    console.error(`Transcription error: ${e.message}`);
    return text;
  }
}

/**
 * Render Tengwar text as SVG
 * @param {string} text - Already transcribed Tengwar text
 * @param {object} options - Rendering options
 * @returns {string} - SVG markup
 */
function renderToSVG(text, options = {}) {
  const {
    fontSize = CONFIG.defaultFontSize,
    fill = CONFIG.defaultFill,
    fontPath = CONFIG.fontPath
  } = options;

  if (!fs.existsSync(fontPath)) {
    throw new Error(`Font file not found: ${fontPath}\nSet TENGWAR_FONT_PATH environment variable or place font in scripts/../fonts/`);
  }

  const textToSVG = TextToSVG.loadSync(fontPath);

  const svgOptions = {
    fontSize,
    anchor: 'left top',
    attributes: { fill }
  };

  return textToSVG.getSVG(text, svgOptions);
}

/**
 * Render Tengwar as inline SVG (for embedding in documents)
 * @param {string} text - Already transcribed Tengwar text
 * @param {object} options - Rendering options
 * @returns {string} - Inline SVG with viewBox for scaling
 */
function renderToInlineSVG(text, options = {}) {
  const {
    fontSize = CONFIG.defaultFontSize,
    fill = CONFIG.defaultFill,
    fontPath = CONFIG.fontPath,
    height = '1.5em'
  } = options;

  if (!fs.existsSync(fontPath)) {
    throw new Error(`Font file not found: ${fontPath}`);
  }

  const textToSVG = TextToSVG.loadSync(fontPath);

  // Get metrics for viewBox
  const metrics = textToSVG.getMetrics(text, { fontSize });
  const pathData = textToSVG.getD(text, { fontSize, anchor: 'left top' });

  const width = Math.ceil(metrics.width);
  const svgHeight = Math.ceil(metrics.height);

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${svgHeight}" style="height: ${height}; vertical-align: middle;"><path d="${pathData}" fill="${fill}"/></svg>`;
}

/**
 * Generate complete HTML page with Tengwar content
 * @param {string} latinText - Original Latin text
 * @param {string} transcribedText - Tengwar-encoded text
 * @param {object} options - HTML generation options
 * @returns {string} - Complete HTML document
 */
function generateHTML(latinText, transcribedText, options = {}) {
  const {
    title = 'Tengwar Text',
    useCDN = true,
    embedFont = false,
    fontBase64 = null
  } = options;

  let fontStyle = '';
  if (useCDN) {
    fontStyle = `<link href="${CONFIG.cdnFontUrl}" rel="stylesheet">`;
  } else if (embedFont && fontBase64) {
    fontStyle = `
    <style>
      @font-face {
        font-family: 'TengwarEmbedded';
        src: url(data:font/woff2;base64,${fontBase64}) format('woff2');
      }
    </style>`;
  }

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  ${fontStyle}
  <style>
    body {
      font-family: 'Georgia', serif;
      max-width: 800px;
      margin: 2rem auto;
      padding: 1rem;
      line-height: 1.6;
    }
    .tengwar {
      font-family: '${useCDN ? CONFIG.fontFamily : 'TengwarEmbedded'}', serif;
      font-size: 2em;
      display: block;
      margin: 1rem 0;
      text-align: center;
    }
    .latin {
      font-style: italic;
      color: #666;
      text-align: center;
    }
    .container {
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 2rem;
      background: #fafafa;
    }
  </style>
</head>
<body>
  <div class="container">
    <p class="tengwar">${transcribedText}</p>
    <p class="latin">${latinText}</p>
  </div>
</body>
</html>`;
}

/**
 * Generate HTML snippet for embedding
 * @param {string} transcribedText - Tengwar-encoded text
 * @returns {string} - HTML snippet with inline styles
 */
function generateHTMLSnippet(transcribedText) {
  return `<span style="font-family: 'Tengwar Annatar', serif; font-size: 1.5em;">${transcribedText}</span>`;
}

// CLI Interface
function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
Tengwar Rendering Script

Usage:
  node render-tengwar.js <text> [options]

Options:
  --format <type>    Output format: svg, inline, html, snippet, transcribe
                     (default: transcribe)
  --mode <mode>      Transcription mode: general-use, classical, beleriand
                     (default: general-use)
  --output <file>    Write output to file instead of stdout
  --font <path>      Path to Tengwar TTF font file
  --font-size <n>    Font size for SVG rendering (default: 48)
  --fill <color>     Fill color for SVG (default: currentColor)
  --height <value>   Height for inline SVG (default: 1.5em)
  --title <title>    Title for HTML output
  --embed-font       Embed font as base64 in HTML (requires --font)

Examples:
  # Just transcribe text
  node render-tengwar.js "mae govannen"

  # Generate full SVG file
  node render-tengwar.js "elen sila" --format svg --output star.svg

  # Generate inline SVG for embedding
  node render-tengwar.js "mellon" --format inline

  # Generate HTML page
  node render-tengwar.js "namarie" --format html --output farewell.html

  # Use classical mode for Quenya
  node render-tengwar.js "Aiya Earendil" --mode classical

Environment:
  TENGWAR_FONT_PATH  Path to Tengwar TTF font (for SVG generation)
`);
    process.exit(0);
  }

  // Parse arguments
  const text = args[0];
  let format = 'transcribe';
  let mode = 'general-use';
  let output = null;
  let fontPath = CONFIG.fontPath;
  let fontSize = CONFIG.defaultFontSize;
  let fill = CONFIG.defaultFill;
  let height = '1.5em';
  let title = 'Tengwar Text';
  let embedFont = false;

  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case '--format':
        format = args[++i];
        break;
      case '--mode':
        mode = args[++i];
        break;
      case '--output':
        output = args[++i];
        break;
      case '--font':
        fontPath = args[++i];
        break;
      case '--font-size':
        fontSize = parseInt(args[++i], 10);
        break;
      case '--fill':
        fill = args[++i];
        break;
      case '--height':
        height = args[++i];
        break;
      case '--title':
        title = args[++i];
        break;
      case '--embed-font':
        embedFont = true;
        break;
    }
  }

  // Transcribe text
  const transcribed = transcribeToTengwar(text, mode);

  let result;
  try {
    switch (format) {
      case 'svg':
        result = renderToSVG(transcribed, { fontSize, fill, fontPath });
        break;
      case 'inline':
        result = renderToInlineSVG(transcribed, { fontSize, fill, fontPath, height });
        break;
      case 'html':
        let fontBase64 = null;
        if (embedFont && fs.existsSync(fontPath)) {
          fontBase64 = fs.readFileSync(fontPath).toString('base64');
        }
        result = generateHTML(text, transcribed, {
          title,
          useCDN: !embedFont,
          embedFont,
          fontBase64
        });
        break;
      case 'snippet':
        result = generateHTMLSnippet(transcribed);
        break;
      case 'transcribe':
      default:
        result = transcribed;
        break;
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }

  // Output result
  if (output) {
    fs.writeFileSync(output, result);
    console.log(`Output written to: ${output}`);
  } else {
    console.log(result);
  }
}

// Export functions for programmatic use
module.exports = {
  transcribeToTengwar,
  renderToSVG,
  renderToInlineSVG,
  generateHTML,
  generateHTMLSnippet,
  CONFIG
};

// Run CLI if executed directly
if (require.main === module) {
  main();
}
