/* =========================================================
   UMAMACHI COFFEE 馬町珈琲 — main.js
   言語切替 / メニュー描画 / スクロール演出
   本文・価格などの原稿は assets/content.js が唯一の出典。
   ここでは content.js に無い「事実」を足さないこと。
   ========================================================= */
(function () {
  'use strict';

  var S = window.SITE;
  if (!S) return;

  var LANGS = S.langs.map(function (l) { return l.code; });
  var FALLBACK = 'ja';

  /* 画像の代替テキスト（写真に写っているものだけを記述） */
  var ALT = {
    logo: {
      ja: '馬町珈琲 UMAMACHI COFFEE', en: 'UMAMACHI COFFEE', zh: '马町珈琲 UMAMACHI COFFEE',
      ko: '우마마치 커피 UMAMACHI COFFEE', es: 'UMAMACHI COFFEE'
    },
    hero: {
      ja: '赤いファサードと「UMAMACHI COFFEE」の看板がある店舗外観',
      en: 'The shopfront, with its red facade and UMAMACHI COFFEE sign',
      zh: '红色外墙与「UMAMACHI COFFEE」招牌的店铺外观',
      ko: '붉은 외벽과 UMAMACHI COFFEE 간판이 있는 매장 외관',
      es: 'La fachada roja del local con el rótulo UMAMACHI COFFEE'
    },
    exterior: {
      ja: '通りから見た店舗の外観', en: 'The shopfront seen from the street',
      zh: '从街道看到的店铺外观', ko: '거리에서 바라본 매장 외관',
      es: 'El local visto desde la calle'
    },
    band: {
      ja: '白い壁にイラストのポスターを飾ったテーブル席',
      en: 'Tables and black chairs below an illustrated poster on the white wall',
      zh: '白墙上挂着插画海报的桌位区',
      ko: '흰 벽에 일러스트 포스터가 걸린 테이블석',
      es: 'Mesas y sillas negras bajo un cartel ilustrado en la pared blanca'
    },
    interiorDeep: {
      ja: '店内奥のカウンターとショーケース', en: 'The counter and display case at the back of the room',
      zh: '店内深处的吧台与展示柜', ko: '매장 안쪽의 카운터와 쇼케이스',
      es: 'La barra y la vitrina al fondo del local'
    },
    interiorSeats: {
      ja: '色とりどりの椅子が並ぶ客席', en: 'Seating with brightly coloured chairs',
      zh: '摆放着彩色椅子的座位区', ko: '알록달록한 의자가 놓인 좌석',
      es: 'La sala con sillas de colores'
    },
    roaster: {
      ja: '焙煎機とコーヒー豆を写したポスター', en: 'A poster showing the roaster and the coffee beans',
      zh: '印有烘豆机与咖啡豆的海报', ko: '로스터와 커피 원두가 담긴 포스터',
      es: 'Un cartel con la tostadora y los granos de café'
    },
    sandwichOmelette: {
      ja: '木の丸皿にのせた厚焼き玉子とハムのサンドイッチと、彩り野菜のピクルス',
      en: 'A thick omelette and ham sandwich on a round wooden plate, with pickled vegetables',
      zh: '木质圆盘上的厚蛋烧火腿三明治，配彩色蔬菜腌菜',
      ko: '나무 원형 접시에 담긴 두툼한 계란과 햄 샌드위치, 그리고 채소 피클',
      es: 'Un sándwich de tortilla gruesa y jamón en un plato redondo de madera, con encurtidos de verduras'
    },
    sandwichTeriyaki: {
      ja: '木の丸皿にのせた、照り焼きチキンとレタス・トマトを厚切りトーストで挟んだサンドイッチ２切れと、彩り野菜のピクルス',
      en: 'Two halves of a teriyaki chicken sandwich with lettuce and tomato on thick toast, on a round wooden plate, with pickled vegetables behind',
      zh: '木质圆盘上的照烧鸡肉三明治两块，夹有生菜与番茄，后方是彩色蔬菜腌菜',
      ko: '나무 원형 접시에 담긴, 데리야키 치킨과 양상추·토마토를 두툼한 토스트로 만든 샌드위치 두 조각과 채소 피클',
      es: 'Dos mitades de un sándwich de pollo teriyaki con lechuga y tomate en pan tostado grueso, en un plato redondo de madera, con encurtidos al fondo'
    },
    sandwichHamegg: {
      ja: '白い角皿にのせた、ハムと厚焼き玉子・レタスをトーストで挟んだサンドイッチ２切れと、彩り野菜のピクルスと黄色い小旗',
      en: 'Two halves of a ham, thick omelette and lettuce sandwich on toast, on a white square plate, with pickled vegetables and a small yellow flag behind',
      zh: '白色方盘上的火腿厚蛋烧生菜三明治两块，后方是彩色蔬菜腌菜与黄色小旗',
      ko: '흰 사각 접시에 담긴, 햄과 두툼한 계란말이·양상추를 토스트로 만든 샌드위치 두 조각과 채소 피클, 노란 작은 깃발',
      es: 'Dos mitades de un sándwich de jamón, tortilla gruesa y lechuga en pan tostado, en un plato blanco cuadrado, con encurtidos y una banderita amarilla al fondo'
    },
    sweets: {
      ja: 'ショーケースに並ぶスイーツ', en: 'Sweets lined up in the display case',
      zh: '展示柜中排列的甜点', ko: '쇼케이스에 진열된 디저트',
      es: 'Los dulces en la vitrina'
    },
    iced: {
      ja: 'ロゴのステッカーを貼ったアイスコーヒー', en: 'An iced coffee in a cup with the shop’s logo sticker',
      zh: '贴有品牌贴纸的冰咖啡', ko: '로고 스티커가 붙은 아이스 커피',
      es: 'Un café frío en un vaso con la pegatina del logotipo'
    },
    coffeeLatte: {
      ja: '木のカウンターに置いた、ハート型のラテアートを描いた白いカップのカフェラテ',
      en: 'A caffe latte with heart latte art, in a white cup on the wooden counter',
      zh: '放在木质吧台上的白色杯子拿铁，拉花为心形',
      ko: '나무 카운터에 놓인, 하트 라떼아트가 그려진 흰 잔의 카페 라떼',
      es: 'Un café con leche con arte laté en forma de corazón, en taza blanca sobre la barra de madera'
    },
    teaLatte: {
      ja: 'グラスに注いだティーラテ', en: 'A tea latte in a glass',
      zh: '玻璃杯中的奶茶拿铁', ko: '유리잔에 담긴 티 라테',
      es: 'Un té con leche en vaso'
    },
    posterWall: {
      ja: '店内の壁に飾られた馬のポスター', en: 'The horse poster on the wall of the shop',
      zh: '店内墙上的马匹海报', ko: '매장 벽에 걸린 말 포스터',
      es: 'El cartel del caballo en la pared del local'
    }
  };

  /* 料理写真のうち、皿や付け合わせまで写っているものは説明文の alt を使う。
     指定のないものは品名をそのまま alt にする（従来どおり）。 */
  var FOOD_ALT = {
    'sandwich-omelette.jpg': 'sandwichOmelette',
    'sandwich-teriyaki.jpg': 'sandwichTeriyaki',
    'sandwich-hamegg.jpg': 'sandwichHamegg'
  };

  /* ---------- 言語の決定 ---------- */
  function pickLang() {
    var q = new URLSearchParams(window.location.search).get('lang');
    if (q && LANGS.indexOf(q) !== -1) return q;

    var saved = null;
    try { saved = window.localStorage.getItem('lang'); } catch (e) {}
    if (saved && LANGS.indexOf(saved) !== -1) return saved;

    var prefs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < prefs.length; i++) {
      var p = String(prefs[i]).toLowerCase();
      if (p.indexOf('ja') === 0) return 'ja';
      if (p.indexOf('ko') === 0) return 'ko';
      if (p.indexOf('es') === 0) return 'es';
      if (p.indexOf('zh') === 0) return 'zh';
      if (p.indexOf('en') === 0) return 'en';
    }
    return FALLBACK;
  }

  var lang = pickLang();
  function T(key) {
    var d = S.t[lang] || S.t[FALLBACK];
    return (d && d[key] != null) ? d[key] : (S.t[FALLBACK][key] || '');
  }
  function alt(key) {
    var a = ALT[key];
    return a ? (a[lang] || a[FALLBACK]) : '';
  }
  function yen(v) { return '¥' + v; }

  /* ---------- 小さな DOM ヘルパ ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function img(file, w, h, altKey, altText) {
    var n = document.createElement('img');
    n.src = 'assets/img/' + file;
    n.width = w; n.height = h;
    n.loading = 'lazy'; n.decoding = 'async';
    n.alt = altText != null ? altText : alt(altKey);
    return n;
  }

  /* ---------- フード ---------- */
  function renderFood() {
    var feature = document.getElementById('foodFeature');
    var list = document.getElementById('foodList');
    var list2 = document.getElementById('foodList2');
    feature.textContent = '';
    list.textContent = '';
    if (list2) list2.textContent = '';

    /* 写真ありの品は2段組のカード。枚数が奇数だと最後の1枚が段に取り残されるので、
       先頭（＝いちばん高い品）を写真と本文の横並びにして全幅で置き、
       残りをちょうど2枚ずつの段にする。列の切れ目は下のリストと同じ位置。 */
    var shot = S.food.filter(function (it) { return it.img; }).length;
    var lead = (shot % 2 === 1);
    var shotSeen = 0;

    /* 写真なしの品は2段組に振り分ける（左段が多くなるように前詰め） */
    var plain = S.food.filter(function (it) { return !it.img; }).length;
    var leftCount = Math.ceil(plain / 2);
    var plainSeen = 0;

    S.food.forEach(function (item) {
      var name = item.name[lang] || item.name[FALLBACK];
      var desc = item.desc ? (item.desc[lang] || item.desc[FALLBACK]) : '';
      var tag = item.tag ? (item.tag[lang] || item.tag[FALLBACK]) : '';
      var side = item.side ? T('food.' + item.side) : '';

      if (item.img) {
        var card = el('article', 'food-card' + (lead && shotSeen === 0 ? ' food-card-lead' : ''));
        var fig = el('figure', 'ph ph-43');
        var altKey = FOOD_ALT[item.img];
        fig.appendChild(img(item.img, 1200, 900, null, altKey ? alt(altKey) : name));
        card.appendChild(fig);

        var body = el('div', 'food-body');
        var head = el('div', 'food-head');
        head.appendChild(el('h3', 'food-name', name));
        head.appendChild(el('span', 'm-price', yen(item.price)));
        body.appendChild(head);

        if (tag) body.appendChild(el('p', 'food-tag', tag));
        if (desc) body.appendChild(el('p', 'food-desc', desc));
        if (side) body.appendChild(el('p', 'food-side', side));
        card.appendChild(body);
        feature.appendChild(card);
        shotSeen++;
      } else {
        var row = el('li', 'mrow');
        var nm = el('div', 'm-name');
        nm.appendChild(el('span', 'm-en', name));
        if (tag) nm.appendChild(el('span', 'm-sub', tag));
        row.appendChild(nm);

        var meta = el('div', 'm-meta');
        meta.appendChild(el('span', 'm-price', yen(item.price)));
        row.appendChild(meta);

        if (desc) row.appendChild(el('p', 'm-desc', desc));
        if (side) row.appendChild(el('p', 'm-side', side));
        (list2 && plainSeen >= leftCount ? list2 : list).appendChild(row);
        plainSeen++;
      }
    });
  }

  /* ---------- ドリンク ---------- */
  function drinkRow(item) {
    var row = el('li', 'mrow');
    var nm = el('div', 'm-name');
    nm.appendChild(el('span', 'm-en', item.en));
    var sub = item.sub ? item.sub[lang] : null;
    if (sub) nm.appendChild(el('span', 'm-sub', sub));
    row.appendChild(nm);

    var meta = el('div', 'm-meta');
    if (item.temp) meta.appendChild(el('span', 'm-temp', T('drink.' + item.temp)));
    meta.appendChild(el('span', 'm-price', yen(item.price)));
    row.appendChild(meta);

    var desc = item.desc ? (item.desc[lang] || item.desc[FALLBACK]) : '';
    if (desc) row.appendChild(el('p', 'm-desc', desc));
    return row;
  }

  function renderDrinks() {
    var cList = document.getElementById('coffeeList');
    cList.textContent = '';
    S.coffee.forEach(function (item) { cList.appendChild(drinkRow(item)); });

    var bList = document.getElementById('bevList');
    bList.textContent = '';
    var current = null;
    S.beverage.forEach(function (item, i) {
      if (item.group !== current) {
        /* 直前のグループが日本茶なら、その下に注記を置く */
        if (current === 'jp') bList.appendChild(el('li', 'mnote', T('drink.jp_note')));
        current = item.group;
        if (current) {
          var g = el('li', 'mgroup');
          g.appendChild(el('span', 'mgroup-name', T(current === 'jp' ? 'drink.jp_group' : 'drink.herbal_group')));
          if (current === 'herbal') g.appendChild(el('span', 'mgroup-tag', T('drink.caffeine_free')));
          bList.appendChild(g);
        }
      }
      bList.appendChild(drinkRow(item));
      if (i === S.beverage.length - 1 && current === 'jp') {
        bList.appendChild(el('li', 'mnote', T('drink.jp_note')));
      }
    });
  }

  /* ---------- Instagram ---------- */
  function renderInstagram() {
    var handle = S.shop.instagram;
    var cta = document.getElementById('igCta');
    if (!cta) return;
    var set = handle && handle !== 'INSTAGRAM_HANDLE';
    if (set && cta.tagName !== 'A') {
      var a = document.createElement('a');
      a.className = 'btn btn-ghost';
      a.id = 'igCta';
      a.setAttribute('data-i18n', 'ig.cta');
      a.href = 'https://www.instagram.com/' + handle + '/';
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = cta.textContent;
      cta.parentNode.replaceChild(a, cta);
    }
  }

  /* ---------- 言語の適用 ---------- */
  function applyLang(next, save) {
    lang = next;
    document.documentElement.lang = lang;
    document.title = T('meta.title');

    var md = document.querySelector('meta[name="description"]');
    if (md) md.setAttribute('content', T('meta.desc'));

    Array.prototype.forEach.call(document.querySelectorAll('[data-i18n]'), function (n) {
      n.textContent = T(n.getAttribute('data-i18n'));
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-i18n-alt]'), function (n) {
      n.alt = alt(n.getAttribute('data-i18n-alt'));
    });

    renderFood();
    renderDrinks();
    renderInstagram();

    var cur = document.getElementById('langCur');
    var label = '';
    S.langs.forEach(function (l) { if (l.code === lang) label = l.label; });
    if (cur) cur.textContent = label;
    Array.prototype.forEach.call(document.querySelectorAll('#langMenu button'), function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-lang') === lang ? 'true' : 'false');
    });

    if (save) { try { window.localStorage.setItem('lang', lang); } catch (e) {} }
  }

  /* ---------- 言語切替 UI ---------- */
  function buildLangMenu() {
    var menu = document.getElementById('langMenu');
    var wrap = document.getElementById('lang');
    var btn = document.getElementById('langBtn');
    if (!menu || !wrap || !btn) return;

    S.langs.forEach(function (l) {
      var li = document.createElement('li');
      li.setAttribute('role', 'none');
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'menuitem');
      b.setAttribute('data-lang', l.code);
      b.setAttribute('lang', l.code);
      b.textContent = l.label;
      b.addEventListener('click', function () {
        applyLang(l.code, true);
        close();
        btn.focus();
      });
      li.appendChild(b);
      menu.appendChild(li);
    });

    function open() { wrap.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    function close() { wrap.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (wrap.classList.contains('is-open')) {
        close();
      } else {
        /* ハンバーガーが開いていれば閉じてから開く（重なり防止） */
        var nav = document.getElementById('nav');
        var burger = document.getElementById('burger');
        if (nav && nav.classList.contains('is-open')) {
          nav.classList.remove('is-open');
          if (burger) burger.setAttribute('aria-expanded', 'false');
        }
        open();
      }
    });
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  /* ---------- ハンバーガー ---------- */
  var navOpen = false;

  function buildNav() {
    var burger = document.getElementById('burger');
    var nav = document.getElementById('nav');
    if (!burger || !nav) return;
    burger.addEventListener('click', function () {
      navOpen = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', navOpen ? 'true' : 'false');
      refreshHeader();
    });
    Array.prototype.forEach.call(nav.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('is-open');
        navOpen = false;
        burger.setAttribute('aria-expanded', 'false');
        refreshHeader();
      });
    });
  }

  /* ---------- 地図リンク ---------- */
  function buildMapLink() {
    var a = document.getElementById('mapLink');
    if (a && S.shop.mapQuery) {
      a.href = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(S.shop.mapQuery);
    }
  }

  /* ---------- 動画 ---------- */
  function buildVideo() {
    var v = document.getElementById('reel');
    var btn = document.getElementById('videoPlay');
    if (!v || !btn) return;
    var frame = v.parentNode;
    btn.addEventListener('click', function () {
      frame.classList.add('is-playing');
      v.play();
    });
    v.addEventListener('play', function () { frame.classList.add('is-playing'); });
    v.addEventListener('ended', function () { frame.classList.remove('is-playing'); });
  }

  /* ---------- スクロール演出 ---------- */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function buildReveal() {
    var items = document.querySelectorAll('.reveal');
    if (reduce || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(items, function (n) { n.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    Array.prototype.forEach.call(items, function (n) { io.observe(n); });
  }

  function buildParallax() {
    var bands = document.querySelectorAll('.band');
    if (!bands.length || reduce) return;
    var ticking = false;

    function update() {
      ticking = false;
      var vh = window.innerHeight || document.documentElement.clientHeight;
      Array.prototype.forEach.call(bands, function (band) {
        var im = band.querySelector('img');
        if (!im) return;
        var r = band.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var p = (vh - r.top) / (vh + r.height);        /* 0 → 1 */
        var shift = (p - 0.5) * (r.height * 0.16);
        im.style.transform = 'translate3d(0,' + shift.toFixed(1) + 'px,0)';
      });
    }
    function onScroll() {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  /* ---------- ヘッダー：ヒーローの上では透明、抜けたらクリーム地 ---------- */
  function refreshHeader() {
    var hdr = document.querySelector('.hdr');
    if (!hdr) return;
    var hero = document.getElementById('hero');
    var over = false;
    if (hero && !navOpen) {
      over = hero.getBoundingClientRect().bottom > (hdr.offsetHeight || 64) + 2;
    }
    hdr.classList.toggle('is-over', over);
  }

  function buildHeaderState() {
    var ticking = false;
    function onScroll() {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(function () { ticking = false; refreshHeader(); });
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    window.addEventListener('load', refreshHeader);
    refreshHeader();
  }

  /* ---------- 起動 ---------- */
  document.documentElement.classList.add('js');

  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());

  buildLangMenu();
  buildNav();
  buildMapLink();
  buildVideo();
  applyLang(lang, false);
  buildHeaderState();
  buildReveal();
  buildParallax();
})();
