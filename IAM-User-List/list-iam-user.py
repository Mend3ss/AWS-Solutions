import boto3
import csv

# Crie um objeto de cliente IAM
iam_client = boto3.client('iam')

# Obtenha uma lista de todos os usuários do IAM
users = iam_client.list_users()

# Crie um arquivo Excel
with open('usuarios_iam_grupos_formatado.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Escreva o cabeçalho da planilha
    writer.writerow(['Nome do usuário', 'ID do usuário', 'Grupos'])

    # Para cada usuário
    for user in users['Users']:
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

