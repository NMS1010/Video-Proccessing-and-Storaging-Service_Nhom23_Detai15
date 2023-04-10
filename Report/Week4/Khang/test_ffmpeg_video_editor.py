import pytest

from videoserver.lib.video_editor.ffmpeg import FFMPEGVideoEditor


@pytest.mark.parametrize('filestreams', [('sample_0.mp4',)], indirect=True)
def test_ffmpeg_video_editor_trim(test_app, filestreams):
    editor = FFMPEGVideoEditor()
    mp4_stream = filestreams[0]

    with test_app.app_context():
        content, metadata = editor.edit_video(
            stream_file=mp4_stream,
            filename='test_ffmpeg_video_editor_sample.mp4',
            trim={'start': 2, 'end': 10}
        )
        assert metadata['duration'] == 8.0
        content, metadata = editor.edit_video(
            stream_file=mp4_stream,
            filename='test_ffmpeg_video_editor_sample.mp4',
            trim={'start': 0, 'end': 3}
        )
        assert metadata['duration'] == 3.0


@pytest.mark.parametrize('filestreams', [('sample_0.mp4',)], indirect=True)
def test_ffmpeg_video_editor_crop(test_app, filestreams):
    editor = FFMPEGVideoEditor()
    mp4_stream = filestreams[0]

    with test_app.app_context():
        content, metadata = editor.edit_video(
            stream_file=mp4_stream,
            filename='test_ffmpeg_video_editor_sample.mp4',
            crop={
                'x': 0,
                'y': 0,
                'width': 640,
                'height': 480
            }
        )
        assert metadata['width'] == 640
        assert metadata['height'] == 480
