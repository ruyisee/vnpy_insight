# -*- coding:utf-8 -*-
"""
@FileName  :utils.py
@Time      :2022/11/2 15:53
@Author    :fsksf
"""
import datetime
from insight_sdk.com.interface.mdc_gateway_base_define import EMarketDataType
from vnpy.trader.constant import Interval, Exchange

Interval_EMarketDataType_MAP = {
    Interval.TICK: EMarketDataType.MD_TICK,
    Interval.MINUTE: EMarketDataType.MD_KLINE_1MIN,
    Interval.HOUR: EMarketDataType.MD_KLINE_60MIN,
    Interval.DAILY: EMarketDataType.MD_KLINE_1D
}
EMarketDataType_Interval_MAP = {v: k for k, v in Interval_EMarketDataType_MAP.items()}

Exchange_Market_MAP = {
    Exchange.SZSE: 'SZ',
    Exchange.SSE: 'SH',
    Exchange.CFFEX: 'CCFX'
}


def to_real_price(value):
    return value / 10000


def get_dt_str(dt: datetime.datetime):
    return dt.strftime('%Y%m%d%H%M%S')


def get_datetime(dt, tm):
    return datetime.datetime.strptime(dt+tm, '%Y%m%d%H%M%S000')
