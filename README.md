# 馬町珈琲 UMAMACHI COFFEE — 公式サイト

京都・東山区常盤町の自家焙煎珈琲店「馬町珈琲」の公式サイト。運営：株式会社緑歩園。

素の HTML / CSS / JS のみ。ビルド不要。GitHub Pages で配信します。

## 構成

```
index.html              ページ本体
assets/
  content.js            全原稿とメニューデータ（5言語）★編集はここ
  style.css
  main.js               言語切替・スクロール演出
  img/                  最適化済み写真
  video/umamachi-reel.mp4
.nojekyll               Pages の Jekyll 処理を止める
```

## 対応言語

日本語 / English / 中文（簡体） / 한국어 / Español

切替はクライアント側。選択は `localStorage` に保存され、初回は `navigator.languages` から推定します。URL に `?lang=en` を付けても切り替わります。

## 文言を直すとき

`assets/content.js` の `SITE.t.<言語コード>` を編集します。HTML は触りません。
5言語すべてに同じキーがあるので、**1言語だけ直して他を放置しない**こと。

## メニューを直すとき

同じく `assets/content.js`。

- `SITE.food` … フード5品
- `SITE.coffee` … 自社焙煎コーヒー
- `SITE.beverage` … その他ドリンク（`group` は `jp`＝日本茶／`herbal`＝ハーブティー／`null`＝グループなし）

価格は文字列で持っています（例 `'1,300'`）。

## Instagram

`assets/content.js` の `SITE.shop.instagram` にハンドル（`@` を除いた英数字）を入れると、
Instagram セクションのリンクが有効になります。初期値 `'INSTAGRAM_HANDLE'` のあいだは
リンクを出さず、店の写真グリッドだけを表示します。

埋め込みウィジェットを使う場合は `index.html` の `#ig-embed` に埋め込みコードを貼ります。

## 公開

`main` ブランチのルートを GitHub Pages のソースにしています。push すると数分で反映されます。

独自ドメインを設定する場合はリポジトリ直下に `CNAME` を置き、DNS 側で CNAME を向けます。
Xserver Domain は CAA レコード非対応のため、SSL 証明書が発行されないときは
apex ドメイン（www なし）で設定し直すと通ることがあります。

## 素材の出典

- 写真・動画：店舗撮影分
- メニュー：`A3_drink.pdf` / `A3_food.pdf`
- 本文：「馬町珈琲のコメント.docx」

焙煎機 GIESEN の製造国は**オランダ**です（店内ポスターの「ドイツGIESEN社」表記は誤り）。

## 今回載せていないもの

- ランチメニュー（旧店名「Gojo Coffee Factory」表記の素材しかなく、現行かどうか未確認のため）
- 価格の税込・税別表記（未確認のため記載していません）
