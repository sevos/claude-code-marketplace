# video-transcript-downloader

Download videos, audio, subtitles, and clean transcripts from YouTube and other yt-dlp supported sites.

## Features

- Extract clean paragraph-style transcripts (no timestamps by default)
- Download videos in best quality
- Extract audio as MP3
- Download subtitle files
- List available formats
- Supports 1000+ sites via yt-dlp

## Prerequisites

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed and on PATH
- [ffmpeg](https://ffmpeg.org/) for audio extraction
- Node.js for the bundled script

## Installation

Dependencies are installed automatically on first use, or manually:

```bash
cd skills/video-transcript-downloader/scripts && npm ci
```

## Usage

This is a skill-based plugin. Claude will automatically use it when you:

- Ask to "download this video" or "get the transcript"
- Request to "rip audio" or "get subtitles"
- Mention YouTube URLs or video/audio extraction
- Need to troubleshoot yt-dlp or formats

## Examples

```
"Get the transcript from this YouTube video: https://..."
"Download this video to my Downloads folder"
"Extract audio from this clip as MP3"
"What formats are available for this video?"
```

## Commands

| Command | Purpose |
|---------|---------|
| `transcript` | Extract text transcript |
| `download` | Download video |
| `audio` | Extract audio as MP3 |
| `subs` | Download subtitle file |
| `formats` | List available formats |
