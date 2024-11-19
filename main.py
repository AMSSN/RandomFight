import json
import random
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
import RandomUI


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = RandomUI.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('muscle.ico'))  # 设置图标
        self.setWindowTitle("RandomFight")  # 设置窗口名称
        # 进度条相关设置
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        # 主体参数
        self.player = []
        self.goal = []
        self.reward = []
        self.base_number = []
        self.multiplying = []
        self.result1 = ""
        self.result2 = ""
        self.result3 = ""
        self.config_path = "config.json"
        self.load_default_configuration()
        self.random_goal = ""
        self.random_reward = ""
        self.random_base_number = ""
        self.random_multiplying = ""
        # 默认设置
        self.set_connect()
        # 其他设置
        self.input_dir_value = None
        self.ui.comboBox.setCurrentIndex(1)

    def load_default_configuration(self, config_path="config.json"):
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
            # 假设配置文件中有 player, goal, reward, base_number 等字段
            self.player = config.get('player', [])
            self.goal = config.get('goal', [])
            self.reward = config.get('reward', [])
            self.base_number = config.get('base_number', [])
            self.multiplying = config.get('multiplying', [])
            # 输出到文本框
            player = "、".join(self.player)
            self.ui.plainTextEdit.appendPlainText(f"玩家:{player}")
            goal = "、".join(self.goal)
            self.ui.plainTextEdit.appendPlainText(f"目标:{goal}")
            reward = "、".join(self.reward)
            self.ui.plainTextEdit.appendPlainText(f"奖励:{reward}")
            base_number = "、".join(map(str, self.base_number))
            self.ui.plainTextEdit.appendPlainText(f"个数:{base_number}")

            for i in range(len(self.multiplying)):
                _text = f"{self.ui.comboBox.itemText(i)}*{self.multiplying[i]}"
                self.ui.plainTextEdit.appendPlainText(_text)
            self.ui.plainTextEdit.appendPlainText("------------------------")
        except FileNotFoundError:
            QMessageBox.about(self, "提示", f"配置文件 {config_path} 未找到")

        except json.JSONDecodeError:
            QMessageBox.about(self, "提示", f"配置文件 {config_path} 格式错误")

    def load_configuration(self):
        self.input_dir_value, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口部件
            "选取配置文件",  # 对话框标题
            ".",  # 起始路径
            "JSON Files (*.json);;All Files (*)"  # 文件过滤器
        )
        if self.input_dir_value:
            self.ui.plainTextEdit.setPlainText("")
            self.ui.plainTextEdit.appendPlainText(f"当前配置文件:{self.input_dir_value}")
            self.load_default_configuration(self.input_dir_value)
            # print(self.input_dir_value)
        else:
            QMessageBox.about(self, "提示", "请检查参数")

    def set_connect(self):
        self.ui.pushButton_input.clicked.connect(self.load_configuration)
        self.ui.pushButton_go_1.clicked.connect(self.go1)
        self.ui.pushButton_go_2.clicked.connect(self.go2)
        self.ui.pushButton_go_3.clicked.connect(self.go3)
        self.ui.comboBox.currentIndexChanged.connect(self.change_comboBox)

    def change_comboBox(self):
        self.ui.plainTextEdit.appendPlainText(
            f"该选手的段位是{self.ui.comboBox.currentText()}，倍率为{self.multiplying[int(self.ui.comboBox.currentIndex())]}")

    def go1(self):
        """ Who ? """
        self.random_goal = random.choice(self.goal)
        self.ui.plainTextEdit.appendPlainText(f"有请 {self.random_goal} 的人")
        self.result1 = f"有请 {self.random_goal} 的人"

    def go2(self):
        """ Do What ? """
        self.random_reward = random.choice(self.reward)
        self.ui.plainTextEdit.appendPlainText(f"完成 {self.random_reward}")
        self.result2 = f"完成 {self.random_reward} "

    def go3(self):
        """ How Much """
        self.ui.label_input_2.setText("")
        # random_goal = random.choice(self.goal)
        # random_reward = random.choice(self.reward)
        self.random_base_number = random.choice(self.base_number)
        self.random_multiplying = self.multiplying[int(self.ui.comboBox.currentIndex())]
        total = self.random_base_number * self.random_multiplying
        self.result3 = self.result1 + self.result2 + f"共计{self.random_base_number}*{self.random_multiplying}={total}个"
        self.ui.plainTextEdit.appendPlainText(f"共计{self.random_base_number}*{self.random_multiplying}={total}个")
        self.ui.label_input_2.setText(self.result3)
        self.ui.plainTextEdit.appendPlainText("------------------------")


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
