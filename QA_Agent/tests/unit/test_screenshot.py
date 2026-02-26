"""
스크린샷 캡처 단위 테스트 (Screenshot Capture Unit Tests)

TestExecutionAgent.capture_screenshot()이 올바른 경로를 반환하는지 검증합니다.

요구사항: 4.4 - 각 TestCase 실행 시 브라우저 스크린샷을 캡처하여 저장한다
"""

import pytest

from qa_agent_system.agents.test_execution_agent import TestExecutionAgent


class TestCaptureScreenshot:
    """TestExecutionAgent.capture_screenshot() 경로 검증 테스트

    요구사항 4.4: 각 TestCase 실행 시 스크린샷 캡처 및 저장 경로 확인
    """

    @pytest.fixture()
    def agent(self):
        """Agent 없이 TestExecutionAgent 인스턴스 생성"""
        return TestExecutionAgent()

    def test_반환값이_비공백_문자열(self, agent):
        """capture_screenshot()이 비어있지 않은 문자열을 반환하는지 확인"""
        path = agent.capture_screenshot("TC-001")
        assert isinstance(path, str)
        assert len(path) > 0

    def test_경로에_테스트_케이스_ID_포함(self, agent):
        """반환된 경로에 test_case_id가 포함되는지 확인"""
        test_case_id = "TC-042"
        path = agent.capture_screenshot(test_case_id)
        assert test_case_id in path

    def test_경로가_png_확장자로_끝남(self, agent):
        """반환된 경로가 .png 확장자로 끝나는지 확인"""
        path = agent.capture_screenshot("TC-001")
        assert path.endswith(".png")

    def test_경로가_스크린샷_디렉토리로_시작(self, agent):
        """반환된 경로가 screenshots 디렉토리로 시작하는지 확인"""
        path = agent.capture_screenshot("TC-001")
        assert path.startswith("screenshots/")

    def test_다른_ID로_호출하면_다른_경로_반환(self, agent):
        """서로 다른 test_case_id로 호출하면 다른 경로를 반환하는지 확인"""
        path_a = agent.capture_screenshot("TC-001")
        path_b = agent.capture_screenshot("TC-002")
        assert path_a != path_b
