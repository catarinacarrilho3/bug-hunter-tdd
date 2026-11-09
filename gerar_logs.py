"""Gera de novo os logs da pasta evidencias, rodando a calculadora ORIGINAL
na máquina de quem executa"""
import os
import pathlib
import re
import subprocess
import sys
import tempfile

PASTA = pathlib.Path("evidencias")
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}
PY = sys.executable


def git(*args, binario=False):
    r = subprocess.run(["git", *args], capture_output=True, check=True)
    return r.stdout if binario else r.stdout.decode("utf-8").strip()


def rodar(cmd, cwd, entrada=""):
    r = subprocess.run(cmd, cwd=cwd, input=entrada, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=ENV)
    # stdout e stderr juntos, tirando o caminho da pasta temporária
    saida = (r.stdout or "") + (r.stderr or "")
    return saida.replace(str(cwd) + os.sep, "").replace("\r\n", "\n")


def limpar_pytest(txt):
    return "\n".join(l for l in txt.split("\n")
                     if not re.match(r"(platform|rootdir|cachedir|plugins)", l))


def salvar(nome, cabecalho, corpo):
    PASTA.mkdir(exist_ok=True)
    (PASTA / nome).write_text(cabecalho + corpo.rstrip("\n") + "\n", encoding="utf-8")
    print("gerado:", nome)


def pasta_de(commit):
    """Cria uma pasta temporária com os arquivos do projeto naquele commit."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    for arq in ("Calculadora.py", "test_calculadora.py"):
        try:
            (tmp / arq).write_bytes(git("show", f"{commit}:{arq}", binario=True))
        except subprocess.CalledProcessError:
            pass
    return tmp


raiz = git("rev-list", "--max-parents=0", "HEAD").split()[0]
original = pasta_de(raiz)
# o teste do HEAD serve para mostrar o erro de import do BUG-001
(original / "test_calculadora.py").write_bytes(pathlib.Path("test_calculadora.py").read_bytes())

CASOS = {
    "bug-002-adicao": "1\n2\n3\nn\n",
    "bug-003-divisao": "4\n10\n0\nn\n",
    "bug-004-fatorial": "7\n5\nn\n",
    "bug-005-fatorial-negativo": "7\n-3\nn\n",
    "bug-006-ln": "8\n2.718\nn\n",
    "bug-007-log10": "9\n100\nn\n",
    "bug-008-log10-zero": "9\n0\nn\n",
    "bug-009-cosseno": "11\n60\nn\n",
    "bug-009-tangente": "12\n45\nn\n",
    "bug-010-seno": "10\nn\n",
    "bug-011-entrada-invalida": "1\nabc\n",
    "bug-012-potencia-zero": "5\n0\n-1\nn\n",
    "bug-012-potencia-neg": "5\n-8\n0.5\nn\n",
}
for nome, entrada in CASOS.items():
    ent = " | ".join(entrada.strip().split("\n"))
    cab = f"# Entradas digitadas (em ordem): {ent}\n$ py Calculadora.py\n"
    salvar(nome + ".log", cab, rodar([PY, "-u", "Calculadora.py"], original, entrada))

salvar("bug-001-import.log", '$ py -c "import Calculadora"\n',
       rodar([PY, "-u", "-c", "import Calculadora"], original, ""))
salvar("bug-001-pytest.log",
       "$ py -m pytest -q   # Calculadora.py original, sem proteção __main__\n",
       limpar_pytest(rodar([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider"], original)))

# fases do TDD, a partir dos commits do histórico
def achar(trecho):
    for linha in git("log", "--format=%H %s").split("\n"):
        if trecho in linha:
            return linha.split()[0]
    return None

for nome, trecho in (("tdd-1-red", "(Red)"), ("tdd-2-green", "(Green)")):
    c = achar(trecho)
    if c:
        salvar(nome + ".log", "$ py -m pytest -v\n",
               limpar_pytest(rodar([PY, "-m", "pytest", "-v", "-p", "no:cacheprovider"], pasta_de(c))))
    else:
        print("não achei o commit", trecho, "-> mantive o log antigo de", nome)

salvar("tdd-3-final.log", "$ py -m pytest -v\n",
       limpar_pytest(rodar([PY, "-m", "pytest", "-v", "-p", "no:cacheprovider"], pathlib.Path.cwd())))
print("\nPronto. Confira os arquivos em evidencias/ e depois apague este script.")
