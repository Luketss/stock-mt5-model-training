# stock-mt5-ml

# Objetivo
Repo teste para treinar modelos em qualquer timeframe passado e presente.
Requer o mt5 instalado. Minha recomendação é baixar ele diretamente pela corretora que possuir \
**USE A VERSÃO DEMO** \
Precisamos do mt5 para fazer a extração dos dados.

Esse código não faz a adição automática do ticker da ação vou deixar alguns exemplos:

| Ticker|
| ------|
| PETR4 |
| VALE3 |
| ABEV3 |
| BBAS3 |
| BBSE3 |
| ABEV3 |
| POMO4 |
| PETZ3 |
| LWSA3 |
| WEGE3 |

Esses tickers devem ser adicionados dentro da janela *observação de mercado* do mt5

# Configuração
Adicione as suas credenciais do Metatrader 5 dentro do arquivo setup.py

# Instalação
Tenha certeza que o diretório está na pasta correta

```bash
pip install virtualenv
```

Em seguida basta utilizar os comandos abaixo para *instalar* as dependencias e executar o código
```bash
python -m virtualenv .env
.env/Scripts/activate
pip install -r requirements.txt
```

Antes da execução altere as datas dentro do main.py de acordo com o tempo que deseja testar.
O `DATE_START` e o `DATE_END` foram criados com o objetivo de ser as variáveis de controle para treinamento.
Podem ser especificados grandes espaços de tempo. Já as `PREVISION_DATE_START` e `PREVISION_DATE_END` idealmente devem bater com as mesmas datas
previstas pela LSTM.
```bash
python main.py
```