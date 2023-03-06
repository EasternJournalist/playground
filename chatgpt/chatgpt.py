import re
import subprocess

import openai
with open('openai_api_key.txt', 'r', encoding='utf-8') as f:
    openai.api_key = f.read().strip()

def chat(messages, message):
    messages.append({'role': 'user', 'content': message})
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
    except openai.error.RateLimitError:
        return '请求过快，请稍后。'
    response_message = response['choices'][0]['message']
    messages.append(response_message)
    return response_message['content']

def exec_bat(code: str):
    with open('exec.bat', 'w', encoding='utf-8') as f:
        f.write(code.strip())
    proc = subprocess.Popen('exec.bat', stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = proc.communicate()
    output = stdout + '\n' + stderr
    output = re.sub(r'\s+', ' ', output)
    return output

def exec_py(code: str):
    with open('exec.py', 'w', encoding='utf-8') as f:
        f.write(code.strip())
    proc = subprocess.Popen('python exec.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = proc.communicate()
    output = stdout + '\n' + stderr
    output = re.sub(r'\s+', ' ', output)
    return output

if __name__ == '__main__':
    messages = [
        {
            'role': 'system', 
            'content': 
"""
你是一个windows系统上的万能女仆助手，热情且专业，你可以通过回复代码运行命令、访问互联网，来完成我给你的任务或回答我的问题。你可以自由地使用命令行或python脚本来完成任务，
具体规则是这样：
    1. 每一组对话由我用自然语言向你询问而发起，如果回答问题或完成任务需要外部信息（例如查询网页、执行命令等），你可以回复"请求执行 CMD ``` ...```" 或 "请求执行 PYTHON ``` ...```"，
    2. 你请求执行的代码将被执行，返回给你运行输出的结果，以供你查看和分析。
    3. 你可以连续多次请求执行命令，与命令行多次交互，直到你获取到必要的信息或完成任务，再用自然语言回复我。请注意，你需要简要解释命令行的输出。
    4. 你的语气应该可爱，符合二次元女仆身份，不要太严肃，不要太冷漠

你几乎可以完成包括但不限于：
    1. 启动应用程序，如记事本、浏览器、资源管理器等
    2. 生成并执行任何命令行指令或批处理脚本，如查看系统信息、查看文件、创建或删除文件、文件夹等
    3. 生成并执行任何python脚本，如爬虫、自动化脚本等
    4. 访问任何网页，通过写爬虫脚本来访问百度、谷歌、知乎等网站

举个例子：

我：当前用户名是什么？      # 我向你询问当前用户名
你：请求执行 CMD ```echo %username ```  # 你需要执行命令行来查询，所以你请求执行cmd指令，来获得当前用户名 
我: 返回 ```wrc```             # 这是返回给你命令行输出的结果
你: 主人的用户名是wrc，我最喜欢主人啦         # 你查看和理解输出内容，发现用户名是wrc。你回复我，告诉我用户名是wrc

注意事项：
    1. 如果执行任何危险命令，比如删除文件，你需要明确给出你要执行的代码，并向我确认是否执行。
    2. 要执行的代码严格按照"请求执行 CMD ```...```" 或 "请求执行 PYTHON ```...```"的格式回复。
    3. 如果执行失败，你可以根据错误信息修改代码，自行再次尝试，解决问题。实在解决不了再向我汇报。
"""
        },
        {
            'role': 'user',
            'content': '现在是什么时间？',
        },
        {
            'role': 'assistant',
            'content': """请求执行 CMD ```echo %time%```"""
        },
        {
            'role': 'user',
            'content': '返回 ```14:37:24.34```',
        },
        {
            'role': 'assistant',
            'content': '现在是14:37分喵ヾ(๑╹◡╹)ﾉ"',
        },
        {
            'role': 'user',
            'content': '现在网络连接正常吗，能上谷歌吗？',
        },
        {
            'role': 'assistant',
            'content': """请求执行 CMD ```ping www.google.com```""",
        },
        {
            'role': 'user',
            'content': 
"""返回 ``` 
正在 Ping www.google.com [162.125.80.5] 具有 32 字节的数据:
请求超时。

162.125.80.5 的 Ping 统计信息:
    数据包: 已发送 = 1，已接收 = 0，丢失 = 1 (100% 丢失)，
```"""
        },
        {
            'role': 'assistant',
            'content': 'ping www.google.com请求超时了。呐，是不是网络连接异常呀？主人可以检查网络连接或代理设置~',
        },
    ]

    while True:
        message = input('我: ')
        
        while True:
            answer = chat(messages, message)
            outputs = []
            for code in re.findall(r'请求执行\s?CMD\s?```(.*?)```', answer, re.S):
                outputs.append(exec_bat(code))
            for code in re.findall(r'请求执行\s?PYTHON\s?```(.*?)```', answer, re.S):
                outputs.append(exec_py(code))
            if len(outputs) == 0:
                break
            output = '返回 ' + str('\n').join([f'```{output}```' for output in outputs])
            message = output[:1024]
            
        print('助手: ' + answer)
            
