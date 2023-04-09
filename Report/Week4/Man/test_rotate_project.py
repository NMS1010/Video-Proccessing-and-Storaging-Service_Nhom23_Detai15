import json
from io import BytesIO
from unittest import mock

import pytest
from flask import url_for
from pymongo.errors import ServerSelectionTimeoutError

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': True},)], indirect=True)
def test_edit_project_rotate_success(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        # edit request
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        resp = client.put(
            url,
            data=json.dumps({
                "rotate": 90
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '202 ACCEPTED'
        assert resp_data == {'processing': True}
        # get details
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp_data['metadata']['width'] == 720
        assert resp_data['metadata']['height'] == 1280


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_edit_project_rotate_fail(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        # edit request
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        resp = client.put(
            url,
            data=json.dumps({
                "rotate": 70
            }),
            content_type='application/json'
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data["project_id"] == ["Video with version 1 is not editable, use duplicated project instead."]
