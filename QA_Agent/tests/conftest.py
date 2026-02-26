"""공통 테스트 픽스처(fixture) 및 Hypothesis 전략(Strategy) 정의

각 데이터 모델에 대한 Hypothesis 전략을 정의하여
속성 기반 테스트(Property-Based Test)에서 재사용합니다.
"""

import pytest
from hypothesis import settings
from hypothesis import strategies as st
from datetime import datetime, timezone

from qa_agent_system.models import (
    AgentStatusEnum,
    AgentStatus,
    TestStep,
    TestCase,
    TestScenario,
    TestCaseResult,
    TestExecutionResult,
    TestSummary,
    TestReport,
    ValidationResult,
)

# Hypothesis 기본 설정: 각 속성 테스트당 최소 100회 반복
settings.register_profile("default", max_examples=100)
settings.register_profile("ci", max_examples=200)
settings.load_profile("default")


# ============================================================
# 기본 전략 (Basic Strategies)
# ============================================================

# 비공백 문자열 전략 (최소 1자 이상)
non_empty_text = st.text(min_size=1, max_size=50).filter(lambda s: s.strip() != "")

# URL 형태 문자열 전략
url_strategy = st.from_regex(r"https?://[a-z]{1,10}\.[a-z]{2,4}", fullmatch=True)

# datetime 전략 (JSON 직렬화 호환)
datetime_strategy = st.datetimes(
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2030, 12, 31),
)


# ============================================================
# 데이터 모델 전략 (Data Model Strategies)
# 함수명에 test_ 접두사를 사용하지 않아 pytest 수집을 방지합니다.
# ============================================================


@st.composite
def st_test_step(draw: st.DrawFn) -> TestStep:
    """임의의 TestStep 생성 전략"""
    return TestStep(
        step_number=draw(st.integers(min_value=1, max_value=100)),
        action=draw(non_empty_text),
        expected_result=draw(non_empty_text),
    )


@st.composite
def st_test_case(draw: st.DrawFn) -> TestCase:
    """임의의 TestCase 생성 전략"""
    return TestCase(
        id=draw(non_empty_text),
        name=draw(non_empty_text),
        preconditions=draw(st.lists(non_empty_text, min_size=0, max_size=5)),
        steps=draw(st.lists(st_test_step(), min_size=1, max_size=5)),
        expected_result=draw(non_empty_text),
        scenario_type=draw(st.sampled_from(["positive", "negative"])),
    )


@st.composite
def st_test_scenario(draw: st.DrawFn) -> TestScenario:
    """임의의 TestScenario 생성 전략"""
    return TestScenario(
        target_url=draw(url_strategy),
        requirements=draw(non_empty_text),
        test_cases=draw(st.lists(st_test_case(), min_size=1, max_size=5)),
        created_at=draw(datetime_strategy),
    )


@st.composite
def st_test_case_result(draw: st.DrawFn) -> TestCaseResult:
    """임의의 TestCaseResult 생성 전략"""
    passed = draw(st.booleans())
    timed_out = draw(st.booleans()) if not passed else False

    return TestCaseResult(
        test_case_id=draw(non_empty_text),
        test_name=draw(non_empty_text),
        passed=passed,
        execution_time_ms=draw(st.floats(min_value=0.0, max_value=60000.0, allow_nan=False, allow_infinity=False)),
        screenshot_path=draw(st.one_of(st.none(), non_empty_text)),
        actual_result=draw(st.one_of(st.none(), non_empty_text)),
        expected_result=draw(st.one_of(st.none(), non_empty_text)),
        failure_reason=draw(st.one_of(st.none(), non_empty_text)) if not passed else None,
        timed_out=timed_out,
    )



@st.composite
def st_test_execution_result(draw: st.DrawFn) -> TestExecutionResult:
    """임의의 TestExecutionResult 생성 전략"""
    return TestExecutionResult(
        scenario_id=draw(non_empty_text),
        target_url=draw(url_strategy),
        results=draw(st.lists(st_test_case_result(), min_size=0, max_size=5)),
        total_execution_time_ms=draw(st.floats(min_value=0.0, max_value=300000.0, allow_nan=False, allow_infinity=False)),
        executed_at=draw(datetime_strategy),
    )


@st.composite
def st_test_summary(draw: st.DrawFn) -> TestSummary:
    """임의의 TestSummary 생성 전략"""
    total = draw(st.integers(min_value=0, max_value=100))
    passed = draw(st.integers(min_value=0, max_value=total))
    failed = total - passed
    success_rate = passed / total if total > 0 else 0.0

    return TestSummary(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        success_rate=success_rate,
    )


@st.composite
def st_test_report(draw: st.DrawFn) -> TestReport:
    """임의의 TestReport 생성 전략"""
    return TestReport(
        title=draw(non_empty_text),
        summary=draw(st_test_summary()),
        detailed_results=draw(st.lists(st_test_case_result(), min_size=0, max_size=5)),
        failed_screenshots=draw(st.lists(non_empty_text, min_size=0, max_size=5)),
        generated_at=draw(datetime_strategy),
        markdown_content=draw(st.text(max_size=200)),
    )
