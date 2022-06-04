# Socket获取AOD Water值
此包提供的函数主要用于获取气溶胶和水汽含量，可以查询点或者是多边形范围内特定时间的参数

## 1 功能介绍

1. 查询单点单个时间的气溶胶水汽值
2. 查询多边形范围内的气溶胶水汽值

## 2 API示范

### 1 单点查询

```python
# 获取全部
aod, water = connect("2013-01-02", 276 * 631 + 402, DownloadType.ALL)
# 获取水汽
water_ = connect("2013-01-02", convert(120.23, 27.123), DownloadType.WATER)
# 获取气溶胶
aod_ = connect("2013-01-02", convert(98.12, 46.765), DownloadType.AOD)

def connect(date: str, index, type: DownloadType,wrongNum:float=-11) -> (float, float):
    """
    下载指定行列对应的值
    :param date: 日期
    :param index: 索引值
    :param type: 下载类型
    :param wrongNum: 错误参数
```

**单点查询函数 connect**

| 参数     | 类型           | 默认参数 | 说明                                              |
| -------- | -------------- | -------- | ------------------------------------------------- |
| date     | 时间           | 无       | 时间格式 yyyy-MM-dd 年月日                        |
| index    | 查询索引       | 无       | 可以指定也可以使用convert函数将经纬度转换为索引值 |
| type     | 查询类型       | ALL      | 三种 AOD,WATER,ALL                                |
| wrongnum | 查询异常填充值 | -12      | 可以指定任意浮点型参数                            |

**经纬度转换函数 convert**

| 参数 | 类型 | 默认参数 | 说明 |
| ---- | ---- | -------- | ---- |
| lon  | 经度 | 浮点     |      |
| lat  | 纬度 | 浮点     |      |

### 2 多边形查询

```python
# 获取全部
ans, points = mutipoly_connect("2013-01-21", [[85, 55], [125, 45], [115, 32], [93, 20]], DownloadType.ALL)
# 获取水汽
ans, points = mutipoly_connect("2013-01-21", [[85, 55], [125, 45], [115, 32], [93, 20]], DownloadType.WATER)
# 获取AOD
ans, points = mutipoly_connect("2013-01-21", [[85, 55], [125, 45], [115, 32], [93, 20]], DownloadType.AOD)
```

| 参数     | 类型                   | 默认参数 | 说明                                       |
| -------- | ---------------------- | -------- | ------------------------------------------ |
| date     | 日期                   | 无       | 时间格式 yyyy-MM-dd 年月日                 |
| points   | 多边形点               | 无       | 嵌套列表 [[x,y],[x1,y1],[x2,y2]...[xn,yn]] |
| type     | 查询类型               | 无       | 三种 AOD,WATER,ALL                         |
| show     | 是否显示多边形范围图像 | true     | 关闭以后不显示图像                         |
| wrongnum | 错误填充               | -12      | 可以指定任意浮点型参数                     |

## 3 实现原理

python socket + java netty

> 预先需要以下包
>
> ```
> matplotlib
> numpy
> shapely.geometry
> tqdm
> ```

多边形采样使用shapely对范围内的点进行判断完成

## 4 项目地址

[链接](https://github.com/GACTeam/pythonSocket)