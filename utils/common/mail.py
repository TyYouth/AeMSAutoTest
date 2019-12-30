#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.common.log import logger
from utils.config import Config, REPORT_FILE


class Mail(object):
    def __init__(self, target_address_list):
        e = Config().get('mail')
        self.mail_host = e.get(
            'mail_host') if e and e.get('mail_host') else "smtp.qq.com"
        self.host_port = e.get(
            'host_port') if e and e.get('host_port') else 465
        self.mail_user = e.get(
            'mail_user') if e and e.get('mail_user') else "78376474@qq.com"
        self.mail_pwd = e.get(
            'mail_pwd') if e and e.get('mail_pwd') else "onctyyqycumtcbbb"

        self.target_addr_list = target_address_list
        self.mail_subject = "Test report"
        self.charset = 'utf-8'

    # create a mail object based on email().MIMEMultipart()
    # module email is responsible for mail's content
    def mail_obj(self):
        mail_obj = MIMEMultipart()
        mail_obj['Subject'] = Header(self.mail_subject, self.charset)
        # mail_obj['From'] = Header(self.mail_user, charset)
        return mail_obj

    def attach_content(self, email_obj):
        f = open(REPORT_FILE, 'rb')
        mail_body = f.read()
        f.close()
        content = MIMEText(mail_body, 'html', self.charset)
        email_obj.attach(content)

    @staticmethod
    def attach_file(email_obj):
        file = MIMEBase('application', 'octet-stream')
        file.set_payload(open(REPORT_FILE, 'rb').read())
        encoders.encode_base64(file)
        file_name = os.path.basename(REPORT_FILE)
        file.add_header('Content-Disposition', 'attachment; filename="%s"' % (file_name))
        email_obj.attach(file)

    # module smtplib is responsible for send mail
    def send_mail(self, email_obj):
        smtp_obj = smtplib.SMTP_SSL(self.mail_host, self.host_port)
        try:
            smtp_obj.login(self.mail_user, self.mail_pwd)
        except smtplib.SMTPAuthenticationError as e:
            logger.exception("Authentication failed!! \r%s" % (e))
        for address in self.target_addr_list:
            try:
                smtp_obj.sendmail(self.mail_user, address, email_obj.as_string())
                logger.info("Report has been successful sent to %s" % (address))
            except smtplib.SMTPException as e:
                logger.error("Fail to sent report to %s" % (address))
                logger.exception("caused by %s" % (e))
        smtp_obj.quit()

    def send(self):
        mail_obj = self.mail_obj()
        self.attach_content(mail_obj)
        self.attach_file(mail_obj)
        self.send_mail(mail_obj)


if __name__ == '__main__':
    target_addr_list = ["dfjakljdsafsdaf@qq.com", "78376474@qq.com"]
    E = Mail(target_addr_list)
    E.send()
