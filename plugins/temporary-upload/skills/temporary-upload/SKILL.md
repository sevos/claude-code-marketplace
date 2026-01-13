---
name: temporary-upload
description: This skill should be used when the user asks to "upload a file", "share this", "host this temporarily", "get a shareable link", "publish to paste.sevos.io", or mentions sharing HTML pages, code snippets, or artifacts. Proactively offer when user creates HTML artifacts or previews that could be shared.
---

# Temporary Upload

Upload files to paste.sevos.io for temporary sharing via rustypaste. HTML files render directly in browser; other files download or display based on type.

## When to Use

**Proactively offer or trigger when:**
- HTML artifacts or previews are created that could be shared
- Requests include "share", "upload", "publish", or "host" temporarily
- Shareable links are needed for showing content to others
- Code snippets, documents, or files are created for sharing
- "Preview", "demo", or "show to someone" is mentioned

## Defaults

- **Expiry**: 7 days
- **URL format**: Random pet-name URLs (e.g., `happy-tiger.html`)
- **Max file size**: 300MB

## Authentication

Retrieve auth token from 1Password inline. **Never hardcode the token.**

```bash
op item get "Rustypaste - paste.sevos.io" --fields password --reveal
```

## Upload Commands

### Basic Upload

```bash
curl -F "file=@<filepath>" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io
```

### Custom Expiry

Supported units: `s`, `m`, `h`, `d`, `w`, `M`, `y`

```bash
curl -F "file=@<filepath>" \
  -H "expire:1h" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io
```

### One-Shot (Deleted After First View)

```bash
curl -F "oneshot=@<filepath>" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io
```

### Upload from Stdin

```bash
echo '<html><body><h1>Hello</h1></body></html>' | \
  curl -F "file=@-;filename=page.html" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io
```

Or with heredoc:

```bash
curl -F "file=@-;filename=demo.html" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Demo</title></head>
<body><h1>Demo Page</h1></body>
</html>
EOF
```

### URL Shortening

```bash
curl -F "url=https://example.com/very/long/url/path" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io
```

### Custom Filename

```bash
curl -F "file=@<filepath>" \
  -H "filename: my-custom-name.html" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io
```

## File Type Behavior

| File Type | Behavior |
|-----------|----------|
| `.html` | Rendered in browser |
| `.txt`, `.md`, `.json`, `.xml` | Displayed as text |
| `.png`, `.jpg`, `.gif`, `.svg` | Displayed as image |
| `.pdf` | Displayed in browser PDF viewer |
| Other | Downloaded |

Append `?download=true` to force download.

## Post-Upload Behavior

### Standalone Upload (direct user request)

Open HTML files in browser automatically:

```bash
URL=$(curl -sF "file=@page.html" \
  -H "Authorization: $(op item get 'Rustypaste - paste.sevos.io' --fields password --reveal)" \
  https://paste.sevos.io)
echo "$URL"
xdg-open "$URL"
```

For other files, print URL only.

### Within a Workflow (part of larger task)

Return URL only. Do not open browser. Let parent workflow decide what to do with the URL.
