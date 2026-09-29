"""
Injetor de Safra de Entradas (SN) no Portal Dashboard_Performance_Operacional_Logistico.html
Atualiza:
  1. const DATA.estoque_parado com os novos dados (incluindo pe, ue, e26, q26, safra).
  2. HTML do painel #acur-sem-giro:
     - Adiciona seletor de Safra de Entrada (SN) ao lado dos filtros de busca e ordenação.
     - Atualiza cabeçalho da tabela com as colunas: 1ª Entrada SN e Última Entrada SN.
  3. JavaScript:
     - Adiciona itemMatchesSafra(it)
     - Atualiza getFilteredEstoqueParadoList()
     - Atualiza renderEstoqueParado() para reagir à Safra de Entrada selecionada
     - Atualiza renderTableEstoqueParado() para renderizar as datas de entrada e badge de safra
     - Atualiza exportEstoqueParadoExcel() com as colunas de safra
"""

import json
import shutil
import re

print("1. Lendo dataset enriquecido com safra de entradas...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/estoque_parado_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

print(f"Dataset carregado com {len(dataset['itens'])} SKUs e {dataset['kpis_gerais']['total_sem_entrada_2026']} sem entrada em 2026.")

print("2. Lendo Dashboard_Performance_Operacional_Logistico.html...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Atualizar const DATA
start_data = html.find('const DATA = ') + len('const DATA = ')
end_data = html.find(';\n', start_data)
if end_data == -1:
    end_data = html.find(';\r\n', start_data)

data_json = json.loads(html[start_data:end_data])
data_json['estoque_parado'] = dataset
new_data_str = json.dumps(data_json, ensure_ascii=False)

html = html[:start_data] + new_data_str + html[end_data:]
print("const DATA atualizado com sucesso!")

# 2. Adicionar o seletor de Safra de Entrada (SN) no HTML dos filtros
old_filter_section = """            <!-- Sort Selector -->
            <div class="flex items-center space-x-2">
              <label class="text-xs text-slate-400 font-semibold whitespace-nowrap">Ordenar por:</label>
              <select id="sort-parado" onchange="paradoCurrentPage=1; renderTableEstoqueParado();" class="text-xs py-2 px-3 rounded-xl bg-slate-900 border border-slate-700 text-amber-300 font-medium focus:outline-none focus:border-blue-500">
                <option value="data-asc" selected>Data Última Venda (Mais Antiga Primeiro - Crítico)</option>
                <option value="valor-desc">Maior Valor Imobilizado (R$ Total)</option>
                <option value="saldo-desc">Maior Saldo Físico Parado</option>
                <option value="data-desc">Data Última Venda (Mais Recente Primeiro)</option>
                <option value="sku-asc">Código SKU (Crescente)</option>
              </select>
            </div>"""

new_filter_section = """            <!-- Safra de Entrada no SN (2025 vs 2026) -->
            <div class="flex items-center space-x-2">
              <label class="text-xs text-amber-300 font-bold whitespace-nowrap flex items-center space-x-1.5">
                <i class="fa-solid fa-calendar-xmark text-amber-400"></i>
                <span>Safra de Entrada (SN):</span>
              </label>
              <select id="filter-parado-safra" onchange="paradoCurrentPage=1; renderEstoqueParado();" class="text-xs py-2 px-3 rounded-xl bg-slate-900 border border-amber-500/50 text-amber-300 font-bold focus:outline-none focus:border-amber-400 shadow-sm">
                <option value="sem-2026" selected>Apenas Entradas até 2025 (Excluir Entradas de 2026)</option>
                <option value="pri-2025">1ª Entrada no SN até 2025 (Exclui Criados em 2026)</option>
                <option value="com-2026">Apenas Entradas em 2026 (Novos / Recebidos 2026)</option>
                <option value="all">Todas as Safras (Visão Geral 100%)</option>
              </select>
            </div>

            <!-- Sort Selector -->
            <div class="flex items-center space-x-2">
              <label class="text-xs text-slate-400 font-semibold whitespace-nowrap">Ordenar por:</label>
              <select id="sort-parado" onchange="paradoCurrentPage=1; renderTableEstoqueParado();" class="text-xs py-2 px-3 rounded-xl bg-slate-900 border border-slate-700 text-amber-300 font-medium focus:outline-none focus:border-blue-500">
                <option value="data-asc" selected>Data Última Venda (Mais Antiga Primeiro - Crítico)</option>
                <option value="valor-desc">Maior Valor Imobilizado (R$ Total)</option>
                <option value="saldo-desc">Maior Saldo Físico Parado</option>
                <option value="data-desc">Data Última Venda (Mais Recente Primeiro)</option>
                <option value="sku-asc">Código SKU (Crescente)</option>
                <option value="pri-ent-asc">1ª Entrada SN (Mais Antiga)</option>
                <option value="ult-ent-desc">Última Entrada SN (Mais Recente)</option>
              </select>
            </div>"""

if 'id="filter-parado-safra"' not in html:
    html = html.replace(old_filter_section, new_filter_section)
    print("Injetado seletor de Safra de Entrada no SN!")

# 3. Atualizar as colunas da tabela no HTML
old_table_header = """                <tr>
                  <th class="py-3 px-3 text-center">#</th>
                  <th class="py-3 px-3">Loja / Filial</th>
                  <th class="py-3 px-3">Cód SKU</th>
                  <th class="py-3 px-4">Descrição do Produto</th>
                  <th class="py-3 px-3 text-right">Saldo Físico Real</th>
                  <th class="py-3 px-3 text-right">Valor Unitário</th>
                  <th class="py-3 px-3 text-right text-amber-400">Valor Total Parado (R$)</th>
                  <th class="py-3 px-3 text-center">Data Última Venda (S7)</th>
                  <th class="py-3 px-3 text-center">Tempo Sem Giro (Aging)</th>
                  <th class="py-3 px-3 text-center">Faixa / Status</th>
                </tr>"""

new_table_header = """                <tr>
                  <th class="py-3 px-3 text-center">#</th>
                  <th class="py-3 px-3">Loja / Filial</th>
                  <th class="py-3 px-3">Cód SKU</th>
                  <th class="py-3 px-4">Descrição do Produto</th>
                  <th class="py-3 px-3 text-right">Saldo Físico Real</th>
                  <th class="py-3 px-3 text-right">Valor Unitário</th>
                  <th class="py-3 px-3 text-right text-amber-400">Valor Total Parado (R$)</th>
                  <th class="py-3 px-3 text-center">1ª Entrada SN</th>
                  <th class="py-3 px-3 text-center">Última Entrada SN</th>
                  <th class="py-3 px-3 text-center">Data Última Venda (S7)</th>
                  <th class="py-3 px-3 text-center">Tempo Sem Giro (Aging)</th>
                  <th class="py-3 px-3 text-center">Safra / Status</th>
                </tr>"""

if '1ª Entrada SN</th>' not in html:
    html = html.replace(old_table_header, new_table_header)
    print("Injetadas novas colunas no cabeçalho da tabela!")

# 4. Injetar a lógica JS para Safra de Entradas
old_js_block = """    function itemMatchesPeriod(it) {
      if (currentPeriodMode === 'all') return true;
      if (currentPeriodMode === '30') return it.dias >= 30;
      if (currentPeriodMode === '60') return it.dias >= 60;
      if (currentPeriodMode === '90') return it.dias >= 90;
      if (currentPeriodMode === '180') return it.dias >= 180;
      if (currentPeriodMode === '365') return it.dias >= 365;
      if (currentPeriodMode === 'sem-venda') return it.dias >= 999;
      if (currentPeriodMode === 'recente') return it.dias < 30;

      if (currentPeriodMode === 'custom') {
        if (customMinDays !== null) return it.dias >= customMinDays;
        if (customMaxDate !== null) {
          if (it.dias >= 999) return true; // sem venda
          return it.dvi <= customMaxDate;
        }
      }
      return true;
    }"""

new_js_block = """    function itemMatchesSafra(it) {
      const safraVal = document.getElementById('filter-parado-safra')?.value || 'sem-2026';
      if (safraVal === 'all') return true;
      if (safraVal === 'sem-2026') return !it.e26; // Desconsiderar tudo que entrou em 2026 (saldo até 2025 / legado)
      if (safraVal === 'pri-2025') return (it.pei && it.pei < '2026-01-01'); // 1ª entrada até 2025
      if (safraVal === 'com-2026') return it.e26; // Teve entrada em 2026
      return true;
    }

    function itemMatchesPeriod(it) {
      if (currentPeriodMode === 'all') return true;
      if (currentPeriodMode === '30') return it.dias >= 30;
      if (currentPeriodMode === '60') return it.dias >= 60;
      if (currentPeriodMode === '90') return it.dias >= 90;
      if (currentPeriodMode === '180') return it.dias >= 180;
      if (currentPeriodMode === '365') return it.dias >= 365;
      if (currentPeriodMode === 'sem-venda') return it.dias >= 999;
      if (currentPeriodMode === 'recente') return it.dias < 30;

      if (currentPeriodMode === 'custom') {
        if (customMinDays !== null) return it.dias >= customMinDays;
        if (customMaxDate !== null) {
          if (it.dias >= 999) return true; // sem venda
          return it.dvi <= customMaxDate;
        }
      }
      return true;
    }"""

if 'function itemMatchesSafra' not in html:
    html = html.replace(old_js_block, new_js_block)
    print("Injetada função itemMatchesSafra(it)!")

# 5. Atualizar getFilteredEstoqueParadoList()
old_filter_list = """      let list = DATA.estoque_parado.itens.filter(it => {
        // 1. Multi-store filter
        if (!selectedStoreIds.includes(it.l)) return false;

        // 2. Period filter
        if (!itemMatchesPeriod(it)) return false;"""

new_filter_list = """      let list = DATA.estoque_parado.itens.filter(it => {
        // 1. Multi-store filter
        if (!selectedStoreIds.includes(it.l)) return false;

        // 2. Safra de Entrada filter (Desconsiderar 2026 / 1ª entrada até 2025)
        if (!itemMatchesSafra(it)) return false;

        // 3. Period filter
        if (!itemMatchesPeriod(it)) return false;"""

if 'itemMatchesSafra(it)' not in html[html.find('function getFilteredEstoqueParadoList'):html.find('function renderEstoqueParado')]:
    html = html.replace(old_filter_list, new_filter_list)
    print("Injetada filtragem por safra em getFilteredEstoqueParadoList!")

# 6. Atualizar ordenação com 1ª entrada e última entrada
old_sort_block = """        } else if (sortVal === 'sku-asc') {
          return a.c - b.c;
        }
        return 0;
      });"""

new_sort_block = """        } else if (sortVal === 'sku-asc') {
          return a.c - b.c;
        } else if (sortVal === 'pri-ent-asc') {
          return (a.pei || '9999').localeCompare(b.pei || '9999');
        } else if (sortVal === 'ult-ent-desc') {
          return (b.uei || '1900').localeCompare(a.uei || '1900');
        }
        return 0;
      });"""

if 'pri-ent-asc' not in html:
    html = html.replace(old_sort_block, new_sort_block)
    print("Injetadas novas opções de ordenação por safra!")

# 7. Atualizar renderEstoqueParado para considerar itemMatchesSafra
old_store_items = """      // Base items in the currently selected stores (having stock > 0)
      const storeItems = DATA.estoque_parado.itens.filter(it => selectedStoreIds.includes(it.l));"""

new_store_items = """      // Base items in the currently selected stores matching the selected Safra (having stock > 0)
      const storeItems = DATA.estoque_parado.itens.filter(it => selectedStoreIds.includes(it.l) && itemMatchesSafra(it));"""

if 'itemMatchesSafra(it)' not in html[html.find('function renderEstoqueParado'):html.find('function renderTableEstoqueParado')]:
    html = html.replace(old_store_items, new_store_items)
    print("Atualizado renderEstoqueParado com filtro de safra ativo!")

# 8. Atualizar linhas da tabela com as novas colunas
old_tr_block = """          <td class="py-2.5 px-3 text-right font-mono font-black text-amber-300 text-sm">
            ${fmtMoeda(it.vt)}
          </td>
          <td class="py-2.5 px-3 text-center font-mono">
            ${isSemVenda 
              ? '<span class="text-rose-400 font-bold bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">Sem Venda na Loja</span>' 
              : `<span class="text-slate-200 font-semibold">${it.dv}</span>`}
          </td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-slate-200 border border-slate-700">
              ${agingStr}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center">
            ${criticidadeBadge}
          </td>"""

new_tr_block = """          <td class="py-2.5 px-3 text-right font-mono font-black text-amber-300 text-sm">
            ${fmtMoeda(it.vt)}
          </td>
          <td class="py-2.5 px-3 text-center font-mono">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700" title="Data da 1ª entrada registrada no SN">
              ${it.pe || 'Legado ≤ 2024'}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center font-mono">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${it.e26 ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}" title="Data da última entrada registrada no SN">
              ${it.ue || 'Legado ≤ 2024'}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center font-mono">
            ${isSemVenda 
              ? '<span class="text-rose-400 font-bold bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">Sem Venda na Loja</span>' 
              : `<span class="text-slate-200 font-semibold">${it.dv}</span>`}
          </td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-slate-200 border border-slate-700">
              ${agingStr}
            </span>
          </td>
          <td class="py-2.5 px-3 text-center">
            ${it.e26 
              ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30" title="Entradas em 2026: +${fmtNum(it.q26)} un">Entrada 2026</span>`
              : `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" title="Material sem nenhuma entrada em 2026">Safra ≤ 2025</span>`}
          </td>"""

if '${it.pe || \'Legado' not in html:
    html = html.replace(old_tr_block, new_tr_block)
    print("Atualizado corpo da tabela com 1ª Entrada, Última Entrada e Safra!")

# 9. Atualizar colunas no exportEstoqueParadoExcel
old_excel_rows = """          "Valor Total Parado (R$)": it.vt,
          "Data Última Venda": it.dv,"""

new_excel_rows = """          "Valor Total Parado (R$)": it.vt,
          "1ª Entrada no SN": it.pe || "Legado ≤ 2024",
          "Última Entrada no SN": it.ue || "Legado ≤ 2024",
          "Entradas em 2026": it.e26 ? "Sim (" + it.q26 + " un)" : "Não",
          "Safra do Material": it.e26 ? "Entrada em 2026" : "Entrada até 2025 (Legado)",
          "Data Última Venda": it.dv,"""

if '"1ª Entrada no SN"' not in html:
    html = html.replace(old_excel_rows, new_excel_rows)
    print("Atualizado exportEstoqueParadoExcel com as colunas de safra de entrada!")

# Salvar HTML atualizado
output_path = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Arquivo local salvo com sucesso: {output_path} ({len(html)/(1024*1024):.2f} MB)")

# Atualizar artefato
artifact_path = r'C:\Users\renan.alves\.gemini\antigravity\brain\43bb33b6-6367-463c-94d9-1306168eb162\dashboard_performance_operacional_logistico.html'
shutil.copyfile(output_path, artifact_path)
print(f"Artefato sincronizado em: {artifact_path}")
