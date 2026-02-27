"""
QA 에이전트 시스템 메인 실행 스크립트

uv run으로 실행할 수 있는 진입점(entrypoint)입니다.
"""

from qa_agent_system.system import QAAgentSystem


def main():
    """QA 에이전트 시스템을 초기화하고 실행합니다."""
    print("=" * 60)
    print("QA 에이전트 시스템 시작")
    print("=" * 60)

    try:
        # 시스템 초기화 (4개 에이전트 생성)
        print("\n[1/2] 시스템 초기화 중...")
        system = QAAgentSystem()
        print("  ✅ 4개 에이전트 초기화 완료")
        print(f"  📋 모델: {system.model_id}")

        # 테스트 실행
        target_url = "https://example.com"
        requirements = (
            "메인 페이지 로드 확인, "
            "페이지 제목 표시 확인, "
            "잘못된 입력에 대한 에러 처리 확인"
        )

        print(f"\n[2/2] QA 프로세스 실행 중...")
        print(f"  🌐 대상 URL: {target_url}")
        print(f"  📝 요구사항: {requirements}")

        report = system.run(target_url=target_url, requirements=requirements)

        # 결과 출력
        print("\n" + "=" * 60)
        print("✅ QA 프로세스 완료")
        print("=" * 60)
        print(f"\n📊 테스트 요약:")
        print(f"  - 총 테스트: {report.summary.total_tests}")
        print(f"  - 성공: {report.summary.passed_tests}")
        print(f"  - 실패: {report.summary.failed_tests}")
        print(f"  - 성공률: {report.summary.success_rate:.1%}")
        print(f"\n📄 Markdown 리포트:\n")
        print(report.markdown_content)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    main()
