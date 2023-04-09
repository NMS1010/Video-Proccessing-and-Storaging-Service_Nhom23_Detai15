import json
from bson import ObjectId

import pytest
from flask import url_for


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_retrieve_project_success(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        # retrieve project
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        resp = client.get(url)
        resp_data = json.loads(resp.data)

        assert resp.status == '200 OK'
        assert '_id' in resp_data
        assert 'filename' in resp_data
        assert 'storage_id' in resp_data
        assert 'create_time' in resp_data
        assert resp_data['mime_type'] == 'video/mp4'
        assert resp_data['request_address'] == '127.0.0.1'
        assert resp_data['original_filename'] == project['original_filename']
        assert resp_data['version'] == 1
        assert resp_data['parent'] is None
        assert resp_data['processing'] == {'video': False, 'thumbnail_preview': False, 'thumbnails_timeline': False}
        assert resp_data['thumbnails'] == {'timeline': [], 'preview': {}}
        assert resp_data['url'] == url_for('projects.get_raw_video', project_id=resp_data["_id"], _external=True)
        assert resp_data['metadata']['codec_name'] == 'h264'
        assert resp_data['metadata']['codec_long_name'] == 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10'
        assert resp_data['metadata']['width'] == 1280
        assert resp_data['metadata']['height'] == 720
        assert resp_data['metadata']['r_frame_rate'] == '25/1'
        assert resp_data['metadata']['bit_rate'] == 1045818
        assert resp_data['metadata']['nb_frames'] == 375
        assert resp_data['metadata']['duration'] == 15.0
        assert resp_data['metadata']['format_name'] == 'mov,mp4,m4a,3gp,3g2,mj2'
        assert 'size' in resp_data['metadata']


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_retrieve_project_404(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        # retrieve project
        url = url_for('projects.retrieve_edit_destroy_project', project_id="definitely_not_object_id")
        resp = client.get(url)
        assert resp.status == '404 NOT FOUND'

        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        client.delete(url)
        resp = client.get(url)
        assert resp.status == '404 NOT FOUND'
