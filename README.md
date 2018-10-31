# yinqiantong SDK for Python

## 创建订单

```
auth.Auth(APP_ID, APP_SECRET).create_order({
    'channel': '1',
    'platform': '2',
    'money': 1,
    'notify_url': 'https://yinqiantong.com/test',
    'client_out_trade_no': 'your_clent_out_trade_no',
    'client_ip': '127.0.0.1',
})
```

## 查询订单状态

```
auth.Auth(APP_ID, APP_SECRET).get_order_state_by_client_out_trade_no(your_client_out_trade_no)
```

## 生成签名

```
auth.Auth(APP_ID, APP_SECRET).create_sign({
    'channel': '1',
    'platform': '2',
    'money': 1,
    'client_ip': '127.0.0.1'
})
```

## 校验签名

```
auth.Auth(APP_ID, APP_SECRET).check_sign(your_data)
```