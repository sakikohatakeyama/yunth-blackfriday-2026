# index-pink.html（第一弾版）から 第二弾版 index-2nd.html / 第三弾版 index-3rd.html を作る
#   python3 tools/make_versions.py
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
base = (root / "index-pink.html").read_text(encoding="utf-8")

def cut(s, a, b):
    """a で始まり b で終わる最初のかたまりを消す"""
    i = s.index(a); j = s.index(b, i) + len(b)
    return s[:i] + s[j:]

def rep(s, a, b):
    assert a in s, a
    return s.replace(a, b)

def wave(no):  # 第○弾の <li class="wave"> を丸ごと消す
    def f(s):
        k = s.index(f'<p class="wave-no">{no}</p>')
        i = s.rindex('<li class="wave', 0, k); j = s.index("</li>", k) + len("</li>")
        while s[i-1] == " ": i -= 1
        if s[i-1] == "\n": i -= 1
        return s[:i] + s[j:]
    return f

def stage(no):  # STAGES の第○弾の行を消す
    def f(s):
        return re.sub(r'\n  \{no:"%s".*?\},?' % no, "", s, count=1)
    return f

def fix_last_comma(s):
    return re.sub(r'\},(\n\];\nconst SERUMS)', r'}\1', s)

# 第二弾版: FV下の左カードを第二弾（楽天スーパーDEAL 30%還元）の画像に。注釈は画像の中にあるので外す
v2 = rep(base, '<img src="images/fv-card-vc.webp?v=3" alt="11/19(木)10:00〜11/20(金)9:59 生VC美白美容液 ポイント20倍"',
               '<img src="images/dai2-fv-card-vc.webp?v=2" alt="11/20(金)10:00〜11/21(土)9:59 生VC美容液 楽天スーパーDEAL ポイント30%還元"')
v2 = rep(v2, '<img src="images/fv-card-device.webp?v=4" alt="11/19(木)10:00〜11/26(木)9:59 Deep Boost 生AZ美容液特別セット 7,809円OFFクーポン"',
             '<img src="images/dai2-fv-card-device.webp?v=1" alt="11/19(木)10:00〜11/26(木)9:59 Deep Boost 生AZ美容液特別セット 7,809円OFFクーポン"')
v2 = v2.replace('width="695" height="940"></a>', 'width="781" height="1023"></a>')
# 新しいカード画像は外側にネオンの光（約6%）が入っているので、内側どうしを重ねてカードの間をつめる
v2 = rep(v2, '<nav class="fv-cards" ', '<nav class="fv-cards is-glow" ')
v2 = rep(v2, "</style>", ".fv-cards.is-glow{column-gap:0}\n.fv-cards.is-glow .fv-card:nth-child(1){margin-right:-2.5%}\n.fv-cards.is-glow .fv-card:nth-child(2){margin-left:-2.5%}\n</style>")
v2 = rep(v2, '\n    <li>※獲得ポイントには上限があります。</li>', "")
v2 = wave("第一弾")(v2)
v2 = fix_last_comma(stage("一")(v2))
v2 = rep(v2, "<title>", "<title>【第二弾】")

# 第三弾版: 左カードを第三弾（20%OFFクーポン）の画像に。右の Deep Boost は第二弾と同じ光つきカード
v3 = rep(base, '<img src="images/fv-card-vc.webp?v=3" alt="11/19(木)10:00〜11/20(金)9:59 生VC美白美容液 ポイント20倍"',
               '<img src="images/dai3-fv-card-vc.webp?v=1" alt="11/21(土)10:00〜11/26(木)9:59 生VC美容液 20%OFFクーポン"')
v3 = rep(v3, '<img src="images/fv-card-device.webp?v=4" alt=', '<img src="images/dai2-fv-card-device.webp?v=1" alt=')
v3 = v3.replace('width="695" height="940"></a>', 'width="781" height="1023"></a>')
v3 = rep(v3, '<nav class="fv-cards" ', '<nav class="fv-cards is-glow" ')
v3 = rep(v3, "</style>", ".fv-cards.is-glow{column-gap:0}\n.fv-cards.is-glow .fv-card:nth-child(1){margin-right:-2.5%}\n.fv-cards.is-glow .fv-card:nth-child(2){margin-left:-2.5%}\n</style>")
v3 = rep(v3, '\n    <li>※獲得ポイントには上限があります。</li>', "")
v3 = wave("第一弾")(v3); v3 = wave("第二弾")(v3)
v3 = fix_last_comma(stage("二")(stage("一")(v3)))
v3 = rep(v3, "<title>", "<title>【第三弾】")
v3 = rep(v3, '美容液<sup>＊</sup> 日替わりキャンペーン</span>', '美容液<sup>＊</sup> 20%OFFクーポン</span>')
v3 = rep(v3, '<a href="#vc" data-nav="vc">日替わり</a>', '<a href="#vc" data-nav="vc">生VC<br>美容液</a>')

(root / "index-2nd.html").write_text(v2, encoding="utf-8")
(root / "index-3rd.html").write_text(v3, encoding="utf-8")
print("ok")
