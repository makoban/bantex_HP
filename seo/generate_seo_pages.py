"""
bantex.jp Programmatic SEO ページ生成スクリプト

業種×サービスパターンで大量のSEOページを自動生成する。
Claude APIで各ページの独自コンテンツを生成し、HTMLファイルとして出力。

使い方:
  python generate_seo_pages.py                  # 全ページ生成
  python generate_seo_pages.py --dry-run        # 生成対象の一覧表示のみ
  python generate_seo_pages.py --limit 10       # 最初の10ページのみ
  python generate_seo_pages.py --pattern hp     # HPパターンのみ
  python generate_seo_pages.py --industry 美容室  # 美容室のみ
"""

import json
import os
import sys
import time
import argparse
import re
from pathlib import Path
from datetime import datetime

# ── 設定 ──────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "template.html"
DATA_PATH = SCRIPT_DIR / "industries.json"
OUTPUT_DIR = SCRIPT_DIR / "pages"
SITEMAP_PATH = SCRIPT_DIR.parent / "sitemap.xml"
BASE_URL = "https://bantex.jp/seo/pages"

# Claude API
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-sonnet-4-6"
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1.5  # seconds between API calls


# ── データ読み込み ─────────────────────────────────────────
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ── スラッグ生成 ──────────────────────────────────────────
def to_slug(text):
    """日本語テキストからURL用スラッグを生成"""
    # 業種名→ローマ字マッピング
    slug_map = {
        "美容室": "biyoushitsu",
        "理容室": "riyoushitsu",
        "エステサロン": "esthe-salon",
        "ネイルサロン": "nail-salon",
        "まつげサロン": "matsuge-salon",
        "整骨院": "seikotsuin",
        "整体院": "seitaiin",
        "鍼灸院": "shinkyuuin",
        "歯科医院": "shika-iin",
        "クリニック": "clinic",
        "内科": "naika",
        "眼科": "ganka",
        "皮膚科": "hifuka",
        "動物病院": "doubutsu-byouin",
        "薬局": "yakkyoku",
        "介護施設": "kaigo-shisetsu",
        "デイサービス": "day-service",
        "税理士事務所": "zeirishi",
        "弁護士事務所": "bengoshi",
        "社労士事務所": "sharoushi",
        "行政書士事務所": "gyouseishoshi",
        "司法書士事務所": "shihoushoshi",
        "会計事務所": "kaikei-jimusho",
        "飲食店": "inshokuten",
        "カフェ": "cafe",
        "居酒屋": "izakaya",
        "ラーメン店": "ramen",
        "パン屋": "panya",
        "ケーキ屋": "cakeshop",
        "テイクアウト専門店": "takeout",
        "不動産会社": "fudousan",
        "不動産管理会社": "fudousan-kanri",
        "建設会社": "kensetsu",
        "リフォーム会社": "reform",
        "塗装会社": "tosou",
        "電気工事会社": "denki-kouji",
        "設備工事会社": "setsubi-kouji",
        "解体業者": "kaitai",
        "学習塾": "gakushuujuku",
        "英会話教室": "eikaiwa",
        "プログラミング教室": "programming",
        "ピアノ教室": "piano",
        "ヨガスタジオ": "yoga",
        "ダンススタジオ": "dance",
        "フィットネスジム": "fitness",
        "スポーツクラブ": "sports-club",
        "写真館": "shashinkan",
        "花屋": "hanaya",
        "ペットショップ": "pet-shop",
        "トリミングサロン": "trimming",
        "自動車整備工場": "jidousha-seibi",
        "中古車販売店": "chuukosha",
        "バイクショップ": "bike-shop",
        "クリーニング店": "cleaning",
        "コインランドリー": "coin-laundry",
        "印刷会社": "insatsu",
        "デザイン事務所": "design-jimusho",
        "IT企業": "it-kigyo",
        "Webデザイン会社": "web-design",
        "人材派遣会社": "jinzai-haken",
        "結婚相談所": "kekkon-soudanjo",
        "葬儀社": "sougisha",
        "旅館": "ryokan",
        "民宿": "minshuku",
        "レンタルスペース": "rental-space",
        "コワーキングスペース": "coworking",
        "農家": "nouka",
        "漁師": "ryoushi",
        "酒蔵": "sakagura",
        "製造業": "seizougyou",
        "運送会社": "unsou",
        "タクシー会社": "taxi",
        "保険代理店": "hoken-dairiten",
        "アパレルショップ": "apparel",
        "雑貨店": "zakkaten",
        "古着屋": "furugiya",
        "リサイクルショップ": "recycle-shop",
        "パーソナルトレーナー": "personal-trainer",
        "占い師": "uranai",
        "音楽スタジオ": "music-studio",
        "カメラマン": "cameraman",
        "ライター": "writer",
        "コンサルタント": "consultant",
    }
    return slug_map.get(text, text.lower().replace(" ", "-"))


# ── Claude API呼び出し ────────────────────────────────────
def generate_content(industry, pattern, services_info):
    """Claude APIで業種×パターンの独自コンテンツを生成"""
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""あなたは中小企業・個人事業主向けのAIサービス「バンテックス」のコンテンツライターです。

以下の条件でSEOページのコンテンツを生成してください。

【業種】{industry["name"]}
【パターン】{pattern["title_template"].replace("{業種}", industry["name"])}
【ページの目的】{pattern["purpose"]}

【バンテックスの関連サービス】
{json.dumps(services_info, ensure_ascii=False, indent=2)}

以下のJSON形式で出力してください（他の文章は不要）：
{{
  "meta_description": "（120文字以内のmeta description）",
  "h1": "（ページのH1見出し、30文字以内）",
  "intro": "（導入文、150-200文字。{industry["name"]}の経営者が共感する課題提起）",
  "sections": [
    {{
      "h2": "（セクション見出し）",
      "content": "（300-400文字の本文。具体的な数値や事例を含む）"
    }},
    {{
      "h2": "（セクション見出し）",
      "content": "（300-400文字の本文）"
    }},
    {{
      "h2": "（セクション見出し）",
      "content": "（300-400文字の本文）"
    }}
  ],
  "recommended_services": [
    {{
      "name": "（サービス名）",
      "reason": "（{industry["name"]}にこのサービスが有効な理由、80文字以内）",
      "url": "（サービスURL）"
    }}
  ],
  "faq": [
    {{
      "question": "（{industry["name"]}の経営者が検索しそうな質問）",
      "answer": "（100-150文字の回答）"
    }},
    {{
      "question": "（質問2）",
      "answer": "（回答2）"
    }},
    {{
      "question": "（質問3）",
      "answer": "（回答3）"
    }}
  ],
  "cta_text": "（行動喚起テキスト、40文字以内）"
}}

【重要な注意点】
- {industry["name"]}業界特有の課題や状況に基づいた具体的な内容にすること
- 一般的すぎる文章は避け、{industry["name"]}ならではの視点を入れること
- 数値や具体例を含めて信頼性を高めること
- 自然な日本語で、読みやすく書くこと
- recommended_servicesは最も関連性の高い2-3サービスを選ぶこと
"""

    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            # JSON部分を抽出
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"  [WARN] JSON parse error (attempt {attempt+1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
        except Exception as e:
            print(f"  [ERROR] API call failed (attempt {attempt+1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5)

    return None


# ── オフラインコンテンツ生成 ──────────────────────────────
def generate_content_offline(industry, pattern, services_info):
    """APIなしでテンプレートベースのコンテンツを生成"""
    name = industry["name"]

    # パターン別のコンテンツテンプレート
    content_map = {
        "ai-hp": {
            "meta_description": f"{name}のホームページをAIで簡単作成。テキスト入力だけで10分でプロ品質のHPが完成。初期費用3,980円、月額480円で{name}の集客力を高めるホームページを。",
            "h1": f"{name}のHP作成はAIにおまかせ",
            "intro": f"{name}を経営されている方、「ホームページを作りたいけど、制作会社に依頼すると数十万円かかる」「自分で作る時間がない」とお悩みではありませんか？OnePage-Flashなら、{name}の情報をテキストで入力するだけで、AIが10分でプロ品質のホームページを自動生成します。",
            "sections": [
                {
                    "h2": f"{name}にホームページが必要な理由",
                    "content": f"総務省の調査によると、消費者の約80%がサービスを利用する前にインターネットで検索しています。{name}を探しているお客様も、まずGoogleで「{name} 近く」「{name} おすすめ」と検索するのが一般的です。ホームページがなければ、そうした見込み客との接点を失っていることになります。また、ホームページがあることで予約率の向上、口コミの掲載、スタッフ紹介による安心感の提供など、集客に直結する効果が期待できます。"
                },
                {
                    "h2": f"AI自動生成だから{name}でも手軽にスタート",
                    "content": f"従来のHP制作は、デザイナーへの依頼で30万円以上、制作期間1〜2ヶ月が当たり前でした。OnePage-Flashなら、{name}の基本情報（店名・住所・メニュー・特徴など）をテキストで入力するだけ。AIが{name}に最適なデザインを選び、SEO対策済みのホームページを自動生成します。12種類のテーマプリセットから、{name}の雰囲気に合ったデザインが選べます。"
                },
                {
                    "h2": "料金とはじめ方",
                    "content": f"OnePage-Flashは初期制作費3,980円、月額480円（初月無料）でご利用いただけます。従来のHP制作費用の100分の1以下で、プロ品質のホームページが手に入ります。初月無料なので、まずは試してみて、{name}の集客にどう活かせるか確認してから本契約いただけます。独自ドメインの設定やSSL対応も標準で含まれています。"
                }
            ],
            "faq": [
                {
                    "question": f"{name}のホームページ制作費用の相場はいくらですか？",
                    "answer": f"一般的な制作会社に依頼した場合、{name}のホームページ制作費は15万〜50万円程度が相場です。OnePage-Flashなら初期3,980円＋月額480円で、AIが自動生成するため大幅にコストを抑えられます。"
                },
                {
                    "question": f"パソコンが苦手でも{name}のホームページは作れますか？",
                    "answer": f"はい、OnePage-Flashはテキストを入力するだけでAIが自動生成するので、専門知識は不要です。{name}の基本情報（店名・住所・サービス内容）を入力するだけで、10分程度で完成します。"
                },
                {
                    "question": "スマートフォン対応していますか？",
                    "answer": "はい、OnePage-Flashで生成されるホームページは全てレスポンシブ対応です。スマートフォン、タブレット、PCのどの画面サイズでも最適に表示されます。"
                }
            ],
            "cta_text": f"{name}のホームページ、AIで今すぐ作りませんか？"
        },
        "ai-sns": {
            "meta_description": f"{name}のX(Twitter)運用をAIで完全自動化。HPのURLを登録するだけで毎日2回、年730投稿を自動配信。月額9,800円で{name}のSNS集客を強化。",
            "h1": f"{name}のSNS運用をAIで自動化",
            "intro": f"{name}を運営していて「SNSをやらなきゃと思っているけど、毎日投稿する時間がない」「何を投稿すればいいかわからない」というお悩みはありませんか？バンテックスのX自動投稿サービスなら、{name}のHPのURLを登録するだけで、AIが毎日自動的に投稿を生成・配信します。",
            "sections": [
                {
                    "h2": f"{name}がSNSを活用すべき理由",
                    "content": f"SNSは今や{name}の集客に欠かせないチャネルです。特にX（旧Twitter）は、リアルタイム性が高く、{name}の日々の情報発信や新メニュー・キャンペーンの告知に最適です。フォロワーとの直接的なコミュニケーションを通じて、{name}のファンを増やし、リピーター獲得につなげることができます。実際にSNS経由での来店・問い合わせが売上の20%以上を占める{name}も増えています。"
                },
                {
                    "h2": "AI自動投稿で手間ゼロのSNS運用",
                    "content": f"バンテックスのX自動投稿サービスは、{name}のHPの内容をAIが読み取り、業種に合った投稿文を自動生成します。毎日朝8時と夜20時の2回、自動で投稿。年間730投稿が完全自動で行われるため、スタッフが投稿作業に時間を取られることはありません。投稿内容はAIが{name}の特徴や季節性を考慮して自動生成するため、マンネリ化も防げます。"
                },
                {
                    "h2": "料金と導入の流れ",
                    "content": f"月額9,800円（7日間無料トライアル付き）で、{name}のSNS運用を完全自動化できます。導入は簡単3ステップ：1)アカウント登録、2){name}のHPのURLを入力、3)X連携を許可。これだけで翌日からAIが自動投稿を開始します。7日間の無料トライアルで効果を実感してからご契約いただけます。"
                }
            ],
            "faq": [
                {
                    "question": f"{name}のSNS投稿、何を書けばいいですか？",
                    "answer": f"バンテックスのAI自動投稿なら、{name}のHP情報をもとにAIが自動で投稿文を作成します。新メニュー紹介、季節のおすすめ、お役立ち情報など、{name}に合った内容を自動生成します。"
                },
                {
                    "question": "自動投稿の内容は変更できますか？",
                    "answer": "はい、AIが生成した投稿内容は事前に確認・編集が可能です。完全自動にすることも、承認制にすることもお選びいただけます。"
                },
                {
                    "question": "既存のXアカウントでも使えますか？",
                    "answer": "はい、既存のXアカウントをそのまま連携してお使いいただけます。新規アカウント作成のサポートも行っています。"
                }
            ],
            "cta_text": f"{name}のSNS運用、AIに任せませんか？"
        },
        "ai-shuukyaku": {
            "meta_description": f"{name}の集客にAIを活用。ホームページ作成からSNS運用、顧客対応まで、{name}に最適なAI集客ツールをご提案。名古屋発のAIサービス、バンテックス。",
            "h1": f"{name}の集客をAIで変える",
            "intro": f"「{name}の集客がうまくいかない」「広告費をかけても効果が見えない」「そもそも集客に手が回らない」。多くの{name}経営者が抱えるこの悩み、AIを活用すれば解決できます。バンテックスは{name}の集客に特化したAIサービスを複数提供しています。",
            "sections": [
                {
                    "h2": f"{name}が直面する集客の課題",
                    "content": f"{name}の集客は年々難しくなっています。ポータルサイトの掲載料は高騰し、チラシの反応率は低下。口コミだけに頼る集客には限界があります。一方で、大手チェーンはデジタルマーケティングに投資を増やし、オンラインでの存在感を高めています。個人経営や小規模な{name}が生き残るには、低コストで効率的な集客手段が必要です。AIを活用したデジタル集客が、その答えになります。"
                },
                {
                    "h2": f"{name}におすすめのAI集客ツール",
                    "content": f"バンテックスでは{name}の集客に役立つ複数のAIサービスを提供しています。まずはホームページ。OnePage-Flashならテキスト入力だけで{name}専用のHPを自動生成（初期3,980円）。次にSNS。X自動投稿サービスで毎日2回の自動投稿（月額9,800円）。そしてLINE対応。ココトモカスタマーで24時間AI自動応答。これらを組み合わせることで、{name}の集客を全方位でカバーできます。"
                },
                {
                    "h2": "まずは小さく始めて、効果を実感",
                    "content": f"「いきなり全部は難しい」という{name}経営者の方へ。まずはホームページから始めることをおすすめします。OnePage-Flashは初月無料で試せるので、リスクゼロで始められます。ホームページができたら、次はSNS自動投稿で認知を広げる。集客の土台を固めてから、LINE対応やDMなど次のステップに進む。段階的に導入することで、無理なくAI集客を取り入れられます。"
                }
            ],
            "faq": [
                {
                    "question": f"{name}の集客で最も効果的な方法は？",
                    "answer": f"{name}の集客にはまず「見つけてもらう」ことが大切です。ホームページとSNSの両方を整備し、検索とSNSの両方からお客様が流入する仕組みを作ることが効果的です。"
                },
                {
                    "question": "AIを使った集客にデメリットはありますか？",
                    "answer": "AIは効率的ですが万能ではありません。自動生成コンテンツは定期的に人間が確認し、お店の雰囲気や想いが正しく伝わっているかチェックすることをおすすめします。"
                },
                {
                    "question": f"小さな{name}でもAI集客は効果がありますか？",
                    "answer": f"はい、むしろ小規模な{name}ほどAI集客の恩恵は大きいです。人手をかけずに24時間365日の情報発信・顧客対応が可能になるため、少人数でも大手に負けない集客力を実現できます。"
                }
            ],
            "cta_text": f"{name}の集客、AIで始めませんか？"
        },
        "ai-gyoumu": {
            "meta_description": f"{name}の業務効率化にAIを導入。顧客対応の自動化、SNS運用の自動化、事務作業の削減まで。{name}の生産性を劇的に向上させるAIサービス。",
            "h1": f"{name}の業務をAIで効率化",
            "intro": f"{name}の経営者の多くが「人手が足りない」「事務作業に追われて本業に集中できない」と感じています。AIを導入すれば、顧客対応やSNS投稿、問い合わせ対応といった日常業務を自動化し、本来の業務に集中できる環境を作れます。",
            "sections": [
                {
                    "h2": f"{name}で自動化できる業務とは",
                    "content": f"{name}の日常業務には、AIで自動化できるものが多くあります。例えば、お客様からの問い合わせ対応（営業時間・場所・メニューの案内）、SNSへの投稿作成・配信、予約確認のメッセージ送信などです。これらの業務にスタッフが1日あたり1〜2時間を費やしているとすれば、年間で約360〜720時間もの業務時間を削減できる計算になります。"
                },
                {
                    "h2": "導入しやすいAIツールから始める",
                    "content": f"{name}のAI導入は、使いやすいツールから始めるのが成功のコツです。ココトモカスタマー（LINE×AI）なら、LINEの友達追加だけでAI自動応答が始まります。お客様からの「営業時間は？」「予約できますか？」といった定型的な質問にAIが24時間自動で回答。スタッフの電話対応の負担を大幅に軽減できます。設定も管理画面から簡単に行えます。"
                },
                {
                    "h2": f"AI導入で{name}はこう変わる",
                    "content": f"AIを導入した{name}では、スタッフが接客や技術に集中できるようになったという声が多く聞かれます。問い合わせ対応の自動化で電話が減り、SNS投稿の自動化で情報発信が途切れなくなり、ホームページの自動生成でWeb集客の基盤が整う。これらの変化が積み重なることで、{name}全体の生産性と売上が向上します。"
                }
            ],
            "faq": [
                {
                    "question": f"{name}にAIを導入するメリットは？",
                    "answer": f"人件費の削減、業務時間の短縮、24時間対応の実現が主なメリットです。{name}の規模に関わらず、月額数千円から始められるため、導入のハードルも低いです。"
                },
                {
                    "question": "AI導入にITの専門知識は必要ですか？",
                    "answer": "バンテックスのAIサービスは全て、専門知識なしで利用できるよう設計されています。テキスト入力やURL登録だけで始められるので、パソコンが苦手な方でも安心です。"
                },
                {
                    "question": "どのサービスから始めればいいですか？",
                    "answer": f"{name}の課題に合わせてお選びください。集客強化ならOnePage-Flash（HP作成）、情報発信ならX自動投稿、顧客対応の効率化ならココトモカスタマー（LINE×AI）がおすすめです。"
                }
            ],
            "cta_text": f"{name}の業務、AIでもっとスマートに"
        },
        "ai-kokyaku": {
            "meta_description": f"{name}の顧客対応をLINE×AIで24時間自動化。予約受付、問い合わせ対応、リマインド通知まで。ココトモカスタマーで{name}の顧客満足度を向上。",
            "h1": f"{name}の顧客対応をAIで自動化",
            "intro": f"{name}では「営業時間外の問い合わせに対応できない」「電話対応でスタッフの手が止まる」「予約の取りこぼしがある」といった課題がよく聞かれます。ココトモカスタマーなら、LINEとAIの力で{name}の顧客対応を24時間365日自動化できます。",
            "sections": [
                {
                    "h2": f"{name}の顧客対応の課題",
                    "content": f"{name}では、接客中の電話対応が大きな課題です。施術中や接客中に電話が鳴ると、目の前のお客様へのサービス品質が下がり、電話のお客様も待たされてしまいます。また、営業時間外（夜間・休日）の問い合わせに対応できず、予約の機会損失が発生しています。ある調査では、初回問い合わせから1時間以内に返答がないと、約60%の見込み客が別の{name}に流れるというデータもあります。"
                },
                {
                    "h2": "LINE×AIで実現する24時間自動応答",
                    "content": f"ココトモカスタマーは、{name}のLINE公式アカウントにAI自動応答機能を追加するサービスです。お客様がLINEで友達追加するだけで、AIが自動で対応を開始。「予約したい」「メニューを教えて」「場所はどこ？」といった質問にAIが即座に回答します。複雑な質問や特別な要望があった場合は、スタッフに通知が届くので、必要な場面だけ人間が対応する運用が可能です。"
                },
                {
                    "h2": "導入効果と始め方",
                    "content": f"ココトモカスタマーを導入した{name}では、電話対応の件数が平均40%減少、営業時間外の予約獲得が増加するなどの効果が報告されています。導入は簡単で、LINE公式アカウントがあればすぐに始められます。{name}のよくある質問や基本情報を管理画面に登録するだけで、AIが学習して自動応答を開始します。"
                }
            ],
            "faq": [
                {
                    "question": f"{name}でLINE公式アカウントを持っていないのですが？",
                    "answer": "LINE公式アカウントは無料で開設できます。開設からココトモカスタマーの連携まで、セットアップのサポートも行っていますのでご安心ください。"
                },
                {
                    "question": "AIが間違った回答をしたらどうなりますか？",
                    "answer": f"AIが判断に迷う質問は自動的にスタッフに転送されます。また、{name}の情報を管理画面から更新できるので、回答精度を継続的に改善できます。"
                },
                {
                    "question": "既存のLINE公式アカウントでも使えますか？",
                    "answer": "はい、既存のLINE公式アカウントにそのまま連携できます。これまでの友達リストやトーク履歴に影響はありません。"
                }
            ],
            "cta_text": f"{name}の顧客対応、AIに任せませんか？"
        }
    }

    pattern_slug = pattern["slug"]
    content_template = content_map.get(pattern_slug, content_map["ai-hp"])

    # サービス情報を付与
    recommended = []
    for svc in services_info[:3]:
        recommended.append({
            "name": svc["name"],
            "reason": f"{name}の{'集客' if 'hp' in svc.get('tags', []) or 'sns' in svc.get('tags', []) else '業務効率化'}に活用できます。{svc['price']}から始められます。",
            "url": svc["url"],
        })

    content_template["recommended_services"] = recommended
    return content_template


# ── HTMLページ生成 ────────────────────────────────────────
def render_page(template, industry, pattern, content):
    """テンプレートにコンテンツを埋め込んでHTMLを生成"""
    title = pattern["title_template"].replace("{業種}", industry["name"])
    slug = f"{pattern['slug']}-{to_slug(industry['name'])}"

    # セクションHTML
    sections_html = ""
    for sec in content.get("sections", []):
        paragraphs = sec["content"].split("\n")
        p_html = "".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
        sections_html += f"""
        <section class="seo-section">
          <h2>{sec["h2"]}</h2>
          {p_html}
        </section>"""

    # おすすめサービスHTML
    services_html = ""
    for svc in content.get("recommended_services", []):
        services_html += f"""
          <div class="seo-service-card">
            <h3><a href="{svc["url"]}">{svc["name"]}</a></h3>
            <p>{svc["reason"]}</p>
            <a href="{svc["url"]}" class="seo-service-link">詳しく見る &rarr;</a>
          </div>"""

    # FAQ HTML + JSON-LD
    faq_html = ""
    faq_jsonld_items = []
    for faq in content.get("faq", []):
        faq_html += f"""
          <div class="seo-faq-item">
            <h3 class="seo-faq-q">{faq["question"]}</h3>
            <p class="seo-faq-a">{faq["answer"]}</p>
          </div>"""
        faq_jsonld_items.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"],
            },
        })

    faq_jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_jsonld_items,
        },
        ensure_ascii=False,
        indent=2,
    )

    # Article JSON-LD
    article_jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": content.get("h1", title),
            "description": content.get("meta_description", ""),
            "author": {
                "@type": "Organization",
                "name": "株式会社バンテックス",
                "url": "https://bantex.jp/",
            },
            "publisher": {
                "@type": "Organization",
                "name": "株式会社バンテックス",
                "url": "https://bantex.jp/",
            },
            "datePublished": datetime.now().strftime("%Y-%m-%d"),
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "mainEntityOfPage": f"{BASE_URL}/{slug}.html",
        },
        ensure_ascii=False,
        indent=2,
    )

    # BreadcrumbList JSON-LD
    breadcrumb_jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "トップページ",
                    "item": "https://bantex.jp/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "AIサービス一覧",
                    "item": "https://bantex.jp/ai-services.html",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": title,
                    "item": f"{BASE_URL}/{slug}.html",
                },
            ],
        },
        ensure_ascii=False,
        indent=2,
    )

    # テンプレート変数置換
    html = template
    replacements = {
        "{{TITLE}}": f"{title} | 株式会社バンテックス",
        "{{META_DESCRIPTION}}": content.get("meta_description", ""),
        "{{CANONICAL_URL}}": f"{BASE_URL}/{slug}.html",
        "{{OG_TITLE}}": title,
        "{{H1}}": content.get("h1", title),
        "{{INTRO}}": content.get("intro", ""),
        "{{SECTIONS}}": sections_html,
        "{{SERVICES}}": services_html,
        "{{FAQ}}": faq_html,
        "{{FAQ_JSONLD}}": faq_jsonld,
        "{{ARTICLE_JSONLD}}": article_jsonld,
        "{{BREADCRUMB_JSONLD}}": breadcrumb_jsonld,
        "{{CTA_TEXT}}": content.get("cta_text", "まずは無料で相談する"),
        "{{INDUSTRY_NAME}}": industry["name"],
        "{{PATTERN_LABEL}}": pattern["label"],
        "{{YEAR}}": str(datetime.now().year),
    }

    for key, value in replacements.items():
        html = html.replace(key, value)

    return html, slug


# ── sitemap.xml 更新 ──────────────────────────────────────
def update_sitemap(generated_pages):
    """生成したページをsitemap.xmlに追加"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 既存のsitemap読み込み
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 既存URLを保持
    existing = content.split("</urlset>")[0]

    # 新規ページ追加
    new_entries = ""
    for page in generated_pages:
        url = f"{BASE_URL}/{page['slug']}.html"
        if url not in existing:
            new_entries += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
"""

    if new_entries:
        updated = existing + new_entries + "</urlset>\n"
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"\n[OK] sitemap.xml updated: {len(generated_pages)} pages added")
    else:
        print("\n[INFO] sitemap.xml: no new pages to add")


# ── メイン処理 ────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="bantex.jp Programmatic SEO Generator")
    parser.add_argument("--dry-run", action="store_true", help="生成対象の一覧表示のみ")
    parser.add_argument("--limit", type=int, default=0, help="生成ページ数の上限")
    parser.add_argument("--pattern", type=str, default="", help="特定パターンのみ (slugで指定)")
    parser.add_argument("--industry", type=str, default="", help="特定業種のみ")
    parser.add_argument("--no-sitemap", action="store_true", help="sitemap更新をスキップ")
    parser.add_argument("--offline", action="store_true", help="API不要のテンプレートベース生成")
    args = parser.parse_args()

    # データ読み込み
    data = load_data()
    industries = data["industries"]
    patterns = data["patterns"]
    services = data["services"]

    # フィルタリング
    if args.pattern:
        patterns = [p for p in patterns if p["slug"] == args.pattern]
    if args.industry:
        industries = [i for i in industries if args.industry in i["name"]]

    # 生成対象一覧
    targets = []
    for pattern in patterns:
        for industry in industries:
            slug = f"{pattern['slug']}-{to_slug(industry['name'])}"
            title = pattern["title_template"].replace("{業種}", industry["name"])
            targets.append({
                "slug": slug,
                "title": title,
                "pattern": pattern,
                "industry": industry,
            })

    if args.limit > 0:
        targets = targets[: args.limit]

    print(f"=== bantex.jp Programmatic SEO Generator ===")
    print(f"Total pages to generate: {len(targets)}")
    print(f"Patterns: {len(patterns)} | Industries: {len(industries)}")
    print()

    if args.dry_run:
        for t in targets:
            print(f"  {t['slug']}.html - {t['title']}")
        return

    # API key チェック（offlineモード以外）
    if not args.offline and not ANTHROPIC_API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY not set. Use --offline or export it:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    # テンプレート読み込み
    template = load_template()

    # 出力ディレクトリ作成
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 生成ループ
    generated = []
    for i, target in enumerate(targets):
        slug = target["slug"]
        output_file = OUTPUT_DIR / f"{slug}.html"

        # スキップ（既存ファイル）
        if output_file.exists():
            print(f"[{i+1}/{len(targets)}] SKIP (exists): {slug}")
            generated.append({"slug": slug})
            continue

        print(f"[{i+1}/{len(targets)}] Generating: {slug}...")

        # 関連サービス情報
        relevant_services = []
        for svc in services:
            if any(tag in target["industry"].get("relevant_services", []) for tag in svc.get("tags", [])):
                relevant_services.append(svc)
        if not relevant_services:
            relevant_services = services[:3]  # デフォルトで上位3つ

        # コンテンツ生成
        if args.offline:
            content = generate_content_offline(
                target["industry"],
                target["pattern"],
                relevant_services,
            )
        else:
            content = generate_content(
                target["industry"],
                target["pattern"],
                relevant_services,
            )

        if content is None:
            print(f"  [FAIL] Could not generate content for {slug}")
            continue

        # HTMLレンダリング
        html, _ = render_page(template, target["industry"], target["pattern"], content)

        # ファイル書き出し
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        generated.append({"slug": slug})
        print(f"  [OK] {output_file.name} ({len(html):,} bytes)")

        # レートリミット対策
        time.sleep(RATE_LIMIT_DELAY)

    # sitemap更新
    if not args.no_sitemap and generated:
        update_sitemap(generated)

    print(f"\n=== Complete: {len(generated)}/{len(targets)} pages generated ===")


if __name__ == "__main__":
    main()
