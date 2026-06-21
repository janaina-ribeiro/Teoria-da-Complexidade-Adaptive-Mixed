import glob
import io
import os
import sys

from app.bpp_am import BPPSolver
from app.save_results import ResultadosExperimento

def main():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
        )

    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(0)

    runs = 3
    filepaths: list = []

    if argv[0] == "--all":
        inst_dir = "instances"
        extra = list(argv[1:])
        if extra and not extra[0].isdigit():
            inst_dir = extra.pop(0)
        if extra:
            runs = int(extra[0])
        all_files = (
            sorted(glob.glob(os.path.join(inst_dir, "*.txt")))
            + sorted(glob.glob(os.path.join(inst_dir, "*.rtf")))
        )
        filepaths = [
            f for f in all_files
            if os.path.basename(f).lower() != "bpp_formato.txt"
        ]
    else:
        filepaths = [argv[0]]
        if len(argv) >= 2:
            runs = int(argv[1])

    if not filepaths:
        print("Nenhuma instância encontrada.")
        sys.exit(1)

    output_file = "resultado.txt"
    results = []
    with open(output_file, "w", encoding="utf-8") as fout:
        sys.stdout = ResultadosExperimento(sys.stdout, fout)

        for fp in filepaths:
            print(f"  [{fp}] processando ({runs} run(s))...", end=" ", flush=True)
            r = BPPSolver.executar_experimento(fp, runs)
            results.append(r)
            print(f"melhor={r['melhor']}  estratégia={r['best_strategy']}")

        BPPSolver.imprimir_tabela(results)
        for r in results:
            BPPSolver.imprimir_melhor_solucao(r)

        sys.stdout = sys.stdout._s1  # restaura stdout original

    print(f"\n  Resultados salvos em: {output_file}")


if __name__ == "__main__":
    main()
