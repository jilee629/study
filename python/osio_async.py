

df = pd.read_excel('테스트고객정보.xlsx', dtype = 'str')
cs_data = list()
# for index, phone in enumerate(df['전화번호'].values.tolist()):
for index, phone in enumerate(df.index):
    data = list()
    data.append(index)
    data.append(df['오시오명'][index])
    # data.append(phone)
    data.append(df['오시오명'][index])
    data.append(df['오시오 잔여값'][index])
    data.append(df['오시오 만료일'][index])
    cs_data.append(data)
[print(cs) for cs in cs_data]

loop = asyncio.get_event_loop()
loop.create_task(main())

