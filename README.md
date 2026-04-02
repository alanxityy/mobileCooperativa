Instalação - Python

### 1. Backend (Django)
Abra o terminal na pasta raiz e siga:

```bash
# Entre na pasta do servidor
cd cooperativa

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale os pacotes necessários
pip install -r requirements.txt

# Execute as migrações do banco
python manage.py migrate

# Inicie o servidor
python manage.py runserver


Instalação - React Native(Expo)

# 1. Entrar na pasta mobile
cd mobile

# 2. Instalar as dependências do Node
npm install

# 3. Iniciar o Expo
npx expo start

Após iniciar, pressione 'w' para rodar no navegador ou use o aplicativo Expo Go no celular para escanear o QR Code.