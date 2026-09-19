"""第10回の区間と四席のSVGを再生成する。標準ライブラリのみ。"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def svg(width,height,title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{title}</title>
<style>text{{font:12px sans-serif;fill:#222}} .axis{{stroke:#666;stroke-width:1}} .a{{fill:#e8dff0;stroke:#593b66}} .c{{fill:#dfeaf4;stroke:#335f7e}} .b{{fill:#e4ecdf;stroke:#466738}}</style>
{body}
</svg>\n'''


body=[]
for row,names in enumerate([('A','C'),('C','A')]):
    y=24+row*72
    body.append(f'<text x="10" y="{y+17}">順序{row+1}</text>')
    for col,name in enumerate(names):
        x=56+col*112
        body.append(f'<rect data-task="{name}" data-start="{col*2}" data-duration="2" class="{name.lower()}" x="{x}" y="{y}" width="112" height="26"/>')
        body.append(f'<text x="{x+56}" y="{y+17}" text-anchor="middle">{name}</text>')
    body.append(f'<line class="axis" x1="56" y1="{y+32}" x2="280" y2="{y+32}"/>')
    for time in (0,2,4):
        x=56+56*time;body.append(f'<line class="axis" x1="{x}" y1="{y+29}" x2="{x}" y2="{y+36}"/><text x="{x}" y="{y+49}" text-anchor="middle">{time}</text>')
(ROOT/'interval-orders.svg').write_text(svg(304,154,'同じ装置のAとC。Aが先でもCが先でも、時刻2で接してよい。','\n'.join(body)))
body=[]
for i,(name,start,duration) in enumerate([('A',0,3),('B',3,2),('C',3,2)]):
    y=20+i*34;x=38+start*36
    body.append(f'<text x="10" y="{y+17}">{name}</text><rect data-task="{name}" data-start="{start}" data-duration="{duration}" class="{name.lower()}" x="{x}" y="{y}" width="{duration*36}" height="26"/><text x="{x+duration*18}" y="{y+17}" text-anchor="middle">[{start}, {start+duration})</text>')
body.append('<line class="axis" x1="38" y1="125" x2="290" y2="125"/>')
for t in range(8):
    x=38+36*t;body.append(f'<line class="axis" x1="{x}" y1="122" x2="{x}" y2="129"/><text x="{x}" y="144" text-anchor="middle">{t}</text>')
body.append('<text x="38" y="168">同じ装置：A・C　　期限：7</text>')
(ROOT/'practice-intervals.svg').write_text(svg(310,181,'必修1の成立例。Aは0〜3、BとCは3〜5。共有装置のAとCは時刻3で接する。','\n'.join(body)))
body=['<text x="12" y="17">左</text><text x="266" y="17">右</text>']
for i in range(4):
    x=12+68*i;body.append(f'<rect x="{x}" y="29" width="58" height="38" fill="none" stroke="#593b66"/><text x="{x+29}" y="53" text-anchor="middle">{i+1}</text>')
body.append('<text x="12" y="91">各席に一人。</text><text x="12" y="109">A・Bの左右の順序は自由。</text>')
(ROOT/'seats.svg').write_text(svg(310,121,'左から1〜4の四席。各席に一人ずつ座る。','\n'.join(body)))
