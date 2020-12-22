import pandas as pd
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def send_email(title, info):
    sender = 'sugang1110@163.com'
    receivers = ['sugang1110@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(title, 'plain', 'utf-8')
    message['From'] = Header("苏港", 'utf-8')  # 发送者
    message['To'] = Header("苏港", 'utf-8')  # 接收者

    message['Subject'] = Header(info, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtpObj.login("sugang1110@163.com", "FCJIKHXKDNKMDKPE")
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        import traceback
        traceback.print_exc()
        print("Error: 无法发送邮件")


def get_config(module_name):
    records = []
    rounds = []
    param = ""
    value = ""
    acc = []

    with open(module_name + ".out") as file:
        for line in file:
            round = re.findall("The minimum is attained in round (\d*)", line)
            if round:
                rounds.append(int(round[0]))

            find_acc = re.findall("acc result is (.*)", line)
            if find_acc:
                acc = [float(acc) for acc in str(find_acc[0]).split(",")]

            find_param = re.findall("change_param is (.*), change_value is (.*)", line)
            if find_param:
                param, value = find_param[0]
                value = str(value)

            time_spend = re.findall("time spend is (.*)", line)
            if time_spend:
                spend = str(time_spend[0])
                record = {"param": param, "value": value, "spend": spend,
                          "max_round": max(rounds), "min_round": min(rounds), "mid_round": sorted(rounds)[3],
                          "avg_round": sum(rounds) / 5,
                          "max_acc": max(acc), "min_acc": min(acc), "mid_acc": sorted(acc)[3], "avg_acc": sum(acc) / 5}
                print(record)
                records.append(pd.DataFrame([record]))

                rounds = []
                param = ""
                value = ""
                acc = []

    return pd.concat(records, axis=0)


import os

model_name = os.getcwd().split("/")[-1]
result = get_config(model_name)
params = result["param"].drop_duplicates()
for param in params:
    result[result["param"] == param].to_csv(f"params/{model_name}_{param}.csv", index=False)

title = f"task {model_name} is done"
send_email(title, title)
