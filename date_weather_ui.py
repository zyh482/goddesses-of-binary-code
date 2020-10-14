# 页面4的布局设计
# 页面4的功能：系统时间与天气查询
def stack4ui(self):
    layout = QVBoxLayout()
    # 显示当前系统时间
    dateEdit = QLabel()
    dateEdit.setText(QDateTime.currentDateTime().toString('yyyy/MM/dd hh:mm:ss'))

    weatherLabel = QLabel('近5天的天气查询')
    # 定义子布局
    # 功能： 显示未来5天天气情况的查询结果
    weatherHbox = QHBoxLayout()
    for i in range(5):
        day = QLabel()
        day.setFrameStyle(1)
        weatherHbox.addWidget(day)
    # 定义子布局
    # 功能： 查询向导，获取城市名称
    cityHbox = QHBoxLayout()
    cityLabel = QLabel('查询城市名：')
    cityEdit = QLineEdit()
    weatherButton = QPushButton('查询')
    # 将城市名与天气对应 并输出
    weatherButton.clicked.connect(lambda: self.find_city(cityEdit, weatherHbox))
    cityHbox.addWidget(cityLabel)
    cityHbox.addWidget(cityEdit)
    cityHbox.addWidget(weatherButton)
    # 总布局的控件排列
    layout.addWidget(dateEdit)
    layout.addWidget(weatherLabel)
    layout.addLayout(cityHbox)
    layout.addLayout(weatherHbox)
    # 将总布局应用到页面4
    self.stack4.setLayout(layout)


# 定义槽函数
# 功能： 依据输入的城市名，找到对应的天气预报信息，并输出
def find_city(self, cityBtn, hbox):
    city_name = cityBtn.text()
    try:  # 测试城市名是否有效
        weather_url = 'http://wthrcdn.etouch.cn/weather_mini?city={}'.format(city_name)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
        city_response = requests.get(weather_url, headers=headers)
        weather_dict = json.loads(city_response.text)
        forecast_weather = weather_dict.get('data').get('forecast')
    except:
        for i in range(5):
            hbox.itemAt(i).widget().setText('城市名无效!')
    else:
        # 生成未来5天天气情况列表
        day = []
        for i in range(5):
            day.append('日期:' + forecast_weather[i].get('date') + '\n' \
                       + '最高温度:' + forecast_weather[i].get('high') + '\n' \
                       + '最低温度:' + forecast_weather[i].get('low') + '\n' \
                       + '风向:' + forecast_weather[i].get('fengxiang') + '\n' \
                       + '风力:' + forecast_weather[i].get('fengli') + '\n' \
                       + '天气状况:' + forecast_weather[i].get('type') + '\n')
        # 写入到 查询结果子布局
        for i in range(5):
            hbox.itemAt(i).widget().setText(day[i])
