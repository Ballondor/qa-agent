# 테스트 시나리오 문서

> 생성일: 2026-02-27 03:00:25 UTC
> 버전: v1
## 요약

| Epic | TC 수 | 긍정 | 부정 |
|------|-------|------|------|
| Epic A: 여론조사 데이터 시각화 서비스 | 73 | 45 | 28 |
| Epic B: 콘텐트 성과 분석 통계 | 33 | 25 | 8 |
| Epic C: 시스템 설정 | 25 | 18 | 7 |
| Epic D: 인증 및 공통 | 21 | 14 | 7 |
| **합계** | **152** | | |

---


# Epic A: 여론조사 데이터 시각화 서비스

- **테스트 대상 URL**: https://metaj.jtbc.co.kr
- **테스트 케이스**: 73개 (긍정: 45, 부정: 28)

## TC-A-0-01-P01: [긍정] 선거 정보 정상 등록

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 선거가 정상 등록되고 고유번호가 생성됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-election-button"]') | 선거 등록 모달/폼이 표시됨 |
| 3 | playwright_fill('input[name="election-name"]', '제21대 대통령선거') | 선거명 입력 필드에 텍스트가 입력됨 |
| 4 | playwright_fill('input[name="election-date"]', '2024-03-09') | 선거일이 입력됨 |
| 5 | playwright_select('select[name="election-type"]', '대선') | 선거타입이 '대선'으로 선택됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.success-message') | 성공 메시지가 표시됨 |
| 8 | playwright_get_text('.election-id') | 선거고유번호가 자동 생성되어 표시됨 |

---

## TC-A-0-01-N01: [부정] 선거명 미입력 시 저장 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 선거명 필수값 입력 안내 메시지가 표시되고 저장이 차단됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-election-button"]') | 선거 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="election-date"]', '2024-03-09') | 선거일만 입력됨 |
| 4 | playwright_select('select[name="election-type"]', '대선') | 선거타입만 선택됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | '필수값 입력 안내 메시지'가 표시됨 |
| 7 | playwright_get_text('.error-message') | 선거명 필수 입력 안내 메시지 텍스트 확인 |

---

## TC-A-0-01-N02: [부정] 선거일 미선택 시 저장 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 선거일 필수값 입력 안내 메시지가 표시되고 저장이 차단됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-election-button"]') | 선거 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="election-name"]', '제21대 대통령선거') | 선거명이 입력됨 |
| 4 | playwright_select('select[name="election-type"]', '대선') | 선거타입만 선택됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 선거일 필수값 입력 안내 메시지가 표시됨 |

---

## TC-A-0-01-N03: [부정] 선거타입 미선택 시 저장 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 선거타입 필수값 입력 안내 메시지가 표시되고 저장이 차단됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-election-button"]') | 선거 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="election-name"]', '제21대 대통령선거') | 선거명이 입력됨 |
| 4 | playwright_fill('input[name="election-date"]', '2024-03-09') | 선거일이 입력됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 선거타입 필수값 입력 안내 메시지가 표시됨 |

---

## TC-A-0-01-N04: [부정] 중복 선거명 등록 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 중복 선거명 경고가 표시되고 저장이 차단됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- '제21대 대통령선거'라는 이름의 선거가 이미 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-election-button"]') | 선거 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="election-name"]', '제21대 대통령선거') | 기존과 동일한 선거명이 입력됨 |
| 4 | playwright_fill('input[name="election-date"]', '2024-03-09') | 선거일이 입력됨 |
| 5 | playwright_select('select[name="election-type"]', '대선') | 선거타입이 선택됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.warning-message') | 중복 경고 메시지가 표시됨 |

---

## TC-A-0-01-P02: [긍정] 등록된 선거 목록 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 등록된 모든 선거가 목록에 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 1개 이상의 선거가 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_wait_for_selector('.election-list') | 선거 목록이 표시됨 |
| 3 | playwright_query_selector_all('.election-item') | 등록된 선거들이 리스트 아이템으로 표시됨 |
| 4 | playwright_get_text('.election-item:first-child .election-name') | 첫 번째 선거의 선거명이 표시됨 |

---

## TC-A-0-02-P01: [긍정] 선거 목록 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 등록된 모든 선거가 리스트로 정상 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 2개 이상의 선거가 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_wait_for_selector('.election-list') | 선거 목록 컨테이너가 표시됨 |
| 3 | playwright_query_selector_all('.election-item') | 등록된 모든 선거가 리스트로 표시됨 |

---

## TC-A-0-02-P02: [긍정] 선거 정보 수정

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 선거 정보가 정상적으로 수정됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 수정 가능한 선거가 1개 이상 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('.election-item:first-child') | 첫 번째 선거가 선택됨 |
| 3 | playwright_click('button[data-testid="edit-election-button"]') | 수정 버튼이 클릭되고 편집 모드로 전환됨 |
| 4 | playwright_fill('input[name="election-name"]', '제21대 대통령선거(수정)') | 선거명이 수정됨 |
| 5 | playwright_fill('input[name="election-date"]', '2024-03-10') | 선거일이 수정됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.success-message') | 수정 성공 메시지가 표시됨 |

---

## TC-A-0-02-N01: [부정] 하위 데이터 존재 시 선거 삭제 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 하위 데이터 존재 시 삭제 불가 경고가 표시되고 삭제가 차단됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거에 연결된 정당/후보자/여론조사 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('.election-item:first-child') | 하위 데이터가 있는 선거가 선택됨 |
| 3 | playwright_click('button[data-testid="delete-election-button"]') | 삭제 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.warning-message') | 삭제 불가 경고 메시지가 표시됨 |
| 5 | playwright_get_text('.warning-message') | 하위 데이터 존재로 인한 삭제 불가 안내 텍스트 확인 |

---

## TC-A-0-02-P03: [긍정] 하위 데이터 없는 선거 삭제

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 하위 데이터가 없는 선거가 정상적으로 삭제됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 하위 데이터가 없는 선거가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('.election-item[data-has-children="false"]') | 하위 데이터가 없는 선거가 선택됨 |
| 3 | playwright_click('button[data-testid="delete-election-button"]') | 삭제 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.confirm-dialog') | 삭제 확인 다이얼로그가 표시됨 |
| 5 | playwright_click('button[data-testid="confirm-delete"]') | 삭제 확인 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.success-message') | 삭제 성공 메시지가 표시됨 |

---

## TC-A-0-03-P01: [긍정] 선거 선택 후 하위 데이터 관리 진입

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 선거 선택 후 해당 선거의 데이터만 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 1개 이상 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('.election-item:first-child') | 특정 선거가 선택됨 |
| 3 | playwright_click('a[href="/admin/data"]') | 데이터 관리 메뉴가 클릭됨 |
| 4 | playwright_wait_for_selector('.selected-election-info') | 선택된 선거 정보가 표시됨 |
| 5 | playwright_get_attribute('.data-list', 'data-election-id') | 데이터 목록이 선택된 선거에 속한 것만 필터링되어 표시됨 |

---

## TC-A-0-03-N01: [부정] 선거 미선택 시 하위 관리 진입

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 선거 미선택 시 선거 선택 안내 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되지 않은 상태

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지로 직접 접근 시도 |
| 2 | playwright_wait_for_selector('.info-message') | 선거 선택 안내 메시지가 표시됨 |
| 3 | playwright_get_text('.info-message') | '선거를 먼저 선택해주세요' 안내 메시지 확인 |

---

## TC-A-0-03-P02: [긍정] 선거 전환 시 데이터 분리 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 선거 전환 시 이전 선거의 데이터는 표시되지 않음 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거 A와 선거 B가 각각 등록되어 있음
- 선거 A에 정당이 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/election') | 선거 관리 페이지가 로드됨 |
| 2 | playwright_click('.election-item[data-election-name="선거A"]') | 선거 A가 선택됨 |
| 3 | playwright_click('a[href="/admin/party"]') | 정당 관리 페이지로 이동 |
| 4 | playwright_query_selector_all('.party-item') | 선거 A의 정당 목록이 표시됨 |
| 5 | playwright_click('button[data-testid="change-election"]') | 선거 변경 버튼 클릭 |
| 6 | playwright_click('.election-item[data-election-name="선거B"]') | 선거 B로 전환됨 |
| 7 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지 재로드 |
| 8 | playwright_query_selector_all('.party-item') | 선거 A의 정당이 표시되지 않음 |

---

## TC-A-1-01-P01: [긍정] XLSX 파일 정상 업로드

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | XLSX 파일이 정상적으로 업로드되고 확인 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 정상적인 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | '정당 지지율' 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/party-support.xlsx') | 파일 선택 다이얼로그에서 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.success-message', {timeout: 10000}) | 10초 이내에 업로드 성공 메시지가 표시됨 |
| 6 | playwright_get_text('.success-message') | 파일 업로드 성공 확인 메시지 확인 |

---

## TC-A-1-01-N01: [부정] 카테고리 미선택 시 업로드 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 카테고리 미선택 시 안내 메시지가 표시되고 업로드가 차단됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_set_input_files('input[type="file"]', './test-data/party-support.xlsx') | 파일만 선택됨 |
| 3 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.error-message') | 카테고리 선택 필수 안내 메시지가 표시됨 |

---

## TC-A-1-01-N02: [부정] 잘못된 파일 형식 업로드 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | xlsx가 아닌 파일 업로드 시 오류 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- .pdf 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | 정당 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/wrong-file.pdf') | PDF 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.error-message') | 파일 형식 오류 메시지가 표시됨 |
| 6 | playwright_get_text('.error-message') | '파일 형식이 잘못되었습니다.' 메시지 확인 |

---

## TC-A-1-01-N03: [부정] 빈 파일 업로드 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 빈 파일 업로드 시 필수 데이터 없음 오류가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 빈 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="candidate"]') | 후보자 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/empty-file.xlsx') | 빈 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.error-message') | 필수 데이터 없음 오류 메시지가 표시됨 |
| 6 | playwright_get_text('.error-message') | '필수 데이터가 없습니다.' 메시지 확인 |

---

## TC-A-1-01-P02: [긍정] 파일 업로드 버전 관리 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 파일 업로드 후 새 버전으로 등록되어 이력이 관리됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 정상적인 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | 정당 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/party-support-v1.xlsx') | 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.success-message') | 업로드 성공 메시지가 표시됨 |
| 6 | playwright_click('a[href="/admin/data/versions"]') | 버전 목록 페이지로 이동 |
| 7 | playwright_wait_for_selector('.version-list') | 버전 목록이 표시됨 |
| 8 | playwright_get_text('.version-item:first-child .version-number') | 새 버전 번호가 표시됨 |
| 9 | playwright_get_text('.version-item:first-child .upload-date') | 업로드 일시가 표시됨 |

---

## TC-A-1-02-P01: [긍정] 정당 지지율 파일 유효성 검사 통과

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모든 유효성 검사를 통과하고 성공 메시지와 데이터 요약이 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있고 필수 컬럼(date, party1~party8)이 설정되어 있음
- 올바른 정당 지지율 .xlsx 파일이 업로드됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | 정당 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/valid-party-support.xlsx') | 올바른 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.validation-result') | 유효성 검사 결과가 표시됨 |
| 6 | playwright_get_text('.validation-result .status') | '검증 성공' 메시지 확인 |
| 7 | playwright_get_text('.validation-result .data-summary') | 데이터 요약(행 수, 기간) 정보가 표시됨 |

---

## TC-A-1-02-N01: [부정] 필수 컬럼 누락된 파일 업로드

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 필수 컬럼 누락 시 오류 메시지와 누락 컬럼명이 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 필수 컬럼이 누락된 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | 정당 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/missing-column.xlsx') | 필수 컬럼이 누락된 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.error-message') | 필수 데이터 없음 오류가 표시됨 |
| 6 | playwright_get_text('.error-message') | '필수 데이터가 없습니다.' 메시지와 누락 컬럼명 확인 |

---

## TC-A-1-02-N02: [부정] 잘못된 날짜 형식 파일 업로드

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 잘못된 날짜 형식 발견 시 오류 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 날짜 컬럼에 잘못된 형식이 있는 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="candidate"]') | 후보자 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/invalid-date-format.xlsx') | 잘못된 날짜 형식 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.error-message') | 날짜 형식 오류 메시지가 표시됨 |
| 6 | playwright_get_text('.error-message') | '날짜 형식이 잘못되었습니다.' 메시지 확인 |

---

## TC-A-1-02-N03: [부정] 수치 데이터에 문자열 포함된 파일 업로드

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 수치 데이터에 문자열 포함 시 셀 위치와 함께 오류가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 수치 컬럼에 문자열이 포함된 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | 정당 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/string-in-numeric.xlsx') | 문자열 포함 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.error-message') | 수치 데이터 오류 메시지가 표시됨 |
| 6 | playwright_get_text('.error-message') | 해당 셀 위치와 함께 오류 내용이 표시됨 |

---

## TC-A-1-02-N04: [부정] 수치 범위 초과 데이터 파일 업로드

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 수치 데이터 범위 초과 시 경고가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 수치 데이터가 0~1 범위를 벗어난 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="candidate"]') | 후보자 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/out-of-range.xlsx') | 범위 초과 데이터 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.warning-message') | 범위 초과 경고 메시지가 표시됨 |
| 6 | playwright_get_text('.warning-message') | 범위 초과 경고 내용 확인 |

---

## TC-A-1-02-N05: [부정] 중복 날짜 데이터 파일 업로드

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 중복 날짜 발견 시 경고가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 중복된 날짜 데이터가 있는 .xlsx 파일이 준비되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('input[type="radio"][value="party"]') | 정당 지지율 카테고리가 선택됨 |
| 3 | playwright_set_input_files('input[type="file"]', './test-data/duplicate-date.xlsx') | 중복 날짜 파일이 선택됨 |
| 4 | playwright_click('button[data-testid="upload-button"]') | 업로드 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.warning-message') | 중복 날짜 경고 메시지가 표시됨 |
| 6 | playwright_get_text('.warning-message') | 중복 날짜 경고 내용 확인 |

---

## TC-A-1-03-P01: [긍정] 정당 지지율 데이터 미리보기

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 정당 지지율 그래프가 FO와 동일한 형태로 미리보기됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 정당 지지율 카테고리로 파일이 성공적으로 업로드됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="preview-button"]') | 미리보기 버튼이 클릭됨 |
| 3 | playwright_wait_for_selector('.preview-chart', {timeout: 1000}) | 1초 이내에 미리보기 그래프가 표시됨 |
| 4 | playwright_get_attribute('.preview-chart', 'data-category') | 'party' 카테고리 그래프가 표시됨 |
| 5 | playwright_query_selector('.preview-chart canvas') | FO와 동일한 형태의 그래프가 렌더링됨 |

---

## TC-A-1-03-P02: [긍정] 후보자 지지율 데이터 미리보기

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 후보자 지지율 그래프가 FO와 동일한 형태로 미리보기됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 후보자 지지율 카테고리로 파일이 성공적으로 업로드됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="preview-button"]') | 미리보기 버튼이 클릭됨 |
| 3 | playwright_wait_for_selector('.preview-chart', {timeout: 1000}) | 1초 이내에 미리보기 그래프가 표시됨 |
| 4 | playwright_get_attribute('.preview-chart', 'data-category') | 'candidate' 카테고리 그래프가 표시됨 |

---

## TC-A-1-03-P03: [긍정] 미리보기 필터 변경

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 필터 변경 시 해당 필터에 맞는 데이터로 그래프가 갱신됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 미리보기 화면이 표시되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_wait_for_selector('.preview-chart') | 미리보기 그래프가 표시됨 |
| 2 | playwright_click('button[data-filter="gender"]') | 성별 필터가 클릭됨 |
| 3 | playwright_click('button[data-filter-value="male"]') | '남성' 필터가 선택됨 |
| 4 | playwright_wait_for_selector('.preview-chart.updated', {timeout: 1000}) | 1초 이내에 그래프가 갱신됨 |
| 5 | playwright_get_attribute('.preview-chart', 'data-current-filter') | 남성 필터가 적용된 데이터로 그래프가 표시됨 |

---

## TC-A-1-03-N01: [부정] 오류 데이터 미리보기 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 데이터 오류 시 오류 영역이 dimmed되고 안내 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 유효성 검사에서 오류가 발견된 데이터가 업로드됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data') | 데이터 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="preview-button"]') | 미리보기 버튼이 클릭됨 |
| 3 | playwright_wait_for_selector('.preview-chart') | 미리보기 화면이 표시됨 |
| 4 | playwright_query_selector('.error-area.dimmed') | 오류 영역이 dimmed 처리됨 |
| 5 | playwright_get_text('.error-message') | 오류 안내 메시지가 표시됨 |

---

## TC-A-1-04-P01: [긍정] 데이터 버전 목록 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 업로드 일시, 버전 번호, 미리보기 상태가 정상 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음
- 데이터가 1회 이상 업로드됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data/versions') | 버전 관리 페이지가 로드됨 |
| 2 | playwright_wait_for_selector('.version-list') | 버전 목록이 표시됨 |
| 3 | playwright_get_text('.version-item:first-child .upload-date') | 업로드 일시가 표시됨 |
| 4 | playwright_get_text('.version-item:first-child .version-number') | 버전 번호가 표시됨 |
| 5 | playwright_get_text('.version-item:first-child .status') | '미리보기(preview)' 상태가 표시됨 |

---

## TC-A-1-04-P02: [긍정] 데이터 버전 게시(publish)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 미리보기 버전을 게시하면 FO에 해당 데이터가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 미리보기 상태의 버전이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data/versions') | 버전 관리 페이지가 로드됨 |
| 2 | playwright_click('.version-item[data-status="preview"]:first-child') | 미리보기 상태의 버전이 선택됨 |
| 3 | playwright_click('button[data-testid="publish-button"]') | 게시 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.success-message') | 게시 성공 메시지가 표시됨 |
| 5 | playwright_get_attribute('.version-item:first-child', 'data-status') | 상태가 'published'로 변경됨 |
| 6 | playwright_navigate('https://metaj.jtbc.co.kr') | FO 메인 페이지로 이동 |
| 7 | playwright_wait_for_selector('.chart-container') | 게시된 버전의 데이터가 FO에 표시됨 |

---

## TC-A-1-04-P03: [긍정] 다른 버전 게시 시 이전 버전 미리보기 전환

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 새 버전 게시 시 이전 버전이 미리보기 상태로 전환됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 게시 상태의 버전 A가 존재함
- 미리보기 상태의 버전 B가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data/versions') | 버전 관리 페이지가 로드됨 |
| 2 | playwright_get_attribute('.version-item[data-version="A"]', 'data-status') | 버전 A의 상태가 'published'임을 확인 |
| 3 | playwright_click('.version-item[data-version="B"]') | 버전 B가 선택됨 |
| 4 | playwright_click('button[data-testid="publish-button"]') | 버전 B 게시 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.success-message') | 게시 성공 메시지가 표시됨 |
| 6 | playwright_get_attribute('.version-item[data-version="A"]', 'data-status') | 버전 A의 상태가 'preview'로 변경됨 |
| 7 | playwright_get_attribute('.version-item[data-version="B"]', 'data-status') | 버전 B의 상태가 'published'로 변경됨 |

---

## TC-A-1-04-P04: [긍정] 이전 버전으로 롤백

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 이전 버전 선택 후 게시하면 FO 데이터가 해당 버전으로 롤백됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 버전 A(미리보기)와 버전 B(게시)가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data/versions') | 버전 관리 페이지가 로드됨 |
| 2 | playwright_click('.version-item[data-version="A"]') | 이전 버전 A가 선택됨 |
| 3 | playwright_click('button[data-testid="publish-button"]') | 버전 A 게시 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.success-message') | 게시 성공 메시지가 표시됨 |
| 5 | playwright_navigate('https://metaj.jtbc.co.kr') | FO 메인 페이지로 이동 |
| 6 | playwright_wait_for_selector('.chart-container') | 버전 A의 데이터가 FO에 표시됨(롤백 완료) |

---

## TC-A-1-04-N01: [부정] 미저장 상태로 페이지 이탈 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 미저장 상태로 페이지 이탈 시 저장 확인 알림이 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 버전의 게시 상태를 변경했으나 저장하지 않음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/data/versions') | 버전 관리 페이지가 로드됨 |
| 2 | playwright_click('.version-item:first-child') | 버전이 선택됨 |
| 3 | playwright_click('button[data-testid="publish-button"]') | 게시 버튼이 클릭됨(저장하지 않음) |
| 4 | playwright_click('a[href="/admin/party"]') | 다른 페이지로 이동 시도 |
| 5 | playwright_wait_for_selector('.confirm-dialog') | 변경사항 저장 확인 알림이 표시됨 |
| 6 | playwright_get_text('.confirm-dialog') | '변경사항을 저장하지 않았습니다' 메시지 확인 |

---

## TC-A-2-01-P01: [긍정] 특정 시점 추가

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 시점이 정상 등록되고 FO 그래프에 마커가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/timepoint') | 시점 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-timepoint-button"]') | 시점 추가 폼이 표시됨 |
| 3 | playwright_fill('input[name="timepoint-name"]', '공식 선거운동 시작') | 시점명이 입력됨 |
| 4 | playwright_click('input[name="timepoint-date"]') | 캘린더가 표시됨 |
| 5 | playwright_click('.calendar-day[data-date="2024-02-15"]') | 날짜가 선택됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.success-message') | 시점 등록 성공 메시지가 표시됨 |
| 8 | playwright_navigate('https://metaj.jtbc.co.kr/party') | FO 정당 지지율 페이지로 이동 |
| 9 | playwright_wait_for_selector('.timepoint-marker[data-date="2024-02-15"]') | 해당 날짜에 시점 마커가 표시됨 |

---

## TC-A-2-01-N01: [부정] 시점명 미입력 시 저장 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 시점명 미입력 시 필수값 입력 안내 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 시점 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/timepoint') | 시점 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-timepoint-button"]') | 시점 추가 폼이 표시됨 |
| 3 | playwright_click('input[name="timepoint-date"]') | 캘린더가 표시됨 |
| 4 | playwright_click('.calendar-day[data-date="2024-02-15"]') | 날짜만 선택됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 필수값 입력 안내 메시지가 표시됨 |

---

## TC-A-2-01-N02: [부정] 날짜 미선택 시 저장 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 날짜 미선택 시 필수 안내 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 시점 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/timepoint') | 시점 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-timepoint-button"]') | 시점 추가 폼이 표시됨 |
| 3 | playwright_fill('input[name="timepoint-name"]', '공식 선거운동 시작') | 시점명만 입력됨 |
| 4 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 5 | playwright_wait_for_selector('.error-message') | 날짜 선택 필수 안내 메시지가 표시됨 |

---

## TC-A-2-01-N03: [부정] 중복 날짜에 시점 추가 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 동일 날짜 시점 추가 시 중복 경고가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 2024-02-15에 이미 시점이 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/timepoint') | 시점 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-timepoint-button"]') | 시점 추가 폼이 표시됨 |
| 3 | playwright_fill('input[name="timepoint-name"]', '후보 등록 마감') | 다른 시점명이 입력됨 |
| 4 | playwright_click('input[name="timepoint-date"]') | 캘린더가 표시됨 |
| 5 | playwright_click('.calendar-day[data-date="2024-02-15"]') | 기존 시점과 동일한 날짜가 선택됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.warning-message') | 중복 경고 메시지가 표시됨 |

---

## TC-A-2-01-P02: [긍정] 시점 수정 및 삭제

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 시점 정보가 정상적으로 수정 및 삭제됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 시점이 1개 이상 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/timepoint') | 시점 관리 페이지가 로드됨 |
| 2 | playwright_click('.timepoint-item:first-child') | 첫 번째 시점이 선택됨 |
| 3 | playwright_click('button[data-testid="edit-timepoint-button"]') | 수정 버튼이 클릭됨 |
| 4 | playwright_fill('input[name="timepoint-name"]', '공식 선거운동 시작(수정)') | 시점명이 수정됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.success-message') | 수정 성공 메시지가 표시됨 |
| 7 | playwright_click('button[data-testid="delete-timepoint-button"]') | 삭제 버튼이 클릭됨 |
| 8 | playwright_wait_for_selector('.confirm-dialog') | 삭제 확인 다이얼로그가 표시됨 |
| 9 | playwright_click('button[data-testid="confirm-delete"]') | 삭제 확인 버튼이 클릭됨 |
| 10 | playwright_wait_for_selector('.success-message') | 삭제 성공 메시지가 표시됨 |

---

## TC-A-3-01-P01: [긍정] 정당 정보 정상 등록

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 정당이 정상 등록되고 목록에 번호 순으로 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-party-button"]') | 정당 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="party-number"]', '1') | 정당 번호가 입력됨 |
| 4 | playwright_fill('input[name="party-name"]', '국민의힘') | 정당명이 입력됨 |
| 5 | playwright_fill('input[name="color-code"]', '#E61E2B') | 색상 코드가 입력됨 |
| 6 | playwright_set_input_files('input[name="party-image"]', './test-data/party-logo.png') | 이미지가 선택됨 |
| 7 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 8 | playwright_wait_for_selector('.success-message') | 정당 등록 성공 메시지가 표시됨 |
| 9 | playwright_wait_for_selector('.party-list') | 정당 목록이 표시됨 |
| 10 | playwright_get_text('.party-item:first-child .party-number') | 정당이 번호 오름차순으로 정렬되어 표시됨 |

---

## TC-A-3-01-N01: [부정] 정당 번호에 문자 입력 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 정당 번호에 문자 입력 시 오류 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-party-button"]') | 정당 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="party-number"]', 'ABC') | 문자가 입력 시도됨 |
| 4 | playwright_wait_for_selector('.error-message') | '숫자만 입력 가능합니다.' 오류가 표시됨 |

---

## TC-A-3-01-N02: [부정] 정당 번호 범위 초과 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 정당 번호가 0 이하 시 범위 오류가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-party-button"]') | 정당 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="party-number"]', '0') | 0이 입력됨 |
| 4 | playwright_fill('input[name="party-name"]', '테스트정당') | 정당명이 입력됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 범위 오류 메시지가 표시됨 |

---

## TC-A-3-01-N03: [부정] 정당명 30자 초과 입력 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 정당명 30자 초과 시 오류 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-party-button"]') | 정당 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="party-number"]', '1') | 정당 번호가 입력됨 |
| 4 | playwright_fill('input[name="party-name"]', '이것은매우긴정당명으로서삼십자를초과하는테스트입니다') | 30자 초과 정당명이 입력됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | '최대 30자까지 입력 가능합니다.' 오류가 표시됨 |

---

## TC-A-3-01-N04: [부정] 필수 입력값 미입력 시 저장 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 필수 입력값 미입력 시 필수값 오류가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-party-button"]') | 정당 등록 폼이 표시됨 |
| 3 | playwright_click('button[type="submit"]') | 필수값 없이 저장 시도 |
| 4 | playwright_wait_for_selector('.error-message') | '정보 입력은 필수값 입니다.' 오류가 표시됨 |

---

## TC-A-3-01-N05: [부정] 중복 정당 번호 등록 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 중복 정당 번호 등록 시 오류가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당 번호 1번이 이미 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-party-button"]') | 정당 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="party-number"]', '1') | 기존과 동일한 번호 입력 |
| 4 | playwright_fill('input[name="party-name"]', '새정당') | 다른 정당명 입력 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 중복 오류 메시지가 표시됨 |

---

## TC-A-3-02-P01: [긍정] 정당 정보 수정

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 정당 정보가 정상적으로 수정됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당이 1개 이상 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('.party-item:first-child') | 첫 번째 정당이 선택됨 |
| 3 | playwright_click('button[data-testid="edit-party-button"]') | 수정 버튼이 클릭되고 편집 화면이 표시됨 |
| 4 | playwright_fill('input[name="party-name"]', '국민의힘(수정)') | 정당명이 수정됨 |
| 5 | playwright_fill('input[name="color-code"]', '#FF0000') | 색상 코드가 수정됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.success-message') | 수정 성공 메시지가 표시됨 |

---

## TC-A-3-02-P02: [긍정] 정당 비활성화

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 정당 비활성화 시 FO에서 표시되지 않음 |

### 사전 조건

- 관리자로 로그인되어 있음
- 정당이 1개 이상 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/party') | 정당 관리 페이지가 로드됨 |
| 2 | playwright_click('.party-item:first-child') | 정당이 선택됨 |
| 3 | playwright_click('button[data-testid="deactivate-party-button"]') | 비활성화 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.success-message') | 비활성화 성공 메시지가 표시됨 |
| 5 | playwright_navigate('https://metaj.jtbc.co.kr/party') | FO 정당 지지율 페이지로 이동 |
| 6 | playwright_wait_for_selector('.chart-container') | 그래프가 표시됨 |
| 7 | playwright_query_selector('.party-legend .deactivated-party') | 비활성화된 정당이 FO에서 표시되지 않음 |

---

## TC-A-4-01-P01: [긍정] 후보자 정보 정상 등록

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 후보자가 정상 등록됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-candidate-button"]') | 후보자 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="candidate-number"]', '1') | 기호가 입력됨 |
| 4 | playwright_fill('input[name="candidate-name"]', '홍길동') | 후보자명이 입력됨 |
| 5 | playwright_set_input_files('input[name="candidate-image-large"]', './test-data/candidate-large.png') | 대형 이미지가 선택됨 |
| 6 | playwright_set_input_files('input[name="candidate-image-small"]', './test-data/candidate-small.png') | 소형 이미지가 선택됨 |
| 7 | playwright_fill('textarea[name="profile-birth"]', '1970년 1월 1일') | 출생 정보가 입력됨 |
| 8 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 9 | playwright_wait_for_selector('.success-message') | 후보자 등록 성공 메시지가 표시됨 |

---

## TC-A-4-01-N01: [부정] 기호에 문자 입력 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 기호에 문자 입력 시 오류 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 후보자 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-candidate-button"]') | 후보자 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="candidate-number"]', 'ABC') | 문자가 입력 시도됨 |
| 4 | playwright_wait_for_selector('.error-message') | '숫자만 입력 가능합니다.' 오류가 표시됨 |

---

## TC-A-4-01-N02: [부정] 후보자명 30자 초과 입력 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 후보자명 30자 초과 시 오류 메시지가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 후보자 관리 페이지에 접근 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-candidate-button"]') | 후보자 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="candidate-number"]', '1') | 기호가 입력됨 |
| 4 | playwright_fill('input[name="candidate-name"]', '이것은매우긴후보자명으로서삼십자를초과하는테스트입니다') | 30자 초과 후보자명이 입력됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | '최대 30자까지 입력 가능합니다.' 오류가 표시됨 |

---

## TC-A-4-01-P02: [긍정] 이미지 및 약력 없이 후보자 등록

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 이미지/약력 없이 후보자가 정상 등록되고 FO에서 디폴트 이미지로 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-candidate-button"]') | 후보자 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="candidate-number"]', '2') | 기호가 입력됨 |
| 4 | playwright_fill('input[name="candidate-name"]', '김철수') | 후보자명이 입력됨 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨(이미지/약력 없음) |
| 6 | playwright_wait_for_selector('.success-message') | 등록 성공 메시지가 표시됨 |
| 7 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | FO 후보자 지지율 페이지로 이동 |
| 8 | playwright_wait_for_selector('.candidate-item[data-candidate="김철수"]') | 후보자가 표시되며 디폴트 이미지가 표시됨 |

---

## TC-A-4-01-P03: [긍정] 사퇴 여부 Y로 설정 후 등록

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 사퇴 여부 Y 설정 시 FO에서 사퇴 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 선거가 선택되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-candidate-button"]') | 후보자 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="candidate-number"]', '3') | 기호가 입력됨 |
| 4 | playwright_fill('input[name="candidate-name"]', '이영희') | 후보자명이 입력됨 |
| 5 | playwright_click('input[name="resigned"][value="Y"]') | 사퇴 여부가 Y로 선택됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.success-message') | 등록 성공 메시지가 표시됨 |
| 8 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | FO 후보자 지지율 페이지로 이동 |
| 9 | playwright_wait_for_selector('.candidate-item[data-candidate="이영희"].resigned') | 후보자가 사퇴 표시와 함께 표시됨 |

---

## TC-A-4-01-N03: [부정] 중복 기호 등록 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 중복 기호 등록 시 오류가 표시됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 기호 1번 후보자가 이미 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('button[data-testid="add-candidate-button"]') | 후보자 등록 폼이 표시됨 |
| 3 | playwright_fill('input[name="candidate-number"]', '1') | 기존과 동일한 기호 입력 |
| 4 | playwright_fill('input[name="candidate-name"]', '박민수') | 다른 후보자명 입력 |
| 5 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 중복 오류 메시지가 표시됨 |

---

## TC-A-4-02-P01: [긍정] 후보자 정보 수정

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 후보자 정보가 정상적으로 수정됨 |

### 사전 조건

- 관리자로 로그인되어 있음
- 후보자가 1개 이상 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('.candidate-item:first-child') | 첫 번째 후보자가 선택됨 |
| 3 | playwright_click('button[data-testid="edit-candidate-button"]') | 수정 버튼이 클릭되고 편집 화면이 표시됨 |
| 4 | playwright_fill('input[name="candidate-name"]', '홍길동(수정)') | 후보자명이 수정됨 |
| 5 | playwright_fill('textarea[name="profile-birth"]', '1975년 5월 5일') | 출생 정보가 수정됨 |
| 6 | playwright_click('button[type="submit"]') | 저장 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.success-message') | 수정 성공 메시지가 표시됨 |

---

## TC-A-4-02-P02: [긍정] 후보자 비활성화

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 후보자 비활성화 시 FO에서 표시되지 않음 |

### 사전 조건

- 관리자로 로그인되어 있음
- 후보자가 1개 이상 등록되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/admin/candidate') | 후보자 관리 페이지가 로드됨 |
| 2 | playwright_click('.candidate-item:first-child') | 후보자가 선택됨 |
| 3 | playwright_click('button[data-testid="deactivate-candidate-button"]') | 비활성화 버튼이 클릭됨 |
| 4 | playwright_wait_for_selector('.success-message') | 비활성화 성공 메시지가 표시됨 |
| 5 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | FO 후보자 지지율 페이지로 이동 |
| 6 | playwright_wait_for_selector('.chart-container') | 그래프가 표시됨 |
| 7 | playwright_query_selector('.candidate-legend .deactivated-candidate') | 비활성화된 후보자가 FO에서 표시되지 않음 |

---

## TC-A-5-01-P01: [긍정] 메인 페이지 로딩 및 표시

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 메인 페이지가 1초 이내에 로딩되고 정당/후보자 지지율 그래프가 표시됨 |

### 사전 조건

- 정당 지지율 및 후보자 지지율 데이터가 게시되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr') | 메인 페이지 로딩 시작 |
| 2 | playwright_wait_for_selector('.main-container', {timeout: 1000}) | 1초 이내에 메인 페이지가 로드됨 |
| 3 | playwright_get_text('h2.subtitle:nth-of-type(1)') | '민심이 선택한 대통령 후보는?' 소타이틀 확인 |
| 4 | playwright_get_text('h2.subtitle:nth-of-type(2)') | '민심이 선택한 정당은?' 소타이틀 확인 |
| 5 | playwright_wait_for_selector('.party-chart') | 정당 지지율 그래프가 표시됨 |
| 6 | playwright_wait_for_selector('.candidate-chart') | 후보자 지지율 그래프가 표시됨 |

---

## TC-A-6-01-P01: [긍정] 정당 지지율 전체 그래프 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 정당 지지율 전체 그래프가 1초 이내에 표시되고 범례, 툴팁, 시점 마커가 정상 표시됨 |

### 사전 조건

- 정당 지지율 데이터가 S3에 JSON 형태로 저장되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지 로딩 시작 |
| 2 | playwright_wait_for_selector('.party-chart', {timeout: 1000}) | 1초 이내에 정당 지지율 그래프가 렌더링됨 |
| 3 | playwright_query_selector_all('.party-legend .party-item') | 정당별 색상과 이름이 범례에 표시됨 |
| 4 | playwright_hover('.party-chart', {position: {x: 100, y: 100}}) | 그래프에 마우스 호버 |
| 5 | playwright_wait_for_selector('.chart-tooltip') | 해당 날짜의 각 정당 지지율 수치가 툴팁으로 표시됨 |
| 6 | playwright_query_selector_all('.timepoint-marker') | 등록된 특정 시점 마커가 그래프에 표시됨 |

---

## TC-A-6-02-P01: [긍정] 정당 지지율 성별 필터 적용

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 성별 필터 선택 시 해당 데이터로 그래프가 1초 이내에 갱신됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음
- 성별 필터 데이터가 JSON에 포함되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_wait_for_selector('.party-chart') | 전체 그래프가 표시됨 |
| 3 | playwright_click('button[data-filter="gender"]') | 성별 필터 버튼이 클릭됨 |
| 4 | playwright_click('button[data-filter-value="male"]') | '남성' 필터가 선택됨 |
| 5 | playwright_wait_for_selector('.party-chart.updated', {timeout: 1000}) | 1초 이내에 남성 데이터로 그래프가 갱신됨 |
| 6 | playwright_get_attribute('.party-chart', 'data-current-filter') | 현재 필터가 'gender-male'로 설정됨 |

---

## TC-A-6-02-P02: [긍정] 정당 지지율 연령 필터 적용

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 연령 필터 선택 시 해당 연령대 데이터로 그래프가 갱신됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-filter="age"]') | 연령 필터 버튼이 클릭됨 |
| 3 | playwright_click('button[data-filter-value="30-39"]') | '30~39' 연령대 필터가 선택됨 |
| 4 | playwright_wait_for_selector('.party-chart.updated', {timeout: 1000}) | 1초 이내에 30대 데이터로 그래프가 갱신됨 |

---

## TC-A-6-02-P03: [긍정] 정당 지지율 지역 필터 적용

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 지역 필터 선택 시 해당 지역 데이터로 그래프가 갱신됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-filter="region"]') | 지역 필터 버튼이 클릭됨 |
| 3 | playwright_click('button[data-filter-value="seoul"]') | '서울' 지역 필터가 선택됨 |
| 4 | playwright_wait_for_selector('.party-chart.updated', {timeout: 1000}) | 서울 지역 데이터로 그래프가 갱신됨 |

---

## TC-A-6-03-P01: [긍정] 정당 지지율 주별 기간 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 주별 선택 시 데이터가 주 단위로 집계되어 표시됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-period="weekly"]') | '주별' 기간 옵션이 선택됨 |
| 3 | playwright_wait_for_selector('.party-chart.updated') | 주 단위로 집계된 그래프가 표시됨 |

---

## TC-A-6-03-P02: [긍정] 정당 지지율 월별 기간 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 월별 선택 시 데이터가 월 단위로 집계되어 표시됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-period="monthly"]') | '월별' 기간 옵션이 선택됨 |
| 3 | playwright_wait_for_selector('.party-chart.updated') | 월 단위로 집계된 그래프가 표시됨 |

---

## TC-A-6-03-P03: [긍정] 정당 지지율 특정 기간 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 기간 설정 시 해당 기간의 데이터가 표시됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-period="custom"]') | '특정 기간 설정' 옵션이 선택됨 |
| 3 | playwright_wait_for_selector('.date-picker') | 시작일/종료일 캘린더가 표시됨 |
| 4 | playwright_fill('input[name="start-date"]', '2024-01-01') | 시작일이 입력됨 |
| 5 | playwright_fill('input[name="end-date"]', '2024-03-31') | 종료일이 입력됨 |
| 6 | playwright_click('button[data-testid="apply-custom-period"]') | 적용 버튼이 클릭됨 |
| 7 | playwright_wait_for_selector('.party-chart.updated') | 선택한 기간의 데이터로 그래프가 표시됨 |

---

## TC-A-6-03-N01: [부정] 시작일이 종료일보다 이후인 경우

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 시작일이 종료일보다 이후인 경우 오류 메시지가 표시됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-period="custom"]') | 특정 기간 설정이 선택됨 |
| 3 | playwright_fill('input[name="start-date"]', '2024-03-31') | 시작일이 입력됨 |
| 4 | playwright_fill('input[name="end-date"]', '2024-01-01') | 종료일이 시작일보다 이전 날짜로 입력됨 |
| 5 | playwright_click('button[data-testid="apply-custom-period"]') | 적용 버튼이 클릭됨 |
| 6 | playwright_wait_for_selector('.error-message') | 기간 설정 오류 메시지가 표시됨 |

---

## TC-A-6-04-P01: [긍정] 정당 체크박스 on/off

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 정당 체크박스 해제 시 라인이 숨겨지고 재체크 시 다시 표시됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음
- 3개 이상의 정당이 표시되고 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_wait_for_selector('.party-legend') | 정당 범례가 표시됨 |
| 3 | playwright_click('input[type="checkbox"][data-party="party1"]') | 첫 번째 정당 체크박스가 해제됨 |
| 4 | playwright_wait_for_selector('.party-chart .party-line[data-party="party1"].hidden') | 해당 정당 라인이 그래프에서 숨겨짐 |
| 5 | playwright_click('input[type="checkbox"][data-party="party1"]') | 체크박스를 다시 체크함 |
| 6 | playwright_wait_for_selector('.party-chart .party-line[data-party="party1"]:not(.hidden)') | 해당 정당 라인이 그래프에 다시 표시됨 |

---

## TC-A-6-04-P02: [긍정] 모든 정당 체크박스 해제

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모든 정당 체크박스 해제 시 빈 그래프가 표시됨 |

### 사전 조건

- 정당 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지가 로드됨 |
| 2 | playwright_query_selector_all('input[type="checkbox"][data-party]') | 모든 정당 체크박스를 찾음 |
| 3 | playwright_eval('document.querySelectorAll("input[type=checkbox][data-party]").forEach(cb => cb.checked = false)') | 모든 체크박스가 해제됨 |
| 4 | playwright_wait_for_selector('.party-chart.empty') | 빈 그래프가 표시됨 |

---

## TC-A-7-01-P01: [긍정] 후보자 지지율 전체 그래프 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 후보자 지지율 전체 그래프가 표시되고 모든 항목이 범례에 표시됨 |

### 사전 조건

- 후보자 지지율 데이터가 S3에 JSON 형태로 저장되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | 후보자 지지율 페이지 로딩 시작 |
| 2 | playwright_wait_for_selector('.candidate-chart', {timeout: 1000}) | 1초 이내에 후보자 지지율 그래프가 렌더링됨 |
| 3 | playwright_query_selector_all('.candidate-legend .candidate-item') | 후보자별 색상과 이름이 범례에 표시됨 |
| 4 | playwright_query_selector('.candidate-legend .non-support') | '지지 후보 없음' 항목이 범례에 표시됨 |
| 5 | playwright_query_selector('.candidate-legend .no-answer') | '모름/무응답' 항목이 범례에 표시됨 |
| 6 | playwright_query_selector_all('.timepoint-marker') | 등록된 특정 시점 마커가 그래프에 표시됨 |

---

## TC-A-7-02-P01: [긍정] 후보자 지지율 성별 필터 적용

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 성별 필터 선택 시 해당 데이터로 그래프가 갱신됨 |

### 사전 조건

- 후보자 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | 후보자 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-filter="gender"]') | 성별 필터 버튼이 클릭됨 |
| 3 | playwright_click('button[data-filter-value="female"]') | '여성' 필터가 선택됨 |
| 4 | playwright_wait_for_selector('.candidate-chart.updated', {timeout: 1000}) | 여성 데이터로 그래프가 갱신됨 |

---

## TC-A-7-03-P01: [긍정] 후보자 지지율 월별 기간 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 월별 선택 시 데이터가 월 단위로 집계되어 표시됨 |

### 사전 조건

- 후보자 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | 후보자 지지율 페이지가 로드됨 |
| 2 | playwright_click('button[data-period="monthly"]') | '월별' 기간 옵션이 선택됨 |
| 3 | playwright_wait_for_selector('.candidate-chart.updated') | 월 단위로 집계된 그래프가 표시됨 |

---

## TC-A-7-04-P01: [긍정] 후보자 체크박스 on/off

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 후보자 체크박스 해제 시 라인이 숨겨지고 재체크 시 다시 표시됨 |

### 사전 조건

- 후보자 지지율 페이지가 로드되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr/candidate') | 후보자 지지율 페이지가 로드됨 |
| 2 | playwright_click('input[type="checkbox"][data-candidate="candi1"]') | 첫 번째 후보자 체크박스가 해제됨 |
| 3 | playwright_wait_for_selector('.candidate-chart .candidate-line[data-candidate="candi1"].hidden') | 해당 후보자 라인이 그래프에서 숨겨짐 |
| 4 | playwright_click('input[type="checkbox"][data-candidate="candi1"]') | 체크박스를 다시 체크함 |
| 5 | playwright_wait_for_selector('.candidate-chart .candidate-line[data-candidate="candi1"]:not(.hidden)') | 해당 후보자 라인이 그래프에 다시 표시됨 |

---

## TC-A-8-01-P01: [긍정] 메타J 소개 페이지 접근

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 메타J 소개 페이지가 1초 이내에 로드되고 콘텐츠가 표시됨 |

### 사전 조건

- 사용자가 사이트에 접속 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr') | 메인 페이지가 로드됨 |
| 2 | playwright_click('a[href="/about"]') | 메타J 소개 메뉴가 클릭됨 |
| 3 | playwright_wait_for_selector('.about-container', {timeout: 1000}) | 1초 이내에 소개 페이지가 로드됨 |
| 4 | playwright_query_selector('.about-content') | 정적 콘텐츠(텍스트/이미지)가 표시됨 |

---

## TC-A-8-02-P01: [긍정] 방법론 페이지 접근

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 방법론 페이지가 로드되고 콘텐츠가 표시됨 |

### 사전 조건

- 사용자가 사이트에 접속 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr') | 메인 페이지가 로드됨 |
| 2 | playwright_click('a[href="/methodology"]') | 방법론 메뉴가 클릭됨 |
| 3 | playwright_wait_for_selector('.methodology-container') | 방법론 페이지가 로드됨 |
| 4 | playwright_query_selector('.methodology-content') | 정적 콘텐츠(텍스트/이미지)가 표시됨 |

---

## TC-A-8-03-P01: [긍정] 공통 헤더/푸터 표시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모든 페이지에서 공통 헤더와 푸터가 일관되게 표시됨 |

### 사전 조건

- 사용자가 사이트에 접속 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr') | 메인 페이지가 로드됨 |
| 2 | playwright_wait_for_selector('header.common-header') | 공통 헤더가 표시됨 |
| 3 | playwright_query_selector('header .logo') | 로고가 헤더에 표시됨 |
| 4 | playwright_query_selector_all('header nav a') | 메뉴(메타J/정당 지지율/후보자 지지율/메타J 소개/방법론)가 표시됨 |
| 5 | playwright_wait_for_selector('footer.common-footer') | 공통 푸터가 표시됨 |
| 6 | playwright_navigate('https://metaj.jtbc.co.kr/party') | 다른 페이지로 이동 |
| 7 | playwright_wait_for_selector('header.common-header') | 동일한 공통 헤더가 표시됨 |
| 8 | playwright_wait_for_selector('footer.common-footer') | 동일한 공통 푸터가 표시됨 |

---

## TC-A-8-03-P02: [긍정] 헤더 메뉴 네비게이션

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 헤더 메뉴를 통해 모든 페이지로 정상 이동됨 |

### 사전 조건

- 사용자가 사이트에 접속 가능함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate('https://metaj.jtbc.co.kr') | 메인 페이지가 로드됨 |
| 2 | playwright_click('header nav a[href="/party"]') | 정당 지지율 메뉴가 클릭됨 |
| 3 | playwright_wait_for_url('https://metaj.jtbc.co.kr/party') | 정당 지지율 페이지로 이동됨 |
| 4 | playwright_click('header nav a[href="/candidate"]') | 후보자 지지율 메뉴가 클릭됨 |
| 5 | playwright_wait_for_url('https://metaj.jtbc.co.kr/candidate') | 후보자 지지율 페이지로 이동됨 |
| 6 | playwright_click('header .logo') | 로고가 클릭됨 |
| 7 | playwright_wait_for_url('https://metaj.jtbc.co.kr') | 메인 페이지로 이동됨 |

---

# Epic B: 콘텐트 성과 분석 통계

- **테스트 대상 URL**: https://metaj.jtbc.co.kr
- **테스트 케이스**: 33개 (긍정: 25, 부정: 8)

## TC-US-A-8-04-001: 모바일 디바이스 반응형 레이아웃 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모바일 디바이스에서 최적화된 레이아웃이 표시되고, 모든 UI 요소가 화면 크기에 맞게 조정됨 |

### 사전 조건

- 테스트 URL https://metaj.jtbc.co.kr 접근 가능
- 모바일 디바이스 에뮬레이션 설정 가능 (iPhone 12 Pro, 390x844)

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' with viewport width=390, height=844 | 페이지가 정상적으로 로드됨 |
| 2 | playwright.screenshot of full page | 모바일 최적화 레이아웃 스크린샷 캡처 |
| 3 | playwright.evaluate document.body.clientWidth | viewport width가 390px로 설정됨 |
| 4 | playwright.query_selector for navigation menu (hamburger icon or mobile menu) | 모바일 전용 네비게이션 메뉴가 표시됨 |
| 5 | playwright.query_selector for responsive content containers | 콘텐츠 컨테이너가 모바일 width에 맞게 배치됨 |

---

## TC-US-A-8-04-002: 모바일 그래프 좌우 스크롤 기능 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모바일에서 그래프 영역을 터치하여 좌우로 스크롤할 수 있음 |

### 사전 조건

- 테스트 URL 접근 가능
- 모바일 viewport 설정 (390x844)
- 그래프 차트가 포함된 페이지 존재

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' with mobile viewport | 페이지 로드 완료 |
| 2 | playwright.query_selector for chart or graph element (canvas, svg, or chart container) | 그래프 요소가 발견됨 |
| 3 | playwright.evaluate to check if graph element has overflow-x: scroll or auto | 그래프 영역에 수평 스크롤 속성이 적용됨 |
| 4 | playwright.touch_start and touch_move on graph element (swipe left) | 터치 이벤트가 정상 처리됨 |
| 5 | playwright.evaluate to check scrollLeft value change | 그래프 영역의 scrollLeft 값이 변경되어 스크롤됨 |

---

## TC-US-A-8-04-003: 태블릿 디바이스 반응형 레이아웃 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 태블릿 디바이스에서 적합한 레이아웃이 표시되고, 화면 크기에 맞는 UI 구성이 적용됨 |

### 사전 조건

- 테스트 URL 접근 가능
- 태블릿 디바이스 에뮬레이션 설정 가능 (iPad Air, 820x1180)

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' with viewport width=820, height=1180 | 페이지가 정상적으로 로드됨 |
| 2 | playwright.screenshot of full page | 태블릿 레이아웃 스크린샷 캡처 |
| 3 | playwright.evaluate to check media query breakpoint | 태블릿용 미디어 쿼리가 활성화됨 |
| 4 | playwright.query_selector for tablet-specific layout elements | 태블릿에 최적화된 2단 또는 3단 레이아웃이 표시됨 |

---

## TC-US-A-8-04-004: 데스크톱 전체 화면 레이아웃 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 데스크톱에서 전체 화면 레이아웃이 표시되고, 넓은 화면을 효율적으로 활용함 |

### 사전 조건

- 테스트 URL 접근 가능
- 데스크톱 viewport 설정 (1920x1080)

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' with viewport width=1920, height=1080 | 페이지가 정상적으로 로드됨 |
| 2 | playwright.screenshot of full page | 데스크톱 레이아웃 스크린샷 캡처 |
| 3 | playwright.query_selector for desktop navigation menu | 데스크톱용 수평 네비게이션 메뉴가 표시됨 |
| 4 | playwright.evaluate to check container max-width or full-width layout | 전체 화면을 활용한 레이아웃이 적용됨 |

---

## TC-US-A-8-04-005: 극소형 모바일 디바이스에서 레이아웃 깨짐 검증 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 극소형 디바이스에서도 레이아웃이 깨지지 않고 모든 콘텐츠가 정상적으로 표시됨 (또는 최소 지원 width 안내) |

### 사전 조건

- 테스트 URL 접근 가능
- 극소형 viewport 설정 (320x568)

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' with viewport width=320, height=568 | 페이지 로드 완료 |
| 2 | playwright.screenshot of full page | 극소형 화면 스크린샷 캡처 |
| 3 | playwright.evaluate to check for horizontal overflow (document.body.scrollWidth > window.innerWidth) | 수평 스크롤이 발생하지 않아야 함 |
| 4 | playwright.query_selector for overlapping elements or text cutoff | UI 요소가 겹치거나 텍스트가 잘리지 않음 |

---

## TC-US-B-1-01-001: QuickSight 기사 PV 데이터 조회 - 기본 표시

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기사 PV 영역에서 기사ID, 제목, 카테고리, PV 수, 유입 경로가 정상적으로 표시됨 |

### 사전 조건

- QuickSight 대시보드 접근 권한 보유
- 테스트 기사 데이터가 존재함
- CMS 시스템에 로그인된 상태

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' (CMS/QuickSight 대시보드 영역) | 대시보드 페이지 로드 완료 |
| 2 | playwright.query_selector for '기사 PV' section or tab | 기사 PV 영역이 표시됨 |
| 3 | playwright.click on 기사 PV 영역 | 기사 PV 데이터 테이블 또는 차트가 로드됨 |
| 4 | playwright.query_selector for table headers: '기사ID', '제목', '카테고리', 'PV 수', '유입 경로' | 모든 필수 컬럼 헤더가 표시됨 |
| 5 | playwright.query_selector for table rows with data | 기사 데이터가 행으로 표시됨 |
| 6 | playwright.evaluate to verify each row contains 기사ID, 제목, 카테고리, PV 수, 유입 경로 | 각 행에 모든 필수 데이터가 포함됨 |

---

## TC-US-B-1-01-002: QuickSight 기사 드릴다운 상세 PV 데이터 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 기사를 드릴다운하면 해당 기사의 날짜별/시간별 상세 PV 데이터가 표시됨 |

### 사전 조건

- 기사 PV 목록이 표시된 상태
- 드릴다운 가능한 기사가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for first article row in PV table | 첫 번째 기사 행이 선택됨 |
| 2 | playwright.click on article row or drill-down button | 드릴다운 액션 실행 |
| 3 | playwright.wait_for_selector for detailed view or modal | 상세 뷰가 로드됨 |
| 4 | playwright.query_selector for date/time breakdown chart or table | 날짜별/시간별 PV 데이터가 표시됨 |
| 5 | playwright.evaluate to verify time-series data presence | 시계열 데이터가 존재하고 날짜/시간 단위로 집계됨 |

---

## TC-US-B-1-01-003: 유입 경로별 PV 데이터 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 유입 경로 데이터에서 JTBC, 네이버, 다음, 네이트, 스포츠빅이벤트, 기타별 PV가 정상적으로 표시됨 |

### 사전 조건

- 기사 PV 데이터가 표시된 상태
- 유입 경로 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for '유입 경로' column or section | 유입 경로 영역이 표시됨 |
| 2 | playwright.click on 유입 경로 데이터 or filter | 유입 경로별 상세 정보 표시 |
| 3 | playwright.query_selector for traffic sources: 'JTBC', '네이버', '다음', '네이트', '스포츠빅이벤트', '기타' | 모든 유입 경로 항목이 표시됨 |
| 4 | playwright.evaluate to verify each source has PV count | 각 유입 경로별 PV 수가 표시됨 |

---

## TC-US-B-1-01-004: 기간 필터 변경 - 일별/주별/월별

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 일별/주별/월별 필터를 변경하면 해당 기간 단위로 집계된 데이터가 표시됨 |

### 사전 조건

- 기사 PV 대시보드가 로드된 상태
- 기간 필터 UI가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for date filter dropdown or buttons (일별/주별/월별) | 기간 필터 UI가 발견됨 |
| 2 | playwright.click on '주별' filter option | 주별 필터 선택됨 |
| 3 | playwright.wait_for_selector for updated data table or chart | 데이터가 갱신됨 |
| 4 | playwright.evaluate to verify data is aggregated by week | 주 단위로 집계된 데이터가 표시됨 |
| 5 | playwright.click on '월별' filter option | 월별 필터 선택됨 |
| 6 | playwright.wait_for_selector for updated data | 월별 집계 데이터로 갱신됨 |

---

## TC-US-B-1-01-005: 카테고리 필터 적용

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 카테고리를 선택하면 해당 카테고리의 기사만 필터링되어 표시됨 |

### 사전 조건

- 기사 PV 대시보드가 로드된 상태
- 카테고리 필터가 존재함
- 여러 카테고리의 기사가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for category filter dropdown | 카테고리 필터 UI가 발견됨 |
| 2 | playwright.click on category filter dropdown | 카테고리 목록이 표시됨 |
| 3 | playwright.click on specific category option (예: '정치') | 정치 카테고리 선택됨 |
| 4 | playwright.wait_for_selector for filtered data table | 데이터 테이블이 갱신됨 |
| 5 | playwright.evaluate to verify all displayed articles belong to selected category | 표시된 모든 기사가 선택한 카테고리에 속함 |

---

## TC-US-B-1-01-006: 기사 PV 데이터 없는 경우 처리 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 데이터가 없는 경우 적절한 안내 메시지가 표시되고, 빈 테이블이 정상적으로 처리됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 선택한 기간 또는 필터에 해당하는 기사 데이터가 없음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 기사 PV 대시보드 | 대시보드 로드 |
| 2 | playwright.click on date filter and select future date range with no data | 미래 날짜 범위 선택됨 |
| 3 | playwright.wait_for_selector for empty state message or 'No data' indicator | 데이터 없음 메시지가 표시됨 |
| 4 | playwright.query_selector to verify no article rows are displayed | 기사 데이터 행이 표시되지 않음 |

---

## TC-US-B-1-02-001: QuickSight 영상 PV 데이터 조회 - 기본 표시

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 영상 PV 영역에서 영상ID, 제목, 재생 횟수, PV 수, 유입 경로가 정상적으로 표시됨 |

### 사전 조건

- QuickSight 대시보드 접근 권한 보유
- 테스트 영상 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to QuickSight 대시보드 | 대시보드 로드 완료 |
| 2 | playwright.query_selector for '영상 PV' section or tab | 영상 PV 영역이 표시됨 |
| 3 | playwright.click on 영상 PV 영역 | 영상 PV 데이터 로드 |
| 4 | playwright.query_selector for table headers: '영상ID', '제목', '재생 횟수', 'PV 수', '유입 경로' | 모든 필수 컬럼 헤더가 표시됨 |
| 5 | playwright.query_selector for table rows with video data | 영상 데이터가 행으로 표시됨 |
| 6 | playwright.evaluate to verify each row contains all required fields | 각 행에 영상ID, 제목, 재생 횟수, PV 수, 유입 경로가 모두 포함됨 |

---

## TC-US-B-1-02-002: 영상 드릴다운 상세 PV 데이터 조회

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 영상을 드릴다운하면 해당 영상의 상세 PV 데이터가 표시됨 |

### 사전 조건

- 영상 PV 목록이 표시된 상태
- 드릴다운 가능한 영상이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for first video row in PV table | 첫 번째 영상 행이 선택됨 |
| 2 | playwright.click on video row or drill-down icon | 드릴다운 실행 |
| 3 | playwright.wait_for_selector for detailed video analytics view | 상세 뷰가 표시됨 |
| 4 | playwright.query_selector for time-series PV data chart | 시계열 PV 데이터가 표시됨 |
| 5 | playwright.evaluate to verify detailed metrics (날짜별/시간별 재생 및 PV) | 상세 메트릭 데이터가 존재함 |

---

## TC-US-B-1-02-003: 영상 PV 일별/주별/월별 필터 변경

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 일별/주별/월별 필터를 변경하면 해당 기간 단위로 집계된 영상 PV 데이터가 표시됨 |

### 사전 조건

- 영상 PV 대시보드가 로드된 상태
- 기간 필터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for date range filter | 기간 필터 UI 발견 |
| 2 | playwright.click on '일별' option | 일별 필터 적용 |
| 3 | playwright.wait_for_selector for updated video PV data | 일별 집계 데이터 표시 |
| 4 | playwright.click on '월별' option | 월별 필터 적용 |
| 5 | playwright.wait_for_selector for updated data aggregated by month | 월별 집계 데이터 표시 |

---

## TC-US-B-1-02-004: 영상 재생 횟수 0인 경우 표시 검증 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 재생 횟수가 0인 영상도 정상적으로 표시되고, 드릴다운 시 데이터 없음을 적절히 안내함 |

### 사전 조건

- 영상 PV 대시보드 접근
- 재생 횟수가 0인 영상이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 영상 PV 대시보드 | 대시보드 로드 |
| 2 | playwright.query_selector for video with 0 play count | 재생 횟수 0인 영상 행 발견 |
| 3 | playwright.evaluate to verify play count displays '0' or equivalent | 재생 횟수가 0으로 명확히 표시됨 |
| 4 | playwright.click on the video row to drill down | 드릴다운 가능 |
| 5 | playwright.wait_for_selector for detailed view with empty or zero metrics | 상세 뷰에서도 재생 데이터가 없음을 정상 표시 |

---

## TC-US-B-2-01-001: 기사 내 영상 PV 비교 차트 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기사 내 영상이 있는 경우 기사 PV와 영상 PV가 하나의 차트에서 비교 표시됨 |

### 사전 조건

- 기사 내 영상이 포함된 콘텐츠가 존재함
- QuickSight 대시보드 접근

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to PV 추이 그래프 대시보드 | 대시보드 로드 |
| 2 | playwright.query_selector for article with embedded video | 영상이 포함된 기사 선택 |
| 3 | playwright.click on article to view PV trend chart | PV 추이 그래프 표시 |
| 4 | playwright.query_selector for chart with multiple series (기사 PV, 영상 PV) | 두 개의 데이터 시리즈가 차트에 표시됨 |
| 5 | playwright.evaluate to verify chart legend shows '기사 PV' and '영상 PV' | 범례에 기사 PV와 영상 PV가 구분되어 표시됨 |
| 6 | playwright.screenshot of comparison chart | 비교 차트 스크린샷 캡처 |

---

## TC-US-B-2-01-002: 영상만 있는 콘텐츠 PV 그래프 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기사가 없는 영상인 경우 영상 PV 그래프만 표시됨 |

### 사전 조건

- 기사 없이 영상만 존재하는 콘텐츠가 있음
- QuickSight 대시보드 접근

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to PV 추이 대시보드 | 대시보드 로드 |
| 2 | playwright.query_selector for video-only content | 영상 단독 콘텐츠 선택 |
| 3 | playwright.click on video content to view PV chart | PV 차트 표시 |
| 4 | playwright.query_selector for chart with single series (영상 PV only) | 영상 PV 데이터만 표시된 차트 확인 |
| 5 | playwright.evaluate to verify no article PV series exists | 기사 PV 시리즈가 차트에 없음 |

---

## TC-US-B-2-01-003: 기사만 있는 콘텐츠 PV 그래프 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 영상이 없는 기사인 경우 기사 PV 그래프만 표시됨 |

### 사전 조건

- 영상 없이 기사만 존재하는 콘텐츠가 있음
- QuickSight 대시보드 접근

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to PV 추이 대시보드 | 대시보드 로드 |
| 2 | playwright.query_selector for article-only content (no video) | 기사 단독 콘텐츠 선택 |
| 3 | playwright.click on article to view PV chart | PV 차트 표시 |
| 4 | playwright.query_selector for chart with single series (기사 PV only) | 기사 PV 데이터만 표시된 차트 확인 |
| 5 | playwright.evaluate to verify no video PV series exists | 영상 PV 시리즈가 차트에 없음 |

---

## TC-US-B-2-01-004: 기사/영상 모두 없는 경우 차트 표시 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | PV 데이터가 없는 경우 적절한 안내 메시지가 표시되거나 빈 차트가 정상 처리됨 |

### 사전 조건

- QuickSight 대시보드 접근
- PV 데이터가 없는 콘텐츠 또는 삭제된 콘텐츠

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to PV 추이 대시보드 | 대시보드 로드 |
| 2 | playwright.query_selector for content with no PV data | 데이터 없는 콘텐츠 선택 시도 |
| 3 | playwright.wait_for_selector for empty chart or 'No data' message | 빈 차트 또는 데이터 없음 메시지 표시 |
| 4 | playwright.evaluate to verify no chart series are rendered | 차트에 데이터 시리즈가 없음 |

---

## TC-US-B-3-01-001: 포털별 유입 비중 차트 표시 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | QuickSight 대시보드에서 네이버, 다음, 네이트, JTBC, 스포츠빅이벤트, 기타별 유입 비중이 차트로 표시됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 유입 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 외부 유입률 분석 대시보드 | 대시보드 로드 |
| 2 | playwright.query_selector for '유입 비중' chart section | 유입 비중 차트 영역 발견 |
| 3 | playwright.query_selector for chart legend or labels: '네이버', '다음', '네이트', 'JTBC', '스포츠빅이벤트', '기타' | 모든 유입 경로 항목이 차트에 표시됨 |
| 4 | playwright.evaluate to verify chart data contains values for each portal | 각 포털별 비중 값이 존재함 |
| 5 | playwright.screenshot of traffic source chart | 유입 비중 차트 스크린샷 캡처 |

---

## TC-US-B-3-01-002: 유입 비중 차트 기간 필터 변경

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기간 필터를 변경하면 해당 기간의 유입 비중이 차트에 갱신되어 표시됨 |

### 사전 조건

- 유입 비중 차트가 표시된 상태
- 기간 필터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for date range filter | 기간 필터 발견 |
| 2 | playwright.click on date filter and select custom date range (예: 최근 30일) | 날짜 범위 선택됨 |
| 3 | playwright.wait_for_selector for chart data refresh | 차트 데이터 갱신 완료 |
| 4 | playwright.evaluate to verify chart reflects selected date range data | 선택한 기간의 유입 비중 데이터가 차트에 반영됨 |

---

## TC-US-B-3-01-003: 유입 데이터 없는 기간 선택 시 차트 표시 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 유입 데이터가 없는 기간을 선택하면 적절한 안내 메시지가 표시되거나 빈 차트가 정상 처리됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 유입 데이터가 없는 기간 존재

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 유입 비중 대시보드 | 대시보드 로드 |
| 2 | playwright.click on date filter and select period with no traffic data | 데이터 없는 기간 선택 |
| 3 | playwright.wait_for_selector for empty chart or 'No data available' message | 빈 차트 또는 안내 메시지 표시 |
| 4 | playwright.evaluate to verify chart has no data series | 차트에 데이터가 표시되지 않음 |

---

## TC-US-B-3-02-001: 포털별 유입 급증 시계열 차트 표시

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | QuickSight 대시보드에서 포털별 유입 추이가 시간 순서로 표시된 시계열 차트 확인 |

### 사전 조건

- QuickSight 대시보드 접근
- 시계열 유입 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 유입 급증 시계열 차트 섹션 | 시계열 차트 영역 로드 |
| 2 | playwright.query_selector for time-series chart with multiple portal lines | 포털별 라인이 표시된 시계열 차트 발견 |
| 3 | playwright.evaluate to verify chart x-axis shows time progression | X축에 시간 순서가 표시됨 |
| 4 | playwright.evaluate to verify chart has separate lines for each portal | 각 포털별로 구분된 라인이 존재함 |
| 5 | playwright.screenshot of time-series traffic chart | 시계열 차트 스크린샷 캡처 |

---

## TC-US-B-3-02-002: 시계열 차트 특정 기간 설정 검증

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 기간을 설정하면 해당 기간의 포털별 유입 추이가 시계열 차트에 표시됨 |

### 사전 조건

- 시계열 차트가 표시된 상태
- 기간 설정 필터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for date range picker | 날짜 범위 선택 UI 발견 |
| 2 | playwright.click on start date input and select date | 시작일 선택 |
| 3 | playwright.click on end date input and select date | 종료일 선택 |
| 4 | playwright.click on apply or submit button | 필터 적용 |
| 5 | playwright.wait_for_selector for updated time-series chart | 차트가 선택한 기간으로 갱신됨 |
| 6 | playwright.evaluate to verify chart x-axis range matches selected period | X축 범위가 선택한 기간과 일치함 |

---

## TC-US-B-3-02-003: 시계열 차트 데이터 포인트 호버 상세 정보 (부정 시나리오 아님, 추가 검증)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 차트 데이터 포인트에 호버 시 해당 시점의 상세 정보가 툴팁으로 표시됨 |

### 사전 조건

- 시계열 차트가 표시된 상태

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for time-series chart canvas or SVG | 차트 요소 발견 |
| 2 | playwright.hover over specific data point on chart line | 데이터 포인트에 마우스 호버 |
| 3 | playwright.wait_for_selector for tooltip or data label | 툴팁이 표시됨 |
| 4 | playwright.evaluate to verify tooltip contains date, portal name, and value | 툴팁에 날짜, 포털명, 유입 수 정보가 표시됨 |

---

## TC-US-B-4-01-001: 기사 TOP10 랭킹 표시 - 디폴트 기간 (최근 7일)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 대시보드 접속 시 최근 7일(종료=오늘) 기준 PV 상위 10개 기사가 순위와 함께 표시됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 기사 PV 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 콘텐트 랭킹 대시보드 | 랭킹 대시보드 로드 |
| 2 | playwright.query_selector for '기사 TOP10' section | 기사 TOP10 영역 발견 |
| 3 | playwright.evaluate to verify default date range is last 7 days ending today | 기본 기간이 최근 7일로 설정됨 |
| 4 | playwright.query_selector for ranked list with 10 items | 10개 항목의 랭킹 리스트 표시 |
| 5 | playwright.evaluate to verify each item has rank number, article title, and PV count | 각 항목에 순위, 제목, PV 수가 표시됨 |
| 6 | playwright.evaluate to verify ranking is sorted by PV count descending | PV 수 기준 내림차순 정렬 확인 |

---

## TC-US-B-4-01-002: 기사 TOP10 랭킹 기간 필터 변경

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기간 필터에서 시작일/종료일을 설정하면 해당 기간의 기사 TOP10이 갱신되어 표시됨 |

### 사전 조건

- 기사 TOP10이 표시된 상태
- 기간 필터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for date range filter (시작일/종료일) | 날짜 필터 UI 발견 |
| 2 | playwright.click on start date and select custom date | 시작일 선택 |
| 3 | playwright.click on end date and select custom date | 종료일 선택 |
| 4 | playwright.click on apply filter button | 필터 적용 |
| 5 | playwright.wait_for_selector for updated TOP10 list | 랭킹 리스트 갱신 |
| 6 | playwright.evaluate to verify ranking reflects selected date range | 선택한 기간의 TOP10이 표시됨 |

---

## TC-US-B-4-01-003: 기사 데이터 10개 미만인 경우 랭킹 표시 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 기사가 10개 미만인 경우 실제 존재하는 기사만 랭킹에 표시되고, 빈 슬롯이나 오류 없이 정상 처리됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 선택한 기간에 기사가 10개 미만

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 기사 TOP10 섹션 | TOP10 섹션 로드 |
| 2 | playwright.click on date filter and select period with fewer than 10 articles | 기사 10개 미만 기간 선택 |
| 3 | playwright.wait_for_selector for ranking list | 랭킹 리스트 표시 |
| 4 | playwright.query_selector_all for list items | 실제 존재하는 기사 수만큼 항목 표시 |
| 5 | playwright.evaluate to verify list contains less than 10 items | 10개 미만의 항목만 표시됨 |

---

## TC-US-B-4-02-001: 영상 TOP10 랭킹 표시 - 디폴트 기간 (최근 7일)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 대시보드 접속 시 최근 7일(종료=오늘) 기준 유입률 상위 10개 영상이 순위와 함께 표시됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 영상 유입 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 콘텐트 랭킹 대시보드 | 랭킹 대시보드 로드 |
| 2 | playwright.query_selector for '영상 TOP10' section | 영상 TOP10 영역 발견 |
| 3 | playwright.evaluate to verify default date range is last 7 days ending today | 기본 기간이 최근 7일로 설정됨 |
| 4 | playwright.query_selector for ranked list with up to 10 video items | 10개 항목의 영상 랭킹 리스트 표시 |
| 5 | playwright.evaluate to verify each item has rank, video title, and traffic rate | 각 항목에 순위, 영상 제목, 유입률이 표시됨 |
| 6 | playwright.evaluate to verify ranking is sorted by traffic rate descending | 유입률 기준 내림차순 정렬 확인 |

---

## TC-US-B-4-02-002: 영상 TOP10 랭킹 기간 필터 변경

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기간 필터를 변경하면 해당 기간의 영상 TOP10이 갱신되어 표시됨 |

### 사전 조건

- 영상 TOP10이 표시된 상태
- 기간 필터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.query_selector for date range filter | 날짜 필터 발견 |
| 2 | playwright.click on date filter and select last 30 days | 최근 30일 선택 |
| 3 | playwright.wait_for_selector for updated video TOP10 list | 영상 랭킹 갱신 |
| 4 | playwright.evaluate to verify ranking reflects 30-day traffic data | 30일 기준 TOP10이 표시됨 |

---

## TC-US-B-4-02-003: 영상 유입률 데이터 없는 기간 TOP10 (부정)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 영상 유입 데이터가 없는 기간을 선택하면 적절한 안내 메시지가 표시되거나 빈 랭킹 리스트가 정상 처리됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 선택한 기간에 영상 유입 데이터가 없음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 영상 TOP10 섹션 | TOP10 섹션 로드 |
| 2 | playwright.click on date filter and select period with no video traffic | 데이터 없는 기간 선택 |
| 3 | playwright.wait_for_selector for empty ranking list or 'No data' message | 빈 리스트 또는 안내 메시지 표시 |
| 4 | playwright.query_selector_all for video ranking items | 랭킹 항목이 없음 |

---

## TC-US-B-INTEGRATION-001: 전체 대시보드 통합 시나리오 - 기사 선택부터 상세 분석까지

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | TOP10 랭킹에서 콘텐츠를 선택하고 상세 PV 분석, 유입 경로 분석까지 전체 워크플로우가 정상 작동함 |

### 사전 조건

- QuickSight 대시보드 전체 접근 권한
- 기사 및 영상 데이터 존재
- 최근 7일 데이터 존재

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to 'https://metaj.jtbc.co.kr' QuickSight dashboard | 대시보드 메인 화면 로드 |
| 2 | playwright.query_selector for 기사 TOP10 ranking section | 기사 TOP10 표시 확인 |
| 3 | playwright.click on first ranked article | 1위 기사 선택 |
| 4 | playwright.wait_for_selector for article detail view with PV trend chart | 기사 상세 뷰 및 PV 추이 차트 로드 |
| 5 | playwright.query_selector for traffic source breakdown | 유입 경로별 데이터 표시 확인 |
| 6 | playwright.screenshot of detailed analytics view | 상세 분석 화면 스크린샷 캡처 |
| 7 | playwright.click on back or close button to return to main dashboard | 메인 대시보드로 복귀 |
| 8 | playwright.query_selector for 영상 TOP10 section | 영상 TOP10 표시 확인 |
| 9 | playwright.click on top video in ranking | 1위 영상 선택 |
| 10 | playwright.wait_for_selector for video analytics detail | 영상 상세 분석 로드 |

---

## TC-US-B-PERFORMANCE-001: 대용량 데이터 로딩 성능 검증 (부정 시나리오)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 대용량 데이터 로딩 시 적절한 로딩 인디케이터가 표시되고, 타임아웃 발생 시 명확한 에러 메시지가 표시됨 |

### 사전 조건

- QuickSight 대시보드 접근
- 대용량 기간 선택 가능 (예: 1년 데이터)

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright.navigate to QuickSight dashboard | 대시보드 로드 |
| 2 | playwright.click on date filter and select 1-year range | 1년 기간 선택 |
| 3 | playwright.wait_for_selector for loading indicator or spinner | 로딩 인디케이터 표시 |
| 4 | playwright.wait_for_selector for data refresh completion (with timeout 30s) | 30초 내 데이터 로드 완료 또는 타임아웃 |
| 5 | playwright.evaluate to check if error message or timeout warning displayed | 타임아웃 시 적절한 에러 메시지 표시 |

---

# Epic C: 시스템 설정

- **테스트 대상 URL**: https://metaj.jtbc.co.kr
- **테스트 케이스**: 25개 (긍정: 18, 부정: 7)

## TC-B-5-01-P01: QuickSight 대시보드 정상 임베딩 및 표시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | QuickSight 대시보드가 CMS 통계 페이지에 정상적으로 임베딩되어 표시됨 |

### 사전 조건

- CMS에 콘텐트 운영자 권한으로 로그인되어 있음
- QuickSight 대시보드가 설정되어 있음
- JWT 인증 토큰이 유효함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/statistics' or similar statistics page | 통계 페이지가 로드됨 |
| 2 | wait for selector 'iframe[src*="quicksight"]' or '[data-testid="quicksight-dashboard"]' with timeout 10000 | QuickSight 대시보드 임베딩 영역이 표시됨 |
| 3 | evaluate '() => document.querySelector("iframe[src*=\"quicksight\"]")?.contentWindow !== null' | 대시보드 iframe이 정상적으로 로드됨 |
| 4 | wait for 3000 milliseconds to ensure dashboard fully renders | 대시보드 콘텐츠가 완전히 렌더링됨 |

---

## TC-B-5-01-P02: QuickSight 대시보드 JWT 자동 인증 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | JWT 토큰을 통해 자동 인증되어 대시보드가 즉시 표시됨 |

### 사전 조건

- CMS에 로그인되어 있음
- JWT 토큰 기반 인증이 설정되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/statistics' | 통계 페이지가 로드됨 |
| 2 | wait for selector 'iframe[src*="quicksight"]' with timeout 15000 | QuickSight iframe이 표시됨 |
| 3 | check that no authentication prompt or login modal is visible | 별도 로그인 프롬프트 없이 대시보드가 표시됨 |
| 4 | wait for selector '[data-testid="dashboard-loaded"]' or similar indicator with timeout 10000 | 대시보드가 정상적으로 로드됨 |

---

## TC-B-5-01-P03: QuickSight 대시보드 인터랙션(필터, 드릴다운) 동작 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | QuickSight 대시보드의 필터 및 드릴다운 기능이 정상 동작함 |

### 사전 조건

- QuickSight 대시보드가 정상적으로 로드되어 있음
- 대시보드에 필터 및 드릴다운 기능이 설정되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/statistics' | 통계 페이지 로드 |
| 2 | wait for selector 'iframe[src*="quicksight"]' with timeout 10000 | 대시보드 표시됨 |
| 3 | switch to iframe context and click on filter dropdown or selector '[data-testid="filter-control"]' | 필터 메뉴가 열림 |
| 4 | select filter option and apply | 필터가 적용되고 대시보드 데이터가 업데이트됨 |
| 5 | click on chart element to trigger drill-down | 드릴다운이 실행되어 상세 데이터가 표시됨 |

---

## TC-B-5-01-N01: QuickSight 대시보드 로딩 실패 시 오류 메시지 표시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 대시보드 로딩 실패 시 명확한 오류 메시지와 재시도 안내가 표시됨 |

### 사전 조건

- CMS에 로그인되어 있음
- 네트워크 오류 또는 QuickSight 서비스 장애 상황 시뮬레이션

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | set offline mode or block requests matching '*quicksight*' | QuickSight 요청이 차단됨 |
| 2 | navigate to 'https://metaj.jtbc.co.kr/statistics' | 통계 페이지 로드 시도 |
| 3 | wait for selector '[data-testid="dashboard-error"]' or text containing '오류' with timeout 15000 | 대시보드 로딩 오류 메시지가 표시됨 |
| 4 | check that error message contains '재시도' or '다시 시도' text | 재시도 안내 메시지가 포함됨 |
| 5 | click on retry button if present '[data-testid="retry-button"]' | 재시도 버튼이 동작함 |

---

## TC-C-1-01-P01: 관리자 계정 정상 생성 (슈퍼 관리자 역할)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 새 슈퍼 관리자 계정이 정상적으로 생성되고 목록에 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 계정 관리 페이지 접근 가능

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' or similar account management page | 계정 관리 페이지 로드 |
| 2 | click on button with text '계정 생성' or '[data-testid="create-account-button"]' | 계정 생성 폼이 표시됨 |
| 3 | fill input '[name="userId"]' with 'testadmin001' | ID 입력됨 |
| 4 | fill input '[name="password"]' with 'Test@1234!@' | 비밀번호 입력됨 |
| 5 | fill input '[name="name"]' with '테스트관리자' | 이름 입력됨 |
| 6 | select option '[name="role"]' with value '슈퍼 관리자' or 'SUPER_ADMIN' | 슈퍼 관리자 역할 선택됨 |
| 7 | click on button with text '저장' or '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for text '생성되었습니다' or '[data-testid="success-message"]' with timeout 5000 | 성공 메시지 표시됨 |
| 9 | check that account list contains text 'testadmin001' | 계정 목록에 새 계정이 표시됨 |

---

## TC-C-1-01-P02: 관리자 계정 정상 생성 (여론조사 관리자 역할)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 여론조사 관리자 권한을 가진 계정이 정상적으로 생성됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on '[data-testid="create-account-button"]' | 계정 생성 폼 표시 |
| 3 | fill '[name="userId"]' with 'pollmanager001' | ID 입력됨 |
| 4 | fill '[name="password"]' with 'Poll@1234!@' | 비밀번호 입력됨 |
| 5 | fill '[name="name"]' with '여론조사담당자' | 이름 입력됨 |
| 6 | select '[name="role"]' with value '여론조사 관리자' or 'POLL_MANAGER' | 여론조사 관리자 역할 선택됨 |
| 7 | click on '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for success message with timeout 5000 | 성공 메시지 표시됨 |

---

## TC-C-1-01-P03: 관리자 계정 정상 생성 (콘텐트 운영자 역할)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 콘텐트 운영자 권한을 가진 계정이 정상적으로 생성됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on '[data-testid="create-account-button"]' | 계정 생성 폼 표시 |
| 3 | fill '[name="userId"]' with 'contentop001' | ID 입력됨 |
| 4 | fill '[name="password"]' with 'Content@1234!@' | 비밀번호 입력됨 |
| 5 | fill '[name="name"]' with '콘텐트운영자' | 이름 입력됨 |
| 6 | select '[name="role"]' with value '콘텐트 운영자' or 'CONTENT_OPERATOR' | 콘텐트 운영자 역할 선택됨 |
| 7 | click on '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for success message with timeout 5000 | 성공 메시지 표시됨 |

---

## TC-C-1-01-N01: 중복 ID로 계정 생성 시 오류 표시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 중복 ID로 계정 생성 시도 시 적절한 오류 메시지가 표시되고 계정이 생성되지 않음 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 'existingadmin' ID를 가진 계정이 이미 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on '[data-testid="create-account-button"]' | 계정 생성 폼 표시 |
| 3 | fill '[name="userId"]' with 'existingadmin' | 기존에 존재하는 ID 입력됨 |
| 4 | fill '[name="password"]' with 'Test@1234!@' | 비밀번호 입력됨 |
| 5 | fill '[name="name"]' with '중복테스트' | 이름 입력됨 |
| 6 | select '[name="role"]' with value 'SUPER_ADMIN' | 역할 선택됨 |
| 7 | click on '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for text containing '중복' or '이미 존재' with timeout 5000 | 중복 ID 오류 메시지가 표시됨 |
| 9 | check that account creation form is still visible | 계정이 생성되지 않고 폼이 유지됨 |

---

## TC-C-1-01-N02: 필수 입력값 누락 시 안내 메시지 표시 확인 (ID 누락)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 필수 입력값(ID) 누락 시 적절한 안내 메시지가 표시되고 계정이 생성되지 않음 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on '[data-testid="create-account-button"]' | 계정 생성 폼 표시 |
| 3 | leave '[name="userId"]' empty | ID 필드가 비어있음 |
| 4 | fill '[name="password"]' with 'Test@1234!@' | 비밀번호 입력됨 |
| 5 | fill '[name="name"]' with '테스트' | 이름 입력됨 |
| 6 | select '[name="role"]' with value 'SUPER_ADMIN' | 역할 선택됨 |
| 7 | click on '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for text containing '필수' or '입력' with timeout 5000 | 필수값 입력 안내 메시지가 표시됨 |
| 9 | check that '[name="userId"]' has validation error indicator | ID 필드에 오류 표시가 나타남 |

---

## TC-C-1-01-N03: 필수 입력값 누락 시 안내 메시지 표시 확인 (비밀번호 누락)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 필수 입력값(비밀번호) 누락 시 적절한 안내 메시지가 표시되고 계정이 생성되지 않음 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on '[data-testid="create-account-button"]' | 계정 생성 폼 표시 |
| 3 | fill '[name="userId"]' with 'testuser123' | ID 입력됨 |
| 4 | leave '[name="password"]' empty | 비밀번호 필드가 비어있음 |
| 5 | fill '[name="name"]' with '테스트' | 이름 입력됨 |
| 6 | select '[name="role"]' with value 'SUPER_ADMIN' | 역할 선택됨 |
| 7 | click on '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for validation error message with timeout 5000 | 비밀번호 필수 입력 안내가 표시됨 |

---

## TC-C-1-01-N04: 필수 입력값 누락 시 안내 메시지 표시 확인 (역할 미선택)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 필수 입력값(역할) 누락 시 적절한 안내 메시지가 표시되고 계정이 생성되지 않음 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on '[data-testid="create-account-button"]' | 계정 생성 폼 표시 |
| 3 | fill '[name="userId"]' with 'testuser456' | ID 입력됨 |
| 4 | fill '[name="password"]' with 'Test@1234!@' | 비밀번호 입력됨 |
| 5 | fill '[name="name"]' with '테스트' | 이름 입력됨 |
| 6 | leave '[name="role"]' unselected or select default empty value | 역할이 선택되지 않음 |
| 7 | click on '[data-testid="save-account-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for text containing '역할' and '선택' with timeout 5000 | 역할 선택 안내 메시지가 표시됨 |

---

## TC-C-1-02-P01: 관리자 계정 목록 조회 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모든 관리자 계정이 리스트 형태로 정상 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 시스템에 최소 1개 이상의 관리자 계정이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | wait for selector '[data-testid="account-list"]' or 'table tbody tr' with timeout 5000 | 계정 목록 테이블이 표시됨 |
| 3 | count elements matching 'table tbody tr' or '[data-testid="account-row"]' | 1개 이상의 계정 행이 표시됨 |
| 4 | check that table headers contain 'ID', '이름', '역할' | 계정 정보 컬럼이 표시됨 |

---

## TC-C-1-02-P02: 관리자 계정 정보 수정 (이름 변경)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 관리자 계정의 이름이 정상적으로 수정됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 수정 가능한 테스트 계정이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on first account row or '[data-testid="account-row"]:first-child' | 계정이 선택됨 |
| 3 | click on button with text '수정' or '[data-testid="edit-account-button"]' | 수정 폼이 표시됨 |
| 4 | clear and fill '[name="name"]' with '수정된이름' | 이름이 변경됨 |
| 5 | click on button with text '저장' or '[data-testid="save-changes-button"]' | 저장 버튼 클릭됨 |
| 6 | wait for success message with timeout 5000 | 수정 완료 메시지가 표시됨 |
| 7 | check that account list contains text '수정된이름' | 변경된 이름이 목록에 반영됨 |

---

## TC-C-1-02-P03: 관리자 계정 역할 변경

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 관리자 계정의 역할이 정상적으로 변경됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 역할 변경 가능한 테스트 계정이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on test account row | 계정 선택됨 |
| 3 | click on '[data-testid="edit-account-button"]' | 수정 폼 표시 |
| 4 | select '[name="role"]' with different role value | 역할이 변경됨 |
| 5 | click on '[data-testid="save-changes-button"]' | 저장 버튼 클릭됨 |
| 6 | wait for success message with timeout 5000 | 수정 완료 메시지 표시 |
| 7 | verify that account row shows updated role | 변경된 역할이 목록에 반영됨 |

---

## TC-C-1-02-P04: 관리자 계정 비활성화

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 관리자 계정이 정상적으로 비활성화되고 로그인 불가 상태가 됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 비활성화 가능한 테스트 계정이 존재함
- 현재 로그인한 계정이 아닌 다른 계정임

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | click on test account row (not current user) | 계정 선택됨 |
| 3 | click on button with text '비활성화' or '[data-testid="deactivate-account-button"]' | 비활성화 확인 대화상자 표시 |
| 4 | click on confirm button in modal | 비활성화 실행됨 |
| 5 | wait for success message with timeout 5000 | 비활성화 완료 메시지 표시 |
| 6 | check that account row shows '비활성' or 'inactive' status | 계정 상태가 비활성으로 변경됨 |

---

## TC-C-1-02-N01: 본인 계정 비활성화 시도 시 오류 표시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 본인 계정 비활성화 시도 시 적절한 오류 메시지가 표시되고 비활성화되지 않음 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/accounts' | 계정 관리 페이지 로드 |
| 2 | find and click on row containing current user's account ID | 본인 계정이 선택됨 |
| 3 | click on '[data-testid="deactivate-account-button"]' | 비활성화 버튼 클릭됨 |
| 4 | wait for error message containing '본인' or '자기 자신' with timeout 5000 | 본인 계정 비활성화 불가 오류 메시지가 표시됨 |
| 5 | check that account status remains active | 계정이 활성 상태로 유지됨 |

---

## TC-C-2-01-P01: 공통 코드 정상 생성

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 새 공통 코드가 정상적으로 등록되고 목록에 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 코드 관리 페이지 접근 가능

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/codes' or similar code management page | 코드 관리 페이지 로드 |
| 2 | click on button with text '코드 생성' or '[data-testid="create-code-button"]' | 코드 생성 폼이 표시됨 |
| 3 | fill '[name="codeGroup"]' with 'TEST_GROUP' | 코드 그룹 입력됨 |
| 4 | fill '[name="codeValue"]' with 'TEST_CODE_001' | 코드 값 입력됨 |
| 5 | fill '[name="codeName"]' with '테스트코드명' | 코드명 입력됨 |
| 6 | fill '[name="codeOrder"]' with '1' | 코드 순서 입력됨 |
| 7 | click on button with text '저장' or '[data-testid="save-code-button"]' | 저장 버튼 클릭됨 |
| 8 | wait for success message with timeout 5000 | 등록 완료 메시지 표시 |
| 9 | check that code list contains 'TEST_CODE_001' | 코드 목록에 새 코드가 표시됨 |

---

## TC-C-2-01-P02: 공통 코드 조회 및 상세 정보 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 코드 선택 시 상세 정보가 정상적으로 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 시스템에 조회 가능한 코드가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/codes' | 코드 관리 페이지 로드 |
| 2 | wait for selector '[data-testid="code-list"]' or 'table tbody tr' with timeout 5000 | 코드 목록이 표시됨 |
| 3 | click on first code row or '[data-testid="code-row"]:first-child' | 코드가 선택됨 |
| 4 | wait for selector '[data-testid="code-detail"]' with timeout 3000 | 코드 상세 정보 영역이 표시됨 |
| 5 | check that detail view contains '코드 그룹', '코드 값', '코드명', '순서' | 모든 코드 상세 정보가 표시됨 |

---

## TC-C-2-01-P03: 공통 코드 수정

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 공통 코드가 정상적으로 수정되고 시스템에 반영됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 수정 가능한 테스트 코드가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/codes' | 코드 관리 페이지 로드 |
| 2 | click on test code row | 코드 선택됨 |
| 3 | click on button with text '수정' or '[data-testid="edit-code-button"]' | 수정 폼이 표시됨 |
| 4 | clear and fill '[name="codeName"]' with '수정된코드명' | 코드명이 변경됨 |
| 5 | clear and fill '[name="codeOrder"]' with '5' | 순서가 변경됨 |
| 6 | click on '[data-testid="save-code-button"]' | 저장 버튼 클릭됨 |
| 7 | wait for success message with timeout 5000 | 수정 완료 메시지 표시 |
| 8 | check that code list shows updated values | 변경된 코드 정보가 목록에 반영됨 |

---

## TC-C-2-01-P04: 공통 코드 삭제

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 공통 코드가 정상적으로 삭제되고 시스템에서 제거됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 시스템에서 사용하지 않는 삭제 가능한 코드가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/codes' | 코드 관리 페이지 로드 |
| 2 | click on unused test code row | 삭제 가능한 코드 선택됨 |
| 3 | click on button with text '삭제' or '[data-testid="delete-code-button"]' | 삭제 확인 대화상자 표시 |
| 4 | click on confirm button in modal | 삭제 실행됨 |
| 5 | wait for success message with timeout 5000 | 삭제 완료 메시지 표시 |
| 6 | check that code is removed from list | 코드가 목록에서 제거됨 |

---

## TC-C-2-01-N01: 시스템 사용 중인 코드 삭제 시도 시 경고 표시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 시스템 사용 중인 코드 삭제 시도 시 적절한 경고 메시지가 표시되고 삭제되지 않음 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 시스템에서 사용 중인 코드가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/codes' | 코드 관리 페이지 로드 |
| 2 | click on code row that is in use by system | 사용 중인 코드 선택됨 |
| 3 | click on '[data-testid="delete-code-button"]' | 삭제 버튼 클릭됨 |
| 4 | wait for error message containing '사용 중' or '삭제 불가' with timeout 5000 | 사용 중 삭제 불가 경고 메시지가 표시됨 |
| 5 | check that code still exists in list | 코드가 삭제되지 않고 목록에 유지됨 |

---

## TC-C-3-01-P01: CMS 접속 로그 조회 (전체)

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 관리자별 로그인/로그아웃 이력이 시간순으로 정상 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 시스템에 접속 로그 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/logs' or similar log management page | 로그 관리 페이지 로드 |
| 2 | click on tab with text '접속 로그' or '[data-testid="access-log-tab"]' | 접속 로그 탭이 활성화됨 |
| 3 | wait for selector '[data-testid="access-log-list"]' or 'table tbody tr' with timeout 5000 | 접속 로그 목록이 표시됨 |
| 4 | check that table headers contain '관리자', '액션', '시간' | 로그 정보 컬럼이 표시됨 |
| 5 | check that log entries show '로그인' or '로그아웃' actions | 로그인/로그아웃 이력이 시간순으로 표시됨 |
| 6 | verify that logs are sorted by timestamp descending | 최신 로그가 상단에 표시됨 |

---

## TC-C-3-01-P02: 특정 관리자 접속 로그 필터링

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 관리자로 필터링 시 해당 관리자의 접속 이력만 정상 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 여러 관리자의 접속 로그가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | click on '[data-testid="access-log-tab"]' | 접속 로그 탭 활성화 |
| 3 | click on or select '[name="adminFilter"]' or '[data-testid="admin-filter"]' | 관리자 필터 드롭다운 열림 |
| 4 | select specific admin from dropdown | 특정 관리자 선택됨 |
| 5 | click on apply filter button or wait for auto-filter | 필터가 적용됨 |
| 6 | check that all visible log entries belong to selected admin | 선택한 관리자의 접속 이력만 표시됨 |

---

## TC-C-3-01-P03: 기간별 접속 로그 필터링

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 기간 필터 설정 시 해당 기간의 접속 이력만 정상 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 다양한 날짜의 접속 로그가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | click on '[data-testid="access-log-tab"]' | 접속 로그 탭 활성화 |
| 3 | fill '[name="startDate"]' or '[data-testid="start-date"]' with specific date | 시작일 입력됨 |
| 4 | fill '[name="endDate"]' or '[data-testid="end-date"]' with specific date | 종료일 입력됨 |
| 5 | click on button with text '조회' or '[data-testid="apply-date-filter"]' | 기간 필터가 적용됨 |
| 6 | check that all visible log entries fall within selected date range | 선택한 기간의 접속 이력만 표시됨 |

---

## TC-C-3-01-P04: 관리자 및 기간 복합 필터링

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 관리자 및 기간 복합 필터 적용 시 조건에 맞는 로그만 정상 표시됨 |

### 사전 조건

- 슈퍼 관리자 권한으로 로그인되어 있음
- 충분한 접속 로그 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | click on '[data-testid="access-log-tab"]' | 접속 로그 탭 활성화 |
| 3 | select specific admin from '[data-testid="admin-filter"]' | 관리자 필터 선택됨 |
| 4 | fill date range in '[data-testid="start-date"]' and '[data-testid="end-date"]' | 기간 필터 입력됨 |
| 5 | click on '[data-testid="apply-filters"]' | 모든 필터가 적용됨 |
| 6 | verify that results match both admin and date criteria | 선택한 관리자의 해당 기간 로그만 표시됨 |

---

# Epic D: 인증 및 공통

- **테스트 대상 URL**: https://metaj.jtbc.co.kr
- **테스트 케이스**: 21개 (긍정: 14, 부정: 7)

## TC-D-1-01-001: 관리자 로그인 - 올바른 인증 정보로 로그인 성공

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 로그인 성공 후 JWT 토큰이 발급되고 대시보드 페이지로 이동 |

### 사전 조건

- CMS 로그인 페이지(https://metaj.jtbc.co.kr/admin/login)에 접근 가능
- 유효한 관리자 계정이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지가 로드됨 |
| 2 | playwright_fill selector='input[name="username"]' or 'input[type="text"]' with text='valid_admin_id' | ID 입력 필드에 값이 입력됨 |
| 3 | playwright_fill selector='input[name="password"]' or 'input[type="password"]' with text='valid_password' | 비밀번호 입력 필드에 값이 입력됨 |
| 4 | playwright_click selector='button[type="submit"]' or 'button:has-text("로그인")' | 로그인 버튼 클릭됨 |
| 5 | playwright_evaluate expression='localStorage.getItem("token")' or check cookies for JWT token | JWT 토큰이 저장됨 |
| 6 | playwright_navigate 현재 URL 확인 | 대시보드 페이지(예: /admin/dashboard)로 리다이렉트됨 |

---

## TC-D-1-01-002: 관리자 로그인 - 잘못된 ID/비밀번호로 로그인 실패

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 인증 실패 메시지가 표시되고 로그인되지 않음 |

### 사전 조건

- CMS 로그인 페이지에 접근 가능

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지가 로드됨 |
| 2 | playwright_fill selector='input[name="username"]' with text='invalid_id' | 잘못된 ID가 입력됨 |
| 3 | playwright_fill selector='input[name="password"]' with text='wrong_password' | 잘못된 비밀번호가 입력됨 |
| 4 | playwright_click selector='button[type="submit"]' | 로그인 버튼 클릭됨 |
| 5 | playwright_screenshot and check for error message selector='.error-message' or '.alert' | 인증 실패 메시지가 표시됨 (예: 'ID 또는 비밀번호가 올바르지 않습니다') |
| 6 | playwright_navigate 현재 URL 확인 | 로그인 페이지에 그대로 머무름 |

---

## TC-D-1-01-003: 관리자 로그인 - 비활성화된 계정으로 로그인 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 계정 비활성화 안내 메시지가 표시되고 로그인 거부됨 |

### 사전 조건

- 비활성화된 관리자 계정이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지가 로드됨 |
| 2 | playwright_fill selector='input[name="username"]' with text='disabled_admin_id' | 비활성화된 계정 ID가 입력됨 |
| 3 | playwright_fill selector='input[name="password"]' with text='correct_password' | 올바른 비밀번호가 입력됨 |
| 4 | playwright_click selector='button[type="submit"]' | 로그인 버튼 클릭됨 |
| 5 | playwright_screenshot and verify error message contains text='비활성화' or '사용 불가' | 계정 비활성화 안내 메시지가 표시됨 |

---

## TC-D-1-01-004: 관리자 로그인 - 여론조사 관리자 권한으로 메뉴 접근 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 여론조사 관리자는 여론조사 관리 메뉴만 접근 가능하고 다른 메뉴는 차단됨 |

### 사전 조건

- 여론조사 관리자 계정으로 로그인됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지 로드 |
| 2 | playwright_fill selector='input[name="username"]' with text='poll_manager_id' | 여론조사 관리자 ID 입력 |
| 3 | playwright_fill selector='input[name="password"]' with text='poll_manager_password' | 비밀번호 입력 |
| 4 | playwright_click selector='button[type="submit"]' | 로그인 실행 |
| 5 | playwright_screenshot and verify navigation menu contains '여론조사 관리' menu | 여론조사 관리 메뉴가 표시됨 |
| 6 | playwright_screenshot and verify navigation menu does NOT contain '계정 관리' or '로그 관리' | 관리자 전용 메뉴는 표시되지 않음 |
| 7 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/accounts' (unauthorized page) | 접근 거부 페이지 또는 403 에러 페이지로 리다이렉트됨 |

---

## TC-D-1-01-005: 관리자 로그인 - 콘텐트 운영자 권한으로 메뉴 접근 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 콘텐트 운영자는 뉴스 통계 관리 메뉴만 접근 가능 |

### 사전 조건

- 콘텐트 운영자 계정으로 로그인됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지 로드 |
| 2 | playwright_fill selector='input[name="username"]' with text='content_operator_id' | 콘텐트 운영자 ID 입력 |
| 3 | playwright_fill selector='input[name="password"]' with text='content_operator_password' | 비밀번호 입력 |
| 4 | playwright_click selector='button[type="submit"]' | 로그인 실행 |
| 5 | playwright_screenshot and verify navigation menu contains '뉴스 통계 관리' menu | 뉴스 통계 관리 메뉴가 표시됨 |
| 6 | playwright_screenshot and verify navigation menu does NOT contain '여론조사 관리' or '계정 관리' | 다른 역할의 메뉴는 표시되지 않음 |

---

## TC-D-1-01-006: 관리자 로그인 - 슈퍼 관리자 권한으로 모든 메뉴 접근 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 슈퍼 관리자는 모든 메뉴에 접근 가능 |

### 사전 조건

- 슈퍼 관리자 계정으로 로그인됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지 로드 |
| 2 | playwright_fill selector='input[name="username"]' with text='super_admin_id' | 슈퍼 관리자 ID 입력 |
| 3 | playwright_fill selector='input[name="password"]' with text='super_admin_password' | 비밀번호 입력 |
| 4 | playwright_click selector='button[type="submit"]' | 로그인 실행 |
| 5 | playwright_screenshot and verify all menus are visible: '대시보드', '여론조사 관리', '뉴스 통계 관리', '계정 관리', '로그 관리' | 모든 메뉴가 표시됨 |
| 6 | playwright_click on '계정 관리' menu | 계정 관리 페이지로 이동 |
| 7 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 접근 가능 |

---

## TC-D-1-01-007: 관리자 로그인 - JWT 토큰 만료 시 재인증 처리

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | JWT 토큰 만료 시 로그인 페이지로 리다이렉트됨 |

### 사전 조건

- 관리자가 로그인되어 있음
- JWT 토큰이 만료됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/dashboard' (already logged in) | 대시보드 페이지가 로드됨 |
| 2 | playwright_evaluate expression to manipulate token expiration or wait for token expiry | JWT 토큰이 만료됨 |
| 3 | playwright_click on any menu or API call triggering action | API 호출 시도 |
| 4 | playwright_navigate 현재 URL 확인 | 로그인 페이지(/admin/login)로 리다이렉트됨 |
| 5 | playwright_screenshot and verify login form is displayed | 로그인 폼이 표시됨 |

---

## TC-D-1-01-008: 관리자 로그인 - 연속 5회 실패 시 계정 잠금

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 5회 연속 실패 후 일정 시간 로그인이 차단됨 |

### 사전 조건

- 유효한 관리자 계정이 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지 로드 |
| 2 | Loop 5 times: playwright_fill ID with 'valid_id', password with 'wrong_password', then playwright_click submit button | 5회 연속 로그인 실패 |
| 3 | playwright_screenshot and verify error message contains '로그인 시도 횟수 초과' or '일시적으로 차단' | 계정 잠금 메시지가 표시됨 |
| 4 | playwright_fill with correct credentials and playwright_click submit | 올바른 인증 정보 입력 |
| 5 | playwright_screenshot and verify login is still blocked | 로그인이 차단되고 대기 시간 안내 메시지가 표시됨 |

---

## TC-D-1-02-001: 관리자 로그아웃 - 정상 로그아웃 처리

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | JWT 토큰이 무효화되고 로그인 페이지로 이동 |

### 사전 조건

- 관리자가 CMS에 로그인되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/dashboard' | 대시보드 페이지가 로드됨 |
| 2 | playwright_click selector='button:has-text("로그아웃")' or '.logout-button' or header logout icon | 로그아웃 버튼 클릭됨 |
| 3 | playwright_evaluate expression='localStorage.getItem("token")' to verify token removal | JWT 토큰이 무효화됨 (localStorage/cookie에서 제거됨) |
| 4 | playwright_navigate 현재 URL 확인 | 로그인 페이지(/admin/login)로 리다이렉트됨 |

---

## TC-D-1-02-002: 관리자 로그아웃 - 로그아웃 후 이전 페이지 접근 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 로그아웃 후 보호된 페이지 접근 시 로그인 페이지로 리다이렉트됨 |

### 사전 조건

- 관리자가 로그아웃을 완료함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지 로드 |
| 2 | Perform login with valid credentials | 로그인 성공 |
| 3 | playwright_click logout button | 로그아웃 실행 |
| 4 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/dashboard' (previous page) | 대시보드 페이지 접근 시도 |
| 5 | playwright_navigate 현재 URL 확인 | 로그인 페이지(/admin/login)로 리다이렉트됨 |
| 6 | playwright_screenshot and verify login form is displayed | 로그인 폼이 표시됨 |

---

## TC-C-3-02-001: 데이터 CRUD 로그 조회 - 전체 이력 시간순 표시

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 데이터 변경 이력이 시간순으로 표시됨 |

### 사전 조건

- 슈퍼 관리자로 로그인됨
- CRUD 로그 데이터가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지가 로드됨 |
| 2 | playwright_click selector='[role="tab"]:has-text("CRUD 로그")' or '.crud-log-tab' | CRUD 로그 탭이 선택됨 |
| 3 | playwright_screenshot and verify table with columns: '시간', '작업 유형', '관리자', '대상 테이블', '상세' | CRUD 로그 테이블이 표시됨 |
| 4 | playwright_evaluate to get first and last row timestamps and verify chronological order (최신순 또는 오래된순) | 데이터가 시간순으로 정렬되어 있음 |
| 5 | playwright_screenshot and verify log entries show types: '생성', '조회', '수정', '삭제' | 생성/조회/수정/삭제 이력이 모두 표시됨 |

---

## TC-C-3-02-002: 데이터 CRUD 로그 조회 - 작업 유형별 필터링

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 선택한 작업 유형의 이력만 필터링되어 표시됨 |

### 사전 조건

- 슈퍼 관리자로 로그인됨
- CRUD 로그 페이지에 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | playwright_click CRUD 로그 탭 | CRUD 로그 탭 활성화 |
| 3 | playwright_click selector='select[name="action_type"]' or '.filter-action-type' | 작업 유형 필터 드롭다운 열림 |
| 4 | playwright_click option with text='생성' or value='CREATE' | '생성' 필터 선택됨 |
| 5 | playwright_screenshot and verify all visible log entries have action type='생성' | '생성' 유형의 이력만 표시됨 |
| 6 | playwright_click filter and select '수정' or 'UPDATE' | '수정' 필터 선택 |
| 7 | playwright_screenshot and verify all entries show action type='수정' | '수정' 유형의 이력만 표시됨 |

---

## TC-C-3-02-003: 데이터 CRUD 로그 조회 - 관리자별 필터링

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 관리자의 변경 이력만 필터링되어 표시됨 |

### 사전 조건

- 슈퍼 관리자로 로그인됨
- 여러 관리자의 CRUD 로그가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | playwright_click CRUD 로그 탭 | CRUD 로그 탭 활성화 |
| 3 | playwright_click selector='select[name="admin_id"]' or '.filter-admin' | 관리자 필터 드롭다운 열림 |
| 4 | playwright_click option with specific admin name (예: '최관리') | 특정 관리자 선택됨 |
| 5 | playwright_screenshot and verify all log entries show selected admin name in '관리자' column | 선택한 관리자의 변경 이력만 표시됨 |
| 6 | playwright_evaluate to count entries and verify all belong to selected admin | 모든 로그가 선택한 관리자의 것임 |

---

## TC-C-3-02-004: 데이터 CRUD 로그 조회 - 대상 테이블/기능별 필터링

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 특정 테이블/기능의 변경 이력만 필터링되어 표시됨 |

### 사전 조건

- 슈퍼 관리자로 로그인됨
- 다양한 테이블/기능의 CRUD 로그가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | playwright_click CRUD 로그 탭 | CRUD 로그 탭 활성화 |
| 3 | playwright_click selector='select[name="target_table"]' or '.filter-table' | 대상 테이블 필터 드롭다운 열림 |
| 4 | playwright_click option with specific table name (예: '여론조사', 'polls') | 특정 테이블/기능 선택됨 |
| 5 | playwright_screenshot and verify all log entries show selected table in '대상 테이블' column | 선택한 영역의 변경 이력만 표시됨 |
| 6 | playwright_evaluate to verify filtered results only contain selected table | 모든 로그가 선택한 테이블/기능과 관련됨 |

---

## TC-C-3-02-005: 데이터 CRUD 로그 조회 - 복합 필터 적용

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 여러 필터를 동시 적용하여 정확한 결과를 조회할 수 있음 |

### 사전 조건

- 슈퍼 관리자로 로그인됨
- 다양한 CRUD 로그가 존재함

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 로드 |
| 2 | playwright_click CRUD 로그 탭 | CRUD 로그 탭 활성화 |
| 3 | playwright_click action type filter and select '수정' | 작업 유형 필터 설정 |
| 4 | playwright_click admin filter and select specific admin | 관리자 필터 설정 |
| 5 | playwright_click table filter and select specific table | 대상 테이블 필터 설정 |
| 6 | playwright_screenshot and verify results match all three filter conditions | 모든 필터 조건을 만족하는 로그만 표시됨 |
| 7 | playwright_evaluate to verify each log entry meets all criteria | 각 로그가 작업 유형, 관리자, 테이블 조건 모두 충족 |

---

## TC-C-3-02-006: 데이터 CRUD 로그 조회 - 권한 없는 사용자 접근 시도

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 슈퍼 관리자가 아닌 경우 로그 관리 페이지 접근이 차단됨 |

### 사전 조건

- 여론조사 관리자 또는 콘텐트 운영자로 로그인됨

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/login' | 로그인 페이지 로드 |
| 2 | Login as poll manager or content operator (non-super admin) | 로그인 완료 |
| 3 | playwright_navigate to 'https://metaj.jtbc.co.kr/admin/logs' | 로그 관리 페이지 접근 시도 |
| 4 | playwright_screenshot and verify access denied message or 403 error | 접근 거부 메시지 또는 에러 페이지 표시 |
| 5 | playwright_navigate 현재 URL 확인 | 대시보드 또는 권한 없음 페이지로 리다이렉트됨 |

---

## TC-D-2-01-001: FO 페이지 SEO - 메타 태그 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모든 FO 페이지에 적절한 메타 태그가 포함되어 있음 |

### 사전 조건

- FO 메인 페이지에 접근 가능

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr' | FO 메인 페이지 로드 |
| 2 | playwright_evaluate expression='document.querySelector("meta[name=\"description\"]")?.content' to get meta description | 메타 description 태그가 존재하고 내용이 있음 |
| 3 | playwright_evaluate expression='document.title' to verify page title | 적절한 페이지 title이 설정되어 있음 |
| 4 | playwright_evaluate to check meta keywords (optional) and other meta tags | SEO 관련 메타 태그들이 적절히 설정됨 |
| 5 | playwright_navigate to 'https://metaj.jtbc.co.kr/poll/[poll-id]' (specific poll page) | 개별 여론조사 페이지 로드 |
| 6 | playwright_evaluate to verify poll-specific title and description | 각 페이지별로 고유한 메타 태그가 설정됨 |

---

## TC-D-2-01-002: FO 페이지 SEO - 시맨틱 HTML 구조 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | FO 페이지가 시맨틱 HTML 구조를 따름 |

### 사전 조건

- FO 페이지에 접근 가능

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr' | FO 메인 페이지 로드 |
| 2 | playwright_evaluate expression='document.querySelector("header")' to verify header tag exists | <header> 태그가 존재함 |
| 3 | playwright_evaluate expression='document.querySelector("nav")' to verify nav tag exists | <nav> 태그가 존재함 |
| 4 | playwright_evaluate expression='document.querySelector("main")' to verify main tag exists | <main> 태그가 존재함 |
| 5 | playwright_evaluate expression='document.querySelector("footer")' to verify footer tag exists | <footer> 태그가 존재함 |
| 6 | playwright_evaluate to check for proper heading hierarchy (h1, h2, h3) | 적절한 제목 계층 구조가 사용됨 |
| 7 | playwright_screenshot and verify semantic HTML structure | 시맨틱 HTML 태그가 올바르게 사용됨 |

---

## TC-D-2-01-003: FO 페이지 SEO - Open Graph 태그 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | 모든 FO 페이지에 Open Graph 태그가 포함되어 있음 |

### 사전 조건

- FO 페이지에 접근 가능

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr' | FO 메인 페이지 로드 |
| 2 | playwright_evaluate expression='document.querySelector("meta[property=\"og:title\"]")?.content' | og:title 태그가 존재하고 값이 있음 |
| 3 | playwright_evaluate expression='document.querySelector("meta[property=\"og:description\"]")?.content' | og:description 태그가 존재하고 값이 있음 |
| 4 | playwright_evaluate expression='document.querySelector("meta[property=\"og:image\"]")?.content' | og:image 태그가 존재하고 이미지 URL이 있음 |
| 5 | playwright_evaluate expression='document.querySelector("meta[property=\"og:url\"]")?.content' | og:url 태그가 존재함 (선택사항) |
| 6 | playwright_evaluate expression='document.querySelector("meta[property=\"og:type\"]")?.content' | og:type 태그가 존재함 (선택사항) |
| 7 | playwright_navigate to specific poll page and verify OG tags are poll-specific | 각 페이지별로 고유한 OG 태그가 설정됨 |

---

## TC-D-2-01-004: FO 페이지 SEO - 메타 태그 누락 시 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ❌ 부정 |
| **기대 결과** | 메타 태그가 누락된 페이지는 SEO 검증 실패로 처리됨 |

### 사전 조건

- 일부 페이지에 메타 태그가 누락되어 있을 수 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr/[potentially-incomplete-page]' | 테스트 대상 페이지 로드 |
| 2 | playwright_evaluate to check if meta description is missing | 메타 description이 없거나 빈 값인지 확인 |
| 3 | playwright_evaluate to check if title is generic or missing | title이 일반적이거나 없는지 확인 |
| 4 | playwright_screenshot and document pages with missing or inadequate SEO tags | SEO 태그 누락 페이지 식별 |

---

## TC-D-2-01-005: FO 페이지 SEO - Open Graph 이미지 유효성 확인

| 항목 | 내용 |
|------|------|
| **시나리오 유형** | ✅ 긍정 |
| **기대 결과** | Open Graph 이미지가 유효하고 적절한 크기임 |

### 사전 조건

- FO 페이지에 OG 이미지가 설정되어 있음

### 테스트 단계

| # | 액션 | 기대 결과 |
|---|------|----------|
| 1 | playwright_navigate to 'https://metaj.jtbc.co.kr' | FO 메인 페이지 로드 |
| 2 | playwright_evaluate expression='document.querySelector("meta[property=\"og:image\"]")?.content' to get image URL | og:image URL 추출 |
| 3 | playwright_navigate to extracted image URL or verify with fetch/img load | 이미지 URL이 유효하고 로드됨 |
| 4 | playwright_evaluate to check image dimensions (recommended: 1200x630 for OG) | 이미지 크기가 소셜 미디어 권장 사이즈에 적합함 |
| 5 | If image fails to load or is invalid, document failure | 이미지 유효성 검증 완료 |

---
