---
name: video-transcript-downloader
description: This skill should be used when the user asks to "download this video", "get the transcript", "save this clip", "rip audio from", "get subtitles for", "transcribe this video", or mentions YouTube URLs, yt-dlp, or video/audio extraction. Use for any video downloading, transcript extraction, or format troubleshooting.
---

# Video Transcript Downloader

Download videos, audio, subtitles, and clean paragraph-style transcripts from YouTube and any yt-dlp supported site.

## Setup

Run once to install dependencies:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts && npm ci
```

## Core Commands

All commands use `${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js`.

### Transcript (Default: Clean Paragraph)

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js transcript --url 'https://...'
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js transcript --url 'https://...' --lang en
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js transcript --url 'https://...' --timestamps
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js transcript --url 'https://...' --keep-brackets
```

**Transcript behavior:**
- YouTube: Fetches via `youtube-transcript-plus` when possible
- Other sites: Pulls subtitles via `yt-dlp`, cleans into paragraph
- Default output: Single paragraph, no timestamps
- Bracketed cues like `[Music]` stripped by default

### Download Video

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js download --url 'https://...' --output-dir ~/Downloads
```

### Download Audio Only

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js audio --url 'https://...' --output-dir ~/Downloads
```

### Download Subtitles

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js subs --url 'https://...' --output-dir ~/Downloads --lang en
```

### List Available Formats

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js formats --url 'https://...'
```

## Advanced Options

### Specific Format Selection

After listing formats, download specific format ID:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js download --url 'https://...' --output-dir ~/Downloads -- --format 137+140
```

### Prefer MP4 Container (Remux)

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js download --url 'https://...' --output-dir ~/Downloads -- --remux-video mp4
```

### Extra yt-dlp Arguments

Pass additional yt-dlp args after `--`:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/video-transcript-downloader/scripts/vtd.js formats --url 'https://...' -- -v
```

## Command Reference

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `transcript` | Extract text transcript | `--lang`, `--timestamps`, `--keep-brackets` |
| `download` | Download video | `--output-dir` |
| `audio` | Extract audio as MP3 | `--output-dir` |
| `subs` | Download subtitle file | `--output-dir`, `--lang` |
| `formats` | List available formats | (none) |

## Prerequisites

Requires `yt-dlp` and `ffmpeg`:

```bash
# Arch Linux
sudo pacman -S yt-dlp ffmpeg

# macOS
brew install yt-dlp ffmpeg

# Verify installation
yt-dlp --version
ffmpeg -version | head -n 1
```

## Troubleshooting

**"missing yt-dlp"**: Install yt-dlp and ensure it's on PATH

**"missing ffmpeg"**: Required for audio extraction; install ffmpeg

**Empty transcript**: Site may not have subtitles; try different `--lang` value

**Format issues**: Use `formats` command to list available formats, then specify with `--format`
