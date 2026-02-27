from pathlib import Path
from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.config import Settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException

CODE_GEN_TYPE_HTML = "html"
CODE_GEN_TYPE_MULTI_FILE = "multi_file"


class CodeFileSaver(ABC):
    code_gen_type: str

    @abstractmethod
    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        raise NotImplementedError


class HtmlCodeFileSaver(CodeFileSaver):
    code_gen_type = CODE_GEN_TYPE_HTML

    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        output_dir = settings.generated_code_path() / f"html_{app_id}"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "index.html"
        output_file.write_text(parsed_code, encoding="utf-8")
        return output_dir


class MultiFileCodeFileSaver(CodeFileSaver):
    code_gen_type = CODE_GEN_TYPE_MULTI_FILE

    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        output_dir = settings.generated_code_path() / f"multi_{app_id}"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "README.md"
        output_file.write_text(parsed_code, encoding="utf-8")
        return output_dir


class CodeFileSaverExecutor:
    def __init__(self, savers: Sequence[CodeFileSaver] | None = None) -> None:
        saver_list = list(savers) if savers is not None else [HtmlCodeFileSaver(), MultiFileCodeFileSaver()]
        self._savers = {saver.code_gen_type: saver for saver in saver_list}

    def save(self, code_gen_type: str, app_id: int, parsed_code: str, settings: Settings) -> Path:
        saver = self._savers.get(code_gen_type)
        if saver is None:
            raise BusinessException(ErrorCode.PARAMS_ERROR, f"Unsupported code_gen_type: {code_gen_type}")
        return saver.save(app_id=app_id, parsed_code=parsed_code, settings=settings)


def save_html_code(app_id: int, html_code: str, settings: Settings) -> Path:
    return HtmlCodeFileSaver().save(app_id=app_id, parsed_code=html_code, settings=settings)
