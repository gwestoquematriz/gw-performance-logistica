import os
import json
import re

print("Loading dataset: estoque_parado_dataset.json...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/estoque_parado_dataset.json', 'r', encoding='utf-8') as f:
    parado_raw = json.load(f)

# Compact the items to optimize JSON size while keeping all data
compact_items = []
for it in parado_raw['itens']:
    compact_items.append({
        'c': it['cod_produto'],
        'e': it['cod_empresa'],
        'l': it['loja_id'],
        'd': it['descricao_produto'],
        'u': it['unidade'],
        'sf': it['saldo_fisico'],
        'sr': it['saldo_reservado'],
        'sd': it['saldo_disponivel'],
        'dv': it['data_ultima_venda'],
        'dias': it['dias_sem_venda'],
        'vu': it['valor_unitario'],
        'vt': it['valor_total_parado'],
        'st': it['status_venda']
    })

estoque_parado_payload = {
    'data_extracao': parado_raw['data_extracao'],
    'kpis_gerais': parado_raw['kpis_gerais'],
    'resumo_por_filial': parado_raw['resumo_por_filial'],
    'itens': compact_items
}

print(f"Compact items prepared: {len(compact_items)} SKUs.")

print("Reading Dashboard_Performance_Operacional_Logistico.html...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update const DATA
start_data = html.find('const DATA = ') + len('const DATA = ')
end_data = html.find(';\n', start_data)

data_json = json.loads(html[start_data:end_data])
data_json['estoque_parado'] = estoque_parado_payload
new_data_str = json.dumps(data_json, ensure_ascii=False)

html = html[:start_data] + new_data_str + html[end_data:]
print("Updated const DATA with estoque_parado!")

# 2. Add Sub-tab button in view-acuracidade header
old_button_anchor = """          <button onclick="switchAcuracidadeTab('acur-6lojas')" id="btn-acur-6lojas" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            7. Comparativo 6 Lojas
          </button>"""

new_button = """          <button onclick="switchAcuracidadeTab('acur-6lojas')" id="btn-acur-6lojas" class="sub-tab-btn px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 border border-slate-700 transition">
            7. Comparativo 6 Lojas
          </button>
          <button onclick="switchAcuracidadeTab('acur-sem-giro')" id="btn-acur-sem-giro" class="sub-tab-btn px-3 py-1 text-xs font-bold rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30 transition flex items-center space-x-1.5 shadow-sm">
            <i class="fa-solid fa-hourglass-half text-amber-400"></i>
            <span>8. Itens Sem Giro & Aging</span>
          </button>"""

if 'id="btn-acur-sem-giro"' not in html:
    html = html.replace(old_button_anchor, new_button)
    print("Added sub-tab button '8. Itens Sem Giro & Aging'!")

# 3. Build HTML for #acur-sem-giro panel
sem_giro_panel = """      <!-- ACURACIDADE SUB-PANEL 8: ITENS SEM GIRO, AGING & CAPITAL IMOBILIZADO -->
      <div id="acur-sem-giro" class="acur-sub-panel hidden space-y-6">

        <!-- Top Header Banner -->
        <div class="glass-card rounded-2xl p-6 border border-amber-500/40 bg-gradient-to-r from-amber-950/30 via-slate-900/70 to-slate-900/70 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-2xl shrink-0 shadow-lg shadow-amber-500/10 border border-amber-500/30">
              <i class="fa-solid fa-hourglass-half"></i>
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  <i class="fa-solid fa-triangle-exclamation mr-1.5"></i> AUDITORIA CRÍTICA DE GIRO
                </span>
                <span class="text-xs text-slate-400">PostgreSQL 17.6 + Kardex ERP S7</span>
              </div>
              <h3 class="text-xl font-extrabold text-white mt-1">Itens Sem Giro, Aging & Capital Imobilizado</h3>
              <p class="text-xs text-slate-300">
                Auditoria de SKUs estagnados com histórico de última venda, aging detalhado (meses e anos) e valor total imobilizado por filial. Ordenado rigorosamente com a <strong>data de venda mais antiga no topo</strong>.
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <button onclick="exportEstoqueParadoExcel()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition flex items-center space-x-2">
              <i class="fa-solid fa-file-excel"></i>
              <span>Exportar Estoque Parado (Excel)</span>
            </button>
            <button onclick="scrollToActionPlan()" class="px-3.5 py-2 rounded-xl bg-indigo-600/30 hover:bg-indigo-600/50 text-indigo-300 font-bold text-xs border border-indigo-500/30 transition flex items-center space-x-2">
              <i class="fa-solid fa-lightbulb"></i>
              <span>Plano Fila Cega WMS</span>
            </button>
          </div>
        </div>

        <!-- Dynamic KPI Cards (Reacts to Multi-Store Filter) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
            <div class="flex items-center justify-between">
              <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Capital Imobilizado</span>
              <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center text-sm">
                <i class="fa-solid fa-coins"></i>
              </div>
            </div>
            <div class="text-2xl font-black text-amber-400 mt-2" id="kpi-parado-valor">R$ 0,00</div>
            <span class="text-[11px] text-slate-400 mt-1 block">Saldo Físico &times; Valor Unitário</span>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
            <div class="flex items-center justify-between">
              <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">SKUs Parados com Saldo</span>
              <div class="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center text-sm">
                <i class="fa-solid fa-boxes-stacked"></i>
              </div>
            </div>
            <div class="text-2xl font-black text-white mt-2" id="kpi-parado-skus">0 SKUs</div>
            <span class="text-[11px] text-slate-400 mt-1 block" id="kpi-parado-unidades">0 unidades físicas retidas</span>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
            <div class="flex items-center justify-between">
              <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Sem Venda na Filial</span>
              <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center text-sm">
                <i class="fa-solid fa-skull-crossbones"></i>
              </div>
            </div>
            <div class="text-2xl font-black text-rose-400 mt-2" id="kpi-parado-sem-venda">0 SKUs</div>
            <span class="text-[11px] text-rose-300/80 mt-1 block">Maior criticidade • > 2 anos ou nunca vendeu</span>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
            <div class="flex items-center justify-between">
              <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">&gt; 1 Ano Parado</span>
              <div class="w-8 h-8 rounded-lg bg-red-500/20 text-red-400 flex items-center justify-center text-sm">
                <i class="fa-solid fa-clock-rotate-left"></i>
              </div>
            </div>
            <div class="text-2xl font-black text-red-400 mt-2" id="kpi-parado-mais-1ano">0 SKUs</div>
            <span class="text-[11px] text-red-300/80 mt-1 block" id="kpi-parado-pct-critico">0% do acervo das filiais selecionadas</span>
          </div>
        </div>

        <!-- Aging Distribution Progress Bar -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
          <div class="flex items-center justify-between flex-wrap gap-2 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
              <i class="fa-solid fa-chart-simple text-blue-400"></i>
              <span>Distribuição de Aging do Estoque Parado (Lojas Selecionadas):</span>
            </span>
            <div class="flex items-center space-x-4 text-[11px] text-slate-400 flex-wrap gap-y-1">
              <span class="flex items-center"><span class="w-2.5 h-2.5 rounded-full bg-rose-600 mr-1.5"></span> Sem Venda / &gt; 2 Anos</span>
              <span class="flex items-center"><span class="w-2.5 h-2.5 rounded-full bg-red-500 mr-1.5"></span> &gt; 1 Ano</span>
              <span class="flex items-center"><span class="w-2.5 h-2.5 rounded-full bg-amber-500 mr-1.5"></span> 6 a 12 Meses</span>
              <span class="flex items-center"><span class="w-2.5 h-2.5 rounded-full bg-blue-500 mr-1.5"></span> 3 a 6 Meses</span>
              <span class="flex items-center"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 mr-1.5"></span> &lt; 90 Dias</span>
            </div>
          </div>

          <div class="w-full h-3.5 rounded-full bg-slate-800/80 overflow-hidden flex shadow-inner" id="aging-bar-container">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Interactive Filters and Search Bar -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-4">
            
            <!-- Search SKU or Description -->
            <div class="relative flex-1 min-w-[280px]">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3 text-slate-500 text-xs"></i>
              <input type="text" id="search-parado" oninput="paradoCurrentPage=1; renderTableEstoqueParado();" placeholder="Filtrar por Código SKU, Descrição do Produto, Categoria..." class="w-full pl-9 pr-4 py-2 text-xs rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition">
            </div>

            <!-- Aging / Criticidade Selector -->
            <div class="flex items-center space-x-2">
              <label class="text-xs text-slate-400 font-semibold whitespace-nowrap">Faixa de Aging:</label>
              <select id="filter-parado-aging" onchange="paradoCurrentPage=1; renderTableEstoqueParado();" class="text-xs py-2 px-3 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                <option value="all">Todas as Faixas de Tempo</option>
                <option value="sem-venda">Crítico: Sem Venda na Loja (&gt; 2 Anos)</option>
                <option value="ano">Alto Risco: &gt; 1 Ano Parado</option>
                <option value="semestre">Alerta: 6 a 12 Meses Parado</option>
                <option value="trimestre">Atenção: 3 a 6 Meses Parado</option>
                <option value="recente">Giro Recente (&lt; 90 Dias)</option>
              </select>
            </div>

            <!-- Sort Selector -->
            <div class="flex items-center space-x-2">
              <label class="text-xs text-slate-400 font-semibold whitespace-nowrap">Ordenar por:</label>
              <select id="sort-parado" onchange="paradoCurrentPage=1; renderTableEstoqueParado();" class="text-xs py-2 px-3 rounded-xl bg-slate-900 border border-slate-700 text-amber-300 font-medium focus:outline-none focus:border-blue-500">
                <option value="data-asc">Data Última Venda (Mais Antiga Primeiro - Crítico)</option>
                <option value="valor-desc">Maior Valor Imobilizado (R$ Total)</option>
                <option value="saldo-desc">Maior Saldo Físico Parado</option>
                <option value="data-desc">Data Última Venda (Mais Recente)</option>
                <option value="sku-asc">Código SKU (Crescente)</option>
              </select>
            </div>

            <!-- Page Size -->
            <div class="flex items-center space-x-2">
              <label class="text-xs text-slate-400 font-semibold whitespace-nowrap">Itens / pág:</label>
              <select id="select-parado-pagesize" onchange="paradoPageSize=parseInt(this.value); paradoCurrentPage=1; renderTableEstoqueParado();" class="text-xs py-2 px-3 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                <option value="25">25</option>
                <option value="50" selected>50</option>
                <option value="100">100</option>
                <option value="200">200</option>
              </select>
            </div>

          </div>

          <!-- Active Filter Status -->
          <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/80 flex-wrap gap-2">
            <div id="parado-results-count">Exibindo 0 itens</div>
            <div class="flex items-center space-x-2" id="parado-pagination-controls">
              <!-- Pagination buttons -->
            </div>
          </div>

          <!-- Main Table -->
          <div class="overflow-x-auto rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 uppercase font-semibold text-[11px] border-b border-slate-800">
                <tr>
                  <th class="py-3 px-3 text-center">#</th>
                  <th class="py-3 px-3">Loja / Filial</th>
                  <th class="py-3 px-3">Cód SKU</th>
                  <th class="py-3 px-4">Descrição do Produto</th>
                  <th class="py-3 px-3 text-right">Saldo Físico</th>
                  <th class="py-3 px-3 text-right">Valor Unitário</th>
                  <th class="py-3 px-3 text-right text-amber-400">Valor Total Parado (R$)</th>
                  <th class="py-3 px-3 text-center">Data Última Venda</th>
                  <th class="py-3 px-3 text-center">Tempo Parado (Aging)</th>
                  <th class="py-3 px-3 text-center">Criticidade / Status</th>
                </tr>
              </thead>
              <tbody id="tbody-estoque-parado" class="divide-y divide-slate-800/50">
                <!-- Dynamically generated rows -->
              </tbody>
            </table>
          </div>

          <!-- Bottom Pagination Controls -->
          <div class="flex items-center justify-between text-xs text-slate-400 pt-2 flex-wrap gap-2">
            <div id="parado-bottom-summary">Página 1 de 1</div>
            <div class="flex items-center space-x-1" id="parado-bottom-pagination">
              <!-- Injected via JS -->
            </div>
          </div>

        </div>

        <!-- PLANO DE AÇÃO ESTRATÉGICO: FILA CEGA & TAKT TIME WMS -->
        <div id="section-action-plan" class="glass-card rounded-2xl p-6 border border-indigo-500/40 bg-gradient-to-br from-indigo-950/20 via-slate-900/80 to-slate-900/80 space-y-6">
          <div class="flex items-center justify-between flex-wrap gap-4 pb-4 border-b border-slate-800">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-xl border border-indigo-500/30">
                <i class="fa-solid fa-gears"></i>
              </div>
              <div>
                <h3 class="text-base font-bold text-white flex items-center space-x-2">
                  <span>Plano de Ação Estratégico: Parametrização da "Fila Cega" & Takt Time no WMS</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Diretriz Operacional</span>
                </h3>
                <p class="text-xs text-slate-400">Eliminação do "cherry-picking" (escolha de pedidos fáceis), balanceamento sequencial de rotas e padronização operacional.</p>
              </div>
            </div>
            <span class="text-xs text-slate-400 font-mono">Módulo WMS Despacho & Expedição</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <!-- Card 1: Parametrização da Fila Cega -->
            <div class="rounded-xl p-5 bg-slate-900/80 border border-slate-800 space-y-4">
              <div class="flex items-center space-x-3 text-indigo-400 font-bold text-sm">
                <div class="w-7 h-7 rounded-lg bg-indigo-500/20 flex items-center justify-center text-xs">1</div>
                <h4>Como Parametrizar a "Fila Cega" no WMS</h4>
              </div>
              <div class="space-y-3 text-xs text-slate-300">
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">Modo de Atribuição de Tarefas:</span>
                  <p class="text-slate-400">Mudar de: <span class="text-rose-400 line-through">Seleção Livre / Lista Aberta pelo Operador</span></p>
                  <p class="text-emerald-400 font-semibold mt-0.5">Para: Distribuição Automática Sequencial (Fila Cega / Round-Robin).</p>
                </div>
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">Critério de Ordenação da Fila:</span>
                  <ul class="space-y-1 list-disc list-inside text-slate-300">
                    <li><strong class="text-white">Horário de Corte / Saída do Romaneio:</strong> Pedidos do caminhão das 14h têm prioridade absoluta sobre o das 17h.</li>
                    <li><strong class="text-white">Zoneamento de Corredor:</strong> Algoritmo evita cruzar 4 operadores na mesma rua simultaneamente.</li>
                  </ul>
                </div>
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">Trava de Rejeição de Tarefa no Coletor:</span>
                  <p class="text-slate-300">O operador não pode cancelar ou pular a ordem atribuída no coletor RF. Troca de tarefa exige <strong>senha de supervisor/encarregado</strong>.</p>
                </div>
              </div>
            </div>

            <!-- Card 2: POP do Encarregado -->
            <div class="rounded-xl p-5 bg-slate-900/80 border border-slate-800 space-y-4">
              <div class="flex items-center space-x-3 text-cyan-400 font-bold text-sm">
                <div class="w-7 h-7 rounded-lg bg-cyan-500/20 flex items-center justify-center text-xs">2</div>
                <h4>Procedimento Operacional Padrão (POP)</h4>
              </div>
              <div class="space-y-3 text-xs text-slate-300">
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">1. Início do Turno (Check-in):</span>
                  <p class="text-slate-300">Operador loga no coletor RF e bipa na estação de trabalho. O encarregado valida operadores ativos na tela de despacho.</p>
                </div>
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">2. Monitoramento em Tempo Real:</span>
                  <p class="text-slate-300">Acompanhar o painel de despacho do WMS para identificar gargalos e desvios de ritmo em relação ao horário de corte do romaneio.</p>
                </div>
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">3. Tratativa de Exceções & Furos:</span>
                  <p class="text-slate-300">Se o endereço apontar furo físico, encarregado valida a divergência no WMS e ativa a compensação com loja com sobra.</p>
                </div>
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">4. Auditoria de Encerramento:</span>
                  <p class="text-slate-300">Fechamento dos romaneios expedidos, conferência de volumes carregados e liberação do veículo para a portaria.</p>
                </div>
              </div>
            </div>

            <!-- Card 3: Takt Time & Produtividade -->
            <div class="rounded-xl p-5 bg-slate-900/80 border border-slate-800 space-y-4">
              <div class="flex items-center space-x-3 text-amber-400 font-bold text-sm">
                <div class="w-7 h-7 rounded-lg bg-amber-500/20 flex items-center justify-center text-xs">3</div>
                <h4>Takt Time Alvo & Produtividade no WMS</h4>
              </div>
              <div class="space-y-3 text-xs text-slate-300">
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-2">Takt Time Padrão por Tipologia:</span>
                  <div class="space-y-2">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-1">
                      <span>📦 Miudezas (Conectores/Abraçadeiras):</span>
                      <strong class="text-emerald-400 font-mono">30 a 45 seg / linha</strong>
                    </div>
                    <div class="flex items-center justify-between border-b border-slate-800 pb-1">
                      <span>📡 Roteadores / ONTs / Caixas CTO:</span>
                      <strong class="text-blue-400 font-mono">15 a 20 seg / un</strong>
                    </div>
                    <div class="flex items-center justify-between">
                      <span>🏗️ Bobinas / Cabos / Paletes:</span>
                      <strong class="text-amber-400 font-mono">2 a 3 min / item</strong>
                    </div>
                  </div>
                </div>
                <div class="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
                  <span class="font-bold text-white block mb-1">Impactos Operacionais Esperados:</span>
                  <ul class="space-y-1 list-disc list-inside text-slate-300">
                    <li><span class="text-emerald-400 font-semibold">+35% de produtividade global</span> ao eliminar o tempo ocioso entre ordens.</li>
                    <li><span class="text-blue-400 font-semibold">100% dos romaneios</span> despachados dentro da janela do horário de corte.</li>
                    <li><span class="text-cyan-400 font-semibold">Auditoria transparente</span> de desempenho individual sem distorções por tipo de pedido.</li>
                  </ul>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
"""

# Insert panel before </section> of view-acuracidade
if 'id="acur-sem-giro"' not in html:
    insert_point = html.find('</section>\n\n    <!-- ======================================================== -->\n    <!-- VIEW 3: CUSTO DE TRANSPORTE')
    if insert_point == -1:
        insert_point = html.find('<section id="view-transporte"')
        # find preceding </section>
        insert_point = html.rfind('</section>', 0, insert_point)
    
    html = html[:insert_point] + sem_giro_panel + "\n    " + html[insert_point:]
    print("Injected #acur-sem-giro HTML panel!")

# 4. Add JavaScript logic for Estoque Parado
js_estoque_parado = """
    // ==========================================
    // MODULE: ITENS SEM GIRO, AGING & CAPITAL IMOBILIZADO
    // ==========================================
    let paradoCurrentPage = 1;
    let paradoPageSize = 50;

    const STORE_LABELS = {
      12: { nome: 'GW Matriz', lojas: 'Lojas 1 e 8', badge: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
      9:  { nome: 'GW Goiânia', lojas: 'Lojas 6 e 90', badge: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
      8:  { nome: 'GW Brasília', lojas: 'Lojas 9 e 91', badge: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30' },
      11: { nome: 'GW Palmas', lojas: 'Lojas 10 e 11', badge: 'bg-amber-500/20 text-amber-400 border-amber-500/30' },
      10: { nome: 'GW Marabá', lojas: 'Lojas 7 e 92', badge: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
      7:  { nome: 'GW São Luís', lojas: 'Loja 14', badge: 'bg-rose-500/20 text-rose-400 border-rose-500/30' }
    };

    function getAgingFormatted(dias) {
      if (dias >= 999) return 'Sem Giro (> 2 anos / Origem)';
      const anos = Math.floor(dias / 365);
      const meses = Math.floor((dias % 365) / 30);
      if (anos > 0) {
        return `${anos} ano${anos > 1 ? 's' : ''}${meses > 0 ? ' e ' + meses + (meses === 1 ? ' mês' : ' meses') : ''}`;
      }
      if (meses > 0) return `${meses} ${meses === 1 ? 'mês' : 'meses'}`;
      return `${dias} dias`;
    }

    function getCriticidadeBadgeHTML(dias) {
      if (dias >= 999) {
        return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">Crítico: Sem Venda</span>';
      } else if (dias >= 365) {
        return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30">Alto Risco: > 1 Ano</span>';
      } else if (dias >= 180) {
        return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Alerta: 6 a 12 Meses</span>';
      } else if (dias >= 90) {
        return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">Atenção: 3 a 6 Meses</span>';
      } else {
        return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Giro Recente (< 90d)</span>';
      }
    }

    function scrollToActionPlan() {
      const el = document.getElementById('section-action-plan');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }

    function getFilteredEstoqueParadoList() {
      if (!DATA.estoque_parado || !DATA.estoque_parado.itens) return [];
      
      const term = (document.getElementById('search-parado')?.value || '').toLowerCase().trim();
      const agingFilter = document.getElementById('filter-parado-aging')?.value || 'all';
      const sortVal = document.getElementById('sort-parado')?.value || 'data-asc';

      let list = DATA.estoque_parado.itens.filter(it => {
        // Multi-store filter
        if (!selectedStoreIds.includes(it.l)) return false;

        // Search term
        if (term) {
          const matchSku = String(it.c).includes(term);
          const matchDesc = it.d.toLowerCase().includes(term);
          const matchUn = it.u.toLowerCase().includes(term);
          if (!matchSku && !matchDesc && !matchUn) return false;
        }

        // Aging filter
        if (agingFilter === 'sem-venda') return it.dias >= 999;
        if (agingFilter === 'ano') return it.dias >= 365 && it.dias < 999;
        if (agingFilter === 'semestre') return it.dias >= 180 && it.dias < 365;
        if (agingFilter === 'trimestre') return it.dias >= 90 && it.dias < 180;
        if (agingFilter === 'recente') return it.dias < 90;

        return true;
      });

      // Sort
      list.sort((a, b) => {
        if (sortVal === 'data-asc') {
          // Oldest sale date first (999 days / null sales first, then oldest dates)
          if (a.dias >= 999 && b.dias < 999) return -1;
          if (a.dias < 999 && b.dias >= 999) return 1;
          if (a.dias !== b.dias) return b.dias - a.dias; // bigger dias = older sale
          return b.vt - a.vt;
        } else if (sortVal === 'data-desc') {
          return a.dias - b.dias;
        } else if (sortVal === 'valor-desc') {
          return b.vt - a.vt;
        } else if (sortVal === 'saldo-desc') {
          return b.sf - a.sf;
        } else if (sortVal === 'sku-asc') {
          return a.c - b.c;
        }
        return 0;
      });

      return list;
    }

    function renderEstoqueParado() {
      if (!DATA.estoque_parado) return;

      // Calculate KPIs for all items in the currently selected stores (unfiltered by text search)
      const storeItems = DATA.estoque_parado.itens.filter(it => selectedStoreIds.includes(it.l));
      
      let totalValor = 0;
      let totalUnidades = 0;
      let countSemVenda = 0;
      let countMais1Ano = 0;
      let countSemestre = 0;
      let countTrimestre = 0;
      let countRecente = 0;

      storeItems.forEach(it => {
        totalValor += it.vt;
        totalUnidades += it.sf;
        if (it.dias >= 999) countSemVenda++;
        else if (it.dias >= 365) countMais1Ano++;
        else if (it.dias >= 180) countSemestre++;
        else if (it.dias >= 90) countTrimestre++;
        else countRecente++;
      });

      const totalCriticos = countSemVenda + countMais1Ano;
      const pctCritico = storeItems.length > 0 ? ((totalCriticos / storeItems.length) * 100).toFixed(1) : 0;

      // Update KPI DOM
      const elVal = document.getElementById('kpi-parado-valor');
      const elSkus = document.getElementById('kpi-parado-skus');
      const elUn = document.getElementById('kpi-parado-unidades');
      const elSemV = document.getElementById('kpi-parado-sem-venda');
      const elAno = document.getElementById('kpi-parado-mais-1ano');
      const elPct = document.getElementById('kpi-parado-pct-critico');

      if (elVal) elVal.textContent = fmtMoeda(totalValor);
      if (elSkus) elSkus.textContent = `${fmtNum(storeItems.length)} SKUs`;
      if (elUn) elUn.textContent = `${fmtNum(totalUnidades)} unidades físicas retidas`;
      if (elSemV) elSemV.textContent = `${fmtNum(countSemVenda)} SKUs`;
      if (elAno) elAno.textContent = `${fmtNum(countMais1Ano)} SKUs`;
      if (elPct) elPct.textContent = `${pctCritico}% do acervo parado (> 1 ano ou sem venda)`;

      // Render Aging Progress Bar
      const barContainer = document.getElementById('aging-bar-container');
      if (barContainer && storeItems.length > 0) {
        const pSemVenda = (countSemVenda / storeItems.length) * 100;
        const pAno = (countMais1Ano / storeItems.length) * 100;
        const pSemestre = (countSemestre / storeItems.length) * 100;
        const pTrimestre = (countTrimestre / storeItems.length) * 100;
        const pRecente = (countRecente / storeItems.length) * 100;

        barContainer.innerHTML = `
          <div class="h-full bg-rose-600 transition-all duration-500" style="width: ${pSemVenda}%" title="Sem Venda / > 2 Anos: ${countSemVenda} SKUs (${pSemVenda.toFixed(1)}%)"></div>
          <div class="h-full bg-red-500 transition-all duration-500" style="width: ${pAno}%" title="> 1 Ano Parado: ${countMais1Ano} SKUs (${pAno.toFixed(1)}%)"></div>
          <div class="h-full bg-amber-500 transition-all duration-500" style="width: ${pSemestre}%" title="6 a 12 Meses: ${countSemestre} SKUs (${pSemestre.toFixed(1)}%)"></div>
          <div class="h-full bg-blue-500 transition-all duration-500" style="width: ${pTrimestre}%" title="3 a 6 Meses: ${countTrimestre} SKUs (${pTrimestre.toFixed(1)}%)"></div>
          <div class="h-full bg-emerald-500 transition-all duration-500" style="width: ${pRecente}%" title="Giro Recente (< 90d): ${countRecente} SKUs (${pRecente.toFixed(1)}%)"></div>
        `;
      }

      renderTableEstoqueParado();
    }

    function renderTableEstoqueParado() {
      const list = getFilteredEstoqueParadoList();
      const total = list.length;
      const totalPages = Math.max(1, Math.ceil(total / paradoPageSize));

      if (paradoCurrentPage > totalPages) paradoCurrentPage = totalPages;
      if (paradoCurrentPage < 1) paradoCurrentPage = 1;

      const startIdx = (paradoCurrentPage - 1) * paradoPageSize;
      const endIdx = Math.min(startIdx + paradoPageSize, total);
      const pageItems = list.slice(startIdx, endIdx);

      // Status text
      const countEl = document.getElementById('parado-results-count');
      if (countEl) {
        countEl.innerHTML = `Mostrando <strong>${total > 0 ? startIdx + 1 : 0} &ndash; ${endIdx}</strong> de <strong>${fmtNum(total)}</strong> itens parados filtrados`;
      }

      const summaryEl = document.getElementById('parado-bottom-summary');
      if (summaryEl) {
        summaryEl.textContent = `Página ${paradoCurrentPage} de ${totalPages} (${fmtNum(total)} registros)`;
      }

      // Render pagination buttons
      const renderPagination = (containerId) => {
        const cont = document.getElementById(containerId);
        if (!cont) return;
        cont.innerHTML = `
          <button onclick="changeParadoPage(1)" ${paradoCurrentPage === 1 ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:bg-slate-800 text-slate-300"'} class="px-2.5 py-1 text-xs rounded-lg border border-slate-700">« Primeira</button>
          <button onclick="changeParadoPage(${paradoCurrentPage - 1})" ${paradoCurrentPage === 1 ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:bg-slate-800 text-slate-300"'} class="px-2.5 py-1 text-xs rounded-lg border border-slate-700">‹ Anterior</button>
          <span class="px-3 py-1 text-xs font-bold text-amber-300 bg-slate-900 border border-slate-700 rounded-lg">${paradoCurrentPage} / ${totalPages}</span>
          <button onclick="changeParadoPage(${paradoCurrentPage + 1})" ${paradoCurrentPage >= totalPages ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:bg-slate-800 text-slate-300"'} class="px-2.5 py-1 text-xs rounded-lg border border-slate-700">Próxima ›</button>
          <button onclick="changeParadoPage(${totalPages})" ${paradoCurrentPage >= totalPages ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:bg-slate-800 text-slate-300"'} class="px-2.5 py-1 text-xs rounded-lg border border-slate-700">Última »</button>
        `;
      };
      renderPagination('parado-pagination-controls');
      renderPagination('parado-bottom-pagination');

      // Render Table Body
      const tbody = document.getElementById('tbody-estoque-parado');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (pageItems.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="10" class="py-12 text-center text-slate-400">
              <i class="fa-solid fa-box-open text-3xl mb-2 block text-slate-600"></i>
              Nenhum produto encontrado com os filtros selecionados.
            </td>
          </tr>
        `;
        return;
      }

      pageItems.forEach((it, idx) => {
        const globalRank = startIdx + idx + 1;
        const store = STORE_LABELS[it.l] || { nome: 'Filial ' + it.l, lojas: 'Loja ' + it.e, badge: 'bg-slate-800 text-slate-300' };
        const agingStr = getAgingFormatted(it.dias);
        const criticidadeBadge = getCriticidadeBadgeHTML(it.dias);

        const isSemVenda = it.dias >= 999;
        const isCritico = it.dias >= 365;

        const tr = document.createElement('tr');
        tr.className = `hover:bg-slate-800/40 transition ${isSemVenda ? 'bg-rose-950/10' : isCritico ? 'bg-red-950/5' : ''}`;
        tr.innerHTML = `
          <td class="py-2.5 px-3 text-center font-bold text-slate-500">#${globalRank}</td>
          <td class="py-2.5 px-3">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold border ${store.badge}">
              ${store.nome}
            </span>
            <span class="block text-[10px] text-slate-500 mt-0.5">${store.lojas}</span>
          </td>
          <td class="py-2.5 px-3 font-mono font-bold text-blue-400">#${it.c}</td>
          <td class="py-2.5 px-4 font-medium text-white max-w-xs truncate" title="${it.d}">
            ${it.d}
            <span class="block text-[10px] text-slate-400">${it.st}</span>
          </td>
          <td class="py-2.5 px-3 text-right font-extrabold text-slate-200">
            ${fmtNum(it.sf)} <span class="text-[10px] text-slate-400 font-normal">${it.u}</span>
          </td>
          <td class="py-2.5 px-3 text-right text-slate-300 font-mono">
            ${fmtMoeda(it.vu)}
          </td>
          <td class="py-2.5 px-3 text-right font-mono font-black text-amber-300 text-sm">
            ${fmtMoeda(it.vt)}
          </td>
          <td class="py-2.5 px-3 text-center font-mono">
            ${isSemVenda 
              ? '<span class="text-rose-400 font-bold bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">Sem Venda na Loja</span>' 
              : `<span class="text-slate-300 font-semibold">${it.dv}</span>`}
          </td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-slate-200 border border-slate-700">
              ${agingStr}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center">
            ${criticidadeBadge}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function changeParadoPage(page) {
      paradoCurrentPage = page;
      renderTableEstoqueParado();
      const el = document.getElementById('search-parado');
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function exportEstoqueParadoExcel() {
      const list = getFilteredEstoqueParadoList();
      if (!list || list.length === 0) {
        alert("Nenhum item filtrado para exportar.");
        return;
      }

      const rows = list.map((it, idx) => {
        const store = STORE_LABELS[it.l] || { nome: 'Filial ' + it.l, lojas: 'Loja ' + it.e };
        return {
          "Rank": idx + 1,
          "Filial": store.nome,
          "Lojas ERP S7": store.lojas,
          "Código SKU": it.c,
          "Descrição do Produto": it.d,
          "Unidade": it.u,
          "Saldo Físico": it.sf,
          "Saldo Reservado": it.sr,
          "Saldo Disponível": it.sd,
          "Valor Unitário (R$)": it.vu,
          "Valor Total Parado (R$)": it.vt,
          "Data Última Venda": it.dv,
          "Dias Sem Venda": it.dias >= 999 ? "Sem Registro (> 2 anos)" : it.dias,
          "Tempo Parado (Aging)": getAgingFormatted(it.dias),
          "Status da Venda": it.st
        };
      });

      const ws = XLSX.utils.json_to_sheet(rows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Estoque_Parado_Aging");
      
      const now = new Date();
      const dateStr = now.toISOString().slice(0, 10);
      XLSX.writeFile(wb, `GW_Estoque_Parado_Aging_Audit_${dateStr}.xlsx`);
    }
"""

# Inject JS before applyAcuracidadeFilters
if 'getFilteredEstoqueParadoList' not in html:
    anchor_js = "function applyAcuracidadeFilters() {"
    replacement_js = js_estoque_parado + "\n\n    function applyAcuracidadeFilters() {\n      renderEstoqueParado();"
    html = html.replace(anchor_js, replacement_js)
    print("Injected JavaScript logic for Estoque Parado!")

# Also ensure DOMContentLoaded calls renderEstoqueParado
if 'renderEstoqueParado();' not in html[html.find("document.addEventListener('DOMContentLoaded'"):html.find("renderTransporteView();")]:
    dom_anchor = "renderAcuracidadeKPIs();"
    # replace first occurrence after DOMContentLoaded
    dom_idx = html.find("document.addEventListener('DOMContentLoaded'")
    sub_idx = html.find("applyAcuracidadeFilters();", dom_idx)
    # applyAcuracidadeFilters already calls renderEstoqueParado(), so that's covered!

# Update Hub Card 2 to highlight the new feature
hub_card_anchor = """            <ul class="text-xs text-slate-300 space-y-1.5 pt-1">
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-triangle-exclamation text-rose-400 text-[10px]"></i>
                <span>Reservas & Furos de Estoque com Loja com Sobra</span>
              </li>"""

hub_card_new = """            <ul class="text-xs text-slate-300 space-y-1.5 pt-1">
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-hourglass-half text-amber-400 text-[10px]"></i>
                <span class="font-bold text-amber-300">Itens Sem Giro / Aging & Capital Imobilizado</span>
              </li>
              <li class="flex items-center space-x-2">
                <i class="fa-solid fa-triangle-exclamation text-rose-400 text-[10px]"></i>
                <span>Reservas & Furos de Estoque com Loja com Sobra</span>
              </li>"""

if 'font-bold text-amber-300">Itens Sem Giro' not in html:
    html = html.replace(hub_card_anchor, hub_card_new)
    print("Updated Hub Card 2 with 'Itens Sem Giro' highlight!")

output_html = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html'
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Updated {output_html} successfully! New size: {len(html) / (1024*1024):.2f} MB")
