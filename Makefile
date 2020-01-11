pull:
	git pull
update:
	pip3 install -r requirements.txt
server:
	mysqld_safe --skip-grant-tables &
	python3 main.py
