# -*- coding: utf-8 -*-
"""馬町珈琲 Instagram 自動投稿 ― 投稿本体。

GitHub Actions から1日1回（日本時間9:00ごろ）実行されます。
  python instagram/autopost/post_instagram.py --dry-run     # 投稿せず「何を投稿するか」だけ表示
  python instagram/autopost/post_instagram.py --only feed   # フィードだけ

ルール
- アクセストークン(IG_ACCESS_TOKEN)とユーザーID(IG_USER_ID)は環境変数からだけ読みます。ファイルやログには書きません。
- 種類（feed / story / reel）ごとに「次に投稿する番号」と「最後に投稿した日（日本時間）」を state.json に記録します。
- 記録を更新するのは、その種類の投稿が成功したときだけ。失敗したら次回、同じものから再挑戦します。
- 同じ日に同じ種類を2回投稿しません（--force を付けたときだけ例外）。
- 1つの種類が失敗しても、ほかの種類は続けます。1つでも失敗したら終了コード1（Actions が赤くなります）。
- 定時実行（schedule）は、リポジトリ変数 IG_AUTOPOST_ENABLED が "true" のときだけ動きます。
"""
import argparse
import datetime as dt
import json
import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config  # noqa: E402
import content  # noqa: E402

STATE_PATH = os.path.join(HERE, "state.json")
LOG_PATH = os.path.join(HERE, "post_log.txt")
JST = dt.timezone(dt.timedelta(hours=9), "JST")
TYPES = ("feed", "story", "reel")
WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
TYPE_LABEL = {"feed": "フィード", "story": "ストーリーズ", "reel": "リール"}


class PostError(Exception):
    """投稿の失敗（HTTPエラー、処理エラー、時間切れなど）。"""


# ───────────────────────── 小さな道具 ─────────────────────────
def now_jst():
    return dt.datetime.now(JST)


def redact(text, secrets):
    """ログに秘密の値が混ざらないよう伏せ字にする。"""
    text = str(text)
    for s in secrets:
        if s:
            text = text.replace(s, "***")
    return text


class Logger:
    def __init__(self, path, secrets=(), write_file=True, clock=now_jst):
        self.path = path
        self.secrets = [s for s in secrets if s]
        self.write_file = write_file
        self.clock = clock

    def __call__(self, level, message):
        line = f"{self.clock().strftime('%Y-%m-%d %H:%M:%S')} JST [{level}] {redact(message, self.secrets)}"
        print(line, flush=True)
        if self.write_file:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")


def default_state():
    return {t: {"last_index": -1, "last_posted_date": None, "last_media_id": None, "last_id": None} for t in TYPES}


def load_state(path=STATE_PATH):
    state = default_state()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        for t in TYPES:
            if isinstance(raw.get(t), dict):
                state[t].update(raw[t])
    return state


def save_state(state, path=STATE_PATH):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def entries_for(kind):
    return {"feed": content.FEED, "story": content.STORIES, "reel": content.REELS}[kind]


def is_eligible(kind, entry, today):
    if entry.get("enabled", True) is False:
        return False                     # enabled=False の項目は投稿しない
    if kind == "reel" and not entry.get("video"):
        return False                     # 動画が未登録のリールは投稿しない
    months = entry.get("months")
    if months and today.month not in months:
        return False                     # 季節ものは対象の月だけ
    return True


def pick_next(kind, state, today):
    """前回の続きから、今日投稿できる最初の項目を選ぶ。無ければ None。"""
    entries = entries_for(kind)
    n = len(entries)
    if n == 0:
        return None
    start = (state[kind].get("last_index", -1) + 1) % n
    for k in range(n):
        i = (start + k) % n
        if is_eligible(kind, entries[i], today):
            return i
    return None


def is_due(kind, today, cadence=None):
    c = (cadence or config.CADENCE).get(kind, {})
    if not c.get("enabled", False):
        return False, "設定で無効（config.py の CADENCE）"
    days = c.get("days", "daily")
    if days == "daily":
        return True, ""
    wd = WEEKDAYS[today.weekday()]
    if wd in [d.lower()[:3] for d in days]:
        return True, ""
    return False, f"今日（{wd}）は投稿日ではありません（config.py の CADENCE）"


def media_url(kind, entry):
    if kind == "feed":
        return config.GENERATED_BASE_URL + "feed/" + entry["id"] + ".jpg"
    if kind == "story":
        return config.GENERATED_BASE_URL + "story/" + entry["id"] + ".jpg"
    v = entry["video"]
    return v if v.startswith("https://") else config.VIDEO_BASE_URL + v


def build_params(kind, entry, url):
    if kind == "feed":
        return {"image_url": url, "caption": entry["caption"]}
    if kind == "story":
        return {"media_type": "STORIES", "image_url": url}   # ストーリーズにキャプションは付けられない
    return {"media_type": "REELS", "video_url": url, "caption": entry["caption"], "share_to_feed": "true"}


def check_public_url(url, session, timeout=config.HTTP_TIMEOUT_SEC):
    """Instagram が取りに来る前に、画像・動画が公開URLで見られるか確かめる。"""
    try:
        r = session.head(url, timeout=timeout, allow_redirects=True)
    except requests.RequestException as e:
        raise PostError(f"公開URLに接続できません: {url} ({type(e).__name__})")
    if r.status_code != 200:
        raise PostError(f"公開URLが見つかりません (HTTP {r.status_code}): {url} "
                        "― アップロード直後なら GitHub Pages の反映を数分待ってください")
    ctype = r.headers.get("Content-Type", "")
    if url.endswith(".jpg") and "jpeg" not in ctype:
        raise PostError(f"JPEGではありません (Content-Type: {ctype}): {url}")


# ───────────────────────── Instagram API ─────────────────────────
class InstagramClient:
    def __init__(self, token, user_id, session=None, sleep=time.sleep,
                 host=config.GRAPH_HOST, version=config.API_VERSION):
        self.token = token
        self.user_id = user_id
        self.s = session or requests.Session()
        self.sleep = sleep
        self.base = f"{host}/{version}"

    def _check(self, r, what):
        if r.status_code != 200:
            body = redact(r.text[:1500], [self.token])
            raise PostError(f"{what} が失敗 (HTTP {r.status_code}) 応答: {body}")
        try:
            return r.json()
        except ValueError:
            raise PostError(f"{what} の応答がJSONではありません: {redact(r.text[:300], [self.token])}")

    def _post(self, path, data, what):
        payload = dict(data)
        payload["access_token"] = self.token        # トークンはURLではなく本文で送る
        try:
            r = self.s.post(f"{self.base}/{path}", data=payload, timeout=config.HTTP_TIMEOUT_SEC)
        except requests.RequestException as e:
            raise PostError(f"{what} で通信エラー ({type(e).__name__})")
        return self._check(r, what)

    def _get(self, path, params, what):
        q = dict(params)
        q["access_token"] = self.token
        try:
            r = self.s.get(f"{self.base}/{path}", params=q, timeout=config.HTTP_TIMEOUT_SEC)
        except requests.RequestException as e:
            # 例外メッセージにはURL（トークン入り）が含まれることがあるので、種類名だけ出す
            raise PostError(f"{what} で通信エラー ({type(e).__name__})")
        return self._check(r, what)

    def create_container(self, params):
        j = self._post(f"{self.user_id}/media", params, "コンテナ作成(/media)")
        if "id" not in j:
            raise PostError(f"コンテナIDが返りませんでした: {j}")
        return j["id"]

    def wait_finished(self, creation_id, interval, timeout):
        waited = 0
        while True:
            j = self._get(creation_id, {"fields": "status_code,status"}, "処理状況の確認")
            code = j.get("status_code")
            if code == "FINISHED":
                return
            if code in ("ERROR", "EXPIRED"):
                raise PostError(f"Instagram側の処理が {code} になりました: {j.get('status', '')}")
            if waited >= timeout:
                raise PostError(f"{timeout}秒待っても処理が終わりませんでした (status_code={code})")
            self.sleep(interval)
            waited += interval

    def publish(self, creation_id):
        j = self._post(f"{self.user_id}/media_publish", {"creation_id": creation_id}, "公開(/media_publish)")
        if "id" not in j:
            raise PostError(f"投稿IDが返りませんでした: {j}")
        return j["id"]

    def post(self, kind, params):
        cid = self.create_container(params)
        if kind == "reel":
            self.wait_finished(cid, config.VIDEO_POLL_INTERVAL_SEC, config.VIDEO_POLL_TIMEOUT_SEC)
        else:
            self.wait_finished(cid, config.IMAGE_POLL_INTERVAL_SEC, config.IMAGE_POLL_TIMEOUT_SEC)
        return self.publish(cid)


# ───────────────────────── 本体 ─────────────────────────
def truthy(v):
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def parse_args(argv, env):
    ap = argparse.ArgumentParser(description="馬町珈琲 Instagram 自動投稿")
    ap.add_argument("--dry-run", action="store_true", help="投稿しないで内容だけ表示")
    ap.add_argument("--force", action="store_true", help="今日すでに投稿済みでも投稿する")
    ap.add_argument("--only", default=None, help="feed / story / reel / all")
    a = ap.parse_args(argv)
    a.dry_run = a.dry_run or truthy(env.get("DRY_RUN", ""))
    a.force = a.force or truthy(env.get("FORCE", ""))
    only = (a.only or env.get("ONLY") or "all").strip().lower()
    a.types = list(TYPES) if only in ("", "all") else [t.strip() for t in only.split(",") if t.strip()]
    bad = [t for t in a.types if t not in TYPES]
    if bad:
        ap.error(f"--only の値が不正です: {bad}")
    return a


def run(argv=None, env=None, session=None, sleep=time.sleep, clock=now_jst,
        state_path=STATE_PATH, log_path=LOG_PATH):
    env = os.environ if env is None else env
    args = parse_args(argv or [], env)

    # 定時実行のスイッチ（リポジトリ変数 IG_AUTOPOST_ENABLED）
    if env.get("GITHUB_EVENT_NAME") == "schedule" and env.get("IG_AUTOPOST_ENABLED", "").strip().lower() != "true":
        print("定時実行は停止中です（リポジトリ変数 IG_AUTOPOST_ENABLED が 'true' ではありません）。何もしません。")
        return 0

    token = env.get("IG_ACCESS_TOKEN", "").strip()
    user_id = env.get("IG_USER_ID", "").strip()
    log = Logger(log_path, secrets=[token, user_id], write_file=not args.dry_run, clock=clock)
    session = session or requests.Session()

    if not args.dry_run and (not token or not user_id):
        log("ERROR", "IG_ACCESS_TOKEN または IG_USER_ID が設定されていません（GitHub の Settings → Secrets を確認）")
        return 1

    now = clock()
    today = now.date()
    today_s = today.isoformat()
    state = load_state(state_path)
    client = None if args.dry_run else InstagramClient(token, user_id, session=session, sleep=sleep)
    failures = 0
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}実行日時: {now.strftime('%Y-%m-%d %H:%M')} JST / 対象: {', '.join(args.types)}"
          f"{' / force' if args.force else ''}")

    for kind in TYPES:
        label = TYPE_LABEL[kind]
        if kind not in args.types:
            continue
        due, why = is_due(kind, today)
        if not due:
            print(f"{prefix}{label}: スキップ ― {why}")
            continue
        if state[kind].get("last_posted_date") == today_s and not args.force:
            print(f"{prefix}{label}: スキップ ― 今日（{today_s}）はすでに投稿済み（二重投稿防止）")
            continue
        idx = pick_next(kind, state, today)
        if idx is None:
            print(f"{prefix}{label}: スキップ ― 投稿できる項目がありません（content.py が空、または動画未登録）")
            continue
        entry = entries_for(kind)[idx]
        url = media_url(kind, entry)
        params = build_params(kind, entry, url)

        if args.dry_run:
            print(f"{prefix}{label}: 投稿予定 #{idx} {entry['id']}")
            print(f"    URL: {url}")
            try:
                check_public_url(url, session)
                print("    公開URLの確認: OK")
            except PostError as e:
                print(f"    公開URLの確認: NG ― {e}")
                failures += 1
            if params.get("caption"):
                print("    キャプション:\n" + "\n".join("      " + line for line in params["caption"].splitlines()))
            continue

        try:
            check_public_url(url, session)
            media_id = client.post(kind, params)
        except Exception as e:  # noqa: BLE001  1種類の失敗で他を止めない
            failures += 1
            log("FAIL", f"{kind} #{idx} {entry['id']} {url} ― {e}")
            continue
        state[kind].update({"last_index": idx, "last_posted_date": today_s,
                            "last_media_id": media_id, "last_id": entry["id"]})
        save_state(state, state_path)        # 成功した種類だけ、すぐ記録
        log("OK", f"{kind} #{idx} {entry['id']} media_id={media_id}")

    if failures:
        print(f"{prefix}失敗: {failures} 件。" + ("上の表示を確認してください。" if args.dry_run else "post_log.txt / Actions のログを確認してください。"))
        return 1
    print(f"{prefix}完了")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
