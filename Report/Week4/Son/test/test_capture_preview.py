import json
from io import BytesIO
from bson import ObjectId

import pytest
from flask import url_for
@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_capture_preview_thumbnail_success(test_app, client, projects):
    project = projects[0]
    position = 4

    with test_app.test_request_context():
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '202 ACCEPTED'
        assert resp_data == {'processing': True}

        resp = client.get(
            url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '200 OK'
        assert test_app.fs.get(resp_data['thumbnails']['preview']['storage_id']).__class__ is bytes

    # postion greater than duration
    position = 20
    with test_app.test_request_context():
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '202 ACCEPTED'
        assert resp_data == {'processing': True}

        resp = client.get(
            url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        )
        resp_data = json.loads(resp.data)
        assert resp.status == '200 OK'
        assert test_app.fs.get(resp_data['thumbnails']['preview']['storage_id']).__class__ is bytes


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_capture_preview_thumbnail_crop_success(test_app, client, projects):
    project = projects[0]
    position = 4
    crop = "0,0,640,480"

    with test_app.test_request_context():
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        assert resp.status == '202 ACCEPTED'

        # get details
        resp = client.get(
            url_for('projects.retrieve_edit_destroy_project', project_id=project['_id'])
        )
        resp_data = json.loads(resp.data)
        assert resp_data['thumbnails']['preview']['width'] == 640
        assert resp_data['thumbnails']['preview']['height'] == 480


@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_capture_preview_thumbnail_crop_fail_width_height(test_app, client, projects):
    project = projects[0]
    position = 4
    with test_app.test_request_context():
        crop = "1000,0,640,480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ['x is less than minimum allowed crop width']}

        crop = "0,1000,640,480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ['y is less than minimum allowed crop height']}

        crop = "0,0,10000,480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ['width 10000 is greater than maximum allowed crop width (3840)']}

        crop = "0,0,640,10000"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ['height 10000 is greater than maximum allowed crop height (2160)']}

        crop = "0,0,1640,480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ["width of crop's frame is outside a video's frame"]}

        crop = "0,0,640,1480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ["height of crop's frame is outside a video's frame"]}

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_capture_preview_thumbnail_crop_fail_outside(test_app, client, projects):
    project = projects[0]
    position = 4

    with test_app.test_request_context():
        crop = "0,0,1640,480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ["width of crop's frame is outside a video's frame"]}

        crop = "0,0,640,1480"
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}&crop={crop}'
        resp = client.get(url)
        resp_data = json.loads(resp.data)
        assert resp.status == '400 BAD REQUEST'
        assert resp_data == {'crop': ["height of crop's frame is outside a video's frame"]}

@pytest.mark.parametrize('projects', [({'file': 'sample_0.mp4', 'duplicate': False},)], indirect=True)
def test_capture_preview_thumbnail_409_resp(test_app, client, projects):
    project = projects[0]
    position = 700

    # since we use CELERY_TASK_ALWAYS_EAGER, task will be executed immediately,
    # it means next request will return a finshed result,
    # since we want to test 409 response, we must set processing flag in db directly
    test_app.mongo.db.projects.find_one_and_update(
        {'_id': ObjectId(project['_id'])},
        {'$set': {'processing.thumbnail_preview': True}}
    )

    with test_app.test_request_context():
        url = url_for(
            'projects.retrieve_or_create_thumbnails', project_id=project['_id']
        ) + f'?type=preview&position={position}'
        resp = client.get(url)
        assert resp.status == '409 CONFLICT'
