# Bug Hunter & TDD Calculator

Atividade individual de identificação de defeitos e correção com TDD sobre uma calculadora científica em Python (`Calculadora.py`).

**Autora:** Catarina Carrilho de Almeida | Ciência de Dados e Inteligência Artificial, SENAI CIMATEC | Data: 04/11/2026

## Como executar

```bash
pip install -r requirements.txt
python Calculadora.py     # executa a calculadora
pytest -v                 # executa os testes
```

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

Mesmo em uma atividade individual, foi possível organizar o trabalho com a lógica do Scrum. O relatório de bugs funcionou como Product Backlog: cada defeito virou um item descrito e priorizado por severidade, o que deixou claro que a adição incorreta (crítica) tinha mais urgência do que o tratamento de potências indefinidas (baixa). A sprint teve uma meta curta e objetiva, que era corrigir um bug de ponta a ponta com TDD, e o incremento entregue foi o conjunto de commits com teste, correção e documentação.

O BUG-001 mostrou na prática o que é um impedimento na sprint. A meta era aplicar TDD ao fatorial, mas o código não podia ser importado pelos testes até que a chamada automática do menu fosse isolada em `__main__`. Resolver o impedimento antes de seguir foi mais produtivo do que contorná-lo com ajustes nos testes. A definição de pronto também ajudou a decidir quando parar: o bug só foi dado como resolvido depois de teste falhando, correção mínima, refatoração, execução de toda a suíte e atualização do relatório.

Na revisão da sprint, o ponto positivo foi o histórico de commits, que conta a história da correção e permite que outra pessoa entenda cada decisão. Como ponto de melhoria para uma próxima sprint, ficam os bugs restantes, que poderiam ser atacados em ordem de severidade, começando pela adição e pelos logaritmos. A retrospectiva também indica que escrever o relatório de bugs antes de mexer no código evitou correções apressadas e deixou o escopo da sprint visível desde o início.
