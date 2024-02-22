from machine import UART, Pin
import time

# fmt: off

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
            txbuf=4096,
            rxbuf=4906,
        )
        self.sendAT("RST")  # reset
        self.sendAT("ATE0")  # 关闭回声
        self.SSID_list = []  # 存储SSID列表
        self.MAC_list = []  # 存储MAC地址列表
        self.sim_mode = 0

        # 格式化标题和分割线
        self.titles = [
            "Index",
            "Type",
            "SSID",
            "Sig amp",
            "MAC Address",
            "sig",
            "Min S",
            "Max S",
            "P Type",
            "Mode",
            "ID Vis",
        ]

        # # 格式化标题和分割线
        # self.titles = [
        #     "Index",
        #     "Type",
        #     "SSID",
        #     "Signal amp",
        #     "MAC Address",
        #     "sig",
        #     "Min Speed",
        #     "Max Speed",
        #     "Password Type",
        #     "Wi-Fi Mode",
        #     "SSID Visible",
        # ]

    def sendAT(self, cmd):
        """
        向 ESP32 发送 AT 命令并打印响应。
        - cmd: 要发送的 AT 命令（不带 'AT+' 前缀）
        """
        try:
            # 240222 this command will cause error, don't use
            # if self.uart.any() != 0:
            #     print(f'clean buffer if not empty: "{self.uart.read()}"')
            self.uart.write(f"AT+{cmd}\r\n")
            while self.uart.any() == 0:
                time.sleep_ms(1)
            time.sleep_ms(200)  # 防止数据丢失
            self.response_b = self.uart.read()  # 原始响应
            self.response = self.response_b.decode("utf-8")  # 转换为字符串
            print("send finished")
            print(f'by "{cmd}" getting \n"{self.response}"\n')
            return self.response
        except Exception as e:
            print(f"Error send AT using {cmd}: {e}")

    def list_wifi(self, justify0="center_justify"):
        """
        列出可用的 Wi-Fi 网络，允许用户选择一个，输入密码，并尝试连接。
        """
        try:
            self.sendAT("CWMODE=1")  # 设置 Wi-Fi 模式为站点
            # time.sleep(0.5)
            self.sendAT("CWLAP")  # 列出可用的 AP
            # need some time for loading the internet
            time.sleep(10)
            self.sendAT("CWLAP")  # 列出可用的 AP
            # self.sendAT("CWLAP")  # 列出可用的 AP
            self.print_wifi(justify=justify0)  # 打印 Wi-Fi 网络列表

        except Exception as e:
            print(f"Error list_wifi: {e}")

    def left_justify(self, s="", width=0):
        """返回左对齐的字符串，如果需要，在右侧填充空格至指定宽度。"""
        return s + " " * (width - len(s))

    def center_justify(self, s="", width=0):
        """返回居中对齐的字符串，如果需要，在两侧填充空格至指定宽度。"""
        padding = (width - len(s)) // 2
        return " " * padding + s + " " * (width - len(s) - padding)

    def print_wifi(self, justify="center_justify", print0=1):
        """
        格式化打印 Wi-Fi 网络列表。
        列出所有找到的 Wi-Fi 以供选择。
        justify: 用于选择对齐方式的参数，可以是 'left_justify' 或 'center_justify'
        """
        try:
            lines = self.response.split("\n")
            # print(f'lines {lines}')
            self.SSID_list.clear()  # 重置SSID列表
            self.MAC_list.clear()  # 重置MAC地址列表
            widths = [0] * len(self.titles)  # 预设每列的最大宽度，包括索引列

            # 计算每列的最大宽度
            for line in lines[1:-1]:  # 排除起始和结束行
                elements = line.split(",")
                if len(elements) > 1:  # 确保有足够的元素
                    self.SSID_list.append(elements[1].strip('"'))  # 存储SSID
                    self.MAC_list.append(elements[3].strip('"'))  # 存储MAC地址
                else:
                    continue  # 如果没有足够的元素，跳过这行

                widths[0] = max(
                    widths[0], len(str(len(self.SSID_list))) + 1
                )  # 更新索引列宽度并留出额外空间
                for i, element in enumerate(elements):
                    if i < len(self.titles) - 1:  # 确保不会超出标题的范围
                        element_str = element.strip('"')  # 移除双引号
                        widths[i + 1] = max(
                            widths[i + 1], len(element_str), len(self.titles[i + 1])
                        )
            if print0 != 0:
                # not to print if no print command, not print detail
                # only SSID list and index

                # 格式化并打印标题、分隔线和数据行
                justify_function = getattr(self, justify)  # 获取对齐函数
                header = "|".join(
                    justify_function(title, widths[i] + 4)
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
                        justify_function(
                            row_elements[i].strip().strip('"'), widths[i] + 4
                        )
                        for i in range(len(self.titles))
                    )
                    print(row)
                    pass
                print(f"the SSID we found is (index start from 1):\n {self.SSID_list}")
                self.index_SSID_list()
                print(f"the MAC we found is (index start from 1):\n {self.MAC_list}")
                pass
            else:
                # only print the SSID we have
                self.index_SSID_list()
                pass

        except Exception as e:
            print(f"Error list wifi: {e}")
            pass
        pass

    def table_gen(self, title_2=["Index", "SSID", "MAC Address"], SSID_list=None, MAC_list=None, justify="center"):
        if SSID_list is None:
            SSID_list = self.SSID_list
        if MAC_list is None:
            MAC_list = self.MAC_list

        # 定义对齐方式
        if justify == "left":
            justify_func = self.left_justify
        else:
            justify_func = self.center_justify

        # 计算每列的最大宽度，包括标题
        max_widths = [max(len(title), max([len(str(item)) for item in column], default=0)) for title, column in zip(title_2, [SSID_list, MAC_list])]

        # 打印标题行
        header = "|".join(justify_func(title, width) for title, width in zip(title_2, max_widths))
        print(header)

        # 打印分隔线
        divider = "+".join("-" * width for width in max_widths)
        print(divider)

        # # 打印每一行的数据
        # for idx, (ssid, mac) in enumerate(zip(SSID_list, MAC_list), start=1):
        #     row = "|".join([justify_func(str(idx), max_widths[0]), justify_func(ssid, max_widths[1]), justify_func(mac, max_widths[2])])
        #     print(row)


    def index_SSID_list(self):
        """
        to print the SSID with index
        """
        print(f"the SSID we found is (index start from 1):")
        c = len(self.SSID_list)
        for i in range(c):
            print(f"{i+1}: {self.SSID_list[i]}")

        pass

    def table_g(self, title_list=["Index", "SSID", "MAC Address"], justify="center"):
        """
        Print the SSID with index along with their corresponding MAC addresses, aligning each column according to the specified justification,
        and include a title row at the top of the table with the same width as the maximum width of the corresponding data columns.
        - title_list: A list containing the titles for each column.
        - justify: The alignment mode, either "left" for left justification or "center" for center justification.
        """
        print("The SSID and MAC addresses we found are (index starts from 1):")

        # Calculate the maximum width for each column considering both title width and data width
        max_widths = [len(title) for title in title_list]  # Initialize with title widths

        for ssid, mac in zip(self.SSID_list, self.MAC_list):
            max_widths[1] = max(max_widths[1], len(ssid))  # Compare and update with SSID widths
            max_widths[2] = max(max_widths[2], len(mac))  # Compare and update with MAC widths
            # 240222 for the future reserve
            # max_widths[3] = max(max_widths[3], len(ip))    # Compare and update with IP widths
        max_widths[0] = max(max_widths[0], len(str(len(self.SSID_list))))  # Compare and update with the length of the index

        # Define the justify function based on the specified mode
        if justify == "left":
            justify_func = self.left_justify
        elif justify == "center":
            justify_func = self.center_justify
        else:
            raise ValueError("Invalid justification mode. Please use 'left' or 'center'.")

        # Print the title row with the calculated maximum width for each column
        title_row = "|".join(justify_func(title, width + 2) for title, width in zip(title_list, max_widths))  # Add 2 for padding
        print(title_row)
        print("-" * len(title_row))  # Print divider

        # Print each SSID and its corresponding MAC address with their index, aligning each column
        for i, (ssid, mac) in enumerate(zip(self.SSID_list, self.MAC_list), start=1):
            row = "|".join([
                justify_func(str(i), max_widths[0] + 2),  # Index column
                justify_func(ssid, max_widths[1] + 2),  # SSID column
                justify_func(mac, max_widths[2] + 2)  # MAC column
                # 240222 for the future reserve
                # justify_func(ip, max_widths[3] + 2)     # IP column
            ])
            print(row)


    def connect_to(self, ssid_ind0=None, password0="0"):

        if self.sim_mode == 0:
            ssid = "PY Chu"
            password = "0294475990"

        else:

            if ssid_ind0 == None:
                # 用户选择网络
                ssid_ind = int(input("Enter network SSID index: "))
                password = input("Enter password: ")
                ssid = self.SSID_list[ssid_ind - 1]
                pass

            else:
                ssid = ssid_ind0
                password = password0
                pass

        # 尝试连接
        self.sendAT(f'CWJAP="{ssid}","{password}"')
        ip_response = self.sendAT("CIFSR")  # 获取 IP 地址
        print("Connected, IP address:\n", ip_response)

        # # 尝试连接
        # self.sendAT(f'CWJAP="{ssid}","{password}"')
        # print(f"to: {ssid}, {password}")

        # # 循環直到獲得IP地址或超時
        # timeout = 30  # 超時時間（秒）
        # start_time = time.time()
        # while True:
        #     ip_response = self.sendAT("CIFSR")  # 获取 IP 地址
        #     if ip_response != "busy p...":
        #         break  # 如果IP地址不再是"busy p..."，則跳出迴圈
        #     elif time.time() - start_time > timeout:
        #         print("Timeout occurred while waiting for IP address.")
        #         break  # 如果超時，則跳出迴圈
        #     else:
        #         print("Loading...")  # 顯示 loading
        #         time.sleep(1)  # 添加一秒的等待時間

        # 檢查是否成功連接並顯示 IP 地址
        time.sleep(1)
        if ip_response != "busy p...":
            print("Connected, IP address:\n", ip_response)
        else:
            print("Connection failed.")

        pass

    def terminal(self):
        """Simulate a terminal to interact with ESP32."""
        print("Enter commands to send AT commands directly to ESP32.")
        print("Enter 'exit' to exit the terminal.")

        while True:
            user_input = input(">> ").strip()

            if user_input.lower() == "exit":
                print("Exiting terminal.")
                break
            elif user_input.startswith("fun;"):
                # If the input starts with "fun;", treat it as a class method
                method_name = user_input[len("fun;") :]
                try:
                    getattr(self, method_name)()
                except AttributeError:
                    print("Invalid command. Method not found.")
            else:
                # Otherwise, treat it as an AT command
                response = self.sendAT(user_input)
                # print("Response:", response)


# 测试代码fun
if __name__ == "__main__":
    esp = esp_uart(1)  # 初始化 esp_uart 对象用于 UART 总线 1
    esp.list_wifi()  # 调用, default center_justify
    esp.table_g()
    # esp.list_wifi(justify0="left_justify")'
    # esp.sendAT("RESTORE")
    # esp.connect_to(ssid_ind0="PY Chu", password0="0294475990")
    # esp.terminal()
