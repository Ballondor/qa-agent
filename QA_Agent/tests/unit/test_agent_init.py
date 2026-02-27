"""
시스템 초기화 단위 테스트 (Agent Initialization Unit Tests)

QAAgentSystem의 4개 에이전트 생성, Bedrock 모델 설정,
초기화 실패 시 에러 처리를 검증합니다.

요구사항:
- 1.1: 4개 에이전트 생성 확인
- 1.2: 각 에이전트에 Bedrock Opus 모델 설정 확인
- 1.4: 에이전트 초기화 실패 시 에러 메시지 확인
- 1.5: Bedrock 모델 연결 실패 시 에러 메시지 및 재시도 안내 확인
"""

from unittest.mock import patch, MagicMock

import pytest

from qa_agent_system.errors import AgentInitError, ModelConnectionError
from qa_agent_system.system import QAAgentSystem, _DEFAULT_MODEL_ID
from qa_agent_system.agents.orchestrator_agent import OrchestratorAgent
from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
from qa_agent_system.agents.test_execution_agent import TestExecutionAgent
from qa_agent_system.agents.report_agent import ReportAgent


class TestQAAgentSystemInit:
    """QAAgentSystem 초기화 테스트"""

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_creates_four_agents(self, mock_create, mock_create_exec):
        """요구사항 1.1: 4개 에이전트가 생성되는지 확인합니다."""
        mock_create.return_value = MagicMock()
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        system = QAAgentSystem()

        # _create_strands_agent가 2번 호출됨 (TC, Report)
        # TestExecutionAgent는 Playwright MCP 연결을 위해 별도 생성
        # 오케스트레이터는 Strands Agent 없이 래핑만 함
        assert mock_create.call_count == 2

        # 각 에이전트 인스턴스가 올바른 타입인지 확인
        assert isinstance(system._tc_agent, TCScenarioAgent)
        assert isinstance(system._execution_agent, TestExecutionAgent)
        assert isinstance(system._report_agent, ReportAgent)
        assert isinstance(system._orchestrator, OrchestratorAgent)

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_default_model_id(self, mock_create, mock_create_exec):
        """요구사항 1.2: 기본 Bedrock Opus 모델 ID가 설정되는지 확인합니다."""
        mock_create.return_value = MagicMock()
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        system = QAAgentSystem()

        assert system.model_id == _DEFAULT_MODEL_ID

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_custom_model_id(self, mock_create, mock_create_exec):
        """요구사항 1.2: 커스텀 모델 ID가 설정되는지 확인합니다."""
        mock_create.return_value = MagicMock()
        mock_create_exec.return_value = TestExecutionAgent(agent=None)
        custom_id = "us.anthropic.claude-sonnet-4-20250514"

        system = QAAgentSystem(model_id=custom_id)

        assert system.model_id == custom_id

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_agent_names_in_create_calls(self, mock_create, mock_create_exec):
        """요구사항 1.1: 각 에이전트가 올바른 이름으로 생성되는지 확인합니다."""
        mock_create.return_value = MagicMock()
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        QAAgentSystem()

        # _create_strands_agent로 생성되는 에이전트 이름 수집 (TC, Report)
        agent_names = [call.args[0] for call in mock_create.call_args_list]
        assert "TCScenarioAgent" in agent_names
        assert "ReportAgent" in agent_names
        # TestExecutionAgent는 Playwright MCP 연결을 위해 별도 메서드로 생성
        assert mock_create_exec.call_count == 1


class TestAgentInitFailure:
    """에이전트 초기화 실패 테스트"""

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_agent_init_error_contains_agent_name(self, mock_create, mock_create_exec):
        """요구사항 1.4: 초기화 실패 시 에이전트 이름이 에러에 포함되는지 확인합니다."""
        mock_create.side_effect = AgentInitError(
            agent_name="TCScenarioAgent",
            cause="모듈 로드 실패",
        )
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        with pytest.raises(AgentInitError) as exc_info:
            QAAgentSystem()

        assert "TCScenarioAgent" in str(exc_info.value)
        assert exc_info.value.agent_name == "TCScenarioAgent"

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_agent_init_error_contains_cause(self, mock_create, mock_create_exec):
        """요구사항 1.4: 초기화 실패 시 오류 원인이 에러에 포함되는지 확인합니다."""
        mock_create.side_effect = AgentInitError(
            agent_name="ReportAgent",
            cause="시스템 프롬프트 설정 오류",
        )
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        with pytest.raises(AgentInitError) as exc_info:
            QAAgentSystem()

        assert "시스템 프롬프트 설정 오류" in str(exc_info.value)
        assert exc_info.value.cause == "시스템 프롬프트 설정 오류"


class TestModelConnectionFailure:
    """Bedrock 모델 연결 실패 테스트"""

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_model_connection_error_contains_cause(self, mock_create, mock_create_exec):
        """요구사항 1.5: 연결 실패 시 원인이 에러에 포함되는지 확인합니다."""
        mock_create.side_effect = ModelConnectionError(
            agent_name="TestExecutionAgent",
            cause="네트워크 타임아웃",
        )
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        with pytest.raises(ModelConnectionError) as exc_info:
            QAAgentSystem()

        assert "네트워크 타임아웃" in str(exc_info.value)
        assert exc_info.value.agent_name == "TestExecutionAgent"

    @patch("qa_agent_system.system.QAAgentSystem._create_execution_agent")
    @patch("qa_agent_system.system.QAAgentSystem._create_strands_agent")
    def test_model_connection_error_contains_retry_guidance(self, mock_create, mock_create_exec):
        """요구사항 1.5: 연결 실패 시 재시도 안내가 포함되는지 확인합니다."""
        mock_create.side_effect = ModelConnectionError(
            agent_name="TCScenarioAgent",
            cause="AWS 자격 증명 만료",
        )
        mock_create_exec.return_value = TestExecutionAgent(agent=None)

        with pytest.raises(ModelConnectionError) as exc_info:
            QAAgentSystem()

        # 재시도 안내 메시지가 포함되어야 함
        assert exc_info.value.retry_guidance is not None
        assert "재시도" in exc_info.value.retry_guidance
        assert "재시도" in str(exc_info.value)
