
class mstplugin:
	infos=[
	['Name','What_Cms'],
	['Description','Match the cms type'],
	['Author','L34Rn'],
	['Mail','cnh4ckff@gmail.com'],
	['Blog','http://hi.baidu.com/l34rn'],
	['DATE','20131023'],
	['IMPORT','[dicts/what_cms/] => [Web_dir::Hash::cms]']
	]
	
	opts=[
	['HOST','www.cms.com','The host need to match'],
	['PORT','80','The port of the webserver'],
	['PATH','/','The path of the cms who need to match']
	]


	def exploit(self):
		host=self.host_reduce_http(HOST)
		port=PORT
		path=PATH
		color.cprint('[+] what_cms start OK!',BLUE)
		color.cprint('[+] [TARGET] '+host,BLUE)
		if str(host)=='443':
			_host='http://'+host+path
		else:
			_host='http://'+host+':'+port+path
		try:
			cms=self.what_cms(_host)
			if cms=='Falied':
				color.cprint('\n[!] All Done!\n[!] But Falied!',RED)
			else:
				color.cprint('\n[+] Good News!\n[+] '+cms,GREEN)
		except Exception,e:
			color.cprint('\n[!] Error=>'+str(e),RED)
			
	def host_reduce_http(self,host):
		l=len(host.split('//'))
		if l==1:
			host=host.strip()
			host=host.split('/')[0]
		elif l==2:
			host=host.split('//')[1]
			host=host.split('/')[0]
		else:
			host='Error!'
		return host

	def what_cms(sself,host):
		
		def get_md5(html):
			m=hashlib.md5()
			m.update(html)
			md5=m.hexdigest()
			return md5

		def get_html(url):
			url=url.strip()
			html=urllib.urlopen(url).read()
			return html

		cms_list=listdir('dicts/what_cms/')
		
		for cms in cms_list:
			f=open('dicts/what_cms/'+cms,'r')
			lines=f.readlines()
			f.close()
			for line in lines:
				l=line.split('::')
				web_dir=l[0]
				hash=l[1]
				cms_version=l[2]
				url=host+web_dir
				sys.stdout.write('\r[*] [TRYING] %s'% web_dir.strip())
				try:
					_html=get_html(url)
					_md5=get_md5(_html)
					if _md5==hash:
						result=url+' => '+cms_version
						return result
						break
				except Exception,e:
					color.cprint('[!] Error=>'+str(e),RED)
					pass
		return 'Falied'
