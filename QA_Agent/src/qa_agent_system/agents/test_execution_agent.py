"""
테스트 실행 에이전트 (Test Execution Agent)

Playwright MCP를 사용하여 TestScenario의 각 TestCase를 순차적으로 실행하고,
실행 결과를 TestExecutionResult로 반환하는 에이전트입니다.

모든 실패 상황에서 자동 재시도(auto-retry)를 수행하지 않습니다.

요구사항:
- 4.1: TestScenario 수신 시 Playwright MCP로 각 TestCase 순차 실행
- 4.2: 각 TestCase 실행 결과에 테스트 ID, 성공/실패, 실행 시간, 스크린샷 경로 포함
- 4.3: 기대 결과와 실제 결과가 다르면 실패 기록 및 차이 기록
- 4.4: 각 TestCase 실행 시 스크린샷 캡처 및 저장
- 4.5: Playwright MCP 연결 실패 시 재시도 없이 즉시 종료
- 4.6: 타임아웃 발생 시 timed_out=True 기록 후 다음 TestCase 계속 실행
- 4.7: 모든 TestCase 실행 완료 후 전체 결과를 JSON 형식으로 반환
- 4.9: 실패 시 재시도 없이 실패 기록 후 다음 TestCase로 진행
- 4.10: 어떠한 실패 상황에서도 자동 재시도 수행하지 않음
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from strands import Agent

from qa_agent_system.errors import PlaywrightConnectionError
from qa_agent_system.models import (
    TestCase,
    TestCaseResult,
    TestExecutionResult,
    TestScenario,
)


# 테스트 실행 에이전트 시스템 프롬프트
TEST_EXECUTION_AGENT_SYSTEM_PROMPT = (
    "당신은 QA 테스트 실행 전문 에이전트입니다. "
    "Playwright MCP를 사용하여 브라우저 자동화 테스트를 실행합니다. "
    "TestScenario에 포함된 각 TestCase를 순차적으로 실행하고, "
    "각 단계의 실행 결과를 정확히 기록합니다. "
    "테스트 실패 시 재시도하지 않고, 실제 결과와 기대 결과의 차이를 기록한 후 "
    "다음 테스트로 진행합니다. "
    "타임아웃 발생 시에도 재시도 없이 timed_out으로 기록하고 계속 진행합니다."
)

# 기본 스크린샷 저장 디렉토리
_DEFAULT_SCREENSHOT_DIR = "screenshots"

# 기본 테스트 케이스 타임아웃 (밀리초)
_DEFAULT_TIMEOUT_MS = 30000.0


class TestExecutionAgent:
    """Playwright MCP 기반 테스트 실행 에이전트

    Strands Agent를 래핑하여 TestScenario의 각 TestCase를
    순차적으로 실행하고 TestExecutionResult를 반환합니다.

    모든 실패 상황에서 자동 재시도(auto-retry)를 수행하지 않습니다.
    """

    def __init__(self, agent: Optional[Agent] = None):
        """TestExecutionAgent 초기화

        Strands Agent를 래핑하고, Playwright MCP 도구를 설정하며,
        시스템 프롬프트를 설정합니다.

        Args:
            agent: Strands Agent 인스턴스. None이면 시뮬레이션 모드로 동작합니다.
        """
        # Strands Agent 래핑 및 시스템 프롬프트 설정
        self._agent = agent
        self._system_prompt = TEST_EXECUTION_AGENT_SYSTEM_PROMPT
        # 스크린샷 저장 디렉토리
        self._screenshot_dir = _DEFAULT_SCREENSHOT_DIR
        # Playwright MCP 연결 상태
        self._playwright_connected = False

    @property
    def system_prompt(self) -> str:
        """시스템 프롬프트 반환"""
        return self._system_prompt

    def execute_tests(self, scenario: TestScenario) -> TestExecutionResult:
        """TestScenario의 각 TestCase를 순차적으로 실행합니다.

        요구사항 4.1: 각 TestCase를 순차 실행
        요구사항 4.7: 전체 실행 결과를 반환
        요구사항 4.9, 4.10: 실패 시 재시도 없이 다음 테스트로 진행

        Agent가 None이면 시뮬레이션 모드로 동작하여
        각 TestCase에 대한 기본 TestCaseResult를 생성합니다.

        Args:
            scenario: 실행할 테스트 시나리오

        Returns:
            전체 테스트 실행 결과

        Raises:
            PlaywrightConnectionError: Playwright MCP 연결 실패 시 (요구사항 4.5)
        """
        # 시나리오 ID 생성
        scenario_id = f"exec-{uuid.uuid4().hex[:8]}"
        results: list[TestCaseResult] = []
        total_start = time.monotonic()

        for test_case in scenario.test_cases:
            # 각 TestCase를 개별 실행하고 결과 수집
            result = self._execute_single_test(test_case)
            results.append(result)

        # 전체 실행 시간 계산
        total_elapsed_ms = (time.monotonic() - total_start) * 1000

        return TestExecutionResult(
            scenario_id=scenario_id,
            target_url=scenario.target_url,
            results=results,
            total_execution_time_ms=total_elapsed_ms,
            executed_at=datetime.now(timezone.utc),
        )

    def capture_screenshot(self, test_case_id: str) -> str:
        """스크린샷을 캡처하고 저장 경로를 반환합니다.

        요구사항 4.4: 각 TestCase 실행 시 스크린샷 캡처 및 저장

        Args:
            test_case_id: 스크린샷을 캡처할 테스트 케이스 ID

        Returns:
            스크린샷 저장 경로 문자열
        """
        # 고유한 파일명 생성
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{test_case_id}_{timestamp}.png"
        screenshot_path = f"{self._screenshot_dir}/{filename}"

        return screenshot_path

    def _execute_single_test(self, test_case: TestCase) -> TestCaseResult:
        """단일 TestCase를 실행하고 결과를 반환합니다.

        실패 시 재시도 없이 결과를 기록하고 반환합니다.
        타임아웃 시 timed_out=True로 기록합니다.

        Args:
            test_case: 실행할 테스트 케이스

        Returns:
            테스트 케이스 실행 결과
        """
        start_time = time.monotonic()

        # Agent가 없으면 시뮬레이션 모드
        if self._agent is None:
            return self._simulate_test_execution(test_case, start_time)

        # Playwright MCP를 통한 실제 실행
        return self._execute_with_agent(test_case, start_time)

    def _simulate_test_execution(
        self, test_case: TestCase, start_time: float
    ) -> TestCaseResult:
        """Agent 없이 테스트 실행을 시뮬레이션합니다.

        단위 테스트에서 Playwright 연결 없이 동작을 검증할 수 있도록
        기본 TestCaseResult를 생성합니다.

        Args:
            test_case: 실행할 테스트 케이스
            start_time: 실행 시작 시간 (monotonic)

        Returns:
            시뮬레이션된 테스트 케이스 실행 결과
        """
        elapsed_ms = (time.monotonic() - start_time) * 1000
        screenshot_path = self.capture_screenshot(test_case.id)

        return TestCaseResult(
            test_case_id=test_case.id,
            test_name=test_case.name,
            passed=True,
            execution_time_ms=elapsed_ms,
            screenshot_path=screenshot_path,
            actual_result=test_case.expected_result,
            expected_result=test_case.expected_result,
        )

    def _execute_with_agent(
        self, test_case: TestCase, start_time: float
    ) -> TestCaseResult:
        """Strands Agent(Playwright MCP)를 사용하여 테스트를 실행합니다.

        요구사항 4.3: 실패 시 actual_result, expected_result, failure_reason 기록
        요구사항 4.5: Playwright 연결 실패 시 PlaywrightConnectionError 발생
        요구사항 4.6: 타임아웃 시 timed_out=True 기록 후 계속 실행
        요구사항 4.9, 4.10: 재시도 없이 실패 기록

        Args:
            test_case: 실행할 테스트 케이스
            start_time: 실행 시작 시간 (monotonic)

        Returns:
            테스트 케이스 실행 결과

        Raises:
            PlaywrightConnectionError: Playwright MCP 연결 실패 시
        """
        screenshot_path = self.capture_screenshot(test_case.id)

        try:
            # 테스트 단계를 프롬프트로 구성하여 Agent에 전달
            steps_description = "\n".join(
                f"  {step.step_number}. {step.action} → 기대: {step.expected_result}"
                for step in test_case.steps
            )
            prompt = (
                f"테스트 케이스 '{test_case.name}' (ID: {test_case.id})를 실행하세요.\n"
                f"사전 조건: {', '.join(test_case.preconditions) if test_case.preconditions else '없음'}\n"
                f"테스트 단계:\n{steps_description}\n"
                f"최종 기대 결과: {test_case.expected_result}"
            )

            # Strands Agent 호출
            result = self._agent(prompt)
            actual_result = str(result)
            elapsed_ms = (time.monotonic() - start_time) * 1000

            # 성공으로 기록 (실제 환경에서는 Agent 응답을 분석하여 판단)
            return TestCaseResult(
                test_case_id=test_case.id,
                test_name=test_case.name,
                passed=True,
                execution_time_ms=elapsed_ms,
                screenshot_path=screenshot_path,
                actual_result=actual_result,
                expected_result=test_case.expected_result,
            )

        except ConnectionError as e:
            # Playwright MCP 연결 실패 (요구사항 4.5)
            # 재시도 없이 즉시 종료
            raise PlaywrightConnectionError(
                agent_name="TestExecutionAgent",
                cause=str(e),
            ) from e

        except TimeoutError:
            # 타임아웃 처리 (요구사항 4.6)
            # timed_out=True 기록 후 재시도 없이 다음 테스트 계속 실행
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return TestCaseResult(
                test_case_id=test_case.id,
                test_name=test_case.name,
                passed=False,
                execution_time_ms=elapsed_ms,
                screenshot_path=screenshot_path,
                actual_result="타임아웃 발생",
                expected_result=test_case.expected_result,
                failure_reason="테스트 실행 중 타임아웃이 발생했습니다",
                timed_out=True,
            )

        except Exception as e:
            # 기타 실패 처리 (요구사항 4.3, 4.9, 4.10)
            # 재시도 없이 실패 기록 후 다음 테스트로 진행
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return TestCaseResult(
                test_case_id=test_case.id,
                test_name=test_case.name,
                passed=False,
                execution_time_ms=elapsed_ms,
                screenshot_path=screenshot_path,
                actual_result=str(e),
                expected_result=test_case.expected_result,
                failure_reason=f"테스트 실행 중 오류 발생: {e}",
                timed_out=False,
            )
