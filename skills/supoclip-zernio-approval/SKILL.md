---
name: supoclip-zernio-approval
description: Render SupoClip/OpusClip-style real estate shorts, generate captions, request approval, and publish via Zernio only after explicit approval. Use when asked to clip a YouTube/video and post to LinkedIn, Instagram, TikTok, Facebook, or YouTube Shorts with approval gate.
---

# SupoClip + Zernio Approval

## Objective

Create a vertical short from a source video, send the user a rendered sample + caption for approval, then publish through Zernio only after explicit approval.

## Non-Negotiables

- Never publish without explicit user approval.
- Send the actual rendered video, not just a local path.
- Include the proposed caption in the approval request.
- Ask for approval in plain language: `Reply APPROVE to publish, EDIT with changes, or REJECT to stop.`
- No default `REALIST.CA MARKET CLIP` branding or bottom label.
- Do not stretch video. All crops must preserve aspect ratio.
- Keep platform tokens/API keys out of prompts, files, commits, and captions.

## Default Clip Format

- Default cut: first 2:45 unless instructed otherwise.
- Vertical output: 720x1280 or 1080x1920, 9:16.
- Burn captions.
- Add opening auto-hook/summary text for ~5-6 seconds.
- If the video begins as face/talking-head before switching to split-screen:
  - intro section: face-only vertical crop;
  - after visual split: stacked vertical split-screen.

## Crop Rules

- Never resize an arbitrary crop into the output if aspect ratios do not match.
- Full 9:16 output from 1920x1080 source: crop approximately `608x1080` around detected face, then scale.
- Stacked halves are 720x640 = 9:8. For market videos with Dan left / screen right:
  - top face crop: `x=0, y=114, w=960, h=853`;
  - bottom screen crop: `x=960, y=114, w=960, h=853`;
  - scale each to 720x640 and stack.
- Detect or inspect the split transition. Do not guess blindly.
- Validate sample frames before sending.

## Validation Before Approval

Export/contact-sheet sample frames at roughly:

- 5s
- 30s
- 60s
- 120s
- 160s

Confirm:

- face-only intro is centered and not cutting off the face;
- split-screen section actually switches to stacked layout;
- captions are readable;
- no stretching;
- no unwanted branding.

## Caption Style

Use Daniel Foch voice:

- direct;
- market-literate;
- no hype;
- explains the counterintuitive point;
- short paragraphs;
- 3-6 hashtags max.

Example:

```text
Toronto is doing the thing that confuses people:

Sales are up.
Prices are down.

That usually means the market is more liquid, not necessarily stronger.

More deals are happening because sellers are finally meeting the market. Buyers are still price-sensitive, rates still matter, and inventory is giving them options.

Transaction volume can recover before prices do.

That distinction matters if you're trying to read the housing market properly.

#TorontoRealEstate #CanadianRealEstate #HousingMarket #RealEstate #Economics
```

## Approval Request Template

Send the rendered video as media/document, then send:

```text
Clip is ready for approval.

Caption:
[caption]

Targets:
[target platforms]

Reply APPROVE to publish, EDIT with changes, or REJECT to stop.
```

If the channel supports buttons, include:

- Approve + publish
- Edit caption
- Reject

## Zernio Publish

After approval only:

1. Upload media:

```bash
zernio media:upload <video> --pretty
```

2. Publish:

```bash
zernio posts:create \
  --text "$(cat caption.txt)" \
  --title "<title>" \
  --accounts "<comma-separated-account-ids>" \
  --media "<zernio-media-url>" \
  --hashtags "TorontoRealEstate,CanadianRealEstate,HousingMarket,RealEstate,Economics" \
  --pretty
```

3. Verify result:

```bash
zernio posts:get <post_id> --pretty
```

4. Report published URLs and any still-processing platforms.

## Definition of Done

- Clip rendered and validated.
- Caption drafted.
- User approval requested with video + caption.
- If approved: Zernio published to requested platforms.
- Final response includes post URLs/status.
