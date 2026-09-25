import os
import json

print("Reading unified_logistics_data.json...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/unified_logistics_data.json', encoding='utf-8') as f:
    raw_data = json.load(f)

json_payload = json.dumps(raw_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Performance Operacional Logístico | GW Wireless</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- FontAwesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- SheetJS & html2canvas -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0b1120;
      color: #f8fafc;
    }}
    .custom-scroll::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scroll::-webkit-scrollbar-track {{
      background: #1e293b;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #475569;
      border-radius: 3px;
    }}
    .glass-card {{
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }}
    .hub-card {{
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .hub-card:hover {{
      transform: translateY(-4px) scale(1.01);
      box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.7);
    }}
    .tab-btn.active {{
      background-color: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
    }}
    .sub-tab-btn.active {{
      background-color: #1e293b;
      color: #38bdf8;
      border-color: #0284c7;
    }}
  </style>
</head>
<body class="min-h-screen custom-scroll flex flex-col">

  <!-- TOP APP BAR -->
  <header class="glass-card sticky top-0 z-50 px-6 py-3 border-b border-slate-800 flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center space-x-4">
      <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20 cursor-pointer" onclick="navigateTo('view-hub')">
        <i class="fa-solid fa-boxes-stacked text-xl text-white"></i>
      </div>
      <div>
        <div class="flex items-center space-x-2">
          <h1 class="text-xl font-bold tracking-tight text-white cursor-pointer hover:text-blue-400 transition" onclick="navigateTo('view-hub')">
            GW Wireless
          </h1>
          <span class="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-400 font-semibold border border-blue-500/30">
            Portal de Gestão Integrada
          </span>
        </div>
        <p class="text-xs text-slate-400" id="header-breadcrumb">Performance Operacional Logístico &bull; Hub Principal</p>
      </div>
    </div>

    <!-- Live Status Badges -->
    <div class="hidden xl:flex items-center space-x-2.5 text-xs">
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" title="WMS Estoque Conectado">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="font-medium">WMS: Conectado</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20" title="ERP S7 Conectado">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
        <span class="font-medium">S7: Conectado</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20" title="GLPI MySQL Conectado">
        <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
        <span class="font-medium">GLPI: Ao Vivo</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20" title="PostgreSQL Hub Frota">
        <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
        <span class="font-medium">Hub PG: 88 Romaneios</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20" title="Telemetria Wisevia & TI5">
        <i class="fa-solid fa-satellite-dish text-xs"></i>
        <span class="font-medium">TI5 & Wisevia: Aguardando API</span>
      </div>
    </div>

    <!-- Navigation Shortcuts -->
    <div class="flex items-center space-x-2">
      <button onclick="navigateTo('view-hub')" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition flex items-center space-x-1.5 border border-slate-700">
        <i class="fa-solid fa-house"></i>
        <span>Início</span>
      </button>
      <button onclick="exportCurrentView()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition flex items-center space-x-1.5 shadow-sm">
        <i class="fa-solid fa-file-excel"></i>
        <span>Excel</span>
      </button>
      <button onclick="captureCurrentSlide()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center space-x-1.5 shadow-sm">
        <i class="fa-solid fa-camera"></i>
        <span>Slide PNG</span>
      </button>
    </div>
  </header>

  <!-- MAIN WRAPPER -->
  <main class="flex-1 p-6 space-y-6 max-w-[1750px] mx-auto w-full" id="portal-capture-area">

    <!-- ======================================================== -->
    <!-- VIEW 0: HUB INICIAL (3 CAMPOS / PILARES PRINCIPAIS)       -->
    <!-- ======================================================== -->
    <section id="view-hub" class="main-view space-y-8">
      
      <!-- Welcome Hero -->
      <div class="glass-card rounded-3xl p-8 border border-slate-800 relative overflow-hidden bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900">
        <div class="relative z-10 max-w-3xl space-y-3">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-medium">
            <i class="fa-solid fa-circle-check"></i>
            <span>Painel Unificado de Performance Operacional Logístico</span>
          </div>
          <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Gestão Estratégica de Operações GW Wireless
          </h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            Selecione um dos três pilares operacionais abaixo para auditar a produtividade da equipe, acompanhar a acuracidade de estoque entre as 6 filiais e analisar os custos e viabilidade do transporte.
          </p>
        </div>
        <div class="absolute -right-12 -bottom-12 w-80 h-80 rounded-full bg-blue-600/10 blur-3xl pointer-events-none"></div>
      </div>

      <!-- THE 3 INTERACTIVE PILLAR CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <!-- CARD 1: PERFORMANCE DA EQUIPE -->
        <div onclick="navigateTo('view-performance')" class="glass-card hub-card rounded-2xl p-6 border border-slate-800 hover:border-blue-500/50 cursor-pointer flex flex-col justify-between group">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="w-14 h-14 rounded-2xl bg-blue-500/10 text-blue-400 flex items-center justify-center text-2xl group-hover:bg-blue-600 group-hover:text-white transition shadow-sm">
                <i class="fa-solid fa-users-gear"></i>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                Operacional WMS
              </span>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white group-hover:text-blue-400 transition">
                Performance da Equipe
              </h3>
              <p class="text-xs text-slate-400 mt-1">
                Produtividade individual e coletiva dos operadores com rankings e métricas de volume.
              </p>
            </div>
            
            <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-center">
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Separação</span>
                <span class="font-extrabold text-blue-400 text-sm">4.720</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Entradas</span>
                <span class="font-extrabold text-emerald-400 text-sm">7.544</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Saídas</span>
                <span class="font-extrabold text-amber-400 text-sm">7.243</span>
              </div>
            </div>

            <ul class="text-xs text-slate-300 space-y-1.5 pt-1">
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-trophy text-amber-400 text-[10px]"></i>
                <span>Ranking de Usuários que Mais Separaram</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-dolly text-cyan-400 text-[10px]"></i>
                <span>Ranking de Armazenamento de Produtos</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-arrow-right-arrow-left text-purple-400 text-[10px]"></i>
                <span>Ranking de Transferências & Expedição</span>
              </li>
            </ul>
          </div>

          <div class="pt-5 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-blue-400 group-hover:translate-x-1 transition">
            <span>Acessar Performance da Equipe</span>
            <i class="fa-solid fa-arrow-right"></i>
          </div>
        </div>

        <!-- CARD 2: ACURACIDADE DE ESTOQUE -->
        <div onclick="navigateTo('view-acuracidade')" class="glass-card hub-card rounded-2xl p-6 border border-slate-800 hover:border-emerald-500/50 cursor-pointer flex flex-col justify-between group">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="w-14 h-14 rounded-2xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-2xl group-hover:bg-emerald-600 group-hover:text-white transition shadow-sm">
                <i class="fa-solid fa-boxes-packing"></i>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Auditoria & Saldos
              </span>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white group-hover:text-emerald-400 transition">
                Acuracidade de Estoque
              </h3>
              <p class="text-xs text-slate-400 mt-1">
                Auditoria de saldos WMS vs SN, reservas ativas, identificação de furos e compensações.
              </p>
            </div>
            
            <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-center">
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Reservas</span>
                <span class="font-extrabold text-emerald-400 text-sm">831 DAVs</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Furos</span>
                <span class="font-extrabold text-rose-400 text-sm">R$ 577k</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Filiais</span>
                <span class="font-extrabold text-cyan-400 text-sm">6 Lojas</span>
              </div>
            </div>

            <ul class="text-xs text-slate-300 space-y-1.5 pt-1">
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-triangle-exclamation text-rose-400 text-[10px]"></i>
                <span>Reservas & Furos de Estoque por DAV</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-tags text-amber-400 text-[10px]"></i>
                <span>Troca de Etiqueta (Nomes/SKUs Similares)</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-scale-balanced text-emerald-400 text-[10px]"></i>
                <span>Compensação Entre-Lojas (Sobras vs Faltas)</span>
              </li>
            </ul>
          </div>

          <div class="pt-5 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-emerald-400 group-hover:translate-x-1 transition">
            <span>Acessar Acuracidade de Estoque</span>
            <i class="fa-solid fa-arrow-right"></i>
          </div>
        </div>

        <!-- CARD 3: CUSTO DE TRANSPORTE & FROTAS -->
        <div onclick="navigateTo('view-transporte')" class="glass-card hub-card rounded-2xl p-6 border border-slate-800 hover:border-indigo-500/50 cursor-pointer flex flex-col justify-between group">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="w-14 h-14 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-2xl group-hover:bg-indigo-600 group-hover:text-white transition shadow-sm">
                <i class="fa-solid fa-truck-ramp-box"></i>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Logística & Frotas
              </span>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white group-hover:text-indigo-400 transition">
                Custo de Transporte & Frotas
              </h3>
              <p class="text-xs text-slate-400 mt-1">
                DRE por placa, programação de romaneios, entregas gota a gota e módulo de telemetria.
              </p>
            </div>
            
            <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-center">
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Frota Total</span>
                <span class="font-extrabold text-indigo-400 text-sm">25 Veículos</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Custo Geral</span>
                <span class="font-extrabold text-amber-400 text-sm">R$ 2,18M</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Romaneios</span>
                <span class="font-extrabold text-cyan-400 text-sm">88 Viagens</span>
              </div>
            </div>

            <ul class="text-xs text-slate-300 space-y-1.5 pt-1">
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-route text-blue-400 text-[10px]"></i>
                <span>Romaneios Master & Entregas Detalhadas</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-gas-pump text-amber-400 text-[10px]"></i>
                <span>Gasola, Sem Parar e Manutenções GLPI</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-video text-rose-400 text-[10px]"></i>
                <span>Módulo de Telemetria Wisevia (37 Alarmes)</span>
              </li>
            </ul>
          </div>

          <div class="pt-5 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-indigo-400 group-hover:translate-x-1 transition">
            <span>Acessar Transporte & Frotas</span>
            <i class="fa-solid fa-arrow-right"></i>
          </div>
        </div>

      </div>

      <!-- Quick Executive Summary Banner -->
      <div class="glass-card rounded-2xl p-6 border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid fa-diagram-project"></i>
          </div>
          <div>
            <h4 class="text-sm font-bold text-white">Próximo Passo: Conexão das APIs de Telemetria TI5 e Wisevia</h4>
            <p class="text-xs text-slate-400">
              O módulo de transporte já conta com todos os Romaneios do Gabriel Joffre, custos da frota e a estrutura de 37 alarmes catalogada. Assim que você disponibilizar as credenciais da TI5 e Wisevia, conectaremos a telemetria ao vivo.
            </p>
          </div>
        </div>
      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 1: PERFORMANCE DA EQUIPE                            -->
    <!-- ======================================================== -->
    <section id="view-performance" class="main-view hidden space-y-6">
      
      <!-- View Header with Back Button -->
      <div class="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div class="flex items-center space-x-3">
          <button onclick="navigateTo('view-hub')" class="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition" title="Voltar ao Hub">
            <i class="fa-solid fa-arrow-left"></i>
          </button>
          <div>
            <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-users-gear text-blue-400"></i>
              <span>Performance Operacional da Equipe</span>
            </h2>
            <p class="text-xs text-slate-400">Produtividade de Separação, Armazenagem / Entradas e Transferências / Saídas</p>
          </div>
        </div>

        <!-- Sub Tabs Selector -->
        <div class="flex flex-wrap gap-2">
          <button onclick="switchPerformanceTab('perf-separacao')" id="btn-perf-separacao" class="sub-tab-btn active px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-box-open mr-1.5 text-amber-400"></i>
            <span>1. Separação de Pedidos</span>
          </button>
          <button onclick="switchPerformanceTab('perf-armazenagem')" id="btn-perf-armazenagem" class="sub-tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-dolly mr-1.5 text-emerald-400"></i>
            <span>2. Armazenagem & Entradas</span>
          </button>
          <button onclick="switchPerformanceTab('perf-transferencias')" id="btn-perf-transferencias" class="sub-tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-arrow-right-arrow-left mr-1.5 text-purple-400"></i>
            <span>3. Transferências & Saídas</span>
          </button>
          <button onclick="switchPerformanceTab('perf-recebimento')" id="btn-perf-recebimento" class="sub-tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-clipboard-check mr-1.5 text-cyan-400"></i>
            <span>4. Recebimento de Cargas</span>
          </button>
        </div>
      </div>

      <!-- PERFORMANCE SUB-PANEL 1: SEPARAÇÃO -->
      <div id="perf-separacao" class="perf-sub-panel space-y-6">
        
        <!-- Podium Top 3 Separadores -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="podium-separacao">
          <!-- Injected via JS -->
        </div>

        <!-- Ranking Table -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-ranking-star text-amber-400"></i>
                <span>Ranking Geral: Usuários que Mais Separaram Pedidos (WMS)</span>
              </h3>
              <p class="text-xs text-slate-400">Ordenado por volume total de pedidos faturados e itens separados</p>
            </div>
            <input type="text" id="search-perf-sep" oninput="renderTableSeparacao()" placeholder="Buscar operador..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800">
                <tr>
                  <th class="py-3 px-4">Posição</th>
                  <th class="py-3 px-4">Operador / Usuário</th>
                  <th class="py-3 px-4 text-right">Pedidos Separados</th>
                  <th class="py-3 px-4 text-right">Linhas de Itens</th>
                  <th class="py-3 px-4 text-right">Unidades Totais</th>
                  <th class="py-3 px-4 text-center">Primeiro Registro</th>
                  <th class="py-3 px-4 text-center">Último Registro</th>
                  <th class="py-3 px-4 text-center">Nível de Atividade</th>
                </tr>
              </thead>
              <tbody id="tbody-perf-sep" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- PERFORMANCE SUB-PANEL 2: ARMAZENAGEM / ENTRADA -->
      <div id="perf-armazenagem" class="perf-sub-panel hidden space-y-6">
        
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-dolly text-emerald-400"></i>
                <span>Ranking de Armazenagem & Entrada de Produtos no Estoque</span>
              </h3>
              <p class="text-xs text-slate-400">Operadores que mais deram entrada, guardaram e endereçaram produtos no WMS</p>
            </div>
            <input type="text" id="search-perf-arm" oninput="renderTableArmazenagem()" placeholder="Buscar operador..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800">
                <tr>
                  <th class="py-3 px-4">Posição</th>
                  <th class="py-3 px-4">Operador</th>
                  <th class="py-3 px-4">Login</th>
                  <th class="py-3 px-4 text-right">Total Movimentações</th>
                  <th class="py-3 px-4 text-right">SKUs Distintos</th>
                  <th class="py-3 px-4 text-right">Unidades Guardadas</th>
                  <th class="py-3 px-4 text-center">Última Entrada</th>
                </tr>
              </thead>
              <tbody id="tbody-perf-arm" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- PERFORMANCE SUB-PANEL 3: TRANSFERÊNCIAS & SAÍDAS -->
      <div id="perf-transferencias" class="perf-sub-panel hidden space-y-6">
        
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-arrow-right-arrow-left text-purple-400"></i>
                <span>Ranking de Transferências & Expedição (Saídas WMS)</span>
              </h3>
              <p class="text-xs text-slate-400">Operadores responsáveis pela movimentação entre galpões, filiais e expedição</p>
            </div>
            <input type="text" id="search-perf-transf" oninput="renderTableTransferencias()" placeholder="Buscar operador..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800">
                <tr>
                  <th class="py-3 px-4">Posição</th>
                  <th class="py-3 px-4">Operador</th>
                  <th class="py-3 px-4">Login</th>
                  <th class="py-3 px-4 text-right">Movimentações de Saída</th>
                  <th class="py-3 px-4 text-right">SKUs Movimentados</th>
                  <th class="py-3 px-4 text-right">Unidades Expedidas</th>
                  <th class="py-3 px-4 text-center">Última Movimentação</th>
                </tr>
              </thead>
              <tbody id="tbody-perf-transf" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- PERFORMANCE SUB-PANEL 4: RECEBIMENTO -->
      <div id="perf-recebimento" class="perf-sub-panel hidden space-y-6">
        
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div>
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-clipboard-check text-cyan-400"></i>
              <span>Auditoria de Recebimento de Mercadorias e Conferência</span>
            </h3>
            <p class="text-xs text-slate-400">Conferentes que receberam carretas e validaram volumes de fornecedores</p>
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800">
                <tr>
                  <th class="py-3 px-4">Conferente / Responsável</th>
                  <th class="py-3 px-4 text-right">Cargas Recebidas</th>
                  <th class="py-3 px-4 text-right">Linhas de Itens</th>
                  <th class="py-3 px-4 text-right">Qtd Esperada</th>
                  <th class="py-3 px-4 text-right">Qtd Conferida</th>
                </tr>
              </thead>
              <tbody id="tbody-perf-rec" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 2: ACURACIDADE DE ESTOQUE                           -->
    <!-- ======================================================== -->
    <section id="view-acuracidade" class="main-view hidden space-y-6">
      
      <!-- View Header with Back Button -->
      <div class="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div class="flex items-center space-x-3">
          <button onclick="navigateTo('view-hub')" class="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition" title="Voltar ao Hub">
            <i class="fa-solid fa-arrow-left"></i>
          </button>
          <div>
            <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-boxes-packing text-emerald-400"></i>
              <span>Acuracidade de Estoque & Auditoria</span>
            </h2>
            <p class="text-xs text-slate-400">Confronto WMS vs SN, Reservas e Furos de Estoque nas 6 Lojas</p>
          </div>
        </div>

        <!-- 7 Sub-Tabs exactly as requested -->
        <div class="flex flex-wrap gap-1.5">
          <button onclick="switchAcuracidadeTab('acur-reservas')" id="btn-acur-reservas" class="sub-tab-btn active px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            1. Reservas & Furo
          </button>
          <button onclick="switchAcuracidadeTab('acur-reunioes')" id="btn-acur-reunioes" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            2. Resumo Reuniões
          </button>
          <button onclick="switchAcuracidadeTab('acur-compensacao')" id="btn-acur-compensacao" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            3. Compensação Lojas
          </button>
          <button onclick="switchAcuracidadeTab('acur-troca')" id="btn-acur-troca" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            4. Troca Etiqueta
          </button>
          <button onclick="switchAcuracidadeTab('acur-sem-wms')" id="btn-acur-sem-wms" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            5. Sem WMS
          </button>
          <button onclick="switchAcuracidadeTab('acur-sem-sn')" id="btn-acur-sem-sn" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            6. Sem SN
          </button>
          <button onclick="switchAcuracidadeTab('acur-6lojas')" id="btn-acur-6lojas" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            7. Comparativo 6 Lojas
          </button>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 1: RESERVAS & FURO -->
      <div id="acur-reservas" class="acur-sub-panel space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Total de Reservas</span>
            <div class="text-2xl font-extrabold text-white mt-1" id="kpi-res-total">831 DAVs</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Identificadas como FURO</span>
            <div class="text-2xl font-extrabold text-rose-400 mt-1" id="kpi-res-furos">121 DAVs</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Valor Total em Furo</span>
            <div class="text-2xl font-extrabold text-amber-400 mt-1">R$ 577.290,14</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Itens Faltantes</span>
            <div class="text-2xl font-extrabold text-cyan-400 mt-1">1.482 un</div>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white">Pedidos e DAVs em Reserva (Destaque para FURO DE ESTOQUE)</h3>
              <p class="text-xs text-slate-400">Consulte número de pedido, produto, quantidade, valor e observações registradas</p>
            </div>
            <input type="text" id="search-acur-res" oninput="renderTableReservas()" placeholder="Buscar pedido, SKU, observação..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-72">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[500px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Pedido / DAV</th>
                  <th class="py-2.5 px-3">Status</th>
                  <th class="py-2.5 px-3">SKU</th>
                  <th class="py-2.5 px-3">Descrição do Produto</th>
                  <th class="py-2.5 px-3 text-right">Qtd Reservada</th>
                  <th class="py-2.5 px-3 text-right">Valor Unit. (R$)</th>
                  <th class="py-2.5 px-3 text-right">Valor Total (R$)</th>
                  <th class="py-2.5 px-3">Observação do Pedido</th>
                </tr>
              </thead>
              <tbody id="tbody-acur-res" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 2: RESUMO REUNIÕES -->
      <div id="acur-reunioes" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
          <h3 class="text-base font-bold text-white">Pauta Executiva para Reunião de Auditoria e Estoque</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="font-bold text-rose-400 block text-sm">1. Regularização de Furos Críticos</span>
              <p>Foram detectados 121 pedidos sinalizados explicitamente com "FURO DE ESTOQUE" na observação. O montante financeiro total retido nessas reservas é de <strong>R$ 577.290,14</strong>. A equipe de auditoria deve verificar fisicamente os endereços no WMS.</p>
            </div>
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="font-bold text-amber-400 block text-sm">2. Ajuste de Inversão de Etiquetas</span>
              <p>Identificamos diversos casos em que produtos com descrições e códigos quase idênticos (ex: bobinas de drop, conectores, cabos ópticos) constam com saldo positivo no WMS e negativo no SN, indicando troca de etiqueta no momento da entrada física.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 3: COMPENSAÇÃO LOJAS -->
      <div id="acur-compensacao" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <h3 class="text-sm font-bold text-white">Compensação Entre-Lojas (Sobras WMS vs Faltas SN)</h3>
          <p class="text-xs text-slate-400">Sugestão de transferências para equilibrar furos e sobras entre as filiais</p>
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[450px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">SKU</th>
                  <th class="py-2.5 px-3">Produto</th>
                  <th class="py-2.5 px-3">Loja com Sobra</th>
                  <th class="py-2.5 px-3 text-right">Saldo Sobrando</th>
                  <th class="py-2.5 px-3">Loja com Falta / Furo</th>
                  <th class="py-2.5 px-3 text-right">Saldo Faltando</th>
                  <th class="py-2.5 px-3 text-center">Ação Sugerida</th>
                </tr>
              </thead>
              <tbody id="tbody-acur-comp" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 4: TROCA ETIQUETA -->
      <div id="acur-troca" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <h3 class="text-sm font-bold text-white">Possíveis Trocas de Etiqueta (Produtos com Descrições e Saldos Invertidos)</h3>
          <p class="text-xs text-slate-400">Produtos semelhantes etiquetados erroneamente na entrada de mercadoria</p>
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[450px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">SKU WMS (Sobra)</th>
                  <th class="py-2.5 px-3">Descrição WMS</th>
                  <th class="py-2.5 px-3 text-right">Saldo WMS</th>
                  <th class="py-2.5 px-3">SKU SN (Falta)</th>
                  <th class="py-2.5 px-3">Descrição SN</th>
                  <th class="py-2.5 px-3 text-right">Saldo SN</th>
                  <th class="py-2.5 px-3 text-center">Similaridade</th>
                </tr>
              </thead>
              <tbody id="tbody-acur-troca" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 5: SEM ESTOQUE WMS -->
      <div id="acur-sem-wms" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <h3 class="text-sm font-bold text-white">Itens Sem Estoque no WMS mas com Saldo no SN</h3>
          <p class="text-xs text-slate-400">Produtos que o ERP S7 acusa ter saldo físico, mas o WMS não possui endereçamento</p>
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[450px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Código</th>
                  <th class="py-2.5 px-3">Descrição do Produto</th>
                  <th class="py-2.5 px-3">Filial</th>
                  <th class="py-2.5 px-3 text-right">Saldo no SN</th>
                  <th class="py-2.5 px-3 text-right">Saldo no WMS</th>
                </tr>
              </thead>
              <tbody id="tbody-acur-sem-wms" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 6: SEM ESTOQUE SN -->
      <div id="acur-sem-sn" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <h3 class="text-sm font-bold text-white">Itens Sem Estoque no SN mas com Saldo no WMS (Sobras Físicas)</h3>
          <p class="text-xs text-slate-400">Produtos que estão fisicamente no WMS mas zerados no ERP S7</p>
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[450px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Código</th>
                  <th class="py-2.5 px-3">Descrição do Produto</th>
                  <th class="py-2.5 px-3">Filial</th>
                  <th class="py-2.5 px-3 text-right">Saldo no WMS</th>
                  <th class="py-2.5 px-3 text-right">Saldo no SN</th>
                </tr>
              </thead>
              <tbody id="tbody-acur-sem-sn" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 7: COMPARATIVO 6 LOJAS -->
      <div id="acur-6lojas" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <h3 class="text-sm font-bold text-white">Comparativo das 6 Filiais GW Wireless</h3>
          <p class="text-xs text-slate-400">Parametrização oficial: Matriz (1 e 8), Goiânia (6 e 90), Brasília (9 e 91), Palmas (10 e 11), Marabá (7 e 92), São Luís (14)</p>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="cards-6lojas">
            <!-- Injected via JS -->
          </div>
        </div>
      </div>

    </section>

    <!-- ======================================================== -->
    <!-- VIEW 3: CUSTO DE TRANSPORTE & FROTAS (OPÇÃO 1)           -->
    <!-- ======================================================== -->
    <section id="view-transporte" class="main-view hidden space-y-6">
      
      <!-- View Header with Back Button -->
      <div class="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div class="flex items-center space-x-3">
          <button onclick="navigateTo('view-hub')" class="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition" title="Voltar ao Hub">
            <i class="fa-solid fa-arrow-left"></i>
          </button>
          <div>
            <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-truck-ramp-box text-indigo-400"></i>
              <span>Custo de Transporte & Romaneios (Opção 1)</span>
            </h2>
            <p class="text-xs text-slate-400">Programação de Viagens, Romaneios Master, Entregas Gota a Gota e Preparação para Telemetria</p>
          </div>
        </div>

        <!-- Sub Tabs Selector -->
        <div class="flex flex-wrap gap-2">
          <button onclick="switchTransporteTab('transp-romaneios')" id="btn-transp-romaneios" class="sub-tab-btn active px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-route mr-1.5 text-blue-400"></i>
            <span>1. Romaneios Master (88)</span>
          </button>
          <button onclick="switchTransporteTab('transp-entregas')" id="btn-transp-entregas" class="sub-tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-location-dot mr-1.5 text-emerald-400"></i>
            <span>2. Entregas Gota a Gota (180)</span>
          </button>
          <button onclick="switchTransporteTab('transp-frota')" id="btn-transp-frota" class="sub-tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-truck text-amber-400 mr-1.5"></i>
            <span>3. DRE Frota por Placa</span>
          </button>
          <button onclick="switchTransporteTab('transp-telemetria')" id="btn-transp-telemetria" class="sub-tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            <i class="fa-solid fa-video mr-1.5 text-rose-400"></i>
            <span>4. Telemetria Wisevia (37 Alarmes) & TI5</span>
          </button>
        </div>
      </div>

      <!-- TRANSPORTE SUB-PANEL 1: ROMANEIOS MASTER -->
      <div id="transp-romaneios" class="transp-sub-panel space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white">Viagens Programadas: powerbi.vw_romaneios_master_completa</h3>
              <p class="text-xs text-slate-400">Controle das viagens geradas no sistema de logística do Gabriel Joffre</p>
            </div>
            <input type="text" id="search-transp-rom" oninput="renderTableRomaneios()" placeholder="Filtrar romaneio, placa, motorista..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[500px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Romaneio</th>
                  <th class="py-2.5 px-3">Status</th>
                  <th class="py-2.5 px-3">Filial Origem</th>
                  <th class="py-2.5 px-3">Previsão Saída</th>
                  <th class="py-2.5 px-3">Placa Veículo</th>
                  <th class="py-2.5 px-3">Modelo</th>
                  <th class="py-2.5 px-3">Motorista</th>
                  <th class="py-2.5 px-3 text-right">Qtd Pedidos</th>
                  <th class="py-2.5 px-3 text-right">Transferências</th>
                  <th class="py-2.5 px-3">Pedidos S7 Embarcados</th>
                </tr>
              </thead>
              <tbody id="tbody-transp-rom" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TRANSPORTE SUB-PANEL 2: ENTREGAS GOTA A GOTA -->
      <div id="transp-entregas" class="transp-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white">Sequência de Entregas: powerbi.vw_romaneio_pedidos_detalhada</h3>
              <p class="text-xs text-slate-400">Rastreamento da ordem de parada do caminhão, cliente, destino e canhoto</p>
            </div>
            <input type="text" id="search-transp-ent" oninput="renderTableEntregas()" placeholder="Buscar cliente, cidade, pedido..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[500px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Romaneio</th>
                  <th class="py-2.5 px-3">Parada</th>
                  <th class="py-2.5 px-3">Pedido S7</th>
                  <th class="py-2.5 px-3">Ticket GLPI</th>
                  <th class="py-2.5 px-3">Cliente</th>
                  <th class="py-2.5 px-3">Cidade Destino</th>
                  <th class="py-2.5 px-3">Motorista</th>
                  <th class="py-2.5 px-3">Placa</th>
                  <th class="py-2.5 px-3">Status Entrega</th>
                  <th class="py-2.5 px-3">Recebido Por</th>
                </tr>
              </thead>
              <tbody id="tbody-transp-ent" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TRANSPORTE SUB-PANEL 3: DRE FROTA -->
      <div id="transp-frota" class="transp-sub-panel hidden space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 uppercase font-semibold">Custo Total Consolidado</span>
            <div class="text-2xl font-extrabold text-white mt-1">R$ 2.189.571,88</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 uppercase font-semibold">Combustível (Gasola)</span>
            <div class="text-2xl font-extrabold text-amber-400 mt-1">R$ 1.575.743,27</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 uppercase font-semibold">Manutenções & Peças</span>
            <div class="text-2xl font-extrabold text-rose-400 mt-1">R$ 417.632,76</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 uppercase font-semibold">Pedágios (Sem Parar)</span>
            <div class="text-2xl font-extrabold text-purple-400 mt-1">R$ 196.195,85</div>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <h3 class="text-sm font-bold text-white">Raio-X de Custos por Placa (25 Veículos)</h3>
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[450px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Placa</th>
                  <th class="py-2.5 px-3">Modelo</th>
                  <th class="py-2.5 px-3">Filial</th>
                  <th class="py-2.5 px-3">Status</th>
                  <th class="py-2.5 px-3 text-right">Combustível (R$)</th>
                  <th class="py-2.5 px-3 text-right">Manutenção (R$)</th>
                  <th class="py-2.5 px-3 text-right">Pedágio (R$)</th>
                  <th class="py-2.5 px-3 text-right font-bold text-blue-400">Custo Total (R$)</th>
                  <th class="py-2.5 px-3 text-right">Consumo Km/L</th>
                  <th class="py-2.5 px-3 text-right">Custo R$/Km</th>
                </tr>
              </thead>
              <tbody id="tbody-transp-frota" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TRANSPORTE SUB-PANEL 4: TELEMETRIA WISEVIA (37 ALARMES) & TI5 -->
      <div id="transp-telemetria" class="transp-sub-panel hidden space-y-6">
        
        <!-- Status Box Waiting for API -->
        <div class="glass-card rounded-2xl p-6 border border-amber-500/30 bg-amber-950/20 space-y-3">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg shrink-0">
              <i class="fa-solid fa-satellite-dish animate-pulse"></i>
            </div>
            <div>
              <h4 class="text-sm font-bold text-white">Central de Telemetria e Monitoramento de Condução</h4>
              <p class="text-xs text-amber-300/80">
                Aguardando chaves de API da plataforma <strong class="text-white">TI5 (Rastreamento / Km / GPS)</strong> e <strong class="text-white">Wisevia (Câmeras Embarcadas & 37 Alarmes)</strong> para ativação das transmissões em tempo real.
              </p>
            </div>
          </div>
          <p class="text-xs text-slate-300">
            Abaixo já estruturamos o catálogo com as <strong>37 regras de alarme da Wisevia</strong> que iremos correlacionar com cada motorista, veículo e viagem (condução segura, cálculo de Km vs Litros e histórico de infrações).
          </p>
        </div>

        <!-- 37 Wisevia Alarms Catalog -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-shield-halved text-rose-400"></i>
                <span>Catálogo de Alertas Wisevia (37 Tipos Parametrizados)</span>
              </h3>
              <p class="text-xs text-slate-400">Regras disparadas pelas câmeras de cabine e sensores dos veículos</p>
            </div>
            <input type="text" id="search-alarmes" oninput="renderTableAlarmes()" placeholder="Buscar alarme ou categoria..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[450px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">ID</th>
                  <th class="py-2.5 px-3">Descrição do Alarme / Evento</th>
                  <th class="py-2.5 px-3">Categoria</th>
                  <th class="py-2.5 px-3">Severidade</th>
                  <th class="py-2.5 px-3">Impacto na Pontuação do Motorista</th>
                </tr>
              </thead>
              <tbody id="tbody-alarmes" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </section>

  </main>

  <!-- FOOTER -->
  <footer class="glass-card mt-auto px-6 py-4 border-t border-slate-800 text-center text-xs text-slate-500 flex flex-wrap justify-between items-center gap-4">
    <div>GW Wireless © 2026 - Performance Operacional Logístico</div>
    <div class="flex items-center space-x-4">
      <span>WMS: <strong class="text-slate-400">sistemaestoque</strong></span>
      <span>PostgreSQL: <strong class="text-slate-400">172.21.10.42:5432</strong></span>
      <span>GLPI: <strong class="text-slate-400">MySQL glpidb</strong></span>
    </div>
  </footer>

  <!-- DATA & LOGIC -->
  <script>
    const DATA = {json_payload};

    // Formatters
    const fmtMoeda = val => new Intl.NumberFormat('pt-BR', {{ style: 'currency', currency: 'BRL' }}).format(val || 0);
    const fmtNum = (val, dec=0) => new Intl.NumberFormat('pt-BR', {{ minimumFractionDigits: dec, maximumFractionDigits: dec }}).format(val || 0);

    // Navigation
    function navigateTo(viewId) {{
      document.querySelectorAll('.main-view').forEach(v => v.classList.add('hidden'));
      const target = document.getElementById(viewId);
      if (target) target.classList.remove('hidden');

      const breadcrumb = document.getElementById('header-breadcrumb');
      if (viewId === 'view-hub') {{
        breadcrumb.textContent = 'Performance Operacional Logístico • Hub Principal';
      }} else if (viewId === 'view-performance') {{
        breadcrumb.textContent = 'Performance Operacional Logístico • 1. Performance da Equipe';
      }} else if (viewId === 'view-acuracidade') {{
        breadcrumb.textContent = 'Performance Operacional Logístico • 2. Acuracidade de Estoque';
      }} else if (viewId === 'view-transporte') {{
        breadcrumb.textContent = 'Performance Operacional Logístico • 3. Custo de Transporte & Frotas';
      }}
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // Sub-tab switchers
    function switchPerformanceTab(tabId) {{
      document.querySelectorAll('.perf-sub-panel').forEach(p => p.classList.add('hidden'));
      document.getElementById(tabId).classList.remove('hidden');
      document.querySelectorAll('#view-performance .sub-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('btn-' + tabId).classList.add('active');
    }}

    function switchAcuracidadeTab(tabId) {{
      document.querySelectorAll('.acur-sub-panel').forEach(p => p.classList.add('hidden'));
      document.getElementById(tabId).classList.remove('hidden');
      document.querySelectorAll('#view-acuracidade .sub-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('btn-' + tabId).classList.add('active');
    }}

    function switchTransporteTab(tabId) {{
      document.querySelectorAll('.transp-sub-panel').forEach(p => p.classList.add('hidden'));
      document.getElementById(tabId).classList.remove('hidden');
      document.querySelectorAll('#view-transporte .sub-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('btn-' + tabId).classList.add('active');
    }}

    // Initializer
    document.addEventListener('DOMContentLoaded', () => {{
      renderPerformanceView();
      renderAcuracidadeView();
      renderTransporteView();
    }});

    // ==========================================
    // RENDER PERFORMANCE VIEW
    // ==========================================
    function renderPerformanceView() {{
      const sep = DATA.team.separacao;
      
      // Podium Top 3
      const podium = document.getElementById('podium-separacao');
      if (podium && sep.length >= 3) {{
        const medals = [
          {{ rank: '1º Lugar', medal: '🥇 Ouro', color: 'border-amber-500/40 bg-amber-500/5 text-amber-400' }},
          {{ rank: '2º Lugar', medal: '🥈 Prata', color: 'border-slate-400/40 bg-slate-400/5 text-slate-300' }},
          {{ rank: '3º Lugar', medal: '🥉 Bronze', color: 'border-orange-500/40 bg-orange-500/5 text-orange-400' }}
        ];
        podium.innerHTML = '';
        for (let i = 0; i < 3; i++) {{
          const u = sep[i];
          const m = medals[i];
          podium.innerHTML += `
            <div class="glass-card rounded-2xl p-5 border ${{m.color}} flex items-center space-x-4">
              <div class="text-3xl font-extrabold">${{i+1}}º</div>
              <div class="flex-1">
                <span class="text-xs font-semibold uppercase tracking-wider block">${{m.medal}}</span>
                <h4 class="text-base font-bold text-white">${{u.usuario}}</h4>
                <div class="mt-2 flex items-center justify-between text-xs text-slate-300">
                  <span><strong>${{fmtNum(u.pedidos)}}</strong> pedidos</span>
                  <span><strong>${{fmtNum(u.unidades)}}</strong> unidades</span>
                </div>
              </div>
            </div>
          `;
        }}
      }}

      renderTableSeparacao();
      renderTableArmazenagem();
      renderTableTransferencias();
      renderTableRecebimento();
    }}

    function renderTableSeparacao() {{
      const term = (document.getElementById('search-perf-sep')?.value || '').toLowerCase().trim();
      const list = DATA.team.separacao.filter(u => !term || u.usuario.toLowerCase().includes(term));
      const tbody = document.getElementById('tbody-perf-sep');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach((u, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-4 font-bold text-slate-400">#${{idx + 1}}</td>
          <td class="py-2.5 px-4 font-semibold text-white">${{u.usuario}}</td>
          <td class="py-2.5 px-4 text-right font-extrabold text-blue-400">${{fmtNum(u.pedidos)}}</td>
          <td class="py-2.5 px-4 text-right text-slate-300">${{fmtNum(u.itens)}}</td>
          <td class="py-2.5 px-4 text-right font-medium text-amber-400">${{fmtNum(u.unidades)}}</td>
          <td class="py-2.5 px-4 text-center text-slate-400 text-xs">${{u.primeiro ? u.primeiro.substring(0, 10) : '-'}}</td>
          <td class="py-2.5 px-4 text-center text-slate-400 text-xs">${{u.ultimo ? u.ultimo.substring(0, 10) : '-'}}</td>
          <td class="py-2.5 px-4 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{u.pedidos > 200 ? 'bg-emerald-500/20 text-emerald-400' : u.pedidos > 50 ? 'bg-blue-500/20 text-blue-400' : 'bg-slate-700 text-slate-300'}}">
              ${{u.pedidos > 200 ? 'Alta Performance' : u.pedidos > 50 ? 'Constante' : 'Apoio'}}
            </span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableArmazenagem() {{
      const term = (document.getElementById('search-perf-arm')?.value || '').toLowerCase().trim();
      const list = DATA.team.armazenagem.filter(u => !term || u.usuario.toLowerCase().includes(term) || (u.login && u.login.toLowerCase().includes(term)));
      const tbody = document.getElementById('tbody-perf-arm');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach((u, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-4 font-bold text-slate-400">#${{idx + 1}}</td>
          <td class="py-2.5 px-4 font-semibold text-white">${{u.usuario}}</td>
          <td class="py-2.5 px-4 font-mono text-slate-400">${{u.login || '-'}}</td>
          <td class="py-2.5 px-4 text-right font-extrabold text-emerald-400">${{fmtNum(u.movimentacoes)}}</td>
          <td class="py-2.5 px-4 text-right text-slate-300">${{fmtNum(u.skus)}}</td>
          <td class="py-2.5 px-4 text-right font-medium text-amber-400">${{fmtNum(u.unidades)}}</td>
          <td class="py-2.5 px-4 text-center text-slate-400 text-xs">${{u.ultimo ? u.ultimo.substring(0, 16) : '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableTransferencias() {{
      const term = (document.getElementById('search-perf-transf')?.value || '').toLowerCase().trim();
      const list = DATA.team.transferencias.filter(u => !term || u.usuario.toLowerCase().includes(term) || (u.login && u.login.toLowerCase().includes(term)));
      const tbody = document.getElementById('tbody-perf-transf');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach((u, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-4 font-bold text-slate-400">#${{idx + 1}}</td>
          <td class="py-2.5 px-4 font-semibold text-white">${{u.usuario}}</td>
          <td class="py-2.5 px-4 font-mono text-slate-400">${{u.login || '-'}}</td>
          <td class="py-2.5 px-4 text-right font-extrabold text-purple-400">${{fmtNum(u.movimentacoes)}}</td>
          <td class="py-2.5 px-4 text-right text-slate-300">${{fmtNum(u.skus)}}</td>
          <td class="py-2.5 px-4 text-right font-medium text-amber-400">${{fmtNum(u.unidades)}}</td>
          <td class="py-2.5 px-4 text-center text-slate-400 text-xs">${{u.ultimo ? u.ultimo.substring(0, 16) : '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableRecebimento() {{
      const tbody = document.getElementById('tbody-perf-rec');
      if (!tbody) return;
      tbody.innerHTML = '';
      DATA.team.recebimento.forEach(u => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-4 font-semibold text-white">${{u.usuario}}</td>
          <td class="py-2.5 px-4 text-right font-bold text-cyan-400">${{fmtNum(u.cargas)}}</td>
          <td class="py-2.5 px-4 text-right text-slate-300">${{fmtNum(u.itens)}}</td>
          <td class="py-2.5 px-4 text-right text-slate-400">${{fmtNum(u.esperado)}}</td>
          <td class="py-2.5 px-4 text-right font-bold text-emerald-400">${{fmtNum(u.conferido)}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // ==========================================
    // RENDER ACURACIDADE VIEW
    // ==========================================
    function renderAcuracidadeView() {{
      renderTableReservas();
      renderTableCompensacao();
      renderTableTroca();
      renderTableSemWms();
      renderTableSemSn();
      renderCards6Lojas();
    }}

    function renderTableReservas() {{
      const term = (document.getElementById('search-acur-res')?.value || '').toLowerCase().trim();
      const list = DATA.reservas.reservas.filter(r => {{
        if (!term) return true;
        return (r.num_pedido && String(r.num_pedido).includes(term)) ||
               (r.produto && r.produto.toLowerCase().includes(term)) ||
               (r.obs_pedido && r.obs_pedido.toLowerCase().includes(term));
      }}).slice(0, 150);

      const tbody = document.getElementById('tbody-acur-res');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(r => {{
        const isFuro = r.is_furo;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition ' + (isFuro ? 'bg-rose-950/20' : '');
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold ${{isFuro ? 'text-rose-400' : 'text-blue-400'}}">#${{r.num_pedido}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{isFuro ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-slate-800 text-slate-300'}}">
              ${{isFuro ? 'FURO DE ESTOQUE' : 'Reserva Normal'}}
            </span>
          </td>
          <td class="py-2.5 px-3 font-mono text-slate-400">${{r.cod_produto}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs">${{r.produto}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-amber-400">${{fmtNum(r.qtd_reservada)}}</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{fmtMoeda(r.preco_unitario)}}</td>
          <td class="py-2.5 px-3 text-right font-extrabold text-white">${{fmtMoeda(r.valor_total_item)}}</td>
          <td class="py-2.5 px-3 text-xs text-slate-400 truncate max-w-xs">${{r.obs_pedido || '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableCompensacao() {{
      const tbody = document.getElementById('tbody-acur-comp');
      if (!tbody) return;
      tbody.innerHTML = '';
      (DATA.stock.top_matches || []).slice(0, 50).forEach(m => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{m.cod_wms || '-'}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs">${{m.desc_wms}}</td>
          <td class="py-2.5 px-3 text-emerald-400 font-semibold">MATRIZ (WMS)</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">+${{fmtNum(m.saldo_wms)}}</td>
          <td class="py-2.5 px-3 text-rose-400 font-semibold">FILIAL (SN)</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">-${{fmtNum(m.saldo_sn)}}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/20 text-blue-400">Transferir & Regularizar</span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableTroca() {{
      const tbody = document.getElementById('tbody-troca') || document.getElementById('tbody-acur-troca');
      if (!tbody) return;
      tbody.innerHTML = '';
      (DATA.stock.top_matches || []).slice(0, 50).forEach(m => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-emerald-400">${{m.cod_wms}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs">${{m.desc_wms}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">${{fmtNum(m.saldo_wms)}}</td>
          <td class="py-2.5 px-3 font-mono text-rose-400">${{m.cod_sn}}</td>
          <td class="py-2.5 px-3 text-slate-300 truncate max-w-xs">${{m.desc_sn}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">${{fmtNum(m.saldo_sn)}}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-400">${{(m.score * 100).toFixed(0)}}% Match</span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableSemWms() {{
      const tbody = document.getElementById('tbody-acur-sem-wms');
      if (!tbody) return;
      tbody.innerHTML = '';
      (DATA.stock.sem_wms || []).slice(0, 100).forEach(i => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{i.codigo}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs">${{i.descricao}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{i.filial || 'MATRIZ'}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">${{fmtNum(i.saldo_sn)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">0</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableSemSn() {{
      const tbody = document.getElementById('tbody-acur-sem-sn');
      if (!tbody) return;
      tbody.innerHTML = '';
      (DATA.stock.sem_sn || []).slice(0, 100).forEach(i => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{i.codigo}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs">${{i.descricao}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{i.filial || 'MATRIZ'}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">${{fmtNum(i.saldo_wms)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">0</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderCards6Lojas() {{
      const container = document.getElementById('cards-6lojas');
      if (!container) return;
      container.innerHTML = '';
      DATA.stock.filiais.forEach(f => {{
        container.innerHTML += `
          <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-white">${{f.nome}}</h4>
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/20 text-blue-400">Lojas: ${{f.lojas.join(', ')}}</span>
            </div>
            <div class="text-xs text-slate-400 flex items-center justify-between pt-2 border-t border-slate-800">
              <span>SKUs Auditados:</span>
              <span class="font-bold text-white">${{fmtNum(f.total_itens)}}</span>
            </div>
            <div class="text-xs text-slate-400 flex items-center justify-between">
              <span>Saldo Físico Unidades:</span>
              <span class="font-bold text-emerald-400">${{fmtNum(f.total_unidades)}} un</span>
            </div>
          </div>
        `;
      }});
    }}

    // ==========================================
    // RENDER TRANSPORTE VIEW
    // ==========================================
    function renderTransporteView() {{
      renderTableRomaneios();
      renderTableEntregas();
      renderTableFrota();
      renderTableAlarmes();
    }}

    function renderTableRomaneios() {{
      const term = (document.getElementById('search-transp-rom')?.value || '').toLowerCase().trim();
      const list = DATA.team.romaneios_master.filter(r => {{
        if (!term) return true;
        return (r.numero && String(r.numero).includes(term)) ||
               (r.placa && r.placa.toLowerCase().includes(term)) ||
               (r.motorista && r.motorista.toLowerCase().includes(term)) ||
               (r.filial && r.filial.toLowerCase().includes(term));
      }});

      const tbody = document.getElementById('tbody-transp-rom');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(r => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold text-white">#${{r.numero}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{r.status === 'Finalizado' ? 'bg-emerald-500/20 text-emerald-400' : r.status === 'Cancelado' ? 'bg-rose-500/20 text-rose-400' : 'bg-blue-500/20 text-blue-400'}}">
              ${{r.status}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${{r.filial}}</td>
          <td class="py-2.5 px-3 text-slate-400 text-xs">${{r.previsao_saida || '-'}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-amber-400">${{r.placa || '-'}}</td>
          <td class="py-2.5 px-3 text-slate-300 text-xs">${{r.modelo || '-'}}</td>
          <td class="py-2.5 px-3 text-white text-xs">${{r.motorista || '-'}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-cyan-400">${{r.pedidos}}</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{r.transferencias}}</td>
          <td class="py-2.5 px-3 font-mono text-slate-400 text-xs truncate max-w-xs">${{r.pedidos_s7 || '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableEntregas() {{
      const term = (document.getElementById('search-transp-ent')?.value || '').toLowerCase().trim();
      const list = DATA.team.romaneios_detalhe.filter(e => {{
        if (!term) return true;
        return (e.cliente && e.cliente.toLowerCase().includes(term)) ||
               (e.cidade && e.cidade.toLowerCase().includes(term)) ||
               (e.pedido_s7 && String(e.pedido_s7).includes(term)) ||
               (e.placa && e.placa.toLowerCase().includes(term));
      }});

      const tbody = document.getElementById('tbody-transp-ent');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(e => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold text-white">#${{e.numero}}</td>
          <td class="py-2.5 px-3 font-bold text-amber-400 text-center">${{e.ordem}}º</td>
          <td class="py-2.5 px-3 font-mono text-blue-400 font-semibold">${{e.pedido_s7}}</td>
          <td class="py-2.5 px-3 text-slate-400">#${{e.ticket_glpi}}</td>
          <td class="py-2.5 px-3 text-white font-medium truncate max-w-xs">${{e.cliente}}</td>
          <td class="py-2.5 px-3 text-cyan-400 font-semibold">${{e.cidade || 'N/D'}}</td>
          <td class="py-2.5 px-3 text-slate-300 text-xs">${{e.motorista || '-'}}</td>
          <td class="py-2.5 px-3 font-mono text-slate-300">${{e.placa || '-'}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{e.status_entrega === 'Entregue' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-300'}}">
              ${{e.status_entrega}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-xs text-slate-300">${{e.recebido_por || '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableFrota() {{
      const tbody = document.getElementById('tbody-transp-frota');
      if (!tbody) return;
      tbody.innerHTML = '';

      DATA.frota.veiculos.forEach(v => {{
        const cKm = v.km_rodado > 0 ? (v.custo_total / v.km_rodado) : 0;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold text-white">${{v.placa}}</td>
          <td class="py-2.5 px-3 text-slate-300 text-xs">${{v.apelido || v.modelo}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{v.filial}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{v.status === 'ATIVO' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}}">
              ${{v.status}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-right font-medium text-amber-400">${{fmtMoeda(v.gasto_combustivel)}}</td>
          <td class="py-2.5 px-3 text-right font-medium text-rose-400">${{fmtMoeda(v.gasto_manutencao)}}</td>
          <td class="py-2.5 px-3 text-right font-medium text-purple-400">${{fmtMoeda(v.gasto_pedagio)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-blue-400">${{fmtMoeda(v.custo_total)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-cyan-400">${{v.media_kml > 0 ? v.media_kml.toFixed(2) : '-'}}</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{cKm > 0 ? fmtMoeda(cKm) : '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableAlarmes() {{
      const term = (document.getElementById('search-alarmes')?.value || '').toLowerCase().trim();
      const list = DATA.alarmes_wisevia.filter(a => {{
        if (!term) return true;
        return a.alarme.toLowerCase().includes(term) || a.categoria.toLowerCase().includes(term);
      }});

      const tbody = document.getElementById('tbody-alarmes');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(a => {{
        const isCrit = a.severidade === 'Crítica';
        const isAlta = a.severidade === 'Alta';
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2 px-3 font-mono text-slate-400">${{a.id}}</td>
          <td class="py-2 px-3 font-bold text-white">${{a.alarme}}</td>
          <td class="py-2 px-3 text-slate-300">${{a.categoria}}</td>
          <td class="py-2 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{isCrit ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : isAlta ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400'}}">
              ${{a.severidade}}
            </span>
          </td>
          <td class="py-2 px-3 text-slate-400 text-xs">
            ${{isCrit ? 'Perda grave de pontuação (-15 pts)' : isAlta ? 'Penalidade média (-10 pts)' : 'Registro informativo (-2 pts)'}}
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Export functions
    function exportCurrentView() {{
      const wb = XLSX.utils.book_new();
      
      // Separacao
      const wsSep = XLSX.utils.json_to_sheet(DATA.team.separacao);
      XLSX.utils.book_append_sheet(wb, wsSep, "Ranking_Separacao");

      // Romaneios
      const wsRom = XLSX.utils.json_to_sheet(DATA.team.romaneios_master);
      XLSX.utils.book_append_sheet(wb, wsRom, "Romaneios_Master");

      // Entregas
      const wsEnt = XLSX.utils.json_to_sheet(DATA.team.romaneios_detalhe);
      XLSX.utils.book_append_sheet(wb, wsEnt, "Entregas_Detalhada");

      // Frota
      const wsFrota = XLSX.utils.json_to_sheet(DATA.frota.veiculos);
      XLSX.utils.book_append_sheet(wb, wsFrota, "Frota_Custos");

      XLSX.writeFile(wb, "GW_Performance_Operacional_Logistico.xlsx");
    }}

    function captureCurrentSlide() {{
      const target = document.getElementById('portal-capture-area');
      html2canvas(target, {{ backgroundColor: '#0b1120', scale: 2 }}).then(canvas => {{
        const link = document.createElement('a');
        link.download = 'GW_Slide_Performance_Logistica.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
      }});
    }}
  </script>
</body>
</html>
"""

target_path = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Portal generated successfully at: {target_path}")

# Copy to artifact dir
artifact_dir = 'C:/Users/renan.alves/.gemini/antigravity/brain/43bb33b6-6367-463c-94d9-1306168eb162'
artifact_path = os.path.join(artifact_dir, 'dashboard_performance_operacional_logistico.html')
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Artifact created at: {artifact_path}")
