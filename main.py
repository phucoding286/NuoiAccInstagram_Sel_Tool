from modules import *
from scroller import random_scroll

sessions_manager_file = "sessions.json"
if not os.path.exists(sessions_manager_file):
    with open(sessions_manager_file, "w", encoding="utf-8") as file:
        json.dump({"data": {}}, file)

def storage_cookies(driver, cookie_f_name="session_name.pkl"):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    driver.get("https://www.instagram.com")
    pickle.dump(driver.get_cookies(), open("instagram_cookie_" + cookie_f_name + ".pkl", "wb"))
    print(success_color("[#] Đã lưu cookie thành công."))

def load_cookies(driver, cookie_f_name="session_name"):
    if not os.path.exists("instagram_cookie_" + cookie_f_name + ".pkl"):
        print(error_color("[!] File cookie chưa tồn lại"))
        return 0
    driver.get("https://www.instagram.com")
    cookies = pickle.load(open("instagram_cookie_" + cookie_f_name + ".pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    print(success_color("[#] Đã load cookie thành công."))

def add_new_session():
    global sessions_manager_file
    # nhập đường dẫn lưu trữ phiên trình duyệt chưa thông tin đã thiết lập
    path = input(system_color("[?] nhập đường dẫn đến phiên của bạn\n-> "))
    data = json.load(open(sessions_manager_file))
    # nhập tên người dùng instagram làm tên phiên
    while True:
        session_name = input(system_color("[?] Nhập username instagram của bạn\n-> "))
        if session_name in data['data']:
            print(error_color(f"[!] username {session_name} đã tồn tại vui lòng nhập username instagram mới!"))
            continue
        else:
            break
    # mở trình duyệt và yêu cầu nhập thông tin thiết lập
    driver = driver_init(path + "\\" + session_name)
    instagram_login(driver)
    # lưu lại tên phiên và phiên đã thiết lập
    data["data"][session_name] = path + "\\" + session_name
    json.dump(data, open(sessions_manager_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    # thông báo hoàn tất
    input(success_color("[#] Đã hoàn tất quy trình thêm phiên của bạn, nhấn enter để thoát\n->"))
    storage_cookies(driver, cookie_f_name=session_name)
    try:
        driver.quit()
    except:
        pass

def main_program():
    data = json.load(open(sessions_manager_file))['data']
    try:
        for username_ins, session_path in data.items():
            print(system_color(f"[>] account đang chạy -> {username_ins}"))
            driver = driver_init(session_path, True)
            load_cookies(driver, cookie_f_name=username_ins)
            if "error" in random_scroll(driver): raise ValueError()
            driver.quit()
    except:
        try:
           driver.quit()
        except:
            pass
        try:
            r = requests.get("https://www.google.com/")
        except:
            print(error_color("\n[!] Không có mạng!"))
            input(system_color("[!] Phát hiện không có mạng, chương trình tạm dừng, chờ can thiệp, enter để tiếp tục chạy\n-> "))

if __name__ == "__main__":
    while True:
        print(system_color(" ----------------------------------------------------"))
        print(system_color("| Tool Nuôi Instagram By PhuTech (Programing-Sama) |"))
        print(system_color("|     Công cụ được xây dựng dựa trên SEL           |"))
        print(system_color(" ----------------------------------------------------"))
        print(system_color("| # Các nguồn tài nguyên phụ thuộc                |"))
        print(system_color("|  $ undetected-chromedriver (python package)     |"))
        print(system_color("|  $ cloudscraper (python package)                |"))
        print(system_color("|  $ selenium (python package)                    |"))
        print(system_color(" -------------------------------------------------"))
        print(system_color("| ? Các lựa chọn theo index                       |"))
        print(system_color("| [1] Thêm phiên                                  |"))
        print(system_color("| [2] Chạy tool                                   |"))
        print(system_color(" -------------------------------------------------"))
        print()

        inp = int(input(system_color("[?] Nhập lựa chọn của bạn\n-> ")))
        print()

        if inp == 1:
            add_new_session()
            os.system("cls") if sys.platform.startswith("win") else os.system("clear")
        elif inp == 2:
            while True:
               main_program()