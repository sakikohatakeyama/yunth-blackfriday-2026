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
        i = s.rindex('<li class="wave"', 0, k); j = s.index("</li>", k) + len("</li>")
        while s[i-1] == " ": i -= 1
        if s[i-1] == "\n": i -= 1
        return s[:i] + s[j:]
    return f

def stage(no):  # STAGES の第○弾の行を消す
    def f(s):
        return re.sub(r'\n  \{no:"%s".*?\},?' % no, "", s, count=1)
    return f

def common(s):
    # FV下: 第一弾（VC ポイント20倍）のカードと、その注釈を外す
    s = re.sub(r'\n  <a class="fv-card is-img" href="#vc">.*?</a>', "", s, count=1)
    s = rep(s, '\n    <li>※獲得ポイントには上限があります。</li>', "")
    s = rep(s, '<nav class="fv-cards" ', '<nav class="fv-cards is-one" ')
    s = rep(s, "</style>", ".fv-cards.is-one .fv-card{grid-column:1/-1;justify-self:center;width:min(62%,340px)}\n</style>")
    return s

def fix_last_comma(s):
    return re.sub(r'\},(\n\];\nconst SERUMS)', r'}\1', s)

v2 = common(base)
v2 = wave("第一弾")(v2)
v2 = fix_last_comma(stage("一")(v2))
v2 = rep(v2, "<title>", "<title>【第二弾】")

v3 = common(base)
v3 = wave("第一弾")(v3); v3 = wave("第二弾")(v3)
v3 = fix_last_comma(stage("二")(stage("一")(v3)))
v3 = rep(v3, "<title>", "<title>【第三弾】")
v3 = rep(v3, '美容液<sup>＊</sup> 日替わりキャンペーン</span>', '美容液<sup>＊</sup> 20%OFFクーポン</span>')
v3 = rep(v3, '<a href="#vc" data-nav="vc">日替わり</a>', '<a href="#vc" data-nav="vc">生VC<br>美容液</a>')

(root / "index-2nd.html").write_text(v2, encoding="utf-8")
(root / "index-3rd.html").write_text(v3, encoding="utf-8")
print("ok")
