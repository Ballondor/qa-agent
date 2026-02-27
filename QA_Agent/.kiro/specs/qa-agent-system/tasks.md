# 구현 계획: QA 에이전트 시스템 (QA Agent System)

## 개요

Strands SDK 기반 멀티 에이전트 QA 자동화 시스템을 구현합니다. Pydantic 데이터 모델 → 에이전트 구현 → 파이프라인 통합 순서로 점진적으로 구축하며, 각 단계마다 속성 기반 테스트와 단위 테스트로 정확성을 검증합니다.

## Tasks

- [x] 1. 프로젝트 구조 설정 및 Pydantic 데이터 모델 구현
  - [x] 1.1 프로젝트 디렉토리 구조 및 의존성 설정
    - `src/qa_agent_system/` 패키지 디렉토리 생성
    - `pyproject.toml` 또는 `requirements.txt`에 의존성 추가 (strands-agents, pydantic, hypothesis, pytest, playwright)
    - `tests/unit/`, `tests/property/` 디렉토리 및 `conftest.py` 생성
    - _요구사항: 1.1, 1.2_

  - [x] 1.2 핵심 데이터 모델 구현 (`src/qa_agent_system/models.py`)
    - `AgentStatusEnum`, `AgentStatus` 모델 구현
    - `TestStep`, `TestCase`, `TestScenario` 모델 구현
    - `TestCaseResult`, `TestExecutionResult` 모델 구현
    - `TestSummary`, `TestReport` 모델 구현
    - `ValidationResult` 모델 구현
    - 각 모델에 Pydantic Field 제약 조건 적용 (비공백 필드 등)
    - _요구사항: 3.2, 3.4, 4.2, 4.7, 5.2, 5.3, 6.1_

  - [x]* 1.3 데이터 모델 JSON 라운드트립 속성 테스트 작성
    - **Property 1: 데이터 모델 JSON 라운드트립 (Data Model JSON Round-Trip)**
    - Hypothesis 전략(Strategy)으로 임의의 TestScenario, TestExecutionResult, TestReport, TestCase, TestCaseResult 생성
    - JSON 직렬화 후 역직렬화하여 원본과 동일한 객체 복원 검증
    - `tests/property/test_roundtrip.py`에 구현
    - **검증 대상: 요구사항 3.5, 4.8, 6.4**

  - [x]* 1.4 데이터 모델 필수 필드 비공백 속성 테스트 작성
    - **Property 10: 데이터 모델 필수 필드 비공백 (Data Model Required Fields Non-Empty)**
    - Hypothesis로 임의의 TestCase, TestCaseResult 생성하여 id, name, steps, expected_result 등 필수 필드 비공백 검증
    - `tests/property/test_scenario.py`에 구현
    - **검증 대상: 요구사항 3.2, 4.2, 1.3**

- [x] 2. 체크포인트 - 데이터 모델 검증
  - 모든 테스트를 실행하여 통과 여부를 확인하고, 문제가 있으면 사용자에게 질문합니다.

- [x] 3. 데이터 검증기 및 에러 처리 구현
  - [x] 3.1 DataValidator 구현 (`src/qa_agent_system/validator.py`)
    - `DataValidator.validate()` 정적 메서드 구현 - JSON 데이터를 Pydantic 스키마로 검증
    - 검증 실패 시 실패 항목과 원인을 포함한 `ValidationResult` 반환
    - _요구사항: 6.2, 6.3_

  - [x]* 3.2 스키마 검증 정확성 속성 테스트 작성
    - **Property 7: 스키마 검증 정확성 (Schema Validation Correctness)**
    - Hypothesis로 유효/무효 JSON 데이터 생성하여 검증 통과/실패 확인
    - 검증 실패 시 ValidationResult.errors에 실패 항목과 원인 포함 확인
    - `tests/property/test_validation.py`에 구현
    - **검증 대상: 요구사항 6.2, 6.3, 2.7**

  - [x] 3.3 에러 처리 모듈 구현 (`src/qa_agent_system/errors.py`)
    - 커스텀 예외 클래스 정의: `AgentInitError`, `ModelConnectionError`, `PipelineError`, `PlaywrightConnectionError`
    - 에러 응답에 에이전트 이름, 오류 원인, 실패 단계 정보 포함
    - _요구사항: 1.4, 1.5, 2.6, 4.5_

  - [x]* 3.4 에러 응답 필수 정보 포함 속성 테스트 작성
    - **Property 8: 에러 응답 필수 정보 포함 (Error Response Required Information)**
    - Hypothesis로 임의의 에이전트 실패 시나리오 생성하여 에러 응답에 필수 정보 포함 검증
    - `tests/property/test_validation.py`에 구현
    - **검증 대상: 요구사항 1.4, 2.6**

- [x] 4. 리포트 생성 에이전트 구현
  - [x] 4.1 ReportAgent 구현 (`src/qa_agent_system/agents/report_agent.py`)
    - `ReportAgent.__init__()` - Strands Agent 래핑 및 시스템 프롬프트 설정
    - `ReportAgent.generate_report()` - TestExecutionResult로부터 TestReport 생성
    - `ReportAgent.format_markdown()` - TestReport를 Markdown 형식으로 포맷팅
    - 빈 실행 결과에 대한 "실행 결과 없음" 리포트 생성 처리
    - TestSummary 통계 계산 로직 (total, passed, failed, success_rate)
    - 실패 테스트의 스크린샷 경로 수집 로직
    - _요구사항: 5.1, 5.2, 5.3, 5.4, 5.5, 5.7_

  - [x]* 4.2 리포트 Markdown 라운드트립 속성 테스트 작성
    - **Property 2: 리포트 Markdown 라운드트립 (Report Markdown Round-Trip)**
    - Hypothesis로 임의의 TestReport 생성하여 Markdown 포맷팅 후 파싱하여 원본 데이터 복원 검증
    - `tests/property/test_roundtrip.py`에 구현
    - **검증 대상: 요구사항 5.6**

  - [x]* 4.3 테스트 요약 통계 정확성 속성 테스트 작성
    - **Property 3: 테스트 요약 통계 정확성 (Test Summary Statistics Accuracy)**
    - Hypothesis로 임의의 TestCaseResult 리스트 생성하여 total == passed + failed, success_rate 정확성 검증
    - `tests/property/test_report_stats.py`에 구현
    - **검증 대상: 요구사항 5.2, 5.3**

  - [x]* 4.4 실패 스크린샷 참조 완전성 속성 테스트 작성
    - **Property 4: 실패 스크린샷 참조 완전성 (Failed Screenshot Reference Completeness)**
    - Hypothesis로 성공/실패 혼합 TestCaseResult 리스트 생성하여 실패 케이스의 스크린샷 경로 포함 검증
    - `tests/property/test_report_stats.py`에 구현
    - **검증 대상: 요구사항 5.4**

  - [x]* 4.5 빈 실행 결과 리포트 단위 테스트 작성
    - 빈 TestExecutionResult에 대해 "실행 결과 없음" 리포트 생성 확인
    - `tests/unit/test_error_handling.py`에 구현
    - _요구사항: 5.7_

- [x] 5. 체크포인트 - 리포트 에이전트 검증
  - 모든 테스트를 실행하여 통과 여부를 확인하고, 문제가 있으면 사용자에게 질문합니다.

- [x] 6. TC 시나리오 작성 에이전트 구현
  - [x] 6.1 TCScenarioAgent 구현 (`src/qa_agent_system/agents/tc_scenario_agent.py`)
    - `TCScenarioAgent.__init__()` - Strands Agent 래핑 및 시스템 프롬프트 설정
    - `TCScenarioAgent.generate_scenario()` - URL과 요구사항으로부터 TestScenario 생성
    - 긍정/부정 시나리오 모두 포함하도록 프롬프트 설계
    - 테스트 단계를 Playwright MCP 실행 가능한 형태로 기술
    - 불충분한 요구사항에 대한 추가 정보 요청 메시지 처리
    - _요구사항: 3.1, 3.2, 3.3, 3.4, 3.6, 3.7_

  - [x]* 6.2 테스트 시나리오 양면성 속성 테스트 작성
    - **Property 9: 테스트 시나리오 양면성 (Test Scenario Dual Coverage)**
    - Hypothesis로 임의의 TestScenario 생성하여 positive/negative 시나리오 각각 최소 1개 포함 검증
    - `tests/property/test_scenario.py`에 구현
    - **검증 대상: 요구사항 3.3**

- [x] 7. 테스트 실행 에이전트 구현
  - [x] 7.1 TestExecutionAgent 구현 (`src/qa_agent_system/agents/test_execution_agent.py`)
    - `TestExecutionAgent.__init__()` - Strands Agent 래핑, Playwright MCP 도구 설정, 시스템 프롬프트 설정
    - `TestExecutionAgent.execute_tests()` - TestScenario의 각 TestCase를 순차 실행
    - `TestExecutionAgent.capture_screenshot()` - 스크린샷 캡처 및 저장 경로 반환
    - 타임아웃 처리: timed_out=true 기록 후 재시도 없이 다음 테스트 계속 실행
    - 실패 시 재시도(retry) 없이 actual_result, expected_result, failure_reason 기록 후 다음 테스트로 진행
    - Playwright MCP 연결 실패 시 재시도 없이 에러 메시지 반환 후 즉시 종료
    - 모든 실패 상황에서 자동 재시도(auto-retry) 수행하지 않음
    - _요구사항: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.9, 4.10_

  - [x]* 7.2 타임아웃 시 계속 실행 속성 테스트 작성
    - **Property 11: 타임아웃 시 계속 실행 (Continue Execution on Timeout)**
    - Hypothesis로 타임아웃 포함 TestScenario 생성하여 결과 목록 길이 == 입력 테스트 케이스 수 검증
    - `tests/property/test_execution.py`에 구현
    - **검증 대상: 요구사항 4.6**

  - [x]* 7.3 실패 테스트 차이 기록 속성 테스트 작성
    - **Property 12: 실패 테스트 차이 기록 (Failed Test Difference Recording)**
    - Hypothesis로 실패 TestCaseResult 생성하여 failure_reason 비공백, actual_result/expected_result 기록 검증
    - `tests/property/test_execution.py`에 구현
    - **검증 대상: 요구사항 4.3**

  - [x]* 7.4 Playwright MCP 연결 실패 및 스크린샷 단위 테스트 작성
    - Playwright MCP 연결 실패 시 에러 메시지 확인
    - 스크린샷 캡처 및 저장 경로 확인
    - `tests/unit/test_error_handling.py`, `tests/unit/test_screenshot.py`에 구현
    - _요구사항: 4.4, 4.5_

- [x] 8. 체크포인트 - 개별 에이전트 검증
  - 모든 테스트를 실행하여 통과 여부를 확인하고, 문제가 있으면 사용자에게 질문합니다.

- [x] 9. 오케스트레이터 에이전트 및 파이프라인 통합
  - [x] 9.1 OrchestratorAgent 구현 (`src/qa_agent_system/agents/orchestrator_agent.py`)
    - `OrchestratorAgent.__init__()` - Strands Agent 래핑 및 시스템 프롬프트 설정
    - `OrchestratorAgent.execute_pipeline()` - TC → Execution → Report 순서로 파이프라인 실행
    - `OrchestratorAgent.validate_data()` - DataValidator를 사용한 에이전트 간 데이터 스키마 검증
    - `OrchestratorAgent.get_agent_status()` - 에이전트 작업 상태 추적 (IDLE → RUNNING → COMPLETED/FAILED)
    - 하위 에이전트 실패 시 에이전트 이름, 실패 단계, 오류 내용 포함 에러 전달
    - _요구사항: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [x]* 9.2 에이전트 상태 전이 순서 속성 테스트 작성
    - **Property 5: 에이전트 상태 전이 순서 (Agent Status Transition Order)**
    - Hypothesis로 임의의 상태 전이 시퀀스 생성하여 IDLE → RUNNING → COMPLETED/FAILED 순서 검증
    - `tests/property/test_pipeline.py`에 구현
    - **검증 대상: 요구사항 2.5**

  - [x]* 9.3 파이프라인 실행 순서 속성 테스트 작성
    - **Property 6: 파이프라인 실행 순서 (Pipeline Execution Order)**
    - 모킹된 에이전트로 파이프라인 실행하여 TC → Execution → Report 순서 및 데이터 전달 검증
    - `tests/property/test_pipeline.py`에 구현
    - **검증 대상: 요구사항 2.1, 2.2, 2.3, 2.4**

- [x] 10. QAAgentSystem 메인 진입점 및 시스템 통합
  - [x] 10.1 QAAgentSystem 구현 (`src/qa_agent_system/system.py`)
    - `QAAgentSystem.__init__()` - 4개 에이전트 초기화 (Bedrock Opus 4.6 모델 설정)
    - `QAAgentSystem.run()` - OrchestratorAgent를 통한 전체 QA 프로세스 실행
    - 에이전트 초기화 실패 시 에이전트 이름 + 원인 포함 에러 반환
    - Bedrock 모델 연결 실패 시 연결 실패 원인 + 재시도 안내 반환
    - _요구사항: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x]* 10.2 시스템 초기화 단위 테스트 작성
    - 4개 에이전트 생성 확인, 각 에이전트에 Bedrock Opus 모델 설정 확인
    - 에이전트 초기화 실패 시 에러 메시지 확인
    - Bedrock 모델 연결 실패 시 에러 메시지 및 재시도 안내 확인
    - `tests/unit/test_agent_init.py`에 구현
    - _요구사항: 1.1, 1.2, 1.4, 1.5_

  - [x] 10.3 `__init__.py` 모듈 내보내기 설정
    - `src/qa_agent_system/__init__.py`에서 주요 클래스 및 모델 내보내기
    - `src/qa_agent_system/agents/__init__.py` 설정
    - _요구사항: 1.1_

- [x] 11. 최종 체크포인트 - 전체 시스템 검증
  - 모든 테스트(단위 테스트 + 속성 기반 테스트)를 실행하여 통과 여부를 확인하고, 문제가 있으면 사용자에게 질문합니다.

## 참고 사항

- 각 태스크는 추적 가능성을 위해 특정 요구사항을 참조합니다
- 체크포인트에서 점진적 검증을 수행합니다
- 속성 테스트는 보편적 정확성 속성을 검증하고, 단위 테스트는 특정 예제와 엣지 케이스를 검증합니다
