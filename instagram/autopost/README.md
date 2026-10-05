# 馬町珈琲 Instagram 自動投稿キット

京都・東山の自家焙煎珈琲店「馬町珈琲 UMAMACHI COFFEE」の Instagram（@umamachi.coffee）に、
**毎日1回、文字入れ画像＋キャプションを自動で投稿**するための一式です。費用はかかりません。

- 投稿：Meta 公式の **Instagram API**（Instagram ログイン方式・graph.instagram.com・無料）
- 実行：**GitHub Actions**（GitHub のサーバーが毎朝動かす仕組み。PCの電源は不要）
- 画像の置き場：公式サイトと同じ **GitHub Pages**（https://umamachicoffee.jp/instagram/…）

> 専門用語メモ
> - **リポジトリ**：公式サイトのファイル一式が入っている GitHub 上の場所（umamachicoffee/umamachicoffee.github.io）
> - **ワークフロー**：GitHub Actions に「いつ・何をするか」を書いた設定ファイル（.github/workflows/〜.yml）
> - **Secrets（シークレット）**：パスワードのように、他人に見えない形で保存する値。トークンはここに入れる
> - **トークン（アクセストークン）**：Instagram に「この投稿は本人の許可済み」と伝える合言葉の文字列

## 読む順番

| 順 | ファイル | 内容 |
|---|---|---|
| 1 | [01_アップロード手順.md](01_アップロード手順.md) | このキットを GitHub のブラウザ画面からアップロードする方法 |
| 2 | [02_Meta設定ガイド.md](02_Meta設定ガイド.md) | Instagram / Facebook / Meta 開発者アプリの準備、トークン発行、GitHub への登録 |
| 3 | [03_テスト手順.md](03_テスト手順.md) | 確認だけの実行 → 許可を得て1回だけ本番投稿 → 毎日の自動投稿をオン |
| 4 | [04_運用ガイド.md](04_運用ガイド.md) | ログの見方、トークン更新、写真・文章の追加、止め方 |
| 5 | [05_要確認リスト.md](05_要確認リスト.md) | まだ確認が取れていないこと（【要確認】） |
| 6 | [06_画像の選定メモ.md](06_画像の選定メモ.md) | 使った写真・使わなかった写真と理由 |

## 毎日の動き

1. 毎朝 **9:00（日本時間）ごろ** に GitHub Actions が動く（混雑時は数時間遅れることがあります）
2. リポジトリ変数 `IG_AUTOPOST_ENABLED` が `true` でなければ、**何もせず終了**（安全のためのスイッチ）
3. フィード1件・ストーリーズ1件を順番に投稿（リールは動画を登録したときだけ、決めた曜日に）
4. 成功した種類だけ `state.json`（次の番号・最後に投稿した日）を更新し、`post_log.txt` に記録して保存

同じ日に同じ種類を2回投稿しない仕組みになっています（手動実行で `force` をオンにしたときだけ例外）。

## ファイル構成（リポジトリ内）

```
.github/workflows/
  instagram-autopost.yml            毎日の自動投稿（＋手動実行）
  instagram-generate-overlays.yml   文字入れ画像の作り直し（手動実行のみ）
instagram/
  photos/                           文字入れの元写真（JPEG）
  generated/feed/                   フィード用 1080x1350（自動で作った完成画像）
  generated/story/                  ストーリーズ用 1080x1920（同上）
  videos/                           リール用動画（いまは空）
  autopost/
    config.py                       ★頻度（毎日／曜日）などの設定はここだけ
    content.py                      ★投稿内容（文字入れの文言・キャプション）はここだけ
    post_instagram.py               投稿本体
    generate_overlays.py            文字入れ画像を作るプログラム
    state.json                      次に投稿する番号・最後に投稿した日（自動更新）
    post_log.txt                    成功・失敗の記録（自動追記）
    requirements*.txt               必要な部品の一覧
    fonts/ZenMaruGothic-Medium.ttf  文字入れのフォント（Zen Maru Gothic、SIL Open Font License）
    fonts/OFL.txt                   フォントのライセンス文
    tests/                          自動チェック（本物の Instagram には接続しません）
```

既存のサイトのファイル（index.html、assets/ など）には一切手を加えていません。

## できないこと（Instagram API の制限）

- **ストーリーズのスタンプ・リンク・音楽・アンケート**、**リールの音楽（BGM）** は API では付けられません。必要なときはアプリから手動で投稿してください。
- **ストーリーズには文章（キャプション）を付けられません**。文字は画像の中に入れてあります。
- 画像は **JPEG** のみ使っています（PNG/WebP は弾かれることがあるため）。

## 注意

- `instagram/` 以下のファイル（state.json、post_log.txt、この説明書を含む）は公開サイトの一部として誰でも見られます。トークンなどの秘密は一切書いていません。今後も書かないでください。
- 自動投稿の結果が毎日1回リポジトリに保存されるため、サイトのコミット履歴に「instagram: update state and log」が毎日並びます。
