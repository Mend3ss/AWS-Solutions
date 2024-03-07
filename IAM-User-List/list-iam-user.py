import boto3
import csv

# Crie um objeto de cliente IAM
iam_client = boto3.client('iam')

# Marcador para a próxima paginação
next_marker = None

# Lista para armazenar todos os usuários
all_users = []

# Loop para iterar pelas páginas de resultados
while True:
    # Obtenha uma lista de usuários (até 100 por padrão)
    if next_marker is None:
        users = iam_client.list_users()
    else:
        users = iam_client.list_users(Marker=next_marker)

    # Armazene os usuários da página atual
    all_users.extend(users['Users'])

    # Verifique se há mais páginas
    next_marker = users.get('Marker')
    if next_marker is None:
        # Não há mais páginas, termine o loop
        break

# Crie um arquivo CSV
with open('usuarios_iam_grupos_formatado.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Escreva o cabeçalho da planilha
    writer.writerow(['Nome do usuário', 'ID do usuário', 'Grupos'])

    # Para cada usuário
    for user in all_users:
        # Obtenha os grupos do usuário
        user_groups = iam_client.list_groups_for_user(UserName=user['UserName'])['Groups']

        # Lista de nomes de grupos
        group_names = [group['GroupName'] for group in user_groups]

        # Escreva as informações do usuário na planilha
        writer.writerow([
            user['UserName'],
            user['UserId'],
            ','.join(group_names),
        ])

print('Arquivo "usuarios_iam_grupos_formatado.csv" criado com sucesso!')