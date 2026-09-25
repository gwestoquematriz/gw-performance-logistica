import os
import json

print("Reading unified_logistics_complete.json...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/unified_logistics_complete.json', encoding='utf-8') as f:
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
      background-color: #080e1a;
      color: #f8fafc;
    }}
    .custom-scroll::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scroll::-webkit-scrollbar-track {{
      background: #0f172a;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 3px;
    }}
    .glass-card {{
      background: rgba(15, 23, 42, 0.8);
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
    .store-chip.active {{
      background-color: #2563eb !important;
      color: #ffffff !important;
      border-color: #60a5fa !important;
      box-shadow: 0 0 10px rgba(37, 99, 235, 0.4);
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
            Performance Operacional Logístico
          </span>
        </div>
        <p class="text-xs text-slate-400" id="header-breadcrumb">Hub Principal &bull; Escolha o Módulo Operacional</p>
      </div>
    </div>

    <!-- Live System Indicators -->
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
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20" title="Hub Frota e Romaneios">
        <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
        <span class="font-medium">Hub PG: 88 Romaneios</span>
      </div>
    </div>

    <!-- Navigation Shortcuts -->
    <div class="flex items-center space-x-2">
      <button onclick="navigateTo('view-hub')" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition flex items-center space-x-1.5 border border-slate-700">
        <i class="fa-solid fa-house"></i>
        <span>Menu Principal</span>
      </button>
      <button onclick="exportCurrentView()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition flex items-center space-x-1.5 shadow-sm">
        <i class="fa-solid fa-file-excel"></i>
        <span>Exportar Excel</span>
      </button>
      <button onclick="captureCurrentSlide()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center space-x-1.5 shadow-sm">
        <i class="fa-solid fa-camera"></i>
        <span>Gerar Slide (PNG)</span>
      </button>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="flex-1 p-6 space-y-6 max-w-[1750px] mx-auto w-full" id="portal-capture-area">

    <!-- ======================================================== -->
    <!-- VIEW 0: HUB INICIAL COM 3 CAMPOS PRINCIPAIS              -->
    <!-- ======================================================== -->
    <section id="view-hub" class="main-view space-y-8">
      
      <!-- Welcome Hero -->
      <div class="glass-card rounded-3xl p-8 border border-slate-800 relative overflow-hidden bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900">
        <div class="relative z-10 max-w-3xl space-y-3">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-medium">
            <i class="fa-solid fa-circle-check"></i>
            <span>Painel Integrado de Performance Operacional Logístico</span>
          </div>
          <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Gestão Estratégica GW Wireless
          </h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            Selecione uma das três áreas abaixo para auditar a produtividade da equipe, confrontar a acuracidade de estoque nas 6 lojas ou analisar a viabilidade e custos do transporte.
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
                WMS Operacional
              </span>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white group-hover:text-blue-400 transition">
                Performance da Equipe
              </h3>
              <p class="text-xs text-slate-400 mt-1">
                Produtividade dos operadores com rankings de separação de pedidos, armazenagem e transferências.
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
                <span>Quem Mais Separou Pedidos (Ranking)</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-dolly text-cyan-400 text-[10px]"></i>
                <span>Quem Mais Armazenou Produtos (Entradas)</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-arrow-right-arrow-left text-purple-400 text-[10px]"></i>
                <span>Quem Mais Fez Transferências (Saídas)</span>
              </li>
            </ul>
          </div>

          <div class="pt-5 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-blue-400 group-hover:translate-x-1 transition">
            <span>Abrir Performance da Equipe</span>
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
                Auditoria 6 Lojas
              </span>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white group-hover:text-emerald-400 transition">
                Acuracidade de Estoque
              </h3>
              <p class="text-xs text-slate-400 mt-1">
                Confronto de saldos WMS vs SN, Reservas & Furos por DAV e compensação com status WMS Maior em.
              </p>
            </div>
            
            <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-center">
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">SKUs</span>
                <span class="font-extrabold text-emerald-400 text-sm">4.242</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Reservas</span>
                <span class="font-extrabold text-blue-400 text-sm">831 DAVs</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Furos</span>
                <span class="font-extrabold text-rose-400 text-sm">121 DAVs</span>
              </div>
            </div>

            <ul class="text-xs text-slate-300 space-y-1.5 pt-1">
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-triangle-exclamation text-rose-400 text-[10px]"></i>
                <span>Reservas & Furos de Estoque com Loja com Sobra</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-tags text-amber-400 text-[10px]"></i>
                <span>Troca de Etiqueta (Produtos Similares Invertidos)</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-store text-cyan-400 text-[10px]"></i>
                <span>Filtro Multi-Loja (Selecione 1 ou Mais Filiais)</span>
              </li>
            </ul>
          </div>

          <div class="pt-5 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-emerald-400 group-hover:translate-x-1 transition">
            <span>Abrir Acuracidade de Estoque</span>
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
                Frotas & Viabilidade
              </span>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white group-hover:text-indigo-400 transition">
                Custo de Transporte & Frotas
              </h3>
              <p class="text-xs text-slate-400 mt-1">
                Programação de romaneios, entregas gota a gota, DRE da frota e preparação para telemetria.
              </p>
            </div>
            
            <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-center">
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Frota</span>
                <span class="font-extrabold text-indigo-400 text-sm">25 Veículos</span>
              </div>
              <div class="p-2 rounded-lg bg-slate-900/60">
                <span class="block text-[10px] text-slate-400 uppercase font-semibold">Custo Total</span>
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
                <span>Romaneios Master e Sequência de Entregas</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-gas-pump text-amber-400 text-[10px]"></i>
                <span>Combustível Gasola, Sem Parar e GLPI</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-satellite-dish text-rose-400 text-[10px]"></i>
                <span>Preparado para APIs TI5 & Wisevia (37 Alarmes)</span>
              </li>
            </ul>
          </div>

          <div class="pt-5 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-indigo-400 group-hover:translate-x-1 transition">
            <span>Abrir Transporte & Frotas</span>
            <i class="fa-solid fa-arrow-right"></i>
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
          <button onclick="navigateTo('view-hub')" class="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition" title="Voltar ao Menu Principal">
            <i class="fa-solid fa-arrow-left"></i>
          </button>
          <div>
            <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-users-gear text-blue-400"></i>
              <span>Performance Operacional da Equipe</span>
            </h2>
            <p class="text-xs text-slate-400">Rankings de Separação de Pedidos, Armazenagem de Produtos e Transferências</p>
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
            <span>4. Recebimento de Mercadorias</span>
          </button>
        </div>
      </div>

      <!-- PERFORMANCE SUB-PANEL 1: SEPARAÇÃO -->
      <div id="perf-separacao" class="perf-sub-panel space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="podium-separacao">
          <!-- Injected via JS -->
        </div>

        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-ranking-star text-amber-400"></i>
                <span>Ranking Completo: Usuários que Mais Separaram Pedidos (WMS)</span>
              </h3>
              <p class="text-xs text-slate-400">Métricas acumuladas de pedidos, linhas de itens e unidades separadas</p>
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
                  <th class="py-3 px-4 text-center">Primeira Separação</th>
                  <th class="py-3 px-4 text-center">Última Separação</th>
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

      <!-- PERFORMANCE SUB-PANEL 2: ARMAZENAGEM -->
      <div id="perf-armazenagem" class="perf-sub-panel hidden space-y-6">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-dolly text-emerald-400"></i>
                <span>Ranking: Usuários que Mais Armazenaram / Deram Entrada no Estoque</span>
              </h3>
              <p class="text-xs text-slate-400">Operadores que guardaram produtos e abasteceram os endereços físicos do WMS</p>
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
                  <th class="py-3 px-4 text-right">Movimentações de Entrada</th>
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

      <!-- PERFORMANCE SUB-PANEL 3: TRANSFERÊNCIAS -->
      <div id="perf-transferencias" class="perf-sub-panel hidden space-y-6">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-arrow-right-arrow-left text-purple-400"></i>
                <span>Ranking: Usuários que Mais Realizaram Transferências / Saídas</span>
              </h3>
              <p class="text-xs text-slate-400">Movimentações de expedição e transferência entre galpões e filiais</p>
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
            <h3 class="text-sm font-bold text-white">Auditoria de Recebimento de Mercadorias e Conferência</h3>
            <p class="text-xs text-slate-400">Conferentes que receberam notas e descarregaram produtos de fornecedores</p>
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
    <!-- VIEW 2: ACURACIDADE DE ESTOQUE (COM FILTRO MULTI-LOJA)   -->
    <!-- ======================================================== -->
    <section id="view-acuracidade" class="main-view hidden space-y-6">
      
      <!-- View Header with Back Button -->
      <div class="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div class="flex items-center space-x-3">
          <button onclick="navigateTo('view-hub')" class="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition" title="Voltar ao Menu Principal">
            <i class="fa-solid fa-arrow-left"></i>
          </button>
          <div>
            <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-boxes-packing text-emerald-400"></i>
              <span>Acuracidade de Estoque & Auditoria (6 Lojas)</span>
            </h2>
            <p class="text-xs text-slate-400">Confronto WMS vs SN, Reservas & Furo de Estoque e Compensação com Status WMS Maior em</p>
          </div>
        </div>

        <!-- 7 Sub-Tabs -->
        <div class="flex flex-wrap gap-1.5">
          <button onclick="switchAcuracidadeTab('acur-reservas')" id="btn-acur-reservas" class="sub-tab-btn active px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            1. Reservas & Furo
          </button>
          <button onclick="switchAcuracidadeTab('acur-reunioes')" id="btn-acur-reunioes" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            2. Resumo Reunião
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

      <!-- MULTI-STORE FILTER BAR (SELECIONAR 1 OU MAIS LOJAS) -->
      <div class="glass-card rounded-2xl p-4 border border-slate-800 space-y-3">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <label class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
            <i class="fa-solid fa-store text-blue-400"></i>
            <span>Filtro de Lojas / Filiais (Selecione 1 ou mais simultaneamente):</span>
          </label>
          <div class="flex items-center space-x-2 text-xs">
            <button onclick="selectAllStores()" class="text-blue-400 hover:text-blue-300 underline font-medium">Selecionar Todas</button>
            <span class="text-slate-600">|</span>
            <button onclick="clearAllStores()" class="text-slate-400 hover:text-white underline font-medium">Limpar Seleção</button>
          </div>
        </div>

        <div class="flex flex-wrap gap-2" id="store-chips-container">
          <!-- Multi-select chips injected via JS -->
        </div>

        <!-- Official Balance Rule Explanation Banner -->
        <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800/80 text-xs text-slate-300 flex items-start space-x-3">
          <div class="text-blue-400 text-base mt-0.5"><i class="fa-solid fa-circle-info"></i></div>
          <div class="space-y-0.5">
            <span class="font-bold text-white block">Regra Oficial de Saldo (Conforme Diretriz Operacional):</span>
            <span>
              O <strong>Saldo SN (Disponível + Reservado)</strong> é a <strong>referência física obrigatória</strong> que deve constar no estoque onde alimentamos o WMS.
              Quando a coluna <em>Divergência</em> aponta status <strong>`WMS maior em (+X)`</strong>, significa que há <strong>sobra física no galpão</strong> pronta para compensar furos de outras filiais.
            </span>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 1: RESERVAS & FURO DE ESTOQUE -->
      <div id="acur-reservas" class="acur-sub-panel space-y-4">
        
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Total de Reservas (Lojas Selecionadas)</span>
            <div class="text-2xl font-extrabold text-white mt-1" id="kpi-res-total">0 DAVs</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Reservas com FURO DE ESTOQUE</span>
            <div class="text-2xl font-extrabold text-rose-400 mt-1" id="kpi-res-furos">0 DAVs</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Valor Retido em Furo</span>
            <div class="text-2xl font-extrabold text-amber-400 mt-1" id="kpi-res-valor">R$ 0,00</div>
          </div>
          <div class="glass-card rounded-xl p-4 border border-slate-800">
            <span class="text-xs text-slate-400 font-semibold uppercase">Unidades Faltantes em Furo</span>
            <div class="text-2xl font-extrabold text-cyan-400 mt-1" id="kpi-res-unidades">0 un</div>
          </div>
        </div>

        <!-- Table of Reservas & Furos with Assertive Sobras -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                <span>Reservas de Estoque & Furos com Indicação Assertiva da Loja com Sobra</span>
              </h3>
              <p class="text-xs text-slate-400">
                Avaliamos a coluna <em>Divergência</em> do WMS onde o status é <strong>WMS maior em</strong> para apontar a loja exata com sobra física
              </p>
            </div>
            <div class="flex items-center space-x-2">
              <select id="filter-apenas-furos" onchange="renderTableReservas()" class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
                <option value="TODOS">Todas as Reservas</option>
                <option value="FURO" selected>Apenas FURO DE ESTOQUE</option>
              </select>
              <input type="text" id="search-acur-res" oninput="renderTableReservas()" placeholder="Buscar pedido, SKU, observação..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
            </div>
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[520px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Pedido / DAV</th>
                  <th class="py-2.5 px-3">Filial da Reserva</th>
                  <th class="py-2.5 px-3">Status Reserva</th>
                  <th class="py-2.5 px-3">SKU</th>
                  <th class="py-2.5 px-3">Produto</th>
                  <th class="py-2.5 px-3 text-right">Qtd Reservada</th>
                  <th class="py-2.5 px-3 text-right">Valor Total (R$)</th>
                  <th class="py-2.5 px-3 text-emerald-400 font-bold bg-emerald-950/20">Loja com Sobra Física (WMS maior em)</th>
                  <th class="py-2.5 px-3">Observação Completa do Pedido</th>
                </tr>
              </thead>
              <tbody id="tbody-acur-res" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ACURACIDADE SUB-PANEL 2: RESUMO REUNIÃO -->
      <div id="acur-reunioes" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-handshake text-blue-400"></i>
              <span>Pauta Executiva & Indicadores para Reunião de Alinhamento Logístico</span>
            </h3>
            <span class="text-xs px-2.5 py-1 rounded bg-blue-500/20 text-blue-400 font-semibold" id="reuniao-filiais-badge">
              Filiais Selecionadas
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="font-bold text-rose-400 text-sm block">1. Auditoria Física dos Furos</span>
              <p class="text-slate-300 leading-relaxed">
                Auditar imediatamente os itens retidos em DAVs com "FURO DE ESTOQUE". A equipe deve bipar os endereços no WMS para validar se o material não está com etiqueta trocada ou alocado em rua divergente.
              </p>
            </div>
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="font-bold text-emerald-400 text-sm block">2. Regularização via Sobras WMS Maior</span>
              <p class="text-slate-300 leading-relaxed">
                Utilizar a coluna <strong>"WMS maior em"</strong> para identificar galpões que possuem saldo físico excedente. Emitir pedidos de transferência de abastecimento para cobrir as faltas de outras filiais.
              </p>
            </div>
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
              <span class="font-bold text-amber-400 text-sm block">3. Correção de Inversão de Etiquetas</span>
              <p class="text-slate-300 leading-relaxed">
                Casos com similaridade acima de 80% (ex: bobinas de cabo, conectores azuis/verdes) devem ser reconciliados no WMS com reetiquetagem física imediata antes da expedição.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- ACURACIDADE SUB-PANEL 3: COMPENSAÇÃO LOJAS -->
      <div id="acur-compensacao" class="acur-sub-panel hidden space-y-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <div>
              <h3 class="text-sm font-bold text-white">Compensação Entre-Lojas (Sobras WMS vs Faltas SN)</h3>
              <p class="text-xs text-slate-400">Oportunidades de transferência entre filiais baseadas na divergência física</p>
            </div>
            <input type="text" id="search-acur-comp" oninput="renderTableCompensacao()" placeholder="Buscar SKU ou produto..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[480px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Código SKU</th>
                  <th class="py-2.5 px-3">Descrição do Produto</th>
                  <th class="py-2.5 px-3 text-emerald-400 font-bold">Loja com Sobra (WMS Maior)</th>
                  <th class="py-2.5 px-3 text-right">Saldo Físico WMS</th>
                  <th class="py-2.5 px-3 text-rose-400 font-bold">Loja com Falta / Furo</th>
                  <th class="py-2.5 px-3 text-right">Saldo Referência SN</th>
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
          <div class="flex items-center justify-between flex-wrap gap-2">
            <div>
              <h3 class="text-sm font-bold text-white">Casos de Troca de Etiqueta (Produtos com Descrições e Saldos Invertidos)</h3>
              <p class="text-xs text-slate-400">Produtos com alta similaridade onde um sobra no WMS e outro falta no SN</p>
            </div>
            <input type="text" id="search-acur-troca" oninput="renderTableTroca()" placeholder="Buscar SKU ou produto..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[480px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">SKU WMS (Sobra)</th>
                  <th class="py-2.5 px-3">Descrição WMS</th>
                  <th class="py-2.5 px-3 text-right">Saldo WMS</th>
                  <th class="py-2.5 px-3">SKU SN (Falta)</th>
                  <th class="py-2.5 px-3">Descrição SN</th>
                  <th class="py-2.5 px-3 text-right">Saldo SN Referência</th>
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
          <div class="flex items-center justify-between flex-wrap gap-2">
            <div>
              <h3 class="text-sm font-bold text-white">Itens Sem Estoque no WMS mas com Saldo no SN</h3>
              <p class="text-xs text-slate-400">Produtos que o ERP S7 acusa ter saldo físico, mas o WMS não possui endereçamento</p>
            </div>
            <input type="text" id="search-acur-sem-wms" oninput="renderTableSemWms()" placeholder="Filtrar por código ou produto..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[480px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Código SKU</th>
                  <th class="py-2.5 px-3">Descrição do Produto</th>
                  <th class="py-2.5 px-3">Filial</th>
                  <th class="py-2.5 px-3 text-right font-bold text-emerald-400">Saldo no SN Referência</th>
                  <th class="py-2.5 px-3 text-right font-bold text-rose-400">Saldo Físico WMS</th>
                  <th class="py-2.5 px-3 text-center">Status</th>
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
          <div class="flex items-center justify-between flex-wrap gap-2">
            <div>
              <h3 class="text-sm font-bold text-white">Itens Sem Estoque no SN mas com Saldo no WMS (Sobras Físicas)</h3>
              <p class="text-xs text-slate-400">Produtos que estão fisicamente no WMS mas zerados no ERP S7</p>
            </div>
            <input type="text" id="search-acur-sem-sn" oninput="renderTableSemSn()" placeholder="Filtrar por código ou produto..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[480px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Código SKU</th>
                  <th class="py-2.5 px-3">Descrição do Produto</th>
                  <th class="py-2.5 px-3">Filial</th>
                  <th class="py-2.5 px-3 text-right font-bold text-emerald-400">Saldo Físico WMS</th>
                  <th class="py-2.5 px-3 text-right font-bold text-rose-400">Saldo no SN Referência</th>
                  <th class="py-2.5 px-3 text-center">Status</th>
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
          <div>
            <h3 class="text-sm font-bold text-white">Raio-X Consolidado das 6 Filiais GW Wireless</h3>
            <p class="text-xs text-slate-400">
              Parametrização oficial: Matriz (1 e 8), Goiânia (6 e 90), Brasília (9 e 91), Palmas (10 e 11), Marabá (7 e 92), São Luís (14)
            </p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="cards-6lojas-container">
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
          <button onclick="navigateTo('view-hub')" class="w-9 h-9 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition" title="Voltar ao Menu Principal">
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

  <!-- DATA ENGINE -->
  <script>
    const DATA = {json_payload};

    // State for Multi-Store selection (default: all 6 stores active)
    let selectedStoreIds = [12, 9, 8, 11, 10, 7];

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
        breadcrumb.textContent = 'Hub Principal • Escolha o Módulo Operacional';
      }} else if (viewId === 'view-performance') {{
        breadcrumb.textContent = 'Módulo 1: Performance da Equipe (Separação, Armazenagem e Transferências)';
      }} else if (viewId === 'view-acuracidade') {{
        breadcrumb.textContent = 'Módulo 2: Acuracidade de Estoque (Auditoria 6 Filiais, Reservas & Furos)';
      }} else if (viewId === 'view-transporte') {{
        breadcrumb.textContent = 'Módulo 3: Custo de Transporte & Romaneios (Frotas, Entregas e Telemetria)';
      }}
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

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

    // Multi-Store Filter Controls
    function renderStoreChips() {{
      const container = document.getElementById('store-chips-container');
      if (!container) return;
      container.innerHTML = '';

      DATA.stock_full.filiais_config.forEach(f => {{
        const isSelected = selectedStoreIds.includes(f.id);
        const btn = document.createElement('button');
        btn.id = 'chip-store-' + f.id;
        btn.className = `store-chip px-3 py-1.5 text-xs font-semibold rounded-lg transition border flex items-center space-x-1.5 ${{isSelected ? 'active bg-blue-600 text-white border-blue-400' : 'bg-slate-900 text-slate-300 border-slate-700 hover:bg-slate-800'}}`;
        btn.onclick = () => toggleStore(f.id);
        btn.innerHTML = `
          <i class="fa-solid ${{isSelected ? 'fa-square-check text-blue-300' : 'fa-square text-slate-500'}}"></i>
          <span>${{f.nome}}</span>
        `;
        container.appendChild(btn);
      }});
    }}

    function toggleStore(storeId) {{
      if (selectedStoreIds.includes(storeId)) {{
        // Don't allow removing all
        if (selectedStoreIds.length > 1) {{
          selectedStoreIds = selectedStoreIds.filter(id => id !== storeId);
        }}
      }} else {{
        selectedStoreIds.push(storeId);
      }}
      renderStoreChips();
      applyAcuracidadeFilters();
    }}

    function selectAllStores() {{
      selectedStoreIds = DATA.stock_full.filiais_config.map(f => f.id);
      renderStoreChips();
      applyAcuracidadeFilters();
    }}

    function clearAllStores() {{
      // Keep at least Matriz
      selectedStoreIds = [12];
      renderStoreChips();
      applyAcuracidadeFilters();
    }}

    function applyAcuracidadeFilters() {{
      renderAcuracidadeKPIs();
      renderTableReservas();
      renderTableCompensacao();
      renderTableTroca();
      renderTableSemWms();
      renderTableSemSn();
      renderCards6Lojas();
    }}

    // DOM Ready
    document.addEventListener('DOMContentLoaded', () => {{
      renderStoreChips();
      renderPerformanceView();
      applyAcuracidadeFilters();
      renderTransporteView();
    }});

    // ==========================================
    // RENDER PERFORMANCE VIEW
    // ==========================================
    function renderPerformanceView() {{
      const sep = DATA.team.separacao;
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
    // RENDER ACURACIDADE VIEW (WITH MULTI-STORE)
    // ==========================================
    function getFilteredReservas() {{
      return DATA.reservas.reservas.filter(r => selectedStoreIds.includes(r.filial_id));
    }}

    function getFilteredStockItems() {{
      const items = [];
      selectedStoreIds.forEach(id => {{
        const storeData = DATA.stock_full.filiais_data[String(id)];
        if (storeData && storeData.itens) {{
          storeData.itens.forEach(it => {{
            items.push({{
              ...it,
              filial_id: id,
              filial_nome: storeData.config.nome_curto,
              filial_oficial: storeData.config.nome
            }});
          }});
        }}
      }});
      return items;
    }}

    function renderAcuracidadeKPIs() {{
      const reservas = getFilteredReservas();
      const furos = reservas.filter(r => r.is_furo_estoque);
      const totalValorFuro = furos.reduce((acc, r) => acc + (r.valor_total_reservado || 0), 0);
      const totalUnidadesFuro = furos.reduce((acc, r) => acc + (r.quantidade_reservada || 0), 0);

      document.getElementById('kpi-res-total').textContent = `${{reservas.length}} DAVs`;
      document.getElementById('kpi-res-furos').textContent = `${{furos.length}} DAVs`;
      document.getElementById('kpi-res-valor').textContent = fmtMoeda(totalValorFuro);
      document.getElementById('kpi-res-unidades').textContent = `${{fmtNum(totalUnidadesFuro)}} un`;

      // Badge on meetings tab
      const badge = document.getElementById('reuniao-filiais-badge');
      if (badge) {{
        badge.textContent = `${{selectedStoreIds.length}} de 6 Lojas Selecionadas`;
      }}
    }}

    function renderTableReservas() {{
      const term = (document.getElementById('search-acur-res')?.value || '').toLowerCase().trim();
      const filtroFuro = document.getElementById('filter-apenas-furos')?.value || 'TODOS';
      
      let list = getFilteredReservas();
      if (filtroFuro === 'FURO') {{
        list = list.filter(r => r.is_furo_estoque);
      }}

      list = list.filter(r => {{
        if (!term) return true;
        return (r.pedido && String(r.pedido).includes(term)) ||
               (r.codigo_sku && String(r.codigo_sku).includes(term)) ||
               (r.descricao_produto && r.descricao_produto.toLowerCase().includes(term)) ||
               (r.observacao_completa && r.observacao_completa.toLowerCase().includes(term)) ||
               (r.sobras_texto && r.sobras_texto.toLowerCase().includes(term));
      }}).slice(0, 200);

      const tbody = document.getElementById('tbody-acur-res');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(r => {{
        const isFuro = r.is_furo_estoque;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition ' + (isFuro ? 'bg-rose-950/20' : '');
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold ${{isFuro ? 'text-rose-400' : 'text-blue-400'}}">#${{r.pedido}}</td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${{r.filial_nome}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{isFuro ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-slate-800 text-slate-300'}}">
              ${{isFuro ? '🚨 FURO DE ESTOQUE' : r.motivo_classificado || 'Reserva'}}
            </span>
          </td>
          <td class="py-2.5 px-3 font-mono text-slate-400">${{r.codigo_sku}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs" title="${{r.descricao_produto}}">${{r.descricao_produto}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-amber-400">${{fmtNum(r.quantidade_reservada)}}</td>
          <td class="py-2.5 px-3 text-right font-extrabold text-white">${{fmtMoeda(r.valor_total_reservado)}}</td>
          <td class="py-2.5 px-3 font-semibold text-emerald-400 bg-emerald-950/20 text-xs">
            ${{r.sobras_texto || 'Sem sobra WMS no grupo'}}
          </td>
          <td class="py-2.5 px-3 text-xs text-slate-400 truncate max-w-xs" title="${{r.observacao_completa || '-'}}">${{r.observacao_completa || '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableCompensacao() {{
      const term = (document.getElementById('search-acur-comp')?.value || '').toLowerCase().trim();
      const tbody = document.getElementById('tbody-acur-comp');
      if (!tbody) return;
      tbody.innerHTML = '';

      const matches = (DATA.stock_full.inter_store_matches || []).filter(m => {{
        if (!term) return true;
        return (m.codigo && String(m.codigo).includes(term)) ||
               (m.produto && m.produto.toLowerCase().includes(term));
      }}).slice(0, 100);

      matches.forEach(m => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{m.codigo}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs">${{m.produto}}</td>
          <td class="py-2.5 px-3 text-emerald-400 font-bold">${{m.loja_sobra || 'GW Matriz'}} (+${{fmtNum(m.qtd_sobra)}})</td>
          <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">${{fmtNum(m.saldo_wms_sobra)}}</td>
          <td class="py-2.5 px-3 text-rose-400 font-bold">${{m.loja_falta || 'GW Filial'}} (-${{fmtNum(m.qtd_falta)}})</td>
          <td class="py-2.5 px-3 text-right text-rose-400 font-bold">${{fmtNum(m.saldo_sn_falta)}}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/20 text-blue-400">Transferência Recomendada</span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableTroca() {{
      const term = (document.getElementById('search-acur-troca')?.value || '').toLowerCase().trim();
      const tbody = document.getElementById('tbody-acur-troca');
      if (!tbody) return;
      tbody.innerHTML = '';

      const inversoes = (DATA.stock_full.top_inversoes || []).filter(i => {{
        if (!term) return true;
        return (i.sku_wms && String(i.sku_wms).includes(term)) ||
               (i.sku_sn && String(i.sku_sn).includes(term)) ||
               (i.desc_wms && i.desc_wms.toLowerCase().includes(term)) ||
               (i.desc_sn && i.desc_sn.toLowerCase().includes(term));
      }}).slice(0, 80);

      inversoes.forEach(i => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-emerald-400 font-bold">${{i.sku_wms}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs" title="${{i.desc_wms}}">${{i.desc_wms}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">+${{fmtNum(i.saldo_wms)}}</td>
          <td class="py-2.5 px-3 font-mono text-rose-400 font-bold">${{i.sku_sn}}</td>
          <td class="py-2.5 px-3 text-slate-300 truncate max-w-xs" title="${{i.desc_sn}}">${{i.desc_sn}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">-${{fmtNum(i.saldo_sn)}}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-400">${{(i.similaridade * 100).toFixed(0)}}% Match</span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableSemWms() {{
      const term = (document.getElementById('search-acur-sem-wms')?.value || '').toLowerCase().trim();
      const allItems = getFilteredStockItems();
      const list = allItems.filter(it => it.status === 'SEM_ESTOQUE_WMS' && (!term || it.codigo.includes(term) || it.produto.toLowerCase().includes(term))).slice(0, 150);

      const tbody = document.getElementById('tbody-acur-sem-wms');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(i => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{i.codigo}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs" title="${{i.produto}}">${{i.produto}}</td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${{i.filial_nome}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">${{fmtNum(i.sn)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">0</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-500/20 text-rose-400">Sem Endereço WMS</span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderTableSemSn() {{
      const term = (document.getElementById('search-acur-sem-sn')?.value || '').toLowerCase().trim();
      const allItems = getFilteredStockItems();
      const list = allItems.filter(it => it.status === 'SEM_ESTOQUE_SN' && (!term || it.codigo.includes(term) || it.produto.toLowerCase().includes(term))).slice(0, 150);

      const tbody = document.getElementById('tbody-acur-sem-sn');
      if (!tbody) return;
      tbody.innerHTML = '';

      list.forEach(i => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{i.codigo}}</td>
          <td class="py-2.5 px-3 text-white truncate max-w-xs" title="${{i.produto}}">${{i.produto}}</td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${{i.filial_nome}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-emerald-400">${{fmtNum(i.wms)}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400">0</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-400">Sobra no WMS (Sem SN)</span>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function renderCards6Lojas() {{
      const container = document.getElementById('cards-6lojas-container');
      if (!container) return;
      container.innerHTML = '';

      DATA.stock_full.filiais_config.forEach(f => {{
        const isSelected = selectedStoreIds.includes(f.id);
        const storeData = DATA.stock_full.filiais_data[String(f.id)] || {{}};
        const resumo = storeData.resumo || {{}};
        
        container.innerHTML += `
          <div class="p-5 rounded-2xl border transition ${{isSelected ? 'bg-slate-900 border-blue-500/40 shadow-lg shadow-blue-500/5' : 'bg-slate-950/60 border-slate-800 opacity-60'}}">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-bold text-white text-sm">${{f.nome}}</h4>
                <span class="text-[11px] text-slate-400">${{f.praca}}</span>
              </div>
              <button onclick="toggleStore(${{f.id}})" class="text-xs px-2 py-1 rounded ${{isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'}}">
                ${{isSelected ? 'Filtrado' : 'Incluir'}}
              </button>
            </div>
            
            <div class="grid grid-cols-2 gap-2 pt-3 mt-3 border-t border-slate-800 text-xs">
              <div>
                <span class="text-slate-400 text-[10px]">Total Itens:</span>
                <span class="font-bold text-white block">${{fmtNum(resumo.totalProdutos)}}</span>
              </div>
              <div>
                <span class="text-slate-400 text-[10px]">Conciliados:</span>
                <span class="font-bold text-emerald-400 block">${{fmtNum(resumo.conciliados)}}</span>
              </div>
              <div>
                <span class="text-slate-400 text-[10px]">Sem WMS:</span>
                <span class="font-bold text-rose-400 block">${{fmtNum(resumo.semEstoqueWms)}}</span>
              </div>
              <div>
                <span class="text-slate-400 text-[10px]">Sem SN (Sobras):</span>
                <span class="font-bold text-amber-400 block">${{fmtNum(resumo.semEstoqueSn)}}</span>
              </div>
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

    // Export Excel
    function exportCurrentView() {{
      const wb = XLSX.utils.book_new();
      
      // Reservas & Furos
      const resFiltered = getFilteredReservas().map(r => ({{
        "Pedido_DAV": r.pedido,
        "Filial": r.filial_nome,
        "Status": r.is_furo_estoque ? "FURO DE ESTOQUE" : r.motivo_classificado,
        "SKU": r.codigo_sku,
        "Produto": r.descricao_produto,
        "Qtd_Reservada": r.quantidade_reservada,
        "Valor_Total": r.valor_total_reservado,
        "Loja_com_Sobra_WMS_Maior": r.sobras_texto,
        "Observacao": r.observacao_completa
      }}));
      const wsRes = XLSX.utils.json_to_sheet(resFiltered);
      XLSX.utils.book_append_sheet(wb, wsRes, "Reservas_e_Furos");

      // Separacao
      const wsSep = XLSX.utils.json_to_sheet(DATA.team.separacao);
      XLSX.utils.book_append_sheet(wb, wsSep, "Ranking_Separacao");

      // Romaneios
      const wsRom = XLSX.utils.json_to_sheet(DATA.team.romaneios_master);
      XLSX.utils.book_append_sheet(wb, wsRom, "Romaneios_Master");

      // Frota
      const wsFrota = XLSX.utils.json_to_sheet(DATA.frota.veiculos);
      XLSX.utils.book_append_sheet(wb, wsFrota, "Frota_Custos");

      XLSX.writeFile(wb, "GW_Performance_Logistico_Completo.xlsx");
    }}

    function captureCurrentSlide() {{
      const target = document.getElementById('portal-capture-area');
      html2canvas(target, {{ backgroundColor: '#080e1a', scale: 2 }}).then(canvas => {{
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

print(f"Updated portal generated successfully at: {target_path}")

artifact_dir = 'C:/Users/renan.alves/.gemini/antigravity/brain/43bb33b6-6367-463c-94d9-1306168eb162'
artifact_path = os.path.join(artifact_dir, 'dashboard_performance_operacional_logistico.html')
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Artifact updated at: {artifact_path}")
