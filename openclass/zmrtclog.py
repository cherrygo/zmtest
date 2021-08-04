#coding:utf8

import xlrd
import xlwt     #导入xlwt

def write_excel():
    filePath = u"D:/测试包/zmrtcDemo_release_2019-01-08_14.50.26/__output_status_data.txt"
    targetPath=u"D:/测试包/data17.xls"
    f0 = xlwt.Workbook()
    sheet1 = f0.add_sheet('Sheet1',cell_overwrite_ok = True)
    result=""
    index=1     #行索引
    first_line = True

    with open(filePath) as f:
        sheet1.write(0, 0, u'本地视频码率')
        sheet1.write(0, 1, u'远端视频码率')
        sheet1.write(0, 2, u'本地视频宽度输出')
        sheet1.write(0, 3, u'本地视频高度输出')
        sheet1.write(0, 4, u'本地音频码率')
        sheet1.write(0, 5, u'远端音频码率')
        sheet1.write(0, 6, u'本地视频帧率')

        for line in f:
            if first_line:
                first_line = False
                continue
            if "_lv_nBytesSent" in line:
                result = line.split("=")[1].replace("\n","").strip()
                sheet1.write(index,0,float(result))
            if "_rv_nBytesReceived" in line:
                result = line.split("=")[1].replace("\n", "").strip()
                sheet1.write(index, 1, float(result))
            if "_lv_nFrameWidthSent" in line:
                result = line.split("=")[1].replace("\n", "").strip()
                sheet1.write(index, 2, float(result))
            if "_lv_nFrameHeightSent" in line:
                result = line.split("=")[1].replace("\n", "").strip()
                sheet1.write(index, 3, float(result))
            if "_la_nBytesSent" in line:
                result=line.split("=")[1].replace("\n","").strip()
                sheet1.write(index, 4,float(result))
            if "_ra_nBytesReceived" in line:
                result = line.split("=")[1].replace("\n", "").strip()
                sheet1.write(index,5,float(result))
            if "_lv_nFrameRateSent" in line:
                result = line.split("=")[1].replace("\n", "").strip()
                sheet1.write(index, 6, float(result))


            if '-------------------------------------' in line:
                index = index + 1

    f0.save(targetPath)

if __name__ == '__main__':
    write_excel()
