# 02 Meta（Instagram / Facebook）の準備と GitHub への登録

ここは俵原さんが手作業で行う部分です。**トークン（合言葉の文字列）は、チャット・メール・ファイルに貼らず、GitHub の Secrets にだけ入れてください。**
Meta の画面は時期によってボタン名や配置が少し変わることがあります。見当たらないときは、似た名前のボタンを探してください。

---

## ステップ1：Instagram を「プロアカウント（ビジネス）」にする

（すでにビジネス／クリエイターなら飛ばしてOK）

1. スマホの Instagram アプリで @umamachi.coffee にログイン
2. 右下のプロフィール → 右上の **≡（メニュー）** → **設定とアクティビティ**
3. **アカウントの種類とツール**（または「クリエイター・ビジネス向けツール」）→ **プロアカウントに切り替える**
4. カテゴリ（例：カフェ）を選び、**ビジネス** を選んで完了
5. アカウントが **公開** になっていることを確認（非公開だと API で投稿できません）

## ステップ2：Facebook ページを作り、Instagram とつなぐ

1. Facebook（俵原さんの個人アカウント）にログイン → 左メニュー **ページ** → **新しいページを作成**
   - ページ名：`馬町珈琲 UMAMACHI COFFEE`、カテゴリ：カフェ → **ページを作成**
   （すでにお店のページがあれば、それを使います）
2. Instagram アプリ → プロフィール → **プロフィールを編集** → **ページ**（「Facebookページをリンク」）
   → 上で作ったページを選んで **完了**
   - または Meta Business Suite（business.facebook.com）→ **設定** → **Instagram アカウント** → **接続** でも可

## ステップ3：Meta for Developers でアプリを作る

1. https://developers.facebook.com/ を開き、右上 **ログイン**（Facebook アカウント）
   - 初めての場合は **スタート**／**Get Started** から開発者登録（電話番号の確認などがあります）
2. 右上 **マイアプリ**（My Apps）→ **アプリを作成**（Create App）
3. アプリ名：`umamachi-ig-autopost` など（「Instagram」「IG」という語は名前に使えないことがあります）、連絡先メール → **次へ**
4. ユースケースで **「Instagramでメッセージとコンテンツを管理」**（Manage messaging & content on Instagram）を選ぶ → **次へ**
   - ビジネスポートフォリオ（ビジネスマネージャ）の選択は「今はリンクしない」でも可
5. 確認画面で **アプリを作成** → パスワードを再入力
6. 自分のアカウントだけに投稿する使い方なので、アプリは **開発モード（Development）のままでOK** です（公開・審査は不要）

## ステップ4：Instagram アカウントを「Instagramテスター」に追加する

1. アプリのダッシュボード左メニュー一番下の **アプリの役割**（App roles）→ **役割**（Roles）
2. 右上 **メンバーを追加**（Add People）
3. 役割の一覧から **Instagramテスター**（Instagram Tester）を選ぶ
4. 下の検索欄に入力して探す
   - **メールアドレスでは見つかりません。**（過去にヒットしなかった実績あり）
   - Instagram のユーザー名 `umamachi.coffee`、または **Facebook の「表示名」**（プロフィールに出ている名前）で検索してください
5. 見つかったアカウントを選んで **追加**。状態が **保留中**（Pending）になります
6. 招待を承認する（Instagram 側）
   - スマホの Instagram アプリ → **≡** → **設定とアクティビティ** → **ウェブサイトのアクセス許可** → **アプリとウェブサイト** → **テスターへの招待** → アプリ名（〜-IG）の **承認**
   - PC の場合：instagram.com → 設定 → **アプリとウェブサイト** → **テスターへの招待**
7. 開発者ダッシュボードに戻り、状態が **有効**（Active）になったことを確認

## ステップ5：アクセストークンを発行する（ダッシュボードの「トークンを生成」）

1. ダッシュボード左メニュー **ユースケース** → 「Instagramでメッセージとコンテンツを管理」の **カスタマイズ**
   → **Instagramログインによる API 設定**（API setup with Instagram login）
   （画面によっては左メニュー **Instagram** → **API setup with Instagram login**）
2. 「**1. アクセストークンを生成**」（Generate access tokens）の欄で **アカウントを追加**（Add account）
   → Instagram のログイン画面が開くので @umamachi.coffee でログイン → 権限（コンテンツの公開など）を **許可**
3. 一覧に @umamachi.coffee が表示されます。その行にある **数字のID** が **Instagram ユーザーID** です（`IG_USER_ID` に使います。17841… で始まる長い数字）
4. 同じ行の **トークンを生成**（Generate token）→ 確認で **許可**
5. 長い文字列（トークン）が表示されます。**コピーボタン**でコピーし、**すぐに次のステップ6で GitHub に貼り付け**てください
   - トークンは一度しか表示されません。メモ帳などに保存しないでください
   - 別の店舗では「長期トークンへの交換（ig_exchange_token）」が「Session key invalid」で失敗しましたが、
     **ここで表示されたトークンをそのまま使えば投稿できています**。交換作業は不要です

### トークンの有効期限

- Meta の説明では、この方法で出したトークンは **約60日** 有効です（実際の期限は【要確認】）。
- 期限は Meta の「アクセストークンデバッガー」（https://developers.facebook.com/tools/debug/accesstoken/ ）にトークンを貼ると確認できます。
  （確認後はページを閉じ、トークンをどこにも残さないでください）
- **期限が切れると投稿が突然止まります。** 50日ごとを目安に、同じ手順でトークンを作り直して Secrets を更新してください（[04_運用ガイド.md](04_運用ガイド.md)）。

## ステップ6：GitHub に Secrets（秘密の値）を登録する

1. https://github.com/umamachicoffee/umamachicoffee.github.io → **Settings**
2. 左メニュー **Secrets and variables** → **Actions**
3. 「Secrets」タブで **New repository secret**
   - Name：`IG_ACCESS_TOKEN`　Secret：ステップ5のトークンを貼り付け → **Add secret**
4. もう一度 **New repository secret**
   - Name：`IG_USER_ID`　Secret：ステップ5の数字のID → **Add secret**

名前は **半角・大文字・この綴りのまま** にしてください。登録した値は、あとから誰も（自分も）表示できません。変更は「Update」から上書きします。

## ステップ7：自動投稿のスイッチ（変数）を用意する

1. 同じ画面の **Variables** タブ → **New repository variable**
2. Name：`IG_AUTOPOST_ENABLED`　Value：**`false`** → **Add variable**

- `true` にすると、毎朝の自動投稿が動き始めます。**いまは `false` のまま**にしておきます。
- **10月5日〜12日は Meta Business Suite で予約投稿が入っているため、`true` にするのは 10月13日以降** にしてください（二重投稿防止）。
- 手順は [03_テスト手順.md](03_テスト手順.md) を参照。
