from PySide2.QtCore import QStateMachine, QState, QPropertyAnimation
from PySide2.QtWidgets import *

# 创建 QStateMachine 对象
machine = QStateMachine(self)

# 创建两个 QState 对象
state1 = QState()
state2 = QState()

# 创建 QPropertyAnimation 对象，并指定要动画的属性
animation = QPropertyAnimation(button, b"geometry")
animation.setDuration(1000)
animation.setStartValue(QRect(0, 0, 100, 30))
animation.setEndValue(QRect(250, 250, 100, 30))

# 将动画添加到状态中
state1.addTransition(button.clicked, state2)
state1.addAnimation(animation)

# 将状态添加到状态机中
machine.addState(state1)
machine.addState(state2)

# 启动状态机
machine.start()
