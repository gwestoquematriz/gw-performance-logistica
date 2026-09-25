import os
import json

print("Reading frota_dashboard_data.json...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/frota_dashboard_data.json', encoding='utf-8') as f:
    raw_data = json.load(f)

json_payload = json.dumps(raw_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard de Gestão de Frota | GW Wireless</title>
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
      background-color: #0f172a;
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
      background: rgba(30, 41, 59, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }}
    .kpi-card {{
      transition: all 0.25s ease-in-out;
    }}
    .kpi-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6);
      border-color: rgba(59, 130, 246, 0.5);
    }}
    .badge-ativo {{
      background-color: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-saiu {{
      background-color: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    .tab-btn.active {{
      background-color: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
    }}
  </style>
</head>
<body class="min-h-screen custom-scroll flex flex-col">

  <!-- TOP HEADER -->
  <header class="glass-card sticky top-0 z-50 px-6 py-3 border-b border-slate-700/60 flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center space-x-4">
      <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
        <i class="fa-solid fa-truck-fast text-xl text-white"></i>
      </div>
      <div>
        <div class="flex items-center space-x-2">
          <h1 class="text-xl font-bold tracking-tight text-white">GW Wireless</h1>
          <span class="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 font-semibold border border-blue-500/30">Frota & Custos</span>
        </div>
        <p class="text-xs text-slate-400">Dashboard Executivo de Gestão de Frota, Combustível, Pedágio e Manutenção</p>
      </div>
    </div>

    <!-- Integration Status Badges -->
    <div class="hidden xl:flex items-center space-x-3 text-xs">
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="font-medium">PostgreSQL GW: Conectado</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
        <i class="fa-solid fa-gas-pump text-xs"></i>
        <span class="font-medium">Gasola API: 2.725 Abastecimentos</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20">
        <i class="fa-solid fa-ticket text-xs"></i>
        <span class="font-medium">Sem Parar: 4.898 Pedágios</span>
      </div>
      <div class="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
        <i class="fa-solid fa-headset text-xs"></i>
        <span class="font-medium">GLPI: 309 Transferências</span>
      </div>
    </div>

    <!-- Quick Action Buttons -->
    <div class="flex items-center space-x-2">
      <button onclick="exportToExcel()" class="px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white flex items-center space-x-1.5 transition shadow-sm">
        <i class="fa-solid fa-file-excel"></i>
        <span>Exportar Excel</span>
      </button>
      <button onclick="captureSlide()" class="px-3.5 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white flex items-center space-x-1.5 transition shadow-sm">
        <i class="fa-solid fa-camera"></i>
        <span>Gerar Slide (PNG)</span>
      </button>
      <button onclick="window.print()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-slate-700 hover:bg-slate-600 text-white flex items-center space-x-1.5 transition">
        <i class="fa-solid fa-print"></i>
      </button>
    </div>
  </header>

  <!-- MAIN WRAPPER -->
  <main class="flex-1 p-6 space-y-6 max-w-[1750px] mx-auto w-full" id="capture-area">

    <!-- FILTERS BAR -->
    <section class="glass-card rounded-2xl p-5 border border-slate-700/60">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        
        <!-- Filial Filter Chips -->
        <div class="space-y-2">
          <label class="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
            <i class="fa-solid fa-building-columns text-blue-400"></i>
            <span>Filiais & Operações (Conforme Regras de Negócio)</span>
          </label>
          <div class="flex flex-wrap gap-2" id="filial-buttons">
            <button onclick="setFilialFilter('TODAS')" class="filial-chip active px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 text-white transition border border-blue-500" data-filial="TODAS">
              Todas Filiais (Frota Completa)
            </button>
            <button onclick="setFilialFilter('MATRIZ')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="MATRIZ">
              Matriz (Lojas 1 e 8)
            </button>
            <button onclick="setFilialFilter('GYN')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="GYN">
              Goiânia (Lojas 6 e 90)
            </button>
            <button onclick="setFilialFilter('BSB')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="BSB">
              Brasília (Lojas 9 e 91)
            </button>
            <button onclick="setFilialFilter('PALMAS')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="PALMAS">
              Palmas (Lojas 10 e 11)
            </button>
            <button onclick="setFilialFilter('MRB')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="MRB">
              Marabá (Lojas 7 e 92)
            </button>
            <button onclick="setFilialFilter('SLZ')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="SLZ">
              São Luís (Loja 14)
            </button>
            <button onclick="setFilialFilter('SERVIÇOS GW')" class="filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700" data-filial="SERVIÇOS GW">
              Serviços GW (Apoio)
            </button>
          </div>
        </div>

        <!-- Veículo / Placa & Status Dropdown Filters -->
        <div class="flex flex-wrap items-center gap-3">
          <div>
            <label class="block text-xs font-medium text-slate-400 mb-1">Selecionar Placa / Veículo</label>
            <select id="placa-select" onchange="applyFilters()" class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-48">
              <option value="TODAS">Todos os Veículos (25)</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-400 mb-1">Status do Veículo</label>
            <select id="status-select" onchange="applyFilters()" class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
              <option value="TODOS">Todos os Status</option>
              <option value="ATIVO" selected>Apenas Ativos (17)</option>
              <option value="SAIU DA FROTA">Saíram da Frota (8)</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-400 mb-1">Ano / Período</label>
            <select id="ano-select" onchange="applyFilters()" class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
              <option value="TODOS">Todo o Período (2025-2026)</option>
              <option value="2026">Ano 2026 (Atual)</option>
              <option value="2025">Ano 2025</option>
            </select>
          </div>

          <div class="pt-5">
            <button onclick="resetAllFilters()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" title="Redefinir filtros">
              <i class="fa-solid fa-arrow-rotate-left mr-1"></i> Resetar
            </button>
          </div>
        </div>

      </div>
    </section>

    <!-- EXECUTIVE KPIS GRID -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
      
      <!-- Card 1: Custo Total -->
      <div class="glass-card kpi-card rounded-2xl p-4 border border-slate-700/60 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Custo Total Frota</span>
          <div class="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <i class="fa-solid fa-wallet text-sm"></i>
          </div>
        </div>
        <div class="mt-3">
          <span class="text-2xl font-extrabold text-white" id="kpi-custo-total">R$ 0,00</span>
          <div class="mt-1 flex items-center text-[11px] text-slate-400">
            <span id="kpi-veiculos-count">25</span>&nbsp;veículos analisados
          </div>
        </div>
      </div>

      <!-- Card 2: Combustível (Gasola) -->
      <div class="glass-card kpi-card rounded-2xl p-4 border border-slate-700/60 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Combustível (Gasola)</span>
          <div class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
            <i class="fa-solid fa-gas-pump text-sm"></i>
          </div>
        </div>
        <div class="mt-3">
          <span class="text-2xl font-extrabold text-amber-400" id="kpi-combustivel">R$ 0,00</span>
          <div class="mt-1 flex items-center justify-between text-[11px] text-slate-400">
            <span id="kpi-combustivel-pct">0% do total</span>
            <span id="kpi-litros">0 L</span>
          </div>
        </div>
      </div>

      <!-- Card 3: Manutenção & Peças -->
      <div class="glass-card kpi-card rounded-2xl p-4 border border-slate-700/60 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Manutenções & Peças</span>
          <div class="w-8 h-8 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center">
            <i class="fa-solid fa-wrench text-sm"></i>
          </div>
        </div>
        <div class="mt-3">
          <span class="text-2xl font-extrabold text-rose-400" id="kpi-manutencao">R$ 0,00</span>
          <div class="mt-1 flex items-center justify-between text-[11px] text-slate-400">
            <span id="kpi-manutencao-pct">0% do total</span>
            <span id="kpi-manutencao-ordens">648 OS</span>
          </div>
        </div>
      </div>

      <!-- Card 4: Pedágio (Sem Parar) -->
      <div class="glass-card kpi-card rounded-2xl p-4 border border-slate-700/60 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Pedágio (Sem Parar)</span>
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
            <i class="fa-solid fa-ticket text-sm"></i>
          </div>
        </div>
        <div class="mt-3">
          <span class="text-2xl font-extrabold text-purple-400" id="kpi-pedagio">R$ 0,00</span>
          <div class="mt-1 flex items-center justify-between text-[11px] text-slate-400">
            <span id="kpi-pedagio-pct">0% do total</span>
            <span id="kpi-pedagio-passagens">0 passagens</span>
          </div>
        </div>
      </div>

      <!-- Card 5: Km Total Rodado -->
      <div class="glass-card kpi-card rounded-2xl p-4 border border-slate-700/60 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Km Total Rodado</span>
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-route text-sm"></i>
          </div>
        </div>
        <div class="mt-3">
          <span class="text-2xl font-extrabold text-emerald-400" id="kpi-km">0 km</span>
          <div class="mt-1 flex items-center text-[11px] text-slate-400">
            Frota monitorada
          </div>
        </div>
      </div>

      <!-- Card 6: Eficiência Km/L & Custo/Km -->
      <div class="glass-card kpi-card rounded-2xl p-4 border border-slate-700/60 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Eficiência Geral</span>
          <div class="w-8 h-8 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center">
            <i class="fa-solid fa-gauge-high text-sm"></i>
          </div>
        </div>
        <div class="mt-3">
          <span class="text-2xl font-extrabold text-cyan-400" id="kpi-kml">0,00 km/L</span>
          <div class="mt-1 flex items-center justify-between text-[11px] text-slate-400">
            <span>Custo:</span>
            <span class="font-bold text-slate-300" id="kpi-custo-km">R$ 0,00 / km</span>
          </div>
        </div>
      </div>

    </section>

    <!-- CHARTS ROW 1: EVOLUÇÃO MENSAL E COMPOSIÇÃO -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Chart: Evolução Mensal Empilhada -->
      <div class="glass-card rounded-2xl p-5 border border-slate-700/60 lg:col-span-2 flex flex-col justify-between">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-chart-column text-blue-400"></i>
              <span>Evolução Mensal de Custos (2025 - 2026)</span>
            </h3>
            <p class="text-xs text-slate-400">Comparativo mensal entre Combustível, Manutenção e Pedágio</p>
          </div>
          <div class="flex items-center space-x-2 text-xs">
            <span class="inline-flex items-center px-2 py-0.5 rounded bg-blue-500/20 text-blue-400">Combustível</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded bg-rose-500/20 text-rose-400">Manutenção</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded bg-purple-500/20 text-purple-400">Pedágio</span>
          </div>
        </div>
        <div class="h-72 w-full">
          <canvas id="chartEvolucaoMensal"></canvas>
        </div>
      </div>

      <!-- Chart: Composição da Despesa (% Donut) -->
      <div class="glass-card rounded-2xl p-5 border border-slate-700/60 flex flex-col justify-between">
        <div class="mb-4">
          <h3 class="text-sm font-bold text-white flex items-center space-x-2">
            <i class="fa-solid fa-chart-pie text-emerald-400"></i>
            <span>Composição dos Custos</span>
          </h3>
          <p class="text-xs text-slate-400">Distribuição percentual por categoria operacional</p>
        </div>
        <div class="h-56 w-full flex items-center justify-center">
          <canvas id="chartComposicao"></canvas>
        </div>
        <div class="grid grid-cols-3 gap-2 pt-3 border-t border-slate-700/40 text-center text-xs">
          <div>
            <span class="block text-slate-400 text-[10px]">Combustível</span>
            <span class="font-bold text-amber-400" id="donut-comb-pct">71.9%</span>
          </div>
          <div>
            <span class="block text-slate-400 text-[10px]">Manutenção</span>
            <span class="font-bold text-rose-400" id="donut-manut-pct">19.1%</span>
          </div>
          <div>
            <span class="block text-slate-400 text-[10px]">Pedágio</span>
            <span class="font-bold text-purple-400" id="donut-ped-pct">9.0%</span>
          </div>
        </div>
      </div>

    </section>

    <!-- CHARTS ROW 2: RANKING DE VEÍCULOS E EFICIÊNCIA KM/L -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- Chart: Top 10 Veículos Mais Onerosos -->
      <div class="glass-card rounded-2xl p-5 border border-slate-700/60">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-ranking-star text-amber-400"></i>
              <span>Ranking: Veículos com Maior Custo Operacional</span>
            </h3>
            <p class="text-xs text-slate-400">Soma acumulada de combustível, manutenção e pedágio por placa</p>
          </div>
        </div>
        <div class="h-64 w-full">
          <canvas id="chartRankingVeiculos"></canvas>
        </div>
      </div>

      <!-- Chart: Eficiência de Consumo (Km/L) por Veículo -->
      <div class="glass-card rounded-2xl p-5 border border-slate-700/60">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-gauge text-cyan-400"></i>
              <span>Eficiência Operacional: Média Km/Litro por Veículo</span>
            </h3>
            <p class="text-xs text-slate-400">Veículos com menor rendimento demandam revisão mecânica ou análise de rota</p>
          </div>
        </div>
        <div class="h-64 w-full">
          <canvas id="chartEficienciaKml"></canvas>
        </div>
      </div>

    </section>

    <!-- STRATEGIC DECISION ALERT BANNER -->
    <section class="glass-card rounded-2xl p-5 border border-blue-500/30 bg-blue-950/20">
      <div class="flex items-start space-x-3">
        <div class="p-2.5 rounded-xl bg-blue-500/20 text-blue-400 text-lg">
          <i class="fa-solid fa-lightbulb"></i>
        </div>
        <div class="flex-1">
          <h4 class="text-sm font-bold text-white">Insights & Apoio à Tomada de Decisão</h4>
          <div class="mt-2 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
            <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700">
              <span class="font-semibold text-rose-400 block mb-1">🚨 Alerta de Manutenção Elevada:</span>
              <span>O veículo <strong class="text-white">OVM0118 (Master - GYN)</strong> consumiu <strong>R$ 45.968,00</strong> em manutenção para <strong>R$ 49.253,94</strong> de combustível (quase 50% do custo em oficina). Recomenda-se plano de substituição ou auditoria técnica.</span>
            </div>
            <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700">
              <span class="font-semibold text-amber-400 block mb-1">⛽ Maiores Consumidores de Combustível:</span>
              <span>Os caminhões pesados <strong class="text-white">RBP9G30 (VW 14.190)</strong> e <strong class="text-white">RMA3J97 (Accelo)</strong> concentram mais de <strong>R$ 287.000,00</strong> em combustível. Monitoramento de telemetria e negociação de diesel na bomba geram até 8% de economia.</span>
            </div>
            <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700">
              <span class="font-semibold text-emerald-400 block mb-1">📋 Rateio GLPI Filiais:</span>
              <span>Total de <strong class="text-white">309 chamados</strong> de transferência de abastecimento registrados no GLPI, garantindo que despesas da Matriz sejam debitadas corretamente nos centros de custo de Palmas, Marabá, Goiânia e BSB.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- DATA EXPLORER TABS -->
    <section class="glass-card rounded-2xl border border-slate-700/60 overflow-hidden">
      
      <!-- Tab Header Buttons -->
      <div class="flex flex-wrap items-center border-b border-slate-700/60 px-6 pt-4 gap-2 bg-slate-800/40">
        <button onclick="switchTab('tab-ranking')" class="tab-btn active px-4 py-2.5 text-xs font-semibold rounded-t-lg transition flex items-center space-x-2 border-b-2" id="btn-tab-ranking">
          <i class="fa-solid fa-list-check"></i>
          <span>1. Resumo da Frota & Ranking</span>
        </button>
        <button onclick="switchTab('tab-kardex')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg text-slate-400 hover:text-white transition flex items-center space-x-2 border-b-2 border-transparent" id="btn-tab-kardex">
          <i class="fa-solid fa-calendar-days"></i>
          <span>2. Histórico Mensal Consolidado</span>
        </button>
        <button onclick="switchTab('tab-manutencao')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg text-slate-400 hover:text-white transition flex items-center space-x-2 border-b-2 border-transparent" id="btn-tab-manutencao">
          <i class="fa-solid fa-wrench"></i>
          <span>3. Manutenções & Oficinas (648)</span>
        </button>
        <button onclick="switchTab('tab-combustivel')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg text-slate-400 hover:text-white transition flex items-center space-x-2 border-b-2 border-transparent" id="btn-tab-combustivel">
          <i class="fa-solid fa-gas-pump"></i>
          <span>4. Eficiência Gasola (Mensal)</span>
        </button>
        <button onclick="switchTab('tab-pedagios')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg text-slate-400 hover:text-white transition flex items-center space-x-2 border-b-2 border-transparent" id="btn-tab-pedagios">
          <i class="fa-solid fa-ticket"></i>
          <span>5. Pedágios Sem Parar</span>
        </button>
        <button onclick="switchTab('tab-glpi')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg text-slate-400 hover:text-white transition flex items-center space-x-2 border-b-2 border-transparent" id="btn-tab-glpi">
          <i class="fa-solid fa-headset"></i>
          <span>6. Transferências GLPI (309)</span>
        </button>
      </div>

      <!-- Tab Content Area -->
      <div class="p-6">

        <!-- TAB 1: RESUMO GERAL & RANKING -->
        <div id="tab-ranking" class="tab-panel space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div class="text-xs text-slate-400">
              Listando <span class="font-bold text-white" id="tab1-count">25</span> veículos da frota
            </div>
            <div class="flex items-center space-x-2">
              <input type="text" id="tab1-search" oninput="renderTable1()" placeholder="Buscar placa, modelo, motorista..." class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
            </div>
          </div>
          
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-700/60">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-800/80 text-slate-300 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-700">
                <tr>
                  <th class="py-3 px-3">Placa</th>
                  <th class="py-3 px-3">Modelo / Descrição</th>
                  <th class="py-3 px-3">Status</th>
                  <th class="py-3 px-3">Filial</th>
                  <th class="py-3 px-3">Motorista</th>
                  <th class="py-3 px-3 text-right">Combustível (R$)</th>
                  <th class="py-3 px-3 text-right">Km Rodado</th>
                  <th class="py-3 px-3 text-right">Média Km/L</th>
                  <th class="py-3 px-3 text-right">Manutenção (R$)</th>
                  <th class="py-3 px-3 text-right">Pedágio (R$)</th>
                  <th class="py-3 px-3 text-right font-bold text-blue-400">Custo Total (R$)</th>
                  <th class="py-3 px-3 text-right">Custo R$/Km</th>
                </tr>
              </thead>
              <tbody id="tab1-tbody" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- TAB 2: HISTÓRICO MENSAL KARDEX -->
        <div id="tab-kardex" class="tab-panel hidden space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div class="text-xs text-slate-400">
              Registros mensais consolidados por categoria de custo
            </div>
            <input type="text" id="tab2-search" oninput="renderTable2()" placeholder="Filtrar ano-mês, placa, categoria..." class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>
          
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-700/60 max-h-[500px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-800/80 text-slate-300 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-700 sticky top-0">
                <tr>
                  <th class="py-3 px-3">Ano-Mês</th>
                  <th class="py-3 px-3">Filial</th>
                  <th class="py-3 px-3">Placa</th>
                  <th class="py-3 px-3">Apelido</th>
                  <th class="py-3 px-3">Categoria</th>
                  <th class="py-3 px-3 text-right">Valor Total (R$)</th>
                </tr>
              </thead>
              <tbody id="tab2-tbody" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- TAB 3: MANUTENÇÕES & OFICINAS -->
        <div id="tab-manutencao" class="tab-panel hidden space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div class="text-xs text-slate-400">
              Ordens de serviço, peças compradas e reparos de oficina
            </div>
            <input type="text" id="tab3-search" oninput="renderTable3()" placeholder="Filtrar por placa, grupo, descrição do reparo..." class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-72">
          </div>
          
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-700/60 max-h-[500px]">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-800/80 text-slate-300 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-700 sticky top-0">
                <tr>
                  <th class="py-3 px-3">Data</th>
                  <th class="py-3 px-3">Placa</th>
                  <th class="py-3 px-3">Grupo</th>
                  <th class="py-3 px-3">Filial</th>
                  <th class="py-3 px-3">Cidade</th>
                  <th class="py-3 px-3 text-right">Valor (R$)</th>
                  <th class="py-3 px-3">Descrição do Serviço / Peça</th>
                </tr>
              </thead>
              <tbody id="tab3-tbody" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- TAB 4: COMBUSTÍVEL GASOLA -->
        <div id="tab-combustivel" class="tab-panel hidden space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div class="text-xs text-slate-400">
              Métricas mensais de abastecimento da plataforma Gasola
            </div>
            <input type="text" id="tab4-search" oninput="renderTable4()" placeholder="Filtrar placa ou mês..." class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>
          
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-700/60 max-h-[500px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-800/80 text-slate-300 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-700 sticky top-0">
                <tr>
                  <th class="py-3 px-3">Mês</th>
                  <th class="py-3 px-3">Placa</th>
                  <th class="py-3 px-3 text-right">Qtd Abastec.</th>
                  <th class="py-3 px-3 text-right">Valor Pago (R$)</th>
                  <th class="py-3 px-3 text-right">Litros</th>
                  <th class="py-3 px-3 text-right">Km Rodado</th>
                  <th class="py-3 px-3 text-right">Preço Médio Litro</th>
                  <th class="py-3 px-3 text-right">Consumo Médio (Km/L)</th>
                </tr>
              </thead>
              <tbody id="tab4-tbody" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- TAB 5: PEDÁGIOS -->
        <div id="tab-pedagios" class="tab-panel hidden space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div class="text-xs text-slate-400">
              Passagens de pedágio registradas via tag Sem Parar
            </div>
            <input type="text" id="tab5-search" oninput="renderTable5()" placeholder="Filtrar concessionária, placa, mês..." class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>
          
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-700/60 max-h-[500px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-800/80 text-slate-300 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-700 sticky top-0">
                <tr>
                  <th class="py-3 px-3">Mês</th>
                  <th class="py-3 px-3">Placa</th>
                  <th class="py-3 px-3">Filial</th>
                  <th class="py-3 px-3">Concessionária / Estabelecimento</th>
                  <th class="py-3 px-3 text-right">Qtd Passagens</th>
                  <th class="py-3 px-3 text-right">Valor Cobrado (R$)</th>
                </tr>
              </thead>
              <tbody id="tab5-tbody" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- TAB 6: GLPI TRANSFERÊNCIAS -->
        <div id="tab-glpi" class="tab-panel hidden space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div class="text-xs text-slate-400">
              Chamados de transferência e rateio de abastecimento no GLPI
            </div>
            <input type="text" id="tab6-search" oninput="renderTable6()" placeholder="Filtrar chamado, solicitante, filial..." class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-64">
          </div>
          
          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-700/60 max-h-[500px]">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-800/80 text-slate-300 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-700 sticky top-0">
                <tr>
                  <th class="py-3 px-3">ID GLPI</th>
                  <th class="py-3 px-3">Título Chamado</th>
                  <th class="py-3 px-3">Status</th>
                  <th class="py-3 px-3">Data</th>
                  <th class="py-3 px-3">Solicitante</th>
                  <th class="py-3 px-3">Empresa Origem</th>
                  <th class="py-3 px-3">Empresa Destino</th>
                  <th class="py-3 px-3">Motivo</th>
                </tr>
              </thead>
              <tbody id="tab6-tbody" class="divide-y divide-slate-800">
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
    <div>
      GW Wireless © 2026 - Sistema de Inteligência em Gestão Logística & Frotas
    </div>
    <div class="flex items-center space-x-4">
      <span>Base PostgreSQL: <strong class="text-slate-400">gwlogistica</strong></span>
      <span>Base GLPI: <strong class="text-slate-400">glpidb (MySQL)</strong></span>
      <span>API Gasola: <strong class="text-slate-400">Ativa & Sincronizada</strong></span>
    </div>
  </footer>

  <!-- EMBEDDED DATASET -->
  <script>
    const RAW_DATA = {json_payload};

    // Global Filter State
    let currentFilial = 'TODAS';
    let currentPlaca = 'TODAS';
    let currentStatus = 'ATIVO';
    let currentAno = 'TODOS';

    // Chart Instances
    let chartEvolucao = null;
    let chartDonut = null;
    let chartRanking = null;
    let chartEficiencia = null;

    // Formatters
    const fmtMoeda = (val) => new Intl.NumberFormat('pt-BR', {{ style: 'currency', currency: 'BRL' }}).format(val || 0);
    const fmtNum = (val, dec=0) => new Intl.NumberFormat('pt-BR', {{ minimumFractionDigits: dec, maximumFractionDigits: dec }}).format(val || 0);

    // Initializer
    document.addEventListener('DOMContentLoaded', () => {{
      populatePlacasDropdown();
      applyFilters();
    }});

    function populatePlacasDropdown() {{
      const select = document.getElementById('placa-select');
      select.innerHTML = '<option value="TODAS">Todos os Veículos (25)</option>';
      
      const sorted = [...RAW_DATA.veiculos].sort((a,b) => a.placa.localeCompare(b.placa));
      sorted.forEach(v => {{
        const opt = document.createElement('option');
        opt.value = v.placa;
        opt.textContent = `${{v.placa}} - ${{v.apelido || v.modelo}} (${{v.status}})`;
        select.appendChild(opt);
      }});
    }}

    function setFilialFilter(filial) {{
      currentFilial = filial;
      // Update buttons style
      document.querySelectorAll('.filial-chip').forEach(btn => {{
        if (btn.getAttribute('data-filial') === filial) {{
          btn.className = 'filial-chip active px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 text-white transition border border-blue-500';
        }} else {{
          btn.className = 'filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700';
        }}
      }});
      applyFilters();
    }}

    function resetAllFilters() {{
      currentFilial = 'TODAS';
      currentPlaca = 'TODAS';
      currentStatus = 'ATIVO';
      currentAno = 'TODOS';

      document.getElementById('placa-select').value = 'TODAS';
      document.getElementById('status-select').value = 'ATIVO';
      document.getElementById('ano-select').value = 'TODOS';
      
      document.querySelectorAll('.filial-chip').forEach(btn => {{
        if (btn.getAttribute('data-filial') === 'TODAS') {{
          btn.className = 'filial-chip active px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 text-white transition border border-blue-500';
        }} else {{
          btn.className = 'filial-chip px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition border border-slate-700';
        }}
      }});

      applyFilters();
    }}

    function applyFilters() {{
      currentPlaca = document.getElementById('placa-select').value;
      currentStatus = document.getElementById('status-select').value;
      currentAno = document.getElementById('ano-select').value;

      // Filter vehicles
      const filteredVeiculos = RAW_DATA.veiculos.filter(v => {{
        if (currentFilial !== 'TODAS' && v.filial !== currentFilial) return false;
        if (currentPlaca !== 'TODAS' && v.placa !== currentPlaca) return false;
        if (currentStatus !== 'TODOS' && v.status !== currentStatus) return false;
        return true;
      }});

      // Filter monthly costs
      const filteredCustos = RAW_DATA.custos_mensais.filter(c => {{
        if (currentFilial !== 'TODAS' && c.filial !== currentFilial) return false;
        if (currentPlaca !== 'TODAS' && c.placa !== currentPlaca) return false;
        if (currentAno !== 'TODOS' && !c.ano_mes.startsWith(currentAno)) return false;
        return true;
      }});

      // Update KPIs
      updateKPIs(filteredVeiculos, filteredCustos);

      // Render Charts
      renderCharts(filteredVeiculos, filteredCustos);

      // Render Tables
      renderTable1(filteredVeiculos);
      renderTable2(filteredCustos);
      renderTable3();
      renderTable4();
      renderTable5();
      renderTable6();
    }}

    function updateKPIs(veiculos, custos) {{
      const totalGasto = veiculos.reduce((acc, v) => acc + v.custo_total, 0);
      const totalComb = veiculos.reduce((acc, v) => acc + v.gasto_combustivel, 0);
      const totalManut = veiculos.reduce((acc, v) => acc + v.gasto_manutencao, 0);
      const totalPed = veiculos.reduce((acc, v) => acc + v.gasto_pedagio, 0);
      const totalKm = veiculos.reduce((acc, v) => acc + v.km_rodado, 0);
      const totalLitros = veiculos.reduce((acc, v) => acc + v.litros, 0);
      const totalPedQtd = veiculos.reduce((acc, v) => acc + v.qtd_pedagio, 0);

      const kmlMedio = totalLitros > 0 ? (totalKm / totalLitros) : 0;
      const custoKm = totalKm > 0 ? (totalGasto / totalKm) : 0;

      const combPct = totalGasto > 0 ? ((totalComb / totalGasto) * 100).toFixed(1) : '0';
      const manutPct = totalGasto > 0 ? ((totalManut / totalGasto) * 100).toFixed(1) : '0';
      const pedPct = totalGasto > 0 ? ((totalPed / totalGasto) * 100).toFixed(1) : '0';

      document.getElementById('kpi-custo-total').textContent = fmtMoeda(totalGasto);
      document.getElementById('kpi-veiculos-count').textContent = veiculos.length;
      document.getElementById('kpi-combustivel').textContent = fmtMoeda(totalComb);
      document.getElementById('kpi-combustivel-pct').textContent = `${{combPct}}% do total`;
      document.getElementById('kpi-litros').textContent = `${{fmtNum(totalLitros, 0)}} L`;

      document.getElementById('kpi-manutencao').textContent = fmtMoeda(totalManut);
      document.getElementById('kpi-manutencao-pct').textContent = `${{manutPct}}% do total`;

      document.getElementById('kpi-pedagio').textContent = fmtMoeda(totalPed);
      document.getElementById('kpi-pedagio-pct').textContent = `${{pedPct}}% do total`;
      document.getElementById('kpi-pedagio-passagens').textContent = `${{fmtNum(totalPedQtd, 0)}} passagens`;

      document.getElementById('kpi-km').textContent = `${{fmtNum(totalKm, 0)}} km`;
      document.getElementById('kpi-kml').textContent = `${{kmlMedio.toFixed(2)}} km/L`;
      document.getElementById('kpi-custo-km').textContent = `${{fmtMoeda(custoKm)}} / km`;

      document.getElementById('donut-comb-pct').textContent = `${{combPct}}%`;
      document.getElementById('donut-manut-pct').textContent = `${{manutPct}}%`;
      document.getElementById('donut-ped-pct').textContent = `${{pedPct}}%`;
    }}

    function renderCharts(veiculos, custos) {{
      // 1. Chart Evolucao Mensal (Stacked Bar)
      const mesesSet = new Set(custos.map(c => c.ano_mes));
      const meses = Array.from(mesesSet).sort();

      const combMap = {{}}, manutMap = {{}}, pedMap = {{}};
      meses.forEach(m => {{ combMap[m] = 0; manutMap[m] = 0; pedMap[m] = 0; }});

      custos.forEach(c => {{
        if (c.categoria === 'COMBUSTÍVEL') combMap[c.ano_mes] = (combMap[c.ano_mes] || 0) + c.valor;
        else if (c.categoria === 'PEDÁGIO') pedMap[c.ano_mes] = (pedMap[c.ano_mes] || 0) + c.valor;
        else manutMap[c.ano_mes] = (manutMap[c.ano_mes] || 0) + c.valor;
      }});

      const ctxEvol = document.getElementById('chartEvolucaoMensal').getContext('2d');
      if (chartEvolucao) chartEvolucao.destroy();
      chartEvolucao = new Chart(ctxEvol, {{
        type: 'bar',
        data: {{
          labels: meses,
          datasets: [
            {{
              label: 'Combustível (Gasola)',
              data: meses.map(m => combMap[m]),
              backgroundColor: '#3b82f6',
              borderRadius: 4
            }},
            {{
              label: 'Manutenção & Peças',
              data: meses.map(m => manutMap[m]),
              backgroundColor: '#f43f5e',
              borderRadius: 4
            }},
            {{
              label: 'Pedágio (Sem Parar)',
              data: meses.map(m => pedMap[m]),
              backgroundColor: '#a855f7',
              borderRadius: 4
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ stacked: true, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
            y: {{ stacked: true, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }}, callback: v => 'R$ ' + (v/1000).toFixed(0) + 'k' }} }}
          }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: ctx => `${{ctx.dataset.label}}: ${{fmtMoeda(ctx.raw)}}`
              }}
            }}
          }}
        }}
      }});

      // 2. Chart Composição Donut
      const totComb = veiculos.reduce((acc, v) => acc + v.gasto_combustivel, 0);
      const totManut = veiculos.reduce((acc, v) => acc + v.gasto_manutencao, 0);
      const totPed = veiculos.reduce((acc, v) => acc + v.gasto_pedagio, 0);

      const ctxDonut = document.getElementById('chartComposicao').getContext('2d');
      if (chartDonut) chartDonut.destroy();
      chartDonut = new Chart(ctxDonut, {{
        type: 'doughnut',
        data: {{
          labels: ['Combustível (Gasola)', 'Manutenção & Peças', 'Pedágio (Sem Parar)'],
          datasets: [{{
            data: [totComb, totManut, totPed],
            backgroundColor: ['#f59e0b', '#f43f5e', '#a855f7'],
            borderColor: '#1e293b',
            borderWidth: 2
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }},
            tooltip: {{
              callbacks: {{
                label: ctx => `${{ctx.label}}: ${{fmtMoeda(ctx.raw)}}`
              }}
            }}
          }}
        }}
      }});

      // 3. Chart Ranking Top 10 Veículos
      const topVeiculos = [...veiculos].sort((a,b) => b.custo_total - a.custo_total).slice(0, 10);
      const ctxRank = document.getElementById('chartRankingVeiculos').getContext('2d');
      if (chartRanking) chartRanking.destroy();
      chartRanking = new Chart(ctxRank, {{
        type: 'bar',
        data: {{
          labels: topVeiculos.map(v => `${{v.placa}} (${{v.apelido || v.modelo.substring(0, 10)}})`),
          datasets: [{{
            label: 'Custo Total (R$)',
            data: topVeiculos.map(v => v.custo_total),
            backgroundColor: '#3b82f6',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }}, callback: v => 'R$ ' + (v/1000).toFixed(0) + 'k' }} }},
            y: {{ grid: {{ display: false }}, ticks: {{ color: '#e2e8f0', font: {{ size: 10 }} }} }}
          }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: ctx => `Custo Total: ${{fmtMoeda(ctx.raw)}}`
              }}
            }}
          }}
        }}
      }});

      // 4. Chart Eficiência Km/L
      const veiculosKml = [...veiculos].filter(v => v.media_kml > 0).sort((a,b) => b.media_kml - a.media_kml);
      const ctxEf = document.getElementById('chartEficienciaKml').getContext('2d');
      if (chartEficiencia) chartEficiencia.destroy();
      chartEficiencia = new Chart(ctxEf, {{
        type: 'bar',
        data: {{
          labels: veiculosKml.map(v => v.placa),
          datasets: [{{
            label: 'Média Km/L',
            data: veiculosKml.map(v => v.media_kml),
            backgroundColor: veiculosKml.map(v => v.media_kml < 4 ? '#ef4444' : v.media_kml < 7 ? '#f59e0b' : '#10b981'),
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }}
          }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: ctx => `Consumo Médio: ${{ctx.raw.toFixed(2)}} km/L`
              }}
            }}
          }}
        }}
      }});
    }}

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
      document.getElementById(tabId).classList.remove('hidden');

      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('active');
        btn.classList.add('text-slate-400', 'border-transparent');
      }});

      const activeBtn = document.getElementById('btn-' + tabId);
      activeBtn.classList.add('active');
      activeBtn.classList.remove('text-slate-400', 'border-transparent');
    }}

    // TAB 1 RENDER
    function renderTable1(filteredList) {{
      const list = filteredList || RAW_DATA.veiculos.filter(v => {{
        if (currentFilial !== 'TODAS' && v.filial !== currentFilial) return false;
        if (currentPlaca !== 'TODAS' && v.placa !== currentPlaca) return false;
        if (currentStatus !== 'TODOS' && v.status !== currentStatus) return false;
        return true;
      }});

      const term = (document.getElementById('tab1-search')?.value || '').toLowerCase().trim();
      const finalItems = list.filter(v => {{
        if (!term) return true;
        return (v.placa && v.placa.toLowerCase().includes(term)) ||
               (v.modelo && v.modelo.toLowerCase().includes(term)) ||
               (v.apelido && v.apelido.toLowerCase().includes(term)) ||
               (v.motorista && v.motorista.toLowerCase().includes(term)) ||
               (v.filial && v.filial.toLowerCase().includes(term));
      }}).sort((a,b) => b.custo_total - a.custo_total);

      document.getElementById('tab1-count').textContent = finalItems.length;
      const tbody = document.getElementById('tab1-tbody');
      tbody.innerHTML = '';

      finalItems.forEach(v => {{
        const cKm = v.km_rodado > 0 ? (v.custo_total / v.km_rodado) : 0;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        tr.innerHTML = `
          <td class="py-3 px-3 font-bold text-white font-mono flex items-center space-x-2">
            <span>${{v.placa}}</span>
          </td>
          <td class="py-3 px-3 text-slate-300">
            <div class="font-medium text-white">${{v.apelido || v.modelo}}</div>
            <div class="text-[10px] text-slate-400 truncate max-w-xs">${{v.modelo}}</div>
          </td>
          <td class="py-3 px-3">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold ${{v.status === 'ATIVO' ? 'badge-ativo' : 'badge-saiu'}}">
              ${{v.status}}
            </span>
          </td>
          <td class="py-3 px-3 text-slate-300">
            <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${{v.filial}}</span>
          </td>
          <td class="py-3 px-3 text-slate-300">${{v.motorista || 'N/D'}}</td>
          <td class="py-3 px-3 text-right font-medium text-amber-400">${{fmtMoeda(v.gasto_combustivel)}}</td>
          <td class="py-3 px-3 text-right text-slate-300">${{fmtNum(v.km_rodado, 0)}} km</td>
          <td class="py-3 px-3 text-right font-semibold ${{v.media_kml < 4 ? 'text-rose-400' : 'text-cyan-400'}}">${{v.media_kml > 0 ? v.media_kml.toFixed(2) : '-'}}</td>
          <td class="py-3 px-3 text-right font-medium text-rose-400">${{fmtMoeda(v.gasto_manutencao)}}</td>
          <td class="py-3 px-3 text-right font-medium text-purple-400">${{fmtMoeda(v.gasto_pedagio)}}</td>
          <td class="py-3 px-3 text-right font-bold text-blue-400 text-sm">${{fmtMoeda(v.custo_total)}}</td>
          <td class="py-3 px-3 text-right text-slate-300">${{cKm > 0 ? fmtMoeda(cKm) : '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // TAB 2 RENDER
    function renderTable2(filteredList) {{
      const list = filteredList || RAW_DATA.custos_mensais;
      const term = (document.getElementById('tab2-search')?.value || '').toLowerCase().trim();
      const finalItems = list.filter(c => {{
        if (!term) return true;
        return (c.ano_mes && c.ano_mes.toLowerCase().includes(term)) ||
               (c.placa && c.placa.toLowerCase().includes(term)) ||
               (c.filial && c.filial.toLowerCase().includes(term)) ||
               (c.categoria && c.categoria.toLowerCase().includes(term));
      }}).slice(0, 300); // cap for fast rendering

      const tbody = document.getElementById('tab2-tbody');
      tbody.innerHTML = '';
      finalItems.forEach(r => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-300">${{r.ano_mes}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{r.filial}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-white">${{r.placa}}</td>
          <td class="py-2.5 px-3 text-slate-400">${{r.apelido || '-'}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{r.categoria === 'COMBUSTÍVEL' ? 'bg-amber-500/20 text-amber-400' : r.categoria === 'PEDÁGIO' ? 'bg-purple-500/20 text-purple-400' : 'bg-rose-500/20 text-rose-400'}}">
              ${{r.categoria}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-right font-semibold text-white">${{fmtMoeda(r.valor)}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // TAB 3 RENDER (MANUTENÇÃO)
    function renderTable3() {{
      const term = (document.getElementById('tab3-search')?.value || '').toLowerCase().trim();
      const list = RAW_DATA.manutencoes.filter(m => {{
        if (currentFilial !== 'TODAS' && m.filial !== currentFilial) return false;
        if (currentPlaca !== 'TODAS' && m.placa !== currentPlaca) return false;
        if (!term) return true;
        return (m.placa && m.placa.toLowerCase().includes(term)) ||
               (m.grupo && m.grupo.toLowerCase().includes(term)) ||
               (m.descricao && m.descricao.toLowerCase().includes(term)) ||
               (m.cidade && m.cidade.toLowerCase().includes(term));
      }}).slice(0, 200);

      const tbody = document.getElementById('tab3-tbody');
      tbody.innerHTML = '';
      list.forEach(m => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 text-slate-400 whitespace-nowrap">${{m.data}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-white whitespace-nowrap">${{m.placa}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">${{m.grupo}}</span>
          </td>
          <td class="py-2.5 px-3 text-slate-300">${{m.filial}}</td>
          <td class="py-2.5 px-3 text-slate-400">${{m.cidade || 'N/D'}}</td>
          <td class="py-2.5 px-3 text-right font-bold text-rose-400 whitespace-nowrap">${{fmtMoeda(m.valor)}}</td>
          <td class="py-2.5 px-3 text-slate-300 text-xs">${{m.descricao}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // TAB 4 RENDER (COMBUSTÍVEL GASOLA)
    function renderTable4() {{
      const term = (document.getElementById('tab4-search')?.value || '').toLowerCase().trim();
      const list = RAW_DATA.combustivel_mensal.filter(c => {{
        if (currentPlaca !== 'TODAS' && c.placa !== currentPlaca) return false;
        if (!term) return true;
        return (c.placa && c.placa.toLowerCase().includes(term)) ||
               (c.ano_mes && c.ano_mes.toLowerCase().includes(term));
      }}).slice(0, 200);

      const tbody = document.getElementById('tab4-tbody');
      tbody.innerHTML = '';
      list.forEach(c => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{c.ano_mes}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-white">${{c.placa}}</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{c.qtd}}</td>
          <td class="py-2.5 px-3 text-right font-semibold text-amber-400">${{fmtMoeda(c.valor)}}</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{fmtNum(c.litros, 1)}} L</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{fmtNum(c.km, 0)}} km</td>
          <td class="py-2.5 px-3 text-right text-slate-400">R$ ${{c.preco_medio.toFixed(3)}}</td>
          <td class="py-2.5 px-3 text-right font-bold ${{c.kml < 4 ? 'text-rose-400' : 'text-cyan-400'}}">${{c.kml.toFixed(2)}} km/L</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // TAB 5 RENDER (PEDÁGIOS)
    function renderTable5() {{
      const term = (document.getElementById('tab5-search')?.value || '').toLowerCase().trim();
      const list = RAW_DATA.pedagios_agrupados.filter(p => {{
        if (currentFilial !== 'TODAS' && p.filial !== currentFilial) return false;
        if (currentPlaca !== 'TODAS' && p.placa !== currentPlaca) return false;
        if (!term) return true;
        return (p.placa && p.placa.toLowerCase().includes(term)) ||
               (p.ano_mes && p.ano_mes.toLowerCase().includes(term)) ||
               (p.estabelecimento && p.estabelecimento.toLowerCase().includes(term));
      }}).slice(0, 200);

      const tbody = document.getElementById('tab5-tbody');
      tbody.innerHTML = '';
      list.forEach(p => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-slate-400">${{p.ano_mes}}</td>
          <td class="py-2.5 px-3 font-mono font-bold text-white">${{p.placa}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{p.filial}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{p.estabelecimento}}</td>
          <td class="py-2.5 px-3 text-right text-slate-300">${{p.passagens}}</td>
          <td class="py-2.5 px-3 text-right font-semibold text-purple-400">${{fmtMoeda(p.valor)}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // TAB 6 RENDER (GLPI)
    function renderTable6() {{
      const term = (document.getElementById('tab6-search')?.value || '').toLowerCase().trim();
      const list = RAW_DATA.glpi_transfers.filter(g => {{
        if (!term) return true;
        return (g.titulo && g.titulo.toLowerCase().includes(term)) ||
               (g.solicitante && g.solicitante.toLowerCase().includes(term)) ||
               (g.origem && g.origem.toLowerCase().includes(term)) ||
               (g.destino && g.destino.toLowerCase().includes(term)) ||
               (String(g.id).includes(term));
      }}).slice(0, 200);

      const tbody = document.getElementById('tab6-tbody');
      tbody.innerHTML = '';
      list.forEach(g => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/50 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono text-blue-400 font-semibold">#${{g.id}}</td>
          <td class="py-2.5 px-3 text-white font-medium">${{g.titulo}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/20 text-blue-400">${{g.status}}</span>
          </td>
          <td class="py-2.5 px-3 text-slate-400 whitespace-nowrap">${{g.data}}</td>
          <td class="py-2.5 px-3 text-slate-300">${{g.solicitante || 'N/D'}}</td>
          <td class="py-2.5 px-3 text-slate-400 text-xs">${{g.origem}}</td>
          <td class="py-2.5 px-3 text-emerald-400 text-xs font-medium">${{g.destino}}</td>
          <td class="py-2.5 px-3 text-slate-400 text-xs">${{g.motivo || '-'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // EXPORTS
    function exportToExcel() {{
      const rows = RAW_DATA.veiculos.map(v => ({{
        "Placa": v.placa,
        "Modelo": v.modelo,
        "Apelido": v.apelido,
        "Status": v.status,
        "Filial": v.filial,
        "Motorista": v.motorista,
        "Combustível (R$)": v.gasto_combustivel,
        "Litros Consumidos": v.litros,
        "Km Rodado": v.km_rodado,
        "Média Km/L": v.media_kml,
        "Manutenção (R$)": v.gasto_manutencao,
        "Pedágio (R$)": v.gasto_pedagio,
        "Custo Total (R$)": v.custo_total,
        "Custo R$/Km": v.km_rodado > 0 ? (v.custo_total / v.km_rodado) : 0
      }}));

      const ws = XLSX.utils.json_to_sheet(rows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Gestao_Frota_GW");
      XLSX.writeFile(wb, "GW_Gestao_Frota_Export.xlsx");
    }}

    function captureSlide() {{
      const target = document.getElementById('capture-area');
      html2canvas(target, {{ backgroundColor: '#0f172a', scale: 2 }}).then(canvas => {{
        const link = document.createElement('a');
        link.download = 'GW_Slide_Gestao_Frota.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
      }});
    }}
  </script>
</body>
</html>
"""

target_path = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Gestao_Frota.html'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Dashboard generated successfully at: {target_path}")

# Also copy to artifact directory
artifact_dir = 'C:/Users/renan.alves/.gemini/antigravity/brain/43bb33b6-6367-463c-94d9-1306168eb162'
artifact_path = os.path.join(artifact_dir, 'dashboard_gestao_frota.html')
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Artifact created at: {artifact_path}")
