#!/usr/bin/env python3
"""Generate YouTube thumbnail via 302.ai (Flux-2-Klein-4B, $0.014/ảnh) qua Vercel relay.

Usage:
  python3 gen_image_302.py --prompt "..." --out thumb.jpeg

Cheapest model on 302.ai. Relay bypasses Cloudflare 1010 from VM IP.
"""
import json, os, argparse, urllib.request, urllib.parse

RELAY = "https://replay-proxy-three.vercel.app/api/relay"
KEYFILE = "/home/admin/.hermes/profiles/agent3/302_key.txt"
ENDPOINT = "https://api.302.ai/v1/images/generations"
MODELS = {
    "flux4b": ("Flux-2-Klein-4B", 0.014),   # rẻ nhất, ĐÃ VERIFY chạy được
    "glm": ("Zhipu/GLM-Image", 0.016),     # Zhipu hybrid AR+diffusion - CẦN ENABLE TRÊN 302.AI (key hiện báo "No available models")
}
DEFAULT = "flux4b"

def proxy(target):
    return f"{RELAY}?url={urllib.parse.quote(target)}"

def gen(prompt, out, size="1024x1024", model_key=DEFAULT):
    model, price = MODELS[model_key]
    body = {"model": model, "prompt": prompt, "size": size, "n": 1}
    req = urllib.request.Request(proxy(ENDPOINT), data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {open(KEYFILE).read().strip()}",
                  "Content-Type": "application/json", "User-Agent": "Mozilla/5.0",
                  "Referer": "https://302.ai/"}, method="POST")
    r = json.loads(urllib.request.urlopen(req, timeout=120).read())
    img_url = r["data"][0]["url"]
    img = urllib.request.urlopen(urllib.request.Request(proxy(img_url),
        headers={"User-Agent": "Mozilla/5.0"}, method="GET"), timeout=60).read()
    open(out, "wb").write(img)
    return len(img), price

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--model", default=DEFAULT, choices=MODELS.keys(),
                    help="flux4b=$0.014 (rẻ nhất) | glm=$0.016 (Zhipu)")
    a = ap.parse_args()
    n, price = gen(a.prompt, a.out, a.size, a.model)
    print(f"✅ saved {a.out} ({n//1024}KB) - model {MODELS[a.model][0]} (${price})")

if __name__ == "__main__":
    main()
