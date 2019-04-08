# 选课小程序:
# 选课多门实现?
# 更友好的输入?

# 如果我登陆后直接访问选课页面会报错
# 如果先访问
# http://zhjw.dlut.edu.cn/xkAction.do?actionType=-1&fajhh=5442  √
# 再去访问
# http://zhjw.dlut.edu.cn/xkAction.do?actionType=3&pageNumber=1&oper1=ori
# 就不会报错

# 完成!
import requests
from bs4 import BeautifulSoup
import re
import os
import time
print ("这是一个DUT多功能选课程序:\n\t\tMade by goldfish\n")
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Szfari/537.36',
        'Referer'  :'http://zhjw.dlut.edu.cn/xkAction.do'}
print("为了更好的体验效果,请给窗口设置如下:\n\t1 : 标题右键->属性->选项->编辑选项->√快速编辑模式\n\t2 : 标题右键->属性->布局->屏幕缓冲区->高度设置为800左右\n")
# beg = input("1 : 设置好了~  2 : 设置什么才不管~\n")
# if(beg == '2'):
# 	print("那就无所畏惧le~\n")
# 	time.sleep(2)
i = os.system('cls')
#登录
while True:
	dl = {
		'zjh':''
		,'mm':''
	}
	print("-------登录-------")
	# dl['zjh'] = input("学号:\n")
	# dl['mm'] = input("密码:\n")
	#dl['mm'] = '222'  #错误密码测试
	dl['zjh'] = '201551010'
	dl['mm'] = '1035679856'
	dlurl = "http://zhjw.dlut.edu.cn/loginAction.do"
	try:
		loginhtml = requests.post(dlurl,data = dl,headers = hea,timeout = 10)
	except Exception as e:
		print(str(e) + "\n")
		print("是否连上校园网了呢?\n")
		time.sleep(2)
		continue
	bs0 = BeautifulSoup(loginhtml.text,"html.parser")
	try :
		if(bs0.font.string):
			print(bs0.font.string+'\n')
	except:
		print("登陆成功~")
		time.sleep(2)
		i = os.system('cls')
		break

# 待改进:
# 非选课阶段输出信息
# 解析界面获取最后4位数字√
# 
# fflag = True 代表异常，直接退出
# pflag 判断是否直接从文件读取信息
fflag = False
pflag = True
xkurl = 'http://zhjw.dlut.edu.cn/xkAction.do'
xkhtml = requests.get(xkurl,cookies=loginhtml.cookies,headers=hea)
bs1 = BeautifulSoup(xkhtml.text,"html.parser")

# 清空list
with open("主要科目list.txt","w") as file:
	file.write("")
with open("选修科目list.txt","w") as file:
	file.write("")

# 检查是否在选课时间段
try: 
	print(bs1.font.string)
	fflag = True
except:
	code = bs1.find_all("input")[0].attrs['value']
# 选培养方案 很重要的一部 未选后面会出错
	tmpurl = 'http://zhjw.dlut.edu.cn/xkAction.do?actionType=-1&fajhh=' + code
	tmphtml = requests.get(tmpurl,cookies = loginhtml.cookies,headers = hea)
# suburl精确无误才能post 一定要完全按照正常选课流程!
while True:
	if (fflag == True):
		break
	opt = input("1 : 查看可选课程信息\n2 : 选课（课程号、课序号）\n3 : 重复选课\n4 : 删除可删课程\n5 : 展示已选课程\n6 : 一键评教\n9 : 清屏\n0 : 退出\n")
	
	if (opt == '1'):
	# 获取可选课程信息
		suburl = 'http://zhjw.dlut.edu.cn/xkAction.do'
		# global pflag
		zk = []
		params1 = {
			'actionType':'2',
			'pageNumber':1,
			# 'oper1':'ori'
		}
		ff = False
		while (pflag):
			zkhtml = requests.get(suburl,cookies = loginhtml.cookies,headers = hea,params=params1)
			bssub = BeautifulSoup(zkhtml.text,"html.parser")
			kcmc1 = bssub.find_all(name="a",attrs={"onclick":re.compile(r'view_kcxx\(\'')})
			for i in range(len(kcmc1)):
				if(kcmc1[i].span):
					kcmc1[i] = kcmc1[i].span.string
				else:
					kcmc1[i] = kcmc1[i].string
			kc_info = bssub.find_all(name="a",attrs={"onclick":re.compile(r'm_ckjs\(\'')})
			kcxh1 = []
			kcjs1 = []
			kcyl1 = []
			for i in range(len(kc_info)):
				kcyl1.append(kc_info[i].parent.next_sibling.next_sibling.string.strip())
				kcxh1.append(re.search(r'\d+\w',kc_info[i].attrs['onclick']).group(0) + '-' + re.search(r'\,\'\w?\d{2,3}',kc_info[i].attrs['onclick']).group(0).split("'")[1])
				kcjs1.append(kc_info[i].string)
				
			if(len(kcxh1) != len(kcmc1) or len(kcmc1) != len(kcjs1) or len(kcyl1) != len(kcjs1)):
				print ("length error!\n课程信息可能不匹配")
			else:
				fmt = "{0:^10}\t{1:^20}\t{2:^15}\t{3:^10}"
				with open("主要科目list.txt","a+") as file:
					if(not ff):
						file.write(fmt.format("课程号-课序号","课程名称","教师名称","课余量"+"\n"))
						ff = True
					for i in range(len(kcxh1)):
						try:
							zk.append([kcxh1[i],kcmc1[i],kcjs1[i],kcyl1[i]])
							file.write(fmt.format(kcxh1[i],kcmc1[i],kcjs1[i],kcyl1[i])+"\n")
						except:
							pass
			np = re.findall(r'下一页',zkhtml.text)
			if(np != []):
				params1['pageNumber'] +=  1
				# print (i);
			else: 
				break;

		xx = []  # 选修
		params2 = {
			'actionType':'3',
			'pageNumber':1,
			'oper1':'ori'
		}
		ff = False
		while (pflag):
			xxhtml = requests.get(suburl,cookies = loginhtml.cookies,headers = hea,params=params2)
			bssub = BeautifulSoup(xxhtml.text,"html.parser")
			kcmc2 = bssub.find_all(name="a",attrs={"onclick":re.compile(r'view_kcxx\(\'')})
			for i in range(len(kcmc2)):
				if(kcmc2[i].span):
					kcmc2[i] = kcmc2[i].span.string
				else:
					kcmc2[i] = kcmc2[i].string
			kc_info = bssub.find_all(name="a",attrs={"onclick":re.compile(r'm_ckjs\(\'')})
			kcxh2 = []
			kcjs2 = []
			kcyl2 = []
			for i in range(len(kc_info)):
				kcyl2.append(kc_info[i].parent.next_sibling.next_sibling.string.strip())
				kcxh2.append(re.search(r'\d+\w?',kc_info[i].attrs['onclick']).group(0) + '-' + re.search(r'\,\'\w?\d{2,3}',kc_info[i].attrs['onclick']).group(0).split("'")[1])
				kcjs2.append(kc_info[i].string)
				
			if(len(kcxh2) != len(kcmc2) or len(kcmc2) != len(kcjs2) or len(kcyl2) != len(kcjs2)):
				print ("length error!\n课程信息可能不匹配")
			else:
				fmt = "{0:^10}\t{1:^20}\t{2:^15}\t{3:^10}"
				with open("选修科目list.txt","a+") as file:
					if(not ff):
						ff = True
						file.write(fmt.format("课程号-课序号","课程名称","教师名称","课余量")+'\n')
					for i in range(len(kcxh2)):
						try:
							xx.append([kcxh2[i],kcmc2[i],kcjs2[i],kcyl2[i]])
							file.write(fmt.format(kcxh2[i],kcmc2[i],kcjs2[i],kcyl2[i])+'\n')
						except:
							pass
			np = re.findall(r'下一页',xxhtml.text)
			if(np != []):
				params2['pageNumber'] +=  1
			else: 
				break;
		# 输出课程信息.....
		if(pflag):
			fmt = "{0:^10}\t{1:^20}\t{2:^15}\t{3:^10}"
			print("\n---------------------------")
			print ("主要科目list:\n")
			print(fmt.format("课程号-课序号","课程名称","教师名称","课余量"),chr(12288))
			for i in range(len(zk)):
				print(fmt.format(zk[i][0],zk[i][1],zk[i][2],zk[i][3]),chr(12288))
			print("\n\n---------------------------")
			print ("选修科目list:\n")
			print(fmt.format("课程号-课序号","课程名称","教师名称","课余量"),chr(12288))
			for i in range(len(xx)):
				print(fmt.format(xx[i][0],xx[i][1],xx[i][2],xx[i][3]),chr(12288))
			print("---------------------------")
		else:
			fmt = "{0:^10}\t{1:^20}\t{2:^15}\t{3:^10}"
			print ("主要科目list:\n")		
			with open("主要科目list.txt","r") as file:
				for line in file.readlines():
					print(line,chr(12288))
			print("\n---------------------------")
			print ("选修科目list:\n")
			with open("选修科目list.txt","r") as file:
				for line in file.readlines():
					print(line,chr(12288))
			print("---------------------------")													
		pflag = False
		
	elif (opt == '2'):
	# 选课 查课
		suburl = 'http://zhjw.dlut.edu.cn/xkAction.do'
		params3 = {
			'actionType':'5',
			'pageNumber':1,
			'oper1':'ori'
		}
		while True:
			cx = {
				'kch' : '',
				'cxkxh' : '',
				'kcm' : '',
				'skjs' : '',
				'kkxsjc' : '',
				'skxq' : '',
				'skjc' : '',
				'pageNumber' : -2,
				'preActionType' : 3,
				'actionType' : 5
			}
			# cx['kch'] = '1010140010'
			# cx['cxkxh'] = '01'
			# 无法post中文 待解决
			# cx['kcm'] = "%C8%CF%CA%B6%CA%B5%CF%B0"
			# cx['skjs'] = "%CE%E2%D1%A9%C3%B7"
			print ("请输入待选课程的课程号、课序号信息,该内容必填")
			kch = cx['kch'] = input("课程号:10位数字\n")
			kxh = cx['kxh'] = input("课序号:2~3位\n")
			# cx['kcm'] = input("课程名称\n")
			# cx['skjs'] = input("教师名称\n")	
			if(kch == '' or kxh == ''):
				print("\t\t课程号或课序号未填,请重新操作.\n")
				continue
			cxhtml = requests.get(suburl,cookies = loginhtml.cookies,headers = hea,params=params3)
			rslhtml = requests.post(suburl,data = cx,cookies = loginhtml.cookies,headers = hea)
			bsrsl = BeautifulSoup(rslhtml.text,"html.parser")
			npc = re.findall(r'下一页',rslhtml.text)
			cbc = bsrsl.find_all(name="a",attrs={"onclick":re.compile(r'view_kcxx\(\'')})
			if (cbc == []):
				print ('\t\t未搜索到课程,请重新搜索\n')
			else:
				break

	# 如果已知到课程号课序号 可以直接跳到该操作要加那些代码
	# post选课
	# 一定要保证之前最后一页面有相应checkbox可以post 否则500
		xk = {
			'kcId':kch+'_'+kxh,
			'preActionType':'5',
			'actionType':'9'
		}
		rsl = requests.post(xkurl,data = xk,cookies = loginhtml.cookies,headers = hea)
		bsrsl = BeautifulSoup(rsl.text,"html.parser")
		try:
			rsltxt = bsrsl.font.string
			print (rsltxt+"\n")
		except:
			print("ERROR! 出现了一个bug?")

	elif(opt == '3'):
	# 重复选课
		suburl = 'http://zhjw.dlut.edu.cn/xkAction.do'
		params3 = {
			'actionType':'5',
			'pageNumber':1,
			'oper1':'ori'
		}
		while True:
			cx = {
				'kch' : '',
				'cxkxh' : '',
				'kcm' : '',
				'skjs' : '',
				'kkxsjc' : '',
				'skxq' : '',
				'skjc' : '',
				'pageNumber' : -2,
				'preActionType' : 3,
				'actionType' : 5
			}
			# cx['kch'] = '1010140010'
			# cx['cxkxh'] = '01'
			# 无法post中文 待解决
			# cx['kcm'] = "%C8%CF%CA%B6%CA%B5%CF%B0"
			# cx['skjs'] = "%CE%E2%D1%A9%C3%B7"
			print ("请输入待选课程的课程号、课序号信息,该内容必填")
			kch = cx['kch'] = input("课程号:10位数字\n")
			kxh = cx['kxh'] = input("课序号:2~3位\n")
			# cx['kcm'] = input("课程名称\n")
			# cx['skjs'] = input("教师名称\n")	
			if(kch == '' or kxh == ''):
				print("\t\t课程号或课序号未填,请重新操作.\n")
				continue
			cxhtml = requests.get(suburl,cookies = loginhtml.cookies,headers = hea,params=params3)
			rslhtml = requests.post(suburl,data = cx,cookies = loginhtml.cookies,headers = hea)
			bsrsl = BeautifulSoup(rslhtml.text,"html.parser")
			npc = re.findall(r'下一页',rslhtml.text)
			cbc = bsrsl.find_all(name="a",attrs={"onclick":re.compile(r'view_kcxx\(\'')})
			if (cbc == []):
				print ('\t\t未搜索到课程,请重新搜索\n')
			else:
				break
		xk = {
			'kcId':kch+'_'+kxh,
			'preActionType':'5',
			'actionType':'9'
		}
		i = input("为了防止查水表,频率别太快~\n 任意键继续~")
		while True:
			tim = int(input("请输入间隔时间(大于:10秒) 单位:s 参考参数:100\n"))
			if(tim >= 10):
				break
			else:
				print("\t\t非法输入 请重试！")
		while True:
			rsl = requests.post(xkurl,data = xk,cookies = loginhtml.cookies,headers = hea)
			bsrsl = BeautifulSoup(rsl.text,"html.parser")
			try:
				rsltxt = bsrsl.font.string
				print (rsltxt+"\n")
			except:
				print("ERROR! 出现了一个bug?")
				break
			if(rsltxt == '选课成功！' or re.findall(r'(你已经选择了课程|对不起)',rsltxt) != []):
				print("\t\t工作好啦~\n")
				break
			time.sleep(tim)

	# 课程删除:
	elif(opt == '4'):
		flag = True
		while(flag):
			suburl = 'http://zhjw.dlut.edu.cn/xkAction.do'
			params4 = {
				'actionType':'7'
			}
			params_del = {
				'actionType':'10',
				'kcId':''
			}
			whhtml = requests.get(suburl,headers = hea,cookies = loginhtml.cookies,params = params4)		
			whsoup = BeautifulSoup(whhtml.text,"html.parser")
			whkc = whsoup.find_all("a",attrs={'onclick':True})
			if(whkc != []):
				del_kcname = []
				del_jsname = []
				del_id = []
				for x in range(len(whkc)):
					# kc = str(kc)
					del_kcname.append(re.search(r'\(\'.+\'',str(whkc[x])).group(0).split('\'')[1])
					del_id.append(re.search(r'kcId=\d+',str(whkc[x])).group(0).split('=')[1])
					kc = whkc[x]
					for x in range(18):
						kc = kc.next_sibling
					# print(kc)
					del_jsname.append(kc.string.strip())
				if(len(del_kcname) != len(del_jsname) or len(del_jsname) != len(del_id)):
					print("\t\t删除列表信息可能缺失\n")
				for x in range(len(del_id)):
					print("-------"+str(x+1)+"---------")
					print(del_kcname[x])
					print(del_jsname[x])
					print(del_id[x])
					print("-----------------")
			else:
					print("\t\t目前无可删除课程\n")
					break
			while (flag):
				decision = input("请输入操作序号\n1：删除指定课程\t2：返回上一级\n")
				if(decision == '1'): 
					params_del['kcId'] = input("请输入删除课程的课程号:10位数字\n")
					delhtml = requests.get(suburl,headers = hea, cookies = loginhtml.cookies,params = params_del)
					break
				elif(decision == '2'):
					flag = False
				else:
					print("\t\t非法输入！\n")

	# 已选课程输出:
	# 效果比较差
	elif(opt == '5'):
		print ('\t\t建设维护中~\n')

	elif(opt == '6'):
		print ('\t\t建设维护中~\n')
		# suburl = 'http://zhjw.dlut.edu.cn/xkAction.do'
		# params4 = {
		# 	'actionType':'6'
		# }
		# yxkchtml = requests.get(suburl,cookies = loginhtml.cookies,params=params4,headers = hea)
		# bsyxkc = BeautifulSoup(yxkchtml.text,"html.parser")
		# yxkc = bsyxkc.find_all("tr",attrs={'class':"odd"})
		# for i in range(len(yxkc)):
			# yxinfo = yxkc[i].find_all("td")
			# for j in range(len(yxinfo)-1):
			# 	if(yxinfo[j+1].string):
			# 		print(yxinfo[j+1].string.strip()+'\t',end='')
			# print("\n")

	elif(opt == '9'):
		i = os.system('cls')
	elif(opt == '0'):
		break
	else:
		print("\t\t请重新输入\n")		

# 玄学!
#############################################################################
# 选课本页查询,界面太乱,已放弃
# 课程名编码一直提交不上去! 
# 其实已实现的也是post不上中文 可能是编码问题??
# while True:
# 	cxurl = 'http://zhjw.dlut.edu.cn/courseSearchAction.do'
# 	cxghtml = requests.get(cxurl,cookies = loginhtml.cookies,headers = hea)
# 	bsgcx = BeautifulSoup(cxghtml.text,"html.parser")
# 	cache = bsgcx.form.input.attrs['value']
# 	kcm = '复变函数'
# 	# skjs = ''
# 	# kch = input("请输入要选课的课程号(10位数字)\n")
# 	# kxh = input("请输入要选课的程序号(2-3位数字)\n")

# 	cx = {
# 		'org.apache.struts.taglib.html.TOKEN':cache,
# 		'kch':'',
# 		'kcm':'复变函数',
# 		'jsm':'',
# 		'xsjc':'',
# 		'skxq':'',
# 		'skjc':'',
# 		'xaqh':'',
# 		'jxlh':'',
# 		'jash':'',
# 		'pageSize':'50',
# 		'showColumn':('kkxsjc#开课系','kch#课程号','kcm#课程名','kxh#课序号','xf#学分',
# 					'kslxmc#考试类型','skjs#教师','zcsm#周次','skxq#星期','skjc#节次',
# 					'xqm#校区','jxlm#教学楼','jasm#教室','bkskrl#课容量','xss#学生数'),
# 		# 'showColumn':('kkxsjc%23%BF%AA%BF%CE%CF%B5','kch%23%BF%CE%B3%CC%BA%C5','kcm%23%BF%CE%B3%CC%C3%FB','kxh%23%BF%CE%D0%F2%BA%C5','xf%23%D1%A7%B7%D6',
# 		# 			'kslxmc%23%BF%BC%CA%D4%C0%E0%D0%CD','skjs%23%BD%CC%CA%A6','zcsm%23%D6%DC%B4%CE','skxq%23%D0%C7%C6%DA','skjc%23%BD%DA%B4%CE',
# 		# 			'xqm%23%D0%A3%C7%F8','jxlm%23%BD%CC%D1%A7%C2%A5','jasm%23%BD%CC%CA%D2','bkskrl%23%BF%CE%C8%DD%C1%BF','xss%23%D1%A7%C9%FA%CA%FD'),
# 		'pageNumber':'0',
# 		'actionType':'1'
# 	}
# 	cxhtml = requests.post(cxurl,data = cx,cookies = loginhtml.cookies,headers = hea)
# 	npc = re.findall(r'下一页',cxhtml.text)
# 	cbc = re.findall(r'class=\'odd\"',cxhtml.text)
# 	if (cbx == []):
# 		print ('未搜索到课程,请重新搜索')
# 	elif (npc == []):
# 		break
# 	else:
# 		print ('查询结果过多,试着换一下关键词吧')
# bscx = BeautifulSoup(cxhtml.text,"html.parser")

# infogain = bscx.find_all("a",attrs={'href':"#"})
# for i in range(len(infogain)):
# 	if(re.find(r''))
