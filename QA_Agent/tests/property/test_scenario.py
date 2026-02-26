"""Property 10: 데이터 모델 필수 필드 비공백 (Data Model Required Fields Non-Empty)

임의의 TestCase에 대해 id, name, steps, expected_result가 비어있지 않아야 하며,
임의의 TestCaseResult에 대해 test_case_id, test_name이 비어있지 않아야 합니다.

Feature: qa-agent-system, Property 10: 데이터 모델 필수 필드 비공백

검증 대상: 요구사항 3.2, 4.2, 1.3
"""

import pytest
from hypothesis import given
from pydantic import ValidationError

from qa_agent_system.models import TestCase, TestCaseResult
from tests.conftest import st_test_case, st_test_case_result


class TestDataModelRequiredFieldsNonEmpty:
    """데이터 모델 필수 필드 비공백 속성 테스트

    **Validates: Requirements 3.2, 4.2, 1.3**

    Hypothesis로 임의의 TestCase, TestCaseResult를 생성하여
    필수 필드가 비어있지 않은지 검증합니다.
    """

    # ============================================================
    # TestCase 필수 필드 비공백 검증
    # 요구사항 3.2: id, name, steps, expected_result 필수 필드 비공백
    # ============================================================

    @given(test_case=st_test_case())
    def test_test_case_id_non_empty(self, test_case: TestCase) -> None:
        """TestCase의 id 필드가 비어있지 않은지 검증

        **Validates: Requirements 3.2**
        """
        assert len(test_case.id) > 0, "TestCase.id는 비공백이어야 합니다"
        assert test_case.id.strip() != "", "TestCase.id는 공백만으로 구성될 수 없습니다"

    @given(test_case=st_test_case())
    def test_test_case_name_non_empty(self, test_case: TestCase) -> None:
        """TestCase의 name 필드가 비어있지 않은지 검증

        **Validates: Requirements 3.2**
        """
        assert len(test_case.name) > 0, "TestCase.name은 비공백이어야 합니다"
        assert test_case.name.strip() != "", "TestCase.name은 공백만으로 구성될 수 없습니다"

    @given(test_case=st_test_case())
    def test_test_case_steps_non_empty(self, test_case: TestCase) -> None:
        """TestCase의 steps 필드가 비어있지 않은지 검증 (최소 1개 이상)

        **Validates: Requirements 3.2**
        """
        assert len(test_case.steps) > 0, "TestCase.steps는 최소 1개 이상이어야 합니다"

    @given(test_case=st_test_case())
    def test_test_case_expected_result_non_empty(self, test_case: TestCase) -> None:
        """TestCase의 expected_result 필드가 비어있지 않은지 검증

        **Validates: Requirements 3.2**
        """
        assert len(test_case.expected_result) > 0, "TestCase.expected_result는 비공백이어야 합니다"
        assert test_case.expected_result.strip() != "", "TestCase.expected_result는 공백만으로 구성될 수 없습니다"

    # ============================================================
    # TestCaseResult 필수 필드 비공백 검증
    # 요구사항 4.2: test_case_id, test_name 필수 필드 비공백
    # ============================================================

    @given(result=st_test_case_result())
    def test_test_case_result_id_non_empty(self, result: TestCaseResult) -> None:
        """TestCaseResult의 test_case_id 필드가 비어있지 않은지 검증

        **Validates: Requirements 4.2**
        """
        assert len(result.test_case_id) > 0, "TestCaseResult.test_case_id는 비공백이어야 합니다"
        assert result.test_case_id.strip() != "", "TestCaseResult.test_case_id는 공백만으로 구성될 수 없습니다"

    @given(result=st_test_case_result())
    def test_test_case_result_name_non_empty(self, result: TestCaseResult) -> None:
        """TestCaseResult의 test_name 필드가 비어있지 않은지 검증

        **Validates: Requirements 4.2**
        """
        assert len(result.test_name) > 0, "TestCaseResult.test_name은 비공백이어야 합니다"
        assert result.test_name.strip() != "", "TestCaseResult.test_name은 공백만으로 구성될 수 없습니다"

    # ============================================================
    # Pydantic 검증: 빈 문자열/빈 리스트 거부 확인
    # 모델 수준에서 빈 값이 거부되는지 확인하는 보조 테스트
    # ============================================================

    def test_test_case_rejects_empty_id(self) -> None:
        """TestCase 생성 시 빈 id를 거부하는지 확인"""
        with pytest.raises(ValidationError):
            TestCase(
                id="",
                name="테스트",
                preconditions=[],
                steps=[{"step_number": 1, "action": "클릭", "expected_result": "성공"}],
                expected_result="성공",
                scenario_type="positive",
            )

    def test_test_case_rejects_empty_name(self) -> None:
        """TestCase 생성 시 빈 name을 거부하는지 확인"""
        with pytest.raises(ValidationError):
            TestCase(
                id="TC-001",
                name="",
                preconditions=[],
                steps=[{"step_number": 1, "action": "클릭", "expected_result": "성공"}],
                expected_result="성공",
                scenario_type="positive",
            )

    def test_test_case_rejects_empty_steps(self) -> None:
        """TestCase 생성 시 빈 steps 리스트를 거부하는지 확인"""
        with pytest.raises(ValidationError):
            TestCase(
                id="TC-001",
                name="테스트",
                preconditions=[],
                steps=[],
                expected_result="성공",
                scenario_type="positive",
            )

    def test_test_case_rejects_empty_expected_result(self) -> None:
        """TestCase 생성 시 빈 expected_result를 거부하는지 확인"""
        with pytest.raises(ValidationError):
            TestCase(
                id="TC-001",
                name="테스트",
                preconditions=[],
                steps=[{"step_number": 1, "action": "클릭", "expected_result": "성공"}],
                expected_result="",
                scenario_type="positive",
            )

    def test_test_case_result_rejects_empty_id(self) -> None:
        """TestCaseResult 생성 시 빈 test_case_id를 거부하는지 확인"""
        with pytest.raises(ValidationError):
            TestCaseResult(
                test_case_id="",
                test_name="테스트",
                passed=True,
                execution_time_ms=100.0,
            )

    def test_test_case_result_rejects_empty_name(self) -> None:
        """TestCaseResult 생성 시 빈 test_name을 거부하는지 확인"""
        with pytest.raises(ValidationError):
            TestCaseResult(
                test_case_id="TC-001",
                test_name="",
                passed=True,
                execution_time_ms=100.0,
            )


# ============================================================
# Feature: qa-agent-system, Property 9: 테스트 시나리오 양면성
# ============================================================

"""Property 9: 테스트 시나리오 양면성 (Test Scenario Dual Coverage)

임의의 생성된 TestScenario에 대해, test_cases 목록에는
scenario_type이 "positive"인 테스트 케이스와 "negative"인 테스트 케이스가
각각 최소 1개 이상 포함되어야 합니다.

검증 대상: 요구사항 3.3
"""

from hypothesis import strategies as st

from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
from qa_agent_system.models import TestScenario

# 충분한 요구사항 문자열 전략 (최소 10자 이상)
_sufficient_requirements = st.text(min_size=10, max_size=100).filter(
    lambda s: len(s.strip()) >= 10
)


class TestScenarioDualCoverage:
    """테스트 시나리오 양면성 속성 테스트

    **Validates: Requirements 3.3**

    TCScenarioAgent가 생성하는 모든 TestScenario에 대해
    긍정(positive)과 부정(negative) 시나리오가 각각 최소 1개 이상
    포함되는지 검증합니다.
    """

    # Feature: qa-agent-system, Property 9: 테스트 시나리오 양면성

    @given(
        target_url=st.from_regex(r"https?://[a-z]{1,10}\.[a-z]{2,4}", fullmatch=True),
        requirements=_sufficient_requirements,
    )
    def test_scenario_contains_positive_case(
        self, target_url: str, requirements: str
    ) -> None:
        """생성된 TestScenario에 긍정(positive) 시나리오가 최소 1개 포함되는지 검증

        **Validates: Requirements 3.3**
        """
        # LLM 없이 기본 시나리오 생성 (agent=None)
        agent = TCScenarioAgent(agent=None)
        result = agent.generate_scenario(target_url, requirements)

        # 충분한 요구사항이므로 TestScenario가 반환되어야 함
        assert isinstance(result, TestScenario), (
            f"충분한 요구사항에 대해 TestScenario가 반환되어야 합니다. "
            f"실제 반환: {type(result)}"
        )

        # 긍정 시나리오 최소 1개 포함 확인
        positive_cases = [
            tc for tc in result.test_cases if tc.scenario_type == "positive"
        ]
        assert len(positive_cases) >= 1, (
            "TestScenario에 긍정(positive) 시나리오가 최소 1개 포함되어야 합니다. "
            f"현재 positive 개수: {len(positive_cases)}"
        )

    @given(
        target_url=st.from_regex(r"https?://[a-z]{1,10}\.[a-z]{2,4}", fullmatch=True),
        requirements=_sufficient_requirements,
    )
    def test_scenario_contains_negative_case(
        self, target_url: str, requirements: str
    ) -> None:
        """생성된 TestScenario에 부정(negative) 시나리오가 최소 1개 포함되는지 검증

        **Validates: Requirements 3.3**
        """
        # LLM 없이 기본 시나리오 생성 (agent=None)
        agent = TCScenarioAgent(agent=None)
        result = agent.generate_scenario(target_url, requirements)

        # 충분한 요구사항이므로 TestScenario가 반환되어야 함
        assert isinstance(result, TestScenario), (
            f"충분한 요구사항에 대해 TestScenario가 반환되어야 합니다. "
            f"실제 반환: {type(result)}"
        )

        # 부정 시나리오 최소 1개 포함 확인
        negative_cases = [
            tc for tc in result.test_cases if tc.scenario_type == "negative"
        ]
        assert len(negative_cases) >= 1, (
            "TestScenario에 부정(negative) 시나리오가 최소 1개 포함되어야 합니다. "
            f"현재 negative 개수: {len(negative_cases)}"
        )

    @given(
        target_url=st.from_regex(r"https?://[a-z]{1,10}\.[a-z]{2,4}", fullmatch=True),
        requirements=_sufficient_requirements,
    )
    def test_scenario_dual_coverage_combined(
        self, target_url: str, requirements: str
    ) -> None:
        """생성된 TestScenario에 긍정/부정 시나리오가 모두 포함되는지 통합 검증

        **Validates: Requirements 3.3**
        """
        # LLM 없이 기본 시나리오 생성 (agent=None)
        agent = TCScenarioAgent(agent=None)
        result = agent.generate_scenario(target_url, requirements)

        assert isinstance(result, TestScenario)

        # 시나리오 유형별 분류
        scenario_types = {tc.scenario_type for tc in result.test_cases}

        # 긍정과 부정 시나리오 모두 포함 확인
        assert "positive" in scenario_types, (
            "TestScenario에 긍정(positive) 시나리오가 포함되어야 합니다"
        )
        assert "negative" in scenario_types, (
            "TestScenario에 부정(negative) 시나리오가 포함되어야 합니다"
        )
