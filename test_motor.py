
import unittest

import motor_inferencia as motor


class TestMotorInferencia(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base = motor.carregar_base_conhecimento()
        cls.perguntas = [
            pergunta["id"]
            for pergunta in cls.base["perguntas"]
        ]

    def criar_respostas(self, nivel=3):
        return {
            pergunta: nivel
            for pergunta in self.perguntas
        }

    def test_01_carregamento_base(self):
        self.assertEqual(len(self.base["trilhas"]), 10)
        self.assertEqual(len(self.perguntas), 12)
        self.assertEqual(len(self.base["regras"]), 20)
        self.assertEqual(
            len(self.base["competencias_junior"]), 10
        )

    def test_02_compatibilidade_ponderada(self):
        pesos = self.base["pesos_afinidade"]["backend"]

        minimo = motor.calcular_compatibilidade(
            self.criar_respostas(1), pesos
        )
        medio = motor.calcular_compatibilidade(
            self.criar_respostas(3), pesos
        )
        maximo = motor.calcular_compatibilidade(
            self.criar_respostas(5), pesos
        )

        self.assertEqual(minimo, 0)
        self.assertEqual(medio, 50)
        self.assertEqual(maximo, 100)

    def test_03_validacao_respostas(self):
        respostas = self.criar_respostas()

        self.assertTrue(
            motor.validar_respostas(respostas, self.base)
        )

        respostas.pop(self.perguntas[0])

        with self.assertRaises(ValueError):
            motor.validar_respostas(respostas, self.base)

        respostas = self.criar_respostas()
        respostas[self.perguntas[0]] = 6

        with self.assertRaises(ValueError):
            motor.validar_respostas(respostas, self.base)

        respostas = self.criar_respostas()
        respostas[self.perguntas[0]] = True

        with self.assertRaises(ValueError):
            motor.validar_respostas(respostas, self.base)

    def test_04_acionamento_das_20_regras(self):
        """
        Constrói um cenário satisfatório para cada regra
        e verifica seu acionamento pelo motor real.
        """
        regras = self.base["regras"]
        identificadores_acionados = set()

        for regra in regras:
            with self.subTest(regra=regra["id"]):
                respostas = self.criar_respostas()

                for condicao in regra["condicoes"]:
                    operador = condicao["operador"]
                    valor = condicao["valor"]

                    if operador == ">":
                        valor += 1
                    elif operador == "<":
                        valor -= 1

                    self.assertTrue(1 <= valor <= 5)

                    respostas[condicao["pergunta"]] = valor

                self.assertTrue(
                    motor.verificar_condicoes(
                        regra, respostas
                    )
                )

                ajuste, acionadas = motor.aplicar_regras(
                    regra["trilha"],
                    respostas,
                    regras
                )

                ids = {
                    item["id"]
                    for item in acionadas
                }

                self.assertIn(regra["id"], ids)

                self.assertEqual(
                    ajuste,
                    sum(
                        item["ajuste"]
                        for item in acionadas
                    )
                )

                identificadores_acionados.add(
                    regra["id"]
                )

        self.assertEqual(
            len(identificadores_acionados), 20
        )

    def test_05_bonificacao_backend(self):
        respostas = self.criar_respostas()
        respostas["desenvolvimento_backend"] = 4
        respostas["raciocinio_logico"] = 4

        ajuste, regras = motor.aplicar_regras(
            "backend",
            respostas,
            self.base["regras"]
        )

        self.assertEqual(ajuste, 5)
        self.assertIn(
            "R01",
            {regra["id"] for regra in regras}
        )

    def test_06_penalidade_backend(self):
        respostas = self.criar_respostas()
        respostas["desenvolvimento_backend"] = 4
        respostas["raciocinio_logico"] = 2

        ajuste, regras = motor.aplicar_regras(
            "backend",
            respostas,
            self.base["regras"]
        )

        self.assertEqual(ajuste, -8)
        self.assertIn(
            "R02",
            {regra["id"] for regra in regras}
        )

    def test_07_ranking_top3(self):
        resultado = motor.recomendar_carreiras(
            self.criar_respostas()
        )

        ranking = resultado["ranking_completo"]
        top3 = resultado["top3"]

        self.assertEqual(len(ranking), 10)
        self.assertEqual(len(top3), 3)
        self.assertEqual(top3, ranking[:3])

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

    def test_08_limites_percentuais(self):
        for nivel in (1, 5):
            with self.subTest(nivel=nivel):
                resultado = motor.recomendar_carreiras(
                    self.criar_respostas(nivel)
                )

                for carreira in resultado["ranking_completo"]:
                    self.assertGreaterEqual(
                        carreira["compatibilidade"], 0
                    )
                    self.assertLessEqual(
                        carreira["compatibilidade"], 100
                    )

    def test_09_skill_gaps_e_roadmap(self):
        competencias = self.base[
            "competencias_junior"
        ]["backend"]

        conhecimentos = {
            competencia["id"]: 0
            for competencia in competencias
        }

        analise = motor.analisar_competencias(
            "backend",
            conhecimentos
        )

        roadmap = motor.gerar_roadmap(
            "backend",
            conhecimentos
        )

        self.assertEqual(len(analise["lacunas"]), 4)
        self.assertEqual(len(roadmap["etapas"]), 4)
        self.assertTrue(analise["analise_completa"])

    def test_10_competencias_nao_avaliadas(self):
        competencia = self.base[
            "competencias_junior"
        ]["backend"][0]

        conhecimentos = {
            competencia["id"]:
                competencia["nivel_requerido"]
        }

        analise = motor.analisar_competencias(
            "backend",
            conhecimentos
        )

        self.assertFalse(analise["analise_completa"])
        self.assertEqual(len(analise["lacunas"]), 0)
        self.assertEqual(len(analise["nao_avaliadas"]), 3)

        roadmap = motor.gerar_roadmap(
            "backend",
            conhecimentos
        )

        self.assertEqual(len(roadmap["etapas"]), 0)
        self.assertFalse(roadmap["analise_completa"])

    def test_11_roadmaps_das_dez_carreiras(self):
        for trilha in self.base["trilhas"]:
            with self.subTest(trilha=trilha["id"]):
                carreira = trilha["id"]

                conhecimentos = {
                    competencia["id"]: 0
                    for competencia in self.base[
                        "competencias_junior"
                    ][carreira]
                }

                resultado = motor.gerar_roadmap(
                    carreira,
                    conhecimentos
                )

                self.assertEqual(
                    len(resultado["etapas"]), 4
                )

                self.assertTrue(
                    resultado["analise_completa"]
                )

    def test_12_empates_proximidade_e_perfil_uniforme(self):
        cenarios = [
            ("Minimo", 1, True, False, True),
            ("Medio", 3, True, False, True),
            ("Maximo", 5, True, False, True),
        ]

        for nome, nivel, empate, proximidade, uniforme in cenarios:
            with self.subTest(cenario=nome):
                respostas = self.criar_respostas(nivel)

                resultado = motor.recomendar_carreiras(respostas)

                self.assertEqual(
                    resultado["empate_primeiro"], empate
                )
                self.assertEqual(
                    resultado["proximidade_primeiro"], proximidade
                )
                self.assertEqual(
                    resultado["perfil_uniforme"], uniforme
                )
                self.assertEqual(
                    resultado["diferenca_top2"], 0
                )

        # Cenário específico de Desenvolvimento Mobile.
        respostas = self.criar_respostas(1)

        respostas.update({
            "desenvolvimento_mobile": 5,
            "interfaces_ux": 4,
            "raciocinio_logico": 4,
        })

        resultado = motor.recomendar_carreiras(respostas)

        self.assertEqual(
            resultado["top3"][0]["id"], "mobile"
        )

        self.assertFalse(
            resultado["empate_primeiro"]
        )

        self.assertTrue(
            resultado["proximidade_primeiro"]
        )

        self.assertFalse(
            resultado["perfil_uniforme"]
        )

        self.assertAlmostEqual(
            resultado["diferenca_top2"], 1.05, places=2
        )

if __name__ == "__main__":
    unittest.main()