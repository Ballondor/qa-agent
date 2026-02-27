"""
파이프라인 속성 기반 테스트 (Pipeline Property-Based Tests)

Property 5: 에이전트 상태 전이 순서 (Agent Status Transition Order)
Property 6: 파이프라인 실행 순서 (Pipeline Execution Order)

Feature: qa-agent-system
"""

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from qa_agent_system.models import (
    AgentStatusEnum,
    TestCaseResult,
    TestExecutionResult,
    TestReport,
    TestScenario,
    TestSummary,
)
from qa_agent_system.agents.orchestrator_agent import OrchestratorAgent
from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
from qa_agent_system.agents.test_execution_agent import TestExecutionAgent
from qa_agent_system.agents.report_agent import ReportAgent
from qa_agent_system.errors import PipelineError

from tests.conftest import (
    st_test_scenario,
    st_test_execution_result,
    st_test_report,
    non_empty_text,
    url_strategy,
)


# ============================================================
# 유효한 상태 전이 정의
# IDLE → RUNNING → COMPLETED 또는 IDLE → RUNNING → FAILED
# ============================================================

_VALID_TRANSITIONS = {
    AgentStatusEnum.IDLE: {AgentStatusEnum.RUNNING},
    AgentStatusEnum.RUNNING: {AgentStatusEnum.COMPLETED, AgentStatusEnum.FAILED},
    AgentStatusEnum.COMPLETED: set(),  # 종료 상태
    AgentStatusEnum.FAILED: set(),  # 종료 상태
}


def _is_valid_transition(from_status: AgentStatusEnum, to_status: AgentStatusEnum) -> bool:
    """상태 전이가 유효한지 확인합니다."""
    return to_status in _VALID_TRANSITIONS.get(from_status, set())


# ============================================================
# Property 5: 에이전트 상태 전이 순서
# Feature: qa-agent-system, Property 5: 에이전트 상태 전이 순서
# ============================================================


# 상태 전이 시퀀스 전략: 유효한 전이만 생성
@st.composite
def st_valid_status_sequence(draw: st.DrawFn) -> list[AgentStatusEnum]:
    """유효한 상태 전이 시퀀스를 생성합니다.
    IDLE → RUNNING → COMPLETED 또는 IDLE → RUNNING → FAILED
    """
    # 항상 IDLE에서 시작
    sequence = [AgentStatusEnum.IDLE, AgentStatusEnum.RUNNING]
    # 최종 상태: COMPLETED 또는 FAILED
    final = draw(st.sampled_from([AgentStatusEnum.COMPLETED, AgentStatusEnum.FAILED]))
    sequence.append(final)
    return sequence


@st.composite
def st_invalid_status_sequence(draw: st.DrawFn) -> list[AgentStatusEnum]:
    """무효한 상태 전이를 포함하는 시퀀스를 생성합니다."""
    # 무효한 전이 패턴들
    invalid_patterns = [
        # IDLE에서 바로 COMPLETED/FAILED로 전이
        [AgentStatusEnum.IDLE, AgentStatusEnum.COMPLETED],
        [AgentStatusEnum.IDLE, AgentStatusEnum.FAILED],
        # COMPLETED에서 다시 전이
        [AgentStatusEnum.IDLE, AgentStatusEnum.RUNNING, AgentStatusEnum.COMPLETED, AgentStatusEnum.RUNNING],
        # FAILED에서 다시 전이
        [AgentStatusEnum.IDLE, AgentStatusEnum.RUNNING, AgentStatusEnum.FAILED, AgentStatusEnum.RUNNING],
        # RUNNING에서 IDLE로 역전이
        [AgentStatusEnum.IDLE, AgentStatusEnum.RUNNING, AgentStatusEnum.IDLE],
    ]
    return draw(st.sampled_from(invalid_patterns))


@given(sequence=st_valid_status_sequence())
def test_property5_valid_status_transitions(sequence: list[AgentStatusEnum]):
    """Property 5: 유효한 상태 전이 시퀀스는 모든 전이가 유효해야 합니다.

    Feature: qa-agent-system, Property 5: 에이전트 상태 전이 순서
    검증 대상: 요구사항 2.5
    """
    for i in range(len(sequence) - 1):
        assert _is_valid_transition(sequence[i], sequence[i + 1]), (
            f"유효하지 않은 상태 전이: {sequence[i].value} → {sequence[i + 1].value}"
        )


@given(sequence=st_invalid_status_sequence())
def test_property5_invalid_status_transitions_detected(sequence: list[AgentStatusEnum]):
    """Property 5: 무효한 상태 전이 시퀀스에는 최소 하나의 무효 전이가 있어야 합니다.

    Feature: qa-agent-system, Property 5: 에이전트 상태 전이 순서
    검증 대상: 요구사항 2.5
    """
    has_invalid = False
    for i in range(len(sequence) - 1):
        if not _is_valid_transition(sequence[i], sequence[i + 1]):
            has_invalid = True
            break
    assert has_invalid, "무효한 시퀀스에 무효 전이가 감지되지 않았습니다"


@given(scenario=st_test_scenario(), execution_result=st_test_execution_result())
def test_property5_orchestrator_status_transitions_on_success(
    scenario: TestScenario, execution_result: TestExecutionResult
):
    """Property 5: 성공적인 파이프라인 실행 시 모든 에이전트가
    IDLE → RUNNING → COMPLETED 순서로 전이해야 합니다.

    Feature: qa-agent-system, Property 5: 에이전트 상태 전이 순서
    검증 대상: 요구사항 2.5
    """
    # 모킹된 에이전트 생성
    tc_agent = TCScenarioAgent(agent=None)
    exec_agent = TestExecutionAgent(agent=None)
    report_agent = ReportAgent(agent=None)

    orchestrator = OrchestratorAgent(tc_agent, exec_agent, report_agent)

    # TC 에이전트가 시나리오를 반환하도록 모킹
    tc_agent.generate_scenario = MagicMock(return_value=scenario)
    # 실행 에이전트가 결과를 반환하도록 모킹
    exec_agent.execute_tests = MagicMock(return_value=execution_result)

    # 파이프라인 실행
    orchestrator.execute_pipeline(scenario.target_url, scenario.requirements)

    # 모든 에이전트가 COMPLETED 상태여야 함
    for agent_name in ["TCScenarioAgent", "TestExecutionAgent", "ReportAgent"]:
        status = orchestrator.get_agent_status(agent_name)
        assert status.status == AgentStatusEnum.COMPLETED, (
            f"{agent_name}의 상태가 COMPLETED가 아닙니다: {status.status.value}"
        )


@given(scenario=st_test_scenario())
def test_property5_orchestrator_status_on_failure(scenario: TestScenario):
    """Property 5: 에이전트 실패 시 해당 에이전트가 FAILED 상태로 전이해야 합니다.

    Feature: qa-agent-system, Property 5: 에이전트 상태 전이 순서
    검증 대상: 요구사항 2.5
    """
    tc_agent = TCScenarioAgent(agent=None)
    exec_agent = TestExecutionAgent(agent=None)
    report_agent = ReportAgent(agent=None)

    orchestrator = OrchestratorAgent(tc_agent, exec_agent, report_agent)

    # TC 에이전트가 시나리오를 반환하도록 모킹
    tc_agent.generate_scenario = MagicMock(return_value=scenario)
    # 실행 에이전트가 예외를 발생시키도록 모킹
    exec_agent.execute_tests = MagicMock(side_effect=RuntimeError("테스트 실행 실패"))

    with pytest.raises(PipelineError):
        orchestrator.execute_pipeline(scenario.target_url, scenario.requirements)

    # TC 에이전트는 COMPLETED, 실행 에이전트는 FAILED
    tc_status = orchestrator.get_agent_status("TCScenarioAgent")
    exec_status = orchestrator.get_agent_status("TestExecutionAgent")
    assert tc_status.status == AgentStatusEnum.COMPLETED
    assert exec_status.status == AgentStatusEnum.FAILED
    assert exec_status.error_message is not None


# ============================================================
# Property 6: 파이프라인 실행 순서
# Feature: qa-agent-system, Property 6: 파이프라인 실행 순서
# ============================================================


@given(scenario=st_test_scenario(), execution_result=st_test_execution_result())
def test_property6_pipeline_execution_order(
    scenario: TestScenario, execution_result: TestExecutionResult
):
    """Property 6: 파이프라인은 반드시 TC → Execution → Report 순서로 실행되어야 합니다.

    Feature: qa-agent-system, Property 6: 파이프라인 실행 순서
    검증 대상: 요구사항 2.1, 2.2, 2.3, 2.4
    """
    # 호출 순서를 기록할 리스트
    call_order: list[str] = []

    tc_agent = TCScenarioAgent(agent=None)
    exec_agent = TestExecutionAgent(agent=None)
    report_agent = ReportAgent(agent=None)

    orchestrator = OrchestratorAgent(tc_agent, exec_agent, report_agent)

    # 각 에이전트 메서드를 래핑하여 호출 순서 기록
    original_generate = tc_agent.generate_scenario
    original_execute = exec_agent.execute_tests
    original_report = report_agent.generate_report

    def mock_generate(*args, **kwargs):
        call_order.append("TC")
        return scenario

    def mock_execute(*args, **kwargs):
        call_order.append("Execution")
        return execution_result

    def mock_report(*args, **kwargs):
        call_order.append("Report")
        return original_report(*args, **kwargs)

    tc_agent.generate_scenario = mock_generate
    exec_agent.execute_tests = mock_execute
    report_agent.generate_report = mock_report

    # 파이프라인 실행
    result = orchestrator.execute_pipeline(scenario.target_url, scenario.requirements)

    # 실행 순서 검증: TC → Execution → Report
    assert call_order == ["TC", "Execution", "Report"], (
        f"파이프라인 실행 순서가 올바르지 않습니다: {call_order}"
    )

    # 결과가 TestReport 타입인지 확인 (요구사항 2.4)
    assert isinstance(result, TestReport)


@given(scenario=st_test_scenario(), execution_result=st_test_execution_result())
def test_property6_data_flows_between_agents(
    scenario: TestScenario, execution_result: TestExecutionResult
):
    """Property 6: 이전 에이전트의 출력이 다음 에이전트의 입력으로 전달되어야 합니다.

    Feature: qa-agent-system, Property 6: 파이프라인 실행 순서
    검증 대상: 요구사항 2.1, 2.2, 2.3, 2.4
    """
    # 각 에이전트에 전달된 인자를 기록
    tc_args: list = []
    exec_args: list = []
    report_args: list = []

    tc_agent = TCScenarioAgent(agent=None)
    exec_agent = TestExecutionAgent(agent=None)
    report_agent = ReportAgent(agent=None)

    orchestrator = OrchestratorAgent(tc_agent, exec_agent, report_agent)

    def mock_generate(target_url, requirements):
        tc_args.append((target_url, requirements))
        return scenario

    def mock_execute(s):
        exec_args.append(s)
        return execution_result

    original_report = report_agent.generate_report

    def mock_report(er):
        report_args.append(er)
        return original_report(er)

    tc_agent.generate_scenario = mock_generate
    exec_agent.execute_tests = mock_execute
    report_agent.generate_report = mock_report

    orchestrator.execute_pipeline(scenario.target_url, scenario.requirements)

    # TC 에이전트에 올바른 인자가 전달되었는지 확인 (요구사항 2.1)
    assert len(tc_args) == 1
    assert tc_args[0] == (scenario.target_url, scenario.requirements)

    # 실행 에이전트에 TC 에이전트의 출력이 전달되었는지 확인 (요구사항 2.2)
    assert len(exec_args) == 1
    assert exec_args[0] is scenario

    # 리포트 에이전트에 실행 에이전트의 출력이 전달되었는지 확인 (요구사항 2.3)
    assert len(report_args) == 1
    assert report_args[0] is execution_result
