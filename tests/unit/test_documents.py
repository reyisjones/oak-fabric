import hashlib
import io

import pytest
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

from src.extraction.documents import ExtractionError, extract_document


def pdf_bytes(texts: list[str], password: str | None = None) -> bytes:
    writer = PdfWriter()
    for text in texts:
        page = writer.add_blank_page(width=300, height=300)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject()
        stream.set_data(f'BT /F1 12 Tf 20 200 Td ({text}) Tj ET'.encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    if password:
        writer.encrypt(password)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def test_markdown_provenance_and_code_fences():
    content = b'# RAG\r\nEvidence.\r\n## Code\r\n```python\r\n# Not a section\r\n```\r\n'
    doc = extract_document('documents/incoming/rag.md', content)
    assert doc.document_id == hashlib.sha256(content).hexdigest()
    assert doc.source == 'documents/incoming/rag.md'
    assert doc.source_type == 'markdown'
    assert doc.title == 'RAG'
    assert [s.section for s in doc.sections] == ['RAG', 'Code']
    assert '# Not a section' in doc.sections[1].text
    assert all(s.page is None for s in doc.sections)
    assert extract_document(doc.source, content).document_id == doc.document_id


def test_pdf_page_provenance():
    content = pdf_bytes(['First page evidence', 'Second page source'])
    doc = extract_document('source.pdf', content)
    assert [s.page for s in doc.sections] == [1, 2]
    assert [s.text for s in doc.sections] == ['First page evidence', 'Second page source']
    assert doc.source_type == 'pdf'
    assert doc.document_id == hashlib.sha256(content).hexdigest()


@pytest.mark.parametrize(('source', 'content', 'message'), [
    ('empty.md', b'', '1 byte'),
    ('blank.md', b'  \n ', 'No extractable'),
    ('bad.md', b'\xff', 'UTF-8'),
    ('bad.pdf', b'not a PDF', 'signature'),
    ('bad.pdf', b'%PDF-1.7\ntruncated', 'parsed'),
    ('source.exe', b'source', 'Supported formats'),
    (' ', b'hello', 'Source reference'),
])
def test_invalid_sources_fail_explicitly(source, content, message):
    with pytest.raises(ExtractionError, match=message):
        extract_document(source, content)


def test_encrypted_pdf_rejected():
    with pytest.raises(ExtractionError, match='Encrypted'):
        extract_document('locked.pdf', pdf_bytes(['Secret'], 'password'))


def test_blank_pdf_requires_ocr():
    with pytest.raises(ExtractionError, match='OCR'):
        extract_document('scan.pdf', pdf_bytes(['']))


def test_oversized_document_rejected(monkeypatch):
    monkeypatch.setattr('src.extraction.documents.MAX_DOCUMENT_BYTES', 4)
    with pytest.raises(ExtractionError, match='20 MiB'):
        extract_document('large.md', b'12345')


def test_page_limit_rejected(monkeypatch):
    monkeypatch.setattr('src.extraction.documents.MAX_PDF_PAGES', 1)
    with pytest.raises(ExtractionError, match='500 pages'):
        extract_document('large.pdf', pdf_bytes(['One', 'Two']))


def test_markdown_preserves_hash_in_technology_name():
    doc = extract_document('source.md', b'# C#\nLanguage notes\n## Details ##\nBody')
    assert doc.title == 'C#'
    assert doc.sections[1].section == 'Details'
