import os
import sys
import shutil


def copydir(src, dst):
    if not os.path.exists(dst):
        shutil.copytree(src, dst)
        return True


def copyfile(src, dst):
    if not os.path.exists(dst):
        shutil.copy(src, dst)
        return True


# Clear pyc
def clearpyc():
    for root, dirs, _ in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))


# Create app
def createapp(args):
    if args[2:]:
        appname = args[2]
    else:
        appname = input('輸入App名稱：')

    if not copydir('./apps/.default', f'./apps/{appname}'):
        print('該App名稱已存在！')
        exit()

    print('建立成功！')


# Initialize
def init():
    os.system('sudo python3.10 -m pip install -r requirements.txt')
    copyfile('./env.example.sh', './env.sh')
    copydir('./instance_example', './instance')
    print('初始化完成！請設定檔案之後再啟動應用程序。')


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        exit()

    match args[1]:
        case 'clearpyc':
            clearpyc()
        case 'createapp':
            createapp(args)
        case 'init':
            init()
