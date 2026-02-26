"""
데이터 검증기 모듈 (Data Validator Module)

에이전트 간 전달되는 JSON 데이터를 Pydantic 스키마로 검증합니다.

요구사항: 6.2, 6.3
- 6.2: 에이전트 간 전달되는 모든 데이터에 대해 스키마 검증 수행
- 6.3: 검증 실패 시 실패 항목과 원인을 포함한 에러 메시지 반환
"""

from pydantic import BaseModel, ValidationError

from qa_agent_system.models import ValidationResult


class DataValidator:
    """에이전트 간 데이터 스키마 검증기

    JSON 데이터(dict)를 Pydantic 모델 스키마로 검증하여
    유효성 여부와 상세 에러 정보를 반환합니다.
    """

    @staticmethod
    def validate(data: dict, schema_class: type[BaseModel]) -> ValidationResult:
        """JSON 데이터를 Pydantic 스키마로 검증합니다.

        Args:
            data: 검증할 JSON 데이터 (dict 형태)
            schema_class: 검증에 사용할 Pydantic 모델 클래스

        Returns:
            ValidationResult: 검증 결과 (is_valid, errors)
                - 성공 시: is_valid=True, errors=[]
                - 실패 시: is_valid=False, errors=[실패 항목과 원인 목록]
        """
        try:
            # Pydantic 모델로 데이터 검증 시도
            schema_class.model_validate(data)
            return ValidationResult(is_valid=True, errors=[])
        except ValidationError as e:
            # 검증 실패 시 각 에러의 위치와 원인을 수집
            error_messages = []
            for error in e.errors():
                # 에러 발생 필드 경로 (예: "steps.0.action")
                field_path = " -> ".join(str(loc) for loc in error["loc"])
                # 에러 메시지 (예: "String should have at least 1 character")
                message = error["msg"]
                # 에러 유형 (예: "string_too_short")
                error_type = error["type"]
                error_messages.append(
                    f"필드 '{field_path}': {message} (유형: {error_type})"
                )
            return ValidationResult(is_valid=False, errors=error_messages)
