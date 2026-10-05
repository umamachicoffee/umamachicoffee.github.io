# -*- coding: utf-8 -*-
"""馬町珈琲 Instagram 自動投稿 ― 設定はこのファイル1か所だけ。

いじってよいのは主に CADENCE（どの種類を、何曜日に投稿するか）です。
キャプションや画像の中身は content.py を編集します。
"""

# ── 投稿の頻度（ここだけで管理） ─────────────────────────────
# days: "daily"（毎日） または 曜日のリスト ["mon","tue","wed","thu","fri","sat","sun"]
# enabled: False にするとその種類は投稿しません（止めたいときに使う）
# 曜日・日付はすべて日本時間（JST）で判定します。
CADENCE = {
    "feed":  {"enabled": True, "days": "daily"},     # フィード投稿（1080x1350の画像）
    "story": {"enabled": True, "days": "daily"},     # ストーリーズ（1080x1920の画像）
    # リールは content.py の REELS に動画(video)が1本も登録されていなければ自動的にスキップ。
    "reel":  {"enabled": True, "days": ["fri"]},
}

# ── 公開URL ───────────────────────────────────────────────
# Instagram はこのURLから画像・動画を取りに来ます（GitHub Pages で公開済みであること）。
SITE_BASE_URL = "https://umamachicoffee.jp/instagram/"
GENERATED_BASE_URL = SITE_BASE_URL + "generated/"   # 文字入れ済み画像（feed/ と story/）
VIDEO_BASE_URL = SITE_BASE_URL + "videos/"          # リール用動画（MP4）

# ── Instagram API ────────────────────────────────────────
# Instagram ログイン方式（graph.instagram.com）。バージョンは仕様書どおり v21.0。
# ※ v21.0 は 2027年1月21日に提供終了予定（Meta公式の一覧より）。それまでに "v25.0" 等へ変更してください。
GRAPH_HOST = "https://graph.instagram.com"
API_VERSION = "v21.0"

# 処理完了（status_code=FINISHED）を待つ時間
IMAGE_POLL_INTERVAL_SEC = 3
IMAGE_POLL_TIMEOUT_SEC = 60
VIDEO_POLL_INTERVAL_SEC = 10
VIDEO_POLL_TIMEOUT_SEC = 300      # リールは最大約5分待つ

HTTP_TIMEOUT_SEC = 30
