from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "service-thumbs"
CONTACT = ROOT / "assets" / "service-thumbs-contact-sheet.jpg"

W, H = 1200, 675
FONT_REG = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"
FONT_MED = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"


def font(size: int, weight: str = "reg") -> ImageFont.FreeTypeFont:
    path = {"reg": FONT_REG, "med": FONT_MED, "bold": FONT_BOLD}.get(weight, FONT_REG)
    return ImageFont.truetype(path, size)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, pos, value, size, fill, weight="reg", anchor=None):
    draw.text(pos, value, font=font(size, weight), fill=fill, anchor=anchor)


def wrap(value: str, size: int, max_width: int, weight="reg") -> list[str]:
    f = font(size, weight)
    lines: list[str] = []
    current = ""
    for ch in value:
        test = current + ch
        if f.getbbox(test)[2] <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def gradient(colors: tuple[tuple[int, int, int], tuple[int, int, int]], accent=(255, 255, 255)) -> Image.Image:
    img = Image.new("RGB", (W, H), colors[0])
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.7) + (y / H * 0.3)
            r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
            g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
            b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
            px[x, y] = (r, g, b)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i, alpha in enumerate((56, 34, 24)):
        d.ellipse((620 + i * 42, -190 + i * 24, 1320 + i * 42, 520 + i * 24), fill=(*accent, alpha))
        d.ellipse((-260 + i * 38, 250 + i * 12, 380 + i * 38, 910 + i * 12), fill=(*accent, alpha // 2))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def glass_card(draw, box, fill=(255, 255, 255, 38), outline=(255, 255, 255, 70), radius=28):
    rounded(draw, box, radius, fill, outline, 2)


def badge(draw, x, y, label, fill=(255, 255, 255, 36), fg=(255, 255, 255)):
    f = font(24, "bold")
    tw = f.getbbox(label)[2]
    rounded(draw, (x, y, x + tw + 42, y + 42), 21, fill, (255, 255, 255, 70), 1)
    draw.text((x + 21, y + 9), label, font=f, fill=fg)


def title_block(draw, title, subtitle, theme, dark=False):
    fg = (255, 255, 255) if dark else (17, 24, 39)
    sub = (226, 232, 240) if dark else (55, 65, 81)
    badge(draw, 62, 54, theme, fill=(255, 255, 255, 34) if dark else (255, 255, 255, 230), fg=fg)
    y = 116
    title_size = 58
    if len(title) > 10:
        title_size = 48
    if len(title) > 15:
        title_size = 42
    title_lines = wrap(title, title_size, 510, "bold")[:2]
    for i, line in enumerate(title_lines):
        text(draw, (62, y + i * int(title_size * 1.18)), line, title_size, fg, "bold")
    y += int(title_size * 1.34) * max(1, len(title_lines))
    for i, line in enumerate(wrap(subtitle, 30, 500, "med")[:2]):
        text(draw, (64, y + 12 + i * 40), line, 30, sub, "med")


def paste_cover(base: Image.Image, src: Image.Image, box, radius=28):
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    s = src.convert("RGB")
    scale = max(bw / s.width, bh / s.height)
    s = s.resize((int(s.width * scale), int(s.height * scale)), Image.Resampling.LANCZOS)
    left = (s.width - bw) // 2
    top = (s.height - bh) // 2
    s = s.crop((left, top, left + bw, top + bh))
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), radius=radius, fill=255)
    base.paste(s, (x1, y1), mask)


def phone(base: Image.Image, src_path: Path, x: int, y: int, h: int, tilt: int = 0):
    src = Image.open(src_path).convert("RGB")
    w = int(h * 0.462)
    shell = Image.new("RGBA", (w + 34, h + 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(shell)
    rounded(d, (0, 0, w + 34, h + 34), 42, (15, 23, 42, 245), (255, 255, 255, 110), 3)
    paste_cover(shell, src, (17, 17, w + 17, h + 17), 30)
    rounded(d, ((w + 34) // 2 - 46, 22, (w + 34) // 2 + 46, 42), 10, (10, 14, 26, 230))
    shadow = Image.new("RGBA", shell.size, (0, 0, 0, 110)).filter(ImageFilter.GaussianBlur(20))
    if tilt:
        shell = shell.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
        shadow = shadow.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
    base.alpha_composite(shadow, (x + 18, y + 26))
    base.alpha_composite(shell, (x, y))


def browser_window(draw, box, title, rows: Iterable[tuple[str, str]], accent):
    x1, y1, x2, y2 = box
    rounded(draw, box, 28, (255, 255, 255, 235), (255, 255, 255, 255), 2)
    rounded(draw, (x1, y1, x2, y1 + 72), 28, (248, 250, 252, 255), None)
    for i, c in enumerate(((239, 68, 68), (245, 158, 11), (34, 197, 94))):
        draw.ellipse((x1 + 30 + i * 28, y1 + 28, x1 + 46 + i * 28, y1 + 44), fill=c)
    text(draw, (x1 + 130, y1 + 24), title, 26, (30, 41, 59), "bold")
    y = y1 + 110
    for label, value in rows:
        rounded(draw, (x1 + 34, y, x2 - 34, y + 64), 18, (241, 245, 249), None)
        draw.rectangle((x1 + 34, y, x1 + 42, y + 64), fill=accent)
        text(draw, (x1 + 62, y + 16), label, 22, (71, 85, 105), "med")
        text(draw, (x2 - 58, y + 16), value, 22, (15, 23, 42), "bold", anchor="ra")
        y += 86


def make_ai_movie():
    img = gradient(((7, 12, 29), (11, 72, 122)), (59, 130, 246))
    d = ImageDraw.Draw(img)
    title_block(d, "AI映像制作", "CM・SNS動画・企業PVをAIで制作", "VIDEO AI", dark=True)
    rounded(d, (610, 82, 1100, 585), 34, (255, 255, 255, 28), (255, 255, 255, 80), 2)
    for i, color in enumerate(((56, 189, 248), (129, 140, 248), (34, 197, 94))):
        x = 650 + i * 130
        rounded(d, (x, 142, x + 96, 412), 18, (*color, 210))
        d.polygon([(x + 34, 235), (x + 34, 318), (x + 78, 276)], fill=(255, 255, 255, 235))
    text(d, (650, 472), "1枚の画像から動画へ", 34, (255, 255, 255), "bold")
    return img


def make_kanji():
    img = gradient(((28, 19, 50), (5, 56, 73)), (250, 204, 21))
    d = ImageDraw.Draw(img)
    title_block(d, "Kanji Compass", "今日の漢字とラッキー方位を表示", "iPhoneアプリ", dark=True)
    root = next(Path("/Users/banmako/dev").glob("漢字コン*"))
    phone(img, root / "designs" / "11_store_screenshot_1.png", 620, 75, 520, -6)
    phone(img, root / "designs" / "12_store_screenshot_2.png", 820, 105, 470, 5)
    text(d, (658, 598), "漢字・方位・壁紙", 32, (255, 255, 255), "bold")
    return img


def make_kuroon():
    img = gradient(((244, 246, 248), (101, 116, 139)), (255, 255, 255))
    d = ImageDraw.Draw(img)
    title_block(d, "クルーン検証", "玉の動きを3Dで確認", "iPhoneアプリ")
    base = Path("/Users/banmako/dev/クルーン/fastlane/screenshots/ja")
    phone(img, base / "01-home.png", 640, 62, 530, -7)
    phone(img, base / "02-balls.png", 840, 105, 470, 5)
    for x, y, c in [(635, 545, (239, 68, 68)), (700, 565, (59, 130, 246)), (760, 540, (34, 197, 94))]:
        d.ellipse((x, y, x + 42, y + 42), fill=c, outline=(255, 255, 255), width=4)
    return img


def make_gekicha():
    img = gradient(((255, 247, 237), (220, 38, 38)), (251, 146, 60))
    d = ImageDraw.Draw(img)
    title_block(d, "ゲキッチャ", "アンケート回答から抽選参加まで", "SURVEY LOTTERY")
    browser_window(d, (575, 80, 1105, 585), "イベント抽選フォーム", [("回答済み", "358人"), ("抽選参加", "124人"), ("当選表示", "ON")], (239, 68, 68))
    rounded(d, (650, 455, 1030, 530), 28, (220, 38, 38), None)
    text(d, (840, 475), "今すぐ抽選", 34, (255, 255, 255), "bold", anchor="ma")
    return img


def make_worker():
    img = gradient(((15, 23, 42), (49, 46, 129)), (14, 165, 233))
    d = ImageDraw.Draw(img)
    title_block(d, "AI社員", "24時間働く会社専用AI", "BUSINESS AI", dark=True)
    browser_window(d, (575, 86, 1105, 580), "AI社員 管理画面", [("問い合わせ対応", "自動"), ("資料作成", "完了"), ("社内ナレッジ", "接続済")], (79, 70, 229))
    d.ellipse((735, 420, 940, 625), fill=(255, 255, 255, 38), outline=(255, 255, 255, 90), width=3)
    d.ellipse((795, 465, 880, 550), fill=(255, 255, 255, 230))
    return img


def make_x():
    img = gradient(((2, 6, 23), (29, 78, 216)), (96, 165, 250))
    d = ImageDraw.Draw(img)
    title_block(d, "X AI自動投稿", "HPから毎日SNS投稿を自動作成", "SOCIAL AUTO", dark=True)
    rounded(d, (610, 82, 1090, 590), 34, (255, 255, 255, 235), None)
    for y, label in [(150, "朝 8:00 投稿予約"), (270, "夜 19:00 投稿予約"), (390, "AIが本文を生成")]:
        rounded(d, (660, y, 1040, y + 74), 22, (241, 245, 249), None)
        text(d, (690, y + 20), label, 26, (15, 23, 42), "bold")
    text(d, (850, 500), "X", 76, (15, 23, 42), "bold", anchor="ma")
    return img


def make_koubo():
    img = gradient(((236, 253, 245), (20, 184, 166)), (45, 212, 191))
    d = ImageDraw.Draw(img)
    title_block(d, "公募ナビAI", "入札・補助金案件を毎朝メール配信", "PUBLIC BID")
    browser_window(d, (575, 80, 1105, 585), "案件マッチング", [("補助金候補", "12件"), ("入札案件", "8件"), ("メール配信", "毎朝")], (20, 184, 166))
    return img


def make_oneflash():
    img = gradient(((248, 250, 252), (59, 130, 246)), (37, 99, 235))
    d = ImageDraw.Draw(img)
    title_block(d, "OnePage-Flash", "10分でホームページを自動生成", "WEB BUILDER")
    rounded(d, (605, 74, 1100, 595), 34, (255, 255, 255, 235), None)
    rounded(d, (640, 125, 1065, 215), 18, (15, 23, 42), None)
    text(d, (670, 152), "店舗名を入力", 28, (255, 255, 255), "bold")
    for i, h in enumerate([120, 80, 145]):
        rounded(d, (650 + i * 130, 265, 755 + i * 130, 265 + h), 18, (219, 234, 254), None)
    text(d, (848, 488), "HP完成", 48, (30, 64, 175), "bold", anchor="ma")
    return img


def make_kokotomo():
    img = gradient(((240, 253, 244), (22, 163, 74)), (34, 197, 94))
    d = ImageDraw.Draw(img)
    title_block(d, "ココトモ カスタマー", "LINEとAIで顧客対応を自動化", "LINE AI")
    rounded(d, (595, 78, 1085, 590), 34, (255, 255, 255, 236), None)
    for y, label, side in [(145, "営業時間を教えて", "r"), (245, "本日は10:00からです", "l"), (345, "予約できますか？", "r"), (445, "空き時間を確認します", "l")]:
        x1, x2, fill = (760, 1040, (220, 252, 231)) if side == "r" else (640, 940, (241, 245, 249))
        rounded(d, (x1, y, x2, y + 62), 24, fill, None)
        text(d, (x1 + 24, y + 16), label, 24, (15, 23, 42), "bold")
    return img


def make_startup():
    img = gradient(((255, 251, 235), (124, 58, 237)), (245, 158, 11))
    d = ImageDraw.Draw(img)
    title_block(d, "事業立ち上げ", "計画・HP・ロゴ・SNSを一括準備", "STARTUP")
    for i, (label, color) in enumerate([("PLAN", (59, 130, 246)), ("LOGO", (236, 72, 153)), ("WEB", (34, 197, 94)), ("SNS", (245, 158, 11))]):
        x = 610 + (i % 2) * 230
        y = 120 + (i // 2) * 190
        rounded(d, (x, y, x + 185, y + 145), 26, (*color, 235), (255, 255, 255, 180), 2)
        text(d, (x + 92, y + 52), label, 34, (255, 255, 255), "bold", anchor="ma")
    text(d, (838, 525), "最短1週間で開始", 40, (255, 255, 255), "bold", anchor="ma")
    return img


def report_thumb(title, subtitle, theme, rows, accent):
    img = gradient(((248, 250, 252), (203, 213, 225)), accent)
    d = ImageDraw.Draw(img)
    title_block(d, title, subtitle, theme)
    browser_window(d, (555, 74, 1110, 590), "AIレポート", rows, accent)
    # Mini chart
    pts = [(650, 505), (730, 455), (820, 475), (910, 400), (1015, 425)]
    d.line(pts, fill=accent, width=8, joint="curve")
    for x, y in pts:
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=accent)
    return img


def save_all():
    makers = {
        "ai-movie.jpg": make_ai_movie,
        "kanji-compass.jpg": make_kanji,
        "kuroon.jpg": make_kuroon,
        "gekicha.jpg": make_gekicha,
        "ai-worker.jpg": make_worker,
        "x-auto-post.jpg": make_x,
        "koubo-navi.jpg": make_koubo,
        "oneflash.jpg": make_oneflash,
        "kokotomo.jpg": make_kokotomo,
        "jigyo-startup.jpg": make_startup,
        "ai-fudosan.jpg": lambda: report_thumb("不動産市場分析", "エリア相場・競合・顧客を分析", "REAL ESTATE", [("相場", "自動算出"), ("競合", "可視化"), ("需要", "スコア化")], (37, 99, 235)),
        "ai-shoken.jpg": lambda: report_thumb("出店商圏分析", "人口・競合・消費力を地図で確認", "STORE AREA", [("人口", "1,892エリア"), ("競合", "比較"), ("消費力", "分析")], (234, 88, 12)),
        "ai-shigyo.jpg": lambda: report_thumb("士業商圏分析", "6士業の開業適性を一括分析", "LEGAL AREA", [("税理士", "競合密度"), ("社労士", "需要"), ("行政書士", "適性")], (79, 70, 229)),
    }
    for name, maker in makers.items():
        img = maker().convert("RGB")
        img.save(OUT / name, quality=91, optimize=True, progressive=True)

    names = list(makers.keys())
    thumb_w, thumb_h = 300, 169
    sheet = Image.new("RGB", (thumb_w * 4, (thumb_h + 44) * 4), (245, 247, 250))
    d = ImageDraw.Draw(sheet)
    for i, name in enumerate(names):
        x = (i % 4) * thumb_w
        y = (i // 4) * (thumb_h + 44)
        im = Image.open(OUT / name).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        text(d, (x + 10, y + thumb_h + 10), name, 18, (15, 23, 42), "bold")
    sheet.save(CONTACT, quality=90)


if __name__ == "__main__":
    save_all()
