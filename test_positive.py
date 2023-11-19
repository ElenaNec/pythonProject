import subprocess
import yaml
from checkers import checkout, ssh_checkout, ssh_get

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, report):
        # test1
        result1 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "11",
                               "ls {}".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files, report):
        # test2
        res = []
        res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                "cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                            "Everything is Ok"))
        res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                "cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]),
                            "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                    "ls {}".format(data["folder_ext"]), item))
        assert all(res)


    def test_step3(self, report):
        # test3
        assert ssh_checkout("0.0.0.0", "user2", "11",
                            "cd {}; 7z t arx2.{}".format(data["folder_out"], data['type']), "Everything is Ok"), "test3 FAIL"

    def test_step4(self, report):
        # test4
        assert ssh_checkout("0.0.0.0", "user2", "11",
                            "cd {}; 7z u {}/arx2.{}".format(data['folder_in'], data['folder_out'],  data['type']),
                            "Everything is Ok"), "test4 FAIL"

    def test_step6(self, make_files, report):
        # test6
        res = []
        res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                "cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                    "cd {}; 7z l arx2.{}".format(data["folder_out"], data['type']),
                                    item))
        assert all(res), "test6 FAIL"

    def test_step7(self, make_files, report):
        # test7
        result1 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z x arx2.{} -o{} -y".format(data['folder_out'], data['type'], data['folder_ext2']),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; ls".format(data['folder_ext2']), make_files[0])
        assert result1 and result2, "test7 FAIL"

    def test_step8(self, clear_folders, make_files, report):
        # self.save_log(start_time, "log8.txt")
        res = []
        for item in make_files:
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z h {}".format(data["folder_in"],
                                                                                                      item),
                                                                                            "Everything is Ok"))
            hash = ssh_get("0.0.0.0", "user2", "11", "cd {}; "
                                                                        "crc32 {}".format(data["folder_in"],
                                                                                          item)).upper()
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z h {}".format(data["folder_in"],
                                                                                                      item), hash))
        assert all(res), "test8 FAIL"

    def test_step5(self, report):
        # test5
        assert ssh_checkout("0.0.0.0", "user2", "11",
                            "cd {}; 7z d arx2.7z".format(data['folder_out']), "Everything is Ok"), "test5 FAIL"
