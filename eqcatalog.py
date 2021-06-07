# 简介：类rdeqcatalog用于读取地震目录，其中包含rdeqt和rdq01两个函数，分别用于读取eqt目录和q01目录
# 作者：wangpengtao
# 时间：2021年6月7日


import pandas as pd
import re

# catalog = '中国大陆Ms6.EQT'
class rdeqcatalog():

    def rdeqt(catalog):
        regex = re.compile(r'(^[\s-][\s\d]{2}\d{12})([-\s\d.]{6})([-\s\d.]{7})([\d.]{4})([\s\d]{3})(\d{3})(\s)([\u4e00-\u9fa5]+)')  # eqt分割正则表达式
        di = {'datetime':[],'lat':[],'lon':[],'mag':[],'dep':[],'sta':[],'name':[]}

        with open(catalog, 'r') as f:    
            ln = f.readline()
            i = 0
            while ln:
                try:
                    m = regex.search(ln)
                    di['datetime'].append(m.group(1))
                    di['lat'].append(m.group(2))
                    di['lon'].append(m.group(3))
                    di['mag'].append(m.group(4))
                    di['dep'].append(m.group(5))
                    di['name'].append(m.group(8))
                except:
                    print('读取EQT格式地震目录第' + str(i+1) + '行出现问题')
                i += 1
                ln = f.readline()

        tb = pd.DataFrame(di)
        return tb

    def rdq01(catalog):
        regex = re.compile(r'(^\d{14})([\d.]{2})([-\s\d]{3})(\d{2})([-\s\d]{4})(\d{2})([\sA-Za-z]{3})([\d.]{3})([\s\d]{4})([\s\d]{6})([\u4e00-\u9fa5]+)')  # eqt分割正则表达式
        di = {'datetime':[],'lat':[],'lon':[],'mag':[],'dep':[],'name':[]}
        with open(incat, 'r') as f:
            ln = f.readline()
            i = 0
            while ln:
                try:
                    m = regex.search(ln)
                    di['datetime'].append(m.group(1))
                    di['lat'].append(int(m.group(3))+int(m.group(4))/60)
                    di['lon'].append(int(m.group(5))+int(m.group(6))/60)
                    di['mag'].append(m.group(8))
                    di['dep'].append(m.group(9))
                    di['name'].append(m.group(11))
                except:
                    print('读取Q01格式地震目录第' + str(i+1) + '行出现问题')
                i += 1
                ln = f.readline()

        tb = pd.DataFrame(di)
        return tb


if __name__ == "__main__":
    rdeqcatalog()
    
