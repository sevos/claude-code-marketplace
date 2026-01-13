# temporary-upload

Upload files to paste.sevos.io for temporary sharing with configurable expiry.

## Features

- Upload any file type with 7-day default expiry
- Custom expiry times (minutes to years)
- One-shot uploads (deleted after first view)
- URL shortening
- HTML files render directly in browser
- Secure authentication via 1Password CLI

## Prerequisites

- [1Password CLI](https://developer.1password.com/docs/cli/) (`op`) installed and configured
- 1Password item named "Rustypaste - paste.sevos.io" with password field

## Usage

This is a skill-based plugin. Claude will automatically use it when you:

- Ask to "upload a file" or "share this"
- Request a "shareable link" or "temporary hosting"
- Create HTML artifacts that could be shared
- Mention "preview", "demo", or sharing content

## Examples

```
"Upload this HTML page so I can share it"
"Get me a temporary link for this file"
"Share this code snippet"
"Host this for 1 hour only"
```

## File Type Behavior

| Type | Behavior |
|------|----------|
| HTML | Rendered in browser |
| Text, JSON, XML | Displayed as text |
| Images | Displayed inline |
| PDF | Browser PDF viewer |
| Other | Downloaded |
