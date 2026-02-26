"""
에러 처리 모듈 단위 테스트 (Error Handling Unit Tests)

커스텀 예외 클래스들이 에이전트 이름, 오류 원인, 실패 단계 등
필수 정보를 올바르게 포함하는지 검증합니다.

요구사항: 1.4, 1.5, 2.6, 4.5
"""

import pytest

from qa_agent_system.errors import (
    QAAgentError,
    AgentInitError,
    ModelConnectionError,
    PipelineError,
    PlaywrightConnectionError,
)


# ============================================================
# QAAgentError 기본 예외 테스트
# ============================================================


class TestQAAgentError:
    """기본 예외 클래스 테스트"""

    def test_에이전트_이름과_원인_저장(self):
        """에이전트 이름과 원인이 속성에 올바르게 저장되는지 확인"""
        error = QAAgentError(agent_name="TestAgent", cause="테스트 원인")
        assert error.agent_name == "TestAgent"
        assert error.cause == "테스트 원인"

    def test_기본_메시지_자동_생성(self):
        """message를 지정하지 않으면 자동으로 생성되는지 확인"""
        error = QAAgentError(agent_name="TestAgent", cause="테스트 원인")
        assert "[TestAgent]" in str(error)
        assert "테스트 원인" in str(error)

    def test_커스텀_메시지_사용(self):
        """message를 직접 지정하면 해당 메시지가 사용되는지 확인"""
        error = QAAgentError(
            agent_name="TestAgent", cause="원인", message="커스텀 메시지"
        )
        assert str(error) == "커스텀 메시지"

    def test_Exception_상속(self):
        """QAAgentError가 Exception을 상속하는지 확인"""
        error = QAAgentError(agent_name="TestAgent", cause="원인")
        assert isinstance(error, Exception)


# ============================================================
# AgentInitError 테스트 (요구사항 1.4)
# ============================================================


class TestAgentInitError:
    """에이전트 초기화 실패 예외 테스트"""

    def test_에이전트_이름_포함(self):
        """에러 메시지에 실패한 에이전트 이름이 포함되는지 확인"""
        error = AgentInitError(
            agent_name="TC_Scenario_Agent", cause="시스템 프롬프트 설정 실패"
        )
        assert error.agent_name == "TC_Scenario_Agent"
        assert "TC_Scenario_Agent" in str(error)

    def test_오류_원인_포함(self):
        """에러 메시지에 오류 원인이 포함되는지 확인"""
        error = AgentInitError(
            agent_name="Report_Agent", cause="모듈 로드 실패"
        )
        assert error.cause == "모듈 로드 실패"
        assert "모듈 로드 실패" in str(error)

    def test_QAAgentError_상속(self):
        """AgentInitError가 QAAgentError를 상속하는지 확인"""
        error = AgentInitError(agent_name="Agent", cause="원인")
        assert isinstance(error, QAAgentError)


# ============================================================
# ModelConnectionError 테스트 (요구사항 1.5)
# ============================================================


class TestModelConnectionError:
    """Bedrock 모델 연결 실패 예외 테스트"""

    def test_에이전트_이름_포함(self):
        """에러 메시지에 에이전트 이름이 포함되는지 확인"""
        error = ModelConnectionError(
            agent_name="Orchestrator_Agent", cause="타임아웃"
        )
        assert error.agent_name == "Orchestrator_Agent"
        assert "Orchestrator_Agent" in str(error)

    def test_연결_실패_원인_포함(self):
        """에러 메시지에 연결 실패 원인이 포함되는지 확인"""
        error = ModelConnectionError(
            agent_name="Agent", cause="AWS 자격 증명 만료"
        )
        assert error.cause == "AWS 자격 증명 만료"
        assert "AWS 자격 증명 만료" in str(error)

    def test_재시도_안내_포함(self):
        """에러 메시지에 재시도 안내가 포함되는지 확인"""
        error = ModelConnectionError(
            agent_name="Agent", cause="네트워크 오류"
        )
        assert error.retry_guidance is not None
        assert len(error.retry_guidance) > 0
        # 에러 메시지 자체에도 재시도 안내가 포함되어야 함
        assert "재시도" in str(error)

    def test_QAAgentError_상속(self):
        """ModelConnectionError가 QAAgentError를 상속하는지 확인"""
        error = ModelConnectionError(agent_name="Agent", cause="원인")
        assert isinstance(error, QAAgentError)


# ============================================================
# PipelineError 테스트 (요구사항 2.6)
# ============================================================


class TestPipelineError:
    """오케스트레이터 파이프라인 실패 예외 테스트"""

    def test_에이전트_이름_포함(self):
        """에러 메시지에 실패한 에이전트 이름이 포함되는지 확인"""
        error = PipelineError(
            agent_name="Test_Execution_Agent",
            failed_step="테스트 실행",
            cause="브라우저 크래시",
        )
        assert error.agent_name == "Test_Execution_Agent"
        assert "Test_Execution_Agent" in str(error)

    def test_실패_단계_포함(self):
        """에러 메시지에 실패 단계 정보가 포함되는지 확인"""
        error = PipelineError(
            agent_name="Agent",
            failed_step="시나리오 작성",
            cause="원인",
        )
        assert error.failed_step == "시나리오 작성"
        assert "시나리오 작성" in str(error)

    def test_오류_내용_포함(self):
        """에러 메시지에 오류 내용이 포함되는지 확인"""
        error = PipelineError(
            agent_name="Agent",
            failed_step="단계",
            cause="JSON 파싱 실패",
        )
        assert error.cause == "JSON 파싱 실패"
        assert "JSON 파싱 실패" in str(error)

    def test_QAAgentError_상속(self):
        """PipelineError가 QAAgentError를 상속하는지 확인"""
        error = PipelineError(
            agent_name="Agent", failed_step="단계", cause="원인"
        )
        assert isinstance(error, QAAgentError)


# ============================================================
# PlaywrightConnectionError 테스트 (요구사항 4.5)
# ============================================================


class TestPlaywrightConnectionError:
    """Playwright MCP 연결 실패 예외 테스트"""

    def test_에이전트_이름_포함(self):
        """에러 메시지에 에이전트 이름이 포함되는지 확인"""
        error = PlaywrightConnectionError(
            agent_name="Test_Execution_Agent", cause="MCP 서버 응답 없음"
        )
        assert error.agent_name == "Test_Execution_Agent"
        assert "Test_Execution_Agent" in str(error)

    def test_연결_실패_원인_포함(self):
        """에러 메시지에 연결 실패 원인이 포함되는지 확인"""
        error = PlaywrightConnectionError(
            agent_name="Agent", cause="포트 충돌"
        )
        assert error.cause == "포트 충돌"
        assert "포트 충돌" in str(error)

    def test_QAAgentError_상속(self):
        """PlaywrightConnectionError가 QAAgentError를 상속하는지 확인"""
        error = PlaywrightConnectionError(agent_name="Agent", cause="원인")
        assert isinstance(error, QAAgentError)


# ============================================================
# 예외 raise/catch 통합 테스트
# ============================================================


class TestErrorRaiseCatch:
    """예외를 실제로 raise하고 catch하는 통합 테스트"""

    def test_AgentInitError_raise_catch(self):
        """AgentInitError를 raise하고 catch할 수 있는지 확인"""
        with pytest.raises(AgentInitError) as exc_info:
            raise AgentInitError(
                agent_name="TC_Scenario_Agent", cause="초기화 실패"
            )
        assert exc_info.value.agent_name == "TC_Scenario_Agent"

    def test_ModelConnectionError_raise_catch(self):
        """ModelConnectionError를 raise하고 catch할 수 있는지 확인"""
        with pytest.raises(ModelConnectionError) as exc_info:
            raise ModelConnectionError(
                agent_name="Orchestrator_Agent", cause="연결 타임아웃"
            )
        assert exc_info.value.agent_name == "Orchestrator_Agent"
        assert exc_info.value.retry_guidance is not None

    def test_PipelineError_raise_catch(self):
        """PipelineError를 raise하고 catch할 수 있는지 확인"""
        with pytest.raises(PipelineError) as exc_info:
            raise PipelineError(
                agent_name="Report_Agent",
                failed_step="리포트 생성",
                cause="데이터 형식 오류",
            )
        assert exc_info.value.agent_name == "Report_Agent"
        assert exc_info.value.failed_step == "리포트 생성"

    def test_PlaywrightConnectionError_raise_catch(self):
        """PlaywrightConnectionError를 raise하고 catch할 수 있는지 확인"""
        with pytest.raises(PlaywrightConnectionError) as exc_info:
            raise PlaywrightConnectionError(
                agent_name="Test_Execution_Agent", cause="MCP 서버 다운"
            )
        assert exc_info.value.agent_name == "Test_Execution_Agent"

    def test_QAAgentError로_모든_예외_catch(self):
        """모든 커스텀 예외를 QAAgentError로 catch할 수 있는지 확인"""
        errors = [
            AgentInitError(agent_name="A", cause="c"),
            ModelConnectionError(agent_name="B", cause="c"),
            PipelineError(agent_name="C", failed_step="s", cause="c"),
            PlaywrightConnectionError(agent_name="D", cause="c"),
        ]
        for error in errors:
            with pytest.raises(QAAgentError):
                raise error


# ============================================================
# 빈 실행 결과 리포트 생성 테스트 (요구사항 5.7)
# ============================================================


class TestEmptyExecutionResultReport:
    """빈 TestExecutionResult에 대해 ReportAgent가
    "실행 결과 없음" 리포트를 올바르게 생성하는지 검증합니다.

    요구사항 5.7: 테스트 실행 결과 데이터가 비어있으면
    실행 결과가 없음을 명시한 리포트를 생성한다.
    """

    @pytest.fixture()
    def report_agent(self):
        """ReportAgent 인스턴스 생성 (Strands Agent 없이)"""
        from qa_agent_system.agents.report_agent import ReportAgent

        return ReportAgent()

    @pytest.fixture()
    def empty_execution_result(self):
        """빈 results를 가진 TestExecutionResult 생성"""
        from datetime import datetime, timezone

        from qa_agent_system.models import TestExecutionResult

        return TestExecutionResult(
            scenario_id="SC-001",
            target_url="https://example.com",
            results=[],
            total_execution_time_ms=0.0,
            executed_at=datetime.now(timezone.utc),
        )

    def test_빈_결과에서_TestReport_반환(self, report_agent, empty_execution_result):
        """generate_report()가 빈 결과에 대해 TestReport를 반환하는지 확인"""
        from qa_agent_system.models import TestReport

        report = report_agent.generate_report(empty_execution_result)
        assert isinstance(report, TestReport)

    def test_요약_통계_모두_0(self, report_agent, empty_execution_result):
        """리포트 요약의 모든 통계가 0인지 확인"""
        report = report_agent.generate_report(empty_execution_result)
        assert report.summary.total_tests == 0
        assert report.summary.passed_tests == 0
        assert report.summary.failed_tests == 0
        assert report.summary.success_rate == 0.0

    def test_상세_결과_비어있음(self, report_agent, empty_execution_result):
        """detailed_results가 빈 리스트인지 확인"""
        report = report_agent.generate_report(empty_execution_result)
        assert report.detailed_results == []

    def test_실패_스크린샷_비어있음(self, report_agent, empty_execution_result):
        """failed_screenshots가 빈 리스트인지 확인"""
        report = report_agent.generate_report(empty_execution_result)
        assert report.failed_screenshots == []

    def test_마크다운에_실행_결과_없음_포함(self, report_agent, empty_execution_result):
        """markdown_content에 '실행 결과 없음' 문구가 포함되는지 확인"""
        report = report_agent.generate_report(empty_execution_result)
        assert "실행 결과 없음" in report.markdown_content

# ============================================================
# Playwright MCP 연결 실패 테스트 (요구사항 4.4, 4.5)
# ============================================================


class TestPlaywrightConnectionFailure:
    """TestExecutionAgent에서 Playwright MCP 연결 실패 시
    PlaywrightConnectionError가 올바르게 발생하는지 검증합니다.

    요구사항 4.5: Playwright MCP 연결 실패 시 연결 실패 원인을 포함한
    에러 메시지를 반환하고 재시도 없이 즉시 종료한다.
    """

    @pytest.fixture()
    def mock_agent_with_connection_error(self):
        """ConnectionError를 발생시키는 모킹된 Strands Agent 생성"""
        from unittest.mock import MagicMock

        agent = MagicMock()
        agent.side_effect = ConnectionError("MCP 서버에 연결할 수 없습니다")
        return agent

    @pytest.fixture()
    def sample_scenario(self):
        """테스트용 TestScenario 생성"""
        from datetime import datetime, timezone

        from qa_agent_system.models import TestCase, TestScenario, TestStep

        return TestScenario(
            target_url="https://example.com",
            requirements="로그인 기능 테스트",
            test_cases=[
                TestCase(
                    id="TC-001",
                    name="로그인 성공 테스트",
                    preconditions=["사용자 계정 존재"],
                    steps=[
                        TestStep(
                            step_number=1,
                            action="로그인 페이지 접속",
                            expected_result="로그인 폼 표시",
                        )
                    ],
                    expected_result="로그인 성공",
                    scenario_type="positive",
                )
            ],
            created_at=datetime.now(timezone.utc),
        )

    def test_연결_실패_시_PlaywrightConnectionError_발생(
        self, mock_agent_with_connection_error, sample_scenario
    ):
        """ConnectionError 발생 시 PlaywrightConnectionError로 변환되는지 확인"""
        from qa_agent_system.agents.test_execution_agent import TestExecutionAgent

        agent = TestExecutionAgent(agent=mock_agent_with_connection_error)

        with pytest.raises(PlaywrightConnectionError):
            agent.execute_tests(sample_scenario)

    def test_에러에_에이전트_이름_포함(
        self, mock_agent_with_connection_error, sample_scenario
    ):
        """PlaywrightConnectionError에 올바른 agent_name이 포함되는지 확인"""
        from qa_agent_system.agents.test_execution_agent import TestExecutionAgent

        agent = TestExecutionAgent(agent=mock_agent_with_connection_error)

        with pytest.raises(PlaywrightConnectionError) as exc_info:
            agent.execute_tests(sample_scenario)

        assert exc_info.value.agent_name == "TestExecutionAgent"

    def test_에러에_원인_포함(
        self, mock_agent_with_connection_error, sample_scenario
    ):
        """PlaywrightConnectionError에 원래 ConnectionError의 원인이 포함되는지 확인"""
        from qa_agent_system.agents.test_execution_agent import TestExecutionAgent

        agent = TestExecutionAgent(agent=mock_agent_with_connection_error)

        with pytest.raises(PlaywrightConnectionError) as exc_info:
            agent.execute_tests(sample_scenario)

        assert "MCP 서버에 연결할 수 없습니다" in exc_info.value.cause

    def test_재시도_없이_즉시_종료(
        self, mock_agent_with_connection_error, sample_scenario
    ):
        """연결 실패 시 재시도 없이 Agent가 정확히 1번만 호출되는지 확인"""
        from qa_agent_system.agents.test_execution_agent import TestExecutionAgent

        agent = TestExecutionAgent(agent=mock_agent_with_connection_error)

        with pytest.raises(PlaywrightConnectionError):
            agent.execute_tests(sample_scenario)

        # 모킹된 Agent가 정확히 1번만 호출되어야 함 (재시도 없음)
        assert mock_agent_with_connection_error.call_count == 1

