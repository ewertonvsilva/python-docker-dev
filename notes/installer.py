import json
import os

def main():
    # Ler o arquivo JSON
    with open('instructions.json') as f:
        instructions = json.load(f)

    # Executar as manipulações definidas no JSON
    for manipulation in instructions:
        action = manipulation['action']
        source = manipulation['source']
        destination = manipulation['destination']
        permissions = manipulation.get('permissions', None)

        if action == 'copy':
            copy_file(source, destination, permissions)

    print_report(instructions)

def copy_file(source, destination, permissions):
    # Criar o arquivo de destino, se necessário
    if not os.path.exists(destination):
        open(destination, 'w').close()

    # Copiar o conteúdo do arquivo de origem para o arquivo de destino
    with open(source, 'r') as f:
        contents = f.read()
    with open(destination, 'w') as f:
        f.write(contents)

    # Se as permissões forem definidas, defini-las no arquivo de destino
    if permissions is not None:
        os.chmod(destination, permissions)

def print_report(instructions):
    # Imprimir um relatório das cópias com nome dos arquivos e outros detalhes relevantes
    print('Arquivos copiados:')
    for manipulation in instructions:
        action = manipulation['action']
        source = manipulation['source']
        destination = manipulation['destination']
        permissions = manipulation.get('permissions', None)

        print('  Arquivo: {}'.format(source))
        print('  Destino: {}'.format(destination))
        if permissions is not None:
            print('  Permissões: {}'.format(permissions))

if __name__ == '__main__':
    main()
