from asyncio import to_thread
from kikiutils.file import async_read_file, async_save_file, get_file_mime, mkdirs, rmdir
from sanic import Blueprint, Request, text
from sanic.response import raw
from sanic.request import File

from ..main.convert import ConvertVideoConfig, convert_video


convert_api = Blueprint('convert_api', url_prefix='/convert')


@convert_api.post('/video/<ext>')
async def video(rq: Request, ext: str):
    video_file: File = rq.files.get('file')

    if video_file is None:
        return text('no_video_file')

    file_data = video_file.body
    file_mime = get_file_mime(file_data)

    if file_mime[0] != 'video':
        return text('file_is_not_video')

    if ext != 'mp4':
        return text('ext_not_allowed')

    config = ConvertVideoConfig(ext)
    mkdirs(config.tmp_dir_path)
    await async_save_file(config.video_path, file_data)

    if await to_thread(convert_video, config):
        new_file_data = await async_read_file(config.converted_video_path)
        rmdir(config.tmp_dir_path)
        return raw(new_file_data, content_type='video/{ext}')

    rmdir(config.tmp_dir_path)
    return text('convert_error', 500)
