# vnpy_insight
华泰insight数据服务vnpy datafeed

# 安装
## 源码安装 
下载源码, cd到源码目录，执行
```angular2html
pip install .
```
## pip源安装
```angular2html
pip install vnpy_insight
```

# 限制规则
数据下载使用的是insight的数据回放功能。
对于回放而言，时间限制由股票只数和天数的乘积决定，要求 回放只数 × 回放天数 × 证券权重 ≤ 450，交易时间段内回放功能 乘积<=200。
- Tick/Transaction/Order回放时间范围限制是30天，每支证券权重为1，即可以回放15只股票30天以内的数据或450支股票1天内数据。
- 日K数据回放时间范围限制是365天，每支证券权重为0.005。
- 分钟K线数据回放时间范围限制是90天，每支证券权重0.05。
- 数据最早可以回放到 2017年1月2日

# 参考资料
- https://findata-insight.htsc.com:9151/help/
