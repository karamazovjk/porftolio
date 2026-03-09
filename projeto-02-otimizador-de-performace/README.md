# Otimizador do PC

**Área:** Ferramentas de sistema · Automação · Interface gráfica  
**Linguagem:** Python 3.x  
**Interface:** Tkinter (desktop nativo)  
**Status:** 🔄 Em desenvolvimento ativo

---

## Sobre o projeto

Ferramenta desktop de otimização de performance desenvolvida para ambientes de desenvolvimento pesados — especialmente máquinas que rodam VSCode, notebooks Jupyter e múltiplas extensões simultaneamente.

O projeto surgiu de uma necessidade real: o ambiente de desenvolvimento estava lento por acúmulo de arquivos temporários, RAM fragmentada e processos desnecessários em segundo plano. A solução foi automatizar toda a rotina de limpeza em uma interface simples, com agendamento e monitoramento em tempo real.

---

## Funcionalidades

### 📊 Monitor em tempo real
- Uso de CPU total e por núcleo (até 8 cores)
- Consumo de RAM com detalhe de memória disponível
- Espaço em disco e I/O de leitura/escrita em MB/s
- Gráficos sparkline com histórico de 60 segundos
- Atualização automática a cada segundo

### 🧹 Limpeza do sistema
| Tarefa | Descrição |
|--------|-----------|
| Arquivos temporários | Remove arquivos de `%TEMP%`, `%WINDIR%\Temp` e `%LOCALAPPDATA%\Temp` |
| Cache de navegadores | Limpa cache do Chrome, Brave, Edge e Firefox |
| Prefetch (Windows) | Remove arquivos `.pf` da pasta `C:\Windows\Prefetch` |
| Cache DNS | Executa `ipconfig /flushdns` |
| Minidumps | Remove arquivos de crash dump |
| Apps em segundo plano | Encerra OneDrive, Teams, Discord, Spotify, Steam e similares |
| Plano de energia | Aplica o plano "Alto Desempenho" via `powercfg` |
| Lixeira | Esvazia a lixeira do sistema |

Todas as tarefas podem ser selecionadas individualmente antes de executar.

### 📅 Agendamento automático
- Limpeza periódica configurável em minutos, horas ou dias
- Configuração persistida em arquivo JSON local
- Histórico de execuções com data e hora
- Reagendamento automático após cada execução

---

## Estrutura do projeto

```
projeto-02-otimizador-de-performace/
├── otimizador_pc_v2.py       ← código principal (interface + lógica)
├── otimizador_schedule.json  ← configuração e histórico do agendador
└── README.md                 ← este arquivo
```

> **Nota:** O arquivo `codewithoutclean` é uma versão anterior do script, sem a interface gráfica, mantido para referência histórica do desenvolvimento.

---

## Pré-requisitos

Python 3.8 ou superior com a biblioteca `psutil`:

```bash
pip install psutil
```

O `tkinter` já vem incluído na instalação padrão do Python no Windows.

---

## Como usar

```bash
python otimizador_pc_v2.py
```

> ⚠️ Algumas funções requerem privilégios de administrador (Prefetch, Minidumps, Plano de energia). Execute como admin para acesso completo.

---

## Detalhes técnicos

O projeto é estruturado em classes independentes para cada painel da interface:

- `MonitorPanel` — coleta métricas via `psutil` e atualiza os widgets a cada 1 segundo em loop não-bloqueante (`after`)
- `LimpezaPanel` — executa as tarefas de limpeza em uma `Thread` separada para não travar a interface
- `AgendadorPanel` — gerencia o agendamento com `after` do Tkinter e persiste o estado em JSON
- `Sparkline` — widget Canvas customizado que renderiza gráfico de linha com histórico deslizante
- `MetricBar` — widget de barra de progresso com mudança de cor automática por threshold (verde → amarelo → vermelho)

---

## Próximos passos

- [ ] Gerar executável `.exe` com PyInstaller (`--onefile --windowed`)
- [ ] Adicionar ícone personalizado ao executável
- [ ] Melhorar tratamento de erros (substituir `except: pass` por logs explícitos)
- [ ] Suporte a múltiplos discos/partições no monitor
- [ ] Notificação de sistema ao concluir limpeza agendada

---

## Aprendizados

Este projeto foi desenvolvido com foco em **programação orientada a objetos com Tkinter** e **automação de tarefas de sistema com Python**. Principais conceitos aplicados:

- Interfaces gráficas com widgets customizados (Canvas, ScrolledText, Spinbox)
- Concorrência leve com `threading.Thread` para não bloquear a UI
- Persistência de configuração com `json`
- Interação com o sistema operacional via `subprocess`, `os`, `shutil` e `psutil`
- Design orientado a componentes reutilizáveis
