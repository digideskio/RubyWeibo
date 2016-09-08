# __author__ = 'Sanwuthree'

import os
import sys
import re

COMPILE_ARGS_REG = re.compile(r'\s*#.+')
COMMENT_REG = re.compile(r'.*//.+')
COMP_NUM = 0  # 编译指令
COMMENT_NUM = 0  # 代码注释
CODE_NUM = 0  # 代码行数
HEAD_FILE_NUM = 0  #头文件数量
CPP_FILE_NUM = 0  # 源文件数量
SPACE_LINE = 0  # 空行
NOTESPACE_LINE = 0



def anisfun(filepath):
    print(filepath)
    global COMPILE_ARGS_REG
    global COMP_NUM
    global COMMENT_REG
    global COMMENT_NUM
    global SPACE_LINE
    global CODE_NUM
    global NOTESPACE_LINE
    is_enter_comment_lines = False
    f = open(filepath)
    contents = f.readlines()
    for li in contents:
        if is_enter_comment_lines:  # 如果进入了多行注释模式，则每行都视为注释，直到出现结束符
            COMMENT_NUM += 1
            if re.match(".*\*/", li):
                is_enter_comment_lines = False
        else:
            complie_match = COMPILE_ARGS_REG.match(li)
            comment_match = COMMENT_REG.match(li)
            if complie_match:
                COMP_NUM += 1
            if comment_match:
                COMMENT_NUM += 1
            if re.match(".*/\*", li):
                is_enter_comment_lines = True
                COMMENT_NUM += 1
            if re.match("^\s*\s$", li) or len(li) == 1:
                SPACE_LINE += 1

    NOTESPACE_LINE += len(contents) - SPACE_LINE
    CODE_NUM += (len(contents) - COMP_NUM - SPACE_LINE - COMMENT_NUM)


def walkdir(path):
    global HEAD_FILE_NUM
    global CPP_FILE_NUM
    global COMMENT_NUM
    for [parent, dirnames, filenames] in os.walk(path):
        for filename in filenames:
            file_enstion_str = os.path.splitext(filename)[1]
            if file_enstion_str == '.h':
                anisfun(parent + filename)
                HEAD_FILE_NUM += 1
            elif file_enstion_str == '.cpp':
                anisfun(parent + filename)
                CPP_FILE_NUM += 1
    print("代码分析完毕")
    print(".h文件数量 " + str(HEAD_FILE_NUM))
    print(".cpp文件数量 " + str(CPP_FILE_NUM))
    print(".编译指令数量 " + str(COMP_NUM))
    print(".注释数量 " + str(COMMENT_NUM))
    # print(".代码数量 " + str(CODE_NUM))
    print(".非空行数量 " + str(NOTESPACE_LINE))
    print(".空行数量 " + str(SPACE_LINE))

if len(sys.argv) > 1:
    walkdir(sys.argv[1])

else:
    print(os.getcwd())
    walkdir(os.getcwd())
