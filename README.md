# Bug Hunter & TDD Calculator

Atividade de identificação de defeitos e correção com TDD sobre uma calculadora científica em Python.

**Autora:** Catarina Carrilho de Almeida | Ciência de Dados e Inteligência Artificial, SENAI CIMATEC | Data: 04/11/2026

## Como executar

```bash
pip install -r requirements.txt
python Calculadora.py     # executa a calculadora
pytest -v                 # executa os testes
```

> **Nota sobre o framework de testes:** o enunciado da atividade cita `unittest` na lista de materiais e `pytest` nas etapas de estudo e prática. Optei pelo `pytest`, que é o framework indicado no passo a passo da atividade e permite escrever os testes de forma mais simples, com `assert` e `@pytest.mark.parametrize`. O `pytest` também executa testes escritos em `unittest`, então a escolha não limita a verificação.

## Estrutura do repositório

```
Calculadora.py        código da calculadora (com a correção do BUG-001 e do BUG-004)
test_calculadora.py   testes automatizados (pytest)
Bugs.md               relatório de bugs (BUG-001 a BUG-012)
evidencias/           logs de erro, prints das execuções e saídas do pytest em cada fase do TDD
```

## Resumo do trabalho

Foram identificados 12 defeitos na calculadora, todos descritos em `Bugs.md` com localização, passos para reproduzir, resultado esperado e obtido, evidências, severidade, impacto e sugestão de correção. Entre eles estão resultado incorreto na adição, fatorial sempre igual a zero, logaritmo natural com função inexistente, logaritmo base 10 calculando o logaritmo natural e funções de seno, cosseno e tangente que aparecem no menu mas nunca foram implementadas.

O defeito escolhido para o TDD foi o BUG-004 (fatorial retorna sempre zero). O ciclo seguiu a ordem Red, Green e Refactor, e cada fase ficou registrada com a saída do pytest em `evidencias/` (`tdd-1-red.log`, `tdd-2-green.log` e `tdd-3-final.log`), além da documentação detalhada no `Bugs.md`. Antes do ciclo, o BUG-001 precisou ser corrigido, já que a chamada solta da função principal impedia qualquer importação do módulo pelos testes. Os demais bugs permanecem registrados como não resolvidos, e o BUG-005, que também envolve o fatorial, aparece nos testes como `xfail` para documentar o comportamento esperado.


## Reflexão sobre o processo com Scrum
Mesmo sendo uma atividade individual, deu para organizar o trabalho como no Scrum. O relatório de bugs fez o papel de Product Backlog: cada defeito virou um item com severidade, e isso ajudou a decidir por onde começar. A soma errada, por exemplo, é crítica porque afeta a operação mais básica, enquanto os casos de potência indefinida pesam menos. A sprint teve uma meta simples, que era corrigir um bug de ponta a ponta com TDD, e o resultado entregue foi o teste, a correção e a documentação no repositório.

O BUG-001 virou um impedimento. Para aplicar o TDD no fatorial, os testes precisavam importar o arquivo, mas a calculadora abria o menu logo no import e o pytest travava. Foi preciso resolver isso antes, colocando a chamada dentro do `__main__`, e só depois o ciclo de teste, correção e refatoração pôde andar. A definição de pronto também ajudou: o bug só foi considerado resolvido depois de rodar todos os testes e atualizar o relatório.

Na revisão, o que funcionou foi registrar cada fase do TDD, porque o histórico de commits e os logs mostram o que mudou em cada etapa. O que poderia melhorar é o ritmo: configurar o ambiente (Git, Python no PATH) e tirar os prints levou mais tempo do que o esperado, e os outros dez bugs ficaram só no relatório. Em uma próxima sprint, o ideal seria atacar esses bugs por ordem de severidade, começando pela adição e pelos logaritmos.
