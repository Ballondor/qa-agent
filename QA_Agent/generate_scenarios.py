"""
유저 스토리 기반 테스트 시나리오 자동 생성 스크립트

user-stories/stories.md 파일을 파싱하여 각 Epic별로
TCScenarioAgent(LLM)를 사용해 구조화된 TestScenario를 생성합니다.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_stories(stories_path: str) -> dict[str, list[dict]]:
    """stories.md 파일을 파싱하여 Epic별 유저 스토리를 추출합니다.

    Returns:
        {"Epic A": [{"id": "US-A-0-01", "title": "...", "feature": "...", ...}, ...], ...}
    """
    content = Path(stories_path).read_text(encoding="utf-8")

    epics: dict[str, list[dict]] = {}
    current_epic = ""
    current_feature = ""
    current_story: dict | None = None
    current_ac: list[str] = []

    for line in content.split("\n"):
        # Epic 감지
        if line.startswith("## Epic"):
            current_epic = line.replace("## ", "").strip()
            if current_epic not in epics:
                epics[current_epic] = []

        # Feature 감지
        elif line.startswith("### Feature"):
            current_feature = line.replace("### ", "").strip()

        # 유저 스토리 ID 감지
        elif line.startswith("#### US-"):
            # 이전 스토리 저장
            if current_story is not None:
                current_story["acceptance_criteria"] = current_ac
                epics[current_epic].append(current_story)

            story_id = line.replace("#### ", "").split(":")[0].strip()
            story_title = ":".join(line.replace("#### ", "").split(":")[1:]).strip() if ":" in line else ""
            current_story = {
                "id": story_id,
                "title": story_title,
                "feature": current_feature,
                "epic": current_epic,
                "as_a": "",
                "i_want_to": "",
                "so_that": "",
                "priority": "",
            }
            current_ac = []

        # 유저 스토리 필드 파싱
        elif current_story is not None:
            if line.startswith("- **As a**"):
                current_story["as_a"] = line.replace("- **As a** ", "").strip()
            elif line.startswith("- **I want to**"):
                current_story["i_want_to"] = line.replace("- **I want to** ", "").strip()
            elif line.startswith("- **So that**"):
                current_story["so_that"] = line.replace("- **So that** ", "").strip()
            elif line.startswith("- **Priority**"):
                current_story["priority"] = line.replace("- **Priority**: ", "").strip()
            elif re.match(r"^\d+\.\s+Given", line):
                current_ac.append(line.strip())

    # 마지막 스토리 저장
    if current_story is not None and current_epic:
        current_story["acceptance_criteria"] = current_ac
        epics[current_epic].append(current_story)

    return epics


def story_to_requirements(story: dict) -> str:
    """단일 유저 스토리를 요구사항 텍스트로 변환합니다."""
    lines = [
        f"유저 스토리 ID: {story['id']}",
        f"기능: {story['feature']}",
        f"제목: {story['title']}",
        f"역할: {story['as_a']}",
        f"목표: {story['i_want_to']}",
        f"가치: {story['so_that']}",
        f"우선순위: {story['priority']}",
        "",
        "인수 조건 (Acceptance Criteria):",
    ]
    for ac in story.get("acceptance_criteria", []):
        lines.append(f"  {ac}")

    return "\n".join(lines)


def epic_to_requirements(epic_name: str, stories: list[dict]) -> str:
    """Epic 내 모든 유저 스토리를 하나의 요구사항 텍스트로 결합합니다."""
    sections = [f"# {epic_name}\n"]
    for story in stories:
        sections.append(story_to_requirements(story))
        sections.append("\n---\n")
    return "\n".join(sections)


def generate_with_llm(target_url: str, requirements: str, output_path: str):
    """LLM을 사용하여 테스트 시나리오를 생성합니다."""
    from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
    from qa_agent_system.models import TestScenario

    try:
        from strands import Agent
        from strands.models.bedrock import BedrockModel

        model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
        model = BedrockModel(model_id=model_id)
        strands_agent = Agent(
            model=model,
            system_prompt=(
                "당신은 QA 테스트 케이스 시나리오 작성 전문 에이전트입니다. "
                "유저 스토리와 인수 조건(Acceptance Criteria)을 분석하여 "
                "구조화된 테스트 시나리오를 생성합니다. "
                "반드시 긍정 시나리오(정상 동작 검증)와 부정 시나리오(오류 상황 검증)를 "
                "모두 포함해야 합니다. "
                "각 테스트 단계는 Playwright MCP가 실행할 수 있는 구체적인 브라우저 액션으로 기술하세요. "
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
            ),
        )
        agent = TCScenarioAgent(agent=strands_agent)
        print(f"  ✅ LLM 에이전트 연결 성공")
    except Exception as e:
        print(f"  ⚠️  LLM 연결 실패, 기본 모드로 생성: {e}")
        agent = TCScenarioAgent()

    result = agent.generate_scenario(target_url, requirements)

    if isinstance(result, TestScenario):
        agent.save_scenario_to_file(result, output_path)
        tc_count = len(result.test_cases)
        pos = sum(1 for tc in result.test_cases if tc.scenario_type == "positive")
        neg = sum(1 for tc in result.test_cases if tc.scenario_type == "negative")
        print(f"  📋 테스트 케이스 {tc_count}개 생성 (긍정: {pos}, 부정: {neg})")
        return result
    else:
        print(f"  ⚠️  시나리오 생성 실패: {result}")
        return None



def get_next_version(tc_dir: Path) -> int:
    """TC 디렉토리에서 다음 버전 번호를 반환합니다.

    scenario-v1.md, scenario-v2.md 등의 패턴에서 최대 버전을 찾아 +1 반환합니다.
    """
    existing = list(tc_dir.glob("scenario-v*.md"))
    if not existing:
        return 1
    versions = []
    for f in existing:
        match = re.search(r"scenario-v(\d+)\.md", f.name)
        if match:
            versions.append(int(match.group(1)))
    return max(versions) + 1 if versions else 1


def convert_json_scenarios_to_markdown(
    json_dir: str = "qa_scenarios",
    tc_dir: str = "TC",
):
    """기존 JSON 시나리오 파일들을 읽어 하나의 통합 MD 파일로 변환합니다.

    Args:
        json_dir: JSON 시나리오 파일이 있는 디렉토리
        tc_dir: MD 파일을 저장할 디렉토리
    """
    from qa_agent_system.agents.tc_scenario_agent import TCScenarioAgent
    from qa_agent_system.models import TestScenario

    json_path = Path(json_dir)
    tc_path = Path(tc_dir)
    tc_path.mkdir(parents=True, exist_ok=True)

    # JSON 파일 목록 (epic 순서대로)
    json_files = sorted(json_path.glob("*_scenarios.json"))
    if not json_files:
        print("❌ JSON 시나리오 파일을 찾을 수 없습니다")
        return

    agent = TCScenarioAgent()
    version = get_next_version(tc_path)

    # 통합 MD 내용 생성
    all_lines: list[str] = []
    all_lines.append("# 테스트 시나리오 문서")
    all_lines.append("")
    all_lines.append(f"> 생성일: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    all_lines.append(f"> 버전: v{version}")
    all_lines.append("")

    total_tc = 0
    epic_summaries: list[str] = []

    for jf in json_files:
        print(f"📖 로딩: {jf.name}")
        scenario = agent.load_scenario_from_file(str(jf))

        # Epic 이름 추출 (requirements 첫 줄에서)
        epic_name = "Unknown Epic"
        for line in scenario.requirements.split("\n"):
            if line.startswith("# Epic"):
                epic_name = line.replace("# ", "").strip()
                break

        tc_count = len(scenario.test_cases)
        pos = sum(1 for tc in scenario.test_cases if tc.scenario_type == "positive")
        neg = sum(1 for tc in scenario.test_cases if tc.scenario_type == "negative")
        total_tc += tc_count
        epic_summaries.append(f"| {epic_name} | {tc_count} | {pos} | {neg} |")

        # Epic 섹션 추가
        all_lines.append(f"# {epic_name}")
        all_lines.append("")
        all_lines.append(f"- **테스트 대상 URL**: {scenario.target_url}")
        all_lines.append(f"- **테스트 케이스**: {tc_count}개 (긍정: {pos}, 부정: {neg})")
        all_lines.append("")

        for tc in scenario.test_cases:
            type_tag = "✅ 긍정" if tc.scenario_type == "positive" else "❌ 부정"
            all_lines.append(f"## {tc.id}: {tc.name}")
            all_lines.append("")
            all_lines.append("| 항목 | 내용 |")
            all_lines.append("|------|------|")
            all_lines.append(f"| **시나리오 유형** | {type_tag} |")
            all_lines.append(f"| **기대 결과** | {tc.expected_result} |")
            all_lines.append("")

            if tc.preconditions:
                all_lines.append("### 사전 조건")
                all_lines.append("")
                for pre in tc.preconditions:
                    all_lines.append(f"- {pre}")
                all_lines.append("")

            all_lines.append("### 테스트 단계")
            all_lines.append("")
            all_lines.append("| # | 액션 | 기대 결과 |")
            all_lines.append("|---|------|----------|")
            for step in tc.steps:
                action = step.action.replace("|", "\\|")
                expected = step.expected_result.replace("|", "\\|")
                all_lines.append(f"| {step.step_number} | {action} | {expected} |")
            all_lines.append("")
            all_lines.append("---")
            all_lines.append("")

    # 요약 테이블을 문서 상단에 삽입
    summary_lines = [
        "## 요약",
        "",
        "| Epic | TC 수 | 긍정 | 부정 |",
        "|------|-------|------|------|",
    ]
    summary_lines.extend(epic_summaries)
    summary_lines.append(f"| **합계** | **{total_tc}** | | |")
    summary_lines.append("")
    summary_lines.append("---")
    summary_lines.append("")

    # 요약을 헤더 바로 뒤에 삽입
    header_end = 4  # 제목 + 생성일 + 버전 + 빈줄
    all_lines = all_lines[:header_end] + summary_lines + all_lines[header_end:]

    # 파일 저장
    output_file = tc_path / f"scenario-v{version}.md"
    output_file.write_text("\n".join(all_lines), encoding="utf-8")
    print(f"\n✅ MD 파일 생성 완료: {output_file}")
    print(f"   총 {total_tc}개 테스트 케이스, {len(json_files)}개 Epic")


def main():
    # 멀티 루트 워크스페이스: user-stories 디렉토리 경로 탐색
    candidate_paths = [
        "/Users/bhj/Desktop/UnicronGym/aidlc-docs/inception/user-stories/stories.md",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user-stories", "stories.md"),
        "../user-stories/stories.md",
        "user-stories/stories.md",
    ]

    stories_path = None
    for p in candidate_paths:
        if os.path.exists(p):
            stories_path = p
            break

    if stories_path is None:
        print("❌ stories.md 파일을 찾을 수 없습니다")
        sys.exit(1)

    print("=" * 60)
    print("📊 유저 스토리 기반 테스트 시나리오 자동 생성")
    print("=" * 60)

    # 1. 유저 스토리 파싱
    epics = parse_stories(stories_path)
    total_stories = sum(len(stories) for stories in epics.values())
    print(f"\n📖 파싱 완료: {len(epics)}개 Epic, {total_stories}개 유저 스토리\n")

    for epic_name, stories in epics.items():
        print(f"  • {epic_name}: {len(stories)}개 스토리")

    # 2. 출력 디렉토리 생성
    output_dir = Path("qa_scenarios")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. 가상 테스트 대상 URL (실제 URL이 없으므로 플레이스홀더)
    target_url = "https://metaj.jtbc.co.kr"

    # 4. Epic별 시나리오 생성
    print(f"\n{'=' * 60}")
    print("🔄 테스트 시나리오 생성 시작...")
    print(f"{'=' * 60}\n")

    all_results = {}

    for epic_name, stories in epics.items():
        # Epic 이름에서 파일명 생성
        epic_key = epic_name.split(":")[0].strip().replace(" ", "_").lower()
        safe_name = re.sub(r"[^a-z0-9_]", "", epic_key)
        if not safe_name:
            safe_name = f"epic_{list(epics.keys()).index(epic_name)}"

        print(f"\n📁 [{epic_name}] ({len(stories)}개 스토리)")
        print(f"   {'─' * 50}")

        # 요구사항 텍스트 생성
        requirements = epic_to_requirements(epic_name, stories)

        # 요구사항 파일 저장 (참고용)
        req_file = output_dir / f"{safe_name}_requirements.txt"
        req_file.write_text(requirements, encoding="utf-8")
        print(f"  📝 요구사항 파일: {req_file}")

        # 시나리오 생성
        output_path = str(output_dir / f"{safe_name}_scenarios.json")
        result = generate_with_llm(target_url, requirements, output_path)

        if result:
            all_results[epic_name] = {
                "stories_count": len(stories),
                "test_cases_count": len(result.test_cases),
                "output_file": output_path,
            }
            print(f"  💾 저장 완료: {output_path}")

    # 5. JSON → MD 변환
    print(f"\n{'=' * 60}")
    print("📝 Markdown 변환 시작...")
    print(f"{'=' * 60}\n")

    convert_json_scenarios_to_markdown(
        json_dir=str(output_dir),
        tc_dir="TC",
    )

    # 6. 요약 리포트
    print(f"\n{'=' * 60}")
    print("📊 생성 결과 요약")
    print(f"{'=' * 60}\n")

    total_tc = 0
    for epic_name, info in all_results.items():
        tc_count = info["test_cases_count"]
        total_tc += tc_count
        print(f"  {epic_name}")
        print(f"    스토리: {info['stories_count']}개 → 테스트 케이스: {tc_count}개")

    print(f"\n  {'─' * 40}")
    print(f"  총 유저 스토리: {total_stories}개")
    print(f"  총 테스트 케이스: {total_tc}개")
    print(f"  출력 디렉토리: {output_dir.resolve()}")
    print(f"\n{'=' * 60}")
    print("✅ 테스트 시나리오 생성 완료!")
    print(f"{'=' * 60}")



if __name__ == "__main__":
    main()
