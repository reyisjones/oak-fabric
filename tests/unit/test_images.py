import hashlib
import io
import json

import pytest
from PIL import Image
from pydantic import ValidationError

from src.embeddings.client import ModelClient, ModelError
from src.extraction.architecture import ArchitectureObservation
from src.extraction.images import ImageInputError, analyze_image, inspect_image
from src.ingestion.images import process_image


def png() -> bytes:
    stream = io.BytesIO()
    Image.new('RGB', (32, 24), 'white').save(stream, format='PNG')
    return stream.getvalue()


def observation() -> dict:
    return {'title': None, 'components': [
        {'id':'client', 'label':'Client', 'technology':None, 'evidence':'Label Client in left box'},
        {'id':'api', 'label':'API', 'technology':None, 'evidence':'Label API in right box'}],
        'connections':[{'source':'client','target':'api','label':None,'evidence':'Arrowhead points right'}],
        'boundaries':[], 'uncertainties':[], 'inferences':[]}


def client(monkeypatch, analysis=None, finish='stop'):
    model = ModelClient('http://unused', 'nomic', 'vision')
    monkeypatch.setattr(model, '_post', lambda path, payload: {'model':'vision','choices':[{
        'finish_reason':finish,'message':{'content':json.dumps(analysis if analysis is not None else observation())}}]})
    return model


def test_decoder_preserves_identity():
    content = png()
    info = inspect_image(content)
    assert (info.width, info.height, info.media_type) == (32,24,'image/png')
    assert info.sha256 == hashlib.sha256(content).hexdigest()


@pytest.mark.parametrize('content', [b'', b'not an image', b'\x89PNG\r\n\x1a\ntruncated'])
def test_bad_images_rejected(content):
    with pytest.raises(ImageInputError): inspect_image(content)


def test_pixel_limit(monkeypatch):
    monkeypatch.setattr('src.extraction.images.MAX_IMAGE_PIXELS', 100)
    with pytest.raises(ImageInputError, match='pixels'): inspect_image(png())


def test_byte_limit(monkeypatch):
    monkeypatch.setattr('src.extraction.images.MAX_IMAGE_BYTES', 10)
    with pytest.raises(ImageInputError, match='MiB'): inspect_image(png())


def test_unsupported_format():
    stream = io.BytesIO()
    Image.new('RGB',(2,2)).save(stream,format='BMP')
    with pytest.raises(ImageInputError, match='formats'): inspect_image(stream.getvalue())


def test_valid_structure_and_separate_inferences():
    data = observation() | {'inferences':['This may be a client-server architecture.']}
    parsed = ArchitectureObservation.model_validate(data)
    assert parsed.components[0].technology is None
    assert parsed.inferences == data['inferences']


@pytest.mark.parametrize('case', ['duplicate_node','unknown_edge','duplicate_edge','unknown_boundary','empty'])
def test_bad_graph_structure(case):
    data = observation()
    if case == 'duplicate_node': data['components'].append(data['components'][0])
    if case == 'unknown_edge': data['connections'][0]['target']='missing'
    if case == 'duplicate_edge': data['connections'].append(data['connections'][0])
    if case == 'unknown_boundary': data['boundaries']=[{'label':'Zone','component_ids':['missing'],'evidence':'Box'}]
    if case == 'empty': data.update(components=[],connections=[])
    with pytest.raises(ValidationError): ArchitectureObservation.model_validate(data)


def test_empty_analysis_requires_explicit_uncertainty():
    data = observation() | {'components':[], 'connections':[], 'uncertainties':['No readable diagram found.']}
    assert ArchitectureObservation.model_validate(data).uncertainties


def test_request_uses_actual_image_bytes(monkeypatch):
    model = client(monkeypatch)
    captured=[]
    respond=model._post
    def capture(path,payload):
        captured.append(payload)
        return respond(path,payload)
    monkeypatch.setattr(model,'_post',capture)
    assert len(analyze_image(png(),model).components)==2
    assert captured[0]['messages'][1]['content'][1]['image_url']['url'].startswith('data:image/png;base64,')
    assert captured[0]['response_format']['type']=='json_schema'


def test_truncated_analysis_is_not_accepted(monkeypatch):
    with pytest.raises(ModelError): analyze_image(png(),client(monkeypatch,finish='length'))


def test_preserves_original_and_prior_drafts(tmp_path,monkeypatch):
    source=tmp_path/'incoming.png'
    content=png(); source.write_bytes(content)
    first=process_image(source,client(monkeypatch),tmp_path)
    previous=first.read_bytes()
    second=process_image(source,client(monkeypatch),tmp_path)
    assert first != second and first.read_bytes()==previous
    draft=json.loads(previous)
    assert (tmp_path/draft['preserved_source']).read_bytes()==source.read_bytes()==content
    assert draft['status']=='review' and draft['validation']['visual_accuracy']=='not_reviewed'


def test_model_failure_retains_source_without_draft(tmp_path,monkeypatch):
    source=tmp_path/'incoming.png'; source.write_bytes(png())
    with pytest.raises(ModelError): process_image(source,client(monkeypatch,finish='length'),tmp_path)
    assert list((tmp_path/'images'/'processed').glob('*.png'))
    assert not list((tmp_path/'documents').rglob('*.json'))


def test_animated_png_rejected():
    stream=io.BytesIO()
    first=Image.new('RGB',(4,4),'white')
    first.save(stream,format='PNG',save_all=True,append_images=[Image.new('RGB',(4,4),'black')])
    with pytest.raises(ImageInputError,match='Animated'): inspect_image(stream.getvalue())


def test_corrupted_preserved_source_is_not_overwritten(tmp_path,monkeypatch):
    source=tmp_path/'incoming.png'; source.write_bytes(png())
    artifact=process_image(source,client(monkeypatch),tmp_path)
    original=tmp_path/json.loads(artifact.read_text())['preserved_source']
    original.write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='checksum'): process_image(source,client(monkeypatch),tmp_path)
    assert original.read_bytes()==b'corrupt'


def test_panel_focus_preserves_full_source_and_records_scope(tmp_path, monkeypatch):
    source = tmp_path / 'incoming.png'
    source.write_bytes(png())
    model = client(monkeypatch)
    captured = []
    respond = model._post

    def capture(path, payload):
        captured.append(payload)
        return respond(path, payload)

    monkeypatch.setattr(model, '_post', capture)
    output = process_image(source, model, tmp_path, focus='Panel 11')
    draft = json.loads(output.read_text())
    assert draft['focus'] == 'Panel 11'
    assert 'Panel 11' in captured[0]['messages'][1]['content'][0]['text']
    assert (tmp_path / draft['preserved_source']).read_bytes() == source.read_bytes()
    assert draft['status'] == 'review'
