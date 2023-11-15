import subprocess
import yaml
from checkers import checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self):
        # test1
        result1 = checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        result2 = checkout("ls {}".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, make_files):
        # test2
        result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(data["folder_out"], ["folder_ext"]), "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["folder_ext"]), make_files[0])
        print(checkout("ls", make_files[0] ))
        assert result1 and result2, "test2 FAIL"

    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx2.7z".format(data["folder_out"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u {}/arx2.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"), "test4 FAIL"

    def test_step6(self):
        # test6
        result1 = checkout("cd {}; 7z l arx2.7z".format(data['folder_out']), "qwe")
        result2 = checkout("cd {}; ls".format(data['folder_in']), "qwe")
        result3 = checkout("cd {}; ls".format(data['folder_in']), "rty")
        assert result1 and result2 and result3, "test6 FAIL"

    def test_step7(self, data_make):
        # test7
        result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(data['folder_out'], data['folder_ext2']),
                           "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data['folder_ext2']), data_make[0])
        assert result1 and result2, "test7 FAIL"


    def test_step8(self):
        # test8
        result1 = subprocess.run("cd {}; 7z h arx2.7z".format(data['folder_out']), shell=True, stdout=subprocess.PIPE,
                                 encoding='utf-8')
        result2 = subprocess.run("cd {}; crc32 arx2.7z".format(data['folder_out']), shell=True, stdout=subprocess.PIPE,
                                 encoding='utf-8')
        assert result1.stdout and result2.stdout, "test8 FAIL"


    def test_step5(self):
        # test5
        assert checkout("cd {}; 7z d arx2.7z".format(data['folder_out']), "Everything is Ok"), "test5 FAIL"
