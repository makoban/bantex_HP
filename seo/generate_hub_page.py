"""
業種別AIサービス ハブページ生成スクリプト
全業種×パターンへのリンクを集約したインデックスページを生成する
"""

import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR / "industries.json"
OUTPUT_PATH = SCRIPT_DIR.parent / "industry-ai.html"
BASE_URL = "https://bantex.jp/seo/pages"


def to_slug(name):
    """generate_seo_pages.pyと同じスラッグマッピング"""
    slug_map = {
        "美容室": "biyoushitsu", "理容室": "riyoushitsu",
        "エステサロン": "esthe-salon", "ネイルサロン": "nail-salon",
        "まつげサロン": "matsuge-salon", "整骨院": "seikotsuin",
        "整体院": "seitaiin", "鍼灸院": "shinkyuuin",
        "歯科医院": "shika-iin", "クリニック": "clinic",
        "内科": "naika", "眼科": "ganka", "皮膚科": "hifuka",
        "動物病院": "doubutsu-byouin", "薬局": "yakkyoku",
        "介護施設": "kaigo-shisetsu", "デイサービス": "day-service",
        "税理士事務所": "zeirishi", "弁護士事務所": "bengoshi",
        "社労士事務所": "sharoushi", "行政書士事務所": "gyouseishoshi",
        "司法書士事務所": "shihoushoshi", "会計事務所": "kaikei-jimusho",
        "飲食店": "inshokuten", "カフェ": "cafe", "居酒屋": "izakaya",
        "ラーメン店": "ramen", "パン屋": "panya", "ケーキ屋": "cakeshop",
        "テイクアウト専門店": "takeout", "不動産会社": "fudousan",
        "不動産管理会社": "fudousan-kanri", "建設会社": "kensetsu",
        "リフォーム会社": "reform", "塗装会社": "tosou",
        "電気工事会社": "denki-kouji", "設備工事会社": "setsubi-kouji",
        "解体業者": "kaitai", "学習塾": "gakushuujuku",
        "英会話教室": "eikaiwa", "プログラミング教室": "programming",
        "ピアノ教室": "piano", "ヨガスタジオ": "yoga",
        "ダンススタジオ": "dance", "フィットネスジム": "fitness",
        "スポーツクラブ": "sports-club", "写真館": "shashinkan",
        "花屋": "hanaya", "ペットショップ": "pet-shop",
        "トリミングサロン": "trimming", "自動車整備工場": "jidousha-seibi",
        "中古車販売店": "chuukosha", "バイクショップ": "bike-shop",
        "クリーニング店": "cleaning", "コインランドリー": "coin-laundry",
        "印刷会社": "insatsu", "デザイン事務所": "design-jimusho",
        "IT企業": "it-kigyo", "Webデザイン会社": "web-design",
        "人材派遣会社": "jinzai-haken", "結婚相談所": "kekkon-soudanjo",
        "葬儀社": "sougisha", "旅館": "ryokan", "民宿": "minshuku",
        "レンタルスペース": "rental-space", "コワーキングスペース": "coworking",
        "農家": "nouka", "漁師": "ryoushi", "酒蔵": "sakagura",
        "製造業": "seizougyou", "運送会社": "unsou", "タクシー会社": "taxi",
        "保険代理店": "hoken-dairiten", "アパレルショップ": "apparel",
        "雑貨店": "zakkaten", "古着屋": "furugiya",
        "リサイクルショップ": "recycle-shop",
        "パーソナルトレーナー": "personal-trainer",
        "占い師": "uranai", "音楽スタジオ": "music-studio",
        "カメラマン": "cameraman", "ライター": "writer",
        "コンサルタント": "consultant",
    }
    return slug_map.get(name, name.lower().replace(" ", "-"))


# 業種カテゴリ分類
CATEGORIES = {
    "美容・リラクゼーション": ["美容室", "理容室", "エステサロン", "ネイルサロン", "まつげサロン"],
    "医療・健康": ["整骨院", "整体院", "鍼灸院", "歯科医院", "クリニック", "内科", "眼科", "皮膚科", "動物病院", "薬局"],
    "介護・福祉": ["介護施設", "デイサービス"],
    "士業・専門サービス": ["税理士事務所", "弁護士事務所", "社労士事務所", "行政書士事務所", "司法書士事務所", "会計事務所"],
    "飲食": ["飲食店", "カフェ", "居酒屋", "ラーメン店", "パン屋", "ケーキ屋", "テイクアウト専門店"],
    "不動産・建設": ["不動産会社", "不動産管理会社", "建設会社", "リフォーム会社", "塗装会社", "電気工事会社", "設備工事会社", "解体業者"],
    "教育・スクール": ["学習塾", "英会話教室", "プログラミング教室", "ピアノ教室"],
    "フィットネス・スポーツ": ["ヨガスタジオ", "ダンススタジオ", "フィットネスジム", "スポーツクラブ", "パーソナルトレーナー"],
    "小売・ショップ": ["花屋", "ペットショップ", "アパレルショップ", "雑貨店", "古着屋", "リサイクルショップ"],
    "自動車": ["自動車整備工場", "中古車販売店", "バイクショップ"],
    "生活サービス": ["写真館", "トリミングサロン", "クリーニング店", "コインランドリー", "結婚相談所", "葬儀社"],
    "IT・クリエイティブ": ["印刷会社", "デザイン事務所", "IT企業", "Webデザイン会社", "音楽スタジオ", "カメラマン", "ライター"],
    "宿泊・スペース": ["旅館", "民宿", "レンタルスペース", "コワーキングスペース"],
    "その他": ["人材派遣会社", "保険代理店", "農家", "酒蔵", "製造業", "運送会社", "タクシー会社", "コンサルタント", "占い師"],
}


def generate():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    patterns = data["patterns"]
    today = datetime.now().strftime("%Y-%m-%d")

    # カテゴリごとのHTML生成
    categories_html = ""
    total_links = 0

    for cat_name, industries in CATEGORIES.items():
        cards_html = ""
        for ind_name in industries:
            links_html = ""
            for p in patterns:
                slug = f"{p['slug']}-{to_slug(ind_name)}"
                url = f"seo/pages/{slug}.html"
                links_html += f'            <a href="{url}">{p["label"]}</a>\n'
                total_links += 1

            cards_html += f"""
        <div class="ind-card">
          <h3 class="ind-name">{ind_name}</h3>
          <div class="ind-links">
{links_html}          </div>
        </div>"""

        categories_html += f"""
      <div class="cat-section">
        <h2 class="cat-heading">{cat_name}</h2>
        <div class="ind-grid">{cards_html}
        </div>
      </div>"""

    # JSON-LD
    items = []
    pos = 1
    for cat_name, industries in CATEGORIES.items():
        for ind_name in industries:
            items.append({
                "@type": "ListItem",
                "position": pos,
                "name": f"{ind_name}向けAIサービス",
                "url": f"https://bantex.jp/seo/pages/ai-hp-{to_slug(ind_name)}.html",
            })
            pos += 1

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "業種別AIサービス活用ガイド",
        "description": "81業種それぞれに最適なAIサービスの活用方法を解説",
        "numberOfItems": len(items),
        "itemListElement": items,
    }, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>業種別AIサービス活用ガイド｜81業種対応 | 株式会社バンテックス</title>
  <meta name="description" content="美容室、飲食店、税理士事務所、不動産会社など81業種のAI活用方法を徹底解説。HP作成、SNS運用、集客、業務効率化、顧客対応の自動化まで、あなたの業種に最適なAIサービスが見つかります。">
  <meta name="author" content="株式会社バンテックス">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://bantex.jp/industry-ai.html">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://bantex.jp/industry-ai.html">
  <meta property="og:title" content="業種別AIサービス活用ガイド｜81業種対応">
  <meta property="og:description" content="81業種それぞれに最適なAIサービスの活用方法を解説。HP作成、SNS運用、集客、業務効率化、顧客対応の自動化まで。">
  <meta property="og:site_name" content="株式会社バンテックス">
  <meta property="og:locale" content="ja_JP">

  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="業種別AIサービス活用ガイド｜81業種対応 | バンテックス">
  <meta name="twitter:description" content="81業種のAI活用方法を徹底解説。あなたの業種に最適なAIサービスが見つかります。">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@800&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {jsonld}
  </script>

  <style>
    :root {{
      --color-primary: #1A2332;
      --color-accent: #2A6EBB;
      --color-bg: #F8F7F5;
      --color-surface: #EDECEA;
      --color-text: #2C2C2C;
      --color-white: #FFFFFF;
      --font-sans: 'Noto Sans JP', sans-serif;
      --font-brand: 'Inter', sans-serif;
      --header-h: 64px;
      --radius: 8px;
      --shadow-md: 0 4px 20px rgba(0,0,0,0.08);
      --transition-base: 0.28s cubic-bezier(0.4,0,0.2,1);
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{ font-family: var(--font-sans); color: var(--color-text); background: var(--color-bg); line-height: 1.8; font-size: 15px; }}
    a {{ color: inherit; text-decoration: none; }}
    .container {{ max-width: 1120px; margin: 0 auto; padding: 0 1rem; }}

    .site-header {{
      position: sticky; top: 0; z-index: 100;
      height: var(--header-h); background: rgba(248,247,245,0.95);
      backdrop-filter: blur(10px); border-bottom: 1px solid rgba(0,0,0,0.06);
    }}
    .header-inner {{ display: flex; align-items: center; justify-content: space-between; height: var(--header-h); }}
    .site-logo {{ font-family: var(--font-brand); font-weight: 800; font-size: 1.5rem; letter-spacing: 0.12em; color: var(--color-primary); }}
    .primary-nav ul {{ display: flex; gap: 2rem; list-style: none; }}
    .primary-nav a {{ font-size: 0.85rem; font-weight: 700; color: var(--color-primary); }}
    .primary-nav a:hover {{ color: var(--color-accent); }}

    .hero {{
      background: linear-gradient(135deg, var(--color-primary), #2A4A6B);
      color: #fff; padding: 5rem 0 3rem; text-align: center;
    }}
    .hero h1 {{ font-size: clamp(1.5rem, 4vw, 2.2rem); margin-bottom: 0.75rem; }}
    .hero p {{ opacity: 0.85; font-size: 0.95rem; max-width: 600px; margin: 0 auto; }}
    .hero-stats {{ display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; }}
    .hero-stat {{ text-align: center; }}
    .hero-stat-num {{ font-family: var(--font-brand); font-size: 2rem; font-weight: 800; }}
    .hero-stat-label {{ font-size: 0.8rem; opacity: 0.7; }}

    .breadcrumb {{ padding: 1rem 0; font-size: 0.8rem; color: #888; }}
    .breadcrumb a {{ color: var(--color-accent); }}

    .cat-section {{ margin-bottom: 3rem; }}
    .cat-heading {{
      font-size: 1.1rem; font-weight: 700; color: var(--color-primary);
      padding: 0.5rem 0; margin-bottom: 1rem;
      border-bottom: 2px solid var(--color-accent);
    }}
    .ind-grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 1rem;
    }}
    .ind-card {{
      background: var(--color-white); border-radius: var(--radius);
      padding: 1rem; box-shadow: var(--shadow-md);
      transition: transform var(--transition-base);
    }}
    .ind-card:hover {{ transform: translateY(-2px); }}
    .ind-name {{ font-size: 0.95rem; font-weight: 700; color: var(--color-primary); margin-bottom: 0.5rem; }}
    .ind-links {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
    .ind-links a {{
      font-size: 0.75rem; padding: 0.2rem 0.6rem;
      background: var(--color-surface); border-radius: 20px;
      color: var(--color-accent); font-weight: 700;
      transition: background var(--transition-base);
    }}
    .ind-links a:hover {{ background: rgba(42,110,187,0.12); }}

    .site-footer {{
      background: var(--color-primary); color: rgba(255,255,255,0.7);
      padding: 2rem 0; text-align: center; font-size: 0.8rem;
    }}
    .footer-nav {{ display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1rem; flex-wrap: wrap; }}
    .footer-nav a {{ color: rgba(255,255,255,0.9); }}

    @media (max-width: 768px) {{
      .primary-nav {{ display: none; }}
      .hero-stats {{ flex-direction: column; gap: 1rem; }}
      .ind-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <div class="header-inner">
        <a href="https://bantex.jp/" class="site-logo">BANTEX</a>
        <nav class="primary-nav">
          <ul>
            <li><a href="https://bantex.jp/">トップ</a></li>
            <li><a href="https://bantex.jp/ai-services.html">AIサービス</a></li>
            <li><a href="https://bantex.jp/#contact">お問い合わせ</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </header>

  <div class="container">
    <nav class="breadcrumb">
      <a href="https://bantex.jp/">トップ</a> &gt;
      <a href="https://bantex.jp/ai-services.html">AIサービス</a> &gt;
      業種別AIサービス活用ガイド
    </nav>
  </div>

  <section class="hero">
    <div class="container">
      <h1>業種別AIサービス活用ガイド</h1>
      <p>あなたの業種に最適なAIサービスの使い方を、HP作成・SNS運用・集客・業務効率化・顧客対応の5つの切り口で解説します。</p>
      <div class="hero-stats">
        <div class="hero-stat">
          <div class="hero-stat-num">81</div>
          <div class="hero-stat-label">対応業種</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-num">405</div>
          <div class="hero-stat-label">記事数</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-num">9</div>
          <div class="hero-stat-label">AIサービス</div>
        </div>
      </div>
    </div>
  </section>

  <main style="padding: 3rem 0;">
    <div class="container">
{categories_html}
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <nav class="footer-nav">
        <a href="https://bantex.jp/">トップ</a>
        <a href="https://bantex.jp/ai-services.html">AIサービス</a>
        <a href="https://bantex.jp/privacy.html">プライバシーポリシー</a>
        <a href="https://bantex.jp/terms.html">利用規約</a>
      </nav>
      <p>&copy; {datetime.now().year} 株式会社バンテックス All rights reserved.</p>
    </div>
  </footer>
</body>
</html>"""

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] {OUTPUT_PATH.name} generated ({total_links} links)")


if __name__ == "__main__":
    generate()
