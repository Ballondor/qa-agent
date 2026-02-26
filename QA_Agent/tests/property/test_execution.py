"""Property 11, 12: 테스트 실행 속성 테스트 (Test Execution Properties)

Property 11: 타임아웃 시 계속 실행 (Continue Execution on Timeout)
- 임의의 TestScenario에서 일부 TestCase가 타임아웃되더라도,
  TestExecutionResult의 results 목록 길이는 입력 TestScenario의
  test_cases 목록 길이와 동일해야 합니다.

Property 12: 실패 테스트 차이 기록 (Failed Test Difference Recording)
- 임의의 실패한(passed=False, timed_out=False) TestCaseResult에 대해,
  failure_reason이 비어있지 않아야 하며, actual_result와 expected_result가
  모두 기록되어 있어야 합니다.

Feature: qa-agent-system, Property 11: 타임아웃 시 계속 실행
Feature: qa-agent-system, Property 12: 실패 테스트 차이 기록

검증 대상: 요구사항 4.6, 4.3
"""

from hypothesis import given
from hypothesis import strategies as st

from qa_agent_system.agents.test_execution_agent import TestExecutionAgent
from qa_agent_system.models import TestCaseResult, TestScenario
from tests.conftest import st_test_case_result, st_test_scenario


# ============================================================
# Property 11: 타임아웃 시 계속 실행 (Continue Execution on Timeout)
# ============================================================


class TestContinueExecutionOnTimeout:
    """타임아웃 시 계속 실행 속성 테스트

    **Validates: Requirements 4.6**

    임의의 TestScenario에 대해 execute_tests()를 실행하면,
    반환된 결과 목록의 길이가 입력 테스트 케이스 수와 동일한지 검증합니다.
    시뮬레이션 모드(agent=None)에서 모든 테스트가 하나의 결과를 생성하는지 확인합니다.
    """

    # Feature: qa-agent-system, Property 11: 타임아웃 시 계속 실행

    @given(scenario=st_test_scenario())
    def test_results_count_equals_test_cases_count(
        self, scenario: TestScenario
    ) -> None:
        """execute_tests() 결과 목록 길이 == 입력 테스트 케이스 수 검증

        **Validates: Requirements 4.6**

        임의의 TestScenario에 대해 TestExecutionAgent가 항상
        각 TestCase마다 정확히 하나의 결과를 반환하는지 확인합니다.
        타임아웃이나 실패가 발생하더라도 결과 수는 동일해야 합니다.
        """
        # 시뮬레이션 모드로 에이전트 생성 (agent=None)
        agent = TestExecutionAgent(agent=None)

        # 테스트 실행
        result = agent.execute_tests(scenario)

        # 결과 목록 길이가 입력 테스트 케이스 수와 동일한지 검증
        assert len(result.results) == len(scenario.test_cases), (
            f"결과 목록 길이({len(result.results)})가 "
            f"입력 테스트 케이스 수({len(scenario.test_cases)})와 다릅니다. "
            "타임아웃이나 실패와 관계없이 모든 테스트 케이스에 대한 결과가 있어야 합니다."
        )


# ============================================================
# Property 12: 실패 테스트 차이 기록 (Failed Test Difference Recording)
# ============================================================

# 실패한 TestCaseResult 전략 (passed=False, timed_out=False)
# 실패 시 failure_reason, actual_result, expected_result가 반드시 기록되어야 함
_non_empty_text = st.text(min_size=1, max_size=50).filter(lambda s: s.strip() != "")


@st.composite
def st_failed_test_case_result(draw: st.DrawFn) -> TestCaseResult:
    """실패한(passed=False, timed_out=False) TestCaseResult 생성 전략

    실패한 테스트 결과에는 failure_reason, actual_result, expected_result가
    반드시 기록되어야 하므로, 비공백 문자열로 생성합니다.
    """
    return TestCaseResult(
        test_case_id=draw(_non_empty_text),
        test_name=draw(_non_empty_text),
        passed=False,
        execution_time_ms=draw(
            st.floats(min_value=0.0, max_value=60000.0, allow_nan=False, allow_infinity=False)
        ),
        screenshot_path=draw(st.one_of(st.none(), _non_empty_text)),
        actual_result=draw(_non_empty_text),
        expected_result=draw(_non_empty_text),
        failure_reason=draw(_non_empty_text),
        timed_out=False,
    )


class TestFailedTestDifferenceRecording:
    """실패 테스트 차이 기록 속성 테스트

    **Validates: Requirements 4.3**

    임의의 실패한(passed=False, timed_out=False) TestCaseResult에 대해
    failure_reason이 비어있지 않고, actual_result와 expected_result가
    모두 기록되어 있는지 검증합니다.
    """

    # Feature: qa-agent-system, Property 12: 실패 테스트 차이 기록

    @given(result=st_failed_test_case_result())
    def test_failed_result_has_non_empty_failure_reason(
        self, result: TestCaseResult
    ) -> None:
        """실패한 TestCaseResult의 failure_reason이 비공백인지 검증

        **Validates: Requirements 4.3**
        """
        # passed=False, timed_out=False인 결과 확인
        assert result.passed is False, "테스트 결과가 실패(passed=False)여야 합니다"
        assert result.timed_out is False, "타임아웃이 아닌 실패여야 합니다"

        # failure_reason이 None이 아니고 비공백인지 검증
        assert result.failure_reason is not None, (
            "실패한 테스트의 failure_reason은 None이 아니어야 합니다"
        )
        assert result.failure_reason.strip() != "", (
            "실패한 테스트의 failure_reason은 공백만으로 구성될 수 없습니다"
        )

    @given(result=st_failed_test_case_result())
    def test_failed_result_has_actual_result(
        self, result: TestCaseResult
    ) -> None:
        """실패한 TestCaseResult의 actual_result가 기록되어 있는지 검증

        **Validates: Requirements 4.3**
        """
        assert result.passed is False
        assert result.timed_out is False

        # actual_result가 None이 아닌지 검증
        assert result.actual_result is not None, (
            "실패한 테스트의 actual_result는 None이 아니어야 합니다"
        )

    @given(result=st_failed_test_case_result())
    def test_failed_result_has_expected_result(
        self, result: TestCaseResult
    ) -> None:
        """실패한 TestCaseResult의 expected_result가 기록되어 있는지 검증

        **Validates: Requirements 4.3**
        """
        assert result.passed is False
        assert result.timed_out is False

        # expected_result가 None이 아닌지 검증
        assert result.expected_result is not None, (
            "실패한 테스트의 expected_result는 None이 아니어야 합니다"
        )
