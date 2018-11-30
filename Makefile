FILE_ID := 17e8BYfvr54-mqi8pEUji_kxN4wEAyGV1JdWy-A80b20

tiaas.tsv:
	@./gdrive export $(FILE_ID) --mime text/tab-separated-values --force
	@mv 'useGalaxy.eu: TIaaS Request Form (Responses)' tiaas.tsv

all:
	@python process.py
