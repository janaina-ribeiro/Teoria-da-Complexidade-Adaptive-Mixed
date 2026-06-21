import math
import time
from itertools import combinations


class BPPSolver:

    """

    Algoritmo Adaptive Mixed (AM) para o problema de Bin Packing (BPP)
    --------------------------------------------------------------------
    Implementa as heurísticas Next Fit, First Fit, Last Fit, Best Fit e Worst Fit,
    aplicadas em diferentes ordenações dos itens, além de combinações sequenciais.
    A ideia é executar múltiplas estratégias e escolher a melhor solução encontrada.

    """


    _HDR = (
        f"{'Nº':>3}  {'Instância':<10} {'n':>5} {'C':>6}  "
        f"{'Val.Ini':>7} {'Pior':>6} {'Média':>6} {'Melhor':>7}  "
        f"{'%perda':>7} {'tempo(s)':>9}"
    )
    _SEP = "─" * len(_HDR)

    @staticmethod
    def _extrair_tokens_rtf(filepath: str) -> list:

        """

        _extrair_tokens_rtf
        -------------------------------------------
        Função apenas para lidar com o formato da instancia com formato .rtf.
        Arquivos: _BP-6 e _BP-7 (instâncias 6 e 7 do BPPLIB).

        """
        import re
        with open(filepath, encoding="cp1252", errors="replace") as fh:
            raw = fh.read()
        text = raw.replace("\\\n", "\n")
        text = re.sub(r"\\'[0-9a-fA-F]{2}", " ", text)
        text = re.sub(r"\\[a-zA-Z]+[-]?\d*", " ", text)
        text = re.sub(r"[{}\\;*]", " ", text)
        tokens = [t for t in text.split() if re.fullmatch(r"-?\d+", t)]
        return tokens

    @staticmethod
    def carregar_instancia(filepath: str):
        
        """
        
        carregar_instancia
        --------------------------------------------
        Carregas os dados de instacias fornecidas para os experimentos, 
        seja no formato .txt ou .rtf (caso das instâncias 6 e 7 do BPPLIB).
        Retorna n (nº de itens), C (capacidade dos bins) e lista
        de itens (pesos).
        
        """

        if filepath.lower().endswith(".rtf"):
            tokens = BPPSolver._extrair_tokens_rtf(filepath)
        else:
            with open(filepath, encoding="utf-8", errors="replace") as fh:
                tokens = fh.read().split()
        tokens = [t for t in tokens if t.lstrip("-").isdigit()]
        n = int(tokens[0])
        C = int(tokens[1])
        items = [int(tokens[i + 2]) for i in range(n)]
        if len(items) != n:
            raise ValueError(
                f"{filepath}: esperados {n} itens, lidos {len(items)}"
            )
        return n, C, items


    @staticmethod
    def _copiar(bi, br):

        """

        _copiar
        ---------------------------------------------------------------
        Função auxiliar para criar cópias do estado atual dos bins e seus espaços
        restantes, permitindo que as heurísticas sejam aplicadas de forma sequencial
        sem interferir umas nas outras.

        """

        return [list(b) for b in bi], list(br)

    @staticmethod
    def _adicionar(bi, br, idx, item):

        """

        _adicionar
        -----------------------------------------
        Adiciona um item ao bin de índice idx e atualiza o espaço restante.
        Entrada: bi (lista de bins), br (espaços restantes), idx (índice do bin), item (peso do item).
        Retorno: nenhum (modifica bi e br in-place).

        """

        bi[idx].append(item)
        br[idx] -= item

    @staticmethod
    def _abrir_bin(bi, br, C, item):

        """

        _abrir_bin
        --------------------------------------
        Abre um novo bin contendo o item fornecido e registra seu espaço restante.
        Entrada: bi (lista de bins), br (espaços restantes), C (capacidade do bin), item (peso do item).
        Retorno: nenhum (modifica bi e br in-place).

        """

        bi.append([item])
        br.append(C - item)

    @classmethod
    def next_fit(cls, items, C, init=None):

        """

        next_fit
        ------------------------------
        Heurística Next Fit: insere cada item no bin atual; abre um novo bin caso não caiba.
        Entrada: items (lista de pesos), C (capacidade), init (estado inicial opcional dos bins).
        Retorno: tupla (bi, br) com a lista de bins e os espaços restantes.

        """

        bi, br = cls._copiar(*init) if init else ([], [])
        for item in items:
            if br and br[-1] >= item:
                cls._adicionar(bi, br, -1, item)
            else:
                cls._abrir_bin(bi, br, C, item)
        return bi, br

    @classmethod
    def first_fit(cls, items, C, init=None):

        """

        first_fit
        ------------------------------
        Heurística First Fit: insere cada item no primeiro bin com espaço suficiente.
        Entrada: items (lista de pesos), C (capacidade), init (estado inicial opcional dos bins).
        Retorno: tupla (bi, br) com a lista de bins e os espaços restantes.

        """

        bi, br = cls._copiar(*init) if init else ([], [])
        for item in items:
            for i, rem in enumerate(br):
                if rem >= item:
                    cls._adicionar(bi, br, i, item)
                    break
            else:
                cls._abrir_bin(bi, br, C, item)
        return bi, br

    @classmethod
    def last_fit(cls, items, C, init=None):

        """

        last_fit
        ------------------------------
        Heurística Last Fit: insere cada item no último bin com espaço suficiente.
        Entrada: items (lista de pesos), C (capacidade), init (estado inicial opcional dos bins).
        Retorno: tupla (bi, br) com a lista de bins e os espaços restantes.

        """

        bi, br = cls._copiar(*init) if init else ([], [])
        for item in items:
            placed = False
            for i in range(len(br) - 1, -1, -1):
                if br[i] >= item:
                    cls._adicionar(bi, br, i, item)
                    placed = True
                    break
            if not placed:
                cls._abrir_bin(bi, br, C, item)
        return bi, br

    @classmethod
    def best_fit(cls, items, C, init=None):

        """

        best_fit
        ------------------------------
        Heurística Best Fit: insere cada item no bin com menor espaço restante suficiente.
        Entrada: items (lista de pesos), C (capacidade), init (estado inicial opcional dos bins).
        Retorno: tupla (bi, br) com a lista de bins e os espaços restantes.

        """

        bi, br = cls._copiar(*init) if init else ([], [])
        for item in items:
            best_i, best_rem = -1, C + 1
            for i, rem in enumerate(br):
                if item <= rem < best_rem:
                    best_i, best_rem = i, rem
            if best_i >= 0:
                cls._adicionar(bi, br, best_i, item)
            else:
                cls._abrir_bin(bi, br, C, item)
        return bi, br

    @classmethod
    def worst_fit(cls, items, C, init=None):

        """

        worst_fit
        ------------------------------
        Heurística Worst Fit: insere cada item no bin com maior espaço restante disponível.
        Entrada: items (lista de pesos), C (capacidade), init (estado inicial opcional dos bins).
        Retorno: tupla (bi, br) com a lista de bins e os espaços restantes.

        """

        bi, br = cls._copiar(*init) if init else ([], [])
        for item in items:
            worst_i, worst_rem = -1, -1
            for i, rem in enumerate(br):
                if rem >= item and rem > worst_rem:
                    worst_i, worst_rem = i, rem
            if worst_i >= 0:
                cls._adicionar(bi, br, worst_i, item)
            else:
                cls._abrir_bin(bi, br, C, item)
        return bi, br

    @staticmethod
    def _ordenar(items, mode):

        """

        _ordenar
        -----------------------------------------
        Retorna a lista de itens ordenada conforme o modo especificado.
        Entrada: items (lista de pesos), mode ('D' para decrescente, 'I' para crescente, outro para original).
        Retorno: nova lista de itens na ordem solicitada.

        """

        if mode == "D":
            return sorted(items, reverse=True)
        if mode == "I":
            return sorted(items)
        return list(items)

    @classmethod
    def executar_todas_estrategias(cls, items, C):

        """

        executar_todas_estrategias
        ------------------------------------------------------------------------
        Executa todas as combinações de heurísticas e ordenações, incluindo pares sequenciais.
        Entrada: items (lista de pesos), C (capacidade dos bins).
        Retorno: lista de tuplas (nome_estratégia, bins) com os resultados de cada estratégia.

        """

        heuristics = [
            ("NF", cls.next_fit),
            ("FF", cls.first_fit),
            ("LF", cls.last_fit),
            ("BF", cls.best_fit),
            ("WF", cls.worst_fit),
        ]
        results = []

        for name, fn in heuristics:
            for suffix, mode in [("", "orig"), ("D", "D"), ("I", "I")]:
                bi, _ = fn(cls._ordenar(items, mode), C)
                results.append((name + suffix, bi))

        half        = len(items) // 2
        first_half  = list(items[:half])
        second_half = list(items[half:])

        for ia, ib in combinations(range(len(heuristics)), 2):
            for (nameA, fnA), (nameB, fnB) in [
                (heuristics[ia], heuristics[ib]),    
                (heuristics[ib], heuristics[ia]),   
            ]:
                state_a = fnA(first_half, C)                    
                bi, _   = fnB(second_half, C, init=state_a)   
                results.append((f"{nameA}x{nameB}", bi))

        return results   

    @staticmethod
    def limite_inferior(items, C):

        """

        limite_inferior
        -------------------------------------
        Calcula o limite inferior teórico para o número mínimo de bins necessários.
        Entrada: items (lista de pesos), C (capacidade dos bins).
        Retorno: inteiro com o valor do limite inferior (ceil da soma dos pesos dividida pela capacidade).

        """

        return math.ceil(sum(items) / C)

    @classmethod
    def executar_experimento(cls, filepath: str, runs: int = 3) -> dict:

        """

        executar_experimento
        --------------------------------------------------
        Carrega uma instância, executa todas as estratégias por múltiplas rodadas e coleta estatísticas.
        Entrada: filepath (caminho do arquivo de instância), runs (número de rodadas, padrão 3).
        Retorno: dicionário com nome da instância, n, C, valor inicial, pior/média/melhor resultado,
                 percentual de perda, tempo médio, melhor estratégia e melhor solução encontrada.

        """

        import re as _re
        n, C, items = cls.carregar_instancia(filepath)
        stem = (
            filepath.replace("\\", "/").rsplit("/", 1)[-1]
            .rsplit(".", 1)[0]
        )
        m = _re.search(r"(?i)(bp[-_]?\d+)", stem)
        name = m.group(1).upper().replace("_", "-") if m else stem.upper()

        bi_nf, _ = cls.next_fit(list(items), C)
        valor_inicial = len(bi_nf)

        lb          = cls.limite_inferior(items, C)
        run_bests   = []           
        best_global = (None, None)  
        total_time  = 0.0

        for _ in range(runs):
            t0         = time.perf_counter()
            strategies = cls.executar_todas_estrategias(items, C)
            total_time += time.perf_counter() - t0

            min_len = min(len(x[1]) for x in strategies)
            empatadas = [x[0] for x in strategies if len(x[1]) == min_len]
            best_bins = next(x[1] for x in strategies if len(x[1]) == min_len)
            best = (", ".join(empatadas), best_bins)

            run_bests.append(min_len)
            if best_global[0] is None or len(best[1]) < len(best_global[1]):
                best_global = best

        melhor = min(run_bests)
        pior   = max(run_bests)
        media  = sum(run_bests) / len(run_bests)
        perda  = (melhor - lb) / lb * 100 if lb > 0 else 0.0

        return {
            "instance":      name,
            "n":             n,
            "C":             C,
            "valor_inicial": valor_inicial,
            "pior":          pior,
            "media":         media,
            "melhor":        melhor,
            "perda":         perda,
            "tempo":         total_time / runs,
            "best_strategy": best_global[0],
            "best_bins":     best_global[1],
            "lb":            lb,
            "todas_estrategias": strategies 
        }


    @classmethod
    def imprimir_tabela(cls, results: list):

        """

        imprimir_tabela
        ----------------------------------------
        Exibe os resultados de todos os experimentos em formato de tabela no terminal.
        Entrada: results (lista de dicionários retornados por run_experiment).
        Retorno: nenhum (imprime diretamente no terminal).

        """

        print("\n  Resultados — BPP / Adaptive Mixed (AM) — Equipe 6")
        print(cls._SEP)
        print(cls._HDR)
        print(cls._SEP)
        for i, r in enumerate(results):
            print(
                f"{i:>3}  {r['instance']:<10} {r['n']:>5} {r['C']:>6}  "
                f"{r['valor_inicial']:>7} {r['pior']:>6} {r['media']:>6.1f} {r['melhor']:>7}  "
                f"{r['perda']:>7.2f} {r['tempo']:>9.4f}"
            )
        print(cls._SEP)

    @staticmethod
    def imprimir_melhor_solucao(r: dict):

        """

        imprimir_melhor_solucao
        -----------------------------------------------
        Exibe a melhor solução encontrada e detalha O VALOR USADO, LIVRE E A HEURÍSTICA para todas as linhas (pedida do usuário).
        Entrada: r (dicionário retornado por run_experiment).
        Retorno: nenhum (imprime diretamente no terminal).

        """
        
        print(f"\n  [--- DETALHAMENTO DAS HEURISTICAS (PURAS E MISTAS) - {r['instance']} ---]")
        for nome_estrategia, bins in r["todas_estrategias"]:
            if len(bins) == r['melhor']:
                for k, bin_items in enumerate(bins, 1):
                    used = sum(bin_items)
                    livre = r['C'] - used
                    print(f"    [Estratégia: {nome_estrategia:>5}] Bin {k:>4}: {bin_items}  [usado={used}  livre={livre}]")
                print() 

        print(
            f"\n  Melhor solução — {r['instance']}: {r['melhor']} bins"
            f"  (LB={r['lb']}, estratégia(s) empatada(s): {r['best_strategy']})"
        )

