# 页面6的布局设计
# 功能： 实现24点游戏
def stack6ui(self):
    layout = QVBoxLayout()
    card_layout = QHBoxLayout()
    op_layout = QGridLayout()

    # 纸牌的图片的文件名，存放于根目录下
    card_figure = ['card_background.jpg', 'cardA.jpg', 'card2.jpg', 'card3.jpg',
                   'card4.jpg', 'card5.jpg', 'card6.jpg', 'card7.jpg', 'card8.jpg',
                   'card9.jpg', 'card10.jpg', 'cardJ.jpg', 'cardQ.jpg', 'cardK.jpg']
    # 设置显示卡片的子布局
    # 定义显示卡片的控件
    card1 = QLabel('卡片1')
    card2 = QLabel('卡片2')
    card3 = QLabel('卡片3')
    card4 = QLabel('卡片4')

    for card in [card1, card2, card3, card4]:
        card.setFrameStyle(1)
        card.setStyleSheet("border-image:url('card_background.jpg')")
        card_layout.addWidget(card)
    card_layout.setSpacing(40)

    # 设置操作区域的子布局
    # 定义控件
    introStr = '24点游戏规则：\n 点击”开始游戏“，随机发放4张扑克牌（其中A对应1，J对应11，Q对应12，K对应13） \n' \
               ' 对纸牌对应的数字仅允许使用“+，-，*，/，（）”运算符 使运算结果为24 \n' \
               ' 注意：4张纸牌的数字都要使用且每张只允许使用1次；游戏允许重复提交。 '
    introLabel = QLabel(introStr)
    outputLabel = QLabel()  # 显示结果
    startButton = QPushButton('开始游戏')
    inputEdit = QLineEdit()
    inputEdit.setPlaceholderText('在此输入你的公式,注意需切换至英文')
    submitButton = QPushButton('提交')
    # 将控件插入操作子布局
    op_layout.addWidget(introLabel, 0, 0, 1, 3)
    op_layout.addWidget(startButton, 0, 3)
    op_layout.addWidget(inputEdit, 1, 0, 1, 3)
    op_layout.addWidget(submitButton, 1, 3)
    op_layout.addWidget(outputLabel, 2, 0, 1, 3)

    startButton.clicked.connect(lambda: self.start24Click([card1, card2, card3, card4], card_figure, inputEdit))
    submitButton.clicked.connect(lambda: self.submit24Click(inputEdit, outputLabel, [card1, card2, card3, card4]))

    # 设置总布局
    layout.addLayout(card_layout)
    layout.addLayout(op_layout)
    # 将总布局应用到页面5
    self.stack6.setLayout(layout)


# 开始按键的槽函数
# 功能： 单击“开始游戏”按键， 发牌
def start24Click(self, cd, cd_figure, inputEdit):
    seed(time())
    for i in range(4):
        num = randint(1, 13)
        cd[i].setText(str(num))
        cd[i].setStyleSheet("border-image:url('" + cd_figure[num] + "')")
    inputEdit.clear()  # 清空输入框


# 提交键槽函数
# 功能： 单击“提交”按键，检验用户输入的公式是否符合规则且结果为24，并输出
def submit24Click(self, inLine, outLabel, cd):
    inStr = inLine.text()
    # 储存允许存在于公式中的字符
    ch_valid = ['+', '-', '*', '/', '(', ')', '1']  # 1用作十位的抵消
    for card in cd:
        ch_valid.append(card.text())  # 将纸牌上的数字放入
    # 检验输入的公式是否符合游戏规则
    preCh = '0'  # 记录前一个字符，当前一个字符为1时，可能是一个两位数
    for ch in inStr:
        try:
            eval(ch)  # 运算符等特殊符号eval后报错
        except:
            if ch_valid.count(ch) == 0:
                outLabel.setText('抱歉，您的输入不符合游戏规则！')
                return
        else:
            if (preCh == '1') and (eval(ch) in range(4)):
                ch = preCh + ch  # 此处应该是一个两位数，不能拆开
                ch_valid.append('1')  # 补偿前一个字符在上一个循环的删除操作
            if ch_valid.count(ch) == 0:
                outLabel.setText('抱歉，您的输入不符合游戏规则！')
                return
            if eval(ch) in range(1, 14):
                ch_valid.remove(ch)  # 将数字删除
        finally:
            preCh = ch  # 更新前一个字符，以便进入下一个循环
    # 检验纸牌上的数字是否都用了
    if ch_valid != ['+', '-', '*', '/', '(', ')', '1']:
        outLabel.setText('抱歉，您未使用所有纸牌的数字！')
        return
    # 检验输入的公式结果是否为24
    try:
        eval(inStr)
    except:
        outLabel.setText('抱歉，您输入的公式无法运算，请检查运算符的排列！')
    else:
        if eval(inStr) == 24:
            outLabel.setText('恭喜，您成功了！')
        else:
            outLabel.setText('抱歉，您输入的公式结果不等于24！')
