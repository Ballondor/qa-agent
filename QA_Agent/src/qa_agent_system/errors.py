"""
에러 처리 모듈 (Error Handling Module)

QA 에이전트 시스템에서 발생하는 다양한 에러 상황을 처리하기 위한
커스텀 예외(Exception) 클래스를 정의합니다.

요구사항:
- 1.4: 에이전트 초기화 실패 시 에이전트 이름과 오류 원인 포함 에러 반환
- 1.5: Bedrock 모델 연결 실패 시 연결 실패 원인 + 재시도 안내 반환
- 2.6: 하위 에이전트 실패 시 에이전트 이름, 실패 단계, 오류 내용 포함 에러 전달
- 4.5: Playwright MCP 연결 실패 시 연결 실패 원인 포함 에러 반환, 재시도 없이 즉시 종료
"""

from typing import Optional


class QAAgentError(Exception):
    """QA 에이전트 시스템의 기본 예외 클래스

    모든 커스텀 예외의 부모 클래스로, 에이전트 이름과 원인 정보를 포함합니다.
    """

    def __init__(self, agent_name: str, cause: str, message: Optional[str] = None):
        """
        Args:
            agent_name: 에러가 발생한 에이전트 이름
            cause: 오류 원인 설명
            message: 사용자에게 표시할 에러 메시지 (없으면 자동 생성)
        """
        self.agent_name = agent_name
        self.cause = cause
        if message is None:
            message = f"[{agent_name}] {cause}"
        super().__init__(message)


class AgentInitError(QAAgentError):
    """에이전트 초기화 실패 예외

    에이전트 생성 또는 초기화 과정에서 발생하는 에러입니다.
    요구사항 1.4: 실패한 에이전트 이름과 오류 원인을 포함합니다.
    """

    def __init__(self, agent_name: str, cause: str):
        """
        Args:
            agent_name: 초기화에 실패한 에이전트 이름
            cause: 초기화 실패 원인
        """
        message = f"에이전트 초기화 실패 [{agent_name}]: {cause}"
        super().__init__(agent_name=agent_name, cause=cause, message=message)


class ModelConnectionError(QAAgentError):
    """Bedrock 모델 연결 실패 예외

    Amazon Bedrock Opus 모델과의 연결에 실패했을 때 발생하는 에러입니다.
    요구사항 1.5: 연결 실패 원인과 재시도 안내를 포함합니다.
    """

    # 재시도 안내 메시지
    RETRY_GUIDANCE = (
        "Bedrock 모델 연결을 재시도하려면 네트워크 상태와 "
        "AWS 자격 증명(credentials)을 확인한 후 다시 시도해주세요."
    )

    def __init__(self, agent_name: str, cause: str):
        """
        Args:
            agent_name: 모델 연결에 실패한 에이전트 이름
            cause: 연결 실패 원인
        """
        self.retry_guidance = self.RETRY_GUIDANCE
        message = f"Bedrock 모델 연결 실패 [{agent_name}]: {cause}. {self.RETRY_GUIDANCE}"
        super().__init__(agent_name=agent_name, cause=cause, message=message)


class PipelineError(QAAgentError):
    """오케스트레이터 파이프라인 실패 예외

    오케스트레이터가 하위 에이전트 작업 실패를 감지했을 때 발생하는 에러입니다.
    요구사항 2.6: 에이전트 이름, 실패 단계, 오류 내용을 포함합니다.
    """

    def __init__(self, agent_name: str, failed_step: str, cause: str):
        """
        Args:
            agent_name: 실패한 하위 에이전트 이름
            failed_step: 실패가 발생한 파이프라인 단계
            cause: 오류 원인 설명
        """
        self.failed_step = failed_step
        message = (
            f"파이프라인 실패 [{agent_name}] "
            f"단계 '{failed_step}': {cause}"
        )
        super().__init__(agent_name=agent_name, cause=cause, message=message)


class PlaywrightConnectionError(QAAgentError):
    """Playwright MCP 연결 실패 예외

    Playwright MCP 서버와의 연결에 실패했을 때 발생하는 에러입니다.
    요구사항 4.5: 연결 실패 원인을 포함하며, 재시도 없이 즉시 종료합니다.
    """

    def __init__(self, agent_name: str, cause: str):
        """
        Args:
            agent_name: Playwright 연결에 실패한 에이전트 이름
            cause: 연결 실패 원인
        """
        message = f"Playwright MCP 연결 실패 [{agent_name}]: {cause}"
        super().__init__(agent_name=agent_name, cause=cause, message=message)
