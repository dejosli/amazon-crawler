import time
from datetime import datetime
# from datetime import datetime
# import threading

# # get current date
# datetime_object = datetime.now()
# print(datetime_object)

# def clock(hour, minute):
#     hours = int(time.strftime("%I"))
#     minutes = int(time.strftime("%M"))
#     seconds = int(time.strftime("%S"))
#     am_pm = str(time.strftime("%p"))
#     clock_display = f"{hours}:{minutes}:{seconds} {am_pm}"

#     print(clock_display)
#     time.sleep(1)
#     if (hour==hours) & (minute==minutes):
#         print("Hi!")
#     else:
#         clock(hour, minute)


# hour = int(input("Hours: "))
# minute = int(input("Minutes: "))
# clock(hour, minute)

# print(time.time())

# start_time = threading.Timer(1, clock)
# start_time.start()
# # clock()


categories = ['Arts & Photography', 'Biographies & Memoirs', 'Business & Money', "Children's eBooks", 'Comics, Manga & Graphic Novels', 'Computers & Technology', 'Cookbooks, Food & Wine', 'Crafts, Hobbies & Home', 'Education & Teaching', 'Engineering & Transportation', 'Foreign Languages', 'Health, Fitness & Dieting', 'History', 'Humor & Entertainment',
              'Law', 'LGBTQ+ eBooks', 'Literature & Fiction', 'Medical eBooks', 'Mystery, Thriller & Suspense', 'Nonfiction', 'Parenting & Relationships', 'Politics & Social Sciences', 'Reference', 'Religion & Spirituality', 'Romance', 'Science & Math', 'Science Fiction & Fantasy', 'Self-Help', 'Sports & Outdoors', 'Teen & Young Adult', 'Travel']

# cate = input()
# for category in categories:
#     if cate.lower() == category.lower():
#         print('matched')
fields_dict = {
    'Title': 'Title',
    'Author': 'Author',
    'ASIN': 'ASIN',
    'Publisher': 'Publisher',
    'Publication date': 'Publication date',
    'Language': 'Language',
    'File size': 'File size',
    'Text-to-Speech': 'Text-to-Speech',
    'Enhanced typesetting': 'Enhanced typesetting',
    'X-Ray': 'X-Ray',
    'Word Wise': 'Word Wise',
    'Print length': 'Print length',
    'Lending': 'Lending',
    'Best Sellers Rank': 'Best Sellers Rank',
    'Customer Reviews': 'Customer Reviews',
    'Narrator': 'Narrator',
    'Listening Length': 'Listening Length',
    'Whispersync for Voice': 'Whispersync for Voice',
    'Program Type': 'Program Type',
    'Version': 'Version',
    'Audible Release Date': 'Audible Release Date'
}
raw_books_url = {26: '/2030-Biggest-Collide-Reshape-Everything-ebook/dp/B084F986RN/ref=zg_bs_154849011_26/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 4: '/AI-Superpowers-China-Silicon-Valley-ebook/dp/B0795DNWCF/ref=zg_bs_154849011_4/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 43: '/Accelerate-Software-Performing-Technology-Organizations-ebook/dp/B07B9F83WM/ref=zg_bs_154849011_43/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 16: '/Age-Surveillance-Capitalism-Future-Frontier-ebook/dp/B01N2QEZE2/ref=zg_bs_154849011_16/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 49: '/Basic-Economics-Thomas-Sowell-ebook/dp/B00L4FSSTA/ref=zg_bs_154849011_49/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 18: '/Big-Short-Inside-Doomsday-Machine-ebook/dp/B003LSTK8G/ref=zg_bs_154849011_18/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 38: '/Bitcoin-Standard-Decentralized-Alternative-Central-ebook/dp/B07BPM3GZQ/ref=zg_bs_154849011_38/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 39: '/Book-Numbers-Analyzing-Pursuit-Women-ebook/dp/B08PTFKLP6/ref=zg_bs_154849011_39/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 14: '/COVID-19-Great-Reset-Klaus-Schwab-ebook/dp/B08CRZ9VZB/ref=zg_bs_154849011_14/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 47: '/Capital-Twenty-First-Century-Thomas-Piketty-ebook/dp/B074DVRW88/ref=zg_bs_154849011_47/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 2: '/Dark-Towers-Deutsche-Donald-Destruction-ebook/dp/B07NLFHHJ3/ref=zg_bs_154849011_2/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 10: '/Data-Detective-Rules-Sense-Statistics-ebook/dp/B089425N6D/ref=zg_bs_154849011_10/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 32: '/Deficit-Myth-Monetary-Peoples-Economy-ebook/dp/B07RM72BT7/ref=zg_bs_154849011_32/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 36: '/Discrimination-Disparities-Thomas-Sowell-ebook/dp/B07JLS7P8D/ref=zg_bs_154849011_36/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 12: '/Evil-Geniuses-Unmaking-America-History-ebook/dp/B0852NXWR5/ref=zg_bs_154849011_12/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 22: '/False-Alarm-Climate-Change-Trillions-ebook/dp/B0827TL851/ref=zg_bs_154849011_22/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 23: '/Fantasyland-America-Haywire-500-Year-History-ebook/dp/B004J4WNJE/ref=zg_bs_154849011_23/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 17: '/Fifth-Risk-Michael-Lewis-ebook/dp/B07FFCMSCX/ref=zg_bs_154849011_17/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 29: '/Flash-Boys-Wall-Street-Revolt-ebook/dp/B00HVJB4VM/ref=zg_bs_154849011_29/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 8: '/How-Avoid-Climate-Disaster-Breakthroughs-ebook/dp/B07YRY461Y/ref=zg_bs_154849011_8/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 3: '/How-Day-Trade-Living-Management-ebook/dp/B012C4AU10/ref=zg_bs_154849011_3/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 24: '/How-Make-Money-Stocks-Winning-ebook/dp/B00916ARYS/ref=zg_bs_154849011_24/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 35: '/I-Hate-You-Marry-Me-ebook/dp/B085LYJPC3/ref=zg_bs_154849011_35/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 5: '/Invent-Wander-Collected-Writings-Introduction-ebook/dp/B08BCCT6MW/ref=zg_bs_154849011_5/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 25: '/Investing-QuickStart-Guide-Simplified-Successfully-ebook/dp/B07H71XXGY/ref=zg_bs_154849011_25/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 50: '/Invisible-Women-Data-World-Designed-ebook/dp/B07N1N6VKT/ref=zg_bs_154849011_50/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 11: '/Lifestyle-Investor-Commandments-Investing-Financial-ebook/dp/B08RLMP6BF/ref=zg_bs_154849011_11/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 20: '/Lights-Out-Delusion-General-Electric-ebook/dp/B084D28MBV/ref=zg_bs_154849011_20/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 31: '/Made-China-Prisoner-Letter-Americas-ebook/dp/B08519KVX5/ref=zg_bs_154849011_31/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 28: '/Mediocre-Dangerous-Legacy-White-America-ebook/dp/B07XDM254H/ref=zg_bs_154849011_28/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 1: '/New-Class-War-Democracy-Managerial-ebook/dp/B07MYKVWZD/ref=zg_bs_154849011_1/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 9: '/New-Great-Depression-Winners-Post-Pandemic-ebook/dp/B08DMVQ184/ref=zg_bs_154849011_9/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 30: '/Nomadland-Surviving-America-Twenty-First-Century-ebook/dp/B06XH3D8VG/ref=zg_bs_154849011_30/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 40: '/Nudge-Improving-Decisions-Health-Happiness-ebook/dp/B00A5DCALY/ref=zg_bs_154849011_40/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 15: '/Peoples-Guide-Capitalism-Introduction-Economics-ebook/dp/B08DCN3RBW/ref=zg_bs_154849011_15/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 33: '/Post-Corona-Opportunity-Scott-Galloway-ebook/dp/B08HL8JYZN/ref=zg_bs_154849011_33/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 19: '/Power-Your-Subconscious-Mind-ebook/dp/B0773RQ55P/ref=zg_bs_154849011_19/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 41: '/Predictably-Irrational-Revised-Expanded-Decisions-ebook/dp/B002C949KE/ref=zg_bs_154849011_41/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 48: '/Price-Peace-Democracy-Maynard-Keynes-ebook/dp/B07WPQD8ZX/ref=zg_bs_154849011_48/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 6: '/Radium-Girls-Story-Americas-Shining-ebook/dp/B01N7KMS7X/ref=zg_bs_154849011_6/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 37: '/Religion-Rise-Capitalism-Benjamin-Friedman-ebook/dp/B087PL2ZCB/ref=zg_bs_154849011_37/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 21: '/Rich-As-More-Money-Than-ebook/dp/B08QY57GFY/ref=zg_bs_154849011_21/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 27: '/Skin-Game-Hidden-Asymmetries-Daily-ebook/dp/B075HYVP7C/ref=zg_bs_154849011_27/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 45: '/Sovereign-Individual-James-Dale-Davidson-ebook/dp/B00AK9IXXM/ref=zg_bs_154849011_45/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 42: '/The-Riches-of-This-Land-The-Untold-True-Story-of-America-Middle-Class-Kindle-Edition/dp/B0827RCB6G/ref=zg_bs_154849011_42/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 44: '/Think-Grow-Rich-Napoleon-Hill-ebook/dp/B08776ZZY4/ref=zg_bs_154849011_44/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 34: '/Think-Grow-Rich-Original-Version-ebook/dp/B07PB1LXYF/ref=zg_bs_154849011_34/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 46: '/Thinking-Systems-Donella-H-Meadows-ebook/dp/B005VSRFEA/ref=zg_bs_154849011_46/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 13: '/What-When-Bubble-Pops-Strategies-ebook/dp/B07V9YT592/ref=zg_bs_154849011_13/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA', 7: '/Zero-One-Notes-Startups-Future-ebook/dp/B00J6YBOFQ/ref=zg_bs_154849011_7/135-2728939-0957448?_encoding=UTF8&psc=1&refRID=GKBXE6KBVZTGW2B0TCKA'}
print({key: value for key, value in sorted(raw_books_url.items(), key=lambda item: item[1])})
# for key, value in fields_dict.items():
#     print(key, value)
# def selected_fields(choice):
#     fields_list = ['Title', 'Author', 'ASIN', 'Publisher', 'Publication date', 'Language', 'File size', 'Text-to-Speech', 'Enhanced typesetting', 'X-Ray', 'Word Wise', 'Print length', 'Lending', 'Best Sellers Rank', 'Customer Reviews', 'Narrator', 'Listening Length', 'Whispersync for Voice', 'Program Type', 'Version', 'Audible Release Date']
#     fields = []
#     if choice.lower() == 'manual':
#         for field in fields_list:
#             print(field, end=': ')
#             ch = input()[0]
#             if ch.lower() == "s":
#                 fields.append(field)
#         return fields
#     else:
#         return fields_list

# sl = input("choice: ")
# print(selected_fields(sl))

# print(fields_dict.keys())


# ASIN File size Text-to-Speech

# 619747200.000000
# def scheduler():
#     year = int(input("year: "))
#     month = int(input("month: "))
#     date = int(input("date: "))
#     hour = int(input("hour: "))
#     minute = int(input("minute: "))
#     # second = int(input(""))
#     second = 0
#     # then = datetime(2012, 3, 5, 23, 8, 15) 
#     then = datetime(year, month, date, hour, minute, second) 
#     print(then)
#     now  = datetime.now()   
#     print(now)                     
#     duration = (then-now)                       
#     duration_in_s = duration.total_seconds() 
#     print(duration_in_s)

    # # Date 1
    # date1 = "1 Jan 2000 00:00:00"

    # # Date 2
    # # Current date
    # date2 = "22 Aug 2019 00:00:00"

    # # Parse the date strings
    # # and convert it in
    # # time.struct_time object using
    # # time.strptime() method
    # obj1 = time.strptime(date1, "%d %b %Y %H:%M:%S")
    # obj2 = time.strptime(date2, "%d %b %Y %H:%M:%S")

    # # Get the time in seconds
    # # since the epoch
    # # for both time.struct_time objects
    # time1 = time.mktime(obj1)
    # time2 = time.mktime(obj2)

    # print("Date 1:", time.asctime(obj1))
    # print("Date 2:", time.asctime(obj2))

    # # Seconds between Date 1 and date 2
    # seconds = time2 - time1
    # print("Seconds between date 1 and date 2 is %f seconds" % seconds)

# scheduler()