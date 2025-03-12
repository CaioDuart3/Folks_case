
class ImageExamChecker:
    # Palavras chaves para auxiliar na identificação de textos que são relacionados a exames de imagem.
    KEYWORDS = [
        "us", "tr", "tc", "tac", "rm", "rx", "digital", "dexa", "pet scan", "rnm",
        "tomografia", "radiografia", "imagem", "imagens", "ultrassom", "ressonância",
        "ecografia", "mamografia","mamas", "mama" "angiografia", "cintilografia", "fluoroscopia",
        "espectroscopia", "scopia", "densitometria"
    ]
    # Palavras chaves para auxiliar na identificação de textos que NÃO são relacionados a exames de imagem.
    NO_KEYWORDS = [
        "orientações", "horas","dia","mg", "ml","uso", "comprimido", "cápsula", "gotas", "xarope", "pomada", "creme",
        "injeção", "vacina", "dose", "tratamento", "uso tópico", "via sublingual",
        "via intramuscular", "via intravenosa", "via retal", "via nasal", "via ocular",
        "hemograma", "sorologia", "urocultura", "PCR", "VHS", "creatinina", "glicemia",
        "colesterol", "triglicerídeos", "hormônio", "tipagem sanguínea", "antígeno",
        "imunoglobulina", "prova de função hepática", "eletrólitos", "cultura bacteriana"
        "ansiedade", "depressão", "psiquiatra","psicológa"
    ]

    # Método utilizado para identicar a existência de palavras chaves nos textos
    @classmethod
    def contains_image_exam_terms(cls, text):
        text_lower = text.lower()
        # Verifica se há palavras que garantem que NÃO é um exame de imagem
        if any(term in text_lower for term in cls.NO_KEYWORDS):
            return False
        # Verifica se há palavras que indicam exame de imagem
        return any(term in text_lower for term in cls.KEYWORDS)
