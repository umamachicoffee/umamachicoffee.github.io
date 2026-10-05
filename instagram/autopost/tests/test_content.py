# -*- coding: utf-8 -*-
"""content.py（キャプション・画像）と同梱ファイルのチェック。"""
import os
import re

import pytest
from PIL import Image

import content
import generate_overlays as go

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # instagram/autopost
INSTAGRAM = os.path.dirname(HERE)
REPO = os.path.dirname(INSTAGRAM)
CJK = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
TAG = re.compile(r"^#[a-z0-9_]+$")

BANNED_TEXT = ["年中無休", "ドイツ", "german", "germany", "ランチ", "lunch", "最高", "no.1", "no1", "best",
               "スペシャルティ", "specialty", "single origin", "シングルオリジン", "絶品", "日本一", "人気no"]
BANNED_TAGS = {"#specialtycoffee", "#singleorigin"}
ALLOWED_PRICES = {"580", "630", "400", "1,000", "1,300", "880", "1,560"}


def all_captions():
    return [(e["id"], e["caption"]) for e in content.FEED + content.REELS]


def active(entries):
    return [e for e in entries if e.get("enabled", True) is not False]


def test_enough_feed_entries_and_unique_ids():
    assert len(active(content.FEED)) >= 12                                   # 稼働中のフィード12本以上
    assert len([e for e in active(content.FEED) if not e.get("months")]) >= 10   # 季節もの以外でも10本以上
    assert len(active(content.STORIES)) >= 5
    assert len(content.REELS) >= 1
    ids = [e["id"] for e in content.FEED + content.STORIES + content.REELS]
    assert len(ids) == len(set(ids))
    assert all(re.fullmatch(r"[a-z0-9-]+", i) for i in ids)


def test_omelette_sandwich_enabled_with_price():
    e = {e["id"]: e for e in content.FEED}["f07-omelette-sandwich"]
    assert e.get("enabled", True) is True and e["photo"] == "sandwich-omelette.jpg"
    assert e["headline"] == "オムレツサンドイッチ" and e["info"] == "¥880（税込）"
    assert "オムレツサンドイッチ ¥880（税込）" in e["caption"] and "Omelette Sandwich ¥880 (tax included)" in e["caption"]
    assert "980" not in e["caption"] + e["info"]
    assert "ふんわり" not in e["caption"] and "fluffy" not in e["caption"].lower()


def test_kyoto_moon_burger_uses_egg_photo():
    # 京都ムーンバーガー＝目玉焼きのせ。必ず目玉焼きの写っている IMG_4147（burger-kyoto-moon.jpg）を使う
    entries = [e for e in content.FEED + content.STORIES
               if "ムーンバーガー" in e["headline"] + e.get("info", "") + e.get("caption", "")]
    assert {e["id"] for e in entries} >= {"f02-kyoto-moon-burger", "s03-kyoto-moon-burger"}
    for e in entries:
        assert e["photo"] == "burger-kyoto-moon.jpg", e["id"]
    cap = {e["id"]: e for e in content.FEED}["f02-kyoto-moon-burger"]["caption"]
    assert "目玉焼きをのせた「京都ムーンバーガー」" in cap and "topped with a fried egg" in cap
    # 目玉焼きのない IMG_4146 は馬町バーガー専用（ムーンバーガーには使わない）
    assert all(e["photo"] != "burger-umamachi.jpg" for e in entries)


def test_umamachi_burger_enabled_with_price():
    e = {e["id"]: e for e in content.FEED}["f11-umamachi-burger"]
    assert e.get("enabled", True) is True and e["photo"] == "burger-umamachi.jpg"
    assert e["info"] == "¥1,300（税込）"
    assert "馬町バーガー ¥1,300（税込）" in e["caption"] and "Umamachi Burger ¥1,300 (tax included)" in e["caption"]
    assert "2枚" not in e["caption"] and "double" not in e["caption"].lower()


BEAN_PHOTOS = {"roaster-poster.jpg"}          # 豆・焙煎機の写真（一杯・料理の価格を載せない）
CUP_FOOD_PRICES = {"580", "630", "400", "1,000", "1,300"}
# ¥880 は「珈琲豆100g」と「オムレツサンドイッチ」の両方の価格。どちらの意味かが必ず分かるようにする


@pytest.mark.parametrize("e", active(content.FEED) + active(content.STORIES), ids=lambda e: e["id"])
def test_no_bean_cup_price_confusion(e):
    overlay = " ".join([e["headline"], e.get("info", ""), e.get("subline", "")])
    prices = set(re.findall(r"¥\s?(\d{1,3}(?:,\d{3})*)", overlay))
    is_bean = e["photo"] in BEAN_PHOTOS
    if is_bean:
        assert not (prices & CUP_FOOD_PRICES), f"{e['id']}: 豆の写真に一杯・料理の価格"
        if prices & {"880", "1,560"}:
            assert "100g" in overlay and "200g" in overlay, f"{e['id']}: 豆の価格は量（100g/200g）と一緒に"
    else:
        assert "1,560" not in prices, f"{e['id']}: 豆の写真以外に豆の価格"
        assert "100g" not in overlay and "200g" not in overlay, f"{e['id']}: 豆以外の写真に豆の量"
        if "880" in prices:
            assert e["headline"] == "オムレツサンドイッチ", f"{e['id']}: ¥880 は商品名と一緒に"
    if "580" in prices:
        assert "一杯" in overlay and "per cup" in overlay
    cap = e.get("caption", "")
    if "¥580" in cap:
        assert "一杯 ¥580" in cap and "per cup" in cap
    for m in re.finditer(r"¥880", cap):          # キャプション内の ¥880 も、豆（100g）か商品名と並べる
        line = cap[cap.rfind("\n", 0, m.start()) + 1: cap.find("\n", m.end()) if "\n" in cap[m.end():] else len(cap)]
        assert "100" in line or "オムレツサンドイッチ" in line or "Omelette Sandwich" in line, (e["id"], line)


def test_confusion_rule_catches_mistakes():
    bad_bean = dict(content.FEED[0], photo="roaster-poster.jpg", headline="馬町ブレンド", info="¥580（税込）")
    bad_sand = dict(content.FEED[0], photo="sandwich-omelette.jpg", headline="珈琲豆", info="100g ¥880（税込）")
    for bad in (bad_bean, bad_sand):
        with pytest.raises(AssertionError):
            test_no_bean_cup_price_confusion(bad)


def test_f03_caption_matches_photo():
    e = {e["id"]: e for e in content.FEED}["f03-interior"]
    assert e["photo"] == "interior-deep.jpg"     # 木の柱・コンクリートの床が写っている写真（目視確認済み）


@pytest.mark.parametrize("eid,cap", all_captions(), ids=[i for i, _ in all_captions()])
def test_caption_structure(eid, cap):
    assert len(cap) <= 2200
    paras = cap.split("\n\n")
    tags = paras[-1].split()
    assert 10 <= len(tags) <= 15, eid
    assert all(TAG.match(t) for t in tags), (eid, tags)       # 英語のみのハッシュタグ
    assert len(set(tags)) == len(tags)
    assert not (set(tags) & BANNED_TAGS)
    body = paras[:-1]
    kinds = ["ja" if CJK.search(p) else "en" for p in body]
    assert kinds[0] == "ja" and kinds[-1] == "en", eid
    assert kinds == sorted(kinds, key=lambda k: k != "ja"), f"{eid}: 日本語→英語の順になっていない"
    assert "#" not in "\n".join(body)                         # 本文中にハッシュタグなし


@pytest.mark.parametrize("eid,text", all_captions() + [
    (e["id"] + "-overlay", " ".join([e["headline"], e.get("info", ""), e.get("subline", "")]))
    for e in content.FEED + content.STORIES], ids=lambda x: x if len(x) < 40 else None)
def test_no_banned_or_unconfirmed_wording(eid, text):
    low = text.lower()
    for w in BANNED_TEXT:
        assert w not in low, f"{eid}: 「{w}」は使わない"
    for p in re.findall(r"¥\s?(\d{1,3}(?:,\d{3})*)", text):
        assert p in ALLOWED_PRICES, f"{eid}: 未確認の価格 ¥{p}"
    if "¥" in text and CJK.search(text):
        assert "税込" in text
    if "定休日" in text:
        assert "定休日なし" in text


def test_confirmed_facts_spelled_correctly():
    joined = "\n".join(c for _, c in all_captions())
    assert "京都市東山区常盤町459-13" in joined
    assert "075-741-8779" in joined
    assert "9:00〜17:00" in joined
    assert "GIESEN" in joined and "オランダ" in joined


@pytest.mark.parametrize("e", active(content.FEED) + active(content.STORIES), ids=lambda e: e["id"])
def test_photo_exists_and_is_safe(e):
    name = e["photo"]
    assert os.path.exists(os.path.join(INSTAGRAM, "photos", name))
    low = name.lower()
    for bad in ("img_4238", "img_4374", "menu", "board", "blackboard", "kokuban"):
        assert bad not in low


def test_photos_folder_contains_only_safe_jpegs():
    for name in os.listdir(os.path.join(INSTAGRAM, "photos")):
        if name.startswith("."):
            continue
        low = name.lower()
        assert low.endswith((".jpg", ".jpeg")) or low.endswith(".md")
        for bad in ("img_4238", "img_4374", "menu", "board"):
            assert bad not in low


@pytest.mark.parametrize("kind,e", [("feed", e) for e in active(content.FEED)] + [("story", e) for e in active(content.STORIES)],
                         ids=lambda x: x if isinstance(x, str) else x["id"])
def test_generated_image_present_and_valid(kind, e):
    p = os.path.join(INSTAGRAM, "generated", kind, e["id"] + ".jpg")
    assert os.path.exists(p), f"{p} がありません（generate_overlays.py を実行）"
    with Image.open(p) as im:
        assert im.format == "JPEG"
        assert im.size == go.SIZES[kind]
        ratio = im.width / im.height
        if kind == "feed":
            assert 0.8 - 1e-6 <= ratio <= 1.91
    assert os.path.getsize(p) < 8 * 1024 * 1024


@pytest.mark.parametrize("kind,e", [("feed", e) for e in active(content.FEED)] + [("story", e) for e in active(content.STORIES)],
                         ids=lambda x: x if isinstance(x, str) else x["id"])
def test_overlay_text_fits(kind, e):
    img = go.render(e, kind)                 # 文字が収まらなければ TextDoesNotFit
    assert img.size == go.SIZES[kind]


def test_disabled_entries_get_no_generated_image(tmp_path, monkeypatch):
    e = dict(content.FEED[0], enabled=False)
    monkeypatch.setattr(content, "FEED", [e])
    monkeypatch.setattr(content, "STORIES", [])
    stale = tmp_path / "feed" / (e["id"] + ".jpg")
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"old")
    assert go.generate(str(tmp_path)) == []
    assert not stale.exists()                 # 古い画像も消える


def test_text_too_long_is_rejected():
    e = dict(content.FEED[0], headline="とても長い見出しは画像からはみ出してしまうので必ずエラーにする")
    with pytest.raises(go.TextDoesNotFit):
        go.render(e, "feed")


def test_font_and_license_included():
    assert os.path.exists(os.path.join(HERE, "fonts", "ZenMaruGothic-Medium.ttf"))
    assert "Open Font License" in open(os.path.join(HERE, "fonts", "OFL.txt"), encoding="utf-8").read()


def test_no_secrets_in_kit():
    pat = re.compile(r"(EAA[A-Za-z0-9]{20,}|IGAA[A-Za-z0-9]{20,}|IGQV[A-Za-z0-9_-]{20,})")
    for root, _, files in os.walk(REPO):
        for f in files:
            if f.endswith((".py", ".md", ".yml", ".json", ".txt")):
                text = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
                assert not pat.search(text), os.path.join(root, f)


def test_workflows():
    wf = os.path.join(REPO, ".github", "workflows")
    post = open(os.path.join(wf, "instagram-autopost.yml"), encoding="utf-8").read()
    assert 'cron: "0 0 * * *"' in post
    assert "workflow_dispatch" in post and "dry_run" in post and "force" in post
    assert "concurrency" in post and "contents: write" in post
    assert "vars.IG_AUTOPOST_ENABLED == 'true'" in post
    assert "secrets.IG_ACCESS_TOKEN" in post and "secrets.IG_USER_ID" in post
    gen = open(os.path.join(wf, "instagram-generate-overlays.yml"), encoding="utf-8").read()
    assert "workflow_dispatch" in gen and "generate_overlays.py" in gen
    assert "IG_ACCESS_TOKEN" not in gen        # 生成と投稿は別の実行
