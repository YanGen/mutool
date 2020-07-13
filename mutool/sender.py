

def sendEmail(title,content,receivers = ['zorage@qq.com']):
    import smtplib
    import mutool.constants as CONSTANTS
    from email.mime.text import MIMEText
    # 第三方 SMTP 服务
    mail_host = CONSTANTS.mail_host  # SMTP服务器
    mail_user = CONSTANTS.mail_user  # 用户名
    if not CONSTANTS.mail_pass:
        print("未置授权码")
        return

    sender = "zorage@163.com"

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, CONSTANTS.mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)
