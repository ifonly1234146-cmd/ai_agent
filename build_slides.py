import subprocess, json, sys, time

PRES_ID = "1h9fJ01x6vPF5QMJjLlZ0j8fQFtS_LhYJGHDT9dOveos"
FOLDER_ID = "1xFgTkZNU-voN_y7Y3gCuBUGn8EZV4wox"

def gws_run(args_str):
    cmd = f'gws {args_str}'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    out = '\n'.join([l for l in r.stdout.split('\n') if 'keyring' not in l.lower()])
    try:
        return json.loads(out), None
    except:
        return None, r.stderr[:300] + out[:300]

def batch_update(requests):
    payload = json.dumps({"requests": requests}, ensure_ascii=False)
    # Write to temp file to avoid encoding issues
    with open('C:/Users/SBS/Desktop/agent02/tmp_batch.json', 'w', encoding='utf-8') as f:
        f.write(payload)
    r = subprocess.run(
        f'gws slides presentations batchUpdate --params \'{{"presentationId":"{PRES_ID}"}}\' --json @C:/Users/SBS/Desktop/agent02/tmp_batch.json',
        shell=True, capture_output=True, text=True, encoding='utf-8'
    )
    out = '\n'.join([l for l in r.stdout.split('\n') if 'keyring' not in l.lower()])
    try:
        return json.loads(out)
    except:
        # Try another way - pipe the json
        r2 = subprocess.run(
            ['gws', 'slides', 'presentations', 'batchUpdate',
             '--params', f'{{"presentationId":"{PRES_ID}"}}',
             '--json', payload],
            capture_output=True, text=True, encoding='utf-8'
        )
        out2 = '\n'.join([l for l in r2.stdout.split('\n') if 'keyring' not in l.lower()])
        try:
            return json.loads(out2)
        except:
            print(f"  BatchUpdate error: {r2.stderr[:200]}")
            return None

def get_pres():
    r = subprocess.run(
        ['gws', 'slides', 'presentations', 'get',
         '--params', f'{{"presentationId":"{PRES_ID}"}}'],
        capture_output=True, text=True, encoding='utf-8'
    )
    out = '\n'.join([l for l in r.stdout.split('\n') if 'keyring' not in l.lower()])
    return json.loads(out)

# 표지 텍스트 확인 및 설정 (이미 했지만 재확인)
print("현재 프레젠테이션 상태 확인...")
pres = get_pres()
print(f"현재 슬라이드 수: {len(pres['slides'])}")

# 표지 슬라이드 텍스트 설정
print("\n[표지] 텍스트 설정 중...")
resp = batch_update([
    {"deleteText": {"objectId": "i0", "textRange": {"type": "ALL"}}},
    {"deleteText": {"objectId": "i1", "textRange": {"type": "ALL"}}},
])
resp = batch_update([
    {"insertText": {"objectId": "i0", "text": "불고기 만들기 레시피", "insertionIndex": 0}},
    {"insertText": {"objectId": "i1", "text": "전통 한국 소고기 요리의 정석\n재료 선별부터 조리까지 완벽 가이드", "insertionIndex": 0}},
])
print(f"  결과: {'OK' if resp and 'presentationId' in resp else resp}")

# 슬라이드 내용 정의
slides = [
    ("불고기란?",
     "• 불고기는 대한민국을 대표하는 전통 소고기 요리\n• 불(fire) + 고기(meat)의 합성어, 불에 구운 고기\n• 간장 기반 양념에 재워 부드럽고 달콤한 맛\n• 세계적으로 가장 잘 알려진 한국 음식 중 하나\n• 삼국시대 맥적(貊炙)에서 유래한 역사 깊은 음식"),
    ("재료 안내 (4인분 기준)",
     "[ 주재료 ]\n소고기 (등심 또는 채끝) 600g\n\n[ 양념장 ]\n간장 5큰술 / 배즙 3큰술 / 설탕 2큰술\n참기름 1큰술 / 다진 마늘 1큰술 / 참깨 1큰술\n다진 생강 1/2작은술 / 후추 약간\n\n[ 채소 ]\n양파 1/2개 / 대파 1대 / 표고버섯 3개 / 당근 1/4개"),
    ("양념장 만들기",
     "① 배 1/4개를 강판에 갈아 즙을 내거나 배즙 준비\n   (단백질 분해 효소가 고기를 부드럽게 만듦)\n\n② 간장 5큰술 + 설탕 2큰술 + 배즙 3큰술 잘 섞기\n\n③ 다진 마늘 1큰술 + 다진 생강 1/2작은술 추가\n\n④ 참기름 1큰술 + 후추 + 참깨 1큰술 혼합\n\nTip: 설탕 대신 꿀이나 조청 사용시 더욱 윤기 있는 불고기 완성"),
    ("고기 손질 & 재우기",
     "[ 고기 손질 ]\n① 소고기를 반해동 상태에서 얇게 (3~4mm) 썰기\n② 결 반대 방향으로 칼집을 넣어 부드럽게 처리\n③ 키친타월로 핏물 제거\n\n[ 채소 손질 ]\n양파: 채 썰기 / 대파: 어슷썰기 / 표고버섯: 슬라이스\n\n[ 재우기 ]\n고기 + 채소 + 양념을 볼에 넣고 조물조물 무치기\n냉장고에서 최소 30분~1시간 숙성 (하룻밤 추천)"),
    ("조리 방법",
     "[ 팬 구이 방법 ]\n① 팬을 센 불로 달군 후 식용유 두르기\n② 재워둔 불고기를 올리고 센 불에서 빠르게 볶기\n③ 고기가 익으면 중불로 낮추기\n④ 양념이 배도록 뒤적이며 2~3분 조리\n⑤ 참기름을 살짝 둘러 마무리\n\n[ 숯불 구이 방법 (전통) ]\n석쇠 또는 불판에 올려 숯불에 직화로 굽기\n\nTip: 팬에 너무 많이 담으면 찌개가 되므로 나눠서 조리!"),
    ("플레이팅 & 곁들임 음식",
     "[ 플레이팅 ]\n접시에 상추/깻잎을 깔고 불고기를 올리기\n참깨와 대파로 마무리 장식\n쌈장, 마늘, 고추를 함께 곁들여 제공\n\n[ 추천 곁들임 ]\n공기밥 / 쌈 채소 (상추, 깻잎) / 된장찌개 / 나물 반찬\n\n[ 활용 메뉴 ]\n불고기 덮밥 / 불고기 김밥 / 불고기 피자 / 불고기 버거"),
    ("영양 정보 & 핵심 Tip",
     "[ 1인분 기준 영양 정보 (약 150g) ]\n칼로리: 약 300 kcal\n단백질: 25g / 지방: 12g / 탄수화물: 18g\n철분, 아연, 비타민 B12 풍부\n\n[ 맛있는 불고기를 위한 핵심 Tip ]\n① 배즙으로 고기를 충분히 재울 것\n② 고기는 얇게 썰수록 맛이 좋음\n③ 센 불에서 빠르게 볶아야 육즙 살아있음\n④ 사이다 소량 추가시 더욱 부드러움\n⑤ 양파 많이 넣을수록 단맛 강해짐"),
]

# 슬라이드 2~8 생성
for i, (title, body) in enumerate(slides):
    print(f"\n[슬라이드 {i+2}] {title}")

    # 슬라이드 생성
    create_resp = batch_update([{
        "createSlide": {
            "insertionIndex": i + 1,
            "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"}
        }
    }])

    if not create_resp or not create_resp.get('replies'):
        print(f"  슬라이드 생성 실패: {create_resp}")
        continue

    new_slide_id = create_resp['replies'][0]['createSlide']['objectId']
    print(f"  슬라이드 ID: {new_slide_id}")
    time.sleep(0.5)

    # 프레젠테이션 재조회
    pres = get_pres()
    target = next((s for s in pres['slides'] if s['objectId'] == new_slide_id), None)
    if not target:
        print("  슬라이드 찾기 실패")
        continue

    # 요소 ID 추출
    t_id = b_id = None
    for e in target.get('pageElements', []):
        ptype = e.get('shape', {}).get('placeholder', {}).get('type', '')
        if ptype == 'TITLE':
            t_id = e['objectId']
        elif ptype in ('BODY', 'OBJECT'):
            b_id = e['objectId']

    print(f"  Title ID: {t_id}, Body ID: {b_id}")

    # 텍스트 삽입
    reqs = []
    if t_id:
        reqs.append({"insertText": {"objectId": t_id, "text": title, "insertionIndex": 0}})
    if b_id:
        reqs.append({"insertText": {"objectId": b_id, "text": body, "insertionIndex": 0}})

    if reqs:
        text_resp = batch_update(reqs)
        print(f"  텍스트: {'OK' if text_resp and 'presentationId' in text_resp else text_resp}")
    time.sleep(0.5)

# Drive에 agent 폴더로 이동
print(f"\n\n=== Drive 폴더 이동 ===")
r = subprocess.run(
    ['gws', 'drive', 'files', 'update',
     '--params', f'{{"fileId":"{PRES_ID}","addParents":"{FOLDER_ID}","removeParents":"root","fields":"id,parents"}}',
     '--json', '{}'],
    capture_output=True, text=True, encoding='utf-8'
)
print("폴더 이동:", "OK" if r.returncode == 0 else r.stderr[:200])

# 공유 권한 설정
r2 = subprocess.run(
    ['gws', 'drive', 'permissions', 'create',
     '--params', f'{{"fileId":"{PRES_ID}"}}',
     '--json', '{"role":"reader","type":"anyone"}'],
    capture_output=True, text=True, encoding='utf-8'
)
out2 = '\n'.join([l for l in r2.stdout.split('\n') if 'keyring' not in l.lower()])
print("권한 설정:", "OK" if 'anyoneWithLink' in out2 else out2[:200])

print(f"\n=== 완료 ===")
print(f"링크: https://docs.google.com/presentation/d/{PRES_ID}/edit")
