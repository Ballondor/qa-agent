"""
파일 I/O 및 파싱 유닛 테스트 (File I/O & Parsing Unit Tests)

새로 추가된 파일 읽기/쓰기 메서드와 실행 결과 파싱 메서드를 검증합니다.

테스트 대상:
- TCScenarioAgent: load_requirements_from_file, save_scenario_to_file,
                   load_scenario_from_file, generate_scenario_from_file
- TestExecutionAgent: _parse_execution_result
- ReportAgent: save_report_markdown, save_report_json, save_report,
               load_report_from_file
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
from qa_agent_system.agents.test_execution_agent import TestExecutionAgent
from qa_agent_system.agents.report_agent import ReportAgent
from qa_agent_system.models import (
    TestCase,
    TestCaseResult,
    TestExecutionResult,
    TestReport,
    TestScenario,
    TestStep,
    TestSummary,
)


# ============================================================
# 공통 픽스처 (Common Fixtures)
# ============================================================


@pytest.fixture
def sample_scenario():
    """테스트용 TestScenario 생성"""
    return TestScenario(
        target_url="https://example.com",
        requirements="로그인 기능 테스트",
        test_cases=[
            TestCase(
                id="TC-001",
                name="정상 로그인",
                preconditions=["브라우저 실행"],
                steps=[
                    TestStep(
                        step_number=1,
                        action="Navigate to https://example.com/login",
                        expected_result="로그인 페이지 로드",
                    )
                ],
                expected_result="로그인 성공",
                scenario_type="positive",
            ),
            TestCase(
                id="TC-002",
                name="잘못된 비밀번호",
                preconditions=["브라우저 실행"],
                steps=[
                    TestStep(
                        step_number=1,
                        action="Fill password with invalid",
                        expected_result="에러 메시지 표시",
                    )
                ],
                expected_result="에러 메시지 표시",
                scenario_type="negative",
            ),
        ],
        created_at=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def sample_report():
    """테스트용 TestReport 생성"""
    summary = TestSummary(
        total_tests=2, passed_tests=1, failed_tests=1, success_rate=0.5
    )
    results = [
        TestCaseResult(
            test_case_id="TC-001",
            test_name="정상 로그인",
            passed=True,
            execution_time_ms=150.0,
            screenshot_path="screenshots/TC-001.png",
            actual_result="로그인 성공",
            expected_result="로그인 성공",
        ),
        TestCaseResult(
            test_case_id="TC-002",
            test_name="잘못된 비밀번호",
            passed=False,
            execution_time_ms=200.0,
            screenshot_path="screenshots/TC-002.png",
            actual_result="에러 없음",
            expected_result="에러 메시지 표시",
            failure_reason="에러 메시지가 표시되지 않음",
        ),
    ]
    report = TestReport(
        title="테스트 리포트 - https://example.com",
        summary=summary,
        detailed_results=results,
        failed_screenshots=["screenshots/TC-002.png"],
        generated_at=datetime(2025, 1, 1, 13, 0, 0, tzinfo=timezone.utc),
        markdown_content="# 테스트 리포트\n\n테스트 내용",
    )
    return report


# ============================================================
# TCScenarioAgent 파일 I/O 테스트
# ============================================================


class TestTCScenarioAgentFileIO:
    """TCScenarioAgent 파일 I/O 메서드 테스트"""

    def test_load_requirements_from_txt(self, tmp_path):
        """txt 파일에서 요구사항을 정상적으로 읽는지 확인합니다."""
        agent = TCScenarioAgent()
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("로그인 기능을 테스트합니다.", encoding="utf-8")

        result = agent.load_requirements_from_file(str(req_file))

        assert result == "로그인 기능을 테스트합니다."

    def test_load_requirements_from_md(self, tmp_path):
        """md 파일에서 요구사항을 정상적으로 읽는지 확인합니다."""
        agent = TCScenarioAgent()
        req_file = tmp_path / "requirements.md"
        content = "# 요구사항\n\n- 로그인 기능\n- 회원가입 기능"
        req_file.write_text(content, encoding="utf-8")

        result = agent.load_requirements_from_file(str(req_file))

        assert result == content

    def test_load_requirements_from_rst(self, tmp_path):
        """rst 파일에서 요구사항을 정상적으로 읽는지 확인합니다."""
        agent = TCScenarioAgent()
        req_file = tmp_path / "requirements.rst"
        req_file.write_text("요구사항 문서입니다.", encoding="utf-8")

        result = agent.load_requirements_from_file(str(req_file))

        assert result == "요구사항 문서입니다."

    def test_load_requirements_file_not_found(self):
        """존재하지 않는 파일 경로에서 FileNotFoundError가 발생하는지 확인합니다."""
        agent = TCScenarioAgent()

        with pytest.raises(FileNotFoundError, match="요구사항 파일을 찾을 수 없습니다"):
            agent.load_requirements_from_file("/nonexistent/path.txt")

    def test_load_requirements_unsupported_extension(self, tmp_path):
        """지원하지 않는 확장자에서 ValueError가 발생하는지 확인합니다."""
        agent = TCScenarioAgent()
        req_file = tmp_path / "requirements.pdf"
        req_file.write_text("내용", encoding="utf-8")

        with pytest.raises(ValueError, match="지원하지 않는 파일 형식"):
            agent.load_requirements_from_file(str(req_file))

    def test_save_scenario_to_file(self, tmp_path, sample_scenario):
        """TestScenario를 JSON 파일로 정상 저장하는지 확인합니다."""
        agent = TCScenarioAgent()
        output = tmp_path / "scenario.json"

        result_path = agent.save_scenario_to_file(sample_scenario, str(output))

        assert Path(result_path).exists()
        # 저장된 JSON을 다시 읽어서 검증
        saved_data = json.loads(output.read_text(encoding="utf-8"))
        assert saved_data["target_url"] == "https://example.com"
        assert len(saved_data["test_cases"]) == 2

    def test_save_scenario_creates_parent_dirs(self, tmp_path, sample_scenario):
        """부모 디렉토리가 없을 때 자동 생성하는지 확인합니다."""
        agent = TCScenarioAgent()
        output = tmp_path / "sub" / "dir" / "scenario.json"

        result_path = agent.save_scenario_to_file(sample_scenario, str(output))

        assert Path(result_path).exists()

    def test_save_scenario_invalid_extension(self, tmp_path, sample_scenario):
        """json이 아닌 확장자에서 ValueError가 발생하는지 확인합니다."""
        agent = TCScenarioAgent()
        output = tmp_path / "scenario.txt"

        with pytest.raises(ValueError, match=".json 형식이어야 합니다"):
            agent.save_scenario_to_file(sample_scenario, str(output))

    def test_load_scenario_from_file(self, tmp_path, sample_scenario):
        """저장된 JSON에서 TestScenario를 정상 로드하는지 확인합니다."""
        agent = TCScenarioAgent()
        output = tmp_path / "scenario.json"
        # 먼저 저장
        agent.save_scenario_to_file(sample_scenario, str(output))

        # 로드
        loaded = agent.load_scenario_from_file(str(output))

        assert loaded.target_url == sample_scenario.target_url
        assert loaded.requirements == sample_scenario.requirements
        assert len(loaded.test_cases) == len(sample_scenario.test_cases)
        assert loaded.test_cases[0].id == "TC-001"

    def test_load_scenario_file_not_found(self):
        """존재하지 않는 파일에서 FileNotFoundError가 발생하는지 확인합니다."""
        agent = TCScenarioAgent()

        with pytest.raises(FileNotFoundError, match="시나리오 파일을 찾을 수 없습니다"):
            agent.load_scenario_from_file("/nonexistent/scenario.json")

    def test_load_scenario_invalid_json(self, tmp_path):
        """잘못된 JSON에서 ValueError가 발생하는지 확인합니다."""
        agent = TCScenarioAgent()
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{invalid json", encoding="utf-8")

        with pytest.raises(ValueError):
            agent.load_scenario_from_file(str(bad_file))

    def test_load_scenario_invalid_schema(self, tmp_path):
        """스키마에 맞지 않는 JSON에서 ValueError가 발생하는지 확인합니다."""
        agent = TCScenarioAgent()
        bad_file = tmp_path / "bad_schema.json"
        bad_file.write_text('{"target_url": "x"}', encoding="utf-8")

        with pytest.raises(ValueError):
            agent.load_scenario_from_file(str(bad_file))

    def test_generate_scenario_from_file(self, tmp_path):
        """파일에서 요구사항을 읽어 시나리오를 생성하는 전체 흐름을 확인합니다."""
        agent = TCScenarioAgent()  # Agent 없이 기본 시나리오 생성
        req_file = tmp_path / "reqs.txt"
        req_file.write_text(
            "로그인 페이지에서 이메일과 비밀번호로 로그인할 수 있어야 합니다.",
            encoding="utf-8",
        )
        output = tmp_path / "output.json"

        result = agent.generate_scenario_from_file(
            "https://example.com", str(req_file), str(output)
        )

        # 시나리오가 정상 생성됨
        assert isinstance(result, TestScenario)
        assert result.target_url == "https://example.com"
        # 파일도 저장됨
        assert output.exists()

    def test_generate_scenario_from_file_no_output(self, tmp_path):
        """output_path가 None이면 파일 저장 없이 시나리오만 반환하는지 확인합니다."""
        agent = TCScenarioAgent()
        req_file = tmp_path / "reqs.txt"
        req_file.write_text(
            "회원가입 기능을 테스트합니다. 이메일 검증 포함.",
            encoding="utf-8",
        )

        result = agent.generate_scenario_from_file(
            "https://example.com", str(req_file), None
        )

        assert isinstance(result, TestScenario)

    def test_generate_scenario_from_file_insufficient(self, tmp_path):
        """요구사항이 불충분하면 문자열 메시지를 반환하는지 확인합니다."""
        agent = TCScenarioAgent()
        req_file = tmp_path / "short.txt"
        req_file.write_text("짧음", encoding="utf-8")  # 10자 미만

        result = agent.generate_scenario_from_file(
            "https://example.com", str(req_file), None
        )

        assert isinstance(result, str)
        assert "불충분" in result


# ============================================================
# TestExecutionAgent 파싱 테스트
# ============================================================


class TestExecutionAgentParsing:
    """TestExecutionAgent._parse_execution_result 메서드 테스트"""

    def setup_method(self):
        """각 테스트 전에 Agent 인스턴스 생성"""
        self.agent = TestExecutionAgent()

    def test_parse_json_passed(self):
        """JSON 형식의 성공 결과를 올바르게 파싱하는지 확인합니다."""
        response = '{"passed": true, "actual_result": "페이지 로드 성공", "failure_reason": null}'

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is True
        assert result["actual_result"] == "페이지 로드 성공"
        assert result["failure_reason"] is None

    def test_parse_json_failed(self):
        """JSON 형식의 실패 결과를 올바르게 파싱하는지 확인합니다."""
        response = '{"passed": false, "actual_result": "404 에러", "failure_reason": "페이지를 찾을 수 없음"}'

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is False
        assert result["actual_result"] == "404 에러"
        assert result["failure_reason"] == "페이지를 찾을 수 없음"

    def test_parse_json_in_code_block(self):
        """코드 블록 안의 JSON을 올바르게 파싱하는지 확인합니다."""
        response = (
            "테스트를 실행했습니다.\n\n"
            "```json\n"
            '{"passed": true, "actual_result": "성공", "failure_reason": null}\n'
            "```\n"
        )

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is True
        assert result["actual_result"] == "성공"

    def test_parse_json_embedded_in_text(self):
        """텍스트 중간에 있는 JSON을 올바르게 추출하는지 확인합니다."""
        response = (
            "브라우저에서 테스트를 실행한 결과입니다. "
            '{"passed": false, "actual_result": "버튼 없음", "failure_reason": "요소를 찾을 수 없음"} '
            "이상입니다."
        )

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is False
        assert "버튼 없음" in result["actual_result"]

    def test_parse_text_fallback_fail_keywords(self):
        """JSON 파싱 실패 시 텍스트 기반으로 실패를 감지하는지 확인합니다."""
        response = "테스트 실행 중 error가 발생했습니다. 요소를 찾을 수 없습니다."

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is False
        assert result["failure_reason"] is not None

    def test_parse_text_fallback_success(self):
        """JSON 파싱 실패 시 실패 키워드가 없으면 성공으로 판단하는지 확인합니다."""
        response = "모든 단계가 정상적으로 완료되었습니다. 페이지가 잘 로드됩니다."

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is True
        assert result["failure_reason"] is None

    def test_parse_korean_fail_keyword(self):
        """한국어 실패 키워드를 감지하는지 확인합니다."""
        response = "테스트 실행 결과 실패했습니다."

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is False

    def test_parse_timeout_keyword(self):
        """timeout 키워드를 실패로 감지하는지 확인합니다."""
        response = "The operation timed out after 30 seconds. Timeout occurred."

        result = self.agent._parse_execution_result(response)

        assert result["passed"] is False

    def test_parse_empty_response(self):
        """빈 응답을 처리하는지 확인합니다."""
        result = self.agent._parse_execution_result("")

        # 빈 문자열에는 실패 키워드가 없으므로 성공으로 판단
        assert result["passed"] is True

    def test_parse_truncates_long_actual_result(self):
        """긴 응답 텍스트가 500자로 잘리는지 확인합니다."""
        long_response = "A" * 1000

        result = self.agent._parse_execution_result(long_response)

        assert len(result["actual_result"]) == 500


# ============================================================
# ReportAgent 파일 쓰기 테스트
# ============================================================


class TestReportAgentFileIO:
    """ReportAgent 파일 쓰기 메서드 테스트"""

    def test_save_report_markdown(self, tmp_path, sample_report):
        """Markdown 리포트를 파일로 정상 저장하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "report.md"

        result_path = agent.save_report_markdown(sample_report, str(output))

        assert Path(result_path).exists()
        content = output.read_text(encoding="utf-8")
        assert content == sample_report.markdown_content

    def test_save_report_markdown_creates_dirs(self, tmp_path, sample_report):
        """부모 디렉토리가 없을 때 자동 생성하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "sub" / "dir" / "report.md"

        result_path = agent.save_report_markdown(sample_report, str(output))

        assert Path(result_path).exists()

    def test_save_report_markdown_invalid_extension(self, tmp_path, sample_report):
        """md가 아닌 확장자에서 ValueError가 발생하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "report.txt"

        with pytest.raises(ValueError, match=".md 형식이어야 합니다"):
            agent.save_report_markdown(sample_report, str(output))

    def test_save_report_json(self, tmp_path, sample_report):
        """JSON 리포트를 파일로 정상 저장하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "report.json"

        result_path = agent.save_report_json(sample_report, str(output))

        assert Path(result_path).exists()
        saved_data = json.loads(output.read_text(encoding="utf-8"))
        assert saved_data["title"] == sample_report.title
        assert saved_data["summary"]["total_tests"] == 2

    def test_save_report_json_invalid_extension(self, tmp_path, sample_report):
        """json이 아닌 확장자에서 ValueError가 발생하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "report.md"

        with pytest.raises(ValueError, match=".json 형식이어야 합니다"):
            agent.save_report_json(sample_report, str(output))

    def test_save_report_both_formats(self, tmp_path, sample_report):
        """save_report가 Markdown과 JSON 모두 저장하는지 확인합니다."""
        agent = ReportAgent()
        output_dir = tmp_path / "reports"

        result = agent.save_report(sample_report, str(output_dir))

        assert "markdown" in result
        assert "json" in result
        assert Path(result["markdown"]).exists()
        assert Path(result["json"]).exists()
        # 파일명에 타임스탬프 포함 확인
        assert "report_" in Path(result["markdown"]).name
        assert Path(result["markdown"]).suffix == ".md"
        assert Path(result["json"]).suffix == ".json"

    def test_load_report_from_file(self, tmp_path, sample_report):
        """저장된 JSON에서 TestReport를 정상 로드하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "report.json"
        agent.save_report_json(sample_report, str(output))

        loaded = ReportAgent.load_report_from_file(str(output))

        assert loaded.title == sample_report.title
        assert loaded.summary.total_tests == sample_report.summary.total_tests
        assert len(loaded.detailed_results) == len(sample_report.detailed_results)

    def test_load_report_file_not_found(self):
        """존재하지 않는 파일에서 FileNotFoundError가 발생하는지 확인합니다."""
        with pytest.raises(FileNotFoundError, match="리포트 파일을 찾을 수 없습니다"):
            ReportAgent.load_report_from_file("/nonexistent/report.json")

    def test_load_report_invalid_json(self, tmp_path):
        """잘못된 JSON에서 ValueError가 발생하는지 확인합니다."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json at all", encoding="utf-8")

        with pytest.raises(ValueError):
            ReportAgent.load_report_from_file(str(bad_file))

    def test_load_report_invalid_schema(self, tmp_path):
        """스키마에 맞지 않는 JSON에서 ValueError가 발생하는지 확인합니다."""
        bad_file = tmp_path / "bad_schema.json"
        bad_file.write_text('{"title": "test"}', encoding="utf-8")

        with pytest.raises(ValueError):
            ReportAgent.load_report_from_file(str(bad_file))

    def test_save_and_load_roundtrip(self, tmp_path, sample_report):
        """저장 후 로드하면 원본과 동일한 데이터를 복원하는지 확인합니다."""
        agent = ReportAgent()
        output = tmp_path / "roundtrip.json"
        agent.save_report_json(sample_report, str(output))

        loaded = ReportAgent.load_report_from_file(str(output))

        assert loaded.title == sample_report.title
        assert loaded.summary == sample_report.summary
        assert loaded.failed_screenshots == sample_report.failed_screenshots
        assert loaded.generated_at == sample_report.generated_at
        for orig, loaded_r in zip(
            sample_report.detailed_results, loaded.detailed_results
        ):
            assert orig.test_case_id == loaded_r.test_case_id
            assert orig.passed == loaded_r.passed
