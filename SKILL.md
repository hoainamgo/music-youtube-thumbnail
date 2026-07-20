---
name: music-youtube-thumbnail
description: Tạo YouTube thumbnail cho bài hát AI (Suno/Mureka S1/S2) target thị trường US. Dùng 302.ai Flux-2-Klein-4B ($0.014) qua Vercel relay. Typography tầng lớp (badge + headline + secondary + hook), 8 phong cách (Neo-Noir / Golden / Blade Runner / Vintage / Epic / Healing Pink / Premium Romance / Warm Acoustic). Qua relay né Cloudflare 1010.
---

# Music YouTube Thumbnail (US Market)

## MỤC ĐÍCH
Tạo thumbnail YouTube cho bài hát AI (Pop-R&B, Session 1/2) — **dự án độc lập, target thị trường Mỹ (US)**.
- ❌ KHÔNG dùng brand nha khoa / mascot răng (đó là skill `dental-youtube-thumbnail` riêng)
- ✅ Visual phù hợp khán giả US: artist đa dạng, vibe phương Tây, **typography tầng lớp đa dạng** (badge + headline + secondary + hook), màu sắc theo mood bài
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

## 🎯 TYPOGRAPHY TẦNG LỚP (CHUẨN MỚI — áp dụng mọi style)
Thay vì 1 dòng text đơn, dùng **4 lớp text** đa dạng, bao quát hơn:
1. **BADGE (top)**: nhãn thể loại nhỏ (vd "NEW LOVE SONG" / "ROMANTIC ACOUSTIC") — deep color, sparkle accent, thin outline
2. **PRIMARY HEADLINE**: chữ lớn nhất thứ 2, thường ivory/white, outline đậm, drop shadow
3. **SECONDARY HEADLINE**: chữ LỚN NHẤT, màu accent (pink/burgundy), hơi nghiêng, glossy — thu hút click
4. **HOOK BURST**: text hook nhỏ trong hình dạng (heart/starburst), deep color, "WORDS?" lớn hơn "FIRST"

> Quy tắc: text LUÔN ở nửa trái, subject (couple/người) ở nửa phải KHÔNG bị che. High contrast, readable ở 320px mobile. KHÔNG anime/comic/watermark.

## SHORT TITLE → 4 TEXT BLOCKS (template cho mọi bài)
Với bài "Stumbling First Words" →
- BADGE: `NEW LOVE SONG` (hoặc `ROMANTIC ACOUSTIC` cho style acoustic)
- PRIMARY: `I CAN'T` (hoặc `STUMBLING`)
- SECONDARY: `SAY IT` (hoặc `FIRST WORDS` script)
- HOOK: `FIRST WORDS?`
> Đổi {badge}/{primary}/{secondary}/{hook} theo title bài. Xem `references/cinematic_prompts.md` copy-paste sẵn.

## VISUAL IDEA THEO THỂ LOẠI (US-friendly, KHÔNG răng)
- Love/tender: young **man+woman** couple at golden-hour window, warm bokeh — xem Style B/F/G
- Upbeat/dance: **man+woman** dancing close under neon club lights — xem Style F (Round Two)
- Acoustic/indie: woman with guitar by window, cozy room — xem Style H
- Sad/emotional: lone figure on rainy city street, blue-grey mood — Style A
- Confidence/anthem: artist on stage spotlight, bold color splash
- Chill/lofi: cozy room, headphones, warm lamp glow
> 🔴 **COUPLE RULE**: love/romance mặc định **nam+nữ** (heterosexual) trừ khi lyric ghi rõ khác. KHÔNG same-sex embrace.

## 🔴 RULE BẮT BUỘC
- PHẢI CÓ 4 TEXT BLOCKS (badge + 2 headline + hook) hiển thị rõ, đọc được ở 320px.
- PHẢI TỈ LỆ 1280x720 NGANG (16:9).
- Prompt LUÔN có: `16:9` / `1280x720 horizontal` + text rõ ở left half.
- Sau gen: MỞ ẢNH CHECK (a) đủ 4 text, (b) đúng ngang → regenerate nếu thiếu/sai.

## PITFALLS
- Flux hay bỏ/sai text → check kỹ, regenerate.
- Luôn `--size 1280x720`.
- BATCH: dùng `terminal(background=true)` (KHÔNG nohup/setsid).
- ⚠️ 302.ai: CHỈ Flux-2-Klein-4B chạy được (GLM/Kling cần enable).
- ⚠️ Flux LoRA/pose/reference: silent ignore qua API → cần ComfyUI local.
- ⚠️ yescale fallback hay 403 (quota/key) → quay lại Flux.
- 🔴 USER PREF: chừa slot YouTube Video + Shorts trên dashboard.

## 📋 GỬI PROMPT CHO USER (box format)
Khi user cần prompt copy → gửi ``` code block ```, mỗi prompt 1 block, head `{A-H} — TÊN`.

## REFERENCES
- `references/cinematic_prompts.md` — 8 prompt phong cách (A-H) layered typography, copy-paste sẵn, verify 1280x720.

## CLI NHANH
```bash
python3 gen_image_302.py --model flux4b --size 1280x720 \
  --prompt "$(cat references/cinematic_prompts.md | sed -n '/## G/,/## Chạy/p')" \
  --out thumb_s2_01.jpeg
```

## 🎯 FLUX PROMPTING GUIDE (từ BFL official)
- ❌ KHÔNG negative prompt (Flux phạt ngược)
- ✅ Flowing prose: subject → setting → details → lighting → mood
- ✅ Hex color codes cụ thể (#FFB347)
- ✅ Cinematic keywords: "volumetric backlight", "anamorphic flare", "shallow depth of field", "8k detail, film grain"
- ✅ Luôn `16:9` / `1280x720 horizontal` + layered text rõ ở left

## 8 PHONG CÁCH (template — xem references/cinematic_prompts.md để copy prompt đầy đủ)
- **A. Neo-Noir**: rain neon, #0B3D3D + #C2185B, chiaroscuro — badge NEON HIT / PRIMARY CAN'T HIDE / SECONDARY SAY GOODBYE / hook IN THE RAIN?
- **B. Golden Romance**: sunlit window #FFB347 + #FF6F91 — badge NEW LOVE SONG / PRIMARY I CAN'T / SECONDARY SAY IT / hook FIRST WORDS?
- **C. Blade Runner**: neon city #00E5FF + #FF4081 — badge SYNTH CITY / PRIMARY WE / SECONDARY COLLIDE / hook AT MIDNIGHT?
- **D. Vintage Film**: 1970s #FFB300 + #A1887F, grain — badge RETRO LOVE / PRIMARY PLAY IT / SECONDARY AGAIN / hook ON REPEAT?
- **E. Epic Cinemascope**: dusk #FF7043 + #7E57C2, god rays — badge BIG LOVE / PRIMARY US / SECONDARY FOREVER / hook UNDER STARS?
- **F. Healing Pink**: heart frame, stars, #F8BBD0 — badge SOFT LOVE / PRIMARY STAY / SECONDARY WITH ME / hook HEALING?
- **G. Premium Romance**: couple right, JP typography, burgundy/ivory — badge NEW LOVE SONG / PRIMARY I CAN'T / SECONDARY SAY IT / hook FIRST WORDS?
- **H. Warm Acoustic**: woman+guitar window, indie poster — badge ROMANTIC ACOUSTIC / PRIMARY STUMBLING / SECONDARY FIRST WORDS (script) / hook [none, 3-block]

> Mọi style dùng layered typography (A-F nâng cấp từ 1 dòng → 4 block theo chuẩn G/H). Copy prompt từ references đổi {badge}/{primary}/{secondary}/{hook}/{TITLE}.
