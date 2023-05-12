import os
# 借助html2text将html文件转换成markdown文件
import html2text as ht

ignore = []


def traversal(path):
    for item in os.listdir(path):
        # 文件绝对路径
        abs_path = path + '/' + item
        # 忽略隐藏目录
        if os.path.isdir(abs_path) and item[0] != '.':
            if item not in ignore:
                traversal(abs_path)

        if item == 'index.html':
            html_to_md(abs_path)


def html_to_md(html_file_abs_path):
    print("html_file_abs_path: " + html_file_abs_path)
    # 取文件所在目录，因为固定以index.html结尾
    dir = html_file_abs_path[:-10]

    split = html_file_abs_path.split('/')
    # 最后一个元素固定为index.html
    real_file_name = split[-2]
    # 后缀在生成文件时指定
    if real_file_name.endswith(".md"):
        real_file_name = real_file_name[:-3]

    print("real_file_name: " + real_file_name)
    text_maker = ht.HTML2Text()
    # 读取html格式文件
    with open(html_file_abs_path, 'r', encoding='UTF-8') as f:
        html_file = f.read()
    # 处理html格式文件中的内容
    text = text_maker.handle(html_file)
    # 写入处理后的内容
    with open(dir + real_file_name + '.md', 'w') as f:
        f.write(text)
        # 删除原html文件
        os.remove(html_file_abs_path)


def main():
    # wiz_to_html.py文件中设置的存放导出笔记目录的全路径；
    path_which_imported = ''
    traversal(path_which_imported)


if __name__ == "__main__":
    main()