from machine import UART, Pin
import time


class esp_uart:
    """
    初始化 UART 通信與 ESP32 並提供控制 Wi-Fi 功能的函數使用 AT 命令。
    - bus_num: UART 总线号
    - baudrate: 通信速率，默认为 ESP32 的 115200
    """

    def __init__(self, bus_num):
        self.uart = UART(
            bus_num,
            baudrate=115200,
            tx=Pin(8),
            rx=Pin(9),
            cts=Pin(10),
            rts=Pin(11),
            txbuf=1024,
            rxbuf=1024,
        )
        self.sendAT("ATE0")  # 关闭回声

        # 格式化标题和分割线
        self.titles = [
            "Index",
            "Type",
            "SSID",
            "Signal Strength",
            "MAC Address",
            "Signal",
            "Min Speed",
            "Max Speed",
            "Pass Type",
            "Wi-Fi Mode",
            "SSID Visible",
        ]

    def sendAT(self, cmd):
        """
        向 ESP32 发送 AT 命令并打印响应。
        - cmd: 要发送的 AT 命令（不带 'AT+' 前缀）
        """
        try:
            self.uart.write(f"AT+{cmd}\r\n")
            while self.uart.any() == 0:
                time.sleep_ms(1)
            time.sleep_ms(50)  # 防止数据丢失
            self.response_b = self.uart.read()  # 原始响应
            self.response = self.response_b.decode("utf-8")  # 转换为字符串
            return self.response
        except Exception as e:
            print(f"Error: {e}")

    def list_wifi(self):
        """
        列出可用的 Wi-Fi 网络，允许用户选择一个，输入密码，并尝试连接。
        """
        try:
            self.sendAT("CWMODE=1")  # 设置 Wi-Fi 模式为站点
            self.sendAT("CWLAP")  # 列出可用的 AP
            self.print_wifi()  # 打印 Wi-Fi 网络列表

            # 用户选择网络
            ssid = input("Enter network SSID index: ")
            password = input("Enter password: ")

            # 尝试连接
            self.sendAT(f'CWJAP="{ssid}","{password}"')
            ip_response = self.sendAT("CIFSR")  # 获取 IP 地址
            print("Connected, IP address:\n", ip_response)
        except Exception as e:
            print(f"Error: {e}")

    def left_justify(self, s="", width=0):
        """返回左对齐的字符串，如果需要，在右侧填充空格至指定宽度。"""
        return s + " " * (width - len(s))

    def center_justify(self, s="", width=0):
        """返回居中对齐的字符串，如果需要，在两侧填充空格至指定宽度。"""
        padding = (width - len(s)) // 2
        return " " * padding + s + " " * (width - len(s) - padding)

    def print_wifi(self):
        """
        格式化打印 Wi-Fi 网络列表。
        列出所有找到的 Wi-Fi 以供选择。
        """
        try:
            lines = self.response.split("\n")
            self.SSID_list = []  # 重置SSID列表
            widths = [0] * 11  # 预设每列的最大宽度，包括索引列

            # 计算每列的最大宽度
            for line in lines[1:-1]:  # 排除起始和结束行
                elements = line.split(",")
                if len(elements) > 1:
                    self.SSID_list.append(elements[1].strip('"'))  # 存储SSID
                else:
                    continue  # 如果没有足够的元素，跳过这行

                widths[0] = max(
                    widths[0], len(str(len(self.SSID_list)))
                )  # 更新索引列宽度
                for i, element in enumerate(elements):
                    if i + 1 < len(widths):  # 确保不会超出widths的范围
                        element_str = element.strip('"')  # 移除双引号
                        widths[i + 1] = max(
                            widths[i + 1], len(element_str), len(self.titles[i + 1])
                        )

            # 格式化并打印标题、分隔线和数据行
            header = "|".join(
                self.center_justify(title, widths[i] + 4)
                for i, title in enumerate(self.titles)
            )
            divider = "-" * len(header)
            print(header)
            print(divider)

            for idx, line in enumerate(lines[1:-1], start=1):
                elements = line.split(",")
                if len(elements) < len(self.titles) - 1:
                    continue  # 如果没有足够的元素，跳过这行
                row_elements = [str(idx)] + elements
                row = "|".join(
                    self.center_justify(
                        row_elements[i].strip().strip('"'), widths[i] + 4
                    )
                    for i in range(len(self.titles))
                )
                print(row)

            print(f"what we have the name of network: {self.SSID_list}")
        except Exception as e:
            print(f"Error: {e}")


# 测试代码
if __name__ == "__main__":
    esp = esp_uart(1)  # 初始化 esp_uart 对象用于 UART 总线 1
    esp.list_wifi()  # 调用
