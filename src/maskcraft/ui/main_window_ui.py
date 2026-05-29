# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    """主窗口 UI 结构。

    该文件由 ``pyside6-uic.exe`` 根据 ``main_window.ui`` 生成，用于创建控件树和
    翻译界面文本。
    """

    def setupUi(self, MainWindow):
        """创建主窗口控件。

        :param MainWindow: 需要绑定 UI 的主窗口对象。
        """

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(980, 660)
        MainWindow.setMinimumSize(QSize(900, 620))
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background: #f6f7f9;\n"
"}\n"
"QWidget {\n"
"    color: #20242a;\n"
"    font-family: \"Microsoft YaHei UI\", \"Segoe UI\", sans-serif;\n"
"    font-size: 14px;\n"
"}\n"
"QLabel#titleLabel {\n"
"    color: #111827;\n"
"    font-size: 26px;\n"
"    font-weight: 700;\n"
"}\n"
"QLabel#subtitleLabel {\n"
"    color: #5b6472;\n"
"    font-size: 14px;\n"
"}\n"
"QGroupBox {\n"
"    background: #ffffff;\n"
"    border: 1px solid #d9dee7;\n"
"    border-radius: 8px;\n"
"    margin-top: 18px;\n"
"    padding: 18px 16px 14px 16px;\n"
"    font-size: 15px;\n"
"    font-weight: 600;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 14px;\n"
"    padding: 0 8px;\n"
"    color: #111827;\n"
"}\n"
"QLineEdit {\n"
"    background: #ffffff;\n"
"    border: 1px solid #cbd3df;\n"
"    border-radius: 6px;\n"
"    padding: 8px 10px;\n"
"    selection-background-color: #2f6feb;\n"
"}\n"
"QLineEdit:focus {\n"
"    border-color: #2f6feb;\n"
"}\n"
"QLineEdit[readOnly=\"true\"] {\n"
"    "
                        "background: #f9fafb;\n"
"    color: #374151;\n"
"}\n"
"QPushButton {\n"
"    background: #ffffff;\n"
"    border: 1px solid #cbd3df;\n"
"    border-radius: 6px;\n"
"    padding: 8px 14px;\n"
"    min-height: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"    background: #f3f6fb;\n"
"}\n"
"QPushButton:pressed {\n"
"    background: #e8edf6;\n"
"}\n"
"QPushButton:disabled {\n"
"    color: #9aa3af;\n"
"    background: #f3f4f6;\n"
"}\n"
"QPushButton#generateButton {\n"
"    background: #1f6feb;\n"
"    border-color: #1f6feb;\n"
"    color: #ffffff;\n"
"    font-weight: 600;\n"
"}\n"
"QPushButton#generateButton:hover {\n"
"    background: #1a5fd0;\n"
"}\n"
"QTextEdit {\n"
"    background: #111827;\n"
"    color: #d1d5db;\n"
"    border: 1px solid #111827;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    font-family: \"Cascadia Mono\", Consolas, monospace;\n"
"    font-size: 12px;\n"
"}\n"
"QProgressBar {\n"
"    border: 1px solid #d9dee7;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background:"
                        " #ffffff;\n"
"    min-height: 10px;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background: #1f6feb;\n"
"    border-radius: 4px;\n"
"}")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.mainLayout = QVBoxLayout(self.centralWidget)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(32, 28, 32, 28)
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setSpacing(6)
        self.headerLayout.setObjectName(u"headerLayout")
        self.titleLabel = QLabel(self.centralWidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.headerLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.centralWidget)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setWordWrap(True)

        self.headerLayout.addWidget(self.subtitleLabel)


        self.mainLayout.addLayout(self.headerLayout)

        self.inputGroupBox = QGroupBox(self.centralWidget)
        self.inputGroupBox.setObjectName(u"inputGroupBox")
        self.inputGridLayout = QGridLayout(self.inputGroupBox)
        self.inputGridLayout.setObjectName(u"inputGridLayout")
        self.inputGridLayout.setHorizontalSpacing(10)
        self.inputGridLayout.setVerticalSpacing(12)
        self.imagePathLabel = QLabel(self.inputGroupBox)
        self.imagePathLabel.setObjectName(u"imagePathLabel")

        self.inputGridLayout.addWidget(self.imagePathLabel, 0, 0, 1, 1)

        self.imagePathLineEdit = QLineEdit(self.inputGroupBox)
        self.imagePathLineEdit.setObjectName(u"imagePathLineEdit")
        self.imagePathLineEdit.setMinimumSize(QSize(560, 0))
        self.imagePathLineEdit.setReadOnly(True)

        self.inputGridLayout.addWidget(self.imagePathLineEdit, 0, 1, 1, 1)

        self.selectImageButton = QPushButton(self.inputGroupBox)
        self.selectImageButton.setObjectName(u"selectImageButton")
        self.selectImageButton.setMinimumSize(QSize(104, 0))

        self.inputGridLayout.addWidget(self.selectImageButton, 0, 2, 1, 1)

        self.videoPathLabel = QLabel(self.inputGroupBox)
        self.videoPathLabel.setObjectName(u"videoPathLabel")

        self.inputGridLayout.addWidget(self.videoPathLabel, 1, 0, 1, 1)

        self.videoPathLineEdit = QLineEdit(self.inputGroupBox)
        self.videoPathLineEdit.setObjectName(u"videoPathLineEdit")
        self.videoPathLineEdit.setMinimumSize(QSize(560, 0))
        self.videoPathLineEdit.setReadOnly(True)

        self.inputGridLayout.addWidget(self.videoPathLineEdit, 1, 1, 1, 1)

        self.selectVideoButton = QPushButton(self.inputGroupBox)
        self.selectVideoButton.setObjectName(u"selectVideoButton")
        self.selectVideoButton.setMinimumSize(QSize(104, 0))

        self.inputGridLayout.addWidget(self.selectVideoButton, 1, 2, 1, 1)


        self.mainLayout.addWidget(self.inputGroupBox)

        self.actionGroupBox = QGroupBox(self.centralWidget)
        self.actionGroupBox.setObjectName(u"actionGroupBox")
        self.actionLayout = QVBoxLayout(self.actionGroupBox)
        self.actionLayout.setSpacing(12)
        self.actionLayout.setObjectName(u"actionLayout")
        self.actionButtonLayout = QHBoxLayout()
        self.actionButtonLayout.setObjectName(u"actionButtonLayout")
        self.generateButton = QPushButton(self.actionGroupBox)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setMinimumSize(QSize(120, 0))

        self.actionButtonLayout.addWidget(self.generateButton)

        self.statusLabel = QLabel(self.actionGroupBox)
        self.statusLabel.setObjectName(u"statusLabel")

        self.actionButtonLayout.addWidget(self.statusLabel)

        self.actionSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actionButtonLayout.addItem(self.actionSpacer)


        self.actionLayout.addLayout(self.actionButtonLayout)

        self.taskProgressBar = QProgressBar(self.actionGroupBox)
        self.taskProgressBar.setObjectName(u"taskProgressBar")
        self.taskProgressBar.setMaximum(100)
        self.taskProgressBar.setValue(0)
        self.taskProgressBar.setTextVisible(False)

        self.actionLayout.addWidget(self.taskProgressBar)


        self.mainLayout.addWidget(self.actionGroupBox)

        self.resultGroupBox = QGroupBox(self.centralWidget)
        self.resultGroupBox.setObjectName(u"resultGroupBox")
        self.resultLayout = QVBoxLayout(self.resultGroupBox)
        self.resultLayout.setSpacing(10)
        self.resultLayout.setObjectName(u"resultLayout")
        self.resultLinkLayout = QHBoxLayout()
        self.resultLinkLayout.setObjectName(u"resultLinkLayout")
        self.resultUrlLineEdit = QLineEdit(self.resultGroupBox)
        self.resultUrlLineEdit.setObjectName(u"resultUrlLineEdit")
        self.resultUrlLineEdit.setMinimumSize(QSize(560, 0))
        self.resultUrlLineEdit.setReadOnly(True)

        self.resultLinkLayout.addWidget(self.resultUrlLineEdit)

        self.copyResultButton = QPushButton(self.resultGroupBox)
        self.copyResultButton.setObjectName(u"copyResultButton")
        self.copyResultButton.setMinimumSize(QSize(104, 0))
        self.copyResultButton.setEnabled(False)

        self.resultLinkLayout.addWidget(self.copyResultButton)

        self.openResultButton = QPushButton(self.resultGroupBox)
        self.openResultButton.setObjectName(u"openResultButton")
        self.openResultButton.setMinimumSize(QSize(104, 0))
        self.openResultButton.setEnabled(False)

        self.resultLinkLayout.addWidget(self.openResultButton)


        self.resultLayout.addLayout(self.resultLinkLayout)

        self.logTextEdit = QTextEdit(self.resultGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setReadOnly(True)

        self.resultLayout.addWidget(self.logTextEdit)


        self.mainLayout.addWidget(self.resultGroupBox)

        MainWindow.setCentralWidget(self.centralWidget)
        QWidget.setTabOrder(self.selectImageButton, self.selectVideoButton)
        QWidget.setTabOrder(self.selectVideoButton, self.generateButton)
        QWidget.setTabOrder(self.generateButton, self.copyResultButton)
        QWidget.setTabOrder(self.copyResultButton, self.openResultButton)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        """翻译主窗口文本。

        :param MainWindow: 需要翻译文本的主窗口对象。
        """

        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MaskCraft", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"MaskCraft", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u4e00\u5f20\u56fe\u7247\u548c\u4e00\u6bb5\u53c2\u8003\u89c6\u9891\uff0c\u751f\u6210\u4efb\u52a1\u5b8c\u6210\u540e\u4f1a\u5728\u4e0b\u65b9\u663e\u793a API \u8fd4\u56de\u7684\u89c6\u9891\u94fe\u63a5\u3002", None))
        self.inputGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u7d20\u6750", None))
        self.imagePathLabel.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None))
        self.imagePathLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"JPG / PNG / BMP / WebP\uff0c\u6700\u5927 5MB", None))
        self.selectImageButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u56fe\u7247", None))
        self.videoPathLabel.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891", None))
        self.videoPathLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"MP4 / AVI / MOV\uff0c2-30 \u79d2\uff0c\u6700\u5927 200MB", None))
        self.selectVideoButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u89c6\u9891", None))
        self.actionGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
        self.generateButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u751f\u6210", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"\u7b49\u5f85\u9009\u62e9\u7d20\u6750", None))
        self.resultGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u7ed3\u679c", None))
        self.resultUrlLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u6210\u529f\u540e\uff0c\u8fd9\u91cc\u4f1a\u663e\u793a\u8fd4\u56de\u7684\u89c6\u9891\u94fe\u63a5", None))
        self.copyResultButton.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u94fe\u63a5", None))
        self.openResultButton.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u94fe\u63a5", None))
        self.logTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u65e5\u5fd7\u4f1a\u663e\u793a\u5728\u8fd9\u91cc", None))
    # retranslateUi

