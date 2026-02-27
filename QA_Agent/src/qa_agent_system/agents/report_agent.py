"""
리포트 생성 에이전트 (Report Agent)

테스트 실행 결과를 분석하여 구조화된 TestReport를 생성하고,
Markdown 형식으로 포맷팅하는 에이전트입니다.

요구사항:
- 5.1: 테스트 실행 결과 수신 시 구조화된 TestReport 생성
- 5.2: 전체 테스트 요약 (총 테스트 수, 성공 수, 실패 수, 성공률) 포함
- 5.3: 각 TestCase별 상세 결과 포함
- 5.4: 실패한 TestCase의 스크린샷 참조 포함
- 5.5: Markdown 형식 출력
- 5.7: 빈 실행 결과에 대한 "실행 결과 없음" 리포트 생성
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from strands import Agent

from qa_agent_system.models import (
    TestCaseResult,
    TestExecutionResult,
    TestReport,
    TestSummary,
)


# 리포트 에이전트 시스템 프롬프트
REPORT_AGENT_SYSTEM_PROMPT = (
    "당신은 QA 테스트 결과 리포트 생성 전문 에이전트입니다. "
    "테스트 실행 결과를 분석하여 명확하고 구조화된 리포트를 생성합니다. "
    "리포트에는 전체 요약 통계, 각 테스트 케이스별 상세 결과, "
    "실패한 테스트의 스크린샷 참조를 포함해야 합니다."
)


class ReportAgent:
    """테스트 결과 리포트 생성 에이전트

    Strands Agent를 래핑하여 TestExecutionResult로부터
    구조화된 TestReport를 생성하고 Markdown으로 포맷팅합니다.
    """

    def __init__(self, agent: Optional[Agent] = None):
        """ReportAgent 초기화

        Args:
            agent: Strands Agent 인스턴스. None이면 기본 설정으로 생성합니다.
        """
        # Strands Agent 래핑 및 시스템 프롬프트 설정
        self._agent = agent
        self._system_prompt = REPORT_AGENT_SYSTEM_PROMPT

    @property
    def system_prompt(self) -> str:
        """시스템 프롬프트 반환"""
        return self._system_prompt

    def generate_report(self, execution_result: TestExecutionResult) -> TestReport:
        """TestExecutionResult로부터 TestReport를 생성합니다.

        요구사항 5.1: 구조화된 TestReport 생성
        요구사항 5.7: 빈 실행 결과 시 "실행 결과 없음" 리포트 생성

        Args:
            execution_result: 테스트 실행 결과

        Returns:
            생성된 TestReport
        """
        results = execution_result.results

        # 빈 실행 결과 처리 (요구사항 5.7)
        if not results:
            return self._generate_empty_report(execution_result)

        # 요약 통계 계산 (요구사항 5.2)
        summary = self._compute_summary(results)

        # 실패 스크린샷 경로 수집 (요구사항 5.4)
        failed_screenshots = self._collect_failed_screenshots(results)

        # 리포트 제목 생성
        title = f"테스트 리포트 - {execution_result.target_url}"

        # 리포트 생성 시간
        generated_at = datetime.now(timezone.utc)

        # TestReport 생성 (markdown_content는 빈 문자열로 초기화)
        report = TestReport(
            title=title,
            summary=summary,
            detailed_results=list(results),
            failed_screenshots=failed_screenshots,
            generated_at=generated_at,
            markdown_content="",
        )

        # Markdown 포맷팅 후 markdown_content 설정 (요구사항 5.5)
        markdown = self.format_markdown(report)
        report = report.model_copy(update={"markdown_content": markdown})

        return report

    def format_markdown(self, report: TestReport) -> str:
        """TestReport를 Markdown 형식으로 포맷팅합니다.

        요구사항 5.5: Markdown 형식 출력
        요구사항 5.6: 라운드트립 가능한 결정론적 형식

        형식은 파싱하여 원본 데이터를 복원할 수 있도록
        구조화된 키-값 쌍과 테이블을 사용합니다.

        Args:
            report: 포맷팅할 TestReport

        Returns:
            Markdown 형식 문자열
        """
        lines: list[str] = []

        # 제목 (H1)
        lines.append(f"# {report.title}")
        lines.append("")

        # 요약 섹션 (H2)
        lines.append("## 요약")
        lines.append("")
        lines.append(f"- total_tests: {report.summary.total_tests}")
        lines.append(f"- passed_tests: {report.summary.passed_tests}")
        lines.append(f"- failed_tests: {report.summary.failed_tests}")
        lines.append(f"- success_rate: {report.summary.success_rate}")
        lines.append("")

        # 생성 시간
        lines.append(f"- generated_at: {report.generated_at.isoformat()}")
        lines.append("")

        # 상세 결과 섹션 (H2) - 테이블 형식 (요구사항 5.3)
        lines.append("## 상세 결과")
        lines.append("")

        if report.detailed_results:
            # 테이블 헤더
            lines.append(
                "| test_case_id | test_name | passed | execution_time_ms "
                "| screenshot_path | actual_result | expected_result "
                "| failure_reason | timed_out |"
            )
            lines.append(
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
            )

            # 테이블 행 - 각 TestCaseResult
            for r in report.detailed_results:
                # None 값은 빈 문자열로 표시, 파이프 문자 이스케이프
                screenshot = _escape_pipe(r.screenshot_path or "")
                actual = _escape_pipe(r.actual_result or "")
                expected = _escape_pipe(r.expected_result or "")
                failure = _escape_pipe(r.failure_reason or "")
                test_name = _escape_pipe(r.test_name)
                test_id = _escape_pipe(r.test_case_id)

                lines.append(
                    f"| {test_id} | {test_name} | {r.passed} "
                    f"| {r.execution_time_ms} | {screenshot} "
                    f"| {actual} | {expected} "
                    f"| {failure} | {r.timed_out} |"
                )
        else:
            lines.append("실행 결과 없음")

        lines.append("")

        # 실패 스크린샷 섹션 (H2) (요구사항 5.4)
        lines.append("## 실패 스크린샷")
        lines.append("")

        if report.failed_screenshots:
            for path in report.failed_screenshots:
                lines.append(f"- {path}")
        else:
            lines.append("없음")

        lines.append("")

        return "\n".join(lines)

    def _generate_empty_report(
        self, execution_result: TestExecutionResult
    ) -> TestReport:
        """빈 실행 결과에 대한 리포트를 생성합니다.

        요구사항 5.7: "실행 결과 없음" 리포트 생성

        Args:
            execution_result: 빈 실행 결과

        Returns:
            "실행 결과 없음" 리포트
        """
        title = f"테스트 리포트 - {execution_result.target_url}"
        summary = TestSummary(
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            success_rate=0.0,
        )
        generated_at = datetime.now(timezone.utc)

        report = TestReport(
            title=title,
            summary=summary,
            detailed_results=[],
            failed_screenshots=[],
            generated_at=generated_at,
            markdown_content="",
        )

        markdown = self.format_markdown(report)
        report = report.model_copy(update={"markdown_content": markdown})

        return report

    def _compute_summary(self, results: list[TestCaseResult]) -> TestSummary:
        """TestCaseResult 목록으로부터 TestSummary 통계를 계산합니다.

        요구사항 5.2: total_tests, passed_tests, failed_tests, success_rate 계산

        Args:
            results: 테스트 케이스 실행 결과 목록

        Returns:
            계산된 TestSummary
        """
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total - passed

        # 0으로 나누기 방지
        success_rate = passed / total if total > 0 else 0.0

        return TestSummary(
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            success_rate=success_rate,
        )

    def _collect_failed_screenshots(
        self, results: list[TestCaseResult]
    ) -> list[str]:
        """실패한 테스트 케이스의 스크린샷 경로를 수집합니다.

        요구사항 5.4: 실패한 TestCase의 스크린샷 참조 포함

        Args:
            results: 테스트 케이스 실행 결과 목록

        Returns:
            실패한 테스트의 스크린샷 경로 목록
        """
        return [
            r.screenshot_path
            for r in results
            if not r.passed and r.screenshot_path is not None
        ]

    # ============================================================
    # 파일 쓰기 메서드 (File Write Methods)
    # ============================================================

    def save_report_markdown(self, report: TestReport, output_path: str) -> str:
        """TestReport의 Markdown 내용을 파일로 저장합니다.

        Args:
            report: 저장할 테스트 리포트
            output_path: 저장할 파일 경로 (.md)

        Returns:
            저장된 파일의 절대 경로

        Raises:
            ValueError: .md 확장자가 아닐 때
        """
        path = Path(output_path)

        if path.suffix.lower() != ".md":
            raise ValueError(
                f"Markdown 리포트 파일은 .md 형식이어야 합니다. 입력값: {path.suffix}"
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report.markdown_content, encoding="utf-8")

        return str(path.resolve())

    def save_report_json(self, report: TestReport, output_path: str) -> str:
        """TestReport를 JSON 파일로 저장합니다.

        Pydantic 모델을 JSON으로 직렬화하여 저장합니다.
        나중에 로드하여 TestReport 객체로 복원할 수 있습니다.

        Args:
            report: 저장할 테스트 리포트
            output_path: 저장할 파일 경로 (.json)

        Returns:
            저장된 파일의 절대 경로

        Raises:
            ValueError: .json 확장자가 아닐 때
        """
        path = Path(output_path)

        if path.suffix.lower() != ".json":
            raise ValueError(
                f"JSON 리포트 파일은 .json 형식이어야 합니다. 입력값: {path.suffix}"
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        json_data = report.model_dump_json(indent=2)
        path.write_text(json_data, encoding="utf-8")

        return str(path.resolve())

    def save_report(
        self,
        report: TestReport,
        output_dir: str = "reports",
    ) -> dict[str, str]:
        """TestReport를 Markdown과 JSON 파일 모두로 저장합니다.

        타임스탬프 기반 파일명을 자동 생성하여 output_dir에 저장합니다.

        Args:
            report: 저장할 테스트 리포트
            output_dir: 저장 디렉토리 경로 (기본값: "reports")

        Returns:
            {"markdown": 절대경로, "json": 절대경로} 딕셔너리
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        dir_path = Path(output_dir)
        dir_path.mkdir(parents=True, exist_ok=True)

        md_path = self.save_report_markdown(
            report, str(dir_path / f"report_{timestamp}.md")
        )
        json_path = self.save_report_json(
            report, str(dir_path / f"report_{timestamp}.json")
        )

        return {"markdown": md_path, "json": json_path}

    @staticmethod
    def load_report_from_file(file_path: str) -> TestReport:
        """JSON 파일에서 TestReport를 로드합니다.

        Args:
            file_path: 리포트 JSON 파일 경로

        Returns:
            로드된 TestReport 객체

        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            ValueError: JSON 파싱 또는 스키마 검증 실패 시
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"리포트 파일을 찾을 수 없습니다: {file_path}")

        try:
            json_text = path.read_text(encoding="utf-8")
            return TestReport.model_validate_json(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {e}") from e
        except Exception as e:
            raise ValueError(f"리포트 스키마 검증 실패: {e}") from e


def _escape_pipe(text: str) -> str:
    """Markdown 테이블 내 파이프(|) 문자를 이스케이프합니다.

    Args:
        text: 이스케이프할 문자열

    Returns:
        파이프 문자가 이스케이프된 문자열
    """
    return text.replace("|", "\\|")
