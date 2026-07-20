---
name: music-youtube-thumbnail
description: Tạo YouTube thumbnail cho bài hát AI (Suno/Mureka S1/S2) target thị trường US. Dùng 302.ai Flux-2-Klein-4B ($0.014) qua Vercel relay. Tự động lấy title/style/lyric từ catalogue, build prompt visual phù hợp khán giả Mỹ (không brand nha khoa). Qua relay né Cloudflare 1010.
---

# Music YouTube Thumbnail (US Market)

## MỤC ĐÍCH
Tạo thumbnail YouTube cho bài hát AI (Pop-R&B, Session 1/2) — **dự án độc lập, target thị trường Mỹ (US)**.
- ❌ KHÔNG dùng brand nha khoa / mascot răng (đó là skill `dental-youtube-thumbnail` riêng)
- ✅ Visual phù hợp khán giả US: artist đa dạng, vibe phương Tây, text lớn dễ đọc, màu sắc theo mood bài
- Tự động load catalogue → lấy title/style → build prompt → gen qua 302.ai Flux (rẻ nhất)

## RELAY & AUTH
- Relay: `https://replay-proxy-three.vercel.app/api/relay` (edge, đã deploy)
- 302.ai key: `/home/admin/.hermes/profiles/agent3/302_key.txt` (KHÔNG commit)
- Script: `gen_image_302.py` (trong repo này)

## MODEL (rẻ nhất đã verify)
- **Flux-2-Klein-4B = $0.014/ảnh** ✅ chạy được, nhanh ~4s, ~190KB
- Size chuẩn: **1280x720 (16:9)** — YouTube bắt buộc ngang
- GLM-Image $0.016: cần enable trên 302.ai (hiện báo "No available models")

## QUY TRÌNH (4 bước)
1. **Load catalogue**: `catalog_melody_v2_en.json` (S2) hoặc `catalog_v1_rewritten.json` (S1)
2. **Lấy info**: `id` → `title`, `style`, `lyrics[:200]`
3. **Build prompt** (template bên dưới, THÊM `1280x720 horizontal` + visual US-phù hợp)
4. **Gen**: `python3 gen_image_302.py --model flux4b --size 1280x720 --prompt "..." --out thumb_s{X}_{id}.jpeg`

## PROMPT TEMPLATE (verify OK — text rõ + ngang 16:9)
```
YouTube thumbnail 16:9 for song '{TITLE}' - {STYLE_DESC}.
Large bold sans-serif text '{SHORT_TITLE}' in white with dark outline at TOP-CENTER,
very readable at small size.
Below: {VISUAL_IDEA_US}.
{MOOD} vibe, clean modern eye-catching layout, no watermark, no small text
```
> LUÔN có dòng text rõ + `16:9` / `1280x720 horizontal` để model ra đúng tỉ lệ.

## VISUAL IDEA THEO THỂ LOẠI (US-friendly, KHÔNG răng)
- Love/tender: young **man+woman** couple at golden-hour window, warm bokeh — xem Style B/F
- Upbeat/dance: **man+woman** dancing close under neon club lights — xem Style F (Round Two)
- Sad/emotional: lone figure on rainy city street, blue-grey mood
- Confidence/anthem: artist on stage spotlight, bold color splash
- Chill/lofi: cozy room, headphones, warm lamp glow
→ Chọn visual theo `style` bài, KHÔNG dùng mascot nha khoa.
> 🔴 **COUPLE RULE (user correction #08)**: Với bài love/romance, **mặc định vẽ cặp nam+nữ** (heterosexual) trừ khi lời bài ghi rõ khác. Anh reject ảnh "2 người nữ ôm ấp" (same-sex embrace) → đổi thành nam/nữ khiêu vũ/gần nhau. KHÔNG dùng same-sex intimate embrace làm default.

## SHORT TITLE (3-5 từ từ title gốc)
- "Stumbling First Words" → "FIRST WORDS"
- "A Thousand Miles" → "THOUSAND MILES"
- "Sorry At the Door" → "SORRY"

## 🔴 RULE BẮT BUỘC (user reject 2 lần thumbnail thiếu text / sai tỉ lệ)
- PHẢI CÓ TEXT hiển thị rõ (tiêu đề 3-5 từ, bold, viền, đọc được ở 320px).
- PHẢI TỈ LỆ 1280x720 NGANG (16:9) — user reject bản vuông 1024x1024.
- Prompt LUÔN có: `Large bold sans-serif text '{SHORT_TITLE}' ... at top-center` + `16:9` / `1280x720 horizontal`.
- Sau gen: MỞ ẢNH CHECK (a) có text thật, (b) đúng ngang 16:9 → regenerate nếu thiếu/sai.

## PITFALLS
- Flux hay bỏ text hoặc sai chính tả → check kỹ, regenerate nếu thiếu/sai.
- Size: luôn `--size 1280x720` (đừng 1024x1024). Flux chấp nhận trực tiếp "1280x720" (verify OK).
- BATCH (9+ ảnh): KHÔNG foreground (timeout 180s terminal). Dùng `terminal(background=true)` — tool TỪ CHỐI nohup/disown/setsid (báo lỗi). Hoặc delegate_task.
- Tránh duplicate: 1 bài 1 file `thumb_s2_{id}.jpeg`.
- ⚠️ **302.ai model availability (verify 2026-07-20)**: CHỈ **Flux-2-Klein-4B ($0.014)** chạy được. **GLM-Image ($0.016)** và **Kling O1/O3 ($0.028)** đều trả `"No available models"` → chưa enable trên tài khoản, KHÔNG dùng được trừ khi user bật trên dashboard 302.ai. Đừng hứa model khác chạy được.
- ⚠️ **Flux LoRA / pose-control / reference-image KHÔNG dùng được qua API 302.ai**: truyền `lora_name` / `image` param thì server nhận (không lỗi) nhưng **silent ignore** — ảnh không thay đổi theo LoRA. Muốn "khung xương"/consistent character thật sự → phải chạy ComfyUI local (Flux.2 Klein 9B + LoRA từ HF), không qua API.
- ⚠️ **yescale fallback thường HỎNG**: key yescale hay báo (a) `"capability_not_allowed"` (sai loại key) hoặc (b) `"You don't have enough quota, need to top up $0.00X"` (hết tiền) — KHÔNG phải region block. Luôn đọc body lỗi 403. Khi yescale hết quota → dùng Flux-4B (302.ai) thay thế, vẫn cinematic.
- 🔴 **USER PREF (2026-07-20)**: Khi build progress/release dashboard, LUÔN chừa slot trống cho **YouTube Video** + **Shorts** (placeholder 🔜, KHÔNG xoá). User: "Chừa chỗ cho video youtube nha e, short nữa".
- 📦 **RELEASE PIPELINE**: có thumbnail + audio rồi → qua skill `ai-music-release` (Drive sync + ONBOARDING + SEO_RELEASE_PLAN + progress site có sẵn video/shorts slots).

## 📋 GỬI PROMPT CHO USER (box format)
- Khi user yêu cầu "gửi prompt copy được" → gửi dạng **``` code block ```** (mỗi prompt 1 block, head comment `{A-F} — TÊN`), KHÔNG rải rác prose. User: "em gửi 5 prompt, dạng box, copy dc nha".
- Mỗi block copy đổi `{TITLE}`/`{SHORT}` là dùng được.

## REFERENCES
- `references/cinematic_prompts.md` — 6 prompt phong cách (Neo-Noir / Golden Romance / Blade Runner / Vintage Film / Epic Cinemascope / Healing Pink) dạng copy-paste sẵn, đã verify sinh ảnh chuẩn 1280x720. COUPLE RULE áp dụng (man+woman).

## CLI NHANH
```bash
python3 gen_image_302.py --model flux4b --size 1280x720 \
  --prompt "YouTube thumbnail 16:9 for song 'Stumbling First Words' - tender Pop-R&B. Large bold sans-serif text 'FIRST WORDS' in white with dark outline at top-center, very readable. Below: young couple silhouette at golden-hour window, warm bokeh. Dreamy romantic vibe, clean layout, no watermark" \
  --out thumb_s2_01.jpeg
```

## 🎯 FLUX PROMPTING GUIDE (từ BFL official + community, ĐÃ ÁP DỤNG)
- ❌ **KHÔNG dùng negative prompt** (Flux phạt ngược, hay sinh ra đúng thứ muốn tránh)
- ✅ Viết **flowing prose** (văn xuôi tự nhiên): subject → setting → details → lighting → mood
- ✅ Dùng **hex color codes** cụ thể ("#FFB347") thay từ mơ hồ ("warm")
- ✅ Từ ngữ cụ thể ("volumetric backlight", "anamorphic flare", "shallow depth of field")
- ✅ Thêm: "8k detail, film grain, glossy reflective surfaces, cinematic color grading"
- ✅ Charlier947 rules: face/subject 30-50% frame, text 3-5 từ, 2 màu chủ đạo, high contrast
- ✅ Luôn có `16:9` / `1280x720 horizontal` + text rõ ở top-center

## 5 PHONG CÁCH CINEMATIC (template đã verify — S2#1)
> Thay `{TITLE}`/`{SHORT}`/`{STYLE_DESC}` cho bài khác. Giữ cấu trúc prose + hex + cinematic keywords.
- **A. Neo-Noir**: rain-slicked neon street, #0B3D3D + #C2185B glow, volumetric streetlight, chiaroscuro
- **B. Golden Romance**: sunlit window golden-hour #FFB347 + #FF6F91 rim, bokeh dust, dreamy
- **C. Blade Runner**: neon futuristic cityscape, #00E5FF + #FF4081 holograms, chrome reflection
- **D. Vintage Film**: 1970s tungsten #FFB300, #A1887F palette, 35mm grain, vignette
- **E. Epic Cinemascope**: hill at dusk, #FF7043 + #7E57C2 sky, god rays, grand scale
- **F. Healing Pink (Chữa lành / Tình yêu thương)**: gam hồng ấm, viền trái tim, ngôi sao/ánh sáng mờ ảo, cảm giác ấm áp của tình yêu thương
- **G. Premium Romance (Typography Nhật cao cấp)**: couple bên phải golden-hour, 4 text block bên trái (badge + 2 headline + heart hook), outline burgundy/ivory, photorealistic

### Prompt mẫu (Style G — Premium Romance, copy đổi text):
```text
Create a premium cinematic YouTube music thumbnail in 16:9 landscape format for an emotional romantic song titled '{TITLE}'. CORE VISUAL: A tender intimate cinematic moment of two attractive young adult lovers beside a large sunlit window at golden hour. Place them on the right half of the frame, chest-up close-up, forehead to forehead, faces large and sharply focused. One person eyes softly closed, other subtle vulnerable smile. Emotion hesitant, sincere, nostalgic, unspoken love. Warm golden-hour backlight #FFB347 behind, delicate rosy rim light #FF6F91 around hair and shoulders, creamy bokeh, floating dust motes, shallow depth of field, subtle anamorphic lens flare, glossy natural skin highlights, warm amber-rose color grading, elegant film grain, dreamy premium romantic music-video mood. TYPOGRAPHY: bold high-impact layered YouTube thumbnail typography inspired by energetic Japanese thumbnail layouts, all text English, elegant romantic. Heavy white outer outlines, deep burgundy inner outlines, strong soft drop shadows, slight angle variation, small sparkle accents, clean spacing. Keep all text on left half. Exactly 4 text elements: 1. TOP-LEFT BADGE 'NEW LOVE SONG' small deep-burgundy rounded label gold sparkle, bold uppercase warm-ivory thin white outline. 2. PRIMARY 'I CAN'T' large upper-left warm ivory #FFF8E7 thick white outline deep wine burgundy #8B1A3A inner outline dark burgundy drop shadow golden edge glow. 3. SECONDARY 'SAY IT' below much larger slightly angled upward blush pink #FF6F91 thick ivory white outline deep burgundy shadow glossy, single largest element. 4. LOWER-LEFT HEART BURST soft-pink heart warm-ivory outline burgundy shadow gold sparkles 'FIRST WORDS?' bold deep burgundy 'WORDS?' larger than 'FIRST'. High contrast, no extra text, no watermark, no anime, photorealistic.
```
> Đặc trưng G: couple không bị che (bên phải), typography Nhật tầng lớp (badge + 2 headline + heart hook), outline burgundy/ivory, premium clickable. Dùng cho bài love/tender chủ chốt. Có thể đổi {primary}=I CAN'T, {secondary}=SAY IT, {badge}=NEW LOVE SONG, {hook}=FIRST WORDS?

```text
Cinematic YouTube thumbnail 16:9 for '{TITLE}' - {STYLE_DESC}.
LARGE bold rounded sans-serif text '{SHORT}' in #FFF0F5 with #C2185B outline at top-center, readable small.
A tender healing scene wrapped in a soft glowing heart-shaped frame border, pastel pink #F8BBD0 and warm rose #F48FB1 palette, gentle floating stars and soft bokeh light orbs drifting like fairy dust, dreamy low-contrast glow, volumetric soft pink backlight, shallow depth of field, warm loving mood, glossy soft highlights, ethereal atmosphere, 8k detail, subtle film grain, no watermark
```
> Đặc trưng F: viền trái tim phát sáng + ngôi sao mờ ảo + gam hồng (pink/rose) + ấm áp, chữa lành. Dùng cho bài chủ đề love/healing/family/self-love.
```
Cinematic YouTube thumbnail 16:9 for '{TITLE}' - {STYLE_DESC}.
LARGE bold rounded sans-serif text '{SHORT}' in #FFF8E7 with #8B1A3A outline at top-center, readable small.
{two lovers golden-hour window scene}, warm #FFB347 backlight + #FF6F91 rim light, soft bokeh,
shallow focus, warm amber rose grading, glossy highlights, anamorphic flare, 8k detail, film grain, no watermark
```
