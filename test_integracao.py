
import unittest

import motor_inferencia as motor


class TestIntegracaoSistema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base = motor.carregar_base_conhecimento()
        cls.perguntas = [
            pergunta["id"]
            for pergunta in cls.base["perguntas"]
        ]

    def criar_respostas(self, nivel=1):
        return {
            pergunta: nivel
            for pergunta in self.perguntas
        }

    def test_01_personas_das_dez_carreiras(self):
        cenarios = [
            ("backend", {
                "desenvolvimento_backend": 5,
                "raciocinio_logico": 5,
            }),
            ("frontend", {
                "interfaces_ux": 5,
                "raciocinio_logico": 4,
            }),
            ("ciencia_dados", {
                "analise_dados_ia": 5,
                "matematica": 5,
                "raciocinio_logico": 4,
            }),
            ("engenharia_dados", {
                "engenharia_dados": 5,
                "raciocinio_logico": 4,
                "cloud_infraestrutura": 4,
            }),
            ("ciberseguranca", {
                "ciberseguranca": 5,
                "raciocinio_logico": 4,
            }),
            ("devops", {
                "devops_sre": 5,
                "desenvolvimento_backend": 4,
                "cloud_infraestrutura": 4,
            }),
            ("cloud", {
                "cloud_infraestrutura": 5,
                "raciocinio_logico": 4,
                "devops_sre": 3,
            }),
            ("mobile", {
                "desenvolvimento_mobile": 5,
                "interfaces_ux": 4,
                "raciocinio_logico": 4,
            }),
            ("qa", {
                "qualidade_testes": 5,
                "raciocinio_logico": 4,
            }),
            ("gestao_produtos", {
                "gestao_produtos": 5,
                "interfaces_ux": 4,
            }),
        ]

        for carreira_esperada, afinidades in cenarios:
            with self.subTest(carreira=carreira_esperada):
                respostas = self.criar_respostas()
                respostas.update(afinidades)

                resultado = motor.recomendar_carreiras(
                    respostas
                )

                ranking = resultado["ranking_completo"]

                self.assertEqual(len(ranking), 10)
                self.assertEqual(len(resultado["top3"]), 3)
                self.assertEqual(
                    ranking[0]["id"],
                    carreira_esperada
                )

                self.assertEqual(
                    resultado["top3"],
                    ranking[:3]
                )

                percentuais = [
                    item["compatibilidade"]
                    for item in ranking
                ]

                self.assertEqual(
                    percentuais,
                    sorted(percentuais, reverse=True)
                )

                self.assertTrue(
                    all(0 <= p <= 100 for p in percentuais)
                )

                for carreira in ranking:
                    ajustes = sum(
                        regra["ajuste"]
                        for regra in carreira["regras_acionadas"]
                    )

                    self.assertEqual(
                        ajustes,
                        carreira["ajuste_percentual"]
                    )

    def test_02_empates_e_perfis_uniformes(self):
        for nivel in (1, 3, 5):
            with self.subTest(nivel=nivel):
                respostas = self.criar_respostas(nivel)

                resultado = motor.recomendar_carreiras(
                    respostas
                )

                self.assertTrue(
                    resultado["perfil_uniforme"]
                )
                self.assertTrue(
                    resultado["empate_primeiro"]
                )
                self.assertFalse(
                    resultado["proximidade_primeiro"]
                )
                self.assertEqual(
                    resultado["diferenca_top2"], 0
                )

    def test_03_lacunas_das_dez_carreiras(self):
        for trilha in self.base["trilhas"]:
            carreira = trilha["id"]

            with self.subTest(carreira=carreira):
                competencias = self.base[
                    "competencias_junior"
                ][carreira]

                conhecimentos = {
                    competencia["id"]: 0
                    for competencia in competencias
                }

                analise = motor.analisar_competencias(
                    carreira, conhecimentos
                )

                roadmap = motor.gerar_roadmap(
                    carreira, conhecimentos
                )

                self.assertEqual(
                    len(analise["lacunas"]), 4
                )
                self.assertEqual(
                    len(roadmap["etapas"]), 4
                )
                self.assertTrue(
                    analise["analise_completa"]
                )

    def test_04_avaliacao_parcial(self):
        carreira = "ciberseguranca"

        competencias = self.base[
            "competencias_junior"
        ][carreira]

        conhecimentos = {
            competencias[0]["id"]:
                competencias[0]["nivel_requerido"],
            competencias[1]["id"]:
                competencias[1]["nivel_requerido"] - 1,
            competencias[3]["id"]: 0,
        }

        analise = motor.analisar_competencias(
            carreira, conhecimentos
        )

        roadmap = motor.gerar_roadmap(
            carreira, conhecimentos
        )

        self.assertEqual(
            len(analise["competencias_atendidas"]), 1
        )
        self.assertEqual(len(analise["lacunas"]), 2)
        self.assertEqual(len(analise["nao_avaliadas"]), 1)
        self.assertFalse(analise["analise_completa"])

        self.assertEqual(
            [etapa["ordem"] for etapa in roadmap["etapas"]],
            [2, 4]
        )

    def test_05_competencias_atendidas(self):
        for trilha in self.base["trilhas"]:
            carreira = trilha["id"]

            with self.subTest(carreira=carreira):
                conhecimentos = {
                    competencia["id"]:
                        competencia["nivel_requerido"]
                    for competencia in self.base[
                        "competencias_junior"
                    ][carreira]
                }

                analise = motor.analisar_competencias(
                    carreira, conhecimentos
                )

                roadmap = motor.gerar_roadmap(
                    carreira, conhecimentos
                )

                self.assertEqual(
                    len(analise["competencias_atendidas"]),
                    4
                )
                self.assertEqual(len(analise["lacunas"]), 0)
                self.assertEqual(len(roadmap["etapas"]), 0)

    def test_06_justificativas_das_regras(self):
        cenarios = [
            ("backend", "R01", {
                "desenvolvimento_backend": 4,
                "raciocinio_logico": 4,
            }),
            ("backend", "R02", {
                "desenvolvimento_backend": 4,
                "raciocinio_logico": 2,
            }),
            ("mobile", "R15", {
                "desenvolvimento_mobile": 5,
                "interfaces_ux": 4,
                "raciocinio_logico": 4,
            }),
        ]

        for carreira, regra_esperada, afinidades in cenarios:
            with self.subTest(regra=regra_esperada):
                respostas = self.criar_respostas(3)
                respostas.update(afinidades)

                resultado = motor.recomendar_carreiras(
                    respostas
                )

                registro = next(
                    item
                    for item in resultado["ranking_completo"]
                    if item["id"] == carreira
                )

                regras = registro["regras_acionadas"]

                self.assertIn(
                    regra_esperada,
                    {regra["id"] for regra in regras}
                )

                self.assertTrue(
                    all(regra["descricao"] for regra in regras)
                )


if __name__ == "__main__":
    unittest.main()
