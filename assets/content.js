/* 馬町珈琲 UMAMACHI COFFEE — サイト原稿データ（5言語）
   出典: 「馬町珈琲のコメント.docx」/ A3_drink.pdf / A3_food.pdf / 店内撮影写真
   GIESEN の国名は「オランダ」で確定（2026-09-07 ユーザー確認済み）。
   ランチメニューは今回不掲載（旧店名 Gojo Coffee Factory 表記の素材のみのため）。 */

window.SITE = {
  langs: [
    { code: 'ja', label: '日本語' },
    { code: 'en', label: 'English' },
    { code: 'zh', label: '中文' },
    { code: 'ko', label: '한국어' },
    { code: 'es', label: 'Español' }
  ],

  /* ---------- 共通データ（言語で変わらないもの） ---------- */
  shop: {
    tel: '075-741-8779',
    telLink: '+81757418779',
    mapQuery: '京都市東山区常盤町459-13 馬町珈琲',
    instagram: 'umamachi.coffee'   // https://www.instagram.com/umamachi.coffee/
  },

  /* ---------- メニュー（価格・構成は A3 メニュー2枚が出典） ---------- */
  food: [
    { img: 'burger-umamachi.jpg', price: '1,300', side: 'fries',
      name: { ja: '馬町バーガー', en: 'Umamachi Burger', zh: '马町汉堡', ko: '우마마치 버거', es: 'Hamburguesa Umamachi' },
      tag:  { ja: '和牛ブレンドパティ', en: 'Wagyu blend patty', zh: '和牛混合肉排', ko: '와규 블렌드 패티', es: 'Carne con mezcla de wagyu' },
      desc: { ja: 'ダブルパティ、チェダーチーズ、オニオン、トマト、レタス、グレイビーソース。',
              en: 'Double patty, cheddar cheese, onion, tomato, lettuce and gravy.',
              zh: '双层肉排、切达奶酪、洋葱、番茄、生菜与肉汁酱。',
              ko: '더블 패티, 체더 치즈, 양파, 토마토, 양상추, 그레이비 소스.',
              es: 'Doble carne, queso cheddar, cebolla, tomate, lechuga y salsa gravy.' } },

    { img: 'burger-moon.jpg', price: '1,000', side: 'fries',
      name: { ja: '京都ムーンバーガー', en: 'Kyoto Moon Burger', zh: '京都月亮汉堡', ko: '교토 문 버거', es: 'Hamburguesa Kyoto Moon' },
      tag:  { ja: '和牛ブレンドパティ', en: 'Wagyu blend patty', zh: '和牛混合肉排', ko: '와규 블렌드 패티', es: 'Carne con mezcla de wagyu' },
      desc: { ja: 'パティ、目玉焼き、オニオン、トマト、レタス、グレイビーソース。',
              en: 'Patty, fried egg, onion, tomato, lettuce and gravy.',
              zh: '肉排、煎蛋、洋葱、番茄、生菜与肉汁酱。',
              ko: '패티, 프라이드 에그, 양파, 토마토, 양상추, 그레이비 소스.',
              es: 'Carne, huevo frito, cebolla, tomate, lechuga y salsa gravy.' } },

    { img: 'sandwich-teriyaki.jpg', price: '980', side: 'pickles',
      name: { ja: '照り焼きチキンのサンドイッチ', en: 'Teriyaki Chicken Sandwich', zh: '照烧鸡肉三明治', ko: '데리야키 치킨 샌드위치', es: 'Sándwich de pollo teriyaki' },
      tag: null,
      desc: { ja: '照り焼きチキン、エッグタルタルソース、レタス、トマト、レッドオニオン。',
              en: 'Teriyaki chicken, egg tartar sauce, lettuce, tomato and red onion.',
              zh: '照烧鸡肉、蛋塔塔酱、生菜、番茄与红洋葱。',
              ko: '데리야키 치킨, 에그 타르타르 소스, 양상추, 토마토, 적양파.',
              es: 'Pollo teriyaki, salsa tártara de huevo, lechuga, tomate y cebolla morada.' } },

    { img: 'sandwich-omelette.jpg', price: '880', side: 'pickles',
      name: { ja: 'オムレツサンドイッチ', en: 'Omelette Sandwich', zh: '厚蛋烧三明治', ko: '오믈렛 샌드위치', es: 'Sándwich de tortilla' },
      tag: null,
      desc: { ja: 'ふんわりオムレツ、エッグタルタルソース、マスタードマヨ。',
              en: 'Fluffy omelette, egg tartar sauce and mustard mayo.',
              zh: '松软厚蛋烧、蛋塔塔酱与芥末美乃滋。',
              ko: '부드러운 오믈렛, 에그 타르타르 소스, 머스터드 마요.',
              es: 'Tortilla esponjosa, salsa tártara de huevo y mayonesa a la mostaza.' } },

    { img: 'sandwich-hamegg.jpg', price: '780', side: 'pickles',
      name: { ja: 'ハムエッグサンドイッチ', en: 'Ham and Egg Sandwich', zh: '火腿鸡蛋三明治', ko: '햄에그 샌드위치', es: 'Sándwich de jamón y huevo' },
      tag: null,
      desc: { ja: 'ダブルハム、エッグタルタルソース、レタス、トマト、レッドオニオン。',
              en: 'Double ham, egg tartar sauce, lettuce, tomato and red onion.',
              zh: '双层火腿、蛋塔塔酱、生菜、番茄与红洋葱。',
              ko: '더블 햄, 에그 타르타르 소스, 양상추, 토마토, 적양파.',
              es: 'Doble jamón, salsa tártara de huevo, lechuga, tomate y cebolla morada.' } }
  ],

  /* ドリンクは「英語名（主）＋各言語の読み（副）」で、店頭メニューの見せ方に合わせる */
  coffee: [
    { en: 'Specialty Coffee A … ask', temp: 'hot', price: '650',
      sub: { ja: 'スペシャルティコーヒー A（本日の豆はスタッフまで）', zh: '精品咖啡 A（当日豆款请询问店员）', ko: '스페셜티 커피 A (오늘의 원두는 직원에게)', es: 'Café de especialidad A (pregunte por el grano del día)' } },
    { en: 'Specialty Coffee B … ask', temp: 'hot', price: '650',
      sub: { ja: 'スペシャルティコーヒー B（本日の豆はスタッフまで）', zh: '精品咖啡 B（当日豆款请询问店员）', ko: '스페셜티 커피 B (오늘의 원두는 직원에게)', es: 'Café de especialidad B (pregunte por el grano del día)' } },
    { en: 'Umamachi Blend — strong roasted', temp: 'hot', price: '580',
      sub: { ja: '馬町ブレンド（深煎り）', zh: '马町综合豆（深烘焙）', ko: '우마마치 블렌드 (강배전)', es: 'Mezcla Umamachi (tueste intenso)' } },
    { en: 'Decaf Coffee', temp: 'hot', price: '650',
      sub: { ja: 'カフェインレスコーヒー', zh: '低因咖啡', ko: '디카페인 커피', es: 'Café descafeinado' } },
    { en: 'Half Decaf & Half Umamachi Blend', temp: 'hot', price: '700',
      sub: { ja: 'カフェインレス × 馬町ブレンド ハーフ', zh: '低因＋马町综合豆 各半', ko: '디카페인 × 우마마치 블렌드 하프', es: 'Mitad descafeinado, mitad mezcla Umamachi' } },
    { en: 'Iced Coffee — original', temp: 'iced', price: '630',
      sub: { ja: 'アイスコーヒー（オリジナル）', zh: '冰咖啡（原创配方）', ko: '아이스 커피 (오리지널)', es: 'Café frío (original)' } },
    { en: 'Caffe Latte', temp: 'both', price: '630',
      sub: { ja: 'カフェラテ', zh: '拿铁', ko: '카페 라테', es: 'Café con leche' } },
    { en: 'Cappuccino', temp: 'both', price: '630',
      sub: { ja: 'カプチーノ', zh: '卡布奇诺', ko: '카푸치노', es: 'Capuchino' } },
    { en: 'Caramel Macchiato', temp: 'both', price: '650',
      sub: { ja: 'キャラメルマキアート', zh: '焦糖玛奇朵', ko: '카라멜 마키아토', es: 'Caramel macchiato' } },
    { en: 'Cafe Mocha', temp: 'both', price: '650',
      sub: { ja: 'カフェモカ', zh: '摩卡', ko: '카페 모카', es: 'Café mocha' } },
    { en: 'Espresso', temp: 'hot', price: '400',
      sub: { ja: 'エスプレッソ', zh: '浓缩咖啡', ko: '에스프레소', es: 'Espresso' } },
    { en: 'Soy Latte', temp: 'both', price: '630',
      sub: { ja: 'ソイラテ', zh: '豆浆拿铁', ko: '소이 라테', es: 'Latte de soja' } },
    { en: 'Mattcha Latte', temp: 'hot', price: '700',
      sub: { ja: '抹茶ラテ', zh: '抹茶拿铁', ko: '말차 라테', es: 'Latte de matcha' } }
  ],

  beverage: [
    { group: null, en: 'Black Tea', temp: 'both', price: '550',
      sub: { ja: '紅茶', zh: '红茶', ko: '홍차', es: 'Té negro' } },

    { group: 'jp', en: 'Uji Sencha Green Tea', temp: 'both', price: '550',
      sub: { ja: '宇治煎茶', zh: '宇治煎茶', ko: '우지 센차', es: 'Té verde sencha de Uji' } },
    { group: 'jp', en: 'Uji Roasted Green Tea (Hojicha)', temp: 'both', price: '600',
      sub: { ja: '宇治ほうじ茶', zh: '宇治焙茶', ko: '우지 호지차', es: 'Té verde tostado de Uji (hojicha)' } },

    { group: 'herbal', en: 'Chamomile Citrus', temp: 'both', price: '600',
      sub: { ja: 'カモミールシトラス', zh: '洋甘菊柑橘', ko: '캐모마일 시트러스', es: 'Manzanilla y cítricos' },
      desc: { ja: 'カモミールに、甘いオレンジと酸味のあるレモンを合わせた定番のハーブティー。',
              en: 'A classic herbal infusion of chamomile, sweet orange and tangy lemon.',
              zh: '洋甘菊搭配甜橙与酸爽柠檬的经典花草茶。',
              ko: '캐모마일에 달콤한 오렌지와 상큼한 레몬을 더한 클래식 허브티.',
              es: 'Una infusión clásica de manzanilla, naranja dulce y limón.' } },
    { group: 'herbal', en: 'Organic African Nectar', temp: 'both', price: '600',
      sub: { ja: 'オーガニック アフリカンネクター', zh: '有机非洲花蜜', ko: '오가닉 아프리칸 넥타', es: 'Néctar africano ecológico' },
      desc: { ja: 'オーガニックのアフリカ産ルイボスに、バニラ・マンゴー・ハイビスカスの香り。',
              en: 'Organic African rooibos leaves with notes of vanilla, mango and hibiscus blossoms.',
              zh: '有机非洲南非国宝茶，带香草、芒果与洛神花香。',
              ko: '유기농 아프리카 루이보스에 바닐라·망고·히비스커스의 향.',
              es: 'Rooibos africano ecológico con notas de vainilla, mango y flor de hibisco.' } },
    { group: 'herbal', en: 'Wild Berry Hibiscus', temp: 'both', price: '600',
      sub: { ja: 'ワイルドベリーハイビスカス', zh: '野莓洛神花', ko: '와일드 베리 히비스커스', es: 'Hibisco y bayas silvestres' },
      desc: { ja: '鮮やかなハイビスカスとエルダーベリーの、華やかなハーブティー。',
              en: 'A lush infusion of bright hibiscus blossoms and elderberries.',
              zh: '鲜艳洛神花与接骨木莓交织的馥郁花草茶。',
              ko: '선명한 히비스커스와 엘더베리가 어우러진 화사한 허브티.',
              es: 'Una infusión intensa de flor de hibisco y bayas de saúco.' } },
    { group: 'herbal', en: 'Ginger Twist', temp: 'both', price: '600',
      sub: { ja: 'ジンジャーツイスト', zh: '姜香果茶', ko: '진저 트위스트', es: 'Jengibre especiado' },
      desc: { ja: 'ジンジャー、レモングラス、トロピカルフルーツ、ミントを調和させて。',
              en: 'A harmonious infusion of ginger, lemongrass, tropical fruits and mint.',
              zh: '生姜、柠檬草、热带水果与薄荷的和谐组合。',
              ko: '생강, 레몬그라스, 트로피컬 프루트, 민트가 조화를 이룬 허브티.',
              es: 'Una infusión armoniosa de jengibre, hierba limón, frutas tropicales y menta.' } },
    { group: 'herbal', en: '"Latte" Organic African Nectar', temp: 'both', price: '700',
      sub: { ja: 'アフリカンネクター ラテ', zh: '非洲花蜜拿铁', ko: '아프리칸 넥타 라테', es: 'Néctar africano con leche' },
      desc: { ja: 'オーガニックのアフリカ産ルイボスをミルクで。バニラ・マンゴー・ハイビスカスの香り。',
              en: 'Organic African rooibos leaves with fresh milk. Notes of vanilla, mango and hibiscus blossoms.',
              zh: '有机非洲南非国宝茶加入鲜奶，带香草、芒果与洛神花香。',
              ko: '유기농 아프리카 루이보스를 우유와 함께. 바닐라·망고·히비스커스의 향.',
              es: 'Rooibos africano ecológico con leche fresca. Notas de vainilla, mango e hibisco.' } },

    { group: null, en: 'Orange Juice', temp: 'iced', price: '550',
      sub: { ja: 'オレンジジュース', zh: '柳橙汁', ko: '오렌지 주스', es: 'Zumo de naranja' } },
    { group: null, en: 'Apple Juice', temp: 'iced', price: '550',
      sub: { ja: 'アップルジュース', zh: '苹果汁', ko: '사과 주스', es: 'Zumo de manzana' } },
    { group: null, en: 'Beer', temp: 'bottle', price: '650',
      sub: { ja: 'ビール（瓶）', zh: '瓶装啤酒', ko: '병맥주', es: 'Cerveza (botella)' } }
  ],

  /* ---------- 本文 ---------- */
  t: {
    ja: {
      'meta.title': '馬町珈琲 UMAMACHI COFFEE｜京都・五条の自家焙煎珈琲店',
      'meta.desc': '京都・五条の自家焙煎珈琲店。オランダ GIESEN の焙煎機で焙煎した豆を、一杯ずつハンドドリップで。バーガー・サンドイッチ・自家工房のスイーツも。大谷本廟・三十三間堂すぐ。',

      'nav.about': '馬町珈琲について', 'nav.coffee': '珈琲', 'nav.roast': '焙煎',
      'nav.food': 'フード', 'nav.drink': 'ドリンク', 'nav.visit': 'ご案内',

      'hero.tagline': '街歩きのとちゅうに、ひと休み。',
      'hero.sub': '京都・五条の自家焙煎珈琲店',
      'hero.scroll': 'SCROLL',

      'about.eyebrow': 'ようこそ',
      'about.title': '京都の街かどで。',
      'about.body1': '京都、五条にOPENした自家焙煎のコーヒーと、サンドイッチやハンバーガー、自家工房のスイーツが気軽にお楽しみいただけます。',
      'about.body2': '大谷本廟や三十三間堂にもほど近く、参拝などの際にぜひお立ち寄りくださいませ。',

      'coffee.eyebrow': '珈琲',
      'coffee.title': '一杯ずつ、手で淹れる。',
      'coffee.body': 'ご注文を承ってから、一杯ずつハンドドリップでお淹れしています。ご注文ごとに豆をその場で挽き、ペーパーフィルターで手淹れします。その一杯ずつに心を込めて、安らぎのひと時を過ごしていただきたいと願っております。',
      'beans.title': '生豆へのこだわり',
      'beans.body': '生豆は産地や農園にこだわって厳選したものを使用。その生豆を、焙煎士が最適の焙煎具合を見極めて焙煎しています。少量ずつ焙煎しますので鮮度は抜群。お湯を入れた瞬間にぷわーと膨らむ姿は、焙煎したてであることの証です。',

      'roast.eyebrow': '焙煎',
      'roast.title': 'オランダの職人がつくる焙煎機、GIESEN。',
      'roast.body1': '当店の焙煎機はオランダ製の〈GIESEN〉。京都・東山界隈ではいち早く導入いたしました。長年技術を培ってきた熟練のオランダ職人が手掛ける一台で、まるで機関車のような見た目と繊細な焙煎具合が、奥深い味わいを醸し出します。',
      'roast.body2': 'また生産管理には〈CROPSTER〉を採用。オーストリア発の、焙煎データをより細かくデータ化するソフトです。投入温度や焙煎時間、焙煎温度など様々なデータを一元管理するため、安定した味わいで焙煎が可能となります。これらを組み合わせることで、当店ならではの味を作り出しています。',

      'food.eyebrow': 'フード',
      'food.title': 'しっかり食べたい日に。',
      'food.note': 'フードをご注文の方は、ドリンクが100円引きになります。',
      'price.tax': '表示価格はすべて税込です。',
      'food.fries': 'ポテト付き',
      'food.pickles': 'ピクルス付き',

      'drink.eyebrow': 'ドリンク',
      'drink.title': 'メニュー',
      'drink.coffee': '自社焙煎コーヒー',
      'drink.other': 'その他のドリンク',
      'drink.milk_note': 'アーモンドミルク／オーツミルクへの変更 +100',
      'drink.jp_group': '日本茶',
      'drink.jp_note': '当店の日本茶は契約茶園の茶葉を使用しています。',
      'drink.herbal_group': 'ハーブティー',
      'drink.caffeine_free': 'カフェインフリー',
      'drink.hot': 'HOT', 'drink.iced': 'ICED', 'drink.both': 'HOT / ICED', 'drink.bottle': '瓶',

      'sweets.eyebrow': 'スイーツ',
      'sweets.title': 'ケースから、選ぶ。',
      'sweets.body': '自家工房でつくるスイーツを、ショーケースからお選びいただけます。その日にご用意しているものが並びますので、店頭でご覧くださいませ。',

      'video.title': 'お店の様子',
      'video.body': '30秒たらずの映像で、店内の雰囲気をご覧ください。',
      'video.play': '再生する',

      'ig.title': 'Instagram',
      'ig.body': '本日のスペシャルティコーヒーや、ケースに並ぶスイーツは Instagram でお知らせしています。',
      'ig.cta': 'Instagram を見る',

      'visit.eyebrow': 'ご案内',
      'visit.title': 'アクセス・営業時間',
      'visit.address_label': '住所',
      'visit.address': '〒605-0981 京都市東山区常盤町459-13',
      'visit.tel_label': '電話',
      'visit.hours_label': '営業時間',
      'visit.hours': '9:00 – 17:00',
      'visit.closed_label': '定休日',
      'visit.closed': '水曜日',
      'visit.access_label': 'アクセス',
      'visit.access': '大谷本廟・三十三間堂からほど近い、東山区馬町。参拝やお散歩の途中にお立ち寄りいただけます。',
      'visit.map': '地図を開く',

      'footer.company': '運営：株式会社緑歩園',
      'footer.rights': 'All rights reserved.'
    },

    en: {
      'meta.title': 'UMAMACHI COFFEE — House-roasted coffee in Gojo, Kyoto',
      'meta.desc': 'A house-roasting coffee shop in Gojo, Kyoto. Beans roasted on a Dutch GIESEN roaster, hand-dripped one cup at a time. Burgers, sandwiches and sweets from our own kitchen. A short walk from Otani Hombyo and Sanjusangendo.',

      'nav.about': 'About', 'nav.coffee': 'Coffee', 'nav.roast': 'Roasting',
      'nav.food': 'Food', 'nav.drink': 'Drinks', 'nav.visit': 'Visit',

      'hero.tagline': 'A pause on your walk.',
      'hero.sub': 'House-roasted coffee in Gojo, Kyoto',
      'hero.scroll': 'SCROLL',

      'about.eyebrow': 'Welcome',
      'about.title': 'On a Kyoto street corner.',
      'about.body1': 'Newly opened in Gojo, Kyoto: house-roasted coffee, sandwiches and burgers, and sweets from our own kitchen — all in an easy, everyday setting.',
      'about.body2': 'We are a short walk from Otani Hombyo and Sanjusangendo, so please drop in on your way to or from a visit.',

      'coffee.eyebrow': 'Coffee',
      'coffee.title': 'Brewed by hand, one cup at a time.',
      'coffee.body': 'Every cup is hand-dripped after you order. We grind the beans on the spot and brew through a paper filter, one cup at a time. We put our heart into each one, hoping you will spend a calm moment here.',
      'beans.title': 'About our green beans',
      'beans.body': 'We select our green beans carefully, by origin and by farm. Our roaster judges the ideal degree of roast for each one. Because we roast in small batches, freshness is outstanding — the way the grounds bloom the instant hot water touches them is proof of a coffee roasted only just now.',

      'roast.eyebrow': 'Roasting',
      'roast.title': 'A roaster built by Dutch craftsmen: GIESEN.',
      'roast.body1': 'Our roaster is a GIESEN, made in the Netherlands, and we were among the first to bring one to the Higashiyama district of Kyoto. Built by skilled Dutch craftsmen with long years of expertise, it looks almost like a steam locomotive, and its delicate control of the roast draws out a deep, layered flavour.',
      'roast.body2': 'For production management we use CROPSTER, software from Austria that turns roasting into fine-grained data. Charge temperature, roast time, roast temperature and more are all managed in one place, which lets us roast to a consistent taste. Together, these are what make the flavour ours.',

      'food.eyebrow': 'Food',
      'food.title': 'For when you want a proper meal.',
      'food.note': '¥100 off any drink when you order food.',
      'price.tax': 'All prices include tax.',
      'food.fries': 'Served with french fries',
      'food.pickles': 'Served with pickled vegetables',

      'drink.eyebrow': 'Drinks',
      'drink.title': 'Menu',
      'drink.coffee': 'House-roasted coffee',
      'drink.other': 'Other beverages',
      'drink.milk_note': 'Switch to almond or oat milk +100',
      'drink.jp_group': 'Japanese tea',
      'drink.jp_note': 'Our Japanese tea leaves are carefully selected from partner tea farms.',
      'drink.herbal_group': 'Herbal tea',
      'drink.caffeine_free': 'Caffeine free',
      'drink.hot': 'HOT', 'drink.iced': 'ICED', 'drink.both': 'HOT / ICED', 'drink.bottle': 'BOTTLE',

      'sweets.eyebrow': 'Sweets',
      'sweets.title': 'Choose from the case.',
      'sweets.body': 'Sweets made in our own kitchen, chosen straight from the display case. What you see is what we have prepared that day, so please take a look when you arrive.',

      'video.title': 'Inside the shop',
      'video.body': 'A short film — under half a minute — of the room and the counter.',
      'video.play': 'Play',

      'ig.title': 'Instagram',
      'ig.body': "Today's specialty coffee and the sweets in the case are posted on Instagram.",
      'ig.cta': 'View on Instagram',

      'visit.eyebrow': 'Visit',
      'visit.title': 'Access & opening hours',
      'visit.address_label': 'Address',
      'visit.address': '459-13 Tokiwa-cho, Higashiyama-ku, Kyoto 605-0981',
      'visit.tel_label': 'Phone',
      'visit.hours_label': 'Open',
      'visit.hours': '9:00 – 17:00',
      'visit.closed_label': 'Closed',
      'visit.closed': 'Wednesdays',
      'visit.access_label': 'Getting here',
      'visit.access': 'In Umamachi, Higashiyama-ku — a short walk from Otani Hombyo and Sanjusangendo. Easy to fold into a temple visit or an afternoon walk.',
      'visit.map': 'Open in Maps',

      'footer.company': 'Operated by Ryokuhoen Co., Ltd.',
      'footer.rights': 'All rights reserved.'
    },

    zh: {
      'meta.title': '马町珈琲 UMAMACHI COFFEE｜京都五条的自家烘焙咖啡馆',
      'meta.desc': '位于京都五条的自家烘焙咖啡馆。以荷兰 GIESEN 烘豆机烘焙，一杯一杯手冲。另有汉堡、三明治与自家工坊甜点。邻近大谷本庙、三十三间堂。',

      'nav.about': '关于本店', 'nav.coffee': '咖啡', 'nav.roast': '烘焙',
      'nav.food': '餐点', 'nav.drink': '饮品', 'nav.visit': '店铺资讯',

      'hero.tagline': '漫步途中，稍作歇息。',
      'hero.sub': '京都五条的自家烘焙咖啡馆',
      'hero.scroll': '向下滚动',

      'about.eyebrow': '欢迎光临',
      'about.title': '在京都的街角。',
      'about.body1': '位于京都五条的咖啡馆。自家烘焙的咖啡、三明治与汉堡，以及自家工坊制作的甜点，都能轻松享用。',
      'about.body2': '距离大谷本庙与三十三间堂很近，参拜途中欢迎顺道前来。',

      'coffee.eyebrow': '咖啡',
      'coffee.title': '一杯一杯，亲手冲煮。',
      'coffee.body': '接到点单后才开始手冲，一次一杯。现点现磨，以滤纸手工冲煮。我们在每一杯里都注入心意，希望您在这里度过一段安心的时光。',
      'beans.title': '关于生豆',
      'beans.body': '生豆严选自讲究的产地与庄园，再由烘焙师判断最合适的烘焙程度。因为每次只少量烘焙，新鲜度格外出色——注入热水的瞬间粉层饱满隆起，正是刚烘焙不久的证明。',

      'roast.eyebrow': '烘焙',
      'roast.title': '荷兰职人打造的烘豆机，GIESEN。',
      'roast.body1': '本店使用荷兰制〈GIESEN〉烘豆机，在京都东山一带率先引进。这台机器由技术积累多年的资深荷兰职人打造，外形宛如蒸汽火车，细腻的烘焙控制酝酿出深邃的风味。',
      'roast.body2': '生产管理则采用〈CROPSTER〉——来自奥地利、能将烘焙过程细致数据化的软件。投豆温度、烘焙时间、烘焙温度等各项数据统一管理，因此能稳定地烘焙出一致的风味。两者结合，造就了本店独有的味道。',

      'food.eyebrow': '餐点',
      'food.title': '想好好吃一顿的日子。',
      'food.note': '点用餐点，饮品即减 100 日元。',
      'price.tax': '标示价格均为含税价。',
      'food.fries': '附薯条',
      'food.pickles': '附腌菜',

      'drink.eyebrow': '饮品',
      'drink.title': '菜单',
      'drink.coffee': '自家烘焙咖啡',
      'drink.other': '其他饮品',
      'drink.milk_note': '更换为杏仁奶／燕麦奶 +100',
      'drink.jp_group': '日本茶',
      'drink.jp_note': '本店的日本茶采用契约茶园的茶叶。',
      'drink.herbal_group': '花草茶',
      'drink.caffeine_free': '无咖啡因',
      'drink.hot': '热', 'drink.iced': '冰', 'drink.both': '热 / 冰', 'drink.bottle': '瓶装',

      'sweets.eyebrow': '甜点',
      'sweets.title': '从甜点柜里挑选。',
      'sweets.body': '自家工坊制作的甜点，可直接从展示柜挑选。柜里陈列的是当天准备的品项，欢迎到店后细看。',

      'video.title': '店内一景',
      'video.body': '不到半分钟的短片，带您看看店内的样子。',
      'video.play': '播放',

      'ig.title': 'Instagram',
      'ig.body': '当日的精品咖啡与柜内甜点，都会在 Instagram 上发布。',
      'ig.cta': '前往 Instagram',

      'visit.eyebrow': '店铺资讯',
      'visit.title': '交通与营业时间',
      'visit.address_label': '地址',
      'visit.address': '〒605-0981 京都市东山区常盘町459-13',
      'visit.tel_label': '电话',
      'visit.hours_label': '营业时间',
      'visit.hours': '9:00 – 17:00',
      'visit.closed_label': '公休日',
      'visit.closed': '星期三',
      'visit.access_label': '交通方式',
      'visit.access': '位于东山区马町，距离大谷本庙与三十三间堂步行可达。适合安排在参拜或散步的途中。',
      'visit.map': '打开地图',

      'footer.company': '营运：株式会社绿步园',
      'footer.rights': 'All rights reserved.'
    },

    ko: {
      'meta.title': '우마마치 커피 UMAMACHI COFFEE｜교토 고조의 자가 배전 커피점',
      'meta.desc': '교토 고조의 자가 배전 커피점. 네덜란드 GIESEN 로스터로 볶은 원두를 한 잔씩 핸드드립으로. 버거·샌드위치와 자체 공방 디저트도 함께. 오타니 혼뵤·산주산겐도에서 가깝습니다.',

      'nav.about': '소개', 'nav.coffee': '커피', 'nav.roast': '배전',
      'nav.food': '푸드', 'nav.drink': '음료', 'nav.visit': '이용 안내',

      'hero.tagline': '거리를 걷다가, 잠시 쉬어가세요.',
      'hero.sub': '교토 고조의 자가 배전 커피점',
      'hero.scroll': '스크롤',

      'about.eyebrow': '어서 오세요',
      'about.title': '교토의 길모퉁이에서.',
      'about.body1': '교토 고조에 문을 연 카페입니다. 자가 배전 커피와 샌드위치·버거, 그리고 자체 공방에서 만든 디저트를 편안하게 즐기실 수 있습니다.',
      'about.body2': '오타니 혼뵤와 산주산겐도에서 가까워, 참배 길에 부담 없이 들러 주세요.',

      'coffee.eyebrow': '커피',
      'coffee.title': '한 잔씩, 손으로 내립니다.',
      'coffee.body': '주문을 받은 뒤 한 잔씩 핸드드립으로 내립니다. 주문할 때마다 그 자리에서 원두를 갈아 페이퍼 필터로 손수 내립니다. 그 한 잔에 마음을 담아, 편안한 시간을 보내시기를 바랍니다.',
      'beans.title': '생두에 대하여',
      'beans.body': '산지와 농원을 까다롭게 골라 선별한 생두를 사용합니다. 그 생두를 배전사가 가장 알맞은 배전도로 가려내어 볶습니다. 소량씩 볶기 때문에 신선도가 뛰어나며, 뜨거운 물을 붓는 순간 부풀어 오르는 모습이 갓 볶았다는 증거입니다.',

      'roast.eyebrow': '배전',
      'roast.title': '네덜란드 장인이 만드는 로스터, GIESEN.',
      'roast.body1': '저희 배전기는 네덜란드제 〈GIESEN〉으로, 교토 히가시야마 일대에서 가장 먼저 도입했습니다. 오랜 세월 기술을 쌓아 온 네덜란드 장인이 만든 기계로, 기관차를 닮은 외관과 섬세한 배전이 깊은 맛을 끌어냅니다.',
      'roast.body2': '생산 관리에는 〈CROPSTER〉를 사용합니다. 오스트리아에서 만든, 배전 데이터를 세밀하게 기록하는 소프트웨어입니다. 투입 온도와 배전 시간, 배전 온도 등 여러 데이터를 한곳에서 관리하기 때문에 안정된 맛으로 볶을 수 있습니다. 이 둘을 함께 써서 저희만의 맛을 만듭니다.',

      'food.eyebrow': '푸드',
      'food.title': '든든히 먹고 싶은 날에.',
      'food.note': '푸드를 주문하시면 음료가 100엔 할인됩니다.',
      'price.tax': '표시 가격은 모두 세금 포함입니다.',
      'food.fries': '감자튀김 포함',
      'food.pickles': '피클 포함',

      'drink.eyebrow': '음료',
      'drink.title': '메뉴',
      'drink.coffee': '자가 배전 커피',
      'drink.other': '그 외 음료',
      'drink.milk_note': '아몬드 밀크·오트 밀크 변경 +100',
      'drink.jp_group': '일본차',
      'drink.jp_note': '저희 일본차는 계약 다원의 찻잎을 사용합니다.',
      'drink.herbal_group': '허브티',
      'drink.caffeine_free': '카페인 프리',
      'drink.hot': 'HOT', 'drink.iced': 'ICED', 'drink.both': 'HOT / ICED', 'drink.bottle': '병',

      'sweets.eyebrow': '디저트',
      'sweets.title': '쇼케이스에서 고르세요.',
      'sweets.body': '자체 공방에서 만든 디저트를 쇼케이스에서 직접 고르실 수 있습니다. 그날 준비한 것들이 진열되니, 오셔서 살펴봐 주세요.',

      'video.title': '가게 풍경',
      'video.body': '30초 남짓의 영상으로 매장 분위기를 담았습니다.',
      'video.play': '재생',

      'ig.title': 'Instagram',
      'ig.body': '오늘의 스페셜티 커피와 쇼케이스의 디저트는 Instagram으로 알려 드립니다.',
      'ig.cta': 'Instagram 보기',

      'visit.eyebrow': '이용 안내',
      'visit.title': '오시는 길 · 영업시간',
      'visit.address_label': '주소',
      'visit.address': '〒605-0981 교토시 히가시야마구 도키와초 459-13',
      'visit.tel_label': '전화',
      'visit.hours_label': '영업시간',
      'visit.hours': '9:00 – 17:00',
      'visit.closed_label': '정기휴일',
      'visit.closed': '수요일',
      'visit.access_label': '오시는 길',
      'visit.access': '히가시야마구 우마마치에 있으며, 오타니 혼뵤와 산주산겐도에서 걸어서 가까운 거리입니다. 참배나 산책 길에 들르기 좋습니다.',
      'visit.map': '지도 열기',

      'footer.company': '운영: 주식회사 료쿠호엔',
      'footer.rights': 'All rights reserved.'
    },

    es: {
      'meta.title': 'UMAMACHI COFFEE — Café de tueste propio en Gojo, Kioto',
      'meta.desc': 'Cafetería de tueste propio en Gojo, Kioto. Grano tostado en una GIESEN neerlandesa y preparado a mano, taza a taza. Hamburguesas, sándwiches y dulces de obrador propio. Muy cerca de Otani Hombyo y Sanjusangendo.',

      'nav.about': 'El local', 'nav.coffee': 'Café', 'nav.roast': 'Tueste',
      'nav.food': 'Comida', 'nav.drink': 'Bebidas', 'nav.visit': 'Visítanos',

      'hero.tagline': 'Una pausa en el paseo.',
      'hero.sub': 'Café de tueste propio en Gojo, Kioto',
      'hero.scroll': 'DESLIZA',

      'about.eyebrow': 'Bienvenido',
      'about.title': 'En una esquina de Kioto.',
      'about.body1': 'Una cafetería en Gojo, Kioto: café de tueste propio, sándwiches y hamburguesas, y dulces elaborados en nuestro propio obrador, en un ambiente tranquilo y cotidiano.',
      'about.body2': 'Estamos a pocos pasos de Otani Hombyo y de Sanjusangendo: pase a vernos de camino a su visita.',

      'coffee.eyebrow': 'Café',
      'coffee.title': 'Preparado a mano, taza a taza.',
      'coffee.body': 'Cada taza se prepara a mano después de tomar el pedido. Molemos el grano en el momento y colamos con filtro de papel, una taza cada vez. Ponemos el corazón en cada una, con el deseo de que pase aquí un rato de calma.',
      'beans.title': 'Sobre el café verde',
      'beans.body': 'Seleccionamos el café verde con cuidado, por origen y por finca. Nuestro tostador determina el punto de tueste ideal para cada uno. Tostamos en pequeñas cantidades, así que la frescura es excepcional: la forma en que el café se hincha al recibir el agua caliente es la prueba de un tueste muy reciente.',

      'roast.eyebrow': 'Tueste',
      'roast.title': 'Una tostadora hecha por artesanos neerlandeses: GIESEN.',
      'roast.body1': 'Nuestra tostadora es una GIESEN fabricada en los Países Bajos, y fuimos de los primeros en incorporarla en el barrio de Higashiyama de Kioto. La construyen artesanos neerlandeses con muchos años de oficio; su aspecto recuerda al de una locomotora y su control delicado del tueste da lugar a un sabor hondo y con matices.',
      'roast.body2': 'Para la gestión de la producción utilizamos CROPSTER, un software austriaco que convierte el tueste en datos detallados. La temperatura de carga, el tiempo y la temperatura de tueste y otros datos se gestionan en un único lugar, lo que nos permite tostar con un sabor constante. De la combinación de ambos nace nuestro sabor.',

      'food.eyebrow': 'Comida',
      'food.title': 'Para los días de comer bien.',
      'food.note': '100 ¥ de descuento en la bebida si pide comida.',
      'price.tax': 'Todos los precios incluyen impuestos.',
      'food.fries': 'Con patatas fritas',
      'food.pickles': 'Con encurtidos',

      'drink.eyebrow': 'Bebidas',
      'drink.title': 'Carta',
      'drink.coffee': 'Café de tueste propio',
      'drink.other': 'Otras bebidas',
      'drink.milk_note': 'Cambio a leche de almendra o avena +100',
      'drink.jp_group': 'Té japonés',
      'drink.jp_note': 'Nuestro té japonés procede de fincas de té con las que trabajamos directamente.',
      'drink.herbal_group': 'Infusiones',
      'drink.caffeine_free': 'Sin cafeína',
      'drink.hot': 'CALIENTE', 'drink.iced': 'FRÍO', 'drink.both': 'CALIENTE / FRÍO', 'drink.bottle': 'BOTELLA',

      'sweets.eyebrow': 'Dulces',
      'sweets.title': 'Elija en la vitrina.',
      'sweets.body': 'Dulces elaborados en nuestro obrador, para escoger directamente de la vitrina. Lo que se ve es lo que hemos preparado ese día, así que écheles un vistazo al llegar.',

      'video.title': 'El local por dentro',
      'video.body': 'Un vídeo de menos de medio minuto por la sala y la barra.',
      'video.play': 'Reproducir',

      'ig.title': 'Instagram',
      'ig.body': 'Publicamos en Instagram el café de especialidad del día y los dulces de la vitrina.',
      'ig.cta': 'Ver en Instagram',

      'visit.eyebrow': 'Visítanos',
      'visit.title': 'Cómo llegar y horario',
      'visit.address_label': 'Dirección',
      'visit.address': '459-13 Tokiwa-cho, Higashiyama-ku, Kioto 605-0981',
      'visit.tel_label': 'Teléfono',
      'visit.hours_label': 'Horario',
      'visit.hours': '9:00 – 17:00',
      'visit.closed_label': 'Cerrado',
      'visit.closed': 'Miércoles',
      'visit.access_label': 'Cómo llegar',
      'visit.access': 'En Umamachi, barrio de Higashiyama, a pocos minutos a pie de Otani Hombyo y Sanjusangendo. Fácil de incluir en una visita a los templos o en un paseo.',
      'visit.map': 'Abrir en Maps',

      'footer.company': 'Gestionado por Ryokuhoen Co., Ltd.',
      'footer.rights': 'All rights reserved.'
    }
  }
};
