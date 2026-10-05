# Arduino IDE + ESP32 环境准备

## 1. 安装 Arduino IDE

从 Arduino 官方网站下载并安装当前版本的 Arduino IDE。

## 2. 添加 ESP32 开发板索引

打开 `文件 > 首选项`，将下面的稳定版地址加入“附加开发板管理器网址”：

```text
https://espressif.github.io/arduino-esp32/package_esp32_index.json
```

如果网络访问 GitHub 或 Espressif 官方地址较慢，可使用 Espressif 文档中提供的中国镜像：

```text
https://jihulab.com/esp-mirror/espressif/arduino-esp32/-/raw/gh-pages/package_esp32_index_cn.json
```

## 3. 安装开发板支持包

1. 打开 `工具 > 开发板 > 开发板管理器`。
2. 搜索 `esp32`。
3. 安装 Espressif Systems 提供的 `esp32` 平台。
4. 安装完成后重启 Arduino IDE。

## 4. 选择开发板和串口

1. 使用 USB 数据线连接 ESP32 开发板。
2. 在 `工具 > 开发板` 中选择与实物型号匹配的开发板。
3. 在 `工具 > 端口` 中选择开发板对应的 COM 端口。
4. 如果上传时卡在连接阶段，按住开发板上的 `BOOT` 键，看到开始连接后松开。

## 5. 编译并上传示例

打开 `src/esp32_blink/esp32_blink.ino`，点击“验证”编译，再点击“上传”写入开发板。

上传成功后，串口监视器可设置为 `115200` 波特率；程序会输出 LED 状态变化。

## 6. 常见问题

- 没有串口：检查 USB 数据线是否支持数据传输，并安装开发板所需的 USB 转串口驱动。
- 找不到开发板包：检查开发板索引地址，关闭并重新打开开发板管理器。
- 上传超时：确认端口没有被其他串口工具占用，必要时按住 `BOOT` 键重试。

安装依据：Espressif Arduino-ESP32 官方安装文档：
https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html
