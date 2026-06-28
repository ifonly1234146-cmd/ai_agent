import subprocess, json, sys

FOLDER_ID = "1xFgTkZNU-voN_y7Y3gCuBUGn8EZV4wox"

def gws(args, json_data=None, params=None):
    cmd = ['powershell', '-Command']
    parts = ['gws'] + args
    if params:
        parts += ['--params', f"'{json.dumps(params)}'"]
    if json_data:
        parts += ['--json', f"'{json.dumps(json_data, ensure_ascii=False)}'"]
    ps = ' '.join(parts)
    r = subprocess.run(['powershell', '-Command', ps], capture_output=True, text=True, encoding='utf-8')
    out = r.stdout.strip()
    # Remove keyring line
    lines = [l for l in out.split('\n') if 'keyring' not in l.lower()]
    try:
        return json.loads('\n'.join(lines))
    except:
        print("RAW:", '\n'.join(lines))
        print("ERR:", r.stderr[:300])
        return None

# 1. 프레젠테이션 생성
print("프레젠테이션 생성 중...")
r = subprocess.run(
    ['powershell', '-Command', "gws slides presentations create --json '{\"title\": \"불고기 만들기 레시피\"}'"],
    capture_output=True, text=True, encoding='utf-8'
)
lines = [l for l in r.stdout.split('\n') if 'keyring' not in l.lower()]
data = json.loads('\n'.join(lines))
PRES_ID = data['presentationId']
SLIDE1_ID = data['slides'][0]['objectId']
print(f"Presentation ID: {PRES_ID}")
print(f"Slide 1 ID: {SLIDE1_ID}")

# 슬라이드 요소 ID 가져오기
elems = data['slides'][0]['pageElements']
title_id = None
body_id = None
for e in elems:
    ph = e.get('shape', {}).get('placeholder', {})
    if ph.get('type') == 'CENTERED_TITLE':
        title_id = e['objectId']
    elif ph.get('type') == 'SUBTITLE':
        body_id = e['objectId']
print(f"Title ID: {title_id}, Body ID: {body_id}")

# 2. 슬라이드 콘텐츠 정의
slides_content = [
    # 슬라이드 1: 표지 (이미 존재)
    None,
    # 슬라이드 2: 불고기란?
    {
        "layout": "TITLE_AND_BODY",
        "title": "불고기란?",
        "body": "• 불고기(不高記)는 대한민국을 대표하는 전통 소고기 요리\n• '불(fire) + 고기(meat)'의 합성어로 불에 구운 고기를 뜻함\n• 간장 기반 양념에 재워 부드럽고 달콤한 맛이 특징\n• 세계적으로 가장 잘 알려진 한국 음식 중 하나\n• 삼국시대 맥적(貊炙)에서 유래한 역사 깊은 음식"
    },
    # 슬라이드 3: 재료 (4인분)
    {
        "layout": "TITLE_AND_BODY",
        "title": "재료 안내 (4인분 기준)",
        "body": "[ 주재료 ]\n• 소고기 (등심 또는 채끝) 600g\n\n[ 양념장 ]\n• 간장 5큰술  •  설탕 2큰술  •  배즙 3큰술\n• 참기름 1큰술  •  다진 마늘 1큰술  •  다진 생강 1/2작은술\n• 후추 약간  •  참깨 1큰술\n\n[ 채소 ]\n• 양파 1/2개  •  대파 1대  •  표고버섯 3개  •  당근 1/4개"
    },
    # 슬라이드 4: 양념장 만들기
    {
        "layout": "TITLE_AND_BODY",
        "title": "양념장 만들기",
        "body": "① 배 1/4개를 강판에 갈아 즙을 내거나 배즙을 준비\n   → 단백질 분해 효소(파파인)가 고기를 부드럽게 만듦\n\n② 간장 5큰술 + 설탕 2큰술 + 배즙 3큰술을 잘 섞기\n\n③ 다진 마늘 1큰술 + 다진 생강 1/2작은술 추가\n\n④ 참기름 1큰술 + 후추 약간 + 참깨 1큰술 넣고 혼합\n\n⑤ 양념이 골고루 섞이도록 잘 저어주기\n   → Tip: 설탕 대신 꿀이나 조청 사용 시 더욱 윤기 있는 불고기 완성"
    },
    # 슬라이드 5: 고기 손질 & 재우기
    {
        "layout": "TITLE_AND_BODY",
        "title": "고기 손질 & 재우기",
        "body": "[ 고기 손질 ]\n① 소고기를 냉동 반해동 상태에서 최대한 얇게 (3~4mm) 썰기\n② 결 반대 방향으로 칼집을 넣어 질기지 않게 처리\n③ 키친타월로 핏물 제거\n\n[ 채소 손질 ]\n• 양파: 0.5cm 두께 채 썰기\n• 대파: 어슷썰기\n• 표고버섯: 밑동 제거 후 슬라이스\n• 당근: 얇게 채 썰기\n\n[ 재우기 ]\n• 고기 + 채소 + 양념을 볼에 넣고 조물조물 무치기\n• 냉장고에서 최소 30분~1시간 숙성 (하룻밤 추천)"
    },
    # 슬라이드 6: 조리 방법
    {
        "layout": "TITLE_AND_BODY",
        "title": "조리 방법",
        "body": "[ 팬 구이 방법 ]\n① 팬을 센 불로 달군 후 식용유를 두르기\n② 재워둔 불고기를 올리고 센 불에서 빠르게 볶기\n③ 고기가 익으면서 수분이 나오면 중불로 낮추기\n④ 양념이 고기에 잘 배도록 뒤적이며 2~3분 조리\n⑤ 참기름을 살짝 둘러 마무리\n\n[ 숯불 구이 방법 (전통) ]\n• 석쇠 또는 불판에 올려 숯불에 직화로 굽기\n• 연기의 향이 더해져 깊은 풍미 완성\n\n⚠ Tip: 팬에 너무 많이 담으면 찌개가 되므로 나눠서 조리!"
    },
    # 슬라이드 7: 플레이팅 & 곁들임
    {
        "layout": "TITLE_AND_BODY",
        "title": "플레이팅 & 곁들임 음식",
        "body": "[ 플레이팅 ]\n• 접시에 상추·깻잎을 깔고 불고기를 올리기\n• 참깨와 송송 썬 대파로 마무리 장식\n• 쌈장, 마늘, 고추를 함께 곁들여 제공\n\n[ 추천 곁들임 음식 ]\n• 공기밥: 달달한 불고기 양념이 밥도둑\n• 쌈 채소: 상추, 깻잎, 배추\n• 된장찌개: 국물 요리로 균형\n• 잡채: 잔치 분위기 연출\n• 나물 반찬: 시금치나물, 도라지나물\n\n[ 활용 메뉴 ]\n• 불고기 덮밥  •  불고기 김밥  •  불고기 피자  •  불고기 버거"
    },
    # 슬라이드 8: 영양 정보 & 마무리
    {
        "layout": "TITLE_AND_BODY",
        "title": "영양 정보 & 요리 완성 Tip",
        "body": "[ 1인분 기준 영양 정보 (약 150g) ]\n• 칼로리: 약 280~320 kcal\n• 단백질: 25g  •  지방: 12g  •  탄수화물: 18g\n• 철분, 아연, 비타민 B12 풍부\n\n[ 맛있는 불고기를 위한 핵심 Tip ]\n✓ 배즙 또는 키위즙으로 고기를 충분히 재울 것\n✓ 고기는 얇게 썰수록 맛이 좋음\n✓ 센 불에서 빠르게 볶아야 육즙이 살아있음\n✓ 양념에 사이다를 소량 추가하면 더욱 부드러움\n✓ 양파를 많이 넣을수록 단맛이 강해짐\n\n🍖 맛있는 한식 불고기 완성!"
    }
]

# 3. 표지 슬라이드 텍스트 입력
print("\n표지 슬라이드 텍스트 설정...")
batch = {
    "requests": [
        {"insertText": {"objectId": title_id, "text": "불고기 만들기 레시피", "insertionIndex": 0}},
        {"insertText": {"objectId": body_id, "text": "전통 한국 소고기 요리의 정석\n재료 선별부터 조리까지 완벽 가이드", "insertionIndex": 0}}
    ]
}

r = subprocess.run(
    ['powershell', '-Command',
     f"gws slides presentations batchUpdate --params '{{\"presentationId\":\"{PRES_ID}\"}}' --json '{json.dumps(batch, ensure_ascii=False)}'"],
    capture_output=True, text=True, encoding='utf-8'
)
print("표지 설정:", "OK" if r.returncode == 0 else r.stderr[:200])

# 4. 나머지 슬라이드 추가 (슬라이드 2~8)
for i, slide in enumerate(slides_content[1:], start=1):
    print(f"\n슬라이드 {i+1} 추가: {slide['title']}")

    # 슬라이드 생성
    create_req = {
        "requests": [{
            "createSlide": {
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": slide['layout']}
            }
        }]
    }
    r = subprocess.run(
        ['powershell', '-Command',
         f"gws slides presentations batchUpdate --params '{{\"presentationId\":\"{PRES_ID}\"}}' --json '{json.dumps(create_req, ensure_ascii=False)}'"],
        capture_output=True, text=True, encoding='utf-8'
    )
    lines = [l for l in r.stdout.split('\n') if 'keyring' not in l.lower()]
    try:
        resp = json.loads('\n'.join(lines))
        new_slide_id = resp['replies'][0]['createSlide']['objectId']
        print(f"  새 슬라이드 ID: {new_slide_id}")
    except Exception as e:
        print(f"  슬라이드 생성 실패: {e}\n  RAW: {r.stdout[:200]}")
        continue

    # 슬라이드 구조 조회
    # 프레젠테이션 전체 조회로 슬라이드 요소 파악
    r3 = subprocess.run(
        ['powershell', '-Command',
         f"gws slides presentations get --params '{{\"presentationId\":\"{PRES_ID}\"}}'"],
        capture_output=True, text=True, encoding='utf-8'
    )
    lines3 = [l for l in r3.stdout.split('\n') if 'keyring' not in l.lower()]
    pres_data = json.loads('\n'.join(lines3))

    # 해당 슬라이드 찾기
    target_slide = None
    for s in pres_data['slides']:
        if s['objectId'] == new_slide_id:
            target_slide = s
            break

    if not target_slide:
        print(f"  슬라이드를 찾을 수 없음")
        continue

    # 텍스트 요소 ID 찾기
    t_id = None
    b_id = None
    for e in target_slide.get('pageElements', []):
        ph = e.get('shape', {}).get('placeholder', {})
        ptype = ph.get('type', '')
        if ptype == 'TITLE':
            t_id = e['objectId']
        elif ptype in ('BODY', 'OBJECT'):
            b_id = e['objectId']

    print(f"  Title ID: {t_id}, Body ID: {b_id}")

    if not t_id:
        print("  제목 요소 없음, 건너뜀")
        continue

    # 텍스트 삽입
    text_reqs = []
    if t_id:
        text_reqs.append({"insertText": {"objectId": t_id, "text": slide['title'], "insertionIndex": 0}})
    if b_id and slide.get('body'):
        text_reqs.append({"insertText": {"objectId": b_id, "text": slide['body'], "insertionIndex": 0}})

    if text_reqs:
        text_batch = {"requests": text_reqs}
        r4 = subprocess.run(
            ['powershell', '-Command',
             f"gws slides presentations batchUpdate --params '{{\"presentationId\":\"{PRES_ID}\"}}' --json '{json.dumps(text_batch, ensure_ascii=False)}'"],
            capture_output=True, text=True, encoding='utf-8'
        )
        print(f"  텍스트 삽입: {'OK' if r4.returncode == 0 else r4.stderr[:200]}")

print(f"\n\n=== 완료 ===")
print(f"Presentation ID: {PRES_ID}")
print(f"링크: https://docs.google.com/presentation/d/{PRES_ID}/edit")
