'''	 BOT ESTRAGIA MHI v2
	- Analise em 1 minuto
	- Entradas para 1 minuto
	- Calcular as cores das velas de cada quadrado, ultimas 3 velas, minutos: 2, 3 e 4 / 7, 8 e 9
	- Entrar contra a maioria
'''

from iqoptionapi.stable_api import IQ_Option
import logging, json, sys
import time, configparser
from datetime import datetime
from dateutil import tz


def stop(lucro, gain, loss):
	if lucro <= float('-' + str(abs(loss))):
		print('Stop Loss batido!')
		sys.exit()
		
	if lucro >= float(abs(gain)):
		print('Stop Gain Batido!')
		sys.exit()

def Martingale(valor, payout):
	lucro_esperado = valor * payout
	perca = float(valor)	
		
	while True:
		if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
			return round(valor, 2)
			break
		valor += 0.01

def Payout(par):
	API.subscribe_strike_list(par, 1)
	while True:
		d = API.get_digital_current_profit(par, 1)
		if d != False:
			d = round(int(d) / 100, 2)
			break
		time.sleep(1)
	API.unsubscribe_strike_list(par, 1)
	
	return d

print('''
 ------------------------------------
 XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
 ------------------------------------ 
       
  ..:: TREX MHI AUTO TRADER 1.0 ::..
   
ESTE SOFTWARE ESTA EM DESENVOLVIMENTO 
              
           [_xXx 2025 xXx_]
             
 ------------------------------------
 XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
 ------------------------------------
''')

def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')

    return {'email': arquivo.get('GERAL', 'email'), 'senha': arquivo.get('GERAL', 'senha'), 'conta': arquivo.get('GERAL', 'conta')}
  
conf = configuracao()
API = IQ_Option(conf['email'], conf['senha'])
API.connect()
API.change_balance(conf['conta'])

if API.check_connect():
	print(' [_ Conectado com sucesso! _] \n')
else:
	print(' [_ Erro ao conectar _] ')
	input('\n\n Aperte enter para sair')
	sys.exit()

def perfil(): # Função para capturar informações do perfil
	perfil = json.loads(json.dumps(API.get_profile_ansyc()))
	
	return perfil
	
	'''
		name
		first_name
		last_name
		email
		city
		nickname
		currency
		currency_char 
		address
		created
		postal_index
		gender
		birthdate
		balance		
	'''

def timestamp_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]
    
x = perfil ()

print(x['name'])
print(x['email'])
print(x['currency'])
print(x['balance'])
print(API.get_balance())

'''
	Para pegar somente a quantia da sua banca utilize: banca = API.get_balance()
'''

print('\n')

def payout(par, tipo, timeframe = 1):
	if tipo == 'turbo':
		a = API.get_all_profit()
		return int(100 * a[par]['turbo'])
		
	elif tipo == 'digital':
	
		API.subscribe_strike_list(par, timeframe)
		while True:
			d = API.get_digital_current_profit(par, timeframe)
			if d != False:
				d = int(d)
				break
			time.sleep(1)
		API.unsubscribe_strike_list(par, timeframe)
		return d

par = API.get_all_open_time()

for paridade in par['turbo']:
	if par['turbo'][paridade]['open'] == True:
		print('[ TURBO ]: '+paridade+' | Payout: '+str(payout(paridade, 'turbo')))
		
print('\n')

for paridade in par['digital']:
	if par['digital'][paridade]['open'] == True:
		print('[ DIGITAL ]: '+paridade+' | Payout: '+str( payout(paridade, 'digital') ))
        
while True:
	try:
		operacao = int(input('\n Deseja operar na\n  1 - Digital\n  2 - Binaria\n  R: '))
		
		if operacao > 0 and operacao < 3 : break
	except:
		print('\n Opção invalida')
print('\n')        

while True:
	try:
		tipo_mhi = int(input(' Deseja operar a favor da\n  1 - Minoria\n  2 - Maioria\n  R: '))
		print('\n')
		if tipo_mhi > 0 and tipo_mhi < 3 : break
	except:
		print('\n Opção invalida')
        


par = input(' Indique uma paridade para operar: ').upper()
print('\n')
valor_entrada = float(input(' Indique um valor para entrar: '))
valor_entrada_b = float(valor_entrada)
print('\n')
martingale = int(input(' Indique a quantia de martingales: '))
martingale += 1
print('\n')
stop_loss = float(input(' Indique o valor de Stop Loss: '))
stop_gain = float(input(' Indique o valor de Stop Gain: '))

lucro = 0
payout = Payout(par)
print('\n')

while True:
	minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
	entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
	print('''    
                        █████████
                        █▄█████▄█
                        █▼▼▼▼▼       ██    ██    ██    ██       ██
                        █            ██                         ██   
                        █            ██ AGUARDANDO OPORTUNIDADE ██
                        █            ██                         ██
                        █▲▲▲▲▲       ██    ██    ██    ██       ██
                        █████████
                         ██ ██
                         
        ''')
	
	if entrar:
		print('\n\n [_ Iniciando Operação ! _] ')
		dir = False
		print('\n Verificando cores: ', end='')
		velas = API.get_candles(par, 60, 3, time.time())
		
		velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
		velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
		velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
		
		cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
		print(cores)
	
		if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = ('put' if tipo_mhi == 1 else 'call')
		if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = ('call' if tipo_mhi == 1 else 'put')
		
		if dir:
			print('\n [_ Direção _]:',dir)
			
			valor_entrada = valor_entrada_b
			for i in range(martingale):
			
				status,id = API.buy_digital_spot(par, valor_entrada, dir, 1) if operacao == 1 else API.buy(valor_entrada, par, dir, 1)
				
				if status:
					while True:
						try:
							status,valor = API.check_win_digital_v2(id) if operacao == 1 else API.check_win_v3(id)
						except:
							status = True
							valor = 0
						
						if status:
							valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
							lucro += round(valor, 2)
							
							print('\n [_ RESULTADO:', end='')
							print(' WIN _] |' if valor > 0 else ' LOSS _] |' , round(valor, 2) ,'| [_ LUCRO: ', round(lucro, 2),('| '+str(i)+ ' GALE _] ' if i > 0 else '' ))
							print('\n')
							valor_entrada = Martingale(valor_entrada, payout)
							
							stop(lucro, stop_gain, stop_loss)
							
							break
						
					if valor > 0 : break
					
				else:
					print('\nERRO AO REALIZAR OPERAÇÃO\n\n')
				
	time.sleep(0.5)
