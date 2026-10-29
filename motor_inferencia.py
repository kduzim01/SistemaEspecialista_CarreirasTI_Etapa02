
import json
import operator
from pathlib import Path


CAMINHO_BASE = Path(__file__).resolve().parent / "regras_carreiras.json"

OPERADORES = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
}


def carregar_base_conhecimento():
    """Carrega a base externa de carreiras, pesos e regras."""
    with open(CAMINHO_BASE, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def validar_respostas(respostas, base):
    """Verifica se todas as perguntas foram respondidas de 1 a 5."""
    perguntas = {p["id"] for p in base["perguntas"]}

    recebidas = set(respostas)

    faltantes = perguntas - recebidas
    desconhecidas = recebidas - perguntas

    if faltantes:
        raise ValueError(
            f"Perguntas não respondidas: {sorted(faltantes)}"
        )

    if desconhecidas:
        raise ValueError(
            f"Perguntas desconhecidas: {sorted(desconhecidas)}"
        )

    for pergunta, valor in respostas.items():
        if type(valor) is not int or not 1 <= valor <= 5:
            raise ValueError(
                f"Resposta inválida para '{pergunta}': {valor}"
            )

    return True


def verificar_condicoes(regra, respostas):
    """Confere se todas as condições de uma regra são verdadeiras."""
    for condicao in regra["condicoes"]:
        pergunta = condicao["pergunta"]
        operador = condicao["operador"]
        referencia = condicao["valor"]

        funcao = OPERADORES[operador]

        if not funcao(respostas[pergunta], referencia):
            return False

    return True


def calcular_compatibilidade(respostas, pesos):
    """Calcula a compatibilidade ponderada entre 0% e 100%."""
    soma_pesos = sum(pesos.values())

    if soma_pesos <= 0:
        raise ValueError("A matriz de pesos não pode ser vazia ou nula.")

    pontuacao = sum(
        ((respostas[pergunta] - 1) / 4) * peso
        for pergunta, peso in pesos.items()
    )

    percentual = (pontuacao / soma_pesos) * 100

    return round(percentual, 2)


def aplicar_regras(trilha_id, respostas, regras):
    """Identifica regras acionadas e acumula ajustes percentuais."""
    ajuste_total = 0
    regras_acionadas = []

    for regra in regras:
        if regra["trilha"] != trilha_id:
            continue

        if verificar_condicoes(regra, respostas):
            ajuste = regra["ajuste_percentual"]
            ajuste_total += ajuste

            regras_acionadas.append({
                "id": regra["id"],
                "descricao": regra["descricao"],
                "tipo": regra["tipo"],
                "ajuste": ajuste,
            })

    return ajuste_total, regras_acionadas


def recomendar_carreiras(respostas):
    """Produz o ranking e as três carreiras mais compatíveis."""
    base = carregar_base_conhecimento()

    validar_respostas(respostas, base)

    resultados = []

    for trilha in base["trilhas"]:
        trilha_id = trilha["id"]
        pesos = base["pesos_afinidade"][trilha_id]

        percentual_base = calcular_compatibilidade(
            respostas, pesos
        )

        ajuste, regras_acionadas = aplicar_regras(
            trilha_id,
            respostas,
            base["regras"]
        )

        percentual_final = max(
            0,
            min(100, percentual_base + ajuste)
        )

        resultados.append({
            "id": trilha_id,
            "nome": trilha["nome"],
            "percentual_base": percentual_base,
            "ajuste_percentual": ajuste,
            "compatibilidade": round(percentual_final, 2),
            "regras_acionadas": regras_acionadas,
        })

    # Ordenação determinística.
    # Compatibilidade é o critério principal.
    # Em empate, compara a pontuação base e depois o nome.
    resultados.sort(
        key=lambda item: (
            -item["compatibilidade"],
            -item["percentual_base"],
            item["nome"],
        )
    )

    quantidade = base["configuracoes"].get(
        "quantidade_recomendacoes", 3
    )

    diferenca_top2 = None

    if len(resultados) > 1:
        diferenca_top2 = round(
            resultados[0]["compatibilidade"]
            - resultados[1]["compatibilidade"],
            2
        )

    empate_primeiro = (
        diferenca_top2 is not None
        and diferenca_top2 == 0
    )

    proximidade_primeiro = (
        diferenca_top2 is not None
        and 0 < diferenca_top2 <= 2.0
    )

    perfil_uniforme = len(set(respostas.values())) == 1

    return {
        "ranking_completo": resultados,
        "top3": resultados[:quantidade],
        "empate_primeiro": empate_primeiro,
        "diferenca_top2": diferenca_top2,
        "proximidade_primeiro": proximidade_primeiro,
        "perfil_uniforme": perfil_uniforme,
    }

def analisar_competencias(trilha_id, conhecimentos):
    """
    Compara conhecimentos declarados com os níveis Júnior.

    Conhecimentos não informados são classificados como
    não avaliados, nunca assumidos como nível zero.
    """
    base = carregar_base_conhecimento()

    competencias = base["competencias_junior"]

    if trilha_id not in competencias:
        raise ValueError(f"Carreira desconhecida: {trilha_id}")

    lista = competencias[trilha_id]

    ids_validos = {item["id"] for item in lista}
    desconhecidos = set(conhecimentos) - ids_validos

    if desconhecidos:
        raise ValueError(
            f"Competências desconhecidas: {sorted(desconhecidos)}"
        )

    lacunas = []
    atendidas = []
    nao_avaliadas = []

    for competencia in lista:
        identificador = competencia["id"]
        requerido = competencia["nivel_requerido"]

        if identificador not in conhecimentos:
            nao_avaliadas.append(competencia)
            continue

        atual = conhecimentos[identificador]

        if type(atual) is not int or not 0 <= atual <= 5:
            raise ValueError(
                f"Nível inválido para '{identificador}': {atual}"
            )

        diferenca = requerido - atual

        resultado = {
            "id": identificador,
            "nome": competencia["nome"],
            "nivel_atual": atual,
            "nivel_requerido": requerido,
            "lacuna": max(0, diferenca),
        }

        if diferenca > 0:
            lacunas.append(resultado)
        else:
            atendidas.append(resultado)

    return {
        "carreira": trilha_id,
        "lacunas": lacunas,
        "competencias_atendidas": atendidas,
        "nao_avaliadas": nao_avaliadas,
        "analise_completa": len(nao_avaliadas) == 0,
    }


def gerar_roadmap(trilha_id, conhecimentos, objetivo_profissional=None):
    """Seleciona etapas de estudo das competências com lacunas."""
    base = carregar_base_conhecimento()
    # Orientações personalizadas conforme o objetivo profissional.
    orientacoes_por_objetivo = {
        "Conquistar minha primeira oportunidade Júnior": [
            "Priorizar as competências necessárias para uma vaga Júnior.",
            "Desenvolver projetos práticos e publicá-los no GitHub com documentação.",
            "Preparar o portfólio e buscar oportunidades de entrada na carreira.",
        ],
        "Migrar para outra área de TI": [
            "Identificar conhecimentos da experiência anterior que podem ser aproveitados.",
            "Priorizar as lacunas técnicas da nova carreira.",
            "Desenvolver projetos que demonstrem competências na área de destino.",
        ],
        "Desenvolver competências para evoluir profissionalmente": [
            "Aprofundar as competências que ainda apresentam lacunas.",
            "Estudar tecnologias avançadas relacionadas à carreira.",
            "Considerar certificações e projetos de maior complexidade.",
        ],
    }

    analise = analisar_competencias(
        trilha_id,
        conhecimentos
    )

    lacunas_por_id = {
        item["id"]: item
        for item in analise["lacunas"]
    }

    etapas = []

    for etapa in base["roadmap_estudos"][trilha_id]:
        competencia_id = etapa["competencia_id"]

        if competencia_id not in lacunas_por_id:
            continue

        etapas.append({
            "competencia_id": competencia_id,
            "competencia": lacunas_por_id[competencia_id]["nome"],
            "ordem": etapa["ordem"],
            "conteudo": etapa["conteudo"],
            "pratica": etapa["pratica"],
            "lacuna": lacunas_por_id[competencia_id]["lacuna"],
        })

    etapas.sort(key=lambda item: item["ordem"])
    return {
        "carreira": trilha_id,
        "etapas": etapas,
        "analise_completa": analise["analise_completa"],
        "competencias_nao_avaliadas": [
            item["id"]
            for item in analise["nao_avaliadas"]
        ],
        "recomendacoes_complementares": base["recomendacoes_complementares"][trilha_id],
        "orientacoes_objetivo": orientacoes_por_objetivo.get(
            objetivo_profissional, []
        ),
    }
