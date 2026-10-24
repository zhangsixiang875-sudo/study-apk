"""把网页版打包成 APK 的 assets，并生成各密度图标。

用法：
    py -3 prepare.py
"""
import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.normpath(os.path.join(HERE, ".."))
SITE = os.path.join(WS, "gh-pages")
ASSETS = os.path.join(HERE, "app", "src", "main", "assets", "www")
RES = os.path.join(HERE, "app", "src", "main", "res")

# 打进 APK 的文件（不含文档）
FILES = ["index.html", "manifest.json", "icon-192.png", "icon-512.png",
         "golden.json"]
DIRS = ["packs"]

if os.path.isdir(ASSETS):
    shutil.rmtree(ASSETS)
os.makedirs(ASSETS)

for f in FILES:
    src = os.path.join(SITE, f)
    if not os.path.exists(src):
        raise SystemExit("缺少文件: " + src)
    shutil.copy2(src, os.path.join(ASSETS, f))
for d in DIRS:
    shutil.copytree(os.path.join(SITE, d), os.path.join(ASSETS, d))

print("assets 就绪：")
for root, _, files in os.walk(ASSETS):
    for fn in files:
        p = os.path.join(root, fn)
        print("  %-40s %d" % (os.path.relpath(p, ASSETS), os.path.getsize(p)))

# 图标：从 512 生成各密度
SRC_ICON = os.path.join(SITE, "icon-512.png")
DENS = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
img = Image.open(SRC_ICON).convert("RGBA")
for name, size in DENS.items():
    out = os.path.join(RES, "mipmap-" + name)
    os.makedirs(out, exist_ok=True)
    img.resize((size, size), Image.LANCZOS).save(os.path.join(out, "ic_launcher.png"))
    print("  mipmap-%-8s ic_launcher.png %dpx" % (name, size))
print("完成")
