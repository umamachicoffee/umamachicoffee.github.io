# -*- coding: utf-8 -*-
"""文字入れ画像（フィード 1080x1350 / ストーリーズ 1080x1920）を作るスクリプト。

  python instagram/autopost/generate_overlays.py                 # instagram/generated/ に全部作る
  python instagram/autopost/generate_overlays.py --contact-sheet preview.jpg   # 一覧画像も作る

GitHub の Actions「Instagram generate overlays」からも実行できます（Pythonのインストール不要）。
投稿と同じ実行の中では作りません（作った画像が公開URLに反映されるまで数分かかるため）。
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content  # noqa: E402

INSTAGRAM_DIR = os.path.dirname(HERE)
PHOTOS_DIR = os.path.join(INSTAGRAM_DIR, "photos")
OUT_DIR = os.path.join(INSTAGRAM_DIR, "generated")
FONT_PATH = os.path.join(HERE, "fonts", "ZenMaruGothic-Medium.ttf")

SIZES = {"feed": (1080, 1350), "story": (1080, 1920)}
LOW_RES_LONG_SIDE = 800

# 落ち着いた配色
INK_DARK = (52, 40, 30)          # 濃い焦げ茶（カード用の文字）
SHADE = (28, 20, 14)             # グラデーションの色
WHITE = (255, 255, 255)

# 種類ごとのレイアウト（px）
LAYOUT = {
    "feed": dict(margin=76, head=66, info=38, sub=29, brand=21, gap1=18, gap2=14, gap3=30,
                 safe_top=76, safe_bottom=76),
    # ストーリーズは上（アカウント名）と下（返信欄）が Instagram の表示で隠れるので余白を広く取る
    "story": dict(margin=84, head=74, info=42, sub=32, brand=23, gap1=22, gap2=16, gap3=34,
                  safe_top=270, safe_bottom=400),
}


class TextDoesNotFit(Exception):
    pass


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def text_width(draw, text, fnt, tracking=0):
    if not text:
        return 0
    return draw.textlength(text, font=fnt) + tracking * (len(text) - 1)


def draw_tracked(draw, xy, text, fnt, fill, tracking=0):
    """字間（tracking）を空けて1行描く。"""
    x, y = xy
    if tracking == 0:
        draw.text((x, y), text, font=fnt, fill=fill)
        return
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def fit_font(draw, text, size, max_w, tracking=0, min_ratio=0.72):
    """幅に収まるまで文字を小さくする。小さくしすぎる場合はエラー（はみ出し防止）。"""
    s = size
    while s >= int(size * min_ratio):
        f = font(s)
        if all(text_width(draw, line, f, tracking) <= max_w for line in text.split("\n")):
            return f
        s -= 2
    raise TextDoesNotFit(f"文字が長すぎて収まりません: {text!r}")


def load_photo(entry):
    path = os.path.join(PHOTOS_DIR, entry["photo"])
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    return im


def base_image(entry, kind):
    W, H = SIZES[kind]
    im = load_photo(entry)
    if entry.get("layout") == "card":
        # ロゴを、ロゴの背景色と同じ無地の上に置く（ロゴ画像が小さいので拡大しすぎない）
        # ロゴ画像のふちの黒い枠を切り落としてから、背景色を拾う
        inset = max(6, int(min(im.size) * 0.03))
        im = im.crop((inset, inset, im.width - inset, im.height - inset))
        bg = im.getpixel((4, 4))
        canvas = Image.new("RGB", (W, H), bg)
        target_h = int(H * (0.50 if kind == "feed" else 0.42))
        scale = target_h / im.height
        logo = im.resize((int(im.width * scale), target_h), Image.LANCZOS)
        top = int(H * (0.08 if kind == "feed" else 0.16))
        # ふちをぼかして、背景になじませる
        feather = 28
        mask = Image.new("L", logo.size, 0)
        ImageDraw.Draw(mask).rectangle([feather, feather, logo.width - feather, logo.height - feather], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
        canvas.paste(logo, ((W - logo.width) // 2, top), mask)
        return canvas
    crop = entry.get("crop")
    if crop:
        l, t, r, b = crop
        im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    fx, fy = entry.get("focus") or (0.5, 0.5)
    return ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(fx, fy))


def text_block(draw, entry, kind, max_w):
    """描く行のリスト [(text, font, tracking, kind)] と全体の高さを返す。"""
    L = LAYOUT[kind]
    rows = []
    rows.append((entry["headline"], fit_font(draw, entry["headline"], L["head"], max_w), 0, "head"))
    if entry.get("info"):
        rows.append((entry["info"], fit_font(draw, entry["info"], L["info"], max_w), 0, "info"))
    if entry.get("subline"):
        rows.append((entry["subline"], fit_font(draw, entry["subline"], L["sub"], max_w, tracking=1), 1, "sub"))
    if entry.get("layout") != "card":   # カードはロゴに店名が入っているので省略
        rows.append(("UMAMACHI COFFEE", font(L["brand"]), 5, "brand"))
    return rows


def line_height(draw, text, fnt):
    # 文字の種類によらず行の高さをそろえる（「あg」で計測）
    l, t, r, b = draw.textbbox((0, 0), "あAg" + text[:1], font=fnt)
    return b - t, t


def render(entry, kind):
    W, H = SIZES[kind]
    L = LAYOUT[kind]
    img = base_image(entry, kind).convert("RGBA")
    card = entry.get("layout") == "card"
    margin = L["margin"]
    max_w = W - margin * 2
    measure = ImageDraw.Draw(img)
    rows = text_block(measure, entry, kind, max_w)

    # 行ごとの高さ（見出しは複数行可）
    blocks = []
    for text, fnt, tr, role in rows:
        lines = text.split("\n")
        h, off = line_height(measure, text, fnt)
        lh = int(h * 1.25) if len(lines) > 1 else h
        blocks.append((lines, fnt, tr, role, h, lh, off))
    gaps = {"head": L["gap1"], "info": L["gap2"], "sub": L["gap3"]}
    total = 0
    for i, (lines, fnt, tr, role, h, lh, off) in enumerate(blocks):
        total += lh * (len(lines) - 1) + h
        if i < len(blocks) - 1:
            total += gaps.get(role, L["gap2"])

    if card:
        top = int(H * (0.66 if kind == "feed" else 0.62))
    elif entry.get("position") == "top":
        top = L["safe_top"] + (10 if kind == "feed" else 0)
    else:
        top = H - L["safe_bottom"] - total
    bottom = top + total

    # 読みやすさのための、やわらかいグラデーション（写真のときだけ）
    if not card:
        shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shade)
        reach = 260 if kind == "feed" else 340
        max_a = 165
        if entry.get("position") == "top":
            # 上は空や窓など明るい部分が多いので、少し濃く・長めにする
            max_a = 200
            reach = int(reach * 1.3)
            y_solid_end, y_fade_end = bottom + 60, bottom + reach
            for y in range(0, min(H, y_fade_end)):
                if y <= y_solid_end:
                    a = max_a
                else:
                    t = (y - y_solid_end) / (y_fade_end - y_solid_end)
                    a = int(max_a * (1 - t) ** 1.6)
                sd.line([(0, y), (W, y)], fill=SHADE + (a,))
        else:
            y_fade_start, y_solid_start = top - reach, top - 40
            for y in range(max(0, y_fade_start), H):
                if y >= y_solid_start:
                    a = max_a
                else:
                    t = (y - y_fade_start) / (y_solid_start - y_fade_start)
                    a = int(max_a * t ** 1.6)
                sd.line([(0, y), (W, y)], fill=SHADE + (a,))
        img = Image.alpha_composite(img, shade)

    fg = INK_DARK if card else WHITE
    # 文字のごく薄い影（写真のときだけ）
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ds = ImageDraw.Draw(shadow)
    y = top
    for i, (lines, fnt, tr, role, h, lh, off) in enumerate(blocks):
        alpha = 255 if role in ("head", "info") else (225 if role == "sub" else 200)
        for j, line in enumerate(lines):
            w = text_width(d, line, fnt, tr)
            x = (W - w) / 2 if card else margin
            if role == "brand" and not card:
                # ブランド名の前に短い線（写真レイアウトのみ）
                rule_w = 36
                ly = y + h // 2
                d.line([(x, ly), (x + rule_w, ly)], fill=fg + (alpha,), width=2)
                x += rule_w + 16
            draw_tracked(d, (x, y - off), line, fnt, fg + (alpha,), tr)
            if not card:
                draw_tracked(ds, (x + 1, y - off + 2), line, fnt, (0, 0, 0, 120), tr)
            y += lh if j < len(lines) - 1 else h
        if i < len(blocks) - 1:
            y += gaps.get(role, L["gap2"])
    if not card:
        shadow = shadow.filter(ImageFilter.GaussianBlur(3))
        img = Image.alpha_composite(img, shadow)
    img = Image.alpha_composite(img, layer)
    return img.convert("RGB")


def check_entry(entry):
    """元写真の確認（無い・小さい）。警告メッセージのリストを返す。"""
    warns = []
    path = os.path.join(PHOTOS_DIR, entry["photo"])
    if not os.path.exists(path):
        raise FileNotFoundError(f"元写真がありません: instagram/photos/{entry['photo']}")
    im = ImageOps.exif_transpose(Image.open(path))
    if max(im.size) < LOW_RES_LONG_SIDE and entry.get("layout") != "card":
        warns.append(f"[注意] {entry['id']}: 元写真が小さい（{im.size[0]}x{im.size[1]}、長辺{LOW_RES_LONG_SIDE}px未満）。画質が粗くなります")
    return warns


def generate(out_dir=OUT_DIR, only=None):
    results = []
    for kind, entries in (("feed", content.FEED), ("story", content.STORIES)):
        os.makedirs(os.path.join(out_dir, kind), exist_ok=True)
        for e in entries:
            if only and e["id"] not in only:
                continue
            path = os.path.join(out_dir, kind, e["id"] + ".jpg")
            if e.get("enabled", True) is False:
                # 投稿しない項目は画像も作らない（古い画像が残っていれば消す）
                if os.path.exists(path):
                    os.remove(path)
                    print(f"削除（enabled=False）: {os.path.relpath(path, INSTAGRAM_DIR)}")
                continue
            for w in check_entry(e):
                print(w)
            img = render(e, kind)
            assert img.size == SIZES[kind]
            img.save(path, "JPEG", quality=90, optimize=True, progressive=False)
            size_kb = os.path.getsize(path) // 1024
            if size_kb > 8 * 1024:
                raise RuntimeError(f"{path} が8MBを超えています（Instagramの上限）")
            print(f"作成: {os.path.relpath(path, INSTAGRAM_DIR)} ({size_kb}KB)")
            results.append((kind, e["id"], path))
    return results


def contact_sheet(paths, out_path, cols=5, thumb_w=300, title="UMAMACHI COFFEE — preview"):
    if not paths:
        return
    thumbs = []
    for kind, eid, p in paths:
        im = Image.open(p)
        r = thumb_w / im.width
        thumbs.append((eid, im.resize((thumb_w, int(im.height * r)), Image.LANCZOS)))
    th = max(t.height for _, t in thumbs)
    pad, label_h, head = 16, 34, 60
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, head + rows * (th + label_h + pad) + pad), (245, 240, 232))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 16), title, font=font(26), fill=INK_DARK)
    f = font(18)
    for i, (eid, t) in enumerate(thumbs):
        x = pad + (i % cols) * (thumb_w + pad)
        y = head + (i // cols) * (th + label_h + pad)
        sheet.paste(t, (x, y))
        d.text((x, y + t.height + 6), eid, font=f, fill=INK_DARK)
    sheet.save(out_path, "JPEG", quality=88)
    print(f"一覧画像: {out_path}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="文字入れ画像を生成します")
    ap.add_argument("--out", default=OUT_DIR, help="出力先（既定: instagram/generated）")
    ap.add_argument("--contact-sheet", help="フィード一覧画像の保存先（任意）")
    ap.add_argument("--story-contact-sheet", help="ストーリーズ一覧画像の保存先（任意）")
    ap.add_argument("--only", nargs="*", help="この id だけ作る")
    a = ap.parse_args(argv)
    res = generate(a.out, set(a.only) if a.only else None)
    if a.contact_sheet:
        contact_sheet([r for r in res if r[0] == "feed"], a.contact_sheet, cols=5, title="UMAMACHI COFFEE — feed 1080x1350")
    if a.story_contact_sheet:
        contact_sheet([r for r in res if r[0] == "story"], a.story_contact_sheet, cols=5, title="UMAMACHI COFFEE — stories 1080x1920")
    print(f"完了: {len(res)} 枚")


if __name__ == "__main__":
    main()
