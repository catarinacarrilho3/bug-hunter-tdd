# Relatório de Bugs - Calculadora.py

Relatório de defeitos identificados no arquivo `Calculadora.py` (calculadora científica), elaborado para a atividade Bug Hunter & TDD Calculator.

**Autora:** Catarina Carrilho de Almeida | Ciência de Dados e Inteligência Artificial, SENAI CIMATEC | Data: 04/11/2026


## Resumo

| ID | Título | Severidade | Status |
|---|---|---|---|
| BUG-001 | Calculadora executa automaticamente ao importar o módulo | Média | Resolvido |
| BUG-002 | Adição retorna o primeiro número somado duas vezes | Crítica | Não resolvido |
| BUG-003 | Divisão por zero encerra o programa com exceção | Alta | Não resolvido |
| BUG-004 | Fatorial retorna sempre zero | Alta | Resolvido |
| BUG-005 | Fatorial aceita número negativo e retorna 1 | Média | Não resolvido |
| BUG-006 | Logaritmo natural usa função inexistente no NumPy | Alta | Não resolvido |
| BUG-007 | Logaritmo base 10 calcula logaritmo natural | Alta | Não resolvido |
| BUG-008 | Logaritmo base 10 aceita zero | Média | Não resolvido |
| BUG-009 | Funções cosseno e tangente não existem | Alta | Não resolvido |
| BUG-010 | Opção Seno do menu não tem função nem tratamento | Média | Não resolvido |
| BUG-011 | Entrada não numérica encerra o programa | Média | Não resolvido |
| BUG-012 | Potenciação sem tratamento de casos indefinidos | Baixa | Não resolvido |

## BUG-001: Calculadora executa automaticamente ao importar o módulo

**Localização do bug:** Calculadora.py, última linha (chamada `calculadora_cientifica()` fora de bloco `__main__`)

**Descrição clara do bug:** A chamada à função principal está no nível do módulo, sem a proteção `if __name__ == "__main__":`. Qualquer `import Calculadora` dispara o menu e aguarda entrada do teclado. Com isso, nenhuma função pode ser importada para teste automatizado, pois o pytest interrompe a coleta com `OSError` ao tentar ler a entrada padrão durante o import. O defeito bloqueia toda a prática de TDD sobre o arquivo.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python -c "import Calculadora"` e observar que o menu aparece e o programa pede a operação.
3. Criar um teste que importe qualquer função do módulo e executar `pytest`.

**Consistência:** Ocorre sempre.

**Resultado esperado:** O import deve apenas carregar as funções, sem executar o menu.

**Resultado obtido:** O menu é exibido e o programa tenta ler a entrada; sem teclado interativo, termina com `EOFError: EOF when reading a line`. No pytest, a coleta é interrompida com `OSError: pytest: reading from stdin while output is captured`.

**Evidências (logs de erro):** `evidencias/bug-001-import.log e evidencias/bug-001-pytest.log`

**Severidade:** Média

**Impacto:** Impede testes automatizados e reaproveitamento das funções em outros módulos.

**Sugestão de correção:** Envolver a chamada final em `if __name__ == "__main__":`.

**Data de identificação:** 04/11/2026

**Status:** Resolvido

**Correção aplicada:** a chamada final `calculadora_cientifica()` foi movida para dentro de `if __name__ == "__main__":`. A alteração foi feita como pré-requisito do TDD, já que os testes precisam importar o módulo sem disparar o menu. O comportamento ao executar `python Calculadora.py` permanece o mesmo.

---

## BUG-002: Adição retorna o primeiro número somado duas vezes

**Localização do bug:** Calculadora.py, função `adicao`

**Descrição clara do bug:** A função retorna `x + np.add(x, y)`, que equivale a `2x + y`. A operação mais básica da calculadora produz resultado incorreto para qualquer entrada diferente de x = 0.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `1` no menu.
4. Informar `2` como primeiro número.
5. Informar `3` como segundo número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Resultado: 5.0

**Resultado obtido:** Resultado: 7.0

**Evidências (logs de erro):** `evidencias/bug-002-adicao.log`

**Severidade:** Crítica

**Impacto:** Todo cálculo que dependa de soma fica errado, sem qualquer aviso ao usuário.

**Sugestão de correção:** Retornar apenas `x + y` ou `np.add(x, y)`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-003: Divisão por zero encerra o programa com exceção

**Localização do bug:** Calculadora.py, função `divisao`

**Descrição clara do bug:** A função executa `x / y` sem verificar se `y` é zero. O Python levanta `ZeroDivisionError` e o programa é interrompido com traceback, em vez de informar o erro ao usuário.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `4` no menu.
4. Informar `10` como primeiro número.
5. Informar `0` como segundo número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Mensagem de erro tratada, mantendo a calculadora em funcionamento.

**Resultado obtido:** `ZeroDivisionError: float division by zero` e encerramento do programa.

**Evidências (logs de erro):** `evidencias/bug-003-divisao.log`

**Severidade:** Alta

**Impacto:** Uma entrada comum derruba a aplicação inteira.

**Sugestão de correção:** Validar `y == 0` antes da divisão e levantar `ValueError` ou retornar mensagem de erro.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-004: Fatorial retorna sempre zero

**Localização do bug:** Calculadora.py, função `fatorial` (laço `for i in range(x+1)`)

**Descrição clara do bug:** O laço começa em `i = 0`, pois `range(x+1)` gera valores de 0 a x. Na primeira iteração `fat *= 0` zera o acumulador, e todas as iterações seguintes mantêm o zero. O resultado é 0 para qualquer entrada positiva, e até para `fatorial(0)`, que deveria valer 1.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `7` no menu.
4. Informar `5` como número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Resultado: 120

**Resultado obtido:** Resultado: 0

**Evidências (logs de erro):** `evidencias/bug-004-fatorial.log`

**Severidade:** Alta

**Impacto:** A operação de fatorial fica totalmente inutilizável.

**Sugestão de correção:** Iniciar o laço em 1: `range(1, x+1)`.

**Data de identificação:** 04/11/2026

**Status:** Resolvido

**Documentação da correção (TDD):** o bug foi tratado seguindo o ciclo Red, Green, Refactor.

1. Red: o arquivo `test_calculadora.py` foi criado com testes parametrizados para `fatorial` (valores 0, 1, 2, 5 e 10). Ao rodar `pytest -v`, os 5 testes falharam, confirmando o defeito (ver `evidencias/tdd-1-red.log`).
2. Green: a correção mínima foi trocar `range(x+1)` por `range(1, x+1)`. Os 5 testes passaram (ver `evidencias/tdd-2-green.log`).
3. Refactor: a variável `fat` foi renomeada para `resultado` e a função recebeu docstring, sem mudar o comportamento. Os testes continuaram passando.
4. Verificação final: foram adicionados testes de regressão para `subtracao`, `multiplicacao` e `raiz_quadrada`, que não foram alteradas, e um teste marcado como `xfail` para o BUG-005, ainda não corrigido (ver `evidencias/tdd-3-final.log`).

A correção resolve o bug porque o acumulador deixa de ser multiplicado por zero, e `fatorial(0)` passa a retornar 1, como define a matemática.

---

## BUG-005: Fatorial aceita número negativo e retorna 1

**Localização do bug:** Calculadora.py, função `fatorial`

**Descrição clara do bug:** Não há validação do argumento. Para valores negativos o laço não executa nenhuma iteração e a função devolve 1, resultado sem sentido matemático, pois o fatorial não é definido para inteiros negativos.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `7` no menu.
4. Informar `-3` como número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Mensagem de erro ou exceção `ValueError`.

**Resultado obtido:** Resultado: 1

**Evidências (logs de erro):** `evidencias/bug-005-fatorial-negativo.log`

**Severidade:** Média

**Impacto:** O usuário recebe um resultado incorreto como se fosse válido.

**Sugestão de correção:** Levantar `ValueError` quando `x < 0`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-006: Logaritmo natural usa função inexistente no NumPy

**Localização do bug:** Calculadora.py, função `logaritmo_natural` (`np.ln`)

**Descrição clara do bug:** O NumPy não possui `np.ln`. A função correta para logaritmo natural é `np.log`. Qualquer entrada válida provoca `AttributeError`.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `8` no menu.
4. Informar `2.718` como número.

**Consistência:** Ocorre sempre para entradas positivas.

**Resultado esperado:** Resultado aproximado de 1.0

**Resultado obtido:** `AttributeError: module 'numpy' has no attribute 'ln'` e encerramento do programa.

**Evidências (logs de erro):** `evidencias/bug-006-ln.log`

**Severidade:** Alta

**Impacto:** A operação de logaritmo natural nunca funciona.

**Sugestão de correção:** Trocar `np.ln(x)` por `np.log(x)`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-007: Logaritmo base 10 calcula logaritmo natural

**Localização do bug:** Calculadora.py, função `logaritmo_base10` (`np.log`)

**Descrição clara do bug:** A função chama `np.log`, que é o logaritmo natural. Para base 10 o correto é `np.log10`. O programa não acusa erro, mas devolve um valor numérico errado.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `9` no menu.
4. Informar `100` como número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Resultado: 2.0

**Resultado obtido:** Resultado: 4.605170185988092

**Evidências (logs de erro):** `evidencias/bug-007-log10.log`

**Severidade:** Alta

**Impacto:** Resultado silenciosamente incorreto, difícil de perceber.

**Sugestão de correção:** Trocar `np.log(x)` por `np.log10(x)`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-008: Logaritmo base 10 aceita zero

**Localização do bug:** Calculadora.py, função `logaritmo_base10` (condição `x < 0`)

**Descrição clara do bug:** A validação usa `x < 0`, mas o logaritmo não é definido para zero. A mensagem de erro da própria função diz "não positivo", o que indica que a condição correta seria `x <= 0`, como já ocorre em `logaritmo_natural`. Para `x = 0` o programa devolve `-inf` e emite `RuntimeWarning`.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `9` no menu.
4. Informar `0` como número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Mensagem: "Erro: Logaritmo de número não positivo"

**Resultado obtido:** `RuntimeWarning: divide by zero encountered in log` e Resultado: -inf

**Evidências (logs de erro):** `evidencias/bug-008-log10-zero.log`

**Severidade:** Média

**Impacto:** Valor inválido é exibido como resultado e a validação fica inconsistente com a outra função de logaritmo.

**Sugestão de correção:** Alterar a condição para `x <= 0`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-009: Funções cosseno e tangente não existem

**Localização do bug:** Calculadora.py, `calculadora_cientifica` (opções 11 e 12 chamam `cosseno` e `tangente`)

**Descrição clara do bug:** O menu oferece cosseno e tangente e o fluxo principal chama essas funções, mas elas nunca foram definidas no arquivo. A chamada de tangente ainda usa o parâmetro `radianos=False`, que também não existe em nenhuma definição.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `11` no menu.
4. Informar `60` como ângulo em graus.
5. Repetir com a opção `12` e o ângulo `45`.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Cosseno de 60° igual a 0.5 e tangente de 45° igual a 1.0 (aproximadamente).

**Resultado obtido:** `NameError: name 'cosseno' is not defined` e `NameError: name 'tangente' is not defined`.

**Evidências (logs de erro):** `evidencias/bug-009-cosseno.log e evidencias/bug-009-tangente.log`

**Severidade:** Alta

**Impacto:** Duas operações anunciadas no menu derrubam o programa.

**Sugestão de correção:** Implementar `cosseno(x)` e `tangente(x, radianos=True)` com `np.cos`, `np.tan` e `np.radians`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-010: Opção Seno do menu não tem função nem tratamento

**Localização do bug:** Calculadora.py, `menu` e `calculadora_cientifica` (opção 10)

**Descrição clara do bug:** O menu lista a opção 10 (Seno), mas não existe função `seno` nem ramo `elif escolha == '10'` no fluxo. A escolha cai no `else` e o programa responde "Operação inválida" para uma opção que aparece como válida.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `10` no menu.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Solicitar o ângulo em graus e exibir o seno.

**Resultado obtido:** Operação inválida. Tente novamente.

**Evidências (logs de erro):** `evidencias/bug-010-seno.log`

**Severidade:** Média

**Impacto:** Funcionalidade anunciada fica inacessível e a mensagem confunde o usuário.

**Sugestão de correção:** Implementar `seno(x)` e adicionar o ramo da opção 10 no fluxo.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-011: Entrada não numérica encerra o programa

**Localização do bug:** Calculadora.py, `calculadora_cientifica` (conversões `float(input(...))` e `int(input(...))`)

**Descrição clara do bug:** As conversões de entrada não são protegidas. Texto no lugar de número gera `ValueError` e o programa termina com traceback. O fatorial usa `int`, então um valor decimal como `3.5` também gera o mesmo erro.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `1` no menu.
4. Informar `abc` como primeiro número.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Mensagem pedindo um número válido, sem encerrar o programa.

**Resultado obtido:** `ValueError: could not convert string to float: 'abc'`.

**Evidências (logs de erro):** `evidencias/bug-011-entrada-invalida.log`

**Severidade:** Média

**Impacto:** Erro comum de digitação derruba a aplicação.

**Sugestão de correção:** Envolver as conversões em `try/except ValueError`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

## BUG-012: Potenciação sem tratamento de casos indefinidos

**Localização do bug:** Calculadora.py, função `potencia`

**Descrição clara do bug:** Casos como `0 ** -1` e base negativa com expoente fracionário (`(-8) ** 0.5`) não são validados. O NumPy emite `RuntimeWarning` e o programa exibe `inf` ou `nan` como se fossem resultados válidos, ao contrário da raiz quadrada, que trata o caso negativo.

**Contexto:** Python 3.14, NumPy 2.5.4, pytest 9.2.0, Windows, execução via terminal do VS Code com `py Calculadora.py`.

**Passo a passo para reproduzir:**

1. Abrir o terminal na pasta do projeto.
2. Executar `python Calculadora.py`.
3. Digitar `5` no menu.
4. Informar `0` como primeiro número.
5. Informar `-1` como segundo número.
6. Repetir com `-8` e `0.5`.

**Consistência:** Ocorre sempre.

**Resultado esperado:** Mensagem de erro para operação indefinida.

**Resultado obtido:** `RuntimeWarning` seguido de Resultado: inf (primeiro caso) e Resultado: nan (segundo caso).

**Evidências (logs de erro):** `evidencias/bug-012-potencia-zero.log e evidencias/bug-012-potencia-neg.log`

**Severidade:** Baixa

**Impacto:** Valores especiais de ponto flutuante são exibidos sem explicação.

**Sugestão de correção:** Validar os casos indefinidos antes de chamar `np.power`.

**Data de identificação:** 04/11/2026

**Status:** Não resolvido

---

