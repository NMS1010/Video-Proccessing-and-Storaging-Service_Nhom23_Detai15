import json
from bson import ObjectId

import pytest
from flask import url_for

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': True},)], indirect=True)
def test_edit_project_scale_success(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        # edit request
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 640
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '202 ACCEPTED'
        assert resp_data == {'processing': True}
        # get details
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp_data['metadata']['width'] == 640
        assert resp_data['metadata']['height'] == 360


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': True},)], indirect=True)
def test_edit_project_scale_fail_min_max(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])

        # edit request
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 0
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'scale': [f'min value is {test_app.config.get("MIN_VIDEO_WIDTH")}']}

        # edit request
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 5000
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'scale': [f'max value is {test_app.config.get("MAX_VIDEO_WIDTH")}']}

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': True},)], indirect=True)
def test_edit_project_scale_fail_same_width(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])

        # edit request
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 1280
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'trim': ['video and crop option have exactly the same width']}

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': True},)], indirect=True)
def test_edit_project_scale_fail_interpolation(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])

        # edit request
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 1440
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {
            'trim': ['interpolation is permitted only for videos which have width less than 1280px']
        }

        # edit request
        test_app.config['ALLOW_INTERPOLATION'] = False
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 1440
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {
            'trim': ['interpolation of pixels is not allowed']
        }
@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': True},)], indirect=True)
def test_edit_project_scale_and_crop_success(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        # edit request
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        resp = client.put(
            url,
            data=json.dumps({
                "scale": 640,
                "crop": "0,0,400,400"
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '202 ACCEPTED'
        assert resp_data == {'processing': True}
        # get details
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp_data['metadata']['width'] == 640
        assert resp_data['metadata']['height'] == 640
