#!/usr/bin/env python3

from datetime import datetime
import osio
import os

if __name__ == "__main__":
    
    fdate = datetime.now().strftime("%Y%m%d")

    file_name = fdate + "_점핑몬스터 미사점_고객정보.xlsx"
    osio.write_phone_len(file_name)

    file_name = "len_" + fdate + "_점핑몬스터 미사점_고객정보.xlsx"
    osio.upload_file(file_name, 'xlsx')

    file_name = "exit_user.log"
    osio.upload_file(file_name)

    file_name = "download_csinfo.log"
    osio.upload_file(file_name)
