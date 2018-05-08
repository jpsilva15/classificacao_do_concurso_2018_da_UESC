import PyPDF2 
import re 
 
class Candidato(object): 
 
    def __init__(self): 
        self.codigo = None 
        self.nome = None 
        self.portuguesa = 0 
        self.informatica = 0 
        self.especifico = 0 
 
    def __repr__(self): 
        return "Código: %s Nome:%s Média: %s | Pontuação P: %s I: %s E: %s" % (self.codigo, self.nome, self.media(), self.portuguesa, self.informatica, self.especifico)
 
    def media(self): 
        return ((self.informatica+self.portuguesa)*0.3+self.especifico*0.7)/2.4 
 
    def __lt__(self, outro):
        return self.media() < outro.media()
 
def scraper(page_content): 
    candidatos = [] 
    nomes = page_content.split("ESPECÍFICOS")[1] 
    todos = re.sub('\d\d\d\d\d\D+AusAusAus', "", nomes) 
    todos = re.sub('\D+.:\d+', "", todos) 
    todos = re.findall('\d\d\d\d\d\D+\d+.\d+.\d+', todos) 
    for candidato in todos: 
        candidato_1 = Candidato() 
        candidato_1.codigo = re.findall('\d\d\d\d\d', candidato)[0] 
        candidato_1.nome = re.findall('\D+', candidato)[0] 
        candidato_1.portuguesa = int(re.findall('\d+\.', candidato)[0][:-1]) 
        candidato_1.informatica = int(re.findall('\.\d+\.', candidato)[0][1:-1]) 
        candidato_1.especifico = int(re.findall('\.\d+', candidato)[1][1:]) 
        candidatos.append(candidato_1) 
 
    return candidatos 
def classificar(candidatos): 
    i = len(candidatos) 
    for n, x in enumerate(sorted(candidatos)): 
        print(i - n, x) 
    return 
 
def print_classificacao(candidatos_analista,candidatos_tecnico): 
    resp = input("\n\nClassificação para\n[1]Cargo: 102-ANALISTA UNIVERSITÁRIO\n[2]Cargo: 201-TECNICO UNIVERSITÁRIO\n[3]Sair\n") 
    if int(resp) == 1: 
        classificar(candidatos_analista) 
        print_classificacao(candidatos_analista, candidatos_tecnico) 
    elif int(resp) == 2: 
        classificar(candidatos_tecnico) 
        print_classificacao(candidatos_analista, candidatos_tecnico) 
    elif int(resp) == 3: 
        exit() 
    else: 
        print_classificacao(candidatos_analista, candidatos_tecnico) 
 
print("Classificação dos candidatos do Concurso Público para os Cargos de Analista e Técnico Universitários 2018 da UESC.") 
pdf_file = open('UESC_RESULTADO_P_OBJETIVA2_EDITAL_13_2018.PDF', 'rb') 
read_pdf = PyPDF2.PdfFileReader(pdf_file) 
candidatos_analista = [] 
candidatos_tecnico = [] 
for x in range(read_pdf.getNumPages()): 
    page_content = read_pdf.getPage(x).extractText() 
    cargo = re.search("-ANALISTA|-TECNICO", page_content) 
    cargo = cargo.group() 
    if cargo == "-ANALISTA": 
        candidatos_analista.extend(scraper(page_content)) 
    elif cargo == "-TECNICO": 
        candidatos_tecnico.extend(scraper(page_content)) 
    else: 
        print("erro em PDF, %s",x) 
 
print_classificacao(candidatos_analista,candidatos_tecnico) 