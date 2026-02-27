"""
QA 에이전트 시스템 메인 진입점 (QAAgentSystem)

Strands SDK와 Bedrock Opus 4.6 모델을 사용하여
4개의 에이전트를 초기화하고 전체 QA 프로세스를 실행하는 메인 클래스입니다.

요구사항:
- 1.1: Strands SDK로 4개 에이전트 초기화
- 1.2: 각 에이전트에 Bedrock Opus 4.6 모델 설정
- 1.3: 각 에이전트에 역할별 시스템 프롬프트 설정
- 1.4: 에이전트 초기화 실패 시 에이전트 이름 + 원인 포함 에러 반환
- 1.5: Bedrock 모델 연결 실패 시 연결 실패 원인 + 재시도 안내 반환
"""

from __future__ import annotations

from qa_agent_system.errors import AgentInitError, ModelConnectionError
from qa_agent_system.models import TestReport
from qa_agent_system.agents.orchestrator_agent import OrchestratorAgent
from qa_agent_system.agents.tc_scenario_agent import (
    TCScenarioAgent,
    TC_SCENARIO_AGENT_SYSTEM_PROMPT,
)
from qa_agent_system.agents.test_execution_agent import (
    TestExecutionAgent,
    TEST_EXECUTION_AGENT_SYSTEM_PROMPT,
)
from qa_agent_system.agents.report_agent import (
    ReportAgent,
    REPORT_AGENT_SYSTEM_PROMPT,
)
from qa_agent_system.agents.orchestrator_agent import ORCHESTRATOR_AGENT_SYSTEM_PROMPT

# 기본 Bedrock 모델 ID (cross-region inference profile 형식)
_DEFAULT_MODEL_ID = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


class QAAgentSystem:
    """QA 에이전트 시스템의 메인 진입점

    Strands SDK와 Bedrock Opus 4.6 모델을 사용하여
    4개의 에이전트(Orchestrator, TC Scenario, Test Execution, Report)를
    초기화하고 전체 QA 프로세스를 실행합니다.
    """

    def __init__(self, model_id: str = _DEFAULT_MODEL_ID):
        """시스템 초기화 - 4개 에이전트 생성

        요구사항 1.1: Strands SDK로 4개 에이전트 초기화
        요구사항 1.2: 각 에이전트에 Bedrock Opus 4.6 모델 설정
        요구사항 1.3: 각 에이전트에 역할별 시스템 프롬프트 설정

        Args:
            model_id: Bedrock 모델 ID (기본값: Opus 4.6)

        Raises:
            AgentInitError: 에이전트 초기화 실패 시 (요구사항 1.4)
            ModelConnectionError: Bedrock 모델 연결 실패 시 (요구사항 1.5)
        """
        self._model_id = model_id

        # 각 에이전트를 순차적으로 초기화
        self._tc_agent = self._create_tc_agent()
        self._execution_agent = self._create_execution_agent()
        self._report_agent = self._create_report_agent()
        self._orchestrator = self._create_orchestrator()

    @property
    def model_id(self) -> str:
        """설정된 Bedrock 모델 ID 반환"""
        return self._model_id

    @property
    def orchestrator(self) -> OrchestratorAgent:
        """오케스트레이터 에이전트 반환"""
        return self._orchestrator

    def run(self, target_url: str, requirements: str) -> TestReport:
        """OrchestratorAgent를 통한 전체 QA 프로세스 실행

        Args:
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항

        Returns:
            최종 TestReport
        """
        return self._orchestrator.execute_pipeline(target_url, requirements)

    # ============================================================
    # 에이전트 생성 메서드
    # ============================================================

    def _create_strands_agent(self, agent_name: str, system_prompt: str):
        """Strands Agent 인스턴스를 생성합니다.

        요구사항 1.2: Bedrock Opus 4.6 모델 설정
        요구사항 1.3: 역할별 시스템 프롬프트 설정

        Args:
            agent_name: 에이전트 이름 (에러 메시지용)
            system_prompt: 시스템 프롬프트

        Returns:
            Strands Agent 인스턴스

        Raises:
            AgentInitError: 에이전트 생성 실패 시
            ModelConnectionError: Bedrock 모델 연결 실패 시
        """
        try:
            from strands import Agent
            from strands.models.bedrock import BedrockModel

            # Bedrock 모델 생성 (요구사항 1.2)
            model = BedrockModel(model_id=self._model_id)

            # Strands Agent 생성 (요구사항 1.3)
            agent = Agent(
                model=model,
                system_prompt=system_prompt,
            )
            return agent

        except ImportError as e:
            raise AgentInitError(
                agent_name=agent_name,
                cause=f"Strands SDK 모듈을 찾을 수 없습니다: {e}",
            ) from e

        except ConnectionError as e:
            # Bedrock 모델 연결 실패 (요구사항 1.5)
            raise ModelConnectionError(
                agent_name=agent_name,
                cause=str(e),
            ) from e

        except Exception as e:
            # 기타 초기화 실패 (요구사항 1.4)
            raise AgentInitError(
                agent_name=agent_name,
                cause=str(e),
            ) from e

    def _create_tc_agent(self) -> TCScenarioAgent:
        """TC 시나리오 작성 에이전트를 생성합니다."""
        agent = self._create_strands_agent(
            "TCScenarioAgent", TC_SCENARIO_AGENT_SYSTEM_PROMPT
        )
        return TCScenarioAgent(agent=agent)

    def _create_execution_agent(self) -> TestExecutionAgent:
        """테스트 실행 에이전트를 생성합니다.

        Playwright MCP 서버를 연결하여 브라우저 자동화 도구를 사용할 수 있도록 합니다.
        """
        try:
            from mcp import stdio_client, StdioServerParameters
            from strands import Agent
            from strands.models.bedrock import BedrockModel
            from strands.tools.mcp import MCPClient

            # Bedrock 모델 생성
            model = BedrockModel(model_id=self._model_id)

            # Playwright MCP 클라이언트 생성
            playwright_mcp = MCPClient(lambda: stdio_client(
                StdioServerParameters(
                    command="npx",
                    args=["@playwright/mcp@latest"],
                )
            ))

            # MCP 클라이언트를 tools에 전달 - 라이프사이클 자동 관리
            agent = Agent(
                model=model,
                system_prompt=TEST_EXECUTION_AGENT_SYSTEM_PROMPT,
                tools=[playwright_mcp],
            )

            # MCP 클라이언트 참조 보관 (정리용)
            self._playwright_mcp = playwright_mcp

            return TestExecutionAgent(agent=agent)

        except ImportError as e:
            raise AgentInitError(
                agent_name="TestExecutionAgent",
                cause=f"MCP 모듈을 찾을 수 없습니다: {e}",
            ) from e

        except ConnectionError as e:
            raise ModelConnectionError(
                agent_name="TestExecutionAgent",
                cause=str(e),
            ) from e

        except Exception as e:
            raise AgentInitError(
                agent_name="TestExecutionAgent",
                cause=str(e),
            ) from e

    def _create_report_agent(self) -> ReportAgent:
        """리포트 생성 에이전트를 생성합니다."""
        agent = self._create_strands_agent(
            "ReportAgent", REPORT_AGENT_SYSTEM_PROMPT
        )
        return ReportAgent(agent=agent)

    def _create_orchestrator(self) -> OrchestratorAgent:
        """오케스트레이터 에이전트를 생성합니다."""
        return OrchestratorAgent(
            tc_agent=self._tc_agent,
            execution_agent=self._execution_agent,
            report_agent=self._report_agent,
        )
