"""
TC 시나리오 작성 에이전트 단위 테스트 (TC Scenario Agent Unit Tests)

TCScenarioAgent의 시나리오 생성, 불충분한 요구사항 처리,
긍정/부정 시나리오 양면성 보장 등을 검증합니다.

요구사항: 3.1, 3.2, 3.3, 3.4, 3.6, 3.7
"""

from unittest.mock import MagicMock

import pytest

from qa_agent_system.agents.tc_scenario_agent import (
    TC_SCENARIO_AGENT_SYSTEM_PROMPT,
    TCScenarioAgent,
)
from qa_agent_system.models import TestScenario


# ============================================================
# 초기화 테스트
# ============================================================


class TestTCScenarioAgentInit:
    """TCScenarioAgent 초기화 테스트"""

    def test_agent_없이_초기화(self):
        """Agent 없이 초기화할 수 있는지 확인"""
        agent = TCScenarioAgent()
        assert agent._agent is None

    def test_agent_전달_초기화(self):
        """Agent를 전달하여 초기화할 수 있는지 확인"""
        mock_agent = MagicMock()
        agent = TCScenarioAgent(agent=mock_agent)
        assert agent._agent is mock_agent

    def test_시스템_프롬프트_설정(self):
        """시스템 프롬프트가 올바르게 설정되는지 확인"""
        agent = TCScenarioAgent()
        assert agent.system_prompt == TC_SCENARIO_AGENT_SYSTEM_PROMPT
        assert len(agent.system_prompt) > 0

    def test_시스템_프롬프트_긍정_부정_언급(self):
        """시스템 프롬프트에 긍정/부정 시나리오 관련 내용이 포함되는지 확인"""
        agent = TCScenarioAgent()
        assert "긍정" in agent.system_prompt
        assert "부정" in agent.system_prompt


# ============================================================
# 기본 시나리오 생성 테스트 (Agent 없이)
# ============================================================


class TestGenerateScenarioWithoutAgent:
    """Agent 없이 기본 시나리오 생성 테스트"""

    @pytest.fixture()
    def agent(self):
        """Agent 없는 TCScenarioAgent 인스턴스"""
        return TCScenarioAgent()

    def test_기본_시나리오_반환_타입(self, agent):
        """Agent 없이 호출 시 TestScenario를 반환하는지 확인 (요구사항 3.1)"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        assert isinstance(result, TestScenario)

    def test_target_url_설정(self, agent):
        """생성된 시나리오에 target_url이 올바르게 설정되는지 확인"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        assert result.target_url == "https://example.com"

    def test_requirements_설정(self, agent):
        """생성된 시나리오에 requirements가 올바르게 설정되는지 확인"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        assert result.requirements == "로그인 기능을 테스트합니다"

    def test_테스트_케이스_비어있지_않음(self, agent):
        """생성된 시나리오에 테스트 케이스가 포함되는지 확인 (요구사항 3.2)"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        assert len(result.test_cases) > 0

    def test_긍정_부정_시나리오_모두_포함(self, agent):
        """긍정/부정 시나리오가 모두 포함되는지 확인 (요구사항 3.3)"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        types = {tc.scenario_type for tc in result.test_cases}
        assert "positive" in types
        assert "negative" in types

    def test_테스트_케이스_필수_필드(self, agent):
        """각 테스트 케이스에 필수 필드가 포함되는지 확인 (요구사항 3.2)"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        for tc in result.test_cases:
            assert len(tc.id) > 0
            assert len(tc.name) > 0
            assert len(tc.steps) > 0
            assert len(tc.expected_result) > 0

    def test_JSON_직렬화_가능(self, agent):
        """생성된 시나리오가 JSON으로 직렬화 가능한지 확인 (요구사항 3.4)"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        json_str = result.model_dump_json()
        assert len(json_str) > 0

    def test_Playwright_MCP_실행_가능한_단계(self, agent):
        """테스트 단계가 Playwright MCP 실행 가능한 형태인지 확인 (요구사항 3.7)"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        for tc in result.test_cases:
            for step in tc.steps:
                # 액션이 비어있지 않아야 함
                assert len(step.action) > 0
                assert len(step.expected_result) > 0


# ============================================================
# 불충분한 요구사항 처리 테스트 (요구사항 3.6)
# ============================================================


class TestInsufficientRequirements:
    """불충분한 요구사항에 대한 추가 정보 요청 메시지 처리 테스트"""

    @pytest.fixture()
    def agent(self):
        return TCScenarioAgent()

    def test_빈_요구사항(self, agent):
        """빈 요구사항 시 문자열 메시지를 반환하는지 확인"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="",
        )
        assert isinstance(result, str)
        assert "불충분" in result or "추가" in result

    def test_짧은_요구사항(self, agent):
        """너무 짧은 요구사항 시 문자열 메시지를 반환하는지 확인"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="테스트",
        )
        assert isinstance(result, str)

    def test_공백만_있는_요구사항(self, agent):
        """공백만 있는 요구사항 시 문자열 메시지를 반환하는지 확인"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="         ",
        )
        assert isinstance(result, str)

    def test_충분한_요구사항은_시나리오_반환(self, agent):
        """충분한 요구사항 시 TestScenario를 반환하는지 확인"""
        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="사용자가 이메일과 비밀번호로 로그인할 수 있어야 합니다",
        )
        assert isinstance(result, TestScenario)


# ============================================================
# LLM 응답 파싱 테스트
# ============================================================


class TestAgentResponseParsing:
    """Strands Agent(LLM) 응답 파싱 테스트"""

    @pytest.fixture()
    def agent_with_mock(self):
        """Mock Agent가 있는 TCScenarioAgent"""
        mock = MagicMock()
        return TCScenarioAgent(agent=mock), mock

    def test_유효한_JSON_응답_파싱(self, agent_with_mock):
        """유효한 JSON 응답이 TestScenario로 파싱되는지 확인"""
        agent, mock = agent_with_mock
        mock.return_value = (
            '{"test_cases": ['
            '{"id": "TC-001", "name": "로그인 성공", '
            '"preconditions": ["브라우저 실행"], '
            '"steps": [{"step_number": 1, "action": "Navigate to https://example.com", '
            '"expected_result": "페이지 로드"}], '
            '"expected_result": "로그인 성공", "scenario_type": "positive"}, '
            '{"id": "TC-002", "name": "잘못된 비밀번호", '
            '"preconditions": ["브라우저 실행"], '
            '"steps": [{"step_number": 1, "action": "Navigate to https://example.com", '
            '"expected_result": "페이지 로드"}], '
            '"expected_result": "에러 표시", "scenario_type": "negative"}'
            "]}"
        )

        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        assert isinstance(result, TestScenario)
        assert len(result.test_cases) >= 2

    def test_코드블록_JSON_응답_파싱(self, agent_with_mock):
        """코드 블록으로 감싸진 JSON 응답이 파싱되는지 확인"""
        agent, mock = agent_with_mock
        mock.return_value = (
            "다음은 테스트 시나리오입니다:\n"
            "```json\n"
            '{"test_cases": ['
            '{"id": "TC-001", "name": "페이지 로드", '
            '"preconditions": [], '
            '"steps": [{"step_number": 1, "action": "Navigate to url", '
            '"expected_result": "로드 완료"}], '
            '"expected_result": "성공", "scenario_type": "positive"}'
            "]}\n"
            "```"
        )

        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="페이지 로드 테스트를 수행합니다",
        )
        assert isinstance(result, TestScenario)

    def test_불충분_요구사항_JSON_응답(self, agent_with_mock):
        """LLM이 불충분한 요구사항 응답을 반환하는 경우 처리"""
        agent, mock = agent_with_mock
        mock.return_value = (
            '{"insufficient_requirements": true, '
            '"message": "테스트 대상 기능의 상세 설명이 필요합니다"}'
        )

        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="기능 테스트를 수행합니다",
        )
        assert isinstance(result, str)
        assert "상세 설명" in result

    def test_잘못된_JSON_응답시_기본_시나리오(self, agent_with_mock):
        """잘못된 JSON 응답 시 기본 시나리오를 반환하는지 확인"""
        agent, mock = agent_with_mock
        mock.return_value = "이것은 유효하지 않은 응답입니다"

        result = agent.generate_scenario(
            target_url="https://example.com",
            requirements="로그인 기능을 테스트합니다",
        )
        assert isinstance(result, TestScenario)
        # 기본 시나리오도 긍정/부정 모두 포함해야 함
        types = {tc.scenario_type for tc in result.test_cases}
        assert "positive" in types
        assert "negative" in types
