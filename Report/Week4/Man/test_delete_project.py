import json
from bson import ObjectId
from unittest import mock

import pytest
from flask import url_for
from pymongo.errors import ServerSelectionTimeoutError

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_delete_project_success(test_app, client, projects):
    project = projects[0]

    with test_app.test_request_context():
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        resp = client.delete(url)
        assert resp.status == '204 NO CONTENT'


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_delete_project_fails(test_app, client, projects):
    project = projects[0]
    
    with test_app.test_request_context():
        url = url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        client.delete(url)
        resp = client.delete(url)
        assert resp.status == '404 NOT FOUND'
