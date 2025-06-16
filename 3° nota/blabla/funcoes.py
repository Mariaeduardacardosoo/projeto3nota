import os

usuarios = []
caronas = []
reservas = []

def carregar_usuarios():
    global usuarios
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            for linha in f:
                nome, email, senha = linha.strip().split(";")
                usuarios.append({"nome": nome, "email": email, "senha": senha})

def salvar_usuario(usuario):
    with open("usuarios.txt", "a", encoding="utf-8") as f:
        f.write(f"{usuario['nome']};{usuario['email']};{usuario['senha']}\n")

def cadastrar_usuario(nome, email, senha):
    for u in usuarios:
        if u["email"] == email:
            return "Email já cadastrado."
    novo = {"nome": nome, "email": email, "senha": senha}
    usuarios.append(novo)
    salvar_usuario(novo)
    return "Cadastro realizado com sucesso."

def login(email, senha):
    for u in usuarios:
        if u["email"] == email and u["senha"] == senha:
            return u
    return None

def carregar_caronas():
    global caronas
    if os.path.exists("caronas.txt"):
        with open("caronas.txt", "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) == 7:
                    carona = {
                        "motorista": dados[0],
                        "origem": dados[1],
                        "destino": dados[2],
                        "data": dados[3],
                        "horario": dados[4],
                        "vagas": int(dados[5]),
                        "valor": float(dados[6]),
                        "passageiros": []
                    }
                    caronas.append(carona)

def salvar_carona(carona):
    with open("caronas.txt", "a", encoding="utf-8") as f:
        f.write(f"{carona['motorista']};{carona['origem']};{carona['destino']};{carona['data']};{carona['horario']};{carona['vagas']};{carona['valor']}\n")

def cadastrar_carona(usuario, origem, destino, data, horario, vagas, valor):
    nova = {
        "motorista": usuario["nome"],
        "origem": origem,
        "destino": destino,
        "data": data,
        "horario": horario,
        "vagas": int(vagas),
        "valor": float(valor),
        "passageiros": []
    }
    caronas.append(nova)
    salvar_carona(nova)
    return "Carona cadastrada com sucesso."

def listar_caronas():
    return [c for c in caronas if c["vagas"] > 0]

def buscar_caronas(origem, destino):
    return [c for c in caronas if c["origem"] == origem and c["destino"] == destino and c["vagas"] > 0]

def remover_carona(usuario, data):
    for c in caronas:
        if c["motorista"] == usuario["nome"] and c["data"] == data:
            caronas.remove(c)
            return "Carona removida."
    return "Carona não encontrada."

def caronas_do_usuario(usuario):
    return [c for c in caronas if c["motorista"] == usuario["nome"]]

def detalhes_carona(email_motorista, data):
    for c in caronas:
        if c["motorista"] == email_motorista and c["data"] == data:
            return c
    return None

def carregar_reservas():
    global reservas
    if os.path.exists("reservas.txt"):
        with open("reservas.txt", "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) == 3:
                    reserva = {
                        "passageiro": dados[0],
                        "motorista": dados[1],
                        "data": dados[2]
                    }
                    reservas.append(reserva)

def salvar_reserva(passageiro, motorista, data):
    with open("reservas.txt", "a", encoding="utf-8") as f:
        f.write(f"{passageiro};{motorista};{data}\n")

def fazer_reserva(email_passageiro, idx_carona):
    if idx_carona < 0 or idx_carona >= len(caronas):
        return "Índice inválido."
    c = caronas[idx_carona]
    if c["vagas"] > 0:
        c["vagas"] -= 1
        c["passageiros"].append(email_passageiro)
        salvar_reserva(email_passageiro, c["motorista"], c["data"])
        return "Reserva feita."
    return "Sem vagas disponíveis."

def cancelar_reserva(email_passageiro, motorista, data):
    for r in reservas:
        if r["passageiro"] == email_passageiro and r["motorista"] == motorista and r["data"] == data:
            reservas.remove(r)
            for c in caronas:
                if c["motorista"] == motorista and c["data"] == data:
                    c["vagas"] += 1
                    if email_passageiro in c["passageiros"]:
                        c["passageiros"].remove(email_passageiro)
            return "Reserva cancelada."
    return "Reserva não encontrada."

def gerar_relatorio(usuario):
    relatorio = []
    total_geral = 0
    for c in caronas:
        if c["motorista"] == usuario["nome"]:
            ocupadas = len(c["passageiros"])
            total = ocupadas * c["valor"]
            total_geral += total
            relatorio.append({
                "origem": c["origem"],
                "destino": c["destino"],
                "data": c["data"],
                "horario": c["horario"],
                "valor": c["valor"],
                "vagas": c["vagas"],
                "passageiros": c["passageiros"],
                "total": total
            })
    return relatorio, total_geral

def salvar_relatorio_txt(relatorio, total_geral):
    with open("relatorio.txt", "w", encoding="utf-8") as f:
        for r in relatorio:
            f.write(f"Origem: {r['origem']}, Destino: {r['destino']}, Data: {r['data']}, Horário: {r['horario']}, Valor por vaga: {r['valor']}, Passageiros: {len(r['passageiros'])}, Total: {r['total']}\n")
        f.write(f"\nTOTAL GERAL: {total_geral}\n")
