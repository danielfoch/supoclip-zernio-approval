# SupoClip + Zernio Approval Workflow

OpenClaw skill/install package for turning long-form market videos into vertical short-form clips, generating a caption, requesting human approval, then publishing through Zernio only after approval.

## What it does

1. Downloads or uses a local source video.
2. Renders a 9:16 SupoClip/OpusClip-style short:
   - default first 2:45 cut;
   - burned captions;
   - opening hook text;
   - face-only intro when the source starts as a single talking-head layout;
   - true vertically stacked split-screen once the source switches to chart/screen-share layout;
   - no stretching;
   - no default branding label.
3. Generates a platform-safe caption.
4. Sends an approval request with:
   - rendered video;
   - sample caption;
   - target platforms;
   - clear approve/reject instruction.
5. Publishes via Zernio only after explicit approval.

## Install

```bash
./install.sh
```

This copies the skill into:

```text
~/.openclaw/skills/supoclip-zernio-approval/
```

## Requirements

- `ffmpeg`
- `python3`
- Python packages: `opencv-python`, `pillow`, `yt-dlp` optional for YouTube download
- `zernio` CLI authenticated with connected social accounts
- OpenClaw message channel configured for approval requests

## Quick start

Render a local video:

```bash
python3 scripts/render_supoclip.py \
  --input path/to/source.mp4 \
  --captions path/to/source.en.vtt \
  --output out/clip.mp4 \
  --hook "Sales are up, but prices are still falling." \
  --duration 165
```

Upload/publish after approval:

```bash
python3 scripts/zernio_publish.py \
  --video out/clip.mp4 \
  --caption-file examples/caption.txt \
  --accounts "LINKEDIN_ID,INSTAGRAM_ID,TIKTOK_ID,FACEBOOK_ID,YOUTUBE_ID" \
  --title "Sales Are Up. Prices Are Down. Toronto Market Update"
```

## Approval protocol

The skill must not publish immediately. It should first send:

```text
Clip is ready for approval.

Caption:
[caption]

Targets:
LinkedIn, Instagram, TikTok, Facebook, YouTube Shorts

Reply APPROVE to publish, EDIT with changes, or REJECT to stop.
```

Only run the Zernio publish step after the user clearly approves.

## Security

- Do not commit API keys, Zernio keys, Telegram IDs, cookies, or platform tokens.
- Do not publish without explicit approval.
- Preserve raw source/caption files locally only as needed.
