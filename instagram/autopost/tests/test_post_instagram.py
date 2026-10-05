# -*- coding: utf-8 -*-
"""post_instagram.py のテスト。Instagram の本物のAPIには一切アクセスしません（すべて偽物の応答）。"""
import datetime as dt
import json

import pytest
import requests

import config
import content
import post_instagram as pi

TOKEN = "TEST_TOKEN_abc123_SECRET"
USER = "17841400000000000"
ENV_OK = {"IG_ACCESS_TOKEN": TOKEN, "IG_USER_ID": USER, "GITHUB_EVENT_NAME": "workflow_dispatch"}
BASE = f"https://graph.instagram.com/{config.API_VERSION}"


class Resp:
    def __init__(self, status=200, payload=None, text=None, headers=None):
        self.status_code = status
        self._payload = payload
        self.text = text if text is not None else json.dumps(payload or {})
        self.headers = headers or {}

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


class FakeSession:
    """requests.Session の代わり。呼ばれた内容を記録し、決められた応答を返す。"""

    def __init__(self, head_status=200, fail_create_for=(), status_seq=None, publish_fail=False,
                 echo_token_in_error=False):
        self.calls = []
        self.head_status = head_status
        self.fail_create_for = set(fail_create_for)   # "image" / "STORIES" / "REELS"
        self.status_seq = list(status_seq or [])
        self.publish_fail = publish_fail
        self.echo = echo_token_in_error
        self.n = 0

    def head(self, url, **kw):
        self.calls.append(("HEAD", url, None))
        ctype = "image/jpeg" if url.endswith(".jpg") else "video/mp4"
        return Resp(self.head_status, {}, headers={"Content-Type": ctype})

    def post(self, url, data=None, **kw):
        self.calls.append(("POST", url, dict(data or {})))
        if url.endswith("/media"):
            mtype = data.get("media_type", "image")
            if mtype in self.fail_create_for:
                body = '{"error":{"message":"Invalid parameter","code":100}}'
                if self.echo:
                    body = body[:-1] + f',"access_token":"{data["access_token"]}"}}'
                return Resp(400, None, text=body)
            self.n += 1
            return Resp(200, {"id": f"C{self.n}"})
        if url.endswith("/media_publish"):
            if self.publish_fail:
                return Resp(500, None, text='{"error":{"message":"oops"}}')
            return Resp(200, {"id": "M_" + data["creation_id"]})
        raise AssertionError(url)

    def get(self, url, params=None, **kw):
        self.calls.append(("GET", url, dict(params or {})))
        code = self.status_seq.pop(0) if self.status_seq else "FINISHED"
        return Resp(200, {"status_code": code, "id": url.rsplit("/", 1)[-1]})

    def graph_calls(self):
        return [c for c in self.calls if c[1].startswith("https://graph.instagram.com")]


def clock_at(y, m, d, hh=9, mm=5):
    return lambda: dt.datetime(y, m, d, hh, mm, tzinfo=pi.JST)


@pytest.fixture
def paths(tmp_path):
    sp = tmp_path / "state.json"
    lp = tmp_path / "post_log.txt"
    pi.save_state(pi.default_state(), str(sp))
    lp.write_text("# log\n", encoding="utf-8")
    return str(sp), str(lp)


def run(paths, argv=None, env=None, session=None, clock=None, sleeps=None):
    sp, lp = paths
    sl = sleeps if sleeps is not None else []
    return pi.run(argv or [], env=env if env is not None else dict(ENV_OK), session=session or FakeSession(),
                  sleep=sl.append, clock=clock or clock_at(2026, 10, 13), state_path=sp, log_path=lp)


@pytest.fixture
def no_reels(monkeypatch):
    monkeypatch.setattr(content, "REELS", [dict(id="r", video=None, caption="x")])


# ───────── スイッチ（定時実行のゲート） ─────────
def test_schedule_does_nothing_when_variable_not_true(paths, capsys):
    s = FakeSession()
    env = dict(ENV_OK, GITHUB_EVENT_NAME="schedule")       # IG_AUTOPOST_ENABLED なし
    assert run(paths, env=env, session=s) == 0
    assert s.calls == []
    assert json.load(open(paths[0])) == pi.default_state()
    for v in ("false", "TRUE ", "1", ""):
        env["IG_AUTOPOST_ENABLED"] = v
        if v.strip().lower() == "true":
            continue
        assert run(paths, env=env, session=s) == 0
    assert s.calls == []


def test_schedule_runs_when_enabled(paths, no_reels):
    s = FakeSession()
    env = dict(ENV_OK, GITHUB_EVENT_NAME="schedule", IG_AUTOPOST_ENABLED="true")
    assert run(paths, env=env, session=s) == 0
    assert len([c for c in s.calls if c[1].endswith("/media_publish")]) == 2


def test_missing_secrets_fails_clearly(paths, capsys):
    s = FakeSession()
    assert run(paths, env={"GITHUB_EVENT_NAME": "workflow_dispatch"}, session=s) == 1
    assert "IG_ACCESS_TOKEN" in capsys.readouterr().out
    assert s.graph_calls() == []


# ───────── ドライラン ─────────
def test_dry_run_makes_no_api_calls_and_changes_nothing(paths, capsys, no_reels):
    s = FakeSession()
    before_log = open(paths[1], encoding="utf-8").read()
    assert run(paths, argv=["--dry-run"], env={"GITHUB_EVENT_NAME": "workflow_dispatch"}, session=s) == 0
    out = capsys.readouterr().out
    assert s.graph_calls() == []
    assert "f01-blend" in out and "s01-hours" in out
    assert "https://umamachicoffee.jp/instagram/generated/feed/f01-blend.jpg" in out
    assert json.load(open(paths[0])) == pi.default_state()
    assert open(paths[1], encoding="utf-8").read() == before_log


def test_dry_run_via_env_and_reports_missing_public_image(paths, capsys, no_reels):
    s = FakeSession(head_status=404)
    rc = run(paths, env={"DRY_RUN": "true", "GITHUB_EVENT_NAME": "workflow_dispatch"}, session=s)
    assert rc == 1
    assert "NG" in capsys.readouterr().out
    assert s.graph_calls() == []


# ───────── 通常の投稿 ─────────
def test_feed_and_story_success(paths, capsys, no_reels):
    s = FakeSession()
    assert run(paths, session=s) == 0
    g = s.graph_calls()
    creates = [c for c in g if c[1].endswith("/media")]
    assert [c[1] for c in creates] == [f"{BASE}/{USER}/media"] * 2
    feed, story = creates[0][2], creates[1][2]
    assert feed["image_url"] == config.GENERATED_BASE_URL + "feed/f01-blend.jpg"
    assert feed["caption"] == content.FEED[0]["caption"]
    assert "media_type" not in feed
    assert story["media_type"] == "STORIES" and "caption" not in story
    assert story["image_url"].endswith("/story/s01-hours.jpg")
    # トークンはURLに入れない
    assert all(TOKEN not in c[1] for c in s.calls)
    st = json.load(open(paths[0]))
    assert st["feed"]["last_index"] == 0 and st["feed"]["last_posted_date"] == "2026-10-13"
    assert st["story"]["last_index"] == 0 and st["story"]["last_media_id"] == "M_C2"
    assert st["reel"]["last_index"] == -1
    log = open(paths[1], encoding="utf-8").read()
    assert log.count("[OK]") == 2
    out = capsys.readouterr().out
    assert TOKEN not in log and TOKEN not in out and USER not in log


def test_rotation_continues_next_day_and_wraps(paths, no_reels):
    s = FakeSession()
    st = pi.default_state()
    st["feed"]["last_index"] = len(content.FEED) - 1        # 最後まで来た → 先頭へ
    st["story"]["last_index"] = 2
    pi.save_state(st, paths[0])
    assert run(paths, session=s, clock=clock_at(2026, 10, 14)) == 0
    st = json.load(open(paths[0]))
    assert st["feed"]["last_index"] == 0
    assert st["story"]["last_index"] == 3


def test_skip_if_already_posted_today_unless_force(paths, capsys, no_reels):
    st = pi.default_state()
    for t in ("feed", "story"):
        st[t]["last_posted_date"] = "2026-10-13"
        st[t]["last_index"] = 0
    pi.save_state(st, paths[0])
    s = FakeSession()
    assert run(paths, session=s) == 0
    assert s.graph_calls() == []
    assert "すでに投稿済み" in capsys.readouterr().out
    assert run(paths, argv=["--force"], session=s) == 0
    assert len([c for c in s.calls if c[1].endswith("/media_publish")]) == 2
    assert json.load(open(paths[0]))["feed"]["last_index"] == 1


def test_only_option_posts_single_type(paths, no_reels):
    s = FakeSession()
    assert run(paths, argv=["--only", "feed"], session=s) == 0
    creates = [c for c in s.calls if c[1].endswith("/media")]
    assert len(creates) == 1 and "image_url" in creates[0][2] and "media_type" not in creates[0][2]
    st = json.load(open(paths[0]))
    assert st["story"]["last_posted_date"] is None
    env = dict(ENV_OK, ONLY="story")
    s2 = FakeSession()
    assert run(paths, env=env, session=s2) == 0
    assert [c[2]["media_type"] for c in s2.calls if c[1].endswith("/media")] == ["STORIES"]


# ───────── 失敗時 ─────────
def test_one_type_failing_does_not_block_others(paths, no_reels):
    s = FakeSession(fail_create_for={"image"}, echo_token_in_error=True)
    assert run(paths, session=s) == 1
    st = json.load(open(paths[0]))
    assert st["feed"]["last_index"] == -1 and st["feed"]["last_posted_date"] is None   # 失敗 → 更新しない
    assert st["story"]["last_index"] == 0                                            # 成功 → 更新
    log = open(paths[1], encoding="utf-8").read()
    assert "[FAIL] feed" in log and "HTTP 400" in log and "Invalid parameter" in log
    assert TOKEN not in log and "***" in log


def test_status_error_and_timeout(paths, no_reels):
    s = FakeSession(status_seq=["ERROR"])
    assert run(paths, argv=["--only", "feed"], session=s) == 1
    assert "ERROR" in open(paths[1], encoding="utf-8").read()
    sleeps = []
    s = FakeSession(status_seq=["IN_PROGRESS"] * 100)
    assert run(paths, argv=["--only", "feed"], session=s, sleeps=sleeps) == 1
    assert sum(sleeps) == config.IMAGE_POLL_TIMEOUT_SEC
    assert json.load(open(paths[0]))["feed"]["last_index"] == -1


def test_publish_failure_does_not_update_state(paths, no_reels):
    s = FakeSession(publish_fail=True)
    assert run(paths, argv=["--only", "feed"], session=s) == 1
    assert json.load(open(paths[0]))["feed"]["last_posted_date"] is None


def test_unreachable_public_url_skips_api(paths, no_reels):
    s = FakeSession(head_status=404)
    assert run(paths, argv=["--only", "feed"], session=s) == 1
    assert s.graph_calls() == []
    assert "HTTP 404" in open(paths[1], encoding="utf-8").read()


def test_network_exception_message_does_not_leak_token(paths, no_reels):
    class Boom(FakeSession):
        def get(self, url, params=None, **kw):
            raise requests.ConnectionError(f"failed {url}?access_token={params['access_token']}")
    s = Boom()
    assert run(paths, argv=["--only", "feed"], session=s) == 1
    log = open(paths[1], encoding="utf-8").read()
    assert "ConnectionError" in log and TOKEN not in log


# ───────── リール ─────────
def test_reel_skipped_cleanly_when_no_videos(paths, capsys):
    assert all(not r.get("video") for r in content.REELS)          # 現在は動画なし
    s = FakeSession()
    # 2026-10-16 は金曜日（CADENCE の reel 曜日）
    assert run(paths, argv=["--only", "reel"], session=s, clock=clock_at(2026, 10, 16)) == 0
    assert s.calls == []
    assert "投稿できる項目がありません" in capsys.readouterr().out


def test_reel_posts_on_listed_weekday_with_polling(paths, monkeypatch):
    monkeypatch.setattr(content, "REELS", [dict(id="r01", video="r01.mp4", caption="キャプション\n\nCaption\n\n#a")])
    sleeps = []
    s = FakeSession(status_seq=["IN_PROGRESS", "IN_PROGRESS", "FINISHED"])
    assert run(paths, argv=["--only", "reel"], session=s, clock=clock_at(2026, 10, 16), sleeps=sleeps) == 0
    create = [c for c in s.calls if c[1].endswith("/media")][0][2]
    assert create["media_type"] == "REELS"
    assert create["video_url"] == "https://umamachicoffee.jp/instagram/videos/r01.mp4"
    assert sleeps == [config.VIDEO_POLL_INTERVAL_SEC] * 2
    assert json.load(open(paths[0]))["reel"]["last_index"] == 0
    # 金曜以外は投稿しない
    s2 = FakeSession()
    assert run(paths, argv=["--only", "reel"], session=s2, clock=clock_at(2026, 10, 17)) == 0
    assert s2.calls == []


def test_reel_timeout_after_about_five_minutes(paths, monkeypatch):
    monkeypatch.setattr(content, "REELS", [dict(id="r01", video="https://example.com/v.mp4", caption="c")])
    sleeps = []
    s = FakeSession(status_seq=["IN_PROGRESS"] * 1000)
    assert run(paths, argv=["--only", "reel"], session=s, clock=clock_at(2026, 10, 16), sleeps=sleeps) == 1
    assert sum(sleeps) == config.VIDEO_POLL_TIMEOUT_SEC == 300


# ───────── 選び方・頻度 ─────────
def test_seasonal_entries_only_in_their_months():
    st = pi.default_state()
    seasonal = [i for i, e in enumerate(content.FEED) if e.get("months")]
    assert seasonal, "季節ものの項目がある前提"
    i = seasonal[0]
    st["feed"]["last_index"] = i - 1
    assert pi.pick_next("feed", st, dt.date(2026, 10, 20)) == i          # 秋は対象
    assert pi.pick_next("feed", st, dt.date(2027, 2, 20)) != i           # 冬は飛ばす


def test_disabled_entries_are_skipped_in_rotation(monkeypatch):
    feed = [dict(e) for e in content.FEED]
    feed[1]["enabled"] = False
    feed[4]["enabled"] = False
    monkeypatch.setattr(content, "FEED", feed)
    st = pi.default_state()
    disabled = [i for i, e in enumerate(content.FEED) if e.get("enabled", True) is False]
    assert disabled == [1, 4]
    for i in disabled:
        st["feed"]["last_index"] = i - 1
        assert pi.pick_next("feed", st, dt.date(2026, 10, 20)) != i
    # 一巡しても無効な項目は一度も選ばれない
    st = pi.default_state()
    seen = set()
    for _ in range(len(content.FEED) * 2):
        i = pi.pick_next("feed", st, dt.date(2026, 10, 20))
        seen.add(i)
        st["feed"]["last_index"] = i
    assert not (seen & set(disabled))


def test_all_disabled_means_skip(paths, monkeypatch):
    monkeypatch.setattr(content, "FEED", [dict(content.FEED[0], enabled=False)])
    monkeypatch.setattr(content, "STORIES", [])
    s = FakeSession()
    assert run(paths, session=s) == 0
    assert s.calls == []


def test_empty_lists_skip(paths, monkeypatch, capsys):
    monkeypatch.setattr(content, "FEED", [])
    monkeypatch.setattr(content, "STORIES", [])
    s = FakeSession()
    assert run(paths, session=s) == 0
    assert s.calls == []


def test_cadence_weekdays():
    c = {"feed": {"enabled": True, "days": ["mon", "thu"]}, "story": {"enabled": False, "days": "daily"}}
    assert pi.is_due("feed", dt.date(2026, 10, 12), c)[0]        # 月
    assert not pi.is_due("feed", dt.date(2026, 10, 13), c)[0]    # 火
    assert not pi.is_due("story", dt.date(2026, 10, 13), c)[0]
    assert not pi.is_due("reel", dt.date(2026, 10, 13), c)[0]    # 設定なし → 投稿しない


def test_default_cadence_matches_decision():
    assert config.CADENCE["feed"] == {"enabled": True, "days": "daily"}
    assert config.CADENCE["story"] == {"enabled": True, "days": "daily"}
    assert config.GRAPH_HOST == "https://graph.instagram.com"
    assert config.API_VERSION == "v21.0"


def test_jst_date_used_not_utc(paths, no_reels):
    # UTC 2026-10-12 23:30 = JST 2026-10-13 08:30 → 日付は 10-13 として扱う
    utc = dt.datetime(2026, 10, 12, 23, 30, tzinfo=dt.timezone.utc)
    s = FakeSession()
    assert run(paths, session=s, clock=lambda: utc.astimezone(pi.JST)) == 0
    assert json.load(open(paths[0]))["feed"]["last_posted_date"] == "2026-10-13"
