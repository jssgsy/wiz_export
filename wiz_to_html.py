#!/usr/bin/env python
import os
import shutil
import sqlite3
import zipfile

# 导出的笔记要存放的目录
ROOT = './WizNotes'
NOTES = './notes/'
ATTACHMENTS = './attachments/'

MAX_FILENAME_LEN = 128


def data_location(acc):
    return os.path.expanduser('~') + '/.wiznote/' + acc + '/data/'


def unzip(src, dst):
    zip_file = zipfile.ZipFile(src)
    for names in zip_file.namelist():
        zip_file.extract(names, dst)
    zip_file.close()


def make_path(path):
    flag = os.path.exists(path)
    if not flag:
        os.makedirs(path)
    return flag


def read_from_db(dbname, sql):
    mydb = sqlite3.connect(dbname)
    cursor = mydb.cursor()
    cursor.execute(sql)
    table = cursor.fetchall()
    return table


def check_note_title(note_title):
    if len(note_title) > MAX_FILENAME_LEN:
        return note_title[:MAX_FILENAME_LEN]
    return note_title


def copy_notes(table):
    for row in table:
        hash, notetitle, location, url = row
        notetitle = check_note_title(notetitle)
        spath = NOTES + '{' + hash + '}'
        dpath = ROOT + location + notetitle
        make_path(dpath)
        if url:
            print(url)
        try:
            unzip(spath, dpath)
            print('[UNZIP]\t' + spath + '->' + dpath)
        except Exception as e:
            print(e)


def copy_attachments(table):
    for row in table:
        hash, location, note_title, attname = row
        note_title = check_note_title(note_title)
        make_path(ROOT + location + note_title)
        spath = ATTACHMENTS + '{' + hash + '}' + attname
        dpath = ROOT + location + note_title + '/' + attname
        try:
            shutil.copyfile(spath, dpath)
            print('[INFO]\t' + spath)
        except Exception as e:
            print(e)


def export_notes(dataLoc):
    # change dir
    os.chdir(dataLoc)
    # exec sql
    sql_note = "select DOCUMENT_GUID, DOCUMENT_TITLE, DOCUMENT_LOCATION, DOCUMENT_URL from WIZ_DOCUMENT"
    sql_attach = "select ATTACHMENT_GUID, DOCUMENT_LOCATION, DOCUMENT_TITLE, ATTACHMENT_NAME from WIZ_DOCUMENT, WIZ_DOCUMENT_ATTACHMENT where  WIZ_DOCUMENT.DOCUMENT_GUID = WIZ_DOCUMENT_ATTACHMENT.DOCUMENT_GUID"
    notes = read_from_db("index.db", sql_note)
    # attachments = read_from_db("index.db", sql_attach)

    # 处理笔记
    copy_notes(notes)

    # 处理附件，需要的话放开
    # copy_attachments(attachments)


def main():
    # 获取为知笔记data目录，入参为为知笔记账号名
    wiz_account = '替换成你的为知笔记账号(邮箱)'
    data_loc = data_location("wiz_account")
    export_notes(data_loc)


if __name__ == "__main__":
    main()