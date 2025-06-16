from blabla import funcoes

funcoes.carregar_usuarios()
funcoes.carregar_caronas()
funcoes.carregar_reservas()

usuario_logado = None

while True:
    if not usuario_logado:
        print("\n--- MENU INICIAL ---")
        print("1 - Cadastrar usuário")
        print("2 - Login")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome completo: ")
            email = input("Email: ")
            senha = input("Senha: ")
            mensagem = funcoes.cadastrar_usuario(nome, email, senha)
            print(mensagem)

        elif opcao == "2":
            email = input("Email: ")
            senha = input("Senha: ")
            usuario = funcoes.login(email, senha)
            if usuario:
                usuario_logado = usuario
                print(f"Login realizado. Bem-vindo, {usuario_logado['nome']}!")
            else:
                print("Email ou senha incorretos.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

    else:
        print(f"\n--- MENU DO USUÁRIO: {usuario_logado['nome']} ---")
        print("1 - Cadastrar carona")
        print("2 - Listar caronas disponíveis")
        print("3 - Buscar caronas por origem e destino")
        print("4 - Reservar vaga em carona")
        print("5 - Cancelar reserva")
        print("6 - Remover carona")
        print("7 - Mostrar detalhes de carona")
        print("8 - Mostrar minhas caronas cadastradas")
        print("9 - Relatório de ganhos como motorista")
        print("10 - Logout")
        print("0 - Sair do sistema")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            origem = input("Origem: ")
            destino = input("Destino: ")
            data = input("Data (dd/mm/aaaa): ")
            horario = input("Horário (hh:mm): ")
            vagas = input("Quantidade de vagas: ")
            valor = input("Valor por vaga: ")
            mensagem = funcoes.cadastrar_carona(usuario_logado, origem, destino, data, horario, vagas, valor)
            print(mensagem)

        elif opcao == "2":
            caronas_disp = funcoes.listar_caronas()
            if not caronas_disp:
                print("Nenhuma carona disponível.")
            else:
                for i, c in enumerate(caronas_disp):
                    print(f"{i + 1} - Motorista: {c['motorista']} | Origem: {c['origem']} | Destino: {c['destino']} | Data: {c['data']} | Horário: {c['horario']} | Vagas: {c['vagas']} | Valor: R${c['valor']}")

        elif opcao == "3":
            origem = input("Digite a origem: ")
            destino = input("Digite o destino: ")
            resultado = funcoes.buscar_caronas(origem, destino)
            if not resultado:
                print("Nenhuma carona encontrada.")
            else:
                for i, c in enumerate(resultado):
                    print(f"{i + 1} - Motorista: {c['motorista']} | Origem: {c['origem']} | Destino: {c['destino']} | Data: {c['data']} | Horário: {c['horario']} | Vagas: {c['vagas']} | Valor: R${c['valor']}")

        elif opcao == "4":
            caronas_disp = funcoes.listar_caronas()
            if not caronas_disp:
                print("Nenhuma carona disponível para reserva.")
            else:
                for i, c in enumerate(caronas_disp):
                    print(f"{i + 1} - Motorista: {c['motorista']} | Origem: {c['origem']} | Destino: {c['destino']} | Data: {c['data']} | Vagas: {c['vagas']}")
                escolha = input("Escolha o número da carona para reservar: ")
                if escolha.isdigit():
                    idx = int(escolha) - 1
                    mensagem = funcoes.fazer_reserva(usuario_logado["email"], idx)
                    print(mensagem)
                else:
                    print("Escolha inválida.")

        elif opcao == "5":
            email_motorista = input("Email do motorista da carona: ")
            data = input("Data da carona (dd/mm/aaaa): ")
            mensagem = funcoes.cancelar_reserva(usuario_logado["email"], email_motorista, data)
            print(mensagem)

        elif opcao == "6":
            data = input("Data da carona que deseja remover (dd/mm/aaaa): ")
            mensagem = funcoes.remover_carona(usuario_logado, data)
            print(mensagem)

        elif opcao == "7":
            email_motorista = input("Email do motorista da carona: ")
            data = input("Data da carona (dd/mm/aaaa): ")
            detalhes = funcoes.detalhes_carona(email_motorista, data)
            if detalhes:
                print(detalhes)
            else:
                print("Carona não encontrada.")

        elif opcao == "8":
            minhas = funcoes.caronas_do_usuario(usuario_logado)
            if not minhas:
                print("Você não cadastrou nenhuma carona.")
            else:
                for c in minhas:
                    passageiros = ', '.join(c['passageiros']) if c['passageiros'] else 'Nenhum'
                    print(f"Origem: {c['origem']} | Destino: {c['destino']} | Data: {c['data']} | Horário: {c['horario']} | Vagas: {c['vagas']} | Passageiros: {passageiros}")

        elif opcao == "9":
            relatorio, total_geral = funcoes.gerar_relatorio(usuario_logado)
            if relatorio:
                salvar = input("Deseja salvar o relatório em .txt? (sim/nao): ").strip().lower()
                if salvar == "sim":
                    funcoes.salvar_relatorio_txt(relatorio, total_geral)
                    print("Relatório salvo com sucesso.")

        elif opcao == "10":
            usuario_logado = None
            print("Logout realizado.")

        elif opcao == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida.")
