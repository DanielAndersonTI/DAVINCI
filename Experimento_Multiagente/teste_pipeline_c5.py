"""Execução da configuração C5 (ablação do Agente 3 sobre candidatos congelados).

O C5 não gera propostas. Para cada sistema de cada rodada, ele relê as Propostas
A e B gravadas por uma execução anterior da C1 e roda o Agente 3 duas vezes
sobre exatamente os mesmos textos — uma com o placar de Precision/Recall/F1 das
propostas (o Agente 3 da C1) e uma sem (a variante que decide pelos requisitos).
A diferença entre os braços isola o efeito do placar.

Onde os candidatos são encontrados
----------------------------------
Nada é passado à mão. Para cada rodada o script lê o JSON agregado de metadados
da execução C1 (`execuion-metadados-C1-Gemini-FS<n>.json`), que traz o
`execution_id` de cada um dos 8 sistemas, e monta o caminho
`result/<sistema>/result_generalized_fewshot/run_<execution_id>/`. O pareamento
com a C1 fica ancorado na proveniência real das execuções, e não em uma lista de
caminhos que pode envelhecer.

As pastas do `result/` não seguem uma grafia única (`cargo tracker` e
`cargo-tracker`, `petclinic` e `pet-clinic`), então a busca casa os nomes por
chave normalizada e confirma o candidato pela existência do run dir esperado —
nunca por adivinhação.

Escopo: só o Gemini — é o único modelo em que os contrastes de consolidação
foram significativos no estudo.

Saída: `result/<sistema>/c5_fewshot/run_<timestamp>/`, com os dois braços, o
registro de fallback de cada um e o tracer da execução (que conta apenas as
chamadas do Agente 3).
"""

import json
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(REPO_ROOT))

import main_fewshot  # noqa: E402
from main_fewshot import executar_pipeline_c5  # noqa: E402

try:
    from Interface.utils.parsers import (  # noqa: E402
        parse_reference_interactions,
        parse_reference_services,
    )
except ModuleNotFoundError:  # pragma: no cover
    from utils.parsers import (  # type: ignore
        parse_reference_interactions,
        parse_reference_services,
    )

# As execuções da C1 (candidatos congelados) e a saída do C5 ficam no result/ da
# raiz do repositório — o mesmo lugar de onde as rodadas originais foram feitas.
RESULTS_ROOT = REPO_ROOT / "result"
ENTRADAS_ROOT = ROOT / "Dates" / "davinci_inputs"

# Garante que o C5 grave ao lado das execuções da C1, sem depender do diretório
# de trabalho de onde o script for chamado.
main_fewshot.RESULTS_ROOT = RESULTS_ROOT


# ---------------------------------------------------------------------------
# Chaveamento: comente com "#" as rodadas que não for usar.
# ---------------------------------------------------------------------------
# (número da rodada, run id da execução C1 correspondente — o mesmo que aparece
# no cabeçalho dos PDFs em Report-and-Dates/Gemini/C1/).
RODADAS = [
    (1, "20260902_234520_573591"),  # Test-1
    (2, "20260903_165838_818171"),  # Test-2
    (3, "20260903_171617_538480"),  # Test-3
]
# RODADAS = [(2, "20260903_165838_818171")]  # rodada isolada, para conferência

# True apenas resolve e imprime o plano, sem chamar o LLM.
SOMENTE_VERIFICAR = False


def _chave(nome: str) -> str:
    """Chave de comparação insensível a caixa, espaços, hífens e underscores."""
    return re.sub(r"[^a-z0-9]", "", str(nome).lower())


def _metadados_da_rodada(numero: int) -> Path:
    """Localiza o JSON agregado de metadados da rodada.

    O diretório do tracer não segue um nome único (o do Test-1 está truncado),
    então a busca é pelo nome do arquivo, que é consistente entre as rodadas.
    """
    arquivo = f"execuion-metadados-C1-Gemini-FS{numero}.json"
    achados = sorted(RESULTS_ROOT.glob(f"results-tracer-*/{arquivo}"))
    if not achados:
        raise FileNotFoundError(f"Nenhum metadado da rodada {numero} em {RESULTS_ROOT} ({arquivo}).")
    if len(achados) > 1:
        print(f"  ⚠ {len(achados)} metadados para a rodada {numero}; usando {achados[0]}")
    return achados[0]


def _execution_ids(numero: int) -> dict:
    """Devolve {nome do sistema -> execution_id} da rodada."""
    itens = json.loads(_metadados_da_rodada(numero).read_text(encoding="utf-8"))
    return {item["system"]: item["execution_id"] for item in itens}


def _run_dir_congelado(system_name: str, execution_id: str) -> Path:
    """Resolve o run dir da C1 daquele sistema, confirmando pelo execution_id."""
    alvo = f"run_{execution_id}"
    candidatos = [
        pasta for pasta in RESULTS_ROOT.iterdir()
        if pasta.is_dir() and _chave(pasta.name) == _chave(system_name)
    ]
    for pasta in candidatos:
        run_dir = pasta / "result_generalized_fewshot" / alvo
        if (run_dir / "proposta_a.csv").exists() and (run_dir / "proposta_b.csv").exists():
            return run_dir
    raise FileNotFoundError(
        f"Sem candidatos congelados para '{system_name}' ({alvo}) em {RESULTS_ROOT}."
    )


def _pasta_entradas(system_name: str) -> Path:
    """Localiza a pasta de entradas do sistema sem depender da grafia do nome."""
    for pasta in ENTRADAS_ROOT.iterdir():
        if pasta.is_dir() and _chave(pasta.name) == _chave(system_name):
            return pasta
    raise FileNotFoundError(f"Sem entradas em {ENTRADAS_ROOT} para '{system_name}'.")


def _carregar_entradas(system_name: str) -> tuple:
    pasta = _pasta_entradas(system_name)
    requirements = (pasta / "requirements.txt").read_text(encoding="utf-8")
    reference_services = parse_reference_services(
        (pasta / "reference_services.txt").read_text(encoding="utf-8")
    )
    interaction_reference = parse_reference_interactions(
        (pasta / "reference_interactions.txt").read_text(encoding="utf-8")
    )
    return requirements, reference_services, interaction_reference


def _planejar_rodada(numero: int) -> list:
    """Monta o plano da rodada: um caso por sistema, com tudo já resolvido."""
    plano = []
    for system_name, execution_id in _execution_ids(numero).items():
        plano.append({
            "system": system_name,
            "execution_id": execution_id,
            "frozen_run_dir": _run_dir_congelado(system_name, execution_id),
        })
    return sorted(plano, key=lambda caso: caso["system"].lower())


def executar_rodada(numero: int, run_id_c1: str) -> list:
    """Roda o C5 sobre os 8 sistemas de uma rodada da C1.

    Um único run id novo é gerado para a rodada inteira e compartilhado pelos 8
    sistemas, como na C1 — mas novo, para não sobrescrever o tracer original.
    """
    plano = _planejar_rodada(numero)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    print("\n" + "=" * 74)
    print(f"RODADA Test-{numero} — candidatos congelados da C1 {run_id_c1}")
    print(f"Tracer desta execução: results-tracer-{run_id}")
    print(f"Sistemas: {len(plano)}")
    print("=" * 74)

    if SOMENTE_VERIFICAR:
        for caso in plano:
            print(f"  {caso['system']:<16} {caso['execution_id']}  {caso['frozen_run_dir']}")
        return []

    resultados = []
    for indice, caso in enumerate(plano, start=1):
        system_name = caso["system"]
        print(f"\n[{indice}/{len(plano)}] {system_name}")
        try:
            requirements, reference_services, interaction_reference = _carregar_entradas(system_name)
            print(f"  Candidatos congelados: {caso['frozen_run_dir']}")

            _, metricas = executar_pipeline_c5(
                system_name,
                requirements,
                reference_services,
                interaction_reference,
                frozen_run_dir=caso["frozen_run_dir"],
                tracer_run_id=run_id,
            )

            sem_placar = metricas.get("consolidada_inter") or {}
            com_placar = metricas.get("consolidada_com_placar_inter") or {}
            resultados.append({
                "system": system_name,
                "ok": True,
                "f1_sem_placar": sem_placar.get("f1_score"),
                "f1_com_placar": com_placar.get("f1_score"),
            })
            print(
                f"  Interações F1 — sem placar: {sem_placar.get('f1_score')} | "
                f"com placar: {com_placar.get('f1_score')}"
            )
        except Exception as erro:
            print(f"  ✗ Falhou: {type(erro).__name__}: {erro}")
            traceback.print_exc()
            resultados.append({"system": system_name, "ok": False, "erro": str(erro)})

    return resultados


def main() -> None:
    if not RODADAS:
        print("Nenhuma rodada ativa em RODADAS.")
        return

    print("Execução C5 — ablação do Agente 3 (Gemini)")
    print(f"Rodadas ativas: {len(RODADAS)} | Sistemas por rodada: 8")
    print(f"Chamadas de Agente 3 previstas: {len(RODADAS) * 8 * 2}")

    todos = []
    for numero, run_id_c1 in RODADAS:
        try:
            todos.extend(executar_rodada(numero, run_id_c1))
        except Exception as erro:
            print(f"\n✗ Rodada Test-{numero} interrompida: {type(erro).__name__}: {erro}")
            traceback.print_exc()

    if SOMENTE_VERIFICAR:
        print("\nSOMENTE_VERIFICAR = True: plano impresso, nenhuma chamada feita.")
        return

    ok = [r for r in todos if r.get("ok")]
    print("\n" + "=" * 74)
    print(f"CONCLUÍDO — {len(ok)}/{len(todos)} casos")
    print("=" * 74)
    for r in todos:
        if r.get("ok"):
            print(f"  {r['system']:<16} F1 interações  sem placar: {r['f1_sem_placar']}  com placar: {r['f1_com_placar']}")
        else:
            print(f"  {r['system']:<16} FALHOU: {r.get('erro')}")


if __name__ == "__main__":
    main()
