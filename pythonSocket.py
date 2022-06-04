# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 15:19
# @Author  : qxcnwu
# @FileName: pythonSocket.py
# @Software: PyCharm

import json
import socket
from enum import Enum
from typing import List, Tuple, Union, Any

import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry
from tqdm import tqdm


class DownloadType(Enum):
    """
    下载全部 0
    下载水汽 1
    下载气溶胶 2
    """
    ALL = 0
    WATER = 1
    AOD = 2


def square_convert(points: List, show: bool = True) -> Tuple[List[Union[int, Any]], List[List[Any]]]:
    """
    点集
    Args:
        points: 点
        show: 是否展示图像
    Returns:
    """
    poly_context = {'type': 'MULTIPOLYGON',
                    'coordinates': [[points]]}
    xtemp = [i[0] for i in points]
    ytemp = [i[1] for i in points]
    poly_shape = shapely.geometry.asShape(poly_context)
    arrayx, arrayy = np.meshgrid(np.linspace(73, 136, 1261), np.linspace(54, 18, 721))
    idx = int((max(min(xtemp), 73) - 73)) * 20 - 1
    idx_ = int((min(max(xtemp), 136) - 73)) * 20 + 1
    idy_ = int((54 - max(min(ytemp), 18)) * 20) - 1
    idy = int((54 - min(max(ytemp), 54)) * 20) + 1
    ans_list = []
    point_list = []
    data = np.zeros((721, 1261))
    for i in tqdm(range(idx, idx_)):
        for j in range(idy, idy_):
            if poly_shape.intersects(shapely.geometry.Point(arrayx[j][i], arrayy[j][i])):
                ans_list.append(j * 1261 + i)
                point_list.append([arrayx[j, i], arrayy[j, i]])
                data[j, i] = np.nan
    if show:
        plt.imshow(data)
        plt.show()
    return ans_list, point_list


def convert(lon: float, lat: float) -> int:
    """
    将经纬度转换为行列号
    :param lon: 经度
    :param lat: 纬度
    :return: 索引值
    """
    assert 73 <= lon <= 136 and 18 <= lat <= 54, \
        "lon should in range(73,136) and lat should in range(18,54) but get lon: " \
        + str(lon) + " lat: " + str(lat)
    row = int((54 - lat) * 20 + 1)
    col = int((lon - 73) * 10 + 1)
    return row * 1261 + col


def connect(date: str, index, type: DownloadType, wrongNum: float = -11) -> (float, float):
    """
    下载指定行列对应的值
    :param date: 日期
    :param index: 索引值
    :param type: 下载类型
    :param wrongNum: 错误参数
    :return:
    """
    if isinstance(index, int):
        soc = socket.socket()
        ip = socket.gethostbyname("159.75.14.197")
        if type == DownloadType.ALL:
            return connect(date, index, DownloadType.AOD), connect(date, index, DownloadType.WATER)
        elif type == DownloadType.AOD:
            soc.connect((ip, 31105))
        else:
            soc.connect((ip, 31115))
        data = {
            "date": date,
            "points": [index],
            "prefix": "qxczjucas",
            "wrongnum": wrongNum
        }
        soc.send((json.dumps(data) + ";").encode("utf-8"))
        ans = soc.recv(32)
        soc.close()
        return float(ans.decode("utf-8").strip(','))
    elif isinstance(index, List):
        soc = socket.socket()
        ip = socket.gethostbyname("159.75.14.197")
        if type == DownloadType.AOD:
            soc.connect((ip, 31105))
        else:
            soc.connect((ip, 31115))
        data = {
            "date": date,
            "points": index,
            "prefix": "qxczjucas",
            "wrongnum": wrongNum
        }
        soc.send((json.dumps(data) + ";").encode("utf-8"))
        ans = soc.recv(1024 * 1024 * 1)
        soc.close()
        return ans.decode("utf-8").strip(',').split(',')
    return None, None


def connect_square(date: str, index, type: DownloadType, wrongnum: float):
    def _connect_square(date: str, index, type: DownloadType):
        num = len(index) // 2000
        ans = []
        for i in tqdm(range(num)):
            if i == num - 1:
                ans = ans + connect(date, index[i * 2000:], type, wrongnum)
            else:
                ans = ans + connect(date, index[i * 2000:i * 2000 + 2000], type, wrongnum)
        return ans

    if type == DownloadType.ALL:
        return _connect_square(date, index, DownloadType.AOD), _connect_square(date, index, DownloadType.WATER)
    return _connect_square(date, index, type)


def mutipoly_connect(date: str, points: List, type: DownloadType, show: bool = True, wrongnum: float = -12):
    ansList, pointList = square_convert(points, show)
    return connect_square(date, ansList, type, wrongnum), pointList


if __name__ == '__main__':
    # 获取全部
    aod, water = connect("2013-01-02", 276 * 631 + 402, DownloadType.ALL)
    # 获取水汽
    water_ = connect("2013-01-02", convert(120.23, 27.123), DownloadType.WATER)
    # 获取气溶胶
    aod_ = connect("2013-01-02", convert(98.12, 46.765), DownloadType.AOD)
    # 获取全部
    ans, points = mutipoly_connect("2013-01-21", [[85, 55], [125, 45], [115, 32], [93, 20]], DownloadType.ALL)
