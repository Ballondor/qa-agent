"""Property 7: 스키마 검증 정확성 (Schema Validation Correctness)

임의의 JSON 데이터에 대해, 유효한 데이터는 스키마 검증을 통과하고,
필수 필드가 누락되거나 타입이 잘못된 데이터는 검증에 실패해야 합니다.
검증 실패 시 ValidationResult의 errors에 실패 항목과 원인이 포함되어야 합니다.

# Feature: qa-agent-system, Property 7: 스키마 검증 정확성

검증 대상: 요구사항 6.2, 6.3, 2.7
"""

from hypothesis import given, assume
from hypothesis import strategies as st

from qa_agent_system.models import (
    TestCase,
    TestCaseResult,
    TestScenario,
    TestExecutionResult,
)
from qa_agent_system.validator import DataValidator
from tests.conftest import (
    st_test_case,
    st_test_case_result,
    st_test_scenario,
    st_test_execution_result,
)


class TestSchemaValidationCorrectness:
    """스키마 검증 정확성 속성 테스트

    **Validates: Requirements 6.2, 6.3, 2.7**

    유효한 데이터는 검증을 통과하고, 무효한 데이터는 검증에 실패하며
    실패 시 errors에 상세 정보가 포함되는지 검증합니다.
    """

    # ============================================================
    # 유효한 데이터 → 검증 통과 (is_valid=True, errors=[])
    # ============================================================

    @given(test_case=st_test_case())
    def test_valid_test_case_passes_validation(self, test_case: TestCase) -> None:
        """유효한 TestCase 데이터는 스키마 검증을 통과해야 합니다.

        **Validates: Requirements 6.2**
        """
        # 유효한 모델을 dict로 변환하여 검증
        data = test_case.model_dump(mode="json")
        result = DataValidator.validate(data, TestCase)

        # 유효한 데이터이므로 검증 통과
        assert result.is_valid is True
        assert result.errors == []

    @given(test_case_result=st_test_case_result())
    def test_valid_test_case_result_passes_validation(
        self, test_case_result: TestCaseResult
    ) -> None:
        """유효한 TestCaseResult 데이터는 스키마 검증을 통과해야 합니다.

        **Validates: Requirements 6.2**
        """
        data = test_case_result.model_dump(mode="json")
        result = DataValidator.validate(data, TestCaseResult)

        assert result.is_valid is True
        assert result.errors == []

    @given(scenario=st_test_scenario())
    def test_valid_test_scenario_passes_validation(
        self, scenario: TestScenario
    ) -> None:
        """유효한 TestScenario 데이터는 스키마 검증을 통과해야 합니다.

        **Validates: Requirements 6.2**
        """
        data = scenario.model_dump(mode="json")
        result = DataValidator.validate(data, TestScenario)

        assert result.is_valid is True
        assert result.errors == []

    @given(execution_result=st_test_execution_result())
    def test_valid_execution_result_passes_validation(
        self, execution_result: TestExecutionResult
    ) -> None:
        """유효한 TestExecutionResult 데이터는 스키마 검증을 통과해야 합니다.

        **Validates: Requirements 6.2**
        """
        data = execution_result.model_dump(mode="json")
        result = DataValidator.validate(data, TestExecutionResult)

        assert result.is_valid is True
        assert result.errors == []

    # ============================================================
    # 필수 필드 누락 → 검증 실패 (is_valid=False, errors 비공백)
    # ============================================================

    @given(test_case=st_test_case(), field_to_remove=st.sampled_from(
        ["id", "name", "steps", "expected_result", "scenario_type"]
    ))
    def test_missing_required_field_fails_validation(
        self, test_case: TestCase, field_to_remove: str
    ) -> None:
        """필수 필드가 누락된 데이터는 스키마 검증에 실패해야 합니다.

        **Validates: Requirements 6.3**
        """
        # 유효한 데이터에서 필수 필드 하나를 제거
        data = test_case.model_dump(mode="json")
        del data[field_to_remove]

        result = DataValidator.validate(data, TestCase)

        # 필수 필드 누락이므로 검증 실패
        assert result.is_valid is False
        # errors에 실패 항목과 원인이 포함되어야 함
        assert len(result.errors) > 0

    @given(test_case_result=st_test_case_result(), field_to_remove=st.sampled_from(
        ["test_case_id", "test_name", "passed", "execution_time_ms"]
    ))
    def test_missing_required_result_field_fails_validation(
        self, test_case_result: TestCaseResult, field_to_remove: str
    ) -> None:
        """TestCaseResult에서 필수 필드가 누락되면 검증에 실패해야 합니다.

        **Validates: Requirements 6.3**
        """
        data = test_case_result.model_dump(mode="json")
        del data[field_to_remove]

        result = DataValidator.validate(data, TestCaseResult)

        assert result.is_valid is False
        assert len(result.errors) > 0

    # ============================================================
    # 잘못된 타입 → 검증 실패 (is_valid=False, errors 비공백)
    # ============================================================

    @given(test_case=st_test_case())
    def test_wrong_type_field_fails_validation(self, test_case: TestCase) -> None:
        """필드 타입이 잘못된 데이터는 스키마 검증에 실패해야 합니다.

        **Validates: Requirements 6.3, 2.7**
        """
        data = test_case.model_dump(mode="json")
        # steps 필드를 리스트가 아닌 문자열로 변경
        data["steps"] = "잘못된 타입"

        result = DataValidator.validate(data, TestCase)

        assert result.is_valid is False
        assert len(result.errors) > 0

    @given(execution_result=st_test_execution_result())
    def test_wrong_type_execution_time_fails_validation(
        self, execution_result: TestExecutionResult
    ) -> None:
        """실행 시간 필드에 잘못된 타입이 들어가면 검증에 실패해야 합니다.

        **Validates: Requirements 6.3, 2.7**
        """
        data = execution_result.model_dump(mode="json")
        # total_execution_time_ms를 문자열로 변경
        data["total_execution_time_ms"] = "잘못된 타입"

        result = DataValidator.validate(data, TestExecutionResult)

        assert result.is_valid is False
        assert len(result.errors) > 0

    # ============================================================
    # 검증 실패 시 errors에 실패 항목과 원인 포함 확인
    # ============================================================

    @given(test_case=st_test_case(), field_to_remove=st.sampled_from(
        ["id", "name", "steps", "expected_result", "scenario_type"]
    ))
    def test_validation_errors_contain_failure_details(
        self, test_case: TestCase, field_to_remove: str
    ) -> None:
        """검증 실패 시 errors 목록에 실패 항목과 원인이 포함되어야 합니다.

        **Validates: Requirements 6.3**
        """
        data = test_case.model_dump(mode="json")
        del data[field_to_remove]

        result = DataValidator.validate(data, TestCase)

        assert result.is_valid is False
        # 각 에러 메시지에 필드 정보가 포함되어야 함
        assert any(field_to_remove in error for error in result.errors)


# ============================================================
# Property 8: 에러 응답 필수 정보 포함 (Error Response Required Information)
# Feature: qa-agent-system, Property 8: 에러 응답 필수 정보 포함
#
# 임의의 에이전트 실패 시나리오에 대해, 에러 응답에는 반드시
# 실패한 에이전트 이름과 오류 원인이 포함되어야 합니다.
# 오케스트레이터의 에러 전달 시에는 추가로 실패 단계 정보가 포함되어야 합니다.
#
# 검증 대상: 요구사항 1.4, 2.6
# ============================================================

from qa_agent_system.errors import (
    QAAgentError,
    AgentInitError,
    ModelConnectionError,
    PipelineError,
    PlaywrightConnectionError,
)

# 에이전트 이름 전략 (비공백 문자열)
agent_name_strategy = st.text(min_size=1, max_size=30).filter(lambda s: s.strip() != "")
# 오류 원인 전략 (비공백 문자열)
cause_strategy = st.text(min_size=1, max_size=100).filter(lambda s: s.strip() != "")
# 실패 단계 전략 (비공백 문자열)
failed_step_strategy = st.text(min_size=1, max_size=50).filter(lambda s: s.strip() != "")


class TestErrorResponseRequiredInformation:
    """에러 응답 필수 정보 포함 속성 테스트

    **Validates: Requirements 1.4, 2.6**

    모든 에러 타입에 에이전트 이름과 오류 원인이 포함되는지,
    PipelineError에 실패 단계 정보가 포함되는지 검증합니다.
    """

    # ============================================================
    # 모든 에러 타입에 agent_name 포함 검증
    # ============================================================

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_agent_init_error_contains_agent_name(
        self, agent_name: str, cause: str
    ) -> None:
        """AgentInitError에 에이전트 이름이 포함되어야 합니다.

        **Validates: Requirements 1.4**
        """
        error = AgentInitError(agent_name=agent_name, cause=cause)

        # agent_name 속성이 비공백이어야 함
        assert error.agent_name == agent_name
        assert len(error.agent_name.strip()) > 0
        # 에러 메시지에 에이전트 이름이 포함되어야 함
        assert agent_name in str(error)

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_model_connection_error_contains_agent_name(
        self, agent_name: str, cause: str
    ) -> None:
        """ModelConnectionError에 에이전트 이름이 포함되어야 합니다.

        **Validates: Requirements 1.4**
        """
        error = ModelConnectionError(agent_name=agent_name, cause=cause)

        assert error.agent_name == agent_name
        assert len(error.agent_name.strip()) > 0
        assert agent_name in str(error)

    @given(
        agent_name=agent_name_strategy,
        failed_step=failed_step_strategy,
        cause=cause_strategy,
    )
    def test_pipeline_error_contains_agent_name(
        self, agent_name: str, failed_step: str, cause: str
    ) -> None:
        """PipelineError에 에이전트 이름이 포함되어야 합니다.

        **Validates: Requirements 2.6**
        """
        error = PipelineError(
            agent_name=agent_name, failed_step=failed_step, cause=cause
        )

        assert error.agent_name == agent_name
        assert len(error.agent_name.strip()) > 0
        assert agent_name in str(error)

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_playwright_connection_error_contains_agent_name(
        self, agent_name: str, cause: str
    ) -> None:
        """PlaywrightConnectionError에 에이전트 이름이 포함되어야 합니다.

        **Validates: Requirements 1.4**
        """
        error = PlaywrightConnectionError(agent_name=agent_name, cause=cause)

        assert error.agent_name == agent_name
        assert len(error.agent_name.strip()) > 0
        assert agent_name in str(error)

    # ============================================================
    # 모든 에러 타입에 cause 포함 검증
    # ============================================================

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_agent_init_error_contains_cause(
        self, agent_name: str, cause: str
    ) -> None:
        """AgentInitError 메시지에 오류 원인이 포함되어야 합니다.

        **Validates: Requirements 1.4**
        """
        error = AgentInitError(agent_name=agent_name, cause=cause)

        assert error.cause == cause
        assert len(error.cause.strip()) > 0
        # 에러 메시지에 원인이 포함되어야 함
        assert cause in str(error)

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_model_connection_error_contains_cause(
        self, agent_name: str, cause: str
    ) -> None:
        """ModelConnectionError 메시지에 오류 원인이 포함되어야 합니다.

        **Validates: Requirements 1.4**
        """
        error = ModelConnectionError(agent_name=agent_name, cause=cause)

        assert error.cause == cause
        assert len(error.cause.strip()) > 0
        assert cause in str(error)

    @given(
        agent_name=agent_name_strategy,
        failed_step=failed_step_strategy,
        cause=cause_strategy,
    )
    def test_pipeline_error_contains_cause(
        self, agent_name: str, failed_step: str, cause: str
    ) -> None:
        """PipelineError 메시지에 오류 원인이 포함되어야 합니다.

        **Validates: Requirements 2.6**
        """
        error = PipelineError(
            agent_name=agent_name, failed_step=failed_step, cause=cause
        )

        assert error.cause == cause
        assert len(error.cause.strip()) > 0
        assert cause in str(error)

    # ============================================================
    # PipelineError에 failed_step 포함 검증 (요구사항 2.6)
    # ============================================================

    @given(
        agent_name=agent_name_strategy,
        failed_step=failed_step_strategy,
        cause=cause_strategy,
    )
    def test_pipeline_error_contains_failed_step(
        self, agent_name: str, failed_step: str, cause: str
    ) -> None:
        """PipelineError 메시지에 실패 단계 정보가 포함되어야 합니다.

        **Validates: Requirements 2.6**
        """
        error = PipelineError(
            agent_name=agent_name, failed_step=failed_step, cause=cause
        )

        # failed_step 속성이 올바르게 설정되어야 함
        assert error.failed_step == failed_step
        assert len(error.failed_step.strip()) > 0
        # 에러 메시지에 실패 단계가 포함되어야 함
        assert failed_step in str(error)

    # ============================================================
    # ModelConnectionError에 retry_guidance 포함 검증 (요구사항 1.5)
    # ============================================================

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_model_connection_error_contains_retry_guidance(
        self, agent_name: str, cause: str
    ) -> None:
        """ModelConnectionError에 재시도 안내가 포함되어야 합니다.

        **Validates: Requirements 1.4**
        """
        error = ModelConnectionError(agent_name=agent_name, cause=cause)

        # retry_guidance 속성이 존재하고 비공백이어야 함
        assert hasattr(error, "retry_guidance")
        assert len(error.retry_guidance.strip()) > 0
        # 에러 메시지에 재시도 안내가 포함되어야 함
        assert error.retry_guidance in str(error)

    # ============================================================
    # 모든 에러가 QAAgentError로 잡힐 수 있는지 검증
    # ============================================================

    @given(agent_name=agent_name_strategy, cause=cause_strategy)
    def test_all_errors_catchable_as_qa_agent_error(
        self, agent_name: str, cause: str
    ) -> None:
        """모든 에러 타입이 QAAgentError로 잡힐 수 있어야 합니다.

        **Validates: Requirements 1.4, 2.6**
        """
        # 각 에러 타입이 QAAgentError의 하위 클래스인지 검증
        errors = [
            AgentInitError(agent_name=agent_name, cause=cause),
            ModelConnectionError(agent_name=agent_name, cause=cause),
            PipelineError(
                agent_name=agent_name, failed_step="test_step", cause=cause
            ),
            PlaywrightConnectionError(agent_name=agent_name, cause=cause),
        ]

        for error in errors:
            # isinstance로 QAAgentError 타입 확인
            assert isinstance(error, QAAgentError)
            # try/except로 QAAgentError로 잡을 수 있는지 확인
            try:
                raise error
            except QAAgentError as caught:
                assert caught.agent_name == agent_name
                assert caught.cause == cause
