# 納品フォルダを作る: python3 tools/make_delivery.py <元のhtml> <出力フォルダ>
#   検索よけ・デモ帯・非表示ブロック内の画像を外し、ページで使う画像だけをコピーする
import re, sys, shutil, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src, out = root / sys.argv[1], pathlib.Path(sys.argv[2]).expanduser()
s = src.read_text(encoding="utf-8")
def drop(pat, n=1):
    global s
    s, k = re.subn(pat, "", s)
    assert k == n, (pat, k)
drop(r'\n<meta name="robots"[^>]*>')
drop(r'\n<div class="demo-band">[^<]*</div>')
drop(r'<img src="images/logo-ink\.png"[^>]*>')
drop(r'\n    <img src="images/serum-vc\.jpg"[^>]*>')
if out.exists(): shutil.rmtree(out)
(out / "images").mkdir(parents=True)
(out / "index.html").write_text(s, encoding="utf-8")
refs = set(re.findall(r'images/([A-Za-z0-9_./-]+?\.(?:png|jpe?g|webp|gif|svg))', s))
refs |= {m for m in re.findall(r'img:"([^"]+)"', s)}
for r in sorted(refs):
    d = out / "images" / r; d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "images" / r, d)
print(len(refs), "images")
