"""리포트 통계 속성 기반 테스트 (Property-Based Tests)

Property 3: 테스트 요약 통계 정확성 (Test Summary Statistics Accuracy)
Property 4: 실패 스크린샷 참조 완전성 (Failed Screenshot Reference Completeness)

Feature: qa-agent-system
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from qa_agent_system.agents.report_agent import ReportAgent
from qa_agent_system.models import TestCaseResult

# conftest.py에서 정의된 Hypothesis 전략 사용
from tests.conftest import st_test_case_result


# ============================================================
# Property 3: 테스트 요약 통계 정확성 (Test Summary Statistics Accuracy)
# Feature: qa-agent-system, Property 3: 테스트 요약 통계 정확성
# **Validates: Requirements 5.2, 5.3**
# ============================================================


@given(results=st.lists(st_test_case_result(), min_size=0, max_size=20))
@settings(max_examples=100)
def test_summary_statistics_accuracy(results: list[TestCaseResult]) -> None:
    """임의의 TestCaseResult 리스트에 대해 요약 통계가 정확한지 검증합니다.

    검증 항목:
    1. total_tests == passed_tests + failed_tests
    2. success_rate == passed_tests / total_tests (total_tests == 0이면 0.0)
    3. total_tests == len(입력 결과 리스트)
    """
    agent = ReportAgent()
    summary = agent._compute_summary(results)

    # 1. total_tests는 passed_tests + failed_tests와 같아야 합니다
    assert summary.total_tests == summary.passed_tests + summary.failed_tests, (
        f"total({summary.total_tests}) != "
        f"passed({summary.passed_tests}) + failed({summary.failed_tests})"
    )

    # 2. success_rate 정확성 검증
    if summary.total_tests == 0:
        # 빈 결과일 때 success_rate는 0.0이어야 합니다
        assert summary.success_rate == 0.0, (
            f"빈 결과의 success_rate가 0.0이 아닙니다: {summary.success_rate}"
        )
    else:
        # success_rate == passed_tests / total_tests
        expected_rate = summary.passed_tests / summary.total_tests
        assert abs(summary.success_rate - expected_rate) < 1e-9, (
            f"success_rate({summary.success_rate}) != "
            f"passed({summary.passed_tests}) / total({summary.total_tests}) = {expected_rate}"
        )

    # 3. total_tests는 입력 결과 리스트의 길이와 같아야 합니다
    assert summary.total_tests == len(results), (
        f"total_tests({summary.total_tests}) != len(results)({len(results)})"
    )


# ============================================================
# Property 4: 실패 스크린샷 참조 완전성 (Failed Screenshot Reference Completeness)
# Feature: qa-agent-system, Property 4: 실패 스크린샷 참조 완전성
# **Validates: Requirements 5.4**
# ============================================================


@given(results=st.lists(st_test_case_result(), min_size=0, max_size=20))
@settings(max_examples=100)
def test_failed_screenshot_reference_completeness(results: list[TestCaseResult]) -> None:
    """임의의 성공/실패 혼합 TestCaseResult 리스트에 대해
    실패 케이스의 스크린샷 경로가 완전히 포함되는지 검증합니다.

    검증 항목:
    1. 실패한(passed == False) TestCaseResult 중 screenshot_path가 있는 것은
       모두 failed_screenshots에 포함되어야 합니다
    2. 성공한(passed == True) TestCaseResult의 screenshot_path는
       failed_screenshots에 포함되지 않아야 합니다
    """
    agent = ReportAgent()
    failed_screenshots = agent._collect_failed_screenshots(results)

    # 1. 실패한 케이스의 스크린샷 경로가 모두 포함되어야 합니다
    for r in results:
        if not r.passed and r.screenshot_path is not None:
            assert r.screenshot_path in failed_screenshots, (
                f"실패 케이스({r.test_case_id})의 스크린샷 경로 "
                f"'{r.screenshot_path}'가 failed_screenshots에 없습니다"
            )

    # 2. 성공한 케이스의 스크린샷 경로는 포함되지 않아야 합니다
    # 성공한 케이스에서만 나오는 고유 경로를 확인합니다
    passed_only_paths = set()
    failed_paths = set()
    for r in results:
        if r.screenshot_path is not None:
            if not r.passed:
                failed_paths.add(r.screenshot_path)
            else:
                passed_only_paths.add(r.screenshot_path)

    # 성공 케이스에만 존재하는 경로(실패 케이스에는 없는)가 failed_screenshots에 없어야 합니다
    truly_passed_only = passed_only_paths - failed_paths
    for path in truly_passed_only:
        assert path not in failed_screenshots, (
            f"성공 케이스의 스크린샷 경로 '{path}'가 "
            f"failed_screenshots에 포함되어 있습니다"
        )
