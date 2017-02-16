#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, subprocess
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


listen_path = r"E:\JavGame\trunk\GameResource\bins\debug\pygame\QServer\Games\newhhdn"
command = [u'新哈哈斗牛.bat'.encode('gbk')]
restart_num = 0

def log(s):
    print('[Monitor] %s' % s)

class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

def kill_process():
    name = "QServer1.0_d.exe"
    for pro in psutil.process_iter():
        if pro.name() == name:
            log('Kill process [%s]...' % pro.name())
            os.system("taskkill /F /IM QServer1.0_d.exe")
            log('Process ended pid %s.' % pro.pid)
            break


def start_process():
    global command
    subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    log('Start  Qserver command=%s...' % (' '.join(command)))


def restart_process():
    global restart_num
    restart_num += 1

    if restart_num > 2:
        restart_num = 1
        return

    kill_process()
    start_process()

def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(restart_process), listen_path, recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    restart_process()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def get_process_byname(name):
    for pro in psutil.process_iter():
        if pro.name() == name:
            return pro
    return None

if __name__ == '__main__':
    path = os.path.abspath('.')
    start_watch(path, None)
