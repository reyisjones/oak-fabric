from dataclasses import asdict, replace

import pytest

from src.chunking.text import chunk_document
from src.extraction.documents import extract_document


def test_chunk_overlap_coverage_and_stable_identity():
    doc = extract_document('source.md', b'abcdefghijklmnopqrstuvwxyz')
    chunks = chunk_document(doc, size=10, overlap=2)
    assert [c.text for c in chunks] == ['abcdefghij', 'ijklmnopqr', 'qrstuvwxyz']
    assert ''.join([chunks[0].text, *[c.text[2:] for c in chunks[1:]]]) == doc.sections[0].text
    assert chunks == chunk_document(doc, size=10, overlap=2)
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    required = {'chunk_id', 'document_id', 'source', 'source_type', 'title', 'section',
                'page', 'image_reference', 'created_at', 'technology', 'architecture', 'tags'}
    assert required <= asdict(chunks[0]).keys()


def test_chunks_preserve_page_and_distinguish_source_aliases():
    doc = extract_document('source.md', b'hello')
    doc = replace(doc, source_type='pdf', sections=(replace(doc.sections[0], page=3),))
    chunk = chunk_document(doc)[0]
    assert chunk.page == 3
    assert chunk.source == 'source.md'
    alias = chunk_document(replace(doc, source='another.md'))[0]
    assert alias.chunk_id != chunk.chunk_id
    assert alias.document_id == chunk.document_id


def test_repeated_headings_do_not_collide():
    doc = extract_document('source.md', b'# Same\nText\n# Same\nText')
    chunks = chunk_document(doc)
    assert len({c.chunk_id for c in chunks}) == 2


@pytest.mark.parametrize(('size', 'overlap'), [(0, 0), (-1, 0), (10, -1), (10, 10), (10, 11)])
def test_invalid_chunk_configuration(size, overlap):
    doc = extract_document('source.md', b'hello')
    with pytest.raises(ValueError, match='overlap'):
        chunk_document(doc, size=size, overlap=overlap)
