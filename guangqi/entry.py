# -*- coding: utf-8 -*-
import base64
from gmssl import sm4


class encry:
    def __init__(self):
        self.crypt_sm4 = sm4.CryptSM4()

    def base64_encode(self, str):
        return base64.b64encode(str.encode("utf-8"))

    def base64_decode(self, str):
        return base64.b64decode(str).decode("utf-8")

    def read_report_base64(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            base64_report = self.base64_encode(f.read())
        return base64_report.decode("utf-8")

    def read_report(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            report = f.read()
        return report

    def encryptSM4(self, encrypt_key, value):
        """
        国密sm4加密
        :param encrypt_key: sm4加密key
        :param value: 待加密的字符串
        :return: sm4加密后的十六进制值
        """
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(encrypt_key.encode(), sm4.SM4_ENCRYPT)  # 设置密钥
        date_str = str(value)
        encrypt_value = crypt_sm4.crypt_ecb(date_str.encode())  # 开始加密。bytes类型
        return encrypt_value.hex()

    def decryptSM4(self, decrypt_key, encrypt_value):
        """
        国密sm4解密
        :param decrypt_key:sm4加密key
        :param encrypt_value: 待解密的十六进制值
        :return: 原字符串
        """
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(decrypt_key.encode(), sm4.SM4_DECRYPT)  # 设置密钥
        decrypt_value = crypt_sm4.crypt_ecb(bytes.fromhex(encrypt_value))  # 开始解密。十六进制类型
        return decrypt_value.decode()


if __name__ == '__main__':
    en = encry()
    # 生成报文BASE64
    # path = r'E:\项目\15.广汽汇理\4人行报告\人行样例报告\二代个人\王小六-改配偶工作单位-2.html'
    # base_report = en.read_report_base64(path)
    # print(base_report)

    # 生成SM4
    key = 'dvpsos1234567890'

    strData = "NO622926198501293113"
    encData = en.encryptSM4(key, strData)
    print("sm4加密结果：", encData)
    # decData = en.decryptSM4(key, encData)
    # print("sm4解密结果：", decData)  # 解密后的数据
