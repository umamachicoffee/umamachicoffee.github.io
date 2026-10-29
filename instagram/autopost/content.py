# -*- coding: utf-8 -*-
"""馬町珈琲 Instagram 自動投稿 ― 投稿内容（画像・文字入れ・キャプション）の一覧。

■ 1件 = 1回の投稿。上から順番に投稿し、最後まで行ったら先頭に戻ります。
■ 画像の文字入れ（headline / info / subline）と、キャプション（caption）は1件の中でセットです。
■ 写真を追加したら instagram/photos/ に JPEG を入れ、ここに1件追加 →
   GitHub の Actions「Instagram generate overlays」を実行すると、文字入れ画像が作られます。

各項目の意味：
  id        : 半角英数字とハイフン。生成される画像のファイル名になります（例 f01-blend → generated/feed/f01-blend.jpg）
  photo     : instagram/photos/ の中の元写真のファイル名
  crop      : 元写真のどの範囲を使うか（左, 上, 右, 下 を 0〜1 の割合で）。None なら全体
  focus     : 縦横比を合わせて切り抜くときの中心（横, 縦 を 0〜1 で。0.5,0.5 が真ん中）
  layout    : "photo"（写真に文字）または "card"（ロゴを無地の背景に置く）
  position  : 文字の位置 "bottom"（下）または "top"（上）
  headline  : 画像に入れる日本語の見出し（短く。改行は \n）
  info      : 見出しの下の小さめの日本語（価格など。無ければ ""）
  subline   : 小さな英語の1行
  caption   : 投稿文（フィードとリールのみ。ストーリーズはAPIの仕様で文章を付けられません）
  months    : その月だけ投稿する（季節もの）。例 [9, 10, 11]。None なら通年
  enabled   : False にすると投稿しない（画像も作らない）。書かなければ True（投稿する）
"""
import textwrap


def cap(ja, en, tags):
    """キャプションを「日本語 → 空行 → 英語 → 空行 → ハッシュタグ」の形に組み立てる。"""
    ja = textwrap.dedent(ja).strip()
    en = textwrap.dedent(en).strip()
    tags = " ".join(textwrap.dedent(tags).split())
    return f"{ja}\n\n{en}\n\n{tags}"


# よく使う基本のハッシュタグ（英語のみ。#specialtycoffee / #singleorigin は使わない）
BASE_TAGS = "#umamachicoffee #kyotocafe #kyotocoffee #higashiyama #kyoto"

# =====================================================================
# フィード投稿（1080x1350）
# =====================================================================
FEED = [
    dict(
        id="f01-blend",
        # 一杯の写真（豆の写真に ¥580 を載せると、豆の価格 100g ¥880 と混同されるため）
        photo="cup-blend.jpg", crop=(0.0, 0.12, 1.0, 0.95), focus=(0.5, 0.5),
        layout="photo", position="bottom",
        headline="馬町ブレンド", info="一杯 ¥580（税込）", subline="Umamachi Blend — ¥580 per cup",
        caption=cap(
            """
            自家焙煎のハウスブレンド「馬町ブレンド」。
            エスプレッソにも、同じ豆を使っています。
            一杯ずつ、ゆっくり味わっていただけたらうれしいです。

            馬町ブレンド 一杯 ¥580（税込）
            """,
            """
            Umamachi Blend is our house blend, roasted by us.
            Our espresso is made with the same beans.
            We hope you enjoy it slowly, one cup at a time.

            Umamachi Blend ¥580 per cup (tax included)
            """,
            BASE_TAGS + " #houseblend #houseroasted #coffeeroaster #coffeetime #blackcoffee #japancafe",
        ),
        months=None,
    ),
    dict(
        id="f02-kyoto-moon-burger",
        # 京都ムーンバーガー＝目玉焼きのせ（オーナー確認済み）。写真は目玉焼きが写っている IMG_4147
        photo="burger-kyoto-moon.jpg", crop=None, focus=(0.5, 0.5),
        layout="photo", position="bottom",
        headline="京都ムーンバーガー", info="¥1,000（税込）", subline="Kyoto Moon Burger",
        caption=cap(
            """
            目玉焼きをのせた「京都ムーンバーガー」。
            珈琲と一緒に、しっかり食べたい日にどうぞ。

            京都ムーンバーガー ¥1,000（税込）
            """,
            """
            Our Kyoto Moon Burger, topped with a fried egg.
            For days when you want a proper meal with your coffee.

            Kyoto Moon Burger ¥1,000 (tax included)
            """,
            BASE_TAGS + " #burger #kyotofood #cafefood #coffeeandburger #kyotoeats #japantravel",
        ),
        months=None,
    ),
    dict(
        id="f03-interior",
        photo="interior-deep.jpg", crop=(0.0, 0.08, 1.0, 1.0), focus=(0.5, 0.5),
        layout="photo", position="bottom",
        headline="奥まで、ゆっくり。", info="", subline="Take your time inside",
        caption=cap(
            """
            入口から奥へと続く、木の柱とコンクリートの床の店内。
            おひとりでも、どなたかとご一緒でも。
            珈琲を片手に、ゆっくりお過ごしください。
            """,
            """
            Wooden pillars and a concrete floor, stretching back from the entrance.
            Whether you come alone or with someone,
            please take your time over a cup of coffee.
            """,
            BASE_TAGS + " #cafeinterior #coffeeshop #kyotocafes #cafetime #japancafe #kyototrip",
        ),
        months=None,
    ),
    dict(
        id="f04-roasting",
        photo="roaster-poster.jpg", crop=(0.03, 0.05, 1.0, 0.62), focus=(0.22, 0.5),
        layout="photo", position="bottom",
        headline="自家焙煎の珈琲", info="焙煎機はオランダ製 GIESEN", subline="House-roasted on a Dutch GIESEN roaster",
        caption=cap(
            """
            馬町珈琲の豆は、オランダ製の焙煎機「GIESEN（ギーセン）」で自家焙煎しています。
            ブレンドもエスプレッソも、同じ豆から。
            """,
            """
            Our beans are roasted by us on a GIESEN roaster, made in the Netherlands.
            Both our blend and our espresso come from the same beans.
            """,
            BASE_TAGS + " #houseroasted #coffeeroasting #giesen #coffeeroaster #roastery #coffeebeans",
        ),
        months=None,
    ),
    dict(
        id="f05-visit",
        photo="exterior.jpg", crop=(0.0, 0.0, 1.0, 0.92), focus=(0.5, 0.5),
        layout="photo", position="top",
        headline="東山・馬町の珈琲店", info="9:00〜17:00 ／ 定休日なし", subline="Open 9:00–17:00, no regular closing day",
        caption=cap(
            """
            京都・東山の自家焙煎珈琲店です。
            お近くにお越しの際は、どうぞお立ち寄りください。

            馬町珈琲 UMAMACHI COFFEE
            京都市東山区常盤町459-13
            営業時間 9:00〜17:00
            定休日なし
            TEL 075-741-8779
            """,
            """
            A house-roasting coffee shop in Higashiyama, Kyoto.
            Please drop by when you are in the area.

            UMAMACHI COFFEE
            459-13 Tokiwacho, Higashiyama-ku, Kyoto
            Open 9:00–17:00, no regular closing day
            TEL 075-741-8779
            """,
            BASE_TAGS + " #kyototrip #visitkyoto #kyotojapan #coffeeshop #houseroasted #japancafe",
        ),
        months=None,
    ),
    dict(
        id="f06-takeout",
        photo="iced-coffee.jpg", crop=None, focus=(0.5, 0.55),
        layout="photo", position="top",
        headline="テイクアウトもできます", info="", subline="Takeout available",
        caption=cap(
            """
            店内でも、お持ち帰りでも。
            お散歩のおともに、珈琲をテイクアウトでどうぞ。
            """,
            """
            Enjoy it here, or take it with you.
            Our coffee is also available for takeout.
            """,
            BASE_TAGS + " #takeoutcoffee #coffeetogo #icedcoffee #coffeetime #kyotowalk #japancafe",
        ),
        months=None,
    ),
    dict(
        id="f07-omelette-sandwich",
        # オムレツサンドイッチ ¥880（税込）（Airレジの販売実績で確認済み）
        photo="sandwich-omelette.jpg", crop=None, focus=(0.5, 0.5),
        layout="photo", position="bottom",
        headline="オムレツサンドイッチ", info="¥880（税込）", subline="Omelette Sandwich",
        caption=cap(
            """
            馬町珈琲の「オムレツサンドイッチ」。
            珈琲と一緒にどうぞ。

            オムレツサンドイッチ ¥880（税込）
            """,
            """
            Our Omelette Sandwich.
            Lovely with a cup of coffee.

            Omelette Sandwich ¥880 (tax included)
            """,
            BASE_TAGS + " #sandwich #eggsandwich #cafefood #coffeeandsandwich #kyotofood #kyotoeats",
        ),
        months=None,
    ),
    dict(
        id="f08-autumn-afternoon",
        photo="interior-wide.jpg", crop=None, focus=(0.45, 0.5),
        layout="photo", position="bottom",
        headline="秋の午後に、一杯を", info="", subline="An autumn afternoon with coffee",
        caption=cap(
            """
            過ごしやすい季節になりました。
            散策のひと休みに、あたたかい珈琲はいかがですか。
            """,
            """
            The weather has turned pleasant.
            How about a warm cup of coffee as a break from your walk?
            """,
            BASE_TAGS + " #autumninkyoto #kyotoautumn #cafetime #coffeebreak #kyototrip #japancafe",
        ),
        months=[9, 10, 11],
    ),
    dict(
        id="f09-beans",
        # TODO: オーナーから珈琲豆の袋の写真が届いたら、その写真に差し替える（今は焙煎機ポスターの豆部分）
        photo="roaster-poster.jpg", crop=(0.0, 0.62, 1.0, 1.0), focus=(0.15, 0.5),
        layout="photo", position="top",
        headline="珈琲豆、100gから", info="100g ¥880 ／ 200g ¥1,560（税込）", subline="Coffee beans from 100 g",
        caption=cap(
            """
            自家焙煎の珈琲豆を販売しています。
            100gから、100g単位でお求めいただけます。

            100g ¥880 ／ 200g ¥1,560（税込）
            """,
            """
            Our house-roasted coffee beans are available to take home.
            Sold from 100 g, in 100 g steps.

            100 g ¥880 / 200 g ¥1,560 (tax included)
            """,
            BASE_TAGS + " #coffeebeans #houseroasted #homecoffee #coffeeroaster #roastery #coffeelover",
        ),
        months=None,
    ),
    dict(
        id="f10-espresso",
        photo="espresso.jpg", crop=(0.0, 0.05, 1.0, 0.95), focus=(0.5, 0.5),
        layout="photo", position="bottom",
        headline="エスプレッソ", info="¥400（税込）", subline="Espresso, from our house blend beans",
        caption=cap(
            """
            エスプレッソには、馬町ブレンドと同じ豆を使っています。
            小さな一杯で、ひと息どうぞ。

            エスプレッソ ¥400（税込）
            """,
            """
            Our espresso is made with the same beans as the Umamachi Blend.
            A small cup for a short pause.

            Espresso ¥400 (tax included)
            """,
            BASE_TAGS + " #espresso #espressoshot #houseblend #coffeetime #baristalife #japancafe",
        ),
        months=None,
    ),
    dict(
        id="f11-umamachi-burger",
        # 馬町バーガー ¥1,300（税込）。写真は IMG_4146（オーナー確認済み）
        photo="burger-umamachi.jpg", crop=None, focus=(0.4, 0.5),
        layout="photo", position="bottom",
        headline="馬町バーガー", info="¥1,300（税込）", subline="Umamachi Burger",
        caption=cap(
            """
            馬町珈琲の「馬町バーガー」。
            珈琲と一緒に、ゆっくり召し上がってください。

            馬町バーガー ¥1,300（税込）
            """,
            """
            Our Umamachi Burger.
            Please take your time and enjoy it with coffee.

            Umamachi Burger ¥1,300 (tax included)
            """,
            BASE_TAGS + " #burger #hamburger #cafefood #kyotofood #kyotoeats #japantravel",
        ),
        months=None,
    ),
    dict(
        id="f12-hours",
        photo="logo-horse.jpg", crop=None, focus=(0.5, 0.5),
        layout="card", position="bottom",
        headline="9:00〜17:00", info="定休日なし", subline="Open 9:00–17:00 · No regular closing day",
        caption=cap(
            """
            営業時間のご案内です。

            営業時間 9:00〜17:00
            定休日なし
            京都市東山区常盤町459-13
            TEL 075-741-8779

            店内のほか、テイクアウトと珈琲豆の販売もしています。
            """,
            """
            Our opening hours.

            Open 9:00–17:00
            No regular closing day
            459-13 Tokiwacho, Higashiyama-ku, Kyoto
            TEL 075-741-8779

            Eat in, takeout, and coffee beans to take home.
            """,
            BASE_TAGS + " #coffeeshop #kyototrip #visitkyoto #kyotojapan #houseroasted #japancafe",
        ),
        months=None,
    ),
    dict(
        id="f13-autumn-walk",
        photo="exterior-wide.jpg", crop=None, focus=(0.45, 0.5),
        layout="photo", position="bottom",
        headline="秋の東山さんぽに", info="", subline="A coffee stop on your autumn walk",
        caption=cap(
            """
            東山を歩くのが心地よい季節です。
            お散歩の途中に、珈琲でひと休みしていきませんか。
            テイクアウトもできます。
            """,
            """
            It is a lovely season for walking around Higashiyama.
            Why not stop for a coffee along the way?
            Takeout is also available.
            """,
            BASE_TAGS + " #kyotoautumn #autumninkyoto #kyotowalk #visitkyoto #coffeebreak #takeoutcoffee",
        ),
        months=[9, 10, 11],
    ),
    dict(
        id="f14-cafe-latte",
        # 元写真が小さい（480x640）ため、ローテーションの最後に置いています。
        photo="latte.jpg", crop=None, focus=(0.4, 0.6),
        layout="photo", position="top",
        headline="カフェラテ", info="¥630（税込）", subline="Caffè latte",
        caption=cap(
            """
            馬町ブレンドと同じ豆のエスプレッソに、ミルクを合わせたカフェラテ。
            やさしい味わいの一杯です。

            カフェラテ ¥630（税込）
            """,
            """
            Our caffè latte: espresso from the same beans as the Umamachi Blend, with milk.
            A gentle, comforting cup.

            Caffè latte ¥630 (tax included)
            """,
            BASE_TAGS + " #cafelatte #latte #latteart #coffeetime #houseblend #japancafe",
        ),
        months=None,
    ),
]

# =====================================================================
# ストーリーズ（1080x1920）。Instagram API ではストーリーズに文章・スタンプ・音楽は付けられません。
# 文字は画像の中に入れています。
# =====================================================================
STORIES = [
    dict(id="s01-hours", photo="logo-horse.jpg", crop=None, focus=(0.5, 0.5), layout="card", position="bottom",
         headline="営業時間 9:00〜17:00", info="定休日なし", subline="Open 9:00–17:00 · No regular closing day"),
    # TODO: 珈琲豆の袋の写真が届いたら差し替える
    dict(id="s02-beans", photo="roaster-poster.jpg", crop=(0.0, 0.55, 1.0, 1.0), focus=(0.25, 0.5), layout="photo", position="top",
         headline="珈琲豆、100gから", info="100g ¥880 ／ 200g ¥1,560（税込）", subline="House-roasted coffee beans"),
    # 京都ムーンバーガー＝目玉焼きのせ。写真は IMG_4147（目玉焼きあり）
    dict(id="s03-kyoto-moon-burger", photo="burger-kyoto-moon.jpg", crop=None, focus=(0.5, 0.5), layout="photo", position="bottom",
         headline="京都ムーンバーガー", info="¥1,000（税込）", subline="Kyoto Moon Burger"),
    dict(id="s04-interior", photo="interior-deep.jpg", crop=None, focus=(0.5, 0.5), layout="photo", position="bottom",
         headline="ゆっくり、どうぞ", info="", subline="Take your time"),
    dict(id="s05-espresso", photo="espresso.jpg", crop=None, focus=(0.5, 0.5), layout="photo", position="bottom",
         headline="エスプレッソ", info="¥400（税込）", subline="Espresso, from our house blend beans"),
    dict(id="s06-takeout", photo="iced-coffee.jpg", crop=None, focus=(0.5, 0.5), layout="photo", position="top",
         headline="テイクアウトもできます", info="", subline="Takeout available"),
    dict(id="s07-roasting", photo="roaster-poster.jpg", crop=(0.0, 0.04, 1.0, 0.66), focus=(0.85, 0.5), layout="photo", position="bottom",
         headline="自家焙煎の珈琲", info="焙煎機はオランダ製 GIESEN", subline="House-roasted on a Dutch GIESEN roaster"),
    dict(id="s08-access", photo="exterior.jpg", crop=None, focus=(0.5, 0.5), layout="photo", position="bottom",
         headline="京都市東山区常盤町459-13", info="TEL 075-741-8779", subline="459-13 Tokiwacho, Higashiyama-ku, Kyoto"),
    # 一杯の写真＋「一杯 ¥580」（豆の価格と混同しないように）
    dict(id="s09-blend", photo="cup-blend.jpg", crop=None, focus=(0.5, 0.5), layout="photo", position="bottom",
         headline="馬町ブレンド", info="一杯 ¥580（税込）", subline="Umamachi Blend — ¥580 per cup"),
]

# =====================================================================
# リール。video に instagram/videos/ の MP4 ファイル名（または https:// から始まる公開URL）を入れると投稿対象になります。
# video が空（None）の項目は投稿しません。いまは動画が無いので、リールは自動的にスキップされます。
# 音楽・スタンプはAPIでは付けられません（必要ならアプリから手動で投稿してください）。
# =====================================================================
REELS = [
    dict(
        id="r01-espresso",
        video=None,
        caption=cap(
            """
            エスプレッソを抽出しているところです。
            馬町ブレンドと同じ豆を使っています。

            エスプレッソ ¥400（税込）
            """,
            """
            Pulling a shot of espresso,
            made with the same beans as our Umamachi Blend.

            Espresso ¥400 (tax included)
            """,
            BASE_TAGS + " #espresso #espressoshot #coffeereels #baristalife #houseblend #japancafe",
        ),
    ),
    dict(
        id="r02-roasting",
        video=None,
        caption=cap(
            """
            オランダ製の焙煎機「GIESEN」で、豆を自家焙煎しています。
            珈琲豆は100gから販売しています（100g ¥880 ／ 200g ¥1,560・税込）。
            """,
            """
            We roast our own beans on a GIESEN roaster, made in the Netherlands.
            Beans are sold from 100 g (100 g ¥880 / 200 g ¥1,560, tax included).
            """,
            BASE_TAGS + " #coffeeroasting #giesen #houseroasted #roastery #coffeebeans #coffeereels",
        ),
    ),
    dict(
        id="r03-shop",
        video=None,
        caption=cap(
            """
            京都・東山の馬町珈琲です。
            営業時間 9:00〜17:00、定休日なし。
            京都市東山区常盤町459-13
            """,
            """
            UMAMACHI COFFEE in Higashiyama, Kyoto.
            Open 9:00–17:00, no regular closing day.
            459-13 Tokiwacho, Higashiyama-ku, Kyoto
            """,
            BASE_TAGS + " #coffeeshop #kyototrip #visitkyoto #cafereels #houseroasted #japancafe",
        ),
    ),
]
