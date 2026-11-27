"""index.html 빌드: src/index.src.html 의 <!--ASSETS--> 자리에 얼굴 모델과 노멀맵을 base64로,
<!--I18N--> 자리에 src/i18n.js(다국어 사전)를 넣는다.

모델을 페이지 안에 넣는 이유: 모바일 앱 뷰어에서는 옆 파일을 따로 불러오지 못하는 경우가 있어서.

사용법:
    python3 build.py          # index.html 생성
"""
import base64
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / "src/index.src.html").read_text(encoding="utf-8")
glb = base64.b64encode((ROOT / "assets/head.glb").read_bytes()).decode()
nrm = base64.b64encode((ROOT / "assets/head_normal.jpg").read_bytes()).decode()

assets = (
    "<script>/* 얼굴 모델 데이터 (Lee Perry-Smith 헤드 스캔, CC BY 3.0) */\n"
    f'const HEAD_GLB="{glb}";\n'
    f'const HEAD_NRM="data:image/jpeg;base64,{nrm}";</script>'
)
assert "<!--ASSETS-->" in src, "src/index.src.html 에 <!--ASSETS--> 자리가 없어요"
i18n = (ROOT / "src/i18n.js").read_text(encoding="utf-8")
src = src.replace("<!--I18N-->", "<script>\n" + i18n + "</script>")
(ROOT / "index.html").write_text(src.replace("<!--ASSETS-->", assets), encoding="utf-8")
photo = (ROOT / "src/photo.src.html").read_text(encoding="utf-8")
assert "<!--I18N-->" in photo
(ROOT / "photo.html").write_text(photo.replace("<!--I18N-->", "<script>\n" + i18n + "</script>"), encoding="utf-8")
print("index.html, photo.html 생성 완료")
