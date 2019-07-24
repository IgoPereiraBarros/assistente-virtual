from selenium.webdriver import Firefox, Chrome

class SearchGoogle:

	def __init__(self, driver, url='https://www.google.com.br'):
		'''Informações
		   ----------- 
		   driver:
		   		- Objeto do tipo selenium.webdriver
		   		- Firefox, Chrome
		   url:
		   		- A url para pesquisa no navegador
		   		- tipo string
		'''
		self.driver = driver
		self.url = url

	def open_navegator(self):
		'''
			Abre a janela do navegador
		'''
		self.driver.get(self.url)

	def search(self, keyword, **kwargs):
		'''
			Informações
			-----------
			keyword:
				- palavra de consulta no navegador
				- tipo string
			kwargs:
				- parâmetro que será o atributo da tag html da página especionada
				- label_class --> buscar o nome do atributo classe
					- <input class="name" name="id">
					- find_element_by_class_name(label_class="name")
				- label_xpath --> busca pelo caminho da tag
					- <input class="pesquisa" name="tudo">
					- find_element_by_class_name(label_class='input[@class="pesquisa"]')
		'''
		self.driver.find_element_by_class_name(kwargs.get('label_class')).send_keys(keyword)
		self.driver.find_element_by_xpath(kwargs.get('label_xpath')).click()