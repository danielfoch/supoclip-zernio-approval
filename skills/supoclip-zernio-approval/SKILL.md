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
- If the video contains any screen share / slides / browser / chart / dashboard content:
  - do **not** render full-face crop throughout;
  - intro/talking-head-only section may use face-only vertical crop;
  - screen-share section must use stacked vertical split-screen or another layout that keeps both Dan and the screen content visible/readable.
- If the video begins as face/talking-head before switching to split-screen:
  - intro section: face-only vertical crop;
  - after visual split: stacked vertical split-screen.

## Layout Planning + Crop Rules

Before rendering, create a simple layout plan for the whole clip. Do **not** assume one transition. The worker must actually inspect/watch enough of the clip to understand the visual structure before choosing layouts.

Required workflow:

1. Sample/inspect the source across the full selected clip, at minimum every 5-10 seconds plus all obvious visual transitions. When available, watch/scrub the clip or generated frame sequence rather than relying only on automated detection.
2. Classify each time range as one of:
   - `talking_head_fullscreen` — Dan/video subject is full screen with no important screen share;
   - `screen_share_split` — Dan + browser/chart/article/dashboard/slides are visible;
   - `broll_fullscreen` — gas pump/street/stock/visual-only footage;
   - `other` — requires manual judgment.
3. Write the segment plan before rendering: `start-end → layout → caption position`.
4. Render each segment with its correct layout, then concatenate.
5. Validate contact sheet against the segment plan. If the output layout does not match the plan, re-render.

Crop/layout rules:

- Never resize an arbitrary crop into the output if aspect ratios do not match.
- `talking_head_fullscreen` must crop-to-fill 9:16. Do not leave black bars or tiny landscape video floating inside vertical canvas.
- `broll_fullscreen` must crop-to-fill 9:16 unless the full frame is essential.
- Full 9:16 output from 1920x1080 source: crop approximately `608x1080` around detected face/subject, then scale.
- `screen_share_split` must **always** use stacked layout. No picture-in-picture, no face-only crop, no decorative-screen judgment. If screen share is active, stacked is the default and expected output.
- Stacked halves are 720x640 = 9:8. For market videos with Dan left / screen right:
  - top face crop: `x=0, y=114, w=960, h=853`;
  - bottom screen crop: `x=960, y=114, w=960, h=853`;
  - scale each to 720x640 and stack.
- Detect or inspect every layout transition. Do not guess blindly.
- Use manual visual inspection if automated split detection is uncertain. A detector returning “no stable split” is **not** enough to choose full-face crop when the source visibly contains screen share, charts, slides, browser windows, dashboards, or article screenshots.
- For Dan market/economics videos, assume screen-share/split-screen can appear, disappear, and reappear unless verified otherwise.
- If any validation frame shows screen content in the source, the final vertical render must preserve that screen content during that segment.
- Validate sample frames before sending.

## Burned Caption Placement

Captions must move with the layout:

- For `talking_head_fullscreen` or `broll_fullscreen` crop-to-fill segments: place captions near the bottom safe area, above platform UI, not across the face/eyes.
- For `screen_share_split` stacked segments: place captions in the center band or lower safe area only if they do not cover important chart/article text. Prefer a readable strip between Dan and screen when possible.
- Never allow caption lines to overlap each other. Increase line spacing/box height or reduce font size before export.
- Do not burn duplicate caption layers. If captions appear slightly overlapped, doubled, shadow-stacked, or ghosted, treat validation as failed and re-render.
- Contact sheet validation must include caption placement for each segment type.

## Validation Before Approval

Export/contact-sheet sample frames at roughly:

- 5s
- 30s
- 60s
- 120s
- 160s

Confirm:

- the contact sheet covers every layout segment in the plan, not just fixed timestamps;
- full-screen/talking-head segments are crop-to-fill 9:16, with no black bars or tiny landscape frame;
- face-only intro/fullscreen sections are centered and not cutting off the face;
- split-screen / screen-share sections actually switch to stacked layout or otherwise keep Dan + screen visible;
- screen text/charts are not cropped out when screen content is being discussed;
- captions move to the correct safe area for each segment type;
- captions are readable and not overlapping/doubled/ghosted;
- no stretching;
- no unwanted branding.

If validation fails because screen-share content is missing, fullscreen content is not crop-to-fill, or captions overlap / sit in the wrong place, re-render before sending. Do not ask for approval on a bad render.

## Caption Style

Use Daniel Foch voice:

- direct;
- market-literate;
- sounds like a human who actually watched the clip;
- no hype;
- no generic AI explainer cadence;
- no “thought leadership” LinkedIn sludge;
- plain phrasing over polished phrasing;
- short paragraphs;
- 3-6 hashtags max.

### Banned AI-slop tells

Do **not** use these patterns in SupoClip/Zernio captions:

- “that distinction matters”
- “here’s the thing”
- “the reality is”
- “what people miss is”
- “the bigger picture”
- “the key takeaway”
- “let’s unpack this”
- “this is important because”
- “in today’s market”
- “now more than ever”
- “it’s not X, it’s Y” when it feels formulaic
- “this tells us…”
- “the data shows…” unless followed by a specific number
- “if you’re trying to…” closing lines
- “pay attention to…”
- “watch this space”
- “game changer”
- “deep dive”
- “unlock” / “leverage” / “navigate” / “empower”
- generic contrast endings like “volume can recover before prices do” followed by an explainer moral
- tidy consultant summaries that sound written by ChatGPT, not Dan

### Caption construction rule

Write captions like Dan texting a sharp market observation:

1. Lead with the uncomfortable fact or contradiction.
2. Use 1-2 specific numbers/details from the clip.
3. Explain the market mechanism in normal language.
4. End bluntly, not with a polished lesson.

Example:

```text
Toronto sales are moving again.

Prices are not.

That usually means sellers are finally taking the hit, not that the market is suddenly healthy.

Buyers have more choice, rates still bite, and inventory is forcing people to get realistic.

More deals does not automatically mean higher prices.

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
