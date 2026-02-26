"""
TC 시나리오 작성 에이전트 (TC Scenario Agent)

테스트 대상 URL과 요구사항을 기반으로 구조화된 TestScenario를 생성하는 에이전트입니다.
긍정(positive) 및 부정(negative) 시나리오를 모두 포함하며,
각 테스트 단계를 Playwright MCP가 실행 가능한 형태로 기술합니다.

요구사항:
- 3.1: 테스트 대상 URL과 요구사항 수신 시 구조화된 TestScenario 생성
- 3.2: 각 TestCase에 고유 ID, 이름, 사전 조건, 테스트 단계, 기대 결과 포함
- 3.3: 긍정 시나리오와 부정 시나리오 모두 포함
- 3.4: JSON 형식으로 출력
- 3.6: 불충분한 요구사항 시 추가 정보 요청 메시지 반환
- 3.7: Playwright MCP 실행 가능한 테스트 단계 기술
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from strands import Agent

from qa_agent_system.models import TestCase, TestScenario, TestStep


# TC 시나리오 에이전트 시스템 프롬프트
TC_SCENARIO_AGENT_SYSTEM_PROMPT = (
    "당신은 QA 테스트 케이스 시나리오 작성 전문 에이전트입니다. "
    "테스트 대상 URL과 요구사항을 분석하여 구조화된 테스트 시나리오를 생성합니다. "
    "반드시 긍정 시나리오(정상 동작 검증)와 부정 시나리오(오류 상황 검증)를 "
    "모두 포함해야 합니다. "
    "각 테스트 단계는 Playwright MCP가 실행할 수 있는 구체적인 브라우저 액션으로 기술하세요. "
    "예: 'Navigate to {url}', 'Click on element with selector #submit-btn', "
    "'Fill input[name=email] with test@example.com', "
    "'Assert that element .success-message is visible'. "
    "응답은 반드시 아래 JSON 형식으로 출력하세요:\n"
    "{\n"
    '  "test_cases": [\n'
    "    {\n"
    '      "id": "TC-001",\n'
    '      "name": "테스트 이름",\n'
    '      "preconditions": ["사전 조건"],\n'
    '      "steps": [\n'
    '        {"step_number": 1, "action": "Playwright MCP 액션", "expected_result": "기대 결과"}\n'
    "      ],\n"
    '      "expected_result": "최종 기대 결과",\n'
    '      "scenario_type": "positive 또는 negative"\n'
    "    }\n"
    "  ]\n"
    "}\n"
    "요구사항이 불충분하여 테스트 시나리오를 작성할 수 없는 경우, "
    "다음 JSON 형식으로 추가 정보 요청 메시지를 반환하세요:\n"
    '{"insufficient_requirements": true, "message": "추가 정보가 필요한 항목 설명"}'
)


# 요구사항 불충분 판단 기준 최소 길이
_MIN_REQUIREMENTS_LENGTH = 10


class TCScenarioAgent:
    """테스트 케이스 시나리오 작성 에이전트

    Strands Agent를 래핑하여 테스트 대상 URL과 요구사항으로부터
    구조화된 TestScenario를 생성합니다.
    """

    def __init__(self, agent: Optional[Agent] = None):
        """TCScenarioAgent 초기화

        Args:
            agent: Strands Agent 인스턴스. None이면 LLM 없이 동작합니다.
        """
        # Strands Agent 래핑 및 시스템 프롬프트 설정
        self._agent = agent
        self._system_prompt = TC_SCENARIO_AGENT_SYSTEM_PROMPT

    @property
    def system_prompt(self) -> str:
        """시스템 프롬프트 반환"""
        return self._system_prompt

    def generate_scenario(
        self, target_url: str, requirements: str
    ) -> Union[TestScenario, str]:
        """테스트 대상 URL과 요구사항으로부터 TestScenario를 생성합니다.

        요구사항 3.1: 구조화된 TestScenario 생성
        요구사항 3.3: 긍정/부정 시나리오 모두 포함
        요구사항 3.6: 불충분한 요구사항 시 추가 정보 요청 메시지 반환
        요구사항 3.7: Playwright MCP 실행 가능한 테스트 단계

        Args:
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항 설명

        Returns:
            TestScenario 또는 추가 정보 요청 메시지 문자열
        """
        # 요구사항 불충분 여부 확인 (요구사항 3.6)
        if self._is_insufficient_requirements(requirements):
            return (
                "테스트 시나리오를 생성하기 위한 요구사항이 불충분합니다. "
                "다음 정보를 추가로 제공해주세요: "
                "테스트 대상 기능 설명, 예상 사용자 흐름, 입력/출력 조건"
            )

        # Strands Agent가 없으면 LLM 호출 불가
        if self._agent is None:
            return self._generate_default_scenario(target_url, requirements)

        # LLM을 통한 시나리오 생성
        return self._generate_with_agent(target_url, requirements)

    def _is_insufficient_requirements(self, requirements: str) -> bool:
        """요구사항이 불충분한지 판단합니다.

        요구사항 3.6: 불충분한 요구사항 감지

        Args:
            requirements: 테스트 요구사항 문자열

        Returns:
            불충분하면 True
        """
        stripped = requirements.strip()
        return len(stripped) < _MIN_REQUIREMENTS_LENGTH

    def _generate_with_agent(
        self, target_url: str, requirements: str
    ) -> Union[TestScenario, str]:
        """Strands Agent(LLM)를 사용하여 시나리오를 생성합니다.

        Args:
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항

        Returns:
            TestScenario 또는 추가 정보 요청 메시지 문자열
        """
        # LLM에 전달할 프롬프트 구성
        prompt = (
            f"테스트 대상 URL: {target_url}\n"
            f"테스트 요구사항:\n{requirements}\n\n"
            "위 정보를 바탕으로 테스트 시나리오를 JSON 형식으로 생성해주세요. "
            "긍정 시나리오와 부정 시나리오를 모두 포함해야 합니다."
        )

        # Strands Agent 호출
        result = self._agent(prompt)

        # LLM 응답 파싱
        response_text = str(result)
        return self._parse_agent_response(response_text, target_url, requirements)

    def _parse_agent_response(
        self, response_text: str, target_url: str, requirements: str
    ) -> Union[TestScenario, str]:
        """LLM 응답을 파싱하여 TestScenario 또는 메시지를 반환합니다.

        Args:
            response_text: LLM 응답 텍스트
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항

        Returns:
            TestScenario 또는 추가 정보 요청 메시지 문자열
        """
        # JSON 블록 추출 (코드 블록 또는 순수 JSON)
        json_str = self._extract_json(response_text)

        try:
            data = json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            # JSON 파싱 실패 시 기본 시나리오 반환
            return self._generate_default_scenario(target_url, requirements)

        # 불충분한 요구사항 응답 처리 (요구사항 3.6)
        if data.get("insufficient_requirements"):
            return data.get(
                "message",
                "추가 정보가 필요합니다. 테스트 대상 기능과 예상 동작을 상세히 기술해주세요.",
            )

        # test_cases 파싱
        test_cases_data = data.get("test_cases", [])
        if not test_cases_data:
            return self._generate_default_scenario(target_url, requirements)

        test_cases = self._parse_test_cases(test_cases_data)

        # 긍정/부정 시나리오 양면성 보장 (요구사항 3.3)
        test_cases = self._ensure_dual_coverage(test_cases, target_url)

        return TestScenario(
            target_url=target_url,
            requirements=requirements,
            test_cases=test_cases,
            created_at=datetime.now(timezone.utc),
        )

    def _extract_json(self, text: str) -> str:
        """텍스트에서 JSON 문자열을 추출합니다.

        코드 블록(```json ... ```) 또는 중괄호로 감싸진 JSON을 추출합니다.

        Args:
            text: LLM 응답 텍스트

        Returns:
            추출된 JSON 문자열
        """
        # 코드 블록에서 JSON 추출
        if "```json" in text:
            start = text.index("```json") + len("```json")
            end = text.index("```", start)
            return text[start:end].strip()

        if "```" in text:
            start = text.index("```") + len("```")
            end = text.index("```", start)
            return text[start:end].strip()

        # 중괄호로 감싸진 JSON 추출
        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            return text[first_brace : last_brace + 1]

        return text.strip()

    def _parse_test_cases(self, test_cases_data: list[dict]) -> list[TestCase]:
        """JSON 데이터에서 TestCase 목록을 파싱합니다.

        Args:
            test_cases_data: 테스트 케이스 딕셔너리 목록

        Returns:
            파싱된 TestCase 목록
        """
        test_cases: list[TestCase] = []

        for tc_data in test_cases_data:
            try:
                # 테스트 단계 파싱
                steps_data = tc_data.get("steps", [])
                steps = [
                    TestStep(
                        step_number=s.get("step_number", idx + 1),
                        action=s.get("action", ""),
                        expected_result=s.get("expected_result", ""),
                    )
                    for idx, s in enumerate(steps_data)
                ]

                # 유효한 단계가 없으면 건너뜀
                if not steps:
                    continue

                test_case = TestCase(
                    id=tc_data.get("id", f"TC-{len(test_cases) + 1:03d}"),
                    name=tc_data.get("name", ""),
                    preconditions=tc_data.get("preconditions", []),
                    steps=steps,
                    expected_result=tc_data.get("expected_result", ""),
                    scenario_type=tc_data.get("scenario_type", "positive"),
                )
                test_cases.append(test_case)
            except (ValueError, TypeError):
                # 개별 테스트 케이스 파싱 실패 시 건너뜀
                continue

        return test_cases

    def _ensure_dual_coverage(
        self, test_cases: list[TestCase], target_url: str
    ) -> list[TestCase]:
        """긍정/부정 시나리오가 모두 포함되도록 보장합니다.

        요구사항 3.3: 긍정 시나리오와 부정 시나리오 모두 포함

        Args:
            test_cases: 현재 테스트 케이스 목록
            target_url: 테스트 대상 URL

        Returns:
            양면성이 보장된 테스트 케이스 목록
        """
        has_positive = any(tc.scenario_type == "positive" for tc in test_cases)
        has_negative = any(tc.scenario_type == "negative" for tc in test_cases)

        if not has_positive:
            # 긍정 시나리오 추가
            test_cases.append(
                TestCase(
                    id=f"TC-{len(test_cases) + 1:03d}",
                    name="기본 페이지 접근 확인",
                    preconditions=["브라우저가 실행 중이어야 합니다"],
                    steps=[
                        TestStep(
                            step_number=1,
                            action=f"Navigate to {target_url}",
                            expected_result="페이지가 정상적으로 로드됩니다",
                        )
                    ],
                    expected_result="페이지가 정상적으로 로드되고 주요 요소가 표시됩니다",
                    scenario_type="positive",
                )
            )

        if not has_negative:
            # 부정 시나리오 추가
            test_cases.append(
                TestCase(
                    id=f"TC-{len(test_cases) + 1:03d}",
                    name="잘못된 입력 처리 확인",
                    preconditions=["브라우저가 실행 중이어야 합니다"],
                    steps=[
                        TestStep(
                            step_number=1,
                            action=f"Navigate to {target_url}",
                            expected_result="페이지가 로드됩니다",
                        ),
                        TestStep(
                            step_number=2,
                            action="Fill input fields with invalid data",
                            expected_result="에러 메시지가 표시됩니다",
                        ),
                    ],
                    expected_result="적절한 에러 메시지가 표시되고 시스템이 안정적으로 동작합니다",
                    scenario_type="negative",
                )
            )

        return test_cases

    def _generate_default_scenario(
        self, target_url: str, requirements: str
    ) -> TestScenario:
        """LLM 없이 기본 테스트 시나리오를 생성합니다.

        Agent가 없거나 LLM 응답 파싱에 실패한 경우 사용됩니다.
        요구사항 3.3: 긍정/부정 시나리오 모두 포함

        Args:
            target_url: 테스트 대상 URL
            requirements: 테스트 요구사항

        Returns:
            기본 TestScenario
        """
        test_cases = [
            # 긍정 시나리오: 기본 페이지 접근
            TestCase(
                id="TC-001",
                name="기본 페이지 접근 및 로드 확인",
                preconditions=["브라우저가 실행 중이어야 합니다"],
                steps=[
                    TestStep(
                        step_number=1,
                        action=f"Navigate to {target_url}",
                        expected_result="페이지가 정상적으로 로드됩니다",
                    ),
                    TestStep(
                        step_number=2,
                        action="Assert that page title is not empty",
                        expected_result="페이지 제목이 존재합니다",
                    ),
                ],
                expected_result="페이지가 정상적으로 로드되고 제목이 표시됩니다",
                scenario_type="positive",
            ),
            # 부정 시나리오: 잘못된 입력 처리
            TestCase(
                id="TC-002",
                name="잘못된 입력에 대한 에러 처리 확인",
                preconditions=["브라우저가 실행 중이어야 합니다"],
                steps=[
                    TestStep(
                        step_number=1,
                        action=f"Navigate to {target_url}",
                        expected_result="페이지가 로드됩니다",
                    ),
                    TestStep(
                        step_number=2,
                        action="Fill input fields with invalid data",
                        expected_result="에러 메시지가 표시됩니다",
                    ),
                ],
                expected_result="적절한 에러 메시지가 표시되고 시스템이 안정적으로 동작합니다",
                scenario_type="negative",
            ),
        ]

        return TestScenario(
            target_url=target_url,
            requirements=requirements,
            test_cases=test_cases,
            created_at=datetime.now(timezone.utc),
        )
