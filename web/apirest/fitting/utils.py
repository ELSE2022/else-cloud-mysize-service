import asyncio
import aiohttp
import json
import subprocess

from datetime import datetime
from data.repositories import CompareVisualizationRepository
from settings import ELSE_3D_SERVICE_FULL
from orientdb_data_layer import data_connection

_compareVisualRep = CompareVisualizationRepository()


def get_visualization_compare_subprocess(last, scan, user_uuid):
    """
    Get visualization compare data from 3d service by subprocess

    Parameters
    ----------
    last :  web.data.models.Model.Model
        Model of product for compare
    scan : web.data.models.Scan.Scan
        User scan for compare
    user_uuid : str or None
        User uuid that has been send in request data
    Returns
    -------
    result_json: JSON
        JSON from 3d service
    """
    p = subprocess.Popen([
        'curl',
        '-X',
        'POST',
        '-F',
        'last=@{}'.format(last.stl_path),
        '-F',
        'scan=@attachments/{}'.format(scan.stl_path),
        '-F',
        'user_uuid={}'.format(user_uuid),
        f'{ELSE_3D_SERVICE_FULL}/visualization/compare_visualization/'
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    result_json = json.loads(output)
    return result_json


async def get_compare_visual(last, scan, environment):
    with open(last.stl_path, 'rb') as a, open('attachments/' + scan.stl_path, 'rb') as b:
        async with aiohttp.ClientSession() as session:
            _graph = data_connection.get_graph()
            values = {'user_uuid': _graph.element_from_link(scan.user).uuid, 'last': a, 'scan': b}
            if environment:
                values['environment_uuid'] = environment
            url = f'{ELSE_3D_SERVICE_FULL}/visualization/compare_visualization/'
            async with session.post(url, data=values) as resp:
                result_json = await resp.json()
                _compareVisualRep.add(dict(scan=scan, model=last,
                                           output_model=result_json.get('output_model'),
                                           output_model_3d=result_json.get('output_model_3d'),
                                           creation_time=datetime.now()))


def get_visualization_compare_aiohttp(last, scans, environment_uuid):
    """
    Get visualization compare data from 3d service by aiohttp

    Parameters
    ----------
    last :  web.data.models.Model.Model
        Model of product for compare
    scans : list of web.data.models.Scan.Scan
        List of user scans for compare
    environment_uuid : str or None
        Environment uuid that has been send in request data
    Returns
    -------
    None
    """
    ioloop = asyncio.get_event_loop()
    for scan in scans:
        tasks = [
            ioloop.create_task(get_compare_visual(last, scan, environment_uuid))
        ]
        ioloop.run_until_complete(asyncio.wait(tasks))

    ioloop.close()
