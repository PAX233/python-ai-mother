from collections.abc import AsyncIterator

from app.ai.openai_compatible_service import OpenAICompatibleService
from app.core.code_file_saver import CodeFileSaverExecutor
from app.core.code_parser import CodeParserExecutor
from app.core.config import Settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException
from app.core.prompt_loader import load_prompt

CODE_GEN_TYPE_HTML = "html"
CODE_GEN_TYPE_MULTI_FILE = "multi_file"


class AiCodeGeneratorFacade:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.ai_service = OpenAICompatibleService(settings)
        self.parser_executor = CodeParserExecutor()
        self.saver_executor = CodeFileSaverExecutor()

    async def generate_and_save_code_stream(
        self,
        app_id: int,
        user_message: str,
        code_gen_type: str,
    ) -> AsyncIterator[str]:
        prompt_name = self._resolve_prompt_name(code_gen_type)
        system_prompt = load_prompt(prompt_name)

        chunks: list[str] = []
        async for chunk in self.ai_service.generate_stream(system_prompt=system_prompt, user_prompt=user_message):
            chunks.append(chunk)
            yield chunk

        final_text = "".join(chunks).strip()
        if not final_text:
            raise BusinessException(ErrorCode.SYSTEM_ERROR, "LLM empty response")

        parsed_code = self.parser_executor.parse(code_gen_type=code_gen_type, raw_text=final_text)
        self.saver_executor.save(
            code_gen_type=code_gen_type,
            app_id=app_id,
            parsed_code=parsed_code,
            settings=self.settings,
        )

    @staticmethod
    def _resolve_prompt_name(code_gen_type: str) -> str:
        if code_gen_type == CODE_GEN_TYPE_HTML:
            return "codegen-html-system-prompt.txt"
        if code_gen_type == CODE_GEN_TYPE_MULTI_FILE:
            return "codegen-multi-file-system-prompt.txt"
        raise BusinessException(ErrorCode.PARAMS_ERROR, f"Unsupported code_gen_type: {code_gen_type}")
