#!/bin/bash
PRES_ID="1h9fJ01x6vPF5QMJjLlZ0j8fQFtS_LhYJGHDT9dOveos"
FOLDER_ID="1xFgTkZNU-voN_y7Y3gCuBUGn8EZV4wox"

gws_batch() {
    local json_file="$1"
    gws slides presentations batchUpdate \
        --params "{\"presentationId\":\"$PRES_ID\"}" \
        --json "$(cat $json_file)" 2>/dev/null
}

get_slide_elements() {
    local slide_id="$1"
    gws slides presentations get \
        --params "{\"presentationId\":\"$PRES_ID\"}" 2>/dev/null | \
    python -c "
import sys,json
d=json.load(sys.stdin)
for s in d['slides']:
    if s['objectId']=='$slide_id':
        for e in s.get('pageElements',[]):
            t=e.get('shape',{}).get('placeholder',{}).get('type','')
            if t=='TITLE': print('T:'+e['objectId'])
            elif t in ('BODY','OBJECT'): print('B:'+e['objectId'])
        break
"
}

echo "=== 표지 슬라이드 설정 ==="
cat > /tmp/cover.json << 'EOF'
{"requests":[
  {"insertText":{"objectId":"i0","text":"불고기 만들기 레시피","insertionIndex":0}},
  {"insertText":{"objectId":"i1","text":"전통 한국 소고기 요리의 정석\n재료 선별부터 조리까지 완벽 가이드","insertionIndex":0}}
]}
EOF
gws_batch /tmp/cover.json | python -c "import sys,json; d=json.load(sys.stdin); print('OK' if 'presentationId' in d else d)"

# 슬라이드 추가 함수
add_slide() {
    local idx=$1
    local title=$2
    local body=$3

    echo -e "\n[슬라이드 $((idx+1))] $title"

    # 1. 슬라이드 생성
    python -c "import json; print(json.dumps({'requests':[{'createSlide':{'insertionIndex':$idx,'slideLayoutReference':{'predefinedLayout':'TITLE_AND_BODY'}}}]}))" > /tmp/create.json
    local RESP=$(gws_batch /tmp/create.json)
    local NEW_ID=$(echo "$RESP" | python -c "import sys,json; d=json.load(sys.stdin); print(d['replies'][0]['createSlide']['objectId'])" 2>/dev/null)
    echo "  새 슬라이드 ID: $NEW_ID"

    sleep 1

    # 2. 요소 ID 조회
    local IDS=$(get_slide_elements "$NEW_ID")
    local T_ID=$(echo "$IDS" | grep "^T:" | sed 's/T://')
    local B_ID=$(echo "$IDS" | grep "^B:" | sed 's/B://')
    echo "  Title=$T_ID Body=$B_ID"

    # 3. 텍스트 삽입
    python -c "
import json,sys
reqs=[]
t_id='$T_ID'; b_id='$B_ID'
title='''$title'''
body='''$body'''
if t_id: reqs.append({'insertText':{'objectId':t_id,'text':title,'insertionIndex':0}})
if b_id: reqs.append({'insertText':{'objectId':b_id,'text':body,'insertionIndex':0}})
print(json.dumps({'requests':reqs}))
" > /tmp/text.json
    gws_batch /tmp/text.json | python -c "import sys,json; d=json.load(sys.stdin); print('  텍스트 OK' if 'presentationId' in d else '  ERR:'+str(d)[:100])" 2>/dev/null
    sleep 1
}

add_slide 1 "불고기란?" "• 불고기는 대한민국을 대표하는 전통 소고기 요리
• 불(fire) + 고기(meat)의 합성어로 불에 구운 고기를 뜻함
• 간장 기반 양념에 재워 부드럽고 달콤한 맛이 특징
• 세계적으로 가장 잘 알려진 한국 음식 중 하나
• 삼국시대 맥적에서 유래한 역사 깊은 음식"

add_slide 2 "재료 안내 (4인분 기준)" "[ 주재료 ]
소고기 (등심 또는 채끝) 600g

[ 양념장 ]
간장 5큰술 / 배즙 3큰술 / 설탕 2큰술
참기름 1큰술 / 다진 마늘 1큰술 / 참깨 1큰술

[ 채소 ]
양파 1/2개 / 대파 1대 / 표고버섯 3개 / 당근 1/4개"

add_slide 3 "양념장 만들기" "① 배 1/4개를 강판에 갈아 즙을 내거나 배즙 준비
② 간장 5큰술 + 설탕 2큰술 + 배즙 3큰술 잘 섞기
③ 다진 마늘 1큰술 + 다진 생강 1/2작은술 추가
④ 참기름 1큰술 + 후추 약간 + 참깨 1큰술 혼합
⑤ 재료가 골고루 섞이도록 잘 저어주기

Tip: 설탕 대신 꿀이나 조청 사용시 더욱 윤기 있는 불고기 완성"

add_slide 4 "고기 손질 & 재우기" "[ 고기 손질 ]
① 소고기를 반해동 상태에서 얇게 (3-4mm) 썰기
② 결 반대 방향으로 칼집을 넣어 부드럽게 처리
③ 키친타월로 핏물 제거

[ 채소 손질 ]
양파: 채 썰기 / 대파: 어슷썰기 / 표고버섯: 슬라이스

[ 재우기 ]
고기 + 채소 + 양념을 볼에 넣고 조물조물 무치기
냉장고에서 최소 30분~1시간 숙성 (하룻밤 추천)"

add_slide 5 "조리 방법" "[ 팬 구이 방법 ]
① 팬을 센 불로 달군 후 식용유 두르기
② 재워둔 불고기를 올리고 센 불에서 빠르게 볶기
③ 고기가 익으면 중불로 낮추기
④ 양념이 배도록 뒤적이며 2-3분 조리
⑤ 참기름을 살짝 둘러 마무리

[ 숯불 구이 방법 (전통) ]
석쇠 또는 불판에 올려 숯불에 직화로 굽기

Tip: 팬에 너무 많이 담으면 볶음이 아닌 찌개가 됩니다!"

add_slide 6 "플레이팅 & 곁들임" "[ 플레이팅 ]
접시에 상추/깻잎을 깔고 불고기를 올리기
참깨와 대파로 마무리 장식
쌈장, 마늘, 고추를 함께 곁들여 제공

[ 추천 곁들임 ]
공기밥 / 쌈 채소 (상추, 깻잎) / 된장찌개 / 나물 반찬

[ 활용 메뉴 ]
불고기 덮밥 / 불고기 김밥 / 불고기 피자 / 불고기 버거"

add_slide 7 "영양 정보 & 핵심 Tip" "[ 1인분 기준 영양 정보 (약 150g) ]
칼로리: 약 300 kcal
단백질: 25g / 지방: 12g / 탄수화물: 18g
철분, 아연, 비타민 B12 풍부

[ 맛있는 불고기를 위한 핵심 Tip ]
① 배즙으로 고기를 충분히 재울 것
② 고기는 얇게 썰수록 맛이 좋음
③ 센 불에서 빠르게 볶아야 육즙이 살아있음
④ 사이다 소량 추가시 더욱 부드러움
⑤ 양파를 많이 넣을수록 단맛이 강해짐"

echo ""
echo "=== Drive 폴더 이동 및 권한 설정 ==="
gws drive files update \
    --params "{\"fileId\":\"$PRES_ID\",\"addParents\":\"$FOLDER_ID\",\"removeParents\":\"root\",\"fields\":\"id,parents\"}" \
    --json '{}' 2>/dev/null | python -c "import sys,json; d=json.load(sys.stdin); print('폴더 이동 OK: agent 폴더')"

gws drive permissions create \
    --params "{\"fileId\":\"$PRES_ID\"}" \
    --json '{"role":"reader","type":"anyone"}' 2>/dev/null | python -c "import sys,json; d=json.load(sys.stdin); print('권한 설정 OK:', d.get('type',''))"

echo ""
echo "=== 최종 완료 ==="
echo "Presentation ID: $PRES_ID"
echo "링크: https://docs.google.com/presentation/d/$PRES_ID/edit"
