import hashlib
import io
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import PurePath

from pypdf import PdfReader
from pypdf.errors import PdfReadError

MAX_DOCUMENT_BYTES = 20 * 1024 * 1024
MAX_PDF_PAGES = 500


class ExtractionError(ValueError):
    """A source cannot be extracted by the supported document pipeline."""


@dataclass(frozen=True)
class Section:
    text: str
    section: str
    page: int | None = None


@dataclass(frozen=True)
class Document:
    document_id: str
    source: str
    source_type: str
    title: str
    created_at: str
    sections: tuple[Section, ...]


def extract_document(source: str, content: bytes) -> Document:
    """Extract supplied bytes without reading paths or changing the original."""
    if not source.strip():
        raise ExtractionError("Source reference is required")
    if not content or len(content) > MAX_DOCUMENT_BYTES:
        raise ExtractionError("Document must contain 1 byte to 20 MiB")
    suffix = PurePath(source).suffix.lower()
    title = PurePath(source).stem
    if suffix in {".md", ".markdown"}:
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ExtractionError("Markdown must use UTF-8") from exc
        sections = _markdown_sections(text)
        heading = next((s.section for s in sections if s.section), None)
        title = heading or title
        source_type = "markdown"
    elif suffix == ".pdf":
        sections = _pdf_sections(content)
        source_type = "pdf"
    else:
        raise ExtractionError("Supported formats are Markdown and PDF")
    if not sections:
        raise ExtractionError("No extractable text; scanned PDFs require OCR")
    return Document(
        document_id=hashlib.sha256(content).hexdigest(),
        source=source,
        source_type=source_type,
        title=title,
        created_at=datetime.now(timezone.utc).isoformat(),
        sections=tuple(sections),
    )


def _markdown_sections(text: str) -> list[Section]:
    sections = []
    heading = ""
    lines: list[str] = []
    fence: str | None = None
    for line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines():
        stripped = line.lstrip()
        marker = re.match(r"(`{3,}|~{3,})", stripped)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            lines.append(line)
            continue
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*$", line) if fence is None else None
        if match:
            body = "\n".join(lines).strip()
            if body:
                sections.append(Section(body, heading))
            heading = re.sub(r"\s+#+$", "", match.group(1))
            lines = [line]
        else:
            lines.append(line)
    body = "\n".join(lines).strip()
    if body:
        sections.append(Section(body, heading))
    return sections


def _pdf_sections(content: bytes) -> list[Section]:
    if not content.startswith(b"%PDF-"):
        raise ExtractionError("Invalid PDF signature")
    try:
        reader = PdfReader(io.BytesIO(content), strict=True)
        if reader.is_encrypted:
            raise ExtractionError("Encrypted PDFs are not supported")
        if len(reader.pages) > MAX_PDF_PAGES:
            raise ExtractionError("PDF exceeds 500 pages")
        return [Section(text, f"Page {number}", number)
                for number, page in enumerate(reader.pages, 1)
                if (text := (page.extract_text() or "").strip())]
    except (PdfReadError, KeyError, TypeError, IndexError, RecursionError) as exc:
        raise ExtractionError("PDF could not be parsed") from exc
