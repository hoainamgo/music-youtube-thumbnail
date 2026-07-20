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
- Love/tender: young couple silhouette at golden-hour window, warm bokeh
- Upbeat/dance: dancer mid-move under neon club lights
- Sad/emotional: lone figure on rainy city street, blue-grey mood
- Confidence/anthem: artist on stage spotlight, bold color splash
- Chill/lofi: cozy room, headphones, warm lamp glow
→ Chọn visual theo `style` bài, KHÔNG dùng mascot nha khoa.

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
- Size: luôn `--size 1280x720` (đừng 1024x1024).
- BATCH (9+ ảnh): KHÔNG foreground (timeout 180s). Chạy `nohup python3 batch.py > log 2>&1 &`.
- Tránh duplicate: 1 bài 1 file `thumb_s2_{id}.jpeg`.

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

### Prompt mẫu (Style B — copy đổi title):
```
Cinematic YouTube thumbnail 16:9 for '{TITLE}' - {STYLE_DESC}.
LARGE bold rounded sans-serif text '{SHORT}' in #FFF8E7 with #8B1A3A outline at top-center, readable small.
{two lovers golden-hour window scene}, warm #FFB347 backlight + #FF6F91 rim light, soft bokeh,
shallow focus, warm amber rose grading, glossy highlights, anamorphic flare, 8k detail, film grain, no watermark
```
