# -*- coding:utf-8 -*-
"""
@FileName  :insight_datafeed.py
@Time      :2022/11/2 13:50
@Author    :fsksf
"""
import datetime
from typing import List, Optional
import asyncio
from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.constant import Interval
from vnpy.trader.object import HistoryRequest, BarData
from vnpy.trader.setting import SETTINGS
from insight_sdk.com.interface.mdc_gateway_base_define import (
    MDPlaybackExrightsType
)
from insight_sdk.com.insight import common, playback
from insight_sdk.com.insight.market_service import market_service
from vnpy_insight.utils import (
    to_real_price, get_dt_str, get_datetime, Interval_EMarketDataType_MAP,
    Exchange_Market_MAP
)


class InsightCallbackService(market_service):

    def __init__(self, req=None):
        self.playback_finish = False
        self.req: HistoryRequest = req
        self.data_list = []
        super(InsightCallbackService, self).__init__()

    def onPlaybackStatus(self, status):
        print('status: ', status)
        if str(status).endswith('status=17'):
            self.playback_finish = True

    def onPlayback_MD_KLINE(self, data):
        kline_data = data['mdKLine']
        if self.req.interval == Interval.TICK:
            pass

        bar = BarData(
            gateway_name='vnpy_insight',
            open_price=to_real_price(kline_data['OpenPx']),
            high_price=to_real_price(kline_data['HighPx']),
            low_price=to_real_price(kline_data['LowPx']),
            close_price=to_real_price(kline_data['ClosePx']),
            volume=kline_data['TotalVolumeTrade'],
            datetime=get_datetime(str(kline_data['MDDate']), str(kline_data['MDTime'])),
            turnover=kline_data['TotalValueTrade'],
            exchange=self.req.exchange,
            interval=self.req.interval,
            symbol=self.req.symbol,
        )
        print(bar)
        self.data_list.append(bar)


class InsightDatafeed(BaseDatafeed):

    gateway_name = 'vnpy_insight'

    def __init__(self, username=None, password=None):
        self.username: str = username or SETTINGS["datafeed.username"]
        self.password: str = password or SETTINGS["datafeed.password"]

        self.req: HistoryRequest = None

    def login(self, service):
        result = common.login(service, self.username, self.password)
        print(result)

    def query_bar_history(self, req: HistoryRequest) -> Optional[List[BarData]]:
        self.req = req
        service = InsightCallbackService(req=req)
        self.login(service)

        ex_rights_type = MDPlaybackExrightsType.FORWARD_EXRIGHTS
        start_time = get_dt_str(req.start)
        stop_time = get_dt_str(req.end)

        freq = Interval_EMarketDataType_MAP[req.interval]
        market = Exchange_Market_MAP[req.exchange]
        ht_security_id = f'{req.symbol}.{market}'

        security_id_type_list = [
            {"HTSCSecurityID": ht_security_id, "EMarketDataType": freq}
        ]
        playback.playback(security_id_type_list, ex_rights_type, start_time, stop_time)

        result = []

        async def get_result():
            # 同步回调，获取结果
            nonlocal result
            while True:
                await asyncio.sleep(0.1)
                if service.playback_finish:
                    break
            result = service.data_list
        asyncio.run(get_result())
        return result


if __name__ == '__main__':
    from vnpy.trader.constant import Exchange
    idf = InsightDatafeed()
    idf.query_bar_history(
        req=HistoryRequest(symbol='601688', exchange=Exchange.SSE,
                           start=datetime.datetime.now() - datetime.timedelta(days=1),
                           end=datetime.datetime.now(),
                           interval=Interval.MINUTE)
    )
