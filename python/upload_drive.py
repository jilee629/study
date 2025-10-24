#!/usr/bin/env python3

from datetime import datetime
import osio

if __name__ == "__main__":
    print('\n', datetime.now())

    file_date = datetime.now().strftime("%Y%m%d")
    folder_id = osio.create_drive_folder(file_date)
    log_date = datetime.now().strftime("%Y%m")

    file_name = log_date + "_daily.log"
    osio.upload_file(folder_id, file_name)

    file_name = "0_unknown_user.log"
    osio.upload_file(folder_id, file_name)

    file_name = file_date + "_점핑몬스터 미사점_고객정보.xlsx"
    osio.upload_file(folder_id, file_name, 'xlsx')

    osio.write_phone_len(file_date)
    file_name = file_date + "_len_점핑몬스터 미사점_고객정보.xlsx"    
    osio.upload_file(folder_id, file_name, 'xlsx')

    



