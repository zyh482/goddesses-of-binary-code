# 页面7的布局设计
# 功能： 实现打地鼠游戏
def stack7ui(self):
    # 定义布局
    layout = QHBoxLayout()  # 总布局
    gameSublayout = QGridLayout()  # 游戏界面子布局
    introSublayout = QVBoxLayout()  # 说明界面子布局

    holes = []  # 存储各地洞的控件，便于参数传递
    flags = []  # 存储各地洞的状态，flag[i]=1 表示第i个地洞有老鼠
    # 将地洞定义为按钮控件，并放至游戏子布局
    for i in range(25):
        exec("mouse{}Btn=QPushButton()".format(i))
        exec("mouse{}Btn.setMinimumHeight(50)".format(i))  # 设置地洞控件最小高度
        exec("mouse{}Btn.setStyleSheet('border-image:url({})')".format(i, 'hole.jpg'))  ## 地洞图片，置于根目录下
        exec("holes.append(mouse{}Btn)".format(i))  # 将地洞控件加入holes
        flags.append(0)
    for i in range(5):
        for j in range(5):
            x = 5 * i + j
            exec("gameSublayout.addWidget(mouse{}Btn, {}, {})".format(x, i, j))

    # 定义说明子布局的各控件
    self.onGaming = 0  # 是否在“游戏中"状态，onGaming=1表示目前正在游戏中
    self.score = 0  # 击中老鼠次数
    self.missing = 0  # 逃离老鼠次数
    startBtn = QPushButton("开始游戏")
    scoreLabel = QLabel('击中数')
    scoreEdit = QLabel()
    scoreEdit.setFrameStyle(1)
    missingLabel = QLabel('逃离数')
    missingEdit = QLabel()
    missingEdit.setFrameStyle(1)
    remainingTimeLabel = QLabel('剩余时间')
    remainingTimeEdit = QLabel()
    remainingTimeEdit.setFrameStyle(1)
    # 将控件放到说明子布局
    introSublayout.addWidget(startBtn)
    introSublayout.addWidget(scoreLabel)
    introSublayout.addWidget(scoreEdit)
    introSublayout.addWidget(missingLabel)
    introSublayout.addWidget(missingEdit)
    introSublayout.addWidget(remainingTimeLabel)
    introSublayout.addWidget(remainingTimeEdit)
    # 计时器
    timer = QTimer()  # 全局计时器
    mouseTimer = QTimer()  # 地鼠出现时间计时器
    remainingTimer = QTimer()
    # 信号与槽函数
    startBtn.clicked.connect(
        lambda: self.gameStart(holes, flags, timer, mouseTimer, remainingTimer, scoreEdit, missingEdit))  # 开始游戏
    timer.timeout.connect(lambda: self.gameEnd(timer, mouseTimer, holes))  # 游戏时间结束
    for btn in holes:
        btn.clicked.connect(lambda: self.hit(holes, flags, mouseTimer, scoreEdit))
    mouseTimer.timeout.connect(lambda: self.mouseTimeout(holes, flags, missingEdit))  # 一轮老鼠显示时间结束
    remainingTimer.timeout.connect(lambda: self.show_remainingTime(timer, remainingTimeEdit))  # 每秒刷新剩余时间

    layout.addLayout(gameSublayout)
    layout.addLayout(introSublayout)
    self.stack7.setLayout(layout)


# 打地鼠游戏开始槽函数
# 功能：单击“开始游戏”按键，开始计时
def gameStart(self, holes, flags, timer, mouseTimer, remainingTimer, scoreEdit, missingEdit):
    if self.onGaming == 1:  # 如果正在游戏中，点击开始游戏按钮无响应
        return
    # 初始化, 将该地洞设置成无老鼠状态, 状态设置成”游戏中“
    self.score = 0
    scoreEdit.setText(str(self.score))
    self.missing = 0
    missingEdit.setText(str(self.missing))
    self.onGaming = 1
    for index in range(25):
        holes[index].setStyleSheet('border-image:url("hole.jpg")')
        flags[index] = 0
    # 单位毫秒 1000为1秒
    timer.start(30 * 1000)  # 游戏总时长30秒
    mouseTimer.start(1.5 * 1000)  # 老鼠出现的时长1.5秒
    remainingTimer.start(1000)  # 剩余时长每一秒更新一次
    self.setCursor(QCursor(QPixmap("hammer.png")))  # 将鼠标设成锤子形状


# 打地鼠游戏结束槽函数
# 功能：游戏时间到后，计数器停止工作，状态设为未在游戏中, 显示”game over“
def gameEnd(self, timer, mouseTimer, holes):
    timer.stop()
    mouseTimer.stop()
    self.onGaming = 0
    self.setCursor(Qt.ArrowCursor)
    holes[11].setStyleSheet('border-image:url("black_game.png")')
    holes[12].setStyleSheet('border-image:url("black.png")')
    holes[13].setStyleSheet('border-image:url("black_over.png")')


# 打击动作的槽函数
# 功能： 若打击的是老鼠，则积一分，并随机挑选地洞显示新的老鼠
def hit(self, holes, flags, mouseTimer, scoreEdit):
    if self.onGaming == 0:  # 状态为”未在游戏中“时，按键无响应
        return
    sender = self.sender()
    index = holes.index(sender)  # 找出是哪个地洞被打击
    if flags[index] == 0:  # 检查该地洞是否有老鼠
        return
    holes[index].setStyleSheet('border-image:url("hittedMouse.jpg")')
    mouseTimer.stop()
    flags[index] = 0.5  # 将该地洞设置成老鼠被打的状态
    self.score += 1  # 积一分
    scoreEdit.setText(str(self.score))
    # 以系统时间为种子，随机选取一个地洞安排老鼠
    seed(time())
    index = randint(0, 24)
    holes[index].setStyleSheet('border-image:url("mouse.jpg")')
    flags[index] = 1
    mouseTimer.start(1.5 * 1000)


# 老鼠显示时间结束槽函数
# 功能： 随机选中地洞，显示老鼠
def mouseTimeout(self, holes, flags, missingEdit):
    # 找到目前是哪个地洞有老鼠，时间到后有老鼠说明该老鼠是逃脱的，逃脱数加一，并还原成无老鼠状态
    for index in range(25):
        if flags[index] == 1:
            self.missing += 1
            missingEdit.setText(str(self.missing))
            holes[index].setStyleSheet('border-image:url("hole.jpg")')
            flags[index] = 0
        if flags[index] == 0.5:
            holes[index].setStyleSheet('border-image:url("hole.jpg")')
            flags[index] = 0
    # 以系统时间为种子，随机选取一个地洞安排老鼠
    seed(time())
    index = randint(0, 24)
    holes[index].setStyleSheet('border-image:url("mouse.jpg")')
    flags[index] = 1
    mouseTimer = self.sender()
    mouseTimer.start(1.5 * 1000)


# 更新剩余时间槽函数
# 功能： 每隔一秒更新游戏剩余时间
def show_remainingTime(self, timer, remainingTimeEdit):
    remaintime = int(round(timer.remainingTime() / 1000, 0))
    remainingTimeEdit.setText(str(remaintime) + "秒")
    self.sender().start(1000)