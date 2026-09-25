# GW Wireless - Performance Operacional Logístico

Portal Executivo Integrado de Inteligência e Performance Operacional para a **GW Wireless**.

## 📌 Visão Geral do Projeto

Este projeto consolida os dados operacionais e financeiros da logística da GW Wireless em um portal único, interativo e de alta performance:

1. **Performance da Equipe (WMS):**
   - Ranking de separadores de pedidos (`vw_separacao_pedidos`).
   - Ranking de armazenagem e entrada de mercadorias (`vw_movimentacoes`).
   - Produtividade em transferências entre filiais.
   - Auditorias de recebimento.

2. **Acuracidade de Estoque & Furo (6 Filiais):**
   - Cruzamento entre saldo físico de referência **Saldo SN (Disponível + Reservado)** e WMS.
   - Diagnóstico assertivo de **Sobras vs Faltas** através da indicação de *"WMS maior em"*.
   - Mapeamento das 6 filiais parametrizadas:
     - GW Matriz (Lojas 1 e 8 - Anápolis)
     - GW Goiânia (Lojas 6 e 90)
     - GW Brasília (Lojas 9 e 91)
     - GW Palmas (Lojas 10 e 11)
     - GW Marabá (Lojas 7 e 12)
     - GW São Luís (Loja 14)
   - Filtro multi-loja dinâmico (seleção de uma ou mais filiais simultâneas).

3. **Custo de Transporte, Romaneios & Telemetria:**
   - 88 Romaneios Master programados por veículo com valor transportado.
   - 180 Entregas detalhadas gota a gota por cliente/cidade.
   - DRE da Frota com 25 veículos (combustível, pedágios Sem Parar e manutenção GLPI).
   - **Telemetria Ao Vivo Wisevia (Yuv Cloud Services):**
     - Rastreamento em tempo real de 13 veículos com câmeras inteligentes.
     - Status de ignição (Ligada/Desligada), velocidade e endereço por geocodificação reversa.
     - Detecção de IA embarcada (11.700+ alarmes de fadiga, olhos fechados, bocejo, distração, celular e saída de faixa).
     - Visualização e reprodução direta dos vídeos MP4 e fotos gravadas pelas câmeras de cabine na nuvem (Oracle Cloud).

---

## 🛠️ Tecnologias e Arquitetura

- **Backend / ETL:** Python 3.12+ (`psycopg2`, `requests`, `python-dotenv`, `openpyxl`, `pandas`)
- **Frontend / Dashboard:** HTML5, Tailwind CSS (Glassmorphism), Chart.js, Font Awesome 6, SheetJS (XLSX), html2canvas
- **Bancos de Dados Integrados:**
  - PostgreSQL 17.6 (Hub Central: `postgres`, `gw_logistics`, `monitor_glpi`)
  - MySQL (WMS e GLPI)
  - Microsoft SQL Server (S7 ERP)
- **APIs:** Wisevia / Yuv Cloud Services (`https://quality.api.cloud-services.yuv.com.br`)

---

## 🚀 Como Executar em seu Computador Pessoal

### 1. Clonar o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd Bancos
```

### 2. Configurar o ambiente Python
```bash
python -m venv .venv
# No Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Configurar as Credenciais
Copie o arquivo `.env.example` para `.env` e preencha as variáveis de banco de dados e chave da API Wisevia:
```bash
copy .env.example .env
```
*(Nota: Se estiver fora da rede interna da empresa, utilize o IP do Tailscale `100.111.205.81` para o banco de dados PostgreSQL).*

### 4. Abrir o Dashboard
Basta abrir o arquivo HTML diretamente no seu navegador preferido (Chrome, Edge, Firefox, Brave):
```bash
start Dashboard_Performance_Operacional_Logistico.html
```
*(O dashboard é 100% autocontido, offline-first e não requer servidor web local para visualização completa).*

### 5. Sincronizar Novos Dados
Para rodar a sincronização dos dados de telemetria da Wisevia com o banco e gerar um novo snapshot:
```bash
python populate_wisevia_data.py
python build_telemetria_module.py
```
