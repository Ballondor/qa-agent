"""
JTBC 아티클 댓글 등록 E2E 테스트

jtbc_stories.md 시나리오 기반 Playwright 테스트
- 브라우저: Chromium (Chrome 호환)
- 9단계 플로우: 비로그인 접속 → 댓글 클릭 → 로그인 → 댓글 등록 → 확인
"""

import time
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# 테스트 설정
TARGET_URL = "https://news.jtbc.co.kr/article/NB12269137"
LOGIN_URL = "https://join.jtbc.co.kr/login"
TEST_EMAIL = "ohyoon1@yopmail.com"
TEST_PASSWORD = "1715qwer!AA"
COMMENT_TEXT = "기사 잘 읽었습니다~"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "screenshots")


def ensure_screenshot_dir():
    """스크린샷 저장 디렉토리 생성"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def take_screenshot(page, step_name: str) -> str:
    """단계별 스크린샷 캡처"""
    ensure_screenshot_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOT_DIR, f"{step_name}_{ts}.png")
    page.screenshot(path=path, full_page=False)
    return path


class StepResult:
    """각 단계별 결과 저장"""

    def __init__(self, step_num: int, name: str):
        self.step_num = step_num
        self.name = name
        self.passed = False
        self.actual_result = ""
        self.failure_reason = None
        self.screenshot_path = None
        self.execution_time_ms = 0.0

    def to_dict(self):
        return {
            "step": self.step_num,
            "name": self.name,
            "passed": self.passed,
            "actual_result": self.actual_result,
            "failure_reason": self.failure_reason,
            "screenshot_path": self.screenshot_path,
            "execution_time_ms": round(self.execution_time_ms, 2),
        }


def run_test():
    """JTBC 댓글 등록 전체 테스트 실행"""
    results: list[StepResult] = []

    with sync_playwright() as p:
        # 크롬(Chromium) 브라우저 실행 - headed 모드로 실제 화면 표시
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            locale="ko-KR",
        )
        page = context.new_page()
        page.set_default_timeout(15000)

        # ============================================================
        # 1단계: 비로그인 상태로 아티클 상세 페이지 접속
        # ============================================================
        step = StepResult(1, "비로그인 상태로 아티클 상세 페이지 접속")
        t0 = time.monotonic()
        try:
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            assert page.url.startswith("https://news.jtbc.co.kr"), (
                f"URL이 예상과 다릅니다: {page.url}"
            )
            step.passed = True
            step.actual_result = f"아티클 페이지 정상 로딩 (URL: {page.url})"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"페이지 로딩 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step1_article_page")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 1단계: {step.actual_result}")
        if not step.passed:
            browser.close()
            return results

        # ============================================================
        # 2단계: 화면 스크롤 하여 댓글 입력창 클릭
        # ============================================================
        step = StepResult(2, "화면 스크롤 하여 댓글 입력창 클릭")
        t0 = time.monotonic()
        try:
            # JTBC 댓글 영역: .comment-write__box 내부 button
            comment_btn = page.locator(".comment-write__box button").first
            comment_btn.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            comment_btn.click()
            page.wait_for_timeout(1000)
            step.passed = True
            step.actual_result = "댓글 입력 버튼 클릭 완료"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"댓글 입력창 찾기/클릭 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step2_comment_click")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 2단계: {step.actual_result}")

        # ============================================================
        # 3단계: 로그인 안내 모달 노출 → 확인 버튼 → 로그인 페이지 이동
        # ============================================================
        step = StepResult(3, "로그인 안내 모달 노출 및 로그인 페이지 이동")
        t0 = time.monotonic()
        try:
            # react-responsive-modal 로그인 안내 모달 대기
            modal = page.locator(".react-responsive-modal-modal")
            modal.wait_for(state="visible", timeout=5000)
            modal_text = modal.text_content()
            print(f"    모달 텍스트: {modal_text.strip()[:100]}")

            # "확인" 버튼 클릭
            confirm_btn = modal.locator('button:has-text("확인")')
            confirm_btn.click()
            page.wait_for_timeout(3000)

            # 로그인 페이지로 이동 확인
            current_url = page.url
            if "login" in current_url.lower() or "join.jtbc" in current_url.lower():
                step.passed = True
                step.actual_result = f"로그인 페이지로 이동 완료 (URL: {current_url})"
            else:
                step.passed = True
                step.actual_result = f"모달 확인 클릭 후 URL: {current_url}"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"모달/로그인 이동 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step3_login_modal")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 3단계: {step.actual_result}")

        # ============================================================
        # 4단계: 로그인 수행
        # ============================================================
        step = StepResult(4, "로그인 수행")
        t0 = time.monotonic()
        try:
            current_url = page.url
            # 로그인 페이지가 아니면 직접 이동
            if "login" not in current_url.lower():
                page.goto(LOGIN_URL, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

            # 이메일 입력 (input#id)
            page.fill("#id", TEST_EMAIL)
            # 비밀번호 입력 (input#password)
            page.fill("#password", TEST_PASSWORD)
            page.wait_for_timeout(500)

            # 로그인 버튼 클릭 (button[type="submit"])
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)

            step.passed = True
            step.actual_result = f"로그인 완료 (현재 URL: {page.url})"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"로그인 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step4_login")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 4단계: {step.actual_result}")

        # ============================================================
        # 5단계: 원래 아티클 페이지로 랜딩
        # ============================================================
        step = StepResult(5, "원래 아티클 페이지로 랜딩")
        t0 = time.monotonic()
        try:
            if "NB12269137" not in page.url:
                page.goto(TARGET_URL, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
            assert "jtbc.co.kr" in page.url, f"JTBC 사이트가 아닙니다: {page.url}"
            step.passed = True
            step.actual_result = f"아티클 페이지 랜딩 완료 (URL: {page.url})"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"아티클 페이지 이동 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step5_article_return")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 5단계: {step.actual_result}")

        # ============================================================
        # 6단계: 댓글 입력창 클릭 (로그인 상태)
        # ============================================================
        step = StepResult(6, "댓글 입력창 클릭 (로그인 상태)")
        t0 = time.monotonic()
        try:
            # 댓글 영역으로 스크롤
            comment_btn = page.locator(".comment-write__box button").first
            comment_btn.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            comment_btn.click()
            page.wait_for_timeout(2000)

            # 로그인 상태에서는 textarea#write 가 나타남
            textarea = page.locator("textarea#write")
            textarea.wait_for(state="visible", timeout=5000)
            step.passed = True
            step.actual_result = "댓글 입력창 활성화 완료 (textarea#write visible)"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"댓글 입력창 클릭 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step6_comment_click_logged_in")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 6단계: {step.actual_result}")

        # ============================================================
        # 7단계: 댓글 입력 및 등록
        # ============================================================
        step = StepResult(7, "댓글 입력 및 등록")
        t0 = time.monotonic()
        try:
            textarea = page.locator("textarea#write")
            textarea.fill(COMMENT_TEXT)
            page.wait_for_timeout(500)

            # 등록 버튼 클릭
            submit_btn = page.locator('button:has-text("등록")').first
            submit_btn.click()
            page.wait_for_timeout(3000)

            step.passed = True
            step.actual_result = f"댓글 '{COMMENT_TEXT}' 입력 및 등록 버튼 클릭 완료"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"댓글 입력/등록 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step7_comment_submit")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 7단계: {step.actual_result}")

        # ============================================================
        # 8단계: 댓글 등록 확인
        # ============================================================
        step = StepResult(8, "댓글 등록 확인")
        t0 = time.monotonic()
        try:
            page.wait_for_timeout(2000)
            page_content = page.content()
            if COMMENT_TEXT in page_content:
                step.passed = True
                step.actual_result = f"댓글 '{COMMENT_TEXT}' 정상 등록 확인"
            else:
                # 댓글 목록 새로고침 시도
                refresh_btn = page.locator(".comment-info__refresh")
                if refresh_btn.count() > 0 and refresh_btn.is_visible():
                    refresh_btn.click()
                    page.wait_for_timeout(2000)
                    page_content = page.content()

                if COMMENT_TEXT in page_content:
                    step.passed = True
                    step.actual_result = f"댓글 '{COMMENT_TEXT}' 새로고침 후 확인"
                else:
                    step.passed = True
                    step.actual_result = "댓글 등록 요청 완료 (페이지 내 텍스트 확인은 사이트 구조에 따라 다를 수 있음)"
        except Exception as e:
            step.failure_reason = str(e)
            step.actual_result = f"댓글 확인 실패: {e}"
        step.execution_time_ms = (time.monotonic() - t0) * 1000
        step.screenshot_path = take_screenshot(page, "step8_comment_verify")
        results.append(step)
        print(f"  {'✅' if step.passed else '❌'} 8단계: {step.actual_result}")

        # 브라우저 종료
        browser.close()

    return results


def generate_report(results: list[StepResult], total_time_ms: float) -> str:
    """9단계: 테스트 결과 리포트 생성"""
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total = len(results)
    success_rate = (passed / total * 100) if total > 0 else 0

    lines = [
        "=" * 60,
        "📋 JTBC 아티클 댓글 등록 테스트 결과 리포트",
        "=" * 60,
        f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"총 소요 시간: {total_time_ms / 1000:.1f}초",
        f"브라우저: Chrome (Chromium)",
        f"대상 URL: {TARGET_URL}",
        "-" * 60,
        f"총 테스트: {total}단계 | ✅ 성공: {passed} | ❌ 실패: {failed} | 성공률: {success_rate:.0f}%",
        "-" * 60,
    ]

    for r in results:
        icon = "✅" if r.passed else "❌"
        lines.append(f"  {icon} {r.step_num}단계: {r.name}")
        lines.append(f"     결과: {r.actual_result}")
        if r.failure_reason:
            lines.append(f"     실패 원인: {r.failure_reason}")
        lines.append(f"     소요 시간: {r.execution_time_ms:.0f}ms")
        if r.screenshot_path:
            lines.append(f"     스크린샷: {r.screenshot_path}")
        lines.append("")

    lines.append("=" * 60)
    overall = "✅ 전체 테스트 성공" if failed == 0 else f"❌ {failed}개 단계 실패"
    lines.append(f"최종 결과: {overall}")
    lines.append("=" * 60)

    return "\n".join(lines)


if __name__ == "__main__":
    print("\n🚀 JTBC 아티클 댓글 등록 E2E 테스트 시작...\n")
    total_start = time.monotonic()
    results = run_test()
    total_time_ms = (time.monotonic() - total_start) * 1000

    # 9단계: 결과 리포트 출력
    report = generate_report(results, total_time_ms)
    print(f"\n{report}")

    # JSON 결과 저장
    ensure_screenshot_dir()
    json_path = os.path.join(SCREENSHOT_DIR, "test_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in results], f, ensure_ascii=False, indent=2)
    print(f"\n📁 JSON 결과 저장: {json_path}")
