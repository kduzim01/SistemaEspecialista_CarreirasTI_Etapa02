# Consultor Inteligente de Carreiras em TI

Sistema Especialista desenvolvido em Python, com interface Streamlit, para auxiliar na identificação de carreiras em Tecnologia da Informação compatíveis com os interesses do usuário.

A aplicação utiliza uma base de conhecimento estruturada em JSON, uma matriz ponderada de afinidades e regras de inferência para apresentar recomendações profissionais, identificar lacunas de competências e gerar roteiros personalizados de estudos.

## 1. Objetivo

O objetivo do sistema é oferecer apoio à orientação de carreiras em Tecnologia da Informação por meio da análise de interesses e conhecimentos.

A aplicação permite que o usuário:

- Identifique carreiras compatíveis com suas afinidades.
- Consulte as três principais recomendações.
- Compreenda os critérios utilizados nas recomendações.
- Avalie seus conhecimentos em competências de referência para o nível Júnior.
- Identifique competências que precisam ser desenvolvidas.
- Consulte um roadmap personalizado de estudos.

O sistema possui finalidade acadêmica e não substitui a orientação profissional especializada.

## 2. Funcionalidades

### Questionário de afinidades


O questionário utiliza um Wizard organizado em quatro etapas:

1. **Perfil pessoal:** duas perguntas sobre matemática, estatística e raciocínio lógico.
2. **Afinidades técnicas:** dez perguntas relacionadas às diferentes áreas de Tecnologia da Informação.
3. **Objetivos de carreira:** seleção do objetivo profissional, utilizado na personalização do roadmap.
4. **Resultados:** apresentação das três carreiras mais compatíveis, avaliação de competências Júnior e roadmap personalizado.

Ao todo, o usuário responde a 12 perguntas de afinidade nas duas primeiras etapas.

As respostas utilizam uma escala de 1 a 5:

| Nível | Significado |
|---|---|
| 1 | Interesse muito baixo |
| 2 | Interesse baixo |
| 3 | Interesse moderado |
| 4 | Interesse alto |
| 5 | Interesse muito alto |

### Recomendações de carreiras

O sistema avalia dez possibilidades profissionais:

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end e UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança
6. DevOps e SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Qualidade de Software (QA)
10. Gestão de Produtos

A classificação utiliza os pesos definidos na base de conhecimento e os ajustes provenientes das regras de inferência.

O resultado apresenta:

- Ranking completo das dez carreiras.
- Três carreiras mais compatíveis (Top 3).
- Percentuais de compatibilidade.
- Pontuações anteriores aos ajustes.
- Bonificações e penalidades aplicadas.
- Justificativas das regras acionadas.

### Interpretação das recomendações

O sistema também identifica:

- Empates exatos entre as primeiras carreiras.
- Proximidade de até dois pontos percentuais entre as primeiras posições.
- Perfis uniformes, nos quais todas as afinidades recebem o mesmo valor.

A proximidade é uma heurística definida para o projeto e não representa uma medida estatística de incerteza.

### Avaliação de competências Júnior

Após receber as recomendações, o usuário pode selecionar uma das três carreiras apresentadas e informar seus conhecimentos atuais.

Cada carreira possui quatro competências com níveis de referência definidos na base de conhecimento.

A avaliação permite identificar:

- Competências atendidas.
- Competências com lacunas.
- Competências não avaliadas.

Os conhecimentos podem ser informados em níveis de 0 a 5. Uma competência não informada não é automaticamente considerada uma lacuna.

### Roadmap personalizado

A partir das competências que apresentam lacunas, o sistema organiza um roteiro de estudos contendo:

- Ordem das etapas.
- Competência a desenvolver.
- Conteúdo teórico sugerido.
- Atividade prática.
- Diferença entre o nível atual e o nível de referência.


Além das etapas de estudo baseadas nas lacunas identificadas, o sistema apresenta recomendações complementares para cada uma das dez carreiras, incluindo:

- **Tecnologias recomendadas:** linguagens, ferramentas e plataformas relacionadas à carreira selecionada.
- **Certificações recomendadas:** sugestões de formação e aprofundamento profissional, sem caráter obrigatório.
- **Projetos para portfólio no GitHub:** atividades práticas que permitem demonstrar competências técnicas e documentar experiências.

O roadmap também considera o objetivo profissional selecionado na terceira etapa do Wizard, apresentando orientações específicas para:

- Conquistar a primeira oportunidade Júnior.
- Migrar para outra área de Tecnologia da Informação.
- Desenvolver competências para evoluir profissionalmente.

As recomendações complementares são apresentadas mesmo quando nenhuma lacuna é identificada. O objetivo profissional personaliza as orientações de desenvolvimento, sem modificar os percentuais de compatibilidade ou o ranking das carreiras.

## 3. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Implementação do sistema |
| Streamlit 1.66.1 | Interface web interativa |
| JSON | Armazenamento da base de conhecimento |
| unittest | Testes automatizados |
| Git | Controle de versão |
| GitHub | Hospedagem do repositório |

O motor de inferência é implementado em Python e interpreta as regras declaradas na base JSON.

## 4. Estrutura do projeto

```text
SistemaEspecialista_CarreirasTI_Etapa02/
|
|-- app.py
|-- motor_inferencia.py
|-- regras_carreiras.json
|-- test_motor.py
|-- test_integracao.py
|-- relatorio_validacao.md
|-- requirements.txt
|-- README.md
|-- .gitignore
```

### Descrição dos arquivos

**app.py**

Implementa a interface Streamlit, incluindo questionário, recomendações, ranking, avaliação de competências e apresentação do roadmap.

**motor_inferencia.py**

Implementa o processamento das respostas, o cálculo das compatibilidades, a aplicação das regras, a classificação das carreiras, a análise das competências e a geração dos roadmaps.

**regras_carreiras.json**

Armazena a base de conhecimento, incluindo carreiras, perguntas, pesos de afinidade, regras de inferência, competências Júnior e roteiros de estudo.

**test_motor.py**

Contém testes automatizados das funcionalidades do motor de inferência.

**test_integracao.py**

Contém testes que verificam o funcionamento conjunto da base de conhecimento e do motor, incluindo personas, rankings, regras, competências e roadmaps.

**relatorio_validacao.md**

Registra os procedimentos, os resultados e as limitações dos testes realizados.

**requirements.txt**

Registra a dependência externa necessária para executar a interface.

## 5. Requisitos

Para executar o sistema, recomenda-se:

- Python 3.12 instalado.
- Acesso ao terminal.
- Navegador web atualizado.
- Git, caso seja necessário clonar o repositório.

Os comandos abaixo utilizam o PowerShell no Windows.

## 6. Instalação

### 6.1. Clonar o repositório

```powershell
git clone https://github.com/kduzim01/SistemaEspecialista_CarreirasTI_Etapa02.git
```

Acessar a pasta do projeto:

```powershell
cd SistemaEspecialista_CarreirasTI_Etapa02
```

### 6.2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 6.3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação devido à política de execução, poderá ser necessário permitir scripts somente na sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois, executar novamente o comando de ativação.

### 6.4. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
```

A dependência principal registrada é:

```text
streamlit==1.66.1
```

## 7. Executar a aplicação

Na raiz do projeto, com o ambiente virtual ativado, execute:

```powershell
python -m streamlit run app.py
```

Após iniciar o servidor, a aplicação poderá ser acessada pelo navegador no endereço local:

http://localhost:8501

O terminal deverá permanecer executando enquanto a aplicação estiver em uso.

Para encerrar o servidor, pressione `Ctrl + C`.

## 8. Como utilizar

1. Acesse a aplicação pelo navegador.
2. Responda às 12 perguntas de afinidade.
3. Clique em **Analisar meu perfil**.
4. Consulte as três recomendações e o ranking completo.
5. Verifique as justificativas e os indicadores de interpretação.
6. Selecione uma carreira para avaliar suas competências.
7. Informe seus níveis atuais de conhecimento.
8. Clique em **Identificar lacunas e gerar roadmap**.
9. Consulte as competências atendidas, as lacunas e as sugestões de estudo.

Uma nova análise de afinidades invalida a avaliação de competências anterior, permitindo que o usuário realize outra entrevista.

## 9. Base de conhecimento e inferência

A base de conhecimento é organizada em JSON e possui:

| Elemento | Quantidade |
|---|---:|
| Carreiras | 10 |
| Perguntas de afinidade | 12 |
| Pesos de correlação | 120 |
| Regras de inferência | 20 |
| Competências Júnior | 40 |
| Etapas de roadmap cadastradas | 40 |

### Cálculo das recomendações

O motor considera as respostas fornecidas pelo usuário e os pesos atribuídos a cada carreira.

A compatibilidade inicial é obtida por um cálculo ponderado, normalizado para a escala percentual utilizada pelo sistema.

Em seguida, são verificadas as condições das regras cadastradas.

Quando uma regra é satisfeita, pode ser aplicada uma bonificação ou penalidade, conforme sua configuração.

Após os ajustes, as carreiras são ordenadas e apresentadas no ranking.

### Justificativas

O sistema mantém o registro das regras acionadas e apresenta suas descrições ao usuário.

Essa abordagem permite compreender quais critérios influenciaram a recomendação final.

## 10. Testes automatizados

O projeto utiliza a biblioteca `unittest` para verificar o funcionamento do motor e sua integração com a base de conhecimento.

Para executar todos os testes:

```powershell
python -m unittest -v test_motor.py test_integracao.py
```

### Testes do motor

O arquivo `test_motor.py` contém 12 métodos de teste, incluindo verificações de:

- Carregamento da base de conhecimento.
- Cálculos de compatibilidade.
- Validação de respostas.
- Aplicação de bonificações e penalidades.
- Ordenação e geração do Top 3.
- Limites percentuais.
- Identificação de lacunas.
- Geração de roadmaps.
- Empates, proximidade e perfis uniformes.

### Testes de integração

O arquivo `test_integracao.py` contém seis métodos de teste, contemplando:

- Dez personas simuladas.
- Ranking completo e Top 3.
- Empates e perfis uniformes.
- Lacunas nas dez carreiras.
- Avaliações parciais.
- Competências atendidas.
- Justificativas das regras acionadas.

Os métodos de teste podem executar múltiplos cenários internos.

### Resultado obtido

A execução consolidada apresentou:

```text
Ran 18 tests in 0.042s

OK
```

Todos os 18 métodos de teste foram aprovados na execução registrada.

## 11. Validação funcional

Além dos testes automatizados, foram realizados testes manuais na interface Streamlit.

Entre os cenários avaliados estão:

| Cenário | Resultado |
|---|---|
| Questionário de afinidades | Recomendações exibidas |
| Perfil uniforme | Empate e uniformidade identificados |
| Quatro competências com nível zero | Quatro lacunas identificadas |
| Avaliação parcialmente preenchida | Lacunas e dados não avaliados diferenciados |
| Nenhuma competência informada | Mensagem informativa exibida |
| Competências atendidas | Nenhuma lacuna identificada |
| Roadmap com duas lacunas | Apenas as etapas necessárias apresentadas |
| Wizard de quatro etapas | Navegação entre perfil pessoal, afinidades técnicas, objetivos e resultados validada |
| Objetivo profissional obrigatório | Mensagem de aviso apresentada quando nenhuma opção é selecionada |
| Recomendações complementares | Tecnologias, certificações e projetos GitHub apresentados corretamente |
| Persistência do objetivo profissional | Objetivo de primeira oportunidade Júnior preservado até a geração do roadmap |
| Orientações personalizadas | Três orientações correspondentes ao objetivo Júnior apresentadas no Streamlit |

As dez personas simuladas produziram as carreiras esperadas na primeira posição do ranking.

Os resultados completos e as limitações dos procedimentos estão documentados no arquivo:

**relatorio_validacao.md**

## 12. Limitações

O sistema utiliza pesos, condições e regras definidos para uma atividade acadêmica.

As recomendações refletem os critérios estabelecidos nessa modelagem.

Os percentuais apresentados não representam probabilidades de sucesso profissional, empregabilidade ou aptidão comprovada.

A identificação de competências depende das informações fornecidas pelo usuário.

Os níveis Júnior são referências acadêmicas e não constituem certificações profissionais.

Os testes com personas são simulações e não substituem avaliações com usuários reais.

Os fluxos da interface foram testados manualmente, sem uma suíte automatizada de testes de navegador.

O sistema deve ser utilizado como ferramenta complementar de exploração e orientação de carreiras.

## 13. Considerações finais

O Consultor Inteligente de Carreiras em TI reúne uma base de conhecimento estruturada, um motor de inferência baseado em regras e uma interface interativa.

A aplicação permite relacionar interesses a possibilidades profissionais, apresentar justificativas para as recomendações e identificar oportunidades de desenvolvimento de competências.

Os testes realizados demonstraram consistência funcional nos cenários avaliados, respeitando as limitações da modelagem acadêmica utilizada.
