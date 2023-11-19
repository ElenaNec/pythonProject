import string
import random
from datetime import datetime

import pytest
from checkers import ssh_checkout, ssh_get
import yaml
from files import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "11", "mkdir {} {} {} {}".format(data["folder_in"],
                                                                             data["folder_out"], data["folder_ext"],
                                                                             data["folder_ext2"]), "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename, data["bs"]),
                        ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"],
                                                            data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "11",
                 "cd {}; 7z a {}/bad_arx ".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "11",
                 "truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "11",
                 "./tests/p7zip-full.deb", "/home/user2/p7zip-full.deb")  # путь откуда путь куда
    res.append(ssh_checkout("0.0.0.0", "user2", "11",
                            "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))

    return all(res)


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True, scope="module")
def make_files_stat():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "touch /home/user2/stat.txt", "")


@pytest.fixture()
def safe_log(start_time):
    with open("stat.txt", "w") as f:
        f.write(ssh_get("0.0.0.0", "user2", "11", "journalctl --since{} >> /home/user2/stat.txt".format(
            self.save_log(start_time, "log8.txt"))))


@pytest.fixture()
def report(start_time):
    yield
    stat = ssh_get("0.0.0.0", "user2", "11", "cat /proc/loadavg")
    ssh_checkout("0.0.0.0", "user2", "11",
                 "echo 'time: {}; count : {}; sise: {}; load: {}' >> stat.txt".format(
                     start_time, data['count'], data['bs'], stat), "")

    # with open("stat.txt", "w") as f:
    #     f.write(ssh_get("0.0.0.0", "user2", "11", "journalctl --since{} >> /home/user2/stat.txt".format(start_time)))