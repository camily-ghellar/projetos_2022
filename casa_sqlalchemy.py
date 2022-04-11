from config_sqlalchemy import *

class Proprietario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(254))
    email = db.Column(db.String(254))
    telefone = db.Column(db.String(254))

    casas = db.relationship("Casa", backref = "proprietario")

    def __str__(self) -> str:
        return f'proprietário(a): ({self.id}) {self.nome}, {self.email}, {self.telefone}'

class Casa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    formato = db.Column(db.String(254))

    quartos = db.relationship("Quarto", backref = "casa")

    proprietario_id = db.Column(db.Integer, db.ForeignKey(Proprietario.id), nullable = False)

    def __str__(self) -> str:
        s = f'casa {self.formato}'
        if self.proprietario:
            s += f' é do(a) {str(self.proprietario)}'
        return s

class Quarto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(254))
    dimensoes = db.Column(db.String(254))

    casa_id = db.Column(db.Integer, db.ForeignKey(Casa.id), nullable = False)

    mobilias = db.relationship("Mobilia", backref = "quarto")

    def __str__(self) -> str:
        s = f'Quarto: {self.nome}, {self.dimensoes}'
        #if self.casa:
        s += f' na {str(self.casa)}'
        return s

class Mobilia(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(254))
    funcao = db.Column(db.String(254))
    material = db.Column(db.String(254))

    quarto_id = db.Column(db.Integer, db.ForeignKey(Quarto.id), nullable = True)

    def __str__(self) -> str:
        s = f'Mobília: ({self.id}) {self.nome}, {self.funcao}, {self.material}'
        if self.quarto:
            s += f', localizada em {str(self.quarto)}'
        return s

if __name__ == "__main__":
    if os.path.exists(arquivobd): # se houver o arquivo...
        os.remove(arquivobd) # ...apagar!

    db.create_all() # criar tabelas

    print()
    print("*** TESTE criando objetos")
    print()

    p1 = Proprietario(nome = "Alice", email = "alice@gmail.com", telefone = "123")
    db.session.add(p1)
    db.session.commit()
    print(p1)
    print()

    c1 = Casa(formato = "russa", proprietario = p1)
    db.session.add(c1)
    db.session.commit()
    print(c1)
    print()
    

    q1 = Quarto(nome = "Sala", dimensoes = "6x5 metros", casa = c1)
    db.session.add(q1)

    q2 = Quarto(nome="Banheiro", dimensoes="3x4 metros", casa = c1)
    db.session.add(q2)

    db.session.commit()
    print(q1)
    print(q2)
    print()

    print("*** TESTE com todos os dados")
    print()
    print(c1)

    # sem lista reversa
    for q in db.session.query(Quarto).filter(Quarto.casa_id == c1.id).all():
        print(q)
    print()

    print("*** TESTE com todos os dados, via lista reversa")
    print()
    print(c1)

    # com lista reversa
    for q in c1.quartos:
        print(q)
    print()

    print("*** TESTE das mobílias")
    print()
    m1 = Mobilia(nome = "Armário", funcao = "Guardar coisas", material = "Madeira", quarto=q1) 
    db.session.add(m1)
    db.session.commit()
    print(m1)
    print()

    # não está em nenhum quarto
    # versão 30/03 - Alice: adicionei "quarto=q2" que é o banheiro
    m2 = Mobilia(nome = "Espelho", funcao = "Ajudar a se arrumar", material = "Vidro polido", quarto = q2)
    db.session.add(m2)
    db.session.commit()
    print(m2)
    print()

    print("*** TESTE exibindo novamente todos os dados")
    print()
    print("*** TESTE com todos os dados CONECTADOS, via lista reversa")
    print()
    print("*** não vai exibir mobílias que não estão em quartos")
    print()
    print(c1)

    print()
    # quartos da casa, com lista reversa
    for q in c1.quartos:
        print(q)
        for m in q.mobilias:
            print(m)
            print()