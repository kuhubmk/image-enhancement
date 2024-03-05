from PySide6.QtCore import Qt
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QCheckBox, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #A52A2A; /* 棕色 */
            }
            QLabel, QSlider, QCheckBox, QPushButton, QLineEdit {
                color: white; /* 字体颜色 */
            }
            QPushButton {
                background-color: #8B4513; /* 更深的棕色, 按钮背景 */
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #A0522D; /* 鼠标悬浮时按钮的颜色 */
            }
            QPushButton:pressed {
                background-color: #8B4513; /* 鼠标按下时按钮的颜色 */
                border-style: inset;
            }
            QLineEdit {
                background-color: #A58F86; /* 指定输入框的颜色 */
                border: none;
                padding: 5px;
                border-radius: 5px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #A58F86;
                height: 8px; /* 滑块的高度 */
                background: #8B4513;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #DAA520;
                border: 1px solid #8B4513;
                width: 18px; /* 滑块的宽度 */
                margin: -2px 0; /* 滑块超出groove的大小 */
                border-radius: 10px;
            }
        """)

    def initUI(self):
        self.setWindowTitle('图像增强工具')
        self.resize(640, 480)

        mainLayout = QVBoxLayout()

        slidersLayout = QVBoxLayout()

        # Scale Slider
        self.scaleSlider = QSlider(Qt.Horizontal)
        self.scaleSlider.setMinimum(0)
        self.scaleSlider.setMaximum(100)
        self.scaleSlider.setTickPosition(QSlider.TicksBelow)
        self.scaleSlider.valueChanged.connect(self.updateScaleLabel)
        self.scaleLabel = QLabel('缩放: 100%')
        slidersLayout.addWidget(self.scaleLabel)
        slidersLayout.addWidget(self.scaleSlider)

        # Brightness Slider
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setTickPosition(QSlider.TicksBelow)
        self.brightnessSlider.valueChanged.connect(self.updateBrightnessLabel)
        self.brightnessLabel = QLabel('亮度: 0')
        slidersLayout.addWidget(self.brightnessLabel)
        slidersLayout.addWidget(self.brightnessSlider)

        # Contrast Slider
        self.contrastSlider = QSlider(Qt.Horizontal)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setTickPosition(QSlider.TicksBelow)
        self.contrastSlider.valueChanged.connect(self.updateContrastLabel)
        self.contrastLabel = QLabel('对比度: 0')
        slidersLayout.addWidget(self.contrastLabel)
        slidersLayout.addWidget(self.contrastSlider)

        # Sharpen Slider
        self.sharpenSlider = QSlider(Qt.Horizontal)
        self.sharpenSlider.setMinimum(0)
        self.sharpenSlider.setMaximum(100)
        self.sharpenSlider.setTickPosition(QSlider.TicksBelow)
        self.sharpenSlider.valueChanged.connect(self.updateSharpenLabel)
        self.sharpenLabel = QLabel('锐化: 0')
        slidersLayout.addWidget(self.sharpenLabel)
        slidersLayout.addWidget(self.sharpenSlider)

        # Saturation Slider
        self.saturationSlider = QSlider(Qt.Horizontal)
        self.saturationSlider.setMinimum(-100)
        self.saturationSlider.setMaximum(100)
        self.saturationSlider.setTickPosition(QSlider.TicksBelow)
        self.saturationSlider.valueChanged.connect(self.updateSaturationLabel)
        self.saturationLabel = QLabel('饱和度: 0')
        slidersLayout.addWidget(self.saturationLabel)
        slidersLayout.addWidget(self.saturationSlider)

        # Blur Slider
        self.blurSlider = QSlider(Qt.Horizontal)
        self.blurSlider.setMinimum(0)
        self.blurSlider.setMaximum(5)
        self.blurSlider.setTickPosition(QSlider.TicksBelow)
        self.blurSlider.valueChanged.connect(self.updateBlurLabel)
        self.blurLabel = QLabel('模糊: 0')
        slidersLayout.addWidget(self.blurLabel)
        slidersLayout.addWidget(self.blurSlider)

        topLayout = QHBoxLayout()

        self.rotateLeftCheckbox = QCheckBox('左转')
        self.rotateRightCheckbox = QCheckBox('右转')
        self.flipCheckbox = QCheckBox('倒转')
        topLayout.addWidget(self.rotateLeftCheckbox)
        topLayout.addWidget(self.rotateRightCheckbox)
        topLayout.addWidget(self.flipCheckbox)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(slidersLayout)

        # Read Folder
        fileLayout = QHBoxLayout()
        self.readLabel = QLabel('读取文件:')
        self.readLineEdit = QLineEdit()
        self.readBrowseButton = QPushButton('浏览')
        self.readBrowseButton.clicked.connect(self.selectReadFolder)
        fileLayout.addWidget(self.readLabel)
        fileLayout.addWidget(self.readLineEdit)
        fileLayout.addWidget(self.readBrowseButton)

        # Save Folder
        self.saveLabel = QLabel('保存文件:')
        self.saveLineEdit = QLineEdit()
        self.saveBrowseButton = QPushButton('浏览')
        self.saveBrowseButton.clicked.connect(self.selectSaveFolder)
        fileLayout.addWidget(self.saveLabel)
        fileLayout.addWidget(self.saveLineEdit)
        fileLayout.addWidget(self.saveBrowseButton)

        mainLayout.addLayout(fileLayout)

        # Enhance Button
        self.enhanceButton = QPushButton('执行')
        self.enhanceButton.clicked.connect(self.enhanceImage)
        mainLayout.addWidget(self.enhanceButton)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def updateScaleLabel(self):
        scale_value = self.scaleSlider.value()
        self.scaleLabel.setText(f'缩放: {scale_value}%')

    def updateBrightnessLabel(self):
        brightness_value = self.brightnessSlider.value()
        self.brightnessLabel.setText(f'亮度: {brightness_value}')

    def updateContrastLabel(self):
        contrast_value = self.contrastSlider.value()
        self.contrastLabel.setText(f'对比度: {contrast_value}')

    def updateSharpenLabel(self):
        sharpen_value = self.sharpenSlider.value()
        self.sharpenLabel.setText(f'锐化: {sharpen_value}')

    def updateSaturationLabel(self):
        saturation_value = self.saturationSlider.value()
        self.saturationLabel.setText(f'饱和度: {saturation_value}')

    def updateBlurLabel(self):
        blur_value = self.blurSlider.value()
        self.blurLabel.setText(f'模糊: {blur_value}')

    def selectReadFolder(self):
        # 打开文件夹选择对话框
        folderPath = QFileDialog.getExistingDirectory(self, "选择读取文件夹")
        if folderPath:
            self.readLineEdit.setText(folderPath)

    def selectSaveFolder(self):
        # 打开文件夹选择对话框
        folderPath = QFileDialog.getExistingDirectory(self, "选择保存文件夹")
        if folderPath:
            self.saveLineEdit.setText(folderPath)


    def enhanceImage(self):
        read_folder = self.readLineEdit.text()
        save_folder = self.saveLineEdit.text()
        if not os.path.exists(read_folder) or not os.path.isdir(read_folder):
            print("Read folder does not exist or is not a directory!")
            return
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for image_filename in os.listdir(read_folder):
            image_path = os.path.join(read_folder, image_filename)
            if os.path.isfile(image_path) and image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                with Image.open(image_path) as image:
                    # Scale
                    scale_factor = self.scaleSlider.value() / 100.0
                    if scale_factor > 0:  # 这里确保缩放比例大于0
                        width, height = image.size
                        new_size = (int(width * scale_factor), int(height * scale_factor))
                        if new_size[0] > 0 and new_size[1] > 0:  # 这里确保新的尺寸大于0
                            image = image.resize(new_size, Image.Resampling.LANCZOS)
                    else:
                        print("Scale factor is too small or slider not adjusted, skipping resizing.")

                    # Brightness
                    enhancer = ImageEnhance.Brightness(image)
                    value = (self.brightnessSlider.value() + 100) / 100  
                    image = enhancer.enhance(value)

                    # Contrast
                    enhancer = ImageEnhance.Contrast(image)
                    value = (self.contrastSlider.value() + 100) / 100
                    image = enhancer.enhance(value)

                    # Sharpen
                    enhancer = ImageEnhance.Sharpness(image)
                    value = (self.sharpenSlider.value() + 100) / 100
                    image = enhancer.enhance(value)

                    # Saturation
                    enhancer = ImageEnhance.Color(image)
                    value = (self.saturationSlider.value() + 100) / 100
                    image = enhancer.enhance(value)

                    # Blur
                    if self.blurSlider.value() > 0:
                        blur_amount = self.blurSlider.value()
                        image = image.filter(ImageFilter.GaussianBlur(blur_amount))

                    # Flip
                    if self.flipCheckbox.isChecked():
                        image = image.transpose(method=Image.FLIP_LEFT_RIGHT)

                    # Rotate
                    if self.rotateLeftCheckbox.isChecked() and self.rotateRightCheckbox.isChecked():
                        # If both are checked, do nothing
                        pass
                    elif self.rotateLeftCheckbox.isChecked():
                        image = image.rotate(90, expand=True)
                    elif self.rotateRightCheckbox.isChecked():
                        image = image.rotate(-90, expand=True)

                    save_path = os.path.join(save_folder, image_filename)
                    image.save(save_path)
                    print(f"Saved enhanced image to '{save_path}'")
        print("All images have been enhanced")

# 下面开始运行应用程序

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec()) 