---
name: vpn_proxy_tor_detection
description: Detectar conexiones anónimas (VPN, proxy, Tor) por IP
type: API
priority: Recomendada
mode: Híbrido
---

# vpn_proxy_tor_detection

Detecta si el usuario se conecta a través de VPN, proxy o Tor, lo cual puede indicar un intento de enmascarar la ubicación real. Usa una combinación de base de datos local y APIs externas como fallback.

## When to use

Usar en el `antifraud_agent` para cada sesión de verificación. La detección de VPN/proxy es una señal de riesgo que incrementa el score de fraude pero no es bloqueante por sí sola.

## Instructions

1. **Detección local**: mantener lista de rangos IP de Tor (exit nodes) actualizados desde `https://check.torproject.org/torbulkexitlist`.
2. Verificar IP contra lista de Tor: `is_tor = ip in tor_exit_nodes`.
3. **Detección por API** (fallback): usar IPQualityScore o ip2proxy.
4. Instalar: `pip install requests` para llamadas al API.
5. Verificar: `response = requests.get(f'https://ipqualityscore.com/api/json/ip/{api_key}/{ip}')`.
6. Evaluar flags: `is_vpn`, `is_proxy`, `is_tor`, `fraud_score`.
7. Agregar flags al score de fraude con peso configurable.

## Notes

- Cachear resultados por IP en Redis con TTL de 1 hora para evitar llamadas repetidas.
- Muchos usuarios corporativos usan VPN legítimamente; no rechazar solo por VPN.
- Actualizar la lista de exit nodes de Tor diariamente.