"""
QA 에이전트 시스템 핵심 데이터 모델

에이전트 간 통신에 사용되는 Pydantic 기반 데이터 모델을 정의합니다.
모든 모델은 JSON 직렬화/역직렬화 및 스키마 검증을 지원합니다.

요구사항: 3.2, 3.4, 4.2, 4.7, 5.2, 5.3, 6.1
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================
# 에이전트 상태 모델 (Agent Status Models)
# ============================================================


class AgentStatusEnum(str, Enum):
    """에이전트 작업 상태 열거형(Enum)

    에이전트의 현재 작업 상태를 나타냅니다.
    상태 전이 순서: IDLE → RUNNING → COMPLETED 또는 IDLE → RUNNING → FAILED
    """

    IDLE = "idle"  # 대기
    RUNNING = "running"  # 진행 중
    COMPLETED = "completed"  # 완료
    FAILED = "failed"  # 실패


class AgentStatus(BaseModel):
    """에이전트 상태 정보 모델

    각 에이전트의 현재 상태와 실행 시간 정보를 추적합니다.
    """

    agent_name: str = Field(..., min_length=1, description="에이전트 이름 (비공백)")
    status: AgentStatusEnum = Field(..., description="현재 작업 상태")
    started_at: Optional[datetime] = Field(
        default=None, description="작업 시작 시간"
    )
    completed_at: Optional[datetime] = Field(
        default=None, description="작업 완료 시간"
    )
    error_message: Optional[str] = Field(
        default=None, description="실패 시 에러 메시지"
    )


# ============================================================
# 테스트 케이스 및 시나리오 모델 (Test Case & Scenario Models)
# 요구사항 3.2: 고유 식별자, 테스트 이름, 사전 조건, 테스트 단계, 기대 결과 포함
# 요구사항 3.4: JSON 형식 출력 지원
# ============================================================


class TestStep(BaseModel):
    """테스트 단계 모델

    Playwright MCP가 실행 가능한 형태로 기술된 개별 테스트 단계입니다.
    """

    step_number: int = Field(..., ge=1, description="단계 번호 (1 이상)")
    action: str = Field(..., min_length=1, description="Playwright MCP 실행 가능한 액션 기술 (비공백)")
    expected_result: str = Field(
        ..., min_length=1, description="기대 결과 (비공백)"
    )


class TestCase(BaseModel):
    """테스트 케이스 모델

    특정 기능이나 시나리오를 검증하기 위한 테스트 항목입니다.
    요구사항 3.2: id, name, steps, expected_result 필수 필드 비공백
    """

    id: str = Field(..., min_length=1, description="고유 식별자 (예: 'TC-001', 비공백)")
    name: str = Field(..., min_length=1, description="테스트 이름 (비공백)")
    preconditions: list[str] = Field(
        default_factory=list, description="사전 조건 목록"
    )
    steps: list[TestStep] = Field(
        ..., min_length=1, description="테스트 단계 목록 (최소 1개)"
    )
    expected_result: str = Field(
        ..., min_length=1, description="기대 결과 (비공백)"
    )
    scenario_type: str = Field(
        ..., description="시나리오 유형: 'positive' 또는 'negative'"
    )

    @field_validator("scenario_type")
    @classmethod
    def validate_scenario_type(cls, v: str) -> str:
        """시나리오 유형이 'positive' 또는 'negative'인지 검증합니다."""
        if v not in ("positive", "negative"):
            raise ValueError(
                f"scenario_type은 'positive' 또는 'negative'여야 합니다. 입력값: '{v}'"
            )
        return v


class TestScenario(BaseModel):
    """테스트 시나리오 모델 - TC Scenario Agent의 출력

    하나 이상의 TestCase를 포함하는 테스트 시나리오 문서입니다.
    요구사항 3.4: JSON 형식으로 직렬화 가능
    """

    target_url: str = Field(
        ..., min_length=1, description="테스트 대상 URL (비공백)"
    )
    requirements: str = Field(
        ..., min_length=1, description="테스트 요구사항 (비공백)"
    )
    test_cases: list[TestCase] = Field(
        ..., min_length=1, description="테스트 케이스 목록 (최소 1개)"
    )
    created_at: datetime = Field(..., description="시나리오 생성 시간")


# ============================================================
# 테스트 실행 결과 모델 (Test Execution Result Models)
# 요구사항 4.2: 테스트 ID, 성공/실패 여부, 실행 시간, 스크린샷 경로 포함
# 요구사항 4.7: JSON 형식 반환 지원
# ============================================================


class TestCaseResult(BaseModel):
    """개별 테스트 케이스 실행 결과 모델

    요구사항 4.2: test_case_id, test_name 필수 필드 비공백
    """

    test_case_id: str = Field(
        ..., min_length=1, description="테스트 케이스 ID (비공백)"
    )
    test_name: str = Field(
        ..., min_length=1, description="테스트 이름 (비공백)"
    )
    passed: bool = Field(..., description="성공/실패 여부")
    execution_time_ms: float = Field(
        ..., ge=0, description="실행 시간 (밀리초, 0 이상)"
    )
    screenshot_path: Optional[str] = Field(
        default=None, description="스크린샷 저장 경로"
    )
    actual_result: Optional[str] = Field(
        default=None, description="실제 결과"
    )
    expected_result: Optional[str] = Field(
        default=None, description="기대 결과"
    )
    failure_reason: Optional[str] = Field(
        default=None, description="실패 원인"
    )
    timed_out: bool = Field(default=False, description="타임아웃 발생 여부")


class TestExecutionResult(BaseModel):
    """전체 테스트 실행 결과 모델 - Test Execution Agent의 출력

    요구사항 4.7: JSON 형식으로 직렬화 가능
    """

    scenario_id: str = Field(
        ..., min_length=1, description="시나리오 ID (비공백)"
    )
    target_url: str = Field(
        ..., min_length=1, description="테스트 대상 URL (비공백)"
    )
    results: list[TestCaseResult] = Field(
        default_factory=list, description="개별 테스트 케이스 실행 결과 목록"
    )
    total_execution_time_ms: float = Field(
        ..., ge=0, description="전체 실행 시간 (밀리초, 0 이상)"
    )
    executed_at: datetime = Field(..., description="실행 시간")


# ============================================================
# 테스트 리포트 모델 (Test Report Models)
# 요구사항 5.2: 전체 테스트 요약 (총 테스트 수, 성공 수, 실패 수, 성공률)
# 요구사항 5.3: 각 TestCase별 상세 결과 포함
# ============================================================


class TestSummary(BaseModel):
    """테스트 요약 모델

    전체 테스트 실행 결과의 통계 요약입니다.
    요구사항 5.2: total_tests, passed_tests, failed_tests, success_rate 포함
    """

    total_tests: int = Field(..., ge=0, description="총 테스트 수 (0 이상)")
    passed_tests: int = Field(..., ge=0, description="성공한 테스트 수 (0 이상)")
    failed_tests: int = Field(..., ge=0, description="실패한 테스트 수 (0 이상)")
    success_rate: float = Field(
        ..., ge=0.0, le=1.0, description="성공률 (0.0 ~ 1.0)"
    )


class TestReport(BaseModel):
    """테스트 리포트 모델 - Report Agent의 출력

    테스트 실행 결과를 요약한 리포트 문서입니다.
    요구사항 5.3: 각 TestCase별 상세 결과 포함
    """

    title: str = Field(..., min_length=1, description="리포트 제목 (비공백)")
    summary: TestSummary = Field(..., description="테스트 요약 통계")
    detailed_results: list[TestCaseResult] = Field(
        default_factory=list, description="각 TestCase별 상세 결과 목록"
    )
    failed_screenshots: list[str] = Field(
        default_factory=list, description="실패한 테스트의 스크린샷 경로 목록"
    )
    generated_at: datetime = Field(..., description="리포트 생성 시간")
    markdown_content: str = Field(
        default="", description="Markdown 형식의 리포트 내용"
    )


# ============================================================
# 검증 결과 모델 (Validation Result Model)
# 요구사항 6.1: 에이전트 간 데이터 전달 시 JSON 형식 사용
# ============================================================


class ValidationResult(BaseModel):
    """데이터 스키마 검증 결과 모델

    에이전트 간 전달되는 데이터의 스키마 검증 결과를 나타냅니다.
    """

    is_valid: bool = Field(..., description="검증 통과 여부")
    errors: list[str] = Field(
        default_factory=list, description="검증 실패 항목 및 원인 목록"
    )
