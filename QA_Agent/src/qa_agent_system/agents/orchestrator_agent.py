"""
오케스트레이터 에이전트 (Orchestrator Agent)

전체 QA 파이프라인의 흐름을 조율하는 에이전트입니다.
TC Scenario Agent → Test Execution Agent → Report Agent 순서로
파이프라인을 실행하고, 에이전트 간 데이터 스키마를 검증합니다.

요구사항:
- 2.1: 사용자 입력 수신 시 TC_Scenario_Agent에게 시나리오 작성 위임
- 2.2: TC_Scenario_Agent 완료 시 Test_Execution_Agent에게 전달
- 2.3: Test_Execution_Agent 완료 시 Report_Agent에게 전달
- 2.4: Report_Agent 완료 시 최종 TestReport를 사용자에게 반환
- 2.5: 각 에이전트의 작업 상태(IDLE → RUNNING → COMPLETED/FAILED) 추적
- 2.6: 하위 에이전트 실패 시 에이전트 이름, 실패 단계, 오류 내용 포함 에러 전달
- 2.7: 에이전트 간 전달 데이터의 형식 검증
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from qa_agent_system.errors import PipelineError
from qa_agent_system.models import (
    AgentStatus,
    AgentStatusEnum,
    TestExecutionResult,
    TestReport,
    TestScenario,
    ValidationResult,
)
from qa_agent_system.validator import DataValidator
from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
from qa_agent_system.agents.test_execution_agent import TestExecutionAgent
from qa_agent_system.agents.report_agent import ReportAgent


# 오케스트레이터 에이전트 시스템 프롬프트
ORCHESTRATOR_AGENT_SYSTEM_PROMPT = (
    "당신은 QA 프로세스 전체를 조율하는 오케스트레이터 에이전트입니다. "
    "TC 시나리오 작성 → 테스트 실행 → 리포트 생성 순서로 "
    "파이프라인을 관리하고, 각 에이전트 간 데이터 전달과 검증을 담당합니다. "
    "하위 에이전트의 작업 상태를 추적하고, 실패 시 상세한 에러 정보를 제공합니다."
)

# 파이프라인 단계 이름 상수
_STEP_SCENARIO = "시나리오 작성"
_STEP_EXECUTION = "테스트 실행"
_STEP_REPORT = "리포트 생성"


class OrchestratorAgent:
    """QA 프로세스 흐름 조율 에이전트

    TC → Execution → Report 순서로 파이프라인을 실행하고,
    에이전트 간 데이터 스키마를 검증하며, 작업 상태를 추적합니다.
    """

    def __init__(
        self,
        tc_agent: TCScenarioAgent,
        execution_agent: TestExecutionAgent,
        report_agent: ReportAgent,
    ):
        """OrchestratorAgent 초기화

        Args:
            tc_agent: TC 시나리오 작성 에이전트
            execution_agent: 테스트 실행 에이전트
            report_agent: 리포트 생성 에이전트
        """
        self._tc_agent = tc_agent
        self._execution_agent = execution_agent
        self._report_agent = report_agent
        self._system_prompt = ORCHESTRATOR_AGENT_SYSTEM_PROMPT

        # 에이전트 상태 추적 (요구사항 2.5)
        self._agent_statuses: dict[str, AgentStatus] = {
            "TCScenarioAgent": AgentStatus(
                agent_name="TCScenarioAgent",
                status=AgentStatusEnum.IDLE,
            ),
            "TestExecutionAgent": AgentStatus(
                agent_name="TestExecutionAgent",
                status=AgentStatusEnum.IDLE,
            ),
            "ReportAgent": AgentStatus(
                agent_name="ReportAgent",
                status=AgentStatusEnum.IDLE,
            ),
        }

    @property
    def system_prompt(self) -> str:
        """시스템 프롬프트 반환"""
        return self._system_prompt

    def execute_pipeline(self, target_url: str, requirements: str) -> TestReport:
        """TC → Execution → Report 순서로 파이프라인을 실행합니다.

        요구사항 2.1~2.4: 순차적 파이프라인 실행 및 데이터 전달
        요구사항 2.6: 하위 에이전트 실패 시 에러 전달
        요구사항 2.7: 에이전트 간 데이터 스키마 검증

        Args:
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항

        Returns:
            최종 TestReport

        Raises:
            PipelineError: 하위 에이전트 실패 시
        """
        # 1단계: TC 시나리오 작성 (요구사항 2.1)
        scenario = self._run_scenario_step(target_url, requirements)

        # 시나리오 데이터 스키마 검증 (요구사항 2.7)
        self._validate_or_raise(
            scenario.model_dump(), TestScenario, "TCScenarioAgent", _STEP_SCENARIO
        )

        # 2단계: 테스트 실행 (요구사항 2.2)
        execution_result = self._run_execution_step(scenario)

        # 실행 결과 데이터 스키마 검증 (요구사항 2.7)
        self._validate_or_raise(
            execution_result.model_dump(),
            TestExecutionResult,
            "TestExecutionAgent",
            _STEP_EXECUTION,
        )

        # 3단계: 리포트 생성 (요구사항 2.3, 2.4)
        report = self._run_report_step(execution_result)

        return report

    def validate_data(
        self, data: dict, schema_class: type
    ) -> ValidationResult:
        """에이전트 간 전달 데이터의 스키마를 검증합니다.

        요구사항 2.7: 에이전트 간 전달 데이터 형식 검증

        Args:
            data: 검증할 JSON 데이터 (dict)
            schema_class: 검증에 사용할 Pydantic 모델 클래스

        Returns:
            ValidationResult: 검증 결과
        """
        return DataValidator.validate(data, schema_class)

    def get_agent_status(self, agent_name: str) -> AgentStatus:
        """에이전트 작업 상태를 조회합니다.

        요구사항 2.5: 에이전트 작업 상태 추적

        Args:
            agent_name: 조회할 에이전트 이름

        Returns:
            AgentStatus: 에이전트 상태 정보

        Raises:
            KeyError: 존재하지 않는 에이전트 이름
        """
        if agent_name not in self._agent_statuses:
            raise KeyError(f"알 수 없는 에이전트: {agent_name}")
        return self._agent_statuses[agent_name]

    # ============================================================
    # 내부 파이프라인 단계 실행 메서드
    # ============================================================

    def _update_status(
        self,
        agent_name: str,
        status: AgentStatusEnum,
        error_message: Optional[str] = None,
    ) -> None:
        """에이전트 상태를 업데이트합니다.

        요구사항 2.5: IDLE → RUNNING → COMPLETED/FAILED 상태 전이

        Args:
            agent_name: 에이전트 이름
            status: 새 상태
            error_message: 실패 시 에러 메시지
        """
        now = datetime.now(timezone.utc)
        current = self._agent_statuses[agent_name]

        updates: dict = {"status": status}
        if status == AgentStatusEnum.RUNNING:
            updates["started_at"] = now
        elif status in (AgentStatusEnum.COMPLETED, AgentStatusEnum.FAILED):
            updates["completed_at"] = now
        if error_message is not None:
            updates["error_message"] = error_message

        self._agent_statuses[agent_name] = current.model_copy(update=updates)

    def _run_scenario_step(
        self, target_url: str, requirements: str
    ) -> TestScenario:
        """TC 시나리오 작성 단계를 실행합니다.

        Args:
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항

        Returns:
            생성된 TestScenario

        Raises:
            PipelineError: 시나리오 생성 실패 시
        """
        agent_name = "TCScenarioAgent"
        self._update_status(agent_name, AgentStatusEnum.RUNNING)

        try:
            result = self._tc_agent.generate_scenario(target_url, requirements)

            # 문자열 반환은 추가 정보 요청 메시지 (요구사항 3.6)
            if isinstance(result, str):
                self._update_status(
                    agent_name, AgentStatusEnum.FAILED, error_message=result
                )
                raise PipelineError(
                    agent_name=agent_name,
                    failed_step=_STEP_SCENARIO,
                    cause=result,
                )

            self._update_status(agent_name, AgentStatusEnum.COMPLETED)
            return result

        except PipelineError:
            raise
        except Exception as e:
            error_msg = str(e)
            self._update_status(
                agent_name, AgentStatusEnum.FAILED, error_message=error_msg
            )
            raise PipelineError(
                agent_name=agent_name,
                failed_step=_STEP_SCENARIO,
                cause=error_msg,
            ) from e

    def _run_execution_step(
        self, scenario: TestScenario
    ) -> TestExecutionResult:
        """테스트 실행 단계를 실행합니다.

        Args:
            scenario: 실행할 테스트 시나리오

        Returns:
            테스트 실행 결과

        Raises:
            PipelineError: 테스트 실행 실패 시
        """
        agent_name = "TestExecutionAgent"
        self._update_status(agent_name, AgentStatusEnum.RUNNING)

        try:
            result = self._execution_agent.execute_tests(scenario)
            self._update_status(agent_name, AgentStatusEnum.COMPLETED)
            return result

        except Exception as e:
            error_msg = str(e)
            self._update_status(
                agent_name, AgentStatusEnum.FAILED, error_message=error_msg
            )
            raise PipelineError(
                agent_name=agent_name,
                failed_step=_STEP_EXECUTION,
                cause=error_msg,
            ) from e

    def _run_report_step(
        self, execution_result: TestExecutionResult
    ) -> TestReport:
        """리포트 생성 단계를 실행합니다.

        Args:
            execution_result: 테스트 실행 결과

        Returns:
            생성된 TestReport

        Raises:
            PipelineError: 리포트 생성 실패 시
        """
        agent_name = "ReportAgent"
        self._update_status(agent_name, AgentStatusEnum.RUNNING)

        try:
            report = self._report_agent.generate_report(execution_result)
            self._update_status(agent_name, AgentStatusEnum.COMPLETED)
            return report

        except Exception as e:
            error_msg = str(e)
            self._update_status(
                agent_name, AgentStatusEnum.FAILED, error_message=error_msg
            )
            raise PipelineError(
                agent_name=agent_name,
                failed_step=_STEP_REPORT,
                cause=error_msg,
            ) from e

    def _validate_or_raise(
        self,
        data: dict,
        schema_class: type,
        agent_name: str,
        step_name: str,
    ) -> None:
        """데이터 스키마를 검증하고, 실패 시 PipelineError를 발생시킵니다.

        요구사항 2.7: 에이전트 간 전달 데이터 형식 검증

        Args:
            data: 검증할 데이터
            schema_class: Pydantic 모델 클래스
            agent_name: 데이터를 생성한 에이전트 이름
            step_name: 파이프라인 단계 이름

        Raises:
            PipelineError: 스키마 검증 실패 시
        """
        result = self.validate_data(data, schema_class)
        if not result.is_valid:
            error_detail = "; ".join(result.errors)
            raise PipelineError(
                agent_name=agent_name,
                failed_step=step_name,
                cause=f"스키마 검증 실패: {error_detail}",
            )
