#!/bin/python3.8
from requests import Session
from eadapi.scrap_utils import getDataByDict

# class for files in tasks : fileuploadsubmission

import os.path as path_os
DIR_NAME, _ = path_os.split(path_os.abspath(__file__))

class SessionEad(Session):

	"""Cria uma Session autenticada com o login e senha passados no site do EAD IFMS.
	Para ser utilizada para realizar os requests.
	
	Author: Êxodo Jaffar
	"""	

	def __init__(self, username: str, password: str) -> None:
		super(SessionEad, self).__init__()

		self.headers.update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'})
		self.verify = f"{DIR_NAME}/../ead-ifms-edu-br-chain.pem"

		self._filter_data = getDataByDict

		self.__url_base = "https://ead.ifms.edu.br/"
		self._login_token = str() 
		self._session_key = str()

		# Shutdown the need for load JS in the pages
		self.get(self._url(), params={"canceljssession":1})
		
		# print("[Session]\t Starts ...")

		self.__login(username, password)
		pass

	def __login(self, username: str, password: str) -> None:
		self.__set_login_token()
		responde_text_login_request = self.__send_login_request(username, password)
		self.__set_session_key(responde_text_login_request)
		
		pass
	
	def _url(self, path=str()) -> str:
		# isso poderia ser feito por uma classe acima?
		url = self.__url_base + path #+ "?"

		return url

	def __set_login_token(self) -> None:
		# print("[Session]\t Get Token ...")
		
		response_text = self.get(self._url(), ).text
		login_token = self._filter_data(response_text, tag="input", filters={"name":"logintoken"}, value="value")

		# print("[Session]\t Done")

		self._login_token = login_token
		pass

	def __set_session_key(self, to_filter_text: str) -> None:
		session_key = getDataByDict(to_filter_text, tag='a', filter={'data-title':'logout,moodle'}, value='href').split('=')[1]
		
		# print("[Session]\t Done")
		
		self._session_key = session_key
		pass
	
	def __send_login_request(self, username: str, password: str) -> str:
		# print("[Session]\t Login ... ")

		payload = {"username":username, "password":password, "logintoken":self._login_token}
		responde_text = self.post(self._url("login/index.php"), data=payload).text

		return responde_text
	
	def set_new_login(self, username: str, password: str) -> None:
		self.__login(username, password)

		pass

if __name__ == '__main__':
	login = input("Digite o seu login >>> ")
	senha = input("Digite a sua senha >>> ")
	main =  SessionEad(login, senha)
