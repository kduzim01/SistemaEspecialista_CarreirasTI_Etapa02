
import streamlit as st

from motor_inferencia import (
    carregar_base_conhecimento,
    recomendar_carreiras,
    analisar_competencias,
    gerar_roadmap,
)


st.set_page_config(
    page_title="Consultor Inteligente de Carreiras em TI",
    page_icon="🧭",
    layout="wide",
)


def formatar_percentual(valor):
    return f"{valor:.2f}%".replace(".", ",")


def formatar_nivel(valor):
    if valor is None:
        return "Não informado"

    descricoes = {
        0: "0 - Nenhum conhecimento",
        1: "1 - Conhecimento inicial",
        2: "2 - Conhecimento básico",
        3: "3 - Conhecimento intermediário",
        4: "4 - Conhecimento avançado",
        5: "5 - Domínio elevado",
    }

    return descricoes[valor]


base = carregar_base_conhecimento()

nomes_carreiras = {
    trilha["id"]: trilha["nome"]
    for trilha in base["trilhas"]
}

# Controle da etapa atual da navegação Wizard.
if "etapa_wizard" not in st.session_state:
    st.session_state["etapa_wizard"] = 1

# Armazena as afinidades independentemente dos sliders.
if "afinidades_wizard" not in st.session_state:
    st.session_state["afinidades_wizard"] = {}

# Armazena o objetivo profissional selecionado.
if "objetivo_profissional" not in st.session_state:
    st.session_state["objetivo_profissional"] = None

# Controla a navegação entre as quatro etapas do Wizard.
def mudar_etapa_wizard(nova_etapa):
    if 1 <= nova_etapa <= 4:
        st.session_state["etapa_wizard"] = nova_etapa


# Perguntas distribuídas entre as etapas do Wizard.
PERGUNTAS_WIZARD = {
    1: (
        "matematica",
        "raciocinio_logico",
    ),
    2: (
        "desenvolvimento_backend",
        "interfaces_ux",
        "analise_dados_ia",
        "engenharia_dados",
        "ciberseguranca",
        "devops_sre",
        "cloud_infraestrutura",
        "desenvolvimento_mobile",
        "qualidade_testes",
        "gestao_produtos",
    ),
}

# Seleciona as perguntas correspondentes à etapa atual.
def obter_perguntas_wizard(etapa):
    identificadores = set(PERGUNTAS_WIZARD.get(etapa, ()))

    return [
        pergunta
        for pergunta in base["perguntas"]
        if pergunta["id"] in identificadores
    ]


# --------------------------------------------------
# Apresentação
# --------------------------------------------------

st.title("🧭 Consultor Inteligente de Carreiras em TI")

st.write(
    "Descubra carreiras de Tecnologia da Informação "
    "compatíveis com seus interesses, identifique "
    "lacunas de competências e construa um roteiro "
    "personalizado de estudos."
)

st.caption(
    "As recomendações utilizam uma matriz acadêmica "
    "de afinidades e regras de inferência. "
    "Os percentuais não representam probabilidades "
    "de sucesso profissional."
)


# --------------------------------------------------
# Barra lateral
# --------------------------------------------------

with st.sidebar:
    st.header("Sobre o sistema")

    st.write(
        "Sistema especialista para orientação "
        "de carreiras em Tecnologia da Informação."
    )

    st.divider()

    st.subheader("Como utilizar")

    st.markdown(
        """
        1. Responda ao questionário de afinidades.
        2. Consulte as três carreiras recomendadas.
        3. Selecione uma carreira para avaliação.
        4. Informe seus conhecimentos atuais.
        5. Consulte as lacunas e o roadmap de estudos.
        """
    )

    st.divider()

    st.subheader("Base de conhecimento")

    st.write(f"Carreiras: {len(base['trilhas'])}")
    st.write(f"Perguntas: {len(base['perguntas'])}")
    st.write(f"Regras: {len(base['regras'])}")

    st.caption(
        "Os níveis de competência são referências "
        "acadêmicas propostas para o perfil Júnior."
    )


# --------------------------------------------------
# Questionário de afinidades
# --------------------------------------------------

st.divider()

# Indicador visual de progresso do Wizard.
etapa_atual = st.session_state["etapa_wizard"]

st.progress(
    etapa_atual / 4,
    text=f"Etapa {etapa_atual} de 4"
)

if etapa_atual == 1:
    st.header("1. Perfil pessoal")
elif etapa_atual == 2:
    st.header("2. Afinidades técnicas")



# Exibe as instruções de afinidade somente nas etapas 1 e 2.
if etapa_atual in (1, 2):
    st.write(
        "Avalie seu interesse em cada atividade, "
        "considerando a escala de 1 a 5."
    )

    st.info(
        "1 = Interesse muito baixo | "
        "2 = Baixo | 3 = Moderado | "
        "4 = Alto | 5 = Muito alto"
    )



enviar_afinidades = False
respostas = {}

if etapa_atual in (1, 2):
    with st.form("formulario_afinidades"):
        coluna_esquerda, coluna_direita = st.columns(2)

        for indice, pergunta in enumerate(obter_perguntas_wizard(etapa_atual)):
            coluna = coluna_esquerda if indice % 2 == 0 else coluna_direita

            with coluna:
                respostas[pergunta["id"]] = st.slider(
                    label=pergunta["texto"],
                    min_value=1,
                    max_value=5,
                    value=st.session_state["afinidades_wizard"].get(
                        pergunta["id"], 3
                    ),
                    step=1,
                    key=f"afinidade_{pergunta['id']}",
                )

        enviar_afinidades = st.form_submit_button(
            "Avançar para afinidades técnicas"
            if etapa_atual == 1
            else "Avançar para objetivos de carreira",
            type="primary",
            use_container_width=True,
        )


# --------------------------------------------------
# Processamento das recomendações
# --------------------------------------------------




if enviar_afinidades:
    st.session_state["afinidades_wizard"].update(respostas)

    if etapa_atual == 1:
        mudar_etapa_wizard(2)
        st.rerun()

    if etapa_atual == 2:
        mudar_etapa_wizard(3)
        st.rerun()
    try:
        # Verifica se todas as 12 afinidades foram informadas.
        ids_obrigatorios = {
            pergunta["id"] for pergunta in base["perguntas"]
        }

        if not ids_obrigatorios.issubset(
            st.session_state["afinidades_wizard"]
        ):
            raise ValueError(
                "Responda às 12 perguntas de afinidade antes "
                "de analisar seu perfil."
            )

        resultado = recomendar_carreiras(
            st.session_state["afinidades_wizard"]
        )

    except (ValueError, KeyError) as erro:
        st.error(
            f"Não foi possível analisar o perfil: {erro}"
        )

    else:
        st.session_state["resultado_carreiras"] = resultado

        # Uma nova entrevista invalida a avaliação anterior.
        st.session_state.pop(
            "avaliacao_competencias", None
        )


resultado = st.session_state.get("resultado_carreiras")

# Etapa 3 — Objetivos de carreira.
if st.session_state["etapa_wizard"] == 3:
    st.header("3. Objetivos de carreira")

    st.write(
        "Informe seu principal objetivo profissional "
        "para personalizar seu plano de desenvolvimento."
    )

    st.selectbox(
        "Qual é seu principal objetivo profissional?",
        options=[
            "Conquistar minha primeira oportunidade Júnior",
            "Migrar para outra área de TI",
            "Desenvolver competências para evoluir profissionalmente",
        ],
        placeholder="Selecione seu objetivo profissional",
        key="objetivo_profissional",
        persist_state="page",
    )

    # Conclui a entrevista e gera as recomendações.
    if st.button(
        "Gerar minhas recomendações",
        type="primary",
        use_container_width=True,
    ):
        if st.session_state["objetivo_profissional"] is None:
            st.warning("Selecione seu objetivo profissional antes de continuar.")
        else:
            try:
                ids_obrigatorios = {
                    pergunta["id"] for pergunta in base["perguntas"]
                }

                if not ids_obrigatorios.issubset(
                    st.session_state["afinidades_wizard"]
                ):
                    raise ValueError(
                        "Responda às 12 perguntas de afinidade antes de continuar."
                    )

                novo_resultado = recomendar_carreiras(
                    st.session_state["afinidades_wizard"]
                )

            except (ValueError, KeyError) as erro:
                st.error(f"Não foi possível gerar as recomendações: {erro}")
            else:
                st.session_state["resultado_carreiras"] = novo_resultado
                st.session_state.pop("avaliacao_competencias", None)
                mudar_etapa_wizard(4)
                st.rerun()


# --------------------------------------------------
# Resultados das recomendações
# --------------------------------------------------



if resultado is None or etapa_atual != 4:
    if etapa_atual == 4:
        st.info(
            "Ainda não há recomendações disponíveis. "
            "Conclua as etapas anteriores para gerar seu resultado."
        )
else:
    st.divider()

    st.header("4. Resultados — Carreiras recomendadas")

    st.write(
        "Confira as três carreiras com maior "
        "compatibilidade segundo suas respostas."
    )

    top3 = resultado["top3"]

    colunas = st.columns(len(top3))

    for indice, carreira in enumerate(top3):
        with colunas[indice]:
            with st.container(border=True):
                st.subheader(
                    f"{indice + 1}º lugar"
                )

                st.write(f"**{carreira['nome']}**")

                st.metric(
                    "Compatibilidade",
                    formatar_percentual(
                        carreira["compatibilidade"]
                    ),
                )

                st.caption(
                    "Pontuação base: "
                    + formatar_percentual(
                        carreira["percentual_base"]
                    )
                )

                st.caption(
                    "Ajuste das regras: "
                    f"{carreira['ajuste_percentual']:+} p.p."
                )


    # ----------------------------------------------
    # Empates e proximidade
    # ----------------------------------------------

    st.subheader("Interpretação do resultado")

    if resultado["perfil_uniforme"]:
        st.warning(
            "Todas as respostas apresentaram "
            "o mesmo nível de afinidade. "
            "Esse perfil não diferencia claramente "
            "os interesses entre as atividades."
        )

    if resultado["empate_primeiro"]:
        st.warning(
            "Foi identificado um empate entre "
            "as duas primeiras carreiras."
        )

    elif resultado["proximidade_primeiro"]:
        st.info(
            "As duas primeiras carreiras possuem "
            "pontuações muito próximas, com diferença "
            "de "
            + formatar_percentual(
                resultado["diferenca_top2"]
            )
            + " em pontos percentuais. "
            "Vale considerar ambas as opções."
        )

    else:
        st.success(
            "Não foi identificado empate exato "
            "nem proximidade de até dois pontos "
            "percentuais entre as primeiras carreiras."
        )


    # ----------------------------------------------
    # Ranking completo
    # ----------------------------------------------

    st.subheader("Ranking completo")

    for posicao, carreira in enumerate(
        resultado["ranking_completo"], start=1
    ):
        percentual = carreira["compatibilidade"]

        st.progress(
            percentual / 100,
            text=(
                f"{posicao}º — {carreira['nome']}: "
                f"{formatar_percentual(percentual)}"
            ),
        )


    # ----------------------------------------------
    # Explicação das regras acionadas
    # ----------------------------------------------

    st.subheader("Justificativas das recomendações")

    st.write(
        "As regras abaixo indicam as condições "
        "que influenciaram a pontuação final."
    )

    for carreira in top3:
        with st.expander(carreira["nome"]):
            st.write(
                "**Compatibilidade inicial:** "
                + formatar_percentual(
                    carreira["percentual_base"]
                )
            )

            st.write(
                "**Ajuste acumulado:** "
                f"{carreira['ajuste_percentual']:+} "
                "pontos percentuais"
            )

            regras_acionadas = carreira[
                "regras_acionadas"
            ]

            if regras_acionadas:
                for regra in regras_acionadas:
                    st.markdown(
                        f"**{regra['id']} — "
                        f"{regra['tipo'].capitalize()}**"
                    )

                    st.write(regra["descricao"])

                    st.caption(
                        f"Ajuste aplicado: "
                        f"{regra['ajuste']:+} p.p."
                    )

            else:
                st.write(
                    "Nenhuma regra adicional foi "
                    "acionada para esta carreira."
                )


    # ----------------------------------------------
    # Avaliação das competências Júnior
    # ----------------------------------------------

    st.divider()

    st.header("Avaliação de competências Júnior")

    st.write(
        "Selecione uma das carreiras recomendadas "
        "e informe seu nível atual de conhecimento."
    )

    ids_top3 = [
        carreira["id"]
        for carreira in top3
    ]

    carreira_selecionada = st.selectbox(
        "Carreira para avaliação",
        options=ids_top3,
        format_func=lambda identificador: (
            nomes_carreiras[identificador]
        ),
    )

    competencias = base["competencias_junior"][
        carreira_selecionada
    ]

    with st.form(
        f"formulario_competencias_{carreira_selecionada}"
    ):
        conhecimentos = {}

        for competencia in competencias:
            nivel = st.selectbox(
                label=(
                    f"{competencia['nome']} "
                    f"(referência Júnior: "
                    f"{competencia['nivel_requerido']})"
                ),
                options=[None, 0, 1, 2, 3, 4, 5],
                format_func=formatar_nivel,
                key=(
                    f"conhecimento_"
                    f"{carreira_selecionada}_"
                    f"{competencia['id']}"
                ),
            )

            if nivel is not None:
                conhecimentos[competencia["id"]] = nivel

        enviar_competencias = st.form_submit_button(
            "Identificar lacunas e gerar roadmap",
            type="primary",
            use_container_width=True,
        )


    # ----------------------------------------------
    # Processamento das competências
    # ----------------------------------------------

    if enviar_competencias:
        try:
            analise = analisar_competencias(
                carreira_selecionada,
                conhecimentos,
            )

            roadmap = gerar_roadmap(
            carreira_selecionada,
            conhecimentos,
            st.session_state.get("objetivo_profissional"),
            )

        except (ValueError, KeyError) as erro:
            st.error(
                f"Erro ao avaliar competências: {erro}"
            )

        else:
            st.session_state[
                "avaliacao_competencias"
            ] = {
                "carreira_id": carreira_selecionada,
                "analise": analise,
                "roadmap": roadmap,
            }


    # ----------------------------------------------
    # Resultados da avaliação de competências
    # ----------------------------------------------

    avaliacao = st.session_state.get(
        "avaliacao_competencias"
    )

    if (
        avaliacao is not None
        and avaliacao["carreira_id"]
        == carreira_selecionada
    ):
        analise = avaliacao["analise"]
        roadmap = avaliacao["roadmap"]

        st.divider()

        st.header("Resultado da avaliação de competências")

        coluna1, coluna2, coluna3 = st.columns(3)

        coluna1.metric(
            "Competências atendidas",
            len(analise["competencias_atendidas"]),
        )

        coluna2.metric(
            "Lacunas identificadas",
            len(analise["lacunas"]),
        )

        coluna3.metric(
            "Não avaliadas",
            len(analise["nao_avaliadas"]),
        )

        if not analise["analise_completa"]:
            st.warning(
                "A avaliação está incompleta. "
                "As competências não informadas "
                "não serão consideradas lacunas."
            )

        st.subheader("Lacunas de competências")

        if analise["lacunas"]:
            for competencia in analise["lacunas"]:
                with st.container(border=True):
                    st.write(
                        f"**{competencia['nome']}**"
                    )

                    st.write(
                        f"Nível atual: "
                        f"{competencia['nivel_atual']} | "
                        f"Nível requerido: "
                        f"{competencia['nivel_requerido']}"
                    )

                    st.caption(
                        f"Defasagem: "
                        f"{competencia['lacuna']} "
                        "nível(is)"
                    )

        else:
            if not analise["competencias_atendidas"]:
                st.info(
                    "Nenhuma competência foi avaliada. "
                    "Informe seus conhecimentos para "
                    "identificar possíveis lacunas."
                )
            else:
                st.success(
                    "Nenhuma lacuna foi identificada "
                    "entre as competências avaliadas."
                )


        # ------------------------------------------
        # Roadmap personalizado
        # ------------------------------------------

        st.divider()

        st.header("Roadmap personalizado")

        if roadmap["etapas"]:
            st.write(
                "As etapas abaixo correspondem "
                "às competências que apresentam "
                "lacunas de conhecimento."
            )

            for etapa in roadmap["etapas"]:
                with st.container(border=True):
                    st.subheader(
                        f"Etapa {etapa['ordem']} — "
                        f"{etapa['competencia']}"
                    )

                    st.write("**Conteúdo de estudo**")
                    st.write(etapa["conteudo"])

                    st.write("**Atividade prática**")
                    st.write(etapa["pratica"])

                    st.caption(
                        f"Lacuna identificada: "
                        f"{etapa['lacuna']} "
                        "nível(is)"
                    )

        else:
            st.info(
                "Nenhuma etapa de estudo foi gerada "
                "para as competências informadas."
            )

        # Tecnologias recomendadas para a carreira selecionada.
        recomendacoes = roadmap.get("recomendacoes_complementares", {})

        if recomendacoes.get("tecnologias"):
            st.subheader("Tecnologias recomendadas")

            for tecnologia in recomendacoes["tecnologias"]:
                st.write(f"- {tecnologia}")

        # Certificações recomendadas para a carreira selecionada.
        if recomendacoes.get("certificacoes"):
            st.subheader("Certificações recomendadas")

            st.caption(
                "Sugestões de formação e certificação. "
                "Não são requisitos obrigatórios para iniciar na carreira."
            )

            for certificacao in recomendacoes["certificacoes"]:
                st.write(f"- {certificacao}")

        # Projetos recomendados para o portfólio no GitHub.
        if recomendacoes.get("projetos_github"):
            st.subheader("Projetos para portfólio no GitHub")

            st.caption(
                "Sugestões de projetos práticos para demonstrar "
                "competências e construir um portfólio profissional."
            )

            for projeto in recomendacoes["projetos_github"]:
                st.write(f"- {projeto}")

        # Orientações conforme o objetivo profissional do usuário.
        if roadmap.get("orientacoes_objetivo"):
            st.subheader("Orientações para seu objetivo profissional")

            st.write(
                f"**Objetivo selecionado:** "
                f"{st.session_state.get('objetivo_profissional')}"
            )

            for orientacao in roadmap["orientacoes_objetivo"]:
                st.write(f"- {orientacao}")




st.divider()

st.caption(
    "Consultor Inteligente de Carreiras em TI | "
    "Sistema especialista acadêmico baseado em regras."
)
