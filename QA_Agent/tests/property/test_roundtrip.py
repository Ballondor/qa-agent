"""Property 1: 데이터 모델 JSON 라운드트립 (Data Model JSON Round-Trip)

임의의 유효한 데이터 모델에 대해, JSON으로 직렬화(serialize)한 후
역직렬화(deserialize)하면 원본과 동일한 객체를 복원해야 합니다.

Feature: qa-agent-system, Property 1: 데이터 모델 JSON 라운드트립

검증 대상: 요구사항 3.5, 4.8, 6.4
"""

from hypothesis import given

from qa_agent_system.models import (
    TestCase,
    TestCaseResult,
    TestExecutionResult,
    TestReport,
    TestScenario,
)
from tests.conftest import (
    st_test_case,
    st_test_case_result,
    st_test_execution_result,
    st_test_report,
    st_test_scenario,
)


class TestDataModelJsonRoundTrip:
    """데이터 모델 JSON 라운드트립 속성 테스트

    **Validates: Requirements 3.5, 4.8, 6.4**

    각 모델에 대해 model_dump_json() → model_validate_json() 라운드트립을
    검증하여, JSON 직렬화/역직렬화 후 원본과 동일한 객체가 복원되는지 확인합니다.
    """

    @given(scenario=st_test_scenario())
    def test_scenario_json_roundtrip(self, scenario: TestScenario) -> None:
        """TestScenario JSON 라운드트립 검증

        **Validates: Requirements 3.5**
        """
        # JSON 직렬화 후 역직렬화하여 원본과 동일한 객체 복원 확인
        json_str = scenario.model_dump_json()
        restored = TestScenario.model_validate_json(json_str)
        assert restored == scenario

    @given(result=st_test_execution_result())
    def test_execution_result_json_roundtrip(self, result: TestExecutionResult) -> None:
        """TestExecutionResult JSON 라운드트립 검증

        **Validates: Requirements 4.8**
        """
        json_str = result.model_dump_json()
        restored = TestExecutionResult.model_validate_json(json_str)
        assert restored == result

    @given(report=st_test_report())
    def test_report_json_roundtrip(self, report: TestReport) -> None:
        """TestReport JSON 라운드트립 검증

        **Validates: Requirements 6.4**
        """
        json_str = report.model_dump_json()
        restored = TestReport.model_validate_json(json_str)
        assert restored == report

    @given(test_case=st_test_case())
    def test_case_json_roundtrip(self, test_case: TestCase) -> None:
        """TestCase JSON 라운드트립 검증

        **Validates: Requirements 3.5**
        """
        json_str = test_case.model_dump_json()
        restored = TestCase.model_validate_json(json_str)
        assert restored == test_case

    @given(result=st_test_case_result())
    def test_case_result_json_roundtrip(self, result: TestCaseResult) -> None:
        """TestCaseResult JSON 라운드트립 검증

        **Validates: Requirements 4.8**
        """
        json_str = result.model_dump_json()
        restored = TestCaseResult.model_validate_json(json_str)
        assert restored == result


# ============================================================
# Property 2: 리포트 Markdown 라운드트립 (Report Markdown Round-Trip)
# Feature: qa-agent-system, Property 2: 리포트 Markdown 라운드트립
#
# 임의의 유효한 TestReport에 대해, Markdown으로 포맷팅한 후
# 다시 파싱하면 원본과 동일한 리포트 데이터를 복원해야 합니다.
#
# 검증 대상: 요구사항 5.6
# ============================================================

import re
from datetime import datetime
from typing import Optional

from hypothesis import given, settings
from hypothesis import strategies as st

from qa_agent_system.agents.report_agent import ReportAgent
from qa_agent_system.models import TestCaseResult, TestReport, TestSummary


def _unescape_pipe(text: str) -> str:
    """Markdown 테이블에서 이스케이프된 파이프(\\|)를 복원합니다."""
    return text.replace("\\|", "|")


def _parse_optional(value: str) -> Optional[str]:
    """빈 문자열을 None으로, 그 외는 언이스케이프된 문자열로 변환합니다."""
    unescaped = _unescape_pipe(value)
    return unescaped if unescaped else None


def _split_table_row(line: str) -> list[str]:
    """Markdown 테이블 행을 파싱하여 셀 값 목록을 반환합니다.

    이스케이프된 파이프(\\|)를 고려하여 셀을 분리합니다.
    """
    # 이스케이프된 파이프를 임시 플레이스홀더로 치환
    placeholder = "\x00PIPE\x00"
    temp = line.replace("\\|", placeholder)
    # 실제 파이프로 분리
    cells = temp.split("|")
    # 앞뒤 빈 셀 제거 (| ... | 형식이므로 첫/마지막은 빈 문자열)
    cells = [c.strip() for c in cells]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    # 플레이스홀더를 이스케이프된 파이프로 복원
    cells = [c.replace(placeholder, "\\|") for c in cells]
    return cells


def parse_markdown(markdown: str) -> dict:
    """ReportAgent.format_markdown()이 생성한 Markdown을 파싱하여
    원본 리포트 데이터를 딕셔너리로 복원합니다.

    Returns:
        {
            "title": str,
            "summary": {"total_tests": int, "passed_tests": int,
                         "failed_tests": int, "success_rate": float},
            "generated_at": str (ISO 형식),
            "detailed_results": list[dict],
            "failed_screenshots": list[str],
        }
    """
    lines = markdown.split("\n")
    result: dict = {
        "title": "",
        "summary": {},
        "generated_at": "",
        "detailed_results": [],
        "failed_screenshots": [],
    }

    current_section = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # H1 제목 파싱
        if line.startswith("# ") and not line.startswith("## "):
            result["title"] = line[2:].strip()
            current_section = "title"
            i += 1
            continue

        # H2 섹션 감지
        if line.startswith("## "):
            section_name = line[3:].strip()
            if section_name == "요약":
                current_section = "summary"
            elif section_name == "상세 결과":
                current_section = "detailed_results"
            elif section_name == "실패 스크린샷":
                current_section = "screenshots"
            i += 1
            continue

        # 요약 섹션 파싱 (키-값 쌍)
        if current_section == "summary" and line.startswith("- "):
            kv = line[2:].strip()
            if ": " in kv:
                key, value = kv.split(": ", 1)
                key = key.strip()
                value = value.strip()
                if key == "generated_at":
                    result["generated_at"] = value
                elif key in ("total_tests", "passed_tests", "failed_tests"):
                    result["summary"][key] = int(value)
                elif key == "success_rate":
                    result["summary"][key] = float(value)
            i += 1
            continue

        # 상세 결과 테이블 파싱
        if current_section == "detailed_results":
            # 구분선(--- 행) 건너뛰기
            if line.strip().startswith("| ---"):
                i += 1
                continue
            # 헤더 행 건너뛰기
            if line.strip().startswith("| test_case_id"):
                i += 1
                continue
            # 데이터 행 파싱
            if line.strip().startswith("|"):
                cells = _split_table_row(line)
                if len(cells) == 9:
                    row = {
                        "test_case_id": _unescape_pipe(cells[0]),
                        "test_name": _unescape_pipe(cells[1]),
                        "passed": cells[2] == "True",
                        "execution_time_ms": float(cells[3]),
                        "screenshot_path": _parse_optional(cells[4]),
                        "actual_result": _parse_optional(cells[5]),
                        "expected_result": _parse_optional(cells[6]),
                        "failure_reason": _parse_optional(cells[7]),
                        "timed_out": cells[8] == "True",
                    }
                    result["detailed_results"].append(row)
            i += 1
            continue

        # 실패 스크린샷 섹션 파싱
        if current_section == "screenshots":
            if line.startswith("- "):
                path = line[2:].strip()
                result["failed_screenshots"].append(path)
            i += 1
            continue

        i += 1

    return result


# ============================================================
# Markdown 라운드트립 테스트용 Hypothesis 전략
# 개행 문자와 특수 제어 문자를 제외한 문자열 전략
# ============================================================

# Markdown 테이블 셀에 안전한 문자열
# 개행, 널 문자, 공백 카테고리 제어 문자를 제외하여
# strip()에 의한 데이터 손실을 방지합니다.
_safe_alphabet = st.characters(
    blacklist_categories=("Cs", "Zl", "Zp", "Cc"),  # 서로게이트, 줄/단락 구분자, 제어 문자 제외
    blacklist_characters="\n\r\x00\x0b\x0c\t ",  # 개행, 탭, 공백 등 제외
)
_safe_text = st.text(alphabet=_safe_alphabet, min_size=1, max_size=30).filter(
    lambda s: len(s.strip()) == len(s) and len(s) > 0
)

# 스크린샷 경로용 안전한 문자열 (동일 제약)
_safe_path = st.text(alphabet=_safe_alphabet, min_size=1, max_size=30).filter(
    lambda s: len(s.strip()) == len(s) and len(s) > 0
)


@st.composite
def st_safe_test_case_result(draw: st.DrawFn) -> TestCaseResult:
    """Markdown 라운드트립 테스트용 TestCaseResult 생성 전략

    개행 문자가 포함되지 않는 안전한 문자열만 사용합니다.
    """
    passed = draw(st.booleans())
    timed_out = draw(st.booleans()) if not passed else False

    return TestCaseResult(
        test_case_id=draw(_safe_text),
        test_name=draw(_safe_text),
        passed=passed,
        execution_time_ms=draw(
            st.floats(min_value=0.0, max_value=60000.0,
                      allow_nan=False, allow_infinity=False)
        ),
        screenshot_path=draw(st.one_of(st.none(), _safe_path)),
        actual_result=draw(st.one_of(st.none(), _safe_text)),
        expected_result=draw(st.one_of(st.none(), _safe_text)),
        failure_reason=draw(st.one_of(st.none(), _safe_text)) if not passed else None,
        timed_out=timed_out,
    )


@st.composite
def st_safe_test_summary(draw: st.DrawFn) -> TestSummary:
    """Markdown 라운드트립 테스트용 TestSummary 생성 전략"""
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
def st_safe_test_report(draw: st.DrawFn) -> TestReport:
    """Markdown 라운드트립 테스트용 TestReport 생성 전략

    개행 문자가 포함되지 않는 안전한 문자열만 사용합니다.
    """
    from tests.conftest import datetime_strategy

    return TestReport(
        title=draw(_safe_text),
        summary=draw(st_safe_test_summary()),
        detailed_results=draw(
            st.lists(st_safe_test_case_result(), min_size=0, max_size=5)
        ),
        failed_screenshots=draw(
            st.lists(_safe_path, min_size=0, max_size=5)
        ),
        generated_at=draw(datetime_strategy),
        markdown_content=draw(st.just("")),  # 라운드트립 테스트에서는 무시
    )


class TestReportMarkdownRoundTrip:
    """리포트 Markdown 라운드트립 속성 테스트

    **Validates: Requirements 5.6**

    임의의 TestReport를 Markdown으로 포맷팅한 후 파싱하여
    원본 데이터가 정확히 복원되는지 검증합니다.
    """

    # Feature: qa-agent-system, Property 2: 리포트 Markdown 라운드트립

    @given(report=st_safe_test_report())
    def test_markdown_roundtrip_title(self, report: TestReport) -> None:
        """Markdown 라운드트립 후 제목이 동일한지 검증

        **Validates: Requirements 5.6**
        """
        agent = ReportAgent()
        markdown = agent.format_markdown(report)
        parsed = parse_markdown(markdown)

        assert parsed["title"] == report.title

    @given(report=st_safe_test_report())
    def test_markdown_roundtrip_summary(self, report: TestReport) -> None:
        """Markdown 라운드트립 후 요약 통계가 동일한지 검증

        **Validates: Requirements 5.6**
        """
        agent = ReportAgent()
        markdown = agent.format_markdown(report)
        parsed = parse_markdown(markdown)

        # 정수 필드 정확 비교
        assert parsed["summary"]["total_tests"] == report.summary.total_tests
        assert parsed["summary"]["passed_tests"] == report.summary.passed_tests
        assert parsed["summary"]["failed_tests"] == report.summary.failed_tests

        # success_rate는 float 포맷팅 정밀도 문제로 근사 비교
        assert abs(
            parsed["summary"]["success_rate"] - report.summary.success_rate
        ) < 1e-6

    @given(report=st_safe_test_report())
    def test_markdown_roundtrip_generated_at(self, report: TestReport) -> None:
        """Markdown 라운드트립 후 생성 시간이 동일한지 검증

        **Validates: Requirements 5.6**
        """
        agent = ReportAgent()
        markdown = agent.format_markdown(report)
        parsed = parse_markdown(markdown)

        # ISO 형식 문자열로 비교
        assert parsed["generated_at"] == report.generated_at.isoformat()

    @given(report=st_safe_test_report())
    def test_markdown_roundtrip_detailed_results(self, report: TestReport) -> None:
        """Markdown 라운드트립 후 상세 결과가 동일한지 검증

        **Validates: Requirements 5.6**
        """
        agent = ReportAgent()
        markdown = agent.format_markdown(report)
        parsed = parse_markdown(markdown)

        # 상세 결과 개수 일치 확인
        assert len(parsed["detailed_results"]) == len(report.detailed_results)

        # 각 결과 항목 비교
        for parsed_row, original in zip(
            parsed["detailed_results"], report.detailed_results
        ):
            assert parsed_row["test_case_id"] == original.test_case_id
            assert parsed_row["test_name"] == original.test_name
            assert parsed_row["passed"] == original.passed
            assert abs(
                parsed_row["execution_time_ms"] - original.execution_time_ms
            ) < 1e-6
            assert parsed_row["screenshot_path"] == original.screenshot_path
            assert parsed_row["actual_result"] == original.actual_result
            assert parsed_row["expected_result"] == original.expected_result
            assert parsed_row["failure_reason"] == original.failure_reason
            assert parsed_row["timed_out"] == original.timed_out

    @given(report=st_safe_test_report())
    def test_markdown_roundtrip_failed_screenshots(self, report: TestReport) -> None:
        """Markdown 라운드트립 후 실패 스크린샷 목록이 동일한지 검증

        **Validates: Requirements 5.6**
        """
        agent = ReportAgent()
        markdown = agent.format_markdown(report)
        parsed = parse_markdown(markdown)

        assert parsed["failed_screenshots"] == report.failed_screenshots
