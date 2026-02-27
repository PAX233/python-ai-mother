from __future__ import annotations

import html
import json
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from app.core.code_gen_types import (
    CODE_GEN_TYPE_HTML,
    CODE_GEN_TYPE_MULTI_FILE,
    CODE_GEN_TYPE_VUE_PROJECT,
)
from app.core.config import Settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException

_FENCE_PATTERN = re.compile(r"```(?P<header>[^\n`]*)\n(?P<body>.*?)```", re.DOTALL)
_XML_FILE_PATTERN = re.compile(
    r"<file\s+path=[\"'](?P<path>[^\"']+)[\"']\s*>(?P<body>.*?)</file>",
    re.IGNORECASE | re.DOTALL,
)
_LINE_HINT_PATTERN = re.compile(r"^(?:#|//|;)?\s*(?:file|filename|path)\s*[:=]\s*(.+)$", re.IGNORECASE)
_KNOWN_LANG_HEADERS = {
    "html",
    "css",
    "javascript",
    "js",
    "typescript",
    "ts",
    "tsx",
    "json",
    "md",
    "txt",
    "yaml",
    "yml",
    "vue",
    "bash",
    "sh",
}


@dataclass(slots=True)
class GeneratedFile:
    path: str
    content: str


class CodeFileSaver(ABC):
    code_gen_type: str

    @abstractmethod
    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        raise NotImplementedError


class HtmlCodeFileSaver(CodeFileSaver):
    code_gen_type = CODE_GEN_TYPE_HTML

    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        output_dir = settings.generated_code_path() / f"{CODE_GEN_TYPE_HTML}_{app_id}"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "index.html"
        output_file.write_text(parsed_code, encoding="utf-8")
        return output_dir


class MultiFileCodeFileSaver(CodeFileSaver):
    code_gen_type = CODE_GEN_TYPE_MULTI_FILE

    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        output_dir = settings.generated_code_path() / f"{CODE_GEN_TYPE_MULTI_FILE}_{app_id}"
        output_dir.mkdir(parents=True, exist_ok=True)
        files = extract_generated_files(parsed_code, code_gen_type=CODE_GEN_TYPE_MULTI_FILE)
        if not files:
            files = [GeneratedFile(path="README.md", content=parsed_code)]
        _write_generated_files(output_dir, files)
        return output_dir


class VueProjectCodeFileSaver(CodeFileSaver):
    code_gen_type = CODE_GEN_TYPE_VUE_PROJECT

    def save(self, app_id: int, parsed_code: str, settings: Settings) -> Path:
        output_dir = settings.generated_code_path() / f"{CODE_GEN_TYPE_VUE_PROJECT}_{app_id}"
        output_dir.mkdir(parents=True, exist_ok=True)
        files = extract_generated_files(parsed_code, code_gen_type=CODE_GEN_TYPE_VUE_PROJECT)
        if not files:
            files = _build_default_vue_project_files(parsed_code)
        files = _ensure_vue_project_preview_files(files)
        _write_generated_files(output_dir, files)
        return output_dir


class CodeFileSaverExecutor:
    def __init__(self, savers: Sequence[CodeFileSaver] | None = None) -> None:
        saver_list = (
            list(savers)
            if savers is not None
            else [HtmlCodeFileSaver(), MultiFileCodeFileSaver(), VueProjectCodeFileSaver()]
        )
        self._savers = {saver.code_gen_type: saver for saver in saver_list}

    def save(self, code_gen_type: str, app_id: int, parsed_code: str, settings: Settings) -> Path:
        saver = self._savers.get(code_gen_type)
        if saver is None:
            raise BusinessException(ErrorCode.PARAMS_ERROR, f"Unsupported code_gen_type: {code_gen_type}")
        return saver.save(app_id=app_id, parsed_code=parsed_code, settings=settings)


def save_html_code(app_id: int, html_code: str, settings: Settings) -> Path:
    return HtmlCodeFileSaver().save(app_id=app_id, parsed_code=html_code, settings=settings)


def extract_generated_files(raw_text: str, code_gen_type: str) -> list[GeneratedFile]:
    text = (raw_text or "").strip()
    if not text or code_gen_type == CODE_GEN_TYPE_HTML:
        return []

    files: dict[str, str] = {}

    for matched in _XML_FILE_PATTERN.finditer(text):
        path = _sanitize_relative_path(matched.group("path"))
        content = matched.group("body").strip("\n")
        if path and content:
            files[path] = content

    for matched in _FENCE_PATTERN.finditer(text):
        header = (matched.group("header") or "").strip()
        body = matched.group("body")
        path = _extract_file_path_from_header(header)
        if path is None:
            lines = body.splitlines()
            if lines:
                hint = _extract_file_path_from_line_hint(lines[0])
                if hint:
                    path = hint
                    body = "\n".join(lines[1:])
        path = _sanitize_relative_path(path) if path else None
        content = body.strip("\n")
        if path and content:
            files[path] = content

    return [GeneratedFile(path=path, content=content) for path, content in files.items()]


def _extract_file_path_from_header(header: str) -> str | None:
    if not header:
        return None
    lowered = header.lower()
    for prefix in ("file:", "filename:", "path:"):
        if lowered.startswith(prefix):
            return header[len(prefix) :].strip()
    for prefix in ("file=", "filename=", "path="):
        if lowered.startswith(prefix):
            return header[len(prefix) :].strip().strip('"').strip("'")

    if " " in header:
        tokens = [token.strip() for token in header.split() if token.strip()]
        for token in reversed(tokens):
            if ("/" in token or "." in token) and token.lower() not in _KNOWN_LANG_HEADERS:
                return token
        return None

    if header.lower() in _KNOWN_LANG_HEADERS:
        return None
    if "/" in header or "." in header:
        return header
    return None


def _extract_file_path_from_line_hint(first_line: str) -> str | None:
    matched = _LINE_HINT_PATTERN.match(first_line.strip())
    if matched is None:
        return None
    return matched.group(1).strip().strip('"').strip("'")


def _sanitize_relative_path(path: str | None) -> str | None:
    if not path:
        return None
    clean = path.strip().replace("\\", "/").lstrip("./")
    if not clean:
        return None
    if clean.startswith("/"):
        return None
    parts = [part for part in clean.split("/") if part and part != "."]
    if not parts or any(part == ".." for part in parts):
        return None
    if ":" in parts[0]:
        return None
    return "/".join(parts)


def _write_generated_files(output_dir: Path, files: list[GeneratedFile]) -> None:
    output_dir_resolved = output_dir.resolve()
    for item in files:
        target = output_dir / item.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target_resolved = target.resolve()
        try:
            target_resolved.relative_to(output_dir_resolved)
        except ValueError as exc:
            raise BusinessException(ErrorCode.PARAMS_ERROR, f"Invalid file path: {item.path}") from exc
        target.write_text(item.content, encoding="utf-8")


def _build_default_vue_project_files(raw_text: str) -> list[GeneratedFile]:
    escaped = html.escape((raw_text or "").strip()[:3000])
    package_json = {
        "name": "generated-vue-project",
        "version": "0.0.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview",
        },
        "dependencies": {
            "vue": "^3.5.0",
        },
        "devDependencies": {
            "vite": "^5.4.0",
            "@vitejs/plugin-vue": "^5.1.0",
            "typescript": "^5.5.0",
        },
    }
    return [
        GeneratedFile(path="package.json", content=json.dumps(package_json, ensure_ascii=False, indent=2)),
        GeneratedFile(
            path="index.html",
            content="""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Generated Vue Project</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
""",
        ),
        GeneratedFile(
            path="vite.config.ts",
            content="""import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
""",
        ),
        GeneratedFile(
            path="src/main.ts",
            content="""import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
""",
        ),
        GeneratedFile(
            path="src/App.vue",
            content=f"""<template>
  <main class="wrapper">
    <h1>Generated Vue Project</h1>
    <p>模型输出内容（截断展示）：</p>
    <pre>{escaped or "No content"}</pre>
  </main>
</template>

<style scoped>
.wrapper {{
  max-width: 960px;
  margin: 40px auto;
  padding: 0 16px;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
}}
pre {{
  white-space: pre-wrap;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  background: #fafafa;
}}
</style>
""",
        ),
    ]


def _ensure_vue_project_preview_files(files: list[GeneratedFile]) -> list[GeneratedFile]:
    file_map: dict[str, GeneratedFile] = {item.path: item for item in files}
    if "dist/index.html" not in file_map:
        if "index.html" in file_map:
            file_map["dist/index.html"] = GeneratedFile(path="dist/index.html", content=file_map["index.html"].content)
        else:
            file_map["dist/index.html"] = GeneratedFile(
                path="dist/index.html",
                content="""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Generated Project Preview</title>
  </head>
  <body>
    <h1>Generated project ready</h1>
    <p>dist/index.html is generated as preview fallback.</p>
  </body>
</html>
""",
            )
    return list(file_map.values())
