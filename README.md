# ESP32 Arduino 入门工程

本仓库用于第 6 周“嵌入式计算”课程的开发环境准备和 ESP32 入门验证。

## 工程内容

- `src/esp32_blink/esp32_blink.ino`：ESP32 板载 LED 闪烁示例
- `docs/setup.md`：Arduino IDE 与 ESP32 支持包安装、编译和上传步骤

## 使用方式

1. 安装 Arduino IDE。
2. 按 `docs/setup.md` 安装 ESP32 开发板支持包。
3. 在 Arduino IDE 中打开 `src/esp32_blink/esp32_blink.ino`。
4. 根据实际开发板选择 `工具 > 开发板` 和串口。
5. 编译并上传，观察板载 LED 是否闪烁。

注意：不同 ESP32 开发板的板载 LED 引脚可能不同。如果默认引脚无法点亮，请根据开发板资料修改代码中的 `LED_PIN`。

## 提交

将本目录推送到自己的 GitHub、Gitee 或课程要求的 Git 平台后，把仓库网页地址提交到学习通。
