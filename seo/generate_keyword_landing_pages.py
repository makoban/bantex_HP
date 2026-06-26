"""
Generate BANTEX service-keyword landing pages.

These pages target general service terms that are too broad for the existing
industry-specific programmatic SEO pages. The generator is deterministic and
does not call external APIs.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "seo" / "services"
SITEMAP_PATH = ROOT / "sitemap.xml"
TODAY = "2026-06-27"
BASE_URL = "https://bantex.jp/seo/services"


PAGES = [
    {
        "slug": "ai-automation-nagoya",
        "title": "AI自動化 名古屋 | 業務自動化・AI導入支援 | 株式会社バンテックス",
        "h1": "名古屋のAI自動化・業務自動化",
        "description": "名古屋でAI自動化・業務自動化を相談するなら株式会社バンテックス。問い合わせ対応、SNS投稿、フォーム営業、社内確認など、AIを実務に合わせて導入します。",
        "keywords": "AI自動化,AI自動化 名古屋,業務自動化,AI導入支援,AIフォーム営業,SNS自動化,名古屋 AI",
        "label": "AI Automation",
        "lead": "AIツールを入れるだけでは、現場の仕事は自動化されません。株式会社バンテックスは名古屋を拠点に、問い合わせ、発信、営業、分析、社内確認といった日常業務を、会社ごとの運用に合わせてAI化します。",
        "summary": [
            "名古屋・愛知の中小企業向けに、AIを使った業務自動化の設計から運用まで相談できます。",
            "既存のホームページ、LINE、SNS、問い合わせフォーム、社内資料など、すでにある業務資産を活かして小さく始めます。",
            "AI社員、AIフォーム営業、SNS自動投稿、LINE自動応答、商圏分析など、単体サービスではなく業務の流れとして組み合わせます。",
        ],
        "sections": [
            {
                "heading": "AI自動化で最初に見るべき業務",
                "body": "AI自動化は、いきなり全社システムを置き換えるより、繰り返し発生している作業から始める方が効果を確認しやすくなります。たとえば、問い合わせへの一次回答、SNS投稿文の作成、営業先の下調べ、フォーム送信前の文面作成、社内資料からの確認、定型レポート作成などです。BANTEXでは、毎日または毎週発生している作業を洗い出し、人が判断すべき部分とAIに任せられる部分を分けて設計します。",
            },
            {
                "heading": "名古屋の会社に合わせた導入設計",
                "body": "名古屋・愛知の企業では、少人数で営業、制作、現場対応、事務作業を兼ねているケースが多くあります。そのため、AI自動化は大規模な開発よりも、今使っているWebサイト、LINE、Googleスプレッドシート、SNS、メール運用に接続する形が現実的です。株式会社バンテックスは、現場で無理なく続くことを重視し、試験運用、確認画面、人の承認、記録保存まで含めて設計します。",
            },
            {
                "heading": "相談できるAI自動化の例",
                "body": "BANTEXでは、AIフォーム営業、X自動投稿、LINEとInstagramの投稿自動化、公募・入札案件の自動抽出、商圏分析レポート、AI映像制作、AIホームページ生成などを提供しています。単発のツール導入ではなく、問い合わせを増やす、発信を継続する、営業の下準備を減らす、資料作成を短縮するなど、経営上の目的に合わせて組み合わせます。",
            },
            {
                "heading": "進め方",
                "body": "まずは現在の業務と、AI化したい作業の頻度を確認します。次に、AIで自動化する範囲、人が確認する範囲、失敗時の戻し方を決めます。そのうえで、小さなテスト運用を行い、回答品質や作業時間の削減効果を見てから本運用へ進めます。検索順位を狙うSEOのように、AI自動化も一度作って終わりではなく、運用データを見ながら改善していく形が現実的です。",
            },
        ],
        "fit": [
            "問い合わせやSNS投稿が止まりがちな会社",
            "営業リスト作成やフォーム営業の下準備を減らしたい会社",
            "AIツールを試したが、社内業務に定着しなかった会社",
            "名古屋・愛知で近くの会社に相談しながら進めたい会社",
        ],
        "links": [
            ("AIサービス一覧", "https://bantex.jp/ai-services.html"),
            ("AI社員 名古屋", "https://bantex.jp/seo/services/ai-staff-nagoya.html"),
            ("AI映像制作 名古屋", "https://bantex.jp/seo/services/ai-video-nagoya.html"),
            ("インスタ 自動投稿", "https://bantex.jp/seo/services/instagram-auto-posting.html"),
            ("AIフォーム営業", "https://ai-form.bantex.jp/"),
            ("X AI自動投稿", "https://tweet.bantex.jp/"),
        ],
        "faqs": [
            ("AI自動化は何から始めるのがよいですか？", "毎日または毎週発生する定型作業から始めるのが現実的です。問い合わせ一次回答、投稿作成、営業文面作成、資料要約などは効果を確認しやすい領域です。"),
            ("名古屋以外の会社でも相談できますか？", "はい。BANTEXは名古屋市天白区を拠点にしていますが、AIサービスの相談と運用は全国対応できます。対面相談が必要な場合は名古屋・愛知近郊が対応しやすいです。"),
            ("AI導入には大きな開発費が必要ですか？", "必ずしも必要ではありません。既存サービスや小さな自動化から始め、効果が見えた部分だけ追加開発する方が、初期費用と失敗リスクを抑えられます。"),
        ],
        "service_type": "AI導入支援",
    },
    {
        "slug": "ai-staff-nagoya",
        "title": "AI社員 名古屋 | 会社専用AI社員・AIエージェント | 株式会社バンテックス",
        "h1": "名古屋で会社専用のAI社員を作る",
        "description": "名古屋でAI社員・AIエージェントの導入を相談するなら株式会社バンテックス。問い合わせ対応、社内確認、発信、営業補助など会社専用のAI社員を設計します。",
        "keywords": "AI社員,AI社員 名古屋,AIエージェント,AI社員サービス,会社専用AI,業務自動化,名古屋",
        "label": "AI Staff",
        "lead": "AI社員は、汎用チャットボットではなく、会社の情報、商品、業務ルール、対応方針を理解して働くAIの担当者です。BANTEXは、名古屋の中小企業でも導入しやすい形で、会社専用AI社員の設計と運用を支援します。",
        "summary": [
            "会社の資料、ホームページ、よくある質問、営業方針をもとに、AI社員の役割を設計します。",
            "問い合わせ対応、社内確認、営業文面作成、SNS投稿、資料要約など、1つの役割から始められます。",
            "完全自動だけでなく、人の確認を挟む運用や、回答できない時の引き継ぎも設計します。",
        ],
        "sections": [
            {
                "heading": "AI社員と通常のチャットAIの違い",
                "body": "通常のチャットAIは、質問に答えることはできますが、会社ごとの商品、料金、対応範囲、営業方針を理解しているわけではありません。AI社員は、会社専用の情報と運用ルールを持たせ、特定の役割を担当させる考え方です。たとえば、問い合わせ担当、SNS担当、営業準備担当、社内FAQ担当など、業務上の役割を決めることで、現場で使いやすくなります。",
            },
            {
                "heading": "AI社員が担当できる仕事",
                "body": "AI社員は、問い合わせの一次回答、社内マニュアルの検索、商談前の下調べ、SNS投稿案の作成、営業メールの下書き、フォーム営業の文面作成、顧客からの質問整理などに向いています。重要なのは、AIに何でも任せることではなく、得意な仕事を明確にすることです。BANTEXでは、業務の中でAIに任せる部分、人が確認する部分、記録として残す部分を分けて設計します。",
            },
            {
                "heading": "中小企業で導入しやすい理由",
                "body": "AI社員は、大企業だけの仕組みではありません。むしろ、少人数で複数の仕事を抱える中小企業ほど、定型確認や発信作業をAIに任せるメリットがあります。BANTEXでは、既存のホームページや資料を活用し、最初から大きなシステムを作らず、必要な役割を一つずつ増やす進め方を推奨しています。",
            },
            {
                "heading": "導入後の改善",
                "body": "AI社員は作って終わりではありません。実際の質問、回答ミス、足りなかった社内情報を確認しながら、回答範囲や文体、参照資料を調整します。特に問い合わせ対応や営業補助では、会社らしい言い回し、断るべき条件、確認が必要な条件を更新していくことで、より現場に合ったAI社員に育てられます。",
            },
        ],
        "fit": [
            "問い合わせや社内確認を人に集中させたくない会社",
            "AIを使いたいが、何を任せるべきか整理できていない会社",
            "営業やSNS発信の下書きを継続的に作りたい会社",
            "名古屋・愛知でAI社員の導入相談先を探している会社",
        ],
        "links": [
            ("AI社員サービス", "https://koala.bantex.jp/"),
            ("AI自動化 名古屋", "https://bantex.jp/seo/services/ai-automation-nagoya.html"),
            ("AI映像制作 名古屋", "https://bantex.jp/seo/services/ai-video-nagoya.html"),
            ("インスタ 自動投稿", "https://bantex.jp/seo/services/instagram-auto-posting.html"),
            ("AIサービス一覧", "https://bantex.jp/ai-services.html"),
            ("お問い合わせ", "https://bantex.jp/#contact"),
        ],
        "faqs": [
            ("AI社員は人間の社員の代わりになりますか？", "すべてを代替するものではありません。定型的な確認、下書き、一次対応を任せ、人が判断すべき部分に時間を戻すための仕組みです。"),
            ("会社の情報をどこまで覚えさせられますか？", "ホームページ、サービス資料、FAQ、営業ルール、対応方針などをもとに設計できます。機密性が高い情報は扱い方を分けて検討します。"),
            ("小さな会社でもAI社員を導入できますか？", "はい。最初は社内FAQ担当や問い合わせ一次対応など、1つの役割から始めることで、小規模な会社でも導入しやすくなります。"),
        ],
        "service_type": "AI社員サービス",
    },
    {
        "slug": "ai-video-nagoya",
        "title": "AI映像制作 名古屋 | AI動画・CM・SNS動画制作 | 株式会社バンテックス",
        "h1": "名古屋のAI映像制作・AI動画制作",
        "description": "名古屋でAI映像制作・AI動画制作を相談するなら株式会社バンテックス。CM、SNS動画、企業PV、LP用動画などをAI活用で短期間・低コストに制作します。",
        "keywords": "AI映像制作,AI映像 名古屋,名古屋 AI映像,AI動画制作 名古屋,AI動画,AI CM制作,SNS動画制作,企業PV 名古屋",
        "label": "AI Video",
        "lead": "AI映像制作は、撮影、モデル、スタジオを毎回用意しなくても、商品やサービスの魅力を動画で伝えやすくする制作手法です。BANTEXは名古屋を拠点に、AI動画、CM、SNS動画、LP用ビジュアルの制作を支援します。",
        "summary": [
            "名古屋・愛知の会社や店舗向けに、広告、SNS、LP、営業資料で使えるAI映像を制作します。",
            "画像1枚、商品写真、店舗写真、テキスト指示から、短尺動画や告知用ビジュアルを作れます。",
            "AI生成だけで終わらせず、日本語テロップ、ロゴ、構成、投稿導線まで編集レイヤーで整えます。",
        ],
        "sections": [
            {
                "heading": "AI映像制作で作れるもの",
                "body": "AI映像制作では、SNS広告、Instagramリール、YouTubeショート、店頭サイネージ用動画、LPのファーストビュー動画、企業PVの短尺版、サービス紹介動画などを作れます。従来の撮影では日程、出演者、ロケーション、スタジオ、編集の調整が必要でしたが、AIを使うことで企画から初稿までの時間を短縮できます。BANTEXでは、AI生成と編集を分け、最後に日本語テロップやロゴ、尺、画角を整えます。",
            },
            {
                "heading": "名古屋の店舗・企業での使い方",
                "body": "名古屋の店舗では、メニュー紹介、キャンペーン、求人、イベント告知、店頭サイネージ用の映像に活用できます。企業では、新サービス説明、展示会用動画、営業資料の冒頭動画、採用向けの短尺動画に使えます。AI映像は、毎回大規模な撮影を行うほどではないが、写真だけでは伝わりにくい内容を動きで見せたい場合に向いています。",
            },
            {
                "heading": "BANTEXの制作範囲",
                "body": "BANTEXでは、AI生成用の構成案、プロンプト設計、素材整理、映像生成、不要な文字や崩れの確認、日本語テロップ追加、ロゴ配置、SNS向け画角調整まで相談できます。必要に応じて、LP、Instagram投稿文、サイネージ表示、LINE配信用の案内文まで一緒に整えます。動画単体ではなく、見た人が問い合わせや来店につながる導線を重視します。",
            },
            {
                "heading": "制作前に準備するもの",
                "body": "制作前には、目的、使う場所、尺、縦型か横型か、入れたい文言、ロゴ、商品写真、店舗写真、参考イメージを整理します。素材が少ない場合でも制作はできますが、実際の商品や店舗の写真があるほど、伝えたい内容に近づけやすくなります。BANTEXでは、素材が十分でない場合も、最初に必要な内容を整理してから制作に進めます。",
            },
        ],
        "fit": [
            "名古屋・愛知でAI動画やAI映像制作を相談したい会社",
            "InstagramやYouTubeショート向けの短尺動画を作りたい店舗",
            "LPや広告に使う動画を短期間で用意したい事業者",
            "撮影予算を抑えつつ、動きのある訴求を試したい会社",
        ],
        "links": [
            ("AI映像制作サービス", "https://aimovie.bantex.jp/"),
            ("AI自動化 名古屋", "https://bantex.jp/seo/services/ai-automation-nagoya.html"),
            ("インスタ 自動投稿", "https://bantex.jp/seo/services/instagram-auto-posting.html"),
            ("AIサービス一覧", "https://bantex.jp/ai-services.html"),
        ],
        "faqs": [
            ("AI映像制作では何秒くらいの動画を作れますか？", "SNSや広告では15秒から30秒程度の短尺動画が使いやすいです。LPや企業PVでは用途に合わせて尺を調整します。"),
            ("名古屋以外でもAI映像制作を依頼できますか？", "はい。BANTEXは名古屋市天白区を拠点にしていますが、素材共有とオンライン確認で全国対応できます。"),
            ("AIで生成した動画に日本語テロップやロゴは入れられますか？", "はい。AI生成映像そのものに任せず、編集工程で日本語テロップ、ロゴ、問い合わせ導線、SNS用の画角を整えます。"),
        ],
        "service_type": "AI映像制作",
    },
    {
        "slug": "instagram-auto-posting",
        "title": "インスタ 自動投稿 | Instagram自動投稿・LINE連携 | 株式会社バンテックス",
        "h1": "インスタ自動投稿・Instagram投稿自動化",
        "description": "インスタ自動投稿・Instagram投稿自動化なら株式会社バンテックス。LINEで写真を送るだけで、AIが投稿文とハッシュタグを作り、Instagramへ予約投稿します。",
        "keywords": "インスタ 自動投稿,Instagram自動投稿,インスタ 投稿 自動化,Instagram 投稿 自動化,LINE Instagram投稿,SNS自動化,店舗SNS運用,名古屋 インスタ 自動投稿",
        "label": "Instagram Auto",
        "lead": "インスタ運用は大切でも、写真選び、文章作成、ハッシュタグ、投稿時間の管理を毎日続けるのは負担です。BANTEXのココトモSNSは、LINEで写真を送るだけでInstagram投稿までつなげる店舗向けの自動投稿サービスです。",
        "summary": [
            "LINEで写真を送るだけで、AIがInstagram向けの投稿文とハッシュタグを作ります。",
            "決めた時間に予約投稿できるため、店舗スタッフが毎日投稿作業を抱えにくくなります。",
            "飲食店、美容室、サロン、整体院など、写真で魅力を伝える店舗の継続投稿に向いています。",
        ],
        "sections": [
            {
                "heading": "インスタ投稿が続かない理由",
                "body": "店舗のInstagram運用では、写真はあるのに投稿文が浮かばない、ハッシュタグを考える時間がない、忙しい時間に投稿できない、担当者が変わると止まるといった課題がよくあります。インスタ自動投稿は、投稿作業の中でも負担になりやすい文章作成、ハッシュタグ作成、予約投稿を仕組み化し、投稿の継続を助けます。",
            },
            {
                "heading": "LINEからInstagramへつなげる仕組み",
                "body": "ココトモSNSでは、店舗スタッフがLINEで写真やメモを送ると、AIが内容を読み取り、Instagram向けの投稿文とハッシュタグ案を作成します。投稿時間をあらかじめ設定しておけば、決めた時間にInstagramへ投稿できます。普段から使っているLINEを入口にすることで、管理画面に毎回ログインする負担を減らせます。",
            },
            {
                "heading": "店舗SNS運用での使い方",
                "body": "飲食店では日替わりメニューや新商品、美容室やサロンでは施術事例や空き枠案内、整体院やクリニックではお知らせや季節の注意喚起などに使えます。投稿文をAIが作ることで、文章が苦手なスタッフでも発信しやすくなります。BANTEXでは、店舗ごとの言い回しや投稿ルールに合わせた運用も相談できます。",
            },
            {
                "heading": "自動投稿で注意すること",
                "body": "Instagram自動投稿は便利ですが、すべてを完全放置にするより、投稿前確認や投稿ルールを決める方が安全です。写真に写ってはいけないもの、価格表記、医療・美容系の表現、キャンペーン条件などは人の確認が必要になる場合があります。BANTEXでは、自動化する部分と人が見る部分を分けて設計します。",
            },
        ],
        "fit": [
            "Instagram投稿が止まりがちな飲食店・美容室・サロン",
            "LINEから写真を送るだけで投稿準備を済ませたい店舗",
            "投稿文やハッシュタグを考える時間を減らしたい事業者",
            "名古屋・愛知で店舗SNS運用を相談したい会社",
        ],
        "links": [
            ("ココトモSNS", "https://kokotomo-sns.bantex.jp/"),
            ("AI映像制作 名古屋", "https://bantex.jp/seo/services/ai-video-nagoya.html"),
            ("AI自動化 名古屋", "https://bantex.jp/seo/services/ai-automation-nagoya.html"),
            ("AIサービス一覧", "https://bantex.jp/ai-services.html"),
        ],
        "faqs": [
            ("インスタ自動投稿は何が自動になりますか？", "写真やメモをもとにした投稿文作成、ハッシュタグ作成、予約投稿を自動化できます。運用により投稿前確認を挟むこともできます。"),
            ("LINEからInstagramに投稿できますか？", "はい。ココトモSNSでは、LINEで写真を送る運用を入口にして、AIが投稿文を作りInstagram投稿につなげます。"),
            ("店舗ごとの文章の雰囲気は調整できますか？", "はい。丁寧、親しみやすい、短め、絵文字控えめなど、店舗の雰囲気に合わせた投稿ルールを相談できます。"),
        ],
        "service_type": "Instagram自動投稿",
    },
    {
        "slug": "small-digital-signage",
        "title": "小型デジタルサイネージ | 店舗・施設向け省スペース表示 | 株式会社バンテックス",
        "h1": "小型デジタルサイネージの相談",
        "description": "小型デジタルサイネージの導入相談なら株式会社バンテックス。店舗、受付、施設、ショールーム向けに、省スペースで使えるサイネージの企画・制作・導入を支援します。",
        "keywords": "小型デジタルサイネージ,デジタルサイネージ 小型,店舗サイネージ,サイネージ 導入,名古屋 デジタルサイネージ",
        "label": "Small Signage",
        "lead": "小型デジタルサイネージは、限られたスペースでも商品案内、受付案内、キャンペーン告知、施設案内を更新しやすい表示手段です。BANTEXは、設置場所と見せたい情報に合わせて、機器選定とコンテンツ制作を相談できます。",
        "summary": [
            "店舗の棚横、受付カウンター、待合スペース、展示台、イベント什器など、省スペースで使う表示に向いています。",
            "印刷物と違い、季節、時間帯、キャンペーン、在庫状況に合わせて表示内容を変えられます。",
            "機器だけでなく、実際に表示する画像、動画、導線、QRコード連携までまとめて設計できます。",
        ],
        "sections": [
            {
                "heading": "小型サイネージが向いている場所",
                "body": "小型デジタルサイネージは、大型ビジョンを置けない場所でも使えるのが強みです。レジ横、受付、商品棚、待合室、ショールーム、展示会ブースなど、近距離で情報を見てもらう場面に向いています。紙のPOPでは更新が手間になる情報も、画面表示なら差し替えやすく、複数の案内を順番に見せることができます。",
            },
            {
                "heading": "表示内容まで含めた導入",
                "body": "サイネージは機器を置くだけでは効果が出ません。誰が、どの距離で、何秒見るのかを考え、文字量、写真、動画、QRコード、問い合わせ導線を設計する必要があります。BANTEXでは、AI映像制作やLP制作の知見も活かし、機器選定だけでなく、表示コンテンツの企画・制作まで相談できます。",
            },
            {
                "heading": "店舗での使い方",
                "body": "飲食店ではメニュー、限定商品、LINE登録、Instagram誘導に使えます。美容室やサロンでは施術メニュー、キャンペーン、予約導線を表示できます。クリニックや施設では受付案内、注意事項、待ち時間の案内、フロア誘導に使えます。小型だからこそ、来店者の目に入りやすい位置に置けることが重要です。",
            },
            {
                "heading": "導入前に確認すること",
                "body": "設置場所の電源、視認距離、明るさ、固定方法、更新頻度、誰が表示内容を更新するかを確認します。屋内か屋外か、常時点灯か営業時間だけかによって、適した機器も変わります。BANTEXでは、導入目的を確認したうえで、必要なサイズ、表示内容、運用方法を整理します。",
            },
        ],
        "fit": [
            "紙POPの貼り替えが多い店舗",
            "受付や待合で案内を分かりやすく見せたい施設",
            "商品やサービスの説明を映像で見せたい会社",
            "小さなスペースでデジタル表示を試したい店舗",
        ],
        "links": [
            ("Vision Creative", "https://visioncreative.bantex.jp/"),
            ("K-SLIM", "https://kslim.bantex.jp/"),
            ("デジタルサイネージ 名古屋", "https://bantex.jp/seo/services/digital-signage-nagoya.html"),
            ("床面LEDサイネージ", "https://bantex.jp/seo/services/floor-led-signage.html"),
        ],
        "faqs": [
            ("小型デジタルサイネージはどこに置けますか？", "店舗のレジ横、受付、商品棚、待合室、展示台、ショールームなど、近距離で案内を見せたい場所に向いています。"),
            ("表示する動画や画像も相談できますか？", "はい。BANTEXでは、サイネージ本体だけでなく、表示する画像、動画、案内文、QRコード導線の制作も相談できます。"),
            ("屋外でも使えますか？", "屋外利用は明るさ、防水、防塵、固定方法の確認が必要です。設置環境に合わせて、屋外向け機器や別シリーズを検討します。"),
        ],
        "service_type": "デジタルサイネージ",
    },
    {
        "slug": "digital-signage-nagoya",
        "title": "デジタルサイネージ 名古屋 | 店舗・施設サイネージ導入相談 | 株式会社バンテックス",
        "h1": "名古屋のデジタルサイネージ導入相談",
        "description": "名古屋でデジタルサイネージを導入するなら株式会社バンテックス。店舗、施設、屋外、床面LEDまで、機器選定・コンテンツ制作・導入相談に対応します。",
        "keywords": "デジタルサイネージ 名古屋,名古屋 デジタルサイネージ,店舗サイネージ,小型デジタルサイネージ,床面LEDサイネージ",
        "label": "Nagoya Signage",
        "lead": "デジタルサイネージは、単なる画面ではなく、来店者や施設利用者に情報を届ける接点です。BANTEXは名古屋を拠点に、店舗、施設、オフィス、イベント、屋外表示まで、目的に合わせたサイネージ導入を支援します。",
        "summary": [
            "名古屋・愛知の店舗、施設、企業向けにデジタルサイネージの相談ができます。",
            "小型サイネージ、屋外LED、床面LED、受付案内、販促表示など目的別に整理します。",
            "機器販売だけでなく、表示するコンテンツ、更新運用、LPやSNSへの導線も含めて設計します。",
        ],
        "sections": [
            {
                "heading": "名古屋でサイネージを導入する時の考え方",
                "body": "名古屋の店舗や施設では、通行量、車移動、商業施設内の視認距離、営業時間、近隣競合などによって適したサイネージが変わります。入口で目を止めたいのか、店内で商品理解を深めたいのか、待ち時間に案内したいのかを決めることが重要です。BANTEXでは、設置場所と目的から逆算して、画面サイズ、明るさ、表示内容、更新方法を整理します。",
            },
            {
                "heading": "店舗サイネージの使い方",
                "body": "店舗では、キャンペーン、メニュー、LINE登録、予約案内、Instagram誘導、商品紹介などに使えます。紙のポスターと違い、時間帯や曜日で内容を変えられるため、ランチ、夕方、週末、イベント時で訴求を切り替えられます。小型サイネージと屋外表示を組み合わせることで、店外の集客と店内の案内を分けて設計できます。",
            },
            {
                "heading": "施設・オフィスでの使い方",
                "body": "施設やオフィスでは、受付案内、フロア案内、注意事項、社内広報、来客向け説明、展示紹介などに活用できます。来訪者が迷いやすい場所や、同じ説明を何度もしている場所ほどサイネージの効果が出やすくなります。必要に応じて、動画、静止画、QRコード、Webページへの誘導を組み合わせます。",
            },
            {
                "heading": "導入と運用",
                "body": "サイネージ導入では、設置後に誰が更新するかも重要です。更新頻度が高い場合は、差し替えしやすい構成にします。更新頻度が低い場合は、長く使える案内と季節差し替えを分けます。BANTEXでは、導入時の見た目だけでなく、運用を続けられる構成まで含めて相談できます。",
            },
        ],
        "fit": [
            "名古屋・愛知で店舗サイネージを導入したい店舗",
            "施設案内や受付案内を分かりやすくしたい企業",
            "屋外LEDや小型サイネージを比較したい会社",
            "映像やLP制作までまとめて相談したい事業者",
        ],
        "links": [
            ("小型デジタルサイネージ", "https://bantex.jp/seo/services/small-digital-signage.html"),
            ("床面LEDサイネージ", "https://bantex.jp/seo/services/floor-led-signage.html"),
            ("Vision Creative", "https://visioncreative.bantex.jp/"),
            ("お問い合わせ", "https://bantex.jp/#contact"),
        ],
        "faqs": [
            ("名古屋でデジタルサイネージの相談はできますか？", "はい。BANTEXは名古屋市天白区を拠点に、店舗、施設、企業向けのデジタルサイネージ導入相談に対応しています。"),
            ("サイネージのコンテンツ制作も依頼できますか？", "はい。表示する静止画、動画、案内文、QRコード導線、LPやSNSへの誘導まで含めて相談できます。"),
            ("小型と屋外LEDのどちらがよいですか？", "設置場所、視認距離、明るさ、目的で変わります。店内や受付は小型、店外や遠距離訴求は屋外LEDが候補になります。"),
        ],
        "service_type": "デジタルサイネージ導入支援",
    },
    {
        "slug": "floor-led-signage",
        "title": "床面LEDサイネージ | 防災誘導・施設案内・空間演出 | 株式会社バンテックス",
        "h1": "床面LEDサイネージの導入相談",
        "description": "床面LEDサイネージの導入相談なら株式会社バンテックス。平常時の空間演出から非常時の防災誘導まで、施設・店舗向けの表示導線を企画します。",
        "keywords": "床面LEDサイネージ,床面LED,防災誘導サイネージ,デジタルサイネージ 名古屋,Vision Yuka",
        "label": "Floor LED",
        "lead": "床面LEDサイネージは、壁面や天井ではなく、歩く人の視線と動線に近い床面へ情報を出す表示手段です。施設案内、空間演出、防災誘導など、通常のサイネージとは違う役割で使えます。",
        "summary": [
            "床面に光の案内を出すことで、歩行導線に沿った誘導や注意喚起ができます。",
            "平常時は演出や案内、非常時は避難誘導など、用途を切り替える設計が可能です。",
            "Vision Yukaを中心に、施設の動線、設置場所、表示内容を合わせて検討します。",
        ],
        "sections": [
            {
                "heading": "床面LEDサイネージの特徴",
                "body": "床面LEDサイネージは、通路、エントランス、ホール、展示施設、商業施設など、人が歩く場所に近い位置で情報を見せられます。壁面表示と違い、足元の動線と連動しやすいため、進行方向、注意喚起、エリア分け、イベント演出に向いています。通常の看板では見落とされやすい案内も、床面の光によって気づきやすくなります。",
            },
            {
                "heading": "防災誘導での活用",
                "body": "非常時は、壁面サインやアナウンスだけでは十分に伝わらない場面があります。床面LEDを使うことで、進む方向、注意エリア、避難経路を視覚的に示しやすくなります。平常時は施設案内や空間演出として使い、非常時は防災誘導に切り替える考え方ができます。施設の安全計画と合わせて設計することが大切です。",
            },
            {
                "heading": "施設・店舗での使い方",
                "body": "商業施設ではイベント演出、フロア誘導、混雑時の動線整理に使えます。展示施設では来場者の進行方向や展示テーマの演出に使えます。オフィスや公共施設では受付から目的地までの案内、注意喚起、避難導線の補助に活用できます。BANTEXでは、設置場所の床材、通行量、明るさ、表示目的を確認して導入を検討します。",
            },
            {
                "heading": "導入前の確認事項",
                "body": "床面LEDは、耐久性、歩行安全、視認性、電源、メンテナンス、清掃導線の確認が必要です。また、どの時間帯に何を表示するか、非常時にどのように切り替えるかも重要です。単に光る床を入れるのではなく、施設の動線計画と合わせて設計することで、実用性のあるサイネージになります。",
            },
        ],
        "fit": [
            "施設の案内や避難導線を分かりやすくしたい事業者",
            "イベントや展示で床面演出を使いたい施設",
            "通常時と非常時で表示用途を切り替えたい施設",
            "Vision Yukaの導入相談をしたい会社",
        ],
        "links": [
            ("Vision Yuka", "https://vision-yuka.bantex.jp/"),
            ("デジタルサイネージ 名古屋", "https://bantex.jp/seo/services/digital-signage-nagoya.html"),
            ("小型デジタルサイネージ", "https://bantex.jp/seo/services/small-digital-signage.html"),
            ("お問い合わせ", "https://bantex.jp/#contact"),
        ],
        "faqs": [
            ("床面LEDサイネージは何に使えますか？", "施設案内、イベント演出、注意喚起、防災誘導、避難経路の補助など、歩行導線に合わせた表示に使えます。"),
            ("通常時と災害時で表示を変えられますか？", "運用設計により、平常時は案内や演出、非常時は避難誘導として使う考え方ができます。施設の安全計画と合わせた検討が必要です。"),
            ("導入前に何を確認すべきですか？", "床材、通行量、明るさ、電源、清掃、耐久性、安全性、非常時の切り替え方法を確認します。"),
        ],
        "service_type": "床面LEDサイネージ",
    },
    {
        "slug": "pipe-bender-nagoya",
        "title": "パイプベンダー 名古屋 | パイプ曲げ加工機・産業機械相談 | 株式会社バンテックス",
        "h1": "名古屋のパイプベンダー導入相談",
        "description": "名古屋でパイプベンダー・パイプ曲げ加工機を相談するなら株式会社バンテックス。製造現場の加工条件、機種選定、導入相談に対応します。",
        "keywords": "パイプベンダー,パイプベンダー 名古屋,パイプ曲げ加工機,パイプ加工,産業機械,工作機械 名古屋",
        "label": "Pipe Bender",
        "lead": "パイプベンダーは、製造現場の加工精度、段取り時間、作業負担に直結する設備です。BANTEXは名古屋を拠点に、パイプ曲げ加工機や関連する産業機械の導入相談に対応します。",
        "summary": [
            "パイプ径、材質、曲げ角度、加工数量、設置スペースに合わせて設備検討が必要です。",
            "機械の価格だけでなく、段取り、治具、作業者の扱いやすさ、保守性まで確認します。",
            "名古屋・愛知の製造現場で、パイプベンダーや工作機械の相談先を探している会社に対応します。",
        ],
        "sections": [
            {
                "heading": "パイプベンダー選定で見る条件",
                "body": "パイプベンダーは、曲げたいパイプの外径、肉厚、材質、曲げR、角度、加工数量によって適した機種が変わります。薄肉材、ステンレス、アルミ、鉄など、材質によって加工時の注意点も異なります。導入前には、現在の加工条件、品質で困っている点、作業時間、量産か試作かを整理しておくことが重要です。",
            },
            {
                "heading": "名古屋・愛知の製造現場での相談",
                "body": "名古屋・愛知には、自動車、設備、建築、機械部品など、パイプ加工を必要とする製造現場が多くあります。現場ごとに、必要な精度、段取り替えの頻度、作業者の熟練度、設置スペースが違います。BANTEXでは、単に機械名で選ぶのではなく、加工内容と現場運用を確認しながら導入の方向性を整理します。",
            },
            {
                "heading": "導入時に注意したいこと",
                "body": "パイプベンダーは、購入後の運用まで考える必要があります。治具の準備、作業手順、試し曲げ、角度補正、メンテナンス、消耗品、設置後の教育などが必要です。価格だけで判断すると、後から加工条件に合わない、段取りに時間がかかる、保守が難しいといった問題が起きることがあります。",
            },
            {
                "heading": "BANTEXに相談できる範囲",
                "body": "BANTEXでは、パイプベンダー、パイプ曲げ加工機、工作機械、産業機械の導入検討について相談できます。既存設備の置き換え、新規導入、加工内容の整理、関連する情報発信や会社案内の制作まで、製造現場と営業面を横断して支援できる点が特徴です。",
            },
        ],
        "fit": [
            "名古屋・愛知でパイプベンダーの相談先を探している製造業",
            "パイプ曲げ加工の精度や段取りに課題がある現場",
            "既存設備の更新や新規導入を検討している会社",
            "産業機械と会社案内・Web発信をまとめて相談したい会社",
        ],
        "links": [
            ("お問い合わせ", "https://bantex.jp/#contact"),
            ("会社概要", "https://bantex.jp/#about"),
            ("デジタルサイネージ 名古屋", "https://bantex.jp/seo/services/digital-signage-nagoya.html"),
            ("AI自動化 名古屋", "https://bantex.jp/seo/services/ai-automation-nagoya.html"),
        ],
        "faqs": [
            ("名古屋でパイプベンダーの相談はできますか？", "はい。BANTEXは名古屋市天白区を拠点に、パイプベンダーやパイプ曲げ加工機の導入相談に対応しています。"),
            ("機種選定では何を伝えればよいですか？", "パイプ径、肉厚、材質、曲げ角度、曲げR、加工数量、設置スペース、現在の課題を伝えると検討しやすくなります。"),
            ("新規導入だけでなく置き換えも相談できますか？", "はい。既存設備の更新、加工条件の見直し、新しい加工内容に合わせた設備検討も相談できます。"),
        ],
        "service_type": "パイプベンダー導入支援",
    },
]


CSS = """
:root {
  --color-primary: #1A2332;
  --color-accent: #2A6EBB;
  --color-bg: #F8F7F5;
  --color-surface: #EDECEA;
  --color-text: #2C2C2C;
  --color-white: #FFFFFF;
  --shadow: 0 18px 50px rgba(26, 35, 50, 0.12);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  font-family: "Noto Sans JP", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.85;
  font-size: 15px;
}
a { color: inherit; text-decoration: none; }
.container { width: min(1120px, calc(100% - 32px)); margin-inline: auto; }
.site-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(248, 247, 245, 0.94);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(26, 35, 50, 0.08);
}
.header-inner {
  min-height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.site-logo {
  font-family: Inter, system-ui, sans-serif;
  font-weight: 900;
  letter-spacing: 0.14em;
  color: var(--color-primary);
}
.primary-nav ul {
  display: flex;
  gap: 18px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 0.86rem;
  font-weight: 700;
  color: rgba(26, 35, 50, 0.74);
}
.primary-nav a:hover { color: var(--color-accent); }
.breadcrumb {
  padding: 18px 0;
  font-size: 0.82rem;
  color: rgba(44, 44, 44, 0.62);
}
.breadcrumb a { color: var(--color-accent); font-weight: 700; }
.hero {
  padding: 76px 0 66px;
  background:
    linear-gradient(135deg, rgba(26,35,50,0.96), rgba(42,110,187,0.88)),
    url("../../assets/generated/bantex-hero-command-desktop.jpg") center / cover;
  color: var(--color-white);
}
.hero-label {
  display: inline-block;
  font-family: Inter, system-ui, sans-serif;
  font-weight: 900;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 0.76rem;
  opacity: 0.72;
  margin-bottom: 14px;
}
.hero h1 {
  max-width: 860px;
  font-size: clamp(1.8rem, 4vw, 3rem);
  line-height: 1.35;
  margin: 0 0 18px;
  letter-spacing: 0;
}
.hero p {
  max-width: 780px;
  margin: 0;
  color: rgba(255,255,255,0.88);
  font-size: 1rem;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: -34px;
  position: relative;
  z-index: 2;
}
.summary-card, .content-card, .side-card, .faq-item {
  background: var(--color-white);
  border: 1px solid rgba(26, 35, 50, 0.08);
  border-radius: 8px;
  box-shadow: var(--shadow);
}
.summary-card {
  padding: 22px;
  font-weight: 700;
  color: var(--color-primary);
}
.main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 310px;
  gap: 32px;
  align-items: start;
  padding: 56px 0 70px;
}
.content-card { padding: 32px; margin-bottom: 22px; }
.content-card h2, .faq h2 {
  margin: 0 0 14px;
  color: var(--color-primary);
  font-size: 1.32rem;
  line-height: 1.45;
  letter-spacing: 0;
}
.content-card p { margin: 0; }
.side { position: sticky; top: 86px; display: grid; gap: 18px; }
.side-card { padding: 22px; }
.side-card h2 {
  margin: 0 0 14px;
  color: var(--color-primary);
  font-size: 1rem;
}
.side-card ul {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.side-card li {
  padding-left: 14px;
  border-left: 3px solid rgba(42,110,187,0.32);
  color: rgba(44,44,44,0.78);
}
.related-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(26,35,50,0.08);
  color: var(--color-accent);
  font-weight: 700;
}
.related-link:last-child { border-bottom: 0; }
.faq { padding: 0 0 72px; }
.faq-grid { display: grid; gap: 14px; }
.faq-item { padding: 24px; }
.faq-item h3 {
  margin: 0 0 8px;
  color: var(--color-primary);
  font-size: 1rem;
}
.faq-item p { margin: 0; }
.cta {
  background: var(--color-primary);
  color: var(--color-white);
  padding: 48px 0;
}
.cta-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.cta h2 { margin: 0 0 8px; font-size: 1.45rem; }
.cta p { margin: 0; color: rgba(255,255,255,0.76); }
.cta a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 20px;
  border-radius: 8px;
  background: var(--color-white);
  color: var(--color-primary);
  font-weight: 900;
  white-space: nowrap;
}
.site-footer {
  background: #121821;
  color: rgba(255,255,255,0.72);
  padding: 34px 0;
  font-size: 0.85rem;
}
.footer-inner {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}
.footer-links { display: flex; gap: 16px; flex-wrap: wrap; }
.footer-links a { color: rgba(255,255,255,0.86); }
@media (max-width: 860px) {
  .primary-nav { display: none; }
  .summary-grid, .main-grid { grid-template-columns: 1fr; }
  .summary-grid { margin-top: 18px; }
  .side { position: static; }
  .cta-inner { display: block; }
  .cta a { margin-top: 18px; width: 100%; }
}
"""


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def json_script(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def absolute_url(slug: str) -> str:
    return f"{BASE_URL}/{slug}.html"


def render_page(page: dict, all_pages: list[dict]) -> str:
    url = absolute_url(page["slug"])
    summary_html = "\n".join(f"      <div class=\"summary-card\">{esc(item)}</div>" for item in page["summary"])
    sections_html = "\n".join(
        f"""      <section class=\"content-card\">
        <h2>{esc(section["heading"])}</h2>
        <p>{esc(section["body"])}</p>
      </section>"""
        for section in page["sections"]
    )
    fit_html = "\n".join(f"          <li>{esc(item)}</li>" for item in page["fit"])
    links_html = "\n".join(
        f"          <a class=\"related-link\" href=\"{esc(href)}\"><span>{esc(label)}</span><span aria-hidden=\"true\">&rarr;</span></a>"
        for label, href in page["links"]
    )
    all_pages_links = "\n".join(
        f"          <a class=\"related-link\" href=\"{absolute_url(other['slug'])}\"><span>{esc(other['h1'])}</span><span aria-hidden=\"true\">&rarr;</span></a>"
        for other in all_pages
        if other["slug"] != page["slug"]
    )
    faq_html = "\n".join(
        f"""      <div class=\"faq-item\">
        <h3>{esc(q)}</h3>
        <p>{esc(a)}</p>
      </div>"""
        for q, a in page["faqs"]
    )

    web_page_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page["h1"],
        "headline": page["h1"],
        "description": page["description"],
        "url": url,
        "inLanguage": "ja",
        "datePublished": TODAY,
        "dateModified": TODAY,
        "publisher": {
            "@type": "Organization",
            "name": "株式会社バンテックス",
            "url": "https://bantex.jp/",
        },
    }
    service_jsonld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": page["service_type"],
        "description": page["description"],
        "provider": {
            "@type": "Organization",
            "name": "株式会社バンテックス",
            "url": "https://bantex.jp/",
            "telephone": "+81-52-847-7500",
            "address": {
                "@type": "PostalAddress",
                "postalCode": "468-0015",
                "addressRegion": "愛知県",
                "addressLocality": "名古屋市天白区",
                "streetAddress": "原3丁目304番1号T&Lビル2A",
                "addressCountry": "JP",
            },
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "愛知県"},
            {"@type": "City", "name": "名古屋市"},
            {"@type": "Country", "name": "日本"},
        ],
        "url": url,
        "keywords": page["keywords"],
    }
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in page["faqs"]
        ],
    }
    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "BANTEX", "item": "https://bantex.jp/"},
            {"@type": "ListItem", "position": 2, "name": "SEOサービスページ", "item": "https://bantex.jp/seo/services/"},
            {"@type": "ListItem", "position": 3, "name": page["h1"], "item": url},
        ],
    }

    return f"""<!DOCTYPE html>
<html lang=\"ja\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{esc(page["title"])}</title>
  <meta name=\"description\" content=\"{esc(page["description"])}\">
  <meta name=\"keywords\" content=\"{esc(page["keywords"])}\">
  <meta name=\"author\" content=\"株式会社バンテックス\">
  <meta name=\"robots\" content=\"index, follow\">
  <link rel=\"canonical\" href=\"{url}\">
  <meta property=\"og:type\" content=\"article\">
  <meta property=\"og:url\" content=\"{url}\">
  <meta property=\"og:title\" content=\"{esc(page["title"])}\">
  <meta property=\"og:description\" content=\"{esc(page["description"])}\">
  <meta property=\"og:image\" content=\"https://bantex.jp/assets/generated/bantex-hero-command-desktop.jpg\">
  <meta property=\"og:site_name\" content=\"株式会社バンテックス\">
  <meta property=\"og:locale\" content=\"ja_JP\">
  <meta name=\"twitter:card\" content=\"summary_large_image\">
  <meta name=\"twitter:title\" content=\"{esc(page["title"])}\">
  <meta name=\"twitter:description\" content=\"{esc(page["description"])}\">
  <meta name=\"twitter:image\" content=\"https://bantex.jp/assets/generated/bantex-hero-command-desktop.jpg\">
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@800;900&family=Noto+Sans+JP:wght@400;500;700;900&display=swap\" rel=\"stylesheet\">
  <script type=\"application/ld+json\">{json_script(web_page_jsonld)}</script>
  <script type=\"application/ld+json\">{json_script(service_jsonld)}</script>
  <script type=\"application/ld+json\">{json_script(faq_jsonld)}</script>
  <script type=\"application/ld+json\">{json_script(breadcrumb_jsonld)}</script>
  <style>{CSS}</style>
</head>
<body>
  <header class=\"site-header\">
    <div class=\"container header-inner\">
      <a class=\"site-logo\" href=\"https://bantex.jp/\">BANTEX</a>
      <nav class=\"primary-nav\" aria-label=\"主要ナビゲーション\">
        <ul>
          <li><a href=\"https://bantex.jp/\">トップ</a></li>
          <li><a href=\"https://bantex.jp/ai-services.html\">AIサービス</a></li>
          <li><a href=\"https://bantex.jp/#fields\">3部門</a></li>
          <li><a href=\"https://bantex.jp/#contact\">お問い合わせ</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <div class=\"container breadcrumb\">
      <a href=\"https://bantex.jp/\">BANTEX</a> / <span>{esc(page["h1"])}</span>
    </div>

    <section class=\"hero\">
      <div class=\"container\">
        <span class=\"hero-label\">{esc(page["label"])}</span>
        <h1>{esc(page["h1"])}</h1>
        <p>{esc(page["lead"])}</p>
      </div>
    </section>

    <section class=\"container summary-grid\" aria-label=\"概要\">
{summary_html}
    </section>

    <section class=\"container main-grid\">
      <div>
{sections_html}
      </div>
      <aside class=\"side\" aria-label=\"関連情報\">
        <div class=\"side-card\">
          <h2>向いている相談</h2>
          <ul>
{fit_html}
          </ul>
        </div>
        <div class=\"side-card\">
          <h2>関連ページ</h2>
{links_html}
        </div>
        <div class=\"side-card\">
          <h2>サービス別ページ</h2>
{all_pages_links}
        </div>
      </aside>
    </section>

    <section class=\"faq\">
      <div class=\"container\">
        <h2>よくある質問</h2>
        <div class=\"faq-grid\">
{faq_html}
        </div>
      </div>
    </section>

    <section class=\"cta\">
      <div class=\"container cta-inner\">
        <div>
          <h2>{esc(page["h1"])}を相談する</h2>
          <p>現在の課題、設置場所、業務内容、導入目的を整理してから、現実的な進め方をご提案します。</p>
        </div>
        <a href=\"https://bantex.jp/#contact\">お問い合わせ</a>
      </div>
    </section>
  </main>

  <footer class=\"site-footer\">
    <div class=\"container footer-inner\">
      <div>© 2026 株式会社バンテックス</div>
      <div class=\"footer-links\">
        <a href=\"https://bantex.jp/terms.html\">利用規約</a>
        <a href=\"https://bantex.jp/privacy.html\">プライバシーポリシー</a>
        <a href=\"https://bantex.jp/tokushoho.html\">特定商取引法に基づく表記</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def render_index(all_pages: list[dict]) -> str:
    url = "https://bantex.jp/seo/services/"
    cards = "\n".join(
        f"""      <a class=\"summary-card\" href=\"{absolute_url(page['slug'])}\">
        <span>{esc(page['label'])}</span><br>
        {esc(page['h1'])}
      </a>"""
        for page in all_pages
    )
    item_list_jsonld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "BANTEX サービス別SEOページ",
        "url": url,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "item": {
                    "@type": "WebPage",
                    "name": page["h1"],
                    "url": absolute_url(page["slug"]),
                    "description": page["description"],
                },
            }
            for index, page in enumerate(all_pages, start=1)
        ],
    }
    return f"""<!DOCTYPE html>
<html lang=\"ja\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>サービス別SEOページ | AI自動化・サイネージ・パイプベンダー | 株式会社バンテックス</title>
  <meta name=\"description\" content=\"株式会社バンテックスのサービス別SEOページ一覧。AI自動化 名古屋、AI社員 名古屋、AI映像制作 名古屋、インスタ 自動投稿、小型デジタルサイネージ、デジタルサイネージ 名古屋、床面LEDサイネージ、パイプベンダー 名古屋を整理しています。\">
  <meta name=\"robots\" content=\"index, follow\">
  <link rel=\"canonical\" href=\"{url}\">
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@800;900&family=Noto+Sans+JP:wght@400;500;700;900&display=swap\" rel=\"stylesheet\">
  <script type=\"application/ld+json\">{json_script(item_list_jsonld)}</script>
  <style>{CSS}</style>
</head>
<body>
  <header class=\"site-header\">
    <div class=\"container header-inner\">
      <a class=\"site-logo\" href=\"https://bantex.jp/\">BANTEX</a>
      <nav class=\"primary-nav\" aria-label=\"主要ナビゲーション\">
        <ul>
          <li><a href=\"https://bantex.jp/\">トップ</a></li>
          <li><a href=\"https://bantex.jp/ai-services.html\">AIサービス</a></li>
          <li><a href=\"https://bantex.jp/#contact\">お問い合わせ</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <main>
    <section class=\"hero\">
      <div class=\"container\">
        <span class=\"hero-label\">Keyword Guides</span>
        <h1>サービス別SEOページ</h1>
        <p>株式会社バンテックスが扱うAI自動化、AI社員、AI映像制作、インスタ自動投稿、デジタルサイネージ、床面LEDサイネージ、パイプベンダーについて、検索キーワード別に説明しています。</p>
      </div>
    </section>
    <section class=\"container summary-grid\" aria-label=\"サービス別ページ一覧\">
{cards}
    </section>
    <section class=\"cta\">
      <div class=\"container cta-inner\">
        <div>
          <h2>BANTEXへの相談</h2>
          <p>AI、サイネージ、産業機械の導入目的に合わせて、現実的な進め方をご提案します。</p>
        </div>
        <a href=\"https://bantex.jp/#contact\">お問い合わせ</a>
      </div>
    </section>
  </main>
  <footer class=\"site-footer\">
    <div class=\"container footer-inner\">
      <div>© 2026 株式会社バンテックス</div>
      <div class=\"footer-links\">
        <a href=\"https://bantex.jp/terms.html\">利用規約</a>
        <a href=\"https://bantex.jp/privacy.html\">プライバシーポリシー</a>
        <a href=\"https://bantex.jp/tokushoho.html\">特定商取引法に基づく表記</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def sitemap_block(loc: str, priority: str) -> str:
    return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>"""


def upsert_sitemap() -> None:
    text = SITEMAP_PATH.read_text(encoding="utf-8")
    entries = [
        ("https://bantex.jp/", "1.0", "weekly"),
        ("https://bantex.jp/ai-services.html", "0.9", "weekly"),
        ("https://bantex.jp/llms.txt", "0.4", "weekly"),
        ("https://bantex.jp/seo/services/", "0.8", "monthly"),
    ]
    entries.extend((absolute_url(page["slug"]), "0.75", "monthly") for page in PAGES)

    for loc, priority, changefreq in entries:
        block = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        pattern = re.compile(
            r"  <url>\n"
            + r"    <loc>"
            + re.escape(loc)
            + r"</loc>\n"
            + r"    <lastmod>.*?</lastmod>\n"
            + r"    <changefreq>.*?</changefreq>\n"
            + r"    <priority>.*?</priority>\n"
            + r"  </url>",
            re.DOTALL,
        )
        if pattern.search(text):
            text = pattern.sub(block, text)
        else:
            text = text.replace("</urlset>", block + "\n</urlset>")

    SITEMAP_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(render_index(PAGES), encoding="utf-8")
    print("wrote seo/services/index.html")
    for page in PAGES:
        path = OUTPUT_DIR / f"{page['slug']}.html"
        path.write_text(render_page(page, PAGES), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    upsert_sitemap()
    print("updated sitemap.xml")


if __name__ == "__main__":
    main()
