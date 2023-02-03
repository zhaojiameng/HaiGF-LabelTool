"""
证书验证流程：
证书->读取证书信息->读取指纹信息->比对
"""
import os
from pathlib import Path
import base64
import copy
# import rsa
import hashlib
import damei as dm
import uuid
import shutil

logger = dm.getLogger(name='License')
pydir = f'{Path(os.path.abspath(__file__)).parent}'


class License(object):

    def __init__(self):
        self.head = 'dacongmei'
        self.rsa_length = 1024
        self.rsa_pubk = f'LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JR0pBb0dCQU1mYzQ1bmREL1VNVXpsS3NsS1N6cG9pU29rL2RHa0dzTitFclVVT2FDVk9YOEN0WFdxNTY3TWoKc0h3OXAvMm5FMmtOdTdvZWxuSlE2MnNxMWpPaVExUXBuejJXbERCZnh5dHloVkRxOFJIZ3NhbU5haERLMzZsTgpRVndTZkpaSEJtRjNCZTJ4bVpoSDk3ZmlDRkFNUzRQS25iRnNOcDNSclNSM3pKekQyYU92QWdNQkFBRT0KLS0tLS1FTkQgUlNBIFBVQkxJQyBLRVktLS0tLQo='
        self.rsa_privk = f'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWUFJQkFBS0JnUUNwSVpOa2ptZHlJOU9rSXZYc1M5bzIybVo1MklrU1hHZ2k5bHErRWk1NnkyWC9TSHg0CmRzNElvOFUxOXNxYUtrMkJpb3ZXbVg4MHVBdmh5RUVkWnBwK3pIdGRNdTJKK0hjRjJLTm9MZEpCbDd6akFRMC8KT09Ud2pDNkljRmNnOFpCSzBNK3dPbHFOMHNQOFU1WmVuWHU4amhldUdCemxNSU5IdWsyOEplRExtd0lEQVFBQgpBb0dBWFFnVC9ENzhsZU14R2xzRXJQcTRTRzN2Nmx2NllmZ2thLzdZd1M1ZEZMeG5HWG4weFlxTUlHSjlLd2JhClFOeStEMkIzTlE3djByN2VBazdWUkRDbEJLSXU5TkNzN3AxZ3U3c3FQZUoyTC9RYkxkOThjR0lDdFpKeXIwRHQKOVFxS0V6Mms3WXlubzAxTjZXeXZoUDM2eWJoWXJpQThhT1RLbk1LeXdIRHVKdUVDUlFEMEFBQVdLL2EzVm1XbgpEb1FlbGc2ay9Ic3NHYTU5VjI1RVVqVHdpMmNldEJ6ajhLb2hXVUVHV0hoVlNpOXd6UFBuOGc4SkFIc1UvdHBtClQ4cFlUbDFJOEZZaEN3STlBTEZ5OXVnUTF2cnVQSmh2ZysyZDgzV3FNS1FzQmhiSnVtM29tejIxelBqbVhIbC8KQWpncURCZXMyYURRWE44a2I4MGZPKy9XOWtrMXd6bTVzUUpGQUlkUXpMdC9EQ2Jtd2g4Z1hNTDlvd2Q2Z2ZDVwpHWCtua2g1UG5NNWQ4UVZGQzlTWmJqQnFhRFpWci81VTB2UnlwVDFYcjJEbHBGeWpiWWxaN0xTR1dST1BQYVM3CkFqeFRNODJUcUhtMHRNb1N5NDczZG0wMlNiTis5dWx2Kyt4L0ptYkwrNWQ5U1Q0bzlhV0x3aU5qWW5lMGtKNUwKUHFGeGMyaStIM1BoaGVUaEJ6RUNSRi9HMTJFajBHY1BhYzVoSTRLWmFGYXpQY2RVMStWWVNzYVpXeGpGMjMxSQpneFgyQnFxMEJxcHJ2QnFpWDUxWFlHeThBRkJwYys5bVFXZFE3NUhndEg5YVVuUjQKLS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0K'
        # 注意：这里是pubk1和privk2，两者不是一对

        self.system = dm.current_system()
        logger.info(f'The current system is {self.system}.')
        self.lic_path = f'{pydir}/license.lic'

    def get_mac(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
        # print(mac)  # 98:5a:eb:8c:05:42
        return mac

    def get_disk_serial(self):
        s = self.system

        def get_du_h():
            ret = dm.popen('df -h')
            ret = [x.split() for x in ret if x.split()[-1] == '/']
            assert len(ret) == 1
            file_system = ret[0][0]  # filesystem是/dev/nvme0n1p6，或sda2之类的，后面的p6和2是卷里分出来的
            # print(file_system)
            return file_system

        if s == 'windows':
            serial = 'i am a serial'
            return serial
        elif s == 'linux':  # linux or macos
            # 寻找主系统/挂载的那个卷
            file_system = get_du_h()
            ret = dm.popen('lsblk --nodeps')
            ret = [x for x in ret if not (x.startswith('loop') or x.startswith('NAME'))]
            volumes = [x.split()[0] for x in ret]  # 这是[sda, sdb, nvme0n1]等

            volume = [x for x in volumes if x in file_system]
            volume = None if len(volume) == 0 else volume[0]
            volume = '/'.join(file_system.split('/')[:-1] + [volume])

            serial = dm.popen(f"lsblk --nodeps -no serial {volume}")
            assert len(serial) == 1
            serial = serial[0]
            # print(f'volume: {volume} serial: {serial}')
            return serial
        else:  # macos
            file_system = get_du_h()
            info = dm.popen(f'diskutil info {file_system}')
            info = [x for x in info if 'Volume UUID:' in x]
            assert len(info) == 1
            serial = info[0].split()[-1]
            # print(info, serial)
            return serial

    def read_fingerpint_info(self):
        """
        读取指纹信息：系统型号、mac地址、硬盘地址
        """
        s = self.system
        mac = self.get_mac()
        disk_serial = self.get_disk_serial()
        finfo = f'head={self.head};sys={s};mac={mac};disk_serial={disk_serial}'
        return finfo

    def finfo2fcode(self, finfo):
        """
        fingerprint info (fi) to fingerprint code by base64 + rsa encrypt
        # 这里仅采用加密方案，没有签名
        :return:
        """
        fcode = dm.rsa.encrypt(plaintext=finfo, pubk=self.rsa_pubk)
        return fcode

    def gen_fcode(self):
        """
        读取本机信息，生成指纹码
        :return: fingerprint code
        """
        finfo = self.read_fingerpint_info()
        # finfo2 = "head=dacongmei;sys=macos;mac=98:5a:eb:8c:05:42;disk_serial=4FBB2C82-D65E-3D68-AB52-472CCF3BF8D0"
        # print(f'finfo: {finfo} {type(finfo)}')
        fcode = self.finfo2fcode(finfo)  # 指纹码
        print(f'fingerprint_code: {fcode} {type(fcode)}')
        return fcode

    def verify_license(self, lic_path=None):
        lic_path = lic_path if lic_path else self.lic_path
        # 无证书，开启激活
        if not os.path.exists(lic_path):
            return False, None
            ret = self.register(acode=None, lic_path=lic_path)
            if not ret:  # 验证失败
                logger.info(f'Register failed.')
                return False, None
        with open(lic_path, 'r') as f:
            lic = f.read()

        # 有证书，要验证md5码和验证时效
        message = self.decrypt(ciphertext=lic)
        if not message:
            return False, None
        passed = self.verify_md5_and_time(message)
        if not passed:
            return False, None
        return True, message

    def verify_md5_and_time(self, message):
        md5, exp_time = [x.split('=')[-1] for x in message.split(';')[-2::]]
        if not self.verify_md5(md5):
            return False
        # 验证时间
        within = dm.within_time(expiration_time=exp_time, current_t=None)
        if not within:
            return False
        return True

    def register(self, acode=None, lic_path=None):
        """
        获取注册码，验证成功后生成注册文件
        :param acode: activate code
        :param lic_path: path to save license.lic
        """
        logger.info(f'Registering...')
        lic_path = lic_path if lic_path else self.lic_path

        acode = acode if acode else input('Please input activation code: ')
        if acode == '':
            self.__call__(acode=None, lic_path=lic_path)
        else:  # 进入激活程序
            # 读取激活码信息
            try:  # 可能会由于激活码位数的导致失败
                message = self.decrypt(ciphertext=acode)  # 返回False是失败了，否则返回解码的消息
            except Exception as e:
                message = False
            if not message:
                return False  # 解码验证失败
            success = self.verify(message)
            if not success:  # 消息格式和md5验证失败
                return False

            # 直接把激活码作为license.lic的内容
            exp_time = message.split(';')[-1].split('=')[-1]
            logger.info(f'Successfully verified the activation code.')
            logger.info(f'Expiration time: {exp_time}.')
            with open(lic_path, 'w') as f:
                f.write(acode)
            logger.info(f'The license.lic is generated.')
            return True

    def decrypt(self, ciphertext):
        """
        签名验证并解码
        :param ciphertext:
        :return:
        """
        # 解密消息，格式是sign;
        plaintext = dm.rsa.decrypt(ciphertext, privk=self.rsa_privk, length=self.rsa_length)
        sign = plaintext.split(';')[0]
        raw_message = ';'.join(plaintext.split(';')[1::])
        message = copy.copy(raw_message)
        # 验证sign
        ret = dm.rsa.verify(message=message, signature=sign, pubk=self.rsa_pubk)
        if not ret:  # 验证失败
            return False

        return raw_message

    def verify(self, message):
        """
        格式验证+MD5验证
        :param message:
        :return:
        """
        # 验证消息格式, head=xx;md5=xx;expiration_time=xx
        message = [x.split('=') for x in message.split(';')]
        try:
            assert len(message) == 3, len(message)
            assert message[0][0] == 'head', message[0][0]
            assert message[0][1] == 'dacongge', finfo[0][1]
            assert message[1][0] == 'md5', message[1][0]
            assert message[2][0] == 'expiration_time', finfo[2][0]
        except Exception as e:
            logger.warn(f'Verify meggage format error, failed. {e}')
            return False

        # 验证md5
        is_match = self.verify_md5(message[1][1])
        return is_match

    def verify_md5(self, md5):
        """验证md5"""
        finfo = self.read_fingerpint_info()
        finfo_md5 = self.md5_encrypt(value=finfo)  # 本地的md5
        is_match = md5 == finfo_md5
        if not is_match:
            logger.error(f'MD5 verify failed. MD5: {md5} Local MD5: {md5}')
        return is_match

    def md5_encrypt(self, value):
        m = hashlib.md5()
        m.update(value.encode('utf-8'))
        md5 = m.hexdigest()  # 返回16进制str
        return md5


if __name__ == '__main__':
    acitvate_code = f'kWUx411Vo4GeFaMbLlA0HWu3EUQePBfFbyxhLKTmqVquiS6J76+AXbsiQMuu7uuIgo982iSyxJ35YwNVoYahZxDb23yBVEBGRPJohCcVC8y9m/ey+JyKd6SQnlRzG2CDB3tAlh3TqTDzerDA1WaYWJdFnU9wNwYScJihbED4Me2Z2z6NyK53JhsbB8PvQQMCbglt7Fy17IKcjAcryoF7MmthL4+sKvZJDy2s2y9Oj1AqHMg/LHzxf6iD8r4xv5pGJB6+wCbd/0vNJd45wii6mkAHBgniVg+DzXK+XJ+fpTWPt3Zni/9WHMAUBiZXCuxP3+HFjCNB8BMmJTM1G/Q4lEbhNN8RSj1QvCnQwk5UB0D1NZT/rFS/kQPwcQ2oQfWna+kcoNq7ImckrZogBmufD4KpfHldqp1o4drfKNpZKS1r8Y183MfMmfbt9s2ahj2nXxa1mosr/4FEa8mKT3MMqQheMHSDFPpxwDrFpcYASjAvPmKQdAsXDduXZfb771Wi'
    acitvate_code = f'FeF4pKaZOtaWSEp9Ua0CLiL4aFBWzizS6h9HQoEPZ69KvU8T581KMzu6hRDE5swN8bkARo2bMlNdvmYgucy7EbhPMm4484b1qamCkmyOZiH1DMolSXp7+NNaTHMc3qtfCSxq31s8IzoIiVtBuFH3zkmOBrE0Pk3PSgbVqvimlbwMAbpo5xbgEXXg2CPKcyezxFXhBGe6KA/p3mAGnx0ySVNfv8DaPc1rer/oIMXoQUmntzFb8lvqVg6w+LVEvLjeS9b9FzlFKaufyRjRKMHDdTgYka+kow4ObZAtDkUeEMkluc2Phwj64Z6DltXjuLHcoz0nHsu2VhUOmhWPPC1of3C0gOpKw+Oh1hM4+fbWHcpixiUA1thsjHO3jgKn40C2C/RQtkQ+srqWd2JVse48vECQouuupJOmTDHZZn7I5/Z/x/UI7OCNp1byRs54d5Nelhz2xlwl39grm7gNxtU/1r/OiTp+FG92cEu4OcxpKgIgllHlovralMSU/I9u3whE'
    lic = License()
    # fcode = lic.gen_fcode()

    # lic.register(acode=acitvate_code)
    ret = lic.verify_license()
    print('ret', ret)