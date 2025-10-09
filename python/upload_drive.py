#!/usr/bin/env python3

from datetime import datetime
import osio

if __name__ == "__main__":
    print('\n', datetime.now())

    fdate = datetime.now().strftime("%Y%m%d")
    folder_id = osio.create_drive_folder(fdate)

    log_date = datetime.now().strftime("%Y-%m")

    exit_log = log_date + "_exit_user.log"
    osio.upload_file(folder_id, exit_log)

    download_log = log_date + "_download_csinfo.log"
    osio.upload_file(folder_id, download_log)

    csinfo_file = fdate + "_점핑몬스터 미사점_고객정보.xlsx"
    osio.upload_file(folder_id, csinfo_file, 'xlsx')

    osio.write_phone_len(csinfo_file)
    len_csinfo_file = "len_" + fdate + "_점핑몬스터 미사점_고객정보.xlsx"    
    osio.upload_file(folder_id, len_csinfo_file, 'xlsx')

    unknown_log = log_date + "_unknown_user.log"
    osio.upload_file(folder_id, unknown_log)



