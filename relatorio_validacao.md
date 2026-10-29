
# Relatório de Validação — Consultor Inteligente de Carreiras em TI

## 1. Objetivo

Verificar o funcionamento do Sistema Especialista Consultor Inteligente de Carreiras em TI, considerando a integração entre a base de conhecimento JSON, o motor de inferência em Python e a interface Streamlit.

## 2. Ambiente de desenvolvimento

- Linguagem: Python 3.12
- Interface: Streamlit 1.66.1
- Testes automatizados: unittest
- Ambiente: Windows, Visual Studio Code e PowerShell
- Controle de versão: Git e GitHub

## 3. Componentes avaliados

O sistema contém:

- 10 carreiras de Tecnologia da Informação.
- 12 perguntas de afinidade.
- 120 pesos de correlação.
- 20 regras de bonificação e penalidade.
- 40 competências de referência para o nível Júnior.
- 40 etapas de roadmap.
- Motor de compatibilidade ponderada.
- Recomendações Top 3 e ranking completo.
- Identificação de lacunas de competências.

## 4. Testes automatizados

Foram executados os arquivos `test_motor.py` e `test_integracao.py` utilizando o comando:

    python -m unittest -v test_motor.py test_integracao.py

Resultado obtido:

    Ran 18 tests in 0.042s

    OK

Os 18 métodos de teste foram aprovados, sem erros ou falhas.

### 4.1. Motor de inferência

Foram aprovados 12 testes automatizados, contemplando carregamento da base, cálculos de compatibilidade, validação de entradas, acionamento de regras, aplicação de ajustes, classificação das carreiras, identificação de lacunas e geração de roadmaps.

### 4.2. Validação integrada

Foram aprovados 6 testes adicionais, contemplando:

1. Recomendações para dez personas simuladas.
2. Empates e perfis uniformes.
3. Lacunas de competências nas dez carreiras.
4. Avaliações parcialmente preenchidas.
5. Competências que atendem aos níveis de referência.
6. Justificativas relacionadas às regras acionadas.

As dez personas simuladas apresentaram a carreira esperada na primeira posição do ranking.

## 5. Validação funcional da interface

A interface Streamlit foi avaliada manualmente por meio de diferentes cenários.

| Cenário | Resultado | Situação |
|---|---|---|
| Questionário com 12 afinidades | Recomendações Top 3 exibidas | Aprovado |
| Perfil com respostas uniformes | Empate e perfil uniforme identificados | Aprovado |
| Quatro competências no nível zero | 4 lacunas identificadas | Aprovado |
| Avaliação parcial | 1 atendida, 2 lacunas, 1 não avaliada | Aprovado |
| Nenhuma competência informada | Mensagem informativa exibida | Aprovado |
| Quatro competências atendidas | Nenhuma lacuna identificada | Aprovado |
| Roadmap com duas lacunas | Etapas 2 e 4 selecionadas | Aprovado |

Os resultados observados foram coerentes com a lógica definida no motor de inferência.

## 6. Ajustes realizados

Durante o desenvolvimento e os testes, foram realizados os seguintes ajustes:

- Refinamento do peso de interfaces e experiência do usuário para a carreira Mobile.
- Inclusão de indicadores de empate, proximidade e perfil uniforme.
- Correção da indentação de um bloco condicional na interface.
- Diferenciação das mensagens para avaliações incompletas e competências atendidas.

Esses ajustes foram verificados nos cenários de teste correspondentes.

## 7. Limitações

As recomendações são produzidas por uma matriz acadêmica de afinidades e regras previamente definidas.

Os percentuais representam compatibilidade segundo essa modelagem, não probabilidades de sucesso profissional.

As personas são simuladas, e os testes automatizados não constituem uma validação com usuários reais.

A interface foi testada manualmente; não foi implementada uma suíte automatizada de testes de navegador.

## 8. Conclusão

O sistema apresentou funcionamento satisfatório nos cenários avaliados.

Os 18 testes automatizados foram aprovados, as dez personas simuladas produziram os resultados esperados e os principais fluxos da interface Streamlit foram validados manualmente.

Os resultados demonstram consistência funcional dentro dos critérios e cenários definidos para a atividade acadêmica.
