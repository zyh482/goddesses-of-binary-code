# 页面三的布局设计
# 页面三的功能： 绘制函数图像
def stack3ui(self):
    layout = QHBoxLayout()
    sublayout = QGridLayout()

    figureEdit = QLabel('绘图区')
    figureEdit.setMinimumWidth(350)
    figureEdit.setFrameStyle(1)
    # 定义注释控件
    funcLabel = QLabel('请输入函数：')
    lowerBoundLabel = QLabel('区间左端点：')
    upperBoundLabel = QLabel('区间右端点：')
    # 定义输入控件
    funcEdit = QTextEdit()
    lowerBoundEdit = QLineEdit()
    upperBoundEdit = QLineEdit()
    plotButton = QPushButton('开始绘图')

    funcEdit.setPlaceholderText("目前仅支持自变量为x的一元函数，且无需输入‘y='（注意python语言 幂运算符为**）")
    lowerBoundEdit.setPlaceholderText('-5')
    upperBoundEdit.setPlaceholderText('5')
    # 对子布局的控件进行排列
    sublayout.addWidget(funcLabel, 1, 0, 1, 2)
    sublayout.addWidget(funcEdit, 2, 0, 1, 2)
    sublayout.addWidget(lowerBoundLabel, 3, 0, 1, 1)
    sublayout.addWidget(upperBoundLabel, 3, 1, 1, 1)
    sublayout.addWidget(lowerBoundEdit, 4, 0, 1, 1)
    sublayout.addWidget(upperBoundEdit, 4, 1, 1, 1)
    sublayout.addWidget(plotButton, 5, 0, 1, 2)
    # 绘图按钮与画图函数连接起来
    plotButton.clicked.connect(lambda: self.plot_image(funcEdit, upperBoundEdit, lowerBoundEdit, figureEdit))
    # 设置总布局
    layout.addLayout(sublayout)
    layout.addWidget(figureEdit)
    # 将总布局应用到stack3
    self.stack3.setLayout(layout)


# 绘图按钮的槽函数
# 函数功能： 依据输入进行绘图，并插入到页面中
def plot_image(self, fEdit, uBoundEdit, lBoundEdit, outWin):
    if fEdit.toPlainText() == '':
        outWin.setText('未输入函数表达式')
        return
    a = -5 if lBoundEdit.text() == '' else eval(lBoundEdit.text())
    b = 5 if uBoundEdit.text() == '' else eval(uBoundEdit.text())
    if a >= b:
        outWin.setText('输入的区间不符合要求')
        return
    stepSize = min(0.1, (b - a) / 100)
    X = list(np.arange(a, b, stepSize))  # 定义域
    try:
        Y = list(eval(fEdit.toPlainText()) for x in X)  # 值域
    except:
        outWin.setText('输入的公式不符合要求，请重新输入！\n 检查输入的公式是否是一元变量x的多项式，且幂运算符为**')
    else:
        plt.figure()
        plt.plot(X, Y)
        plt.xlabel('x')
        plt.ylabel('y= ' + fEdit.toPlainText())
        plt.savefig('figure.jpg')  # 将图像保存为图片
        png = QPixmap('figure.jpg')  # 将图片插入到窗口
        outWin.setPixmap(png)
