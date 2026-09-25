# 📐 Regras de Negócio do Projeto - Mapeamento de Filiais e Sistemas

Documento oficial de parametrização para geração de relatórios, dashboards, conciliações e consultas entre **WMS**, **ERP S7 (SN)** e **Data Hub**.

---

## 🏢 Parametrização Oficial de Filiais

| Nome Oficial da Filial | Praça / Cidade | ID no WMS | Códigos da Loja no ERP S7 (SN) | Empresas Vinculadas no ERP |
| :--- | :--- | :---: | :---: | :--- |
| **GW Matriz** | Anápolis - GO | **12** | **1 e 8** | `1`: GW Wireless (Distribuição)<br>`8`: Fiber Telecom (Telecom) |
| **GW Filial Goiânia** | Goiânia - GO | **9** | **6 e 90** | `6`: GW Wireless Eireli (Distribuição)<br>`90`: Fiber Goiânia (Telecom) |
| **GW Filial Brasília** | Brasília - DF | **8** | **9 e 91** | `9`: GW DF (Distribuição)<br>`91`: Fiber Brasília (Telecom) |
| **GW Filial Palmas** | Palmas - TO | **11** | **10 e 11** | `10`: Palmas (Distribuição)<br>`11`: GW Wireless (Telecom) |
| **GW Filial Marabá** | Marabá - PA | **10** | **7 e 92** | `7`: GW Wireless Filial PA (Distribuição)<br>`92`: Fiber Marabá (Telecom) |
| **GW Filial São Luís** | São Luís - MA | **7** | **14** | `14`: Fiber Telecom São Luís (Distribuição / Telecom) |

---

## 📌 Diretrizes de Aplicação das Regras:

1. **Relatórios e Dashboards:**
   * Sempre exibir a identificação da filial com o nome padronizado e a indicação explícita dos códigos das lojas (ex.: `GW Matriz (Lojas 1 e 8)`).
2. **Consultas no ERP S7 (SN):**
   * Ao filtrar dados por filial no ERP, utilizar a cláusula `WHERE COD_EMPRESA IN (...)` com os códigos correspondentes acima.
3. **Consultas no WMS:**
   * Ao filtrar dados no sistema WMS (API ou banco MySQL), utilizar o respectivo `filialId` / `ID WMS`.
4. **Agrupamentos de Conciliação:**
   * A soma dos saldos das lojas vinculadas no ERP compõe o saldo contábil total da respectiva praça/filial.
