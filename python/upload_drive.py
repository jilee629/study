#!/usr/bin/env python3

from datetime import datetime
import osio

if __name__ == "__main__":

    fdate = datetime.now().strftime("%Y%m%d")
    folder_id = osio.create_drive_folder(fdate)

    osio.upload_file(folder_id, '0_exit_user.log')

    osio.upload_file(folder_id, '0_download_csinfo.log')

    csinfo_file = fdate + "_점핑몬스터 미사점_고객정보.xlsx"
    osio.upload_file(folder_id, csinfo_file, 'xlsx')

    osio.write_phone_len(csinfo_file)
    len_csinfo_file = "len_" + fdate + "_점핑몬스터 미사점_고객정보.xlsx"    
    osio.upload_file(folder_id, len_csinfo_file, 'xlsx')

    osio.upload_file(folder_id, '0_unknown_user.log')



