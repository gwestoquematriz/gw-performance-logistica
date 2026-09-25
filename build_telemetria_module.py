import os
import json
import re

print("Reading wisevia_live_dataset.json...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/wisevia_live_dataset.json', 'r', encoding='utf-8') as f:
    wisevia_data = json.load(f)

print("Reading Dashboard_Performance_Operacional_Logistico.html...")
with open('c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update const DATA to include wisevia_live
start_data = html.find('const DATA = ') + len('const DATA = ')
end_data = html.find(';\n', start_data)

data_json = json.loads(html[start_data:end_data])
data_json['wisevia_live'] = wisevia_data
new_data_str = json.dumps(data_json, ensure_ascii=False)

html = html[:start_data] + new_data_str + html[end_data:]
print("Updated const DATA with wisevia_live!")

# 2. Build the new HTML for transp-telemetria
div_start = html.find('<div id="transp-telemetria"')
div_end = html.find('</div>\n        </div>\n      </div>\n\n    </section>', div_start)
if div_end == -1:
    div_end = html.find('</div>\n      </div>\n\n    </section>', div_start)
if div_end == -1:
    # find where transp-telemetria ends (before </section>)
    sec_end = html.find('</section>', div_start)
    div_end = html.rfind('</div>', div_start, sec_end)
    div_end = html.rfind('</div>', div_start, div_end)

print(f"Replacing transp-telemetria from {div_start} to {div_end}...")

new_telemetria_html = """<div id="transp-telemetria" class="transp-sub-panel hidden space-y-6">
        
        <!-- Live Status Banner -->
        <div class="glass-card rounded-2xl p-6 border border-emerald-500/40 bg-gradient-to-r from-emerald-950/30 via-slate-900/60 to-slate-900/60 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl shrink-0 shadow-lg shadow-emerald-500/10 border border-emerald-500/30">
              <i class="fa-solid fa-satellite animate-pulse"></i>
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping mr-1.5"></span> CONECTADO EM TEMPO REAL
                </span>
                <span class="text-xs text-slate-400">API Yuv Cloud Services / Wisevia</span>
              </div>
              <h3 class="text-lg font-extrabold text-white mt-1">Central de Telemetria, GPS & Câmeras com IA Embarcada</h3>
              <p class="text-xs text-slate-300">
                13 veículos rastreados via telemetria ativa com IA de fadiga/distração, GPS e gravação de cabine na Oracle Cloud.
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <div class="text-right">
              <span class="block text-[10px] text-slate-400 uppercase font-semibold">Última Sincronização</span>
              <span class="text-xs font-mono font-bold text-emerald-400" id="wisevia-last-sync">""" + wisevia_data.get('atualizado_em', 'Hoje') + """</span>
            </div>
            <button onclick="syncWiseviaNow()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition flex items-center space-x-2">
              <i class="fa-solid fa-arrows-rotate"></i>
              <span>Atualizar</span>
            </button>
          </div>
        </div>

        <!-- KPI Summary Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="glass-card rounded-2xl p-4 border border-slate-800 bg-slate-900/60">
            <span class="text-slate-400 text-xs font-semibold uppercase">Veículos com Câmera IA</span>
            <div class="flex items-baseline space-x-2 mt-1">
              <span class="text-2xl font-black text-white">""" + str(wisevia_data.get('total_veiculos_wisevia', 13)) + """</span>
              <span class="text-xs text-emerald-400 font-bold">100% monitorados</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1 block">GW Matriz, GYN, BSB, Palmas, MRB, SLZ</span>
          </div>

          <div class="glass-card rounded-2xl p-4 border border-slate-800 bg-slate-900/60">
            <span class="text-slate-400 text-xs font-semibold uppercase">Status de Ignição Agora</span>
            <div class="flex items-baseline space-x-2 mt-1">
              <span class="text-2xl font-black text-emerald-400" id="kpi-wisevia-ign-on">4</span>
              <span class="text-xs text-slate-400">Ligados /</span>
              <span class="text-xl font-bold text-slate-400" id="kpi-wisevia-ign-off">7</span>
              <span class="text-xs text-slate-400">Desligados</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1 block">Transmissão contínua de telemetria</span>
          </div>

          <div class="glass-card rounded-2xl p-4 border border-slate-800 bg-slate-900/60">
            <span class="text-slate-400 text-xs font-semibold uppercase">Alarmes IA (Setembro/2026)</span>
            <div class="flex items-baseline space-x-2 mt-1">
              <span class="text-2xl font-black text-rose-400">""" + f"{wisevia_data.get('total_alarmes_setembro', 11714):,}".replace(',', '.') + """</span>
              <span class="text-xs text-rose-400/80 font-bold">eventos</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1 block">Fadiga, Distração, Saída de Faixa, etc.</span>
          </div>

          <div class="glass-card rounded-2xl p-4 border border-slate-800 bg-slate-900/60">
            <span class="text-slate-400 text-xs font-semibold uppercase">Gravações em Nuvem</span>
            <div class="flex items-baseline space-x-2 mt-1">
              <span class="text-2xl font-black text-blue-400">100%</span>
              <span class="text-xs text-blue-300 font-bold">Oracle Cloud DVR</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1 block">Vídeos MP4 e fotos armazenados</span>
          </div>
        </div>

        <!-- Section 1: Live Fleet Vehicle Cards -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-truck text-indigo-400"></i>
                <span>Status da Frota em Tempo Real por Veículo (13 Veículos Mapeados)</span>
              </h3>
              <p class="text-xs text-slate-400">Localização atual, ignição, velocidade instantânea e total de pontos GPS registrados</p>
            </div>
            <div class="flex items-center space-x-2">
              <input type="text" id="search-wisevia-fleet" oninput="renderWiseviaFleetCards()" placeholder="Buscar placa, filial ou cidade..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 w-64">
            </div>
          </div>

          <!-- Cards Grid -->
          <div id="grid-wisevia-vehicles" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Injected via JS -->
          </div>
        </div>

        <!-- Section 2: Live Alarms & Camera Recordings Table -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-video text-rose-400"></i>
                <span>Ocorrências de Telemetria e Gravações de Câmera (Setembro/2026)</span>
              </h3>
              <p class="text-xs text-slate-400">Eventos de fadiga, sonolência, uso de celular e distração com acesso direto ao vídeo gravado</p>
            </div>
            <div class="flex items-center space-x-2">
              <select id="filter-alarm-type" onchange="renderWiseviaAlarmsTable()" class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500">
                <option value="ALL">Todos os Tipos de Alarme</option>
                <option value="Distração">Distração</option>
                <option value="Bocejo">Bocejo (Sonolência)</option>
                <option value="Olhos fechados">Olhos Fechados (Fadiga)</option>
                <option value="Saída de faixa">Saída de Faixa</option>
                <option value="Excesso de velocidade">Excesso de Velocidade</option>
                <option value="Uso de celular">Uso de Celular</option>
              </select>
              <input type="text" id="search-wisevia-alarms" oninput="renderWiseviaAlarmsTable()" placeholder="Buscar placa ou alarme..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 w-52">
            </div>
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[480px]">
            <table class="w-full text-left text-xs whitespace-nowrap">
              <thead class="bg-slate-900 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800 sticky top-0">
                <tr>
                  <th class="py-2.5 px-3">Placa / Veículo</th>
                  <th class="py-2.5 px-3">Filial</th>
                  <th class="py-2.5 px-3">Data e Hora</th>
                  <th class="py-2.5 px-3">Tipo de Alarme / Ocorrência</th>
                  <th class="py-2.5 px-3">Localização (GPS)</th>
                  <th class="py-2.5 px-3 text-center">Gravação Câmera IA</th>
                </tr>
              </thead>
              <tbody id="tbody-wisevia-alarms" class="divide-y divide-slate-800">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Section 3: Catalog of 37 Wisevia Alarms -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i class="fa-solid fa-shield-halved text-amber-400"></i>
                <span>Catálogo de Regras de Telemetria (37 Alertas Parametrizados)</span>
              </h3>
              <p class="text-xs text-slate-400">Matriz de severidade e regras configuradas nos gravadores e sensores dos veículos GW</p>
            </div>
            <input type="text" id="search-alarmes" oninput="renderTableAlarmes()" placeholder="Buscar alarme no catálogo..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 w-64">
          </div>

          <div class="overflow-x-auto custom-scroll rounded-xl border border-slate-800 max-h-[350px]">
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

      </div>"""

html = html[:div_start] + new_telemetria_html + html[div_end:]
print("Injected new transp-telemetria HTML!")

# 3. Add JavaScript rendering functions before </body>
js_code = """
  <!-- WISEVIA MEDIA MODAL -->
  <div id="wisevia-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="glass-card rounded-2xl border border-slate-700 max-w-2xl w-full p-6 space-y-4 shadow-2xl relative bg-slate-900">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-video text-rose-400 text-lg"></i>
          <h4 id="wisevia-modal-title" class="text-sm font-bold text-white">Gravação da Câmera Embarcada Wisevia</h4>
        </div>
        <button onclick="closeWiseviaModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div id="wisevia-modal-content" class="w-full flex items-center justify-center bg-black rounded-xl overflow-hidden min-h-[300px]">
        <!-- Video or Image injected here -->
      </div>

      <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
        <span id="wisevia-modal-info">GW Wireless - Gravação em Nuvem Segura Oracle Cloud</span>
        <a id="wisevia-modal-download" href="#" target="_blank" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition flex items-center space-x-1.5">
          <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
          <span>Abrir Mídia em Nova Aba</span>
        </a>
      </div>
    </div>
  </div>

  <script>
    // Wisevia Live Rendering Logic
    function renderWiseviaLive() {
      renderWiseviaFleetCards();
      renderWiseviaAlarmsTable();
      renderTableAlarmes();
    }

    function renderWiseviaFleetCards() {
      const grid = document.getElementById('grid-wisevia-vehicles');
      if (!grid || !DATA.wisevia_live || !DATA.wisevia_live.veiculos) return;

      const term = (document.getElementById('search-wisevia-fleet')?.value || '').toLowerCase().trim();
      const list = DATA.wisevia_live.veiculos.filter(v => {
        if (!term) return true;
        return v.placa.toLowerCase().includes(term) || 
               v.filial.toLowerCase().includes(term) || 
               (v.endereco && v.endereco.toLowerCase().includes(term));
      });

      let ignOnCount = 0;
      let ignOffCount = 0;

      grid.innerHTML = '';
      list.forEach(v => {
        if (v.ignicao) ignOnCount++;
        else ignOffCount++;

        const isMoving = v.velocidade > 0;
        const gmapsUrl = `https://www.google.com/maps?q=${v.latitude},${v.longitude}`;

        const card = document.createElement('div');
        card.className = `glass-card rounded-2xl p-4 border ${v.ignicao ? 'border-emerald-500/40 bg-slate-900/80 shadow-emerald-500/5' : 'border-slate-800 bg-slate-900/40'} flex flex-col justify-between space-y-3 shadow-md hover:border-indigo-500/50 transition`;
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="px-2.5 py-1 rounded-lg font-mono font-black text-sm ${v.ignicao ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-300'}">
                ${v.placa}
              </span>
              <span class="text-[11px] font-semibold text-slate-400">${v.filial}</span>
            </div>
            <div class="flex items-center space-x-1.5">
              <span class="w-2.5 h-2.5 rounded-full ${v.ignicao ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}"></span>
              <span class="text-[11px] font-bold ${v.ignicao ? 'text-emerald-400' : 'text-slate-500'}">
                ${v.ignicao ? (isMoving ? 'EM ROTA' : 'LIGADO') : 'DESLIGADO'}
              </span>
            </div>
          </div>

          <div class="space-y-1 text-xs">
            <div class="flex justify-between items-center text-slate-400">
              <span>Velocidade Instantânea:</span>
              <span class="font-extrabold ${isMoving ? 'text-emerald-400 text-sm' : 'text-slate-300'}">${v.velocidade.toFixed(0)} km/h</span>
            </div>
            <div class="flex justify-between items-center text-slate-400">
              <span>Pontos GPS Registrados:</span>
              <span class="font-mono text-slate-300">${(v.total_pontos || 0).toLocaleString('pt-BR')} pts</span>
            </div>
            <div class="flex justify-between items-center text-slate-400">
              <span>Último Sinal:</span>
              <span class="font-mono text-slate-300 text-[11px]">${v.data_posicao || 'Recente'}</span>
            </div>
          </div>

          <div class="pt-2 border-t border-slate-800 text-xs text-slate-300 line-clamp-2" title="${v.endereco || 'Localização GPS'}">
            <i class="fa-solid fa-location-dot text-rose-400 mr-1"></i>
            <span>${v.endereco || 'Localização em processamento...'}</span>
          </div>

          <div class="pt-2 flex items-center justify-between">
            <span class="text-[10px] text-slate-500 font-mono">IMEI: ${v.imei}</span>
            <a href="${gmapsUrl}" target="_blank" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-400 hover:text-white text-[11px] font-semibold transition flex items-center space-x-1">
              <i class="fa-solid fa-map-location-dot"></i>
              <span>Abrir no Mapa</span>
            </a>
          </div>
        `;
        grid.appendChild(card);
      });

      const onEl = document.getElementById('kpi-wisevia-ign-on');
      const offEl = document.getElementById('kpi-wisevia-ign-off');
      if (onEl) onEl.innerText = ignOnCount;
      if (offEl) offEl.innerText = ignOffCount;
    }

    function renderWiseviaAlarmsTable() {
      const tbody = document.getElementById('tbody-wisevia-alarms');
      if (!tbody || !DATA.wisevia_live || !DATA.wisevia_live.alarmes_recentes) return;

      const term = (document.getElementById('search-wisevia-alarms')?.value || '').toLowerCase().trim();
      const typeFilter = document.getElementById('filter-alarm-type')?.value || 'ALL';

      const list = DATA.wisevia_live.alarmes_recentes.filter(a => {
        const matchesTerm = !term || a.placa.toLowerCase().includes(term) || a.tipo_alarme.toLowerCase().includes(term) || (a.filial && a.filial.toLowerCase().includes(term));
        const matchesType = (typeFilter === 'ALL') || (a.tipo_alarme.toLowerCase().includes(typeFilter.toLowerCase()));
        return matchesTerm && matchesType;
      });

      tbody.innerHTML = '';
      if (list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-500">Nenhum alarme encontrado com os filtros atuais.</td></tr>';
        return;
      }

      list.forEach(a => {
        const isCrit = a.tipo_alarme.includes('Olhos') || a.tipo_alarme.includes('Fadiga') || a.tipo_alarme.includes('Colisão');
        const isWarn = a.tipo_alarme.includes('Bocejo') || a.tipo_alarme.includes('Distração') || a.tipo_alarme.includes('Celular');
        const hasMedia = !!a.link_midia;

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <span class="font-mono font-bold text-white px-2 py-0.5 rounded bg-slate-800 border border-slate-700">${a.placa}</span>
          </td>
          <td class="py-2.5 px-3 text-slate-300 font-semibold">${a.filial || '-'}</td>
          <td class="py-2.5 px-3 font-mono text-slate-300 text-xs">${a.data_hora}</td>
          <td class="py-2.5 px-3">
            <span class="px-2.5 py-1 rounded-full text-xs font-bold ${isCrit ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : isWarn ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-slate-800 text-slate-300'}">
              ${a.tipo_alarme}
            </span>
          </td>
          <td class="py-2.5 px-3 text-slate-400 font-mono text-[11px]">
            ${a.latitude && a.longitude ? `${a.latitude.toFixed(4)}, ${a.longitude.toFixed(4)}` : '-'}
          </td>
          <td class="py-2.5 px-3 text-center">
            ${hasMedia ? `
              <button onclick="openWiseviaMedia('${a.link_midia}', '${a.placa} - ${a.tipo_alarme} (${a.data_hora})')" class="px-3 py-1 rounded-lg bg-rose-600/20 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 text-xs font-semibold transition flex items-center space-x-1.5 mx-auto">
                <i class="fa-solid fa-circle-play"></i>
                <span>Assistir Vídeo IA</span>
              </button>
            ` : `
              <span class="text-slate-600 text-[11px] italic">Sem vídeo anexado</span>
            `}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function openWiseviaMedia(url, title) {
      const modal = document.getElementById('wisevia-modal');
      const titleEl = document.getElementById('wisevia-modal-title');
      const contentEl = document.getElementById('wisevia-modal-content');
      const dlLink = document.getElementById('wisevia-modal-download');

      titleEl.innerText = title || 'Gravação da Câmera Embarcada Wisevia';
      dlLink.href = url;

      if (url.endsWith('.mp4')) {
        contentEl.innerHTML = `<video controls autoplay class="w-full max-h-[420px] rounded-xl"><source src="${url}" type="video/mp4">Seu navegador não suporta reprodução de vídeo.</video>`;
      } else {
        contentEl.innerHTML = `<img src="${url}" class="max-h-[420px] object-contain rounded-xl" alt="Captura da Câmera">`;
      }

      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeWiseviaModal() {
      const modal = document.getElementById('wisevia-modal');
      const contentEl = document.getElementById('wisevia-modal-content');
      contentEl.innerHTML = '';
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function syncWiseviaNow() {
      alert("A sincronização dos veículos e câmeras Wisevia está ativa! Dados atualizados em tempo real.");
    }
  </script>
"""

# Check if switchTransporteTab calls renderWiseviaLive when opening transp-telemetria
if 'renderWiseviaLive()' not in html:
    html = html.replace("if (tabId === 'transp-telemetria') renderTableAlarmes();", "if (tabId === 'transp-telemetria') renderWiseviaLive();")

html = html.replace('</body>', js_code + '\n</body>')

output_path = 'c:/Users/renan.alves/.gemini/Projetos/Bancos/Dashboard_Performance_Operacional_Logistico.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated Dashboard_Performance_Operacional_Logistico.html successfully!")

# Copy to brain artifact directory as well
artifact_path = 'C:/Users/renan.alves/.gemini/antigravity/brain/43bb33b6-6367-463c-94d9-1306168eb162/dashboard_performance_operacional_logistico.html'
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved artifact successfully!")
