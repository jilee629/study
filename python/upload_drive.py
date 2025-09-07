#!/usr/bin/env python3

from datetime import datetime, timedelta
import osio


fdate = datetime.now().strftime("%Y%m%d")
folder_id = osio.create_drive_folder(fdate)

filelist = [
    ['exit_user.log', 'text'],
    ['download_csinfo.log', 'text'],
]
for file in filelist:
    osio.upload_file(folder_id, file[0])


csinfo_file = fdate + "_점핑몬스터 미사점_고객정보.xlsx"
osio.write_phone_len(csinfo_file)
len_csinfo_file = "len_" + fdate + "_점핑몬스터 미사점_고객정보.xlsx"

filelist = [
    [csinfo_file, 'xlsx'],
    [len_csinfo_file, 'xlsx'],
]
for file in filelist:
    osio.upload_file(folder_id, file[0], file[1])

