import unittest
from utils.Config import CASE_PATH, REPORT_FILE
from utils.common.HTMLTestRunner import HTMLTestRunner
from utils.common.mail import Mail
# from utils.common.UTX import *


def main():
    discover = unittest.defaultTestLoader.discover(CASE_PATH, pattern="test*.py")
    with open(REPORT_FILE, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title=u'Test Report', description=u'Report')
        runner.run(discover)

    # add the target mail address you want in list
    target_email_address_list = ["78376474@qq.com"]
    mail = Mail(target_email_address_list)
    mail.send()


if __name__ == '__main__':
    main()
