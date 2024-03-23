from openpyxl import Workbook as Planilha

planilhinha = Planilha()
folha_ativa = planilhinha.active

lista = [
    ["Nome", "Idade", "Cidade"]
]


for _ in range(3):    
    nome = input("Insira seu nome: ")    
    idade = input("Insira sua idade: ")
    cidade = input("Insira sua cidade: ")
    lista.append([nome, idade, cidade])
        
for linha in lista:
    folha_ativa.append(linha)

    planilhinha.save("alunos.xlsx")
    
