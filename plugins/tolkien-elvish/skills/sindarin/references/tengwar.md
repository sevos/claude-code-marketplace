# Tengwar Script Reference

Tengwar is the Elvish writing system created by J.R.R. Tolkien, used to write Quenya, Sindarin, and other languages of Middle-earth. This reference covers rendering Tengwar for web and digital applications.

## Unicode Status

Tengwar is **NOT in official Unicode**. The Tolkien Estate has declined to permit standardization. All implementations use:

- **ConScript Unicode Registry (CSUR)**: Private Use Area U+E000-U+E07F
- **Font-specific mappings**: Each font has its own character-to-glyph mappings

## Available Fonts

### Recommended Fonts

| Font | License | CDN Available | Notes |
|------|---------|---------------|-------|
| **Tengwar Annatar** | Freeware | Yes (CDNFonts) | Most popular, multiple variants |
| **Alcarin Tengwar** | SIL OFL 1.1 | No | High-quality, academic design |
| **Tengwar Formal CSUR** | SIL OFL 1.1 | No | CSUR-compatible |
| **FreeMonoTengwar** | GPL v3 | No | Monospace variant |

### CDN Usage

```html
<!-- Tengwar Annatar via CDNFonts -->
<link href="https://fonts.cdnfonts.com/css/tengwar-annatar" rel="stylesheet">

<!-- Other Tengwar fonts on CDNFonts -->
<link href="https://fonts.cdnfonts.com/css/tengwar-sindarin" rel="stylesheet">
<link href="https://fonts.cdnfonts.com/css/tengwar-cursive" rel="stylesheet">
<link href="https://fonts.cdnfonts.com/css/tengwar-quenya" rel="stylesheet">
```

```css
.tengwar {
  font-family: 'Tengwar Annatar', serif;
  font-size: 1.5em;
}
```

### Font Downloads

- **Alcarin Tengwar**: https://github.com/Tosche/Alcarin-Tengwar
- **Free Tengwar Font Project**: https://freetengwar.sourceforge.net/
- **DaFont Tengwar Annatar**: https://www.dafont.com/tengwar-annatar.font

## Transcription Libraries

Tengwar fonts map Latin keyboard characters to Tengwar glyphs. You need a transcription library to convert readable text to the correct font mappings.

### TengwarJS (Recommended)

**npm**: `tengwar`

```bash
npm install tengwar
```

**Browser usage**:
```html
<script src="https://cdn.jsdelivr.net/npm/tengwar@1.2.6/tengwar.min.js"></script>
<link rel="stylesheet" href="tengwar-annatar.css">

<!-- Automatic transcription -->
<span class="tengwar annatar" data-tengwar="mae govannen"></span>
```

**Node.js usage**:
```javascript
const { transcribe, encode, parse } = require('tengwar/general-use');

// Transcribe phonetic Latin to Tengwar font bindings
const result = transcribe('mae govannen');
// Returns characters that render correctly with Tengwar Annatar font
```

**Modes**:
- `tengwar/general-use` - For Sindarin and general text
- `tengwar/classical` - For Quenya
- `tengwar/beleriand` - Mode of Beleriand

### Glaemscribe (Most Comprehensive)

**npm**: `glaemscribe`

```bash
npm install glaemscribe
```

**CDN**:
```html
<script src="https://cdn.jsdelivr.net/npm/glaemscribe@1.3.1/lib/api/glaemscribe.min.js"></script>
```

**Features**:
- Multiple language modes: Quenya, Sindarin, English, Spanish, Italian, Japanese
- Multiple writing systems: Tengwar, Cirth, Sarati
- Extensive mode customization

**License**: GNU AGPL v3 (copyleft)

### Tecendil-JS

Open source engine behind tecendil.com:
- Repository: https://github.com/arnog/tecendil-js
- License: MIT

## Rendering Methods

### Method 1: CSS @font-face with CDN

Best for: Simple web pages with Tengwar content.

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.cdnfonts.com/css/tengwar-annatar" rel="stylesheet">
  <style>
    .tengwar {
      font-family: 'Tengwar Annatar', serif;
      font-size: 2em;
      direction: ltr;
    }
  </style>
</head>
<body>
  <p class="tengwar"><!-- Transcribed Tengwar characters --></p>

  <!-- With TengwarJS for auto-transcription -->
  <p class="tengwar annatar" data-tengwar="Elen síla lúmenn' omentielvo"></p>
  <script src="tengwar.min.js"></script>
</body>
</html>
```

### Method 2: SVG Path Generation

Best for: Claude web interface, self-contained rendering, high-quality scalable output.

```javascript
const TextToSVG = require('text-to-svg');

// Load Tengwar font
const textToSVG = TextToSVG.loadSync('./fonts/tengwar-annatar.ttf');

// Generate SVG from transcribed text
function renderTengwarSVG(transcribedText, options = {}) {
  const defaults = {
    fontSize: 48,
    anchor: 'left top',
    attributes: { fill: 'currentColor' }
  };

  return textToSVG.getSVG(transcribedText, { ...defaults, ...options });
}

// Returns complete <svg> element
const svg = renderTengwarSVG(transcribedText);
```

### Method 3: Base64 Embedded Font

Best for: Self-contained HTML files with no external dependencies.

```html
<style>
@font-face {
  font-family: 'TengwarEmbedded';
  src: url(data:font/woff2;base64,d09GMgABAAAAA...) format('woff2');
}
.tengwar { font-family: 'TengwarEmbedded', serif; }
</style>
```

To generate base64:
```javascript
const fs = require('fs');
const fontBase64 = fs.readFileSync('tengwar-annatar.woff2').toString('base64');
console.log(`data:font/woff2;base64,${fontBase64}`);
```

### Method 4: Canvas Rendering

Best for: Dynamic graphics, game interfaces, image generation.

```javascript
// Load font using FontFace API
const tengwarFont = new FontFace('TengwarAnnatar',
  'url(/fonts/tengwar-annatar.woff2)');

tengwarFont.load().then(font => {
  document.fonts.add(font);

  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  ctx.font = '48px TengwarAnnatar';
  ctx.fillStyle = '#000';
  ctx.fillText(transcribedText, 10, 50);
});
```

## Inline SVG for Claude Web Interface

For rendering Tengwar inline in Claude's web interface (where external fonts may not load), use pre-rendered inline SVG:

```html
<!-- Self-contained inline SVG -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" style="height: 1.5em; vertical-align: middle;">
  <path d="M10,40 ... [path data from text-to-svg]" fill="currentColor"/>
</svg>
```

This approach:
- Works without external font loading
- Scales perfectly (vector)
- Inherits text color via `currentColor`
- Renders immediately

## Tengwar Mode Selection

Different modes map sounds to Tengwar differently:

| Mode | Use For | Library Path |
|------|---------|--------------|
| General Use | Sindarin, modern text | `tengwar/general-use` |
| Classical | Quenya | `tengwar/classical` |
| Beleriand | Mode of Beleriand | `tengwar/beleriand` |
| English | English text | Glaemscribe modes |

### Mode Examples

**General Use (Sindarin)**:
- "mae govannen" → Tengwar for [m-a-e g-o-v-a-n-n-e-n]

**Classical (Quenya)**:
- "Elen síla" → Tengwar with tehtar (diacritics) above consonants

## Common Tengwar Characters

### Primary Letters (Tengwar)

| Tengwar | Sound | Name |
|---------|-------|------|
| 1 | t | tinco |
| 2 | p | parma |
| 3 | c/k | calma |
| 4 | qu | quessë |
| q | nd | ando |
| w | mb | umbar |
| e | ng | anga |
| r | ngw | ungwë |

### Tehtar (Vowel Diacritics)

Vowels are typically written as marks (tehtar) above or below consonants:
- **a** - three dots above
- **e** - acute accent
- **i** - single dot above
- **o** - right curl
- **u** - left curl

## Online Tools

| Tool | URL | Features |
|------|-----|----------|
| **Tecendil** | https://www.tecendil.com/ | Most accurate, export options |
| **Tengwar Transcriber** | https://tengwar.3rin.gs/ | Multiple modes |
| **Tengwar Feanor** | https://tengwartranscriber.github.io/ | Simple interface |

## Implementation Checklist

For HTML pages:
- [ ] Include CDN font link or embed font as base64
- [ ] Include TengwarJS or use pre-transcribed text
- [ ] Apply `.tengwar` class with proper font-family
- [ ] Set appropriate font-size (Tengwar often needs larger sizing)

For inline rendering (Claude):
- [ ] Pre-render text as SVG paths using text-to-svg
- [ ] Use inline `<svg>` with `viewBox` for scaling
- [ ] Set `fill="currentColor"` for theme compatibility

## Licensing Notes

| Resource | License | Commercial Use |
|----------|---------|----------------|
| Tengwar Annatar | Freeware | Requires providing copy to creator |
| Alcarin Tengwar | SIL OFL 1.1 | Yes, freely |
| Tengwar Formal CSUR | SIL OFL 1.1 | Yes, freely |
| TengwarJS | MIT | Yes |
| Glaemscribe | AGPL v3 | Yes (copyleft applies) |
| Tecendil-JS | MIT | Yes |

**Legal Note**: The Tolkien Estate may have intellectual property claims over Tengwar itself for commercial projects. Consult legal advice for commercial use.
