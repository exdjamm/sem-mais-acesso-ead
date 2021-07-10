from eadapi import scrapead 

import os.path as path_os

from json import loads, dumps

DIR_NAME, _ = path_os.split(path_os.abspath(__file__))
session = None

## Code for fun
from time import sleep
import sys

TIME_LESS =  0.05
TIME = 0.07
TIME_MORE = 0.1
WAIT_TIME = 1


def print_letra(letra):
	sys.stdout.write(letra)
	sys.stdout.flush()

def print_slow(text: str):
	for letra in text:
		print_letra(letra)	
		sleep(TIME)

	sleep(WAIT_TIME)
	pass

def print_slow(text: str):
	for letra in text:
		print_letra(letra)	
		sleep(TIME)

	sleep(WAIT_TIME)
	pass

def print_more_slow(text: str):
	for letra in text:
		print_letra(letra)	
		sleep(TIME_MORE)

	sleep(WAIT_TIME)
	pass

def print_not_slow(text: str):
	for letra in text:
		print_letra(letra)	
	pass	

def print_clear(s: str):
	n = len(s)

	for i in range(n):
		max_n = n-i-1
		min_n = i+1
		text = "\r" + s[0:max_n] + " "*min_n

		print_not_slow(text)
		sleep(TIME_LESS)

	print_letra('\r')
	pass

## Code for EAD
def get_login():
	name_file = f"{DIR_NAME}/login.json"
	file_exists = path_os.exists(name_file)

	login = list()

	if file_exists:
		with open(name_file, 'r') as login_data:
			login = loads(login_data.read())

		print_slow("Parece que voce ja fez login...")
		print()	
		print_slow("Então vamos direto aos negocios!!")	
		print()
		print()

	else:
		print_slow("Sua primeira vez, ha?")
		print()
		print_slow("Não preocupe, tudo será rapido, mas vou pedir seu login do EAD")
		print()
		print()

		with open(name_file, 'w') as login_data:
			login = [
					input('Login: '), 
					input('Password: ')
				]

			login_data.write(dumps(login))

		print()

	return login

def filter_courses(course_name, course_id) -> bool:
	from datetime import date
	today = date.today()
	today_year = today.year

	# Cria uma lista de variação de marcação de semestres do ano
	# Ex: 2020/1, 2020-1, 2020/2, 2020-2
	semestres = []
	for semestre in range(1, 3):
		for divisor in ['-', '/']:
			semestres.append(f"{today_year}{divisor}{semestre}") 

	is_this_semestre = [term in course_name for term in semestres ]
	return any(is_this_semestre)

def filter_tasks(task_data) -> bool:
	return True

def marcar_presencas():
	global session

	courses_data = session.get_courses_data()

	for course_data in courses_data:
		nome = course_data['course_name']
		url = course_data['link']

		session.get(url)

		print(f"Marcando em: {nome}")

	pass

def main():
	global session

	print_slow("Bom dia!!!\n")

	print_slow("Hoje é belo dia para enganar o EAD, não é mesmo?")
	print_clear("Hoje é belo dia para enganar o EAD, não é mesmo?")
	
	print_more_slow("Hummm ...")

	username, password = get_login()

	session = scrapead.ScrapEad(username, password, filter_courses, filter_tasks)

	print_slow("Indo marcar presenças...")
	print()

	marcar_presencas()
	print("Presenças marcadas!!\n")
	print_slow("Finalizando sistema.... \nTenha um bom dia!!")
	print()


if __name__ == '__main__':
	main()