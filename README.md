# Teoria-da-Complexidade-Adaptive-Mixed
Este repositório contém a implementação da meta-heurística **Adaptive Mixed** para o Problema de Empacotamento em Caixas (*Bin Packing Problem - BPP*), desenvolvida como parte da disciplina de Teoria da Complexidade.

## Estrutura do Projeto
- `main.py`: Ponto de entrada do programa. Orquestra a leitura das instâncias e a execução do algoritmo.
- `bpp_am.py`: Contém a lógica principal da meta-heurística Adaptive Mixed para otimização do BPP.
- `save_results.py`: Módulo responsável por formatar e gravar os resultados obtidos.
- `instances/`: Diretório que armazena os arquivos de instâncias do BPP (ex: `_BP-1_n50C1000.txt`).
- `resultado.txt`: Arquivo gerado automaticamente contendo o log e os resultados da execução.

## Pré-requisitos
- **Python 3.x** instalado.
- Nenhuma biblioteca externa complexa além das presentes na biblioteca padrão do Python (caso utilize `numpy` ou outra, certifique-se de instalá-la, ex: `pip install -r requirements.txt`).

## Como Executar
1. Clone ou baixe este repositório.
2. Abra o terminal na pasta raiz do projeto.
3. Para executar o código, basta rodar o comando:
   ```bash
  python -m app.main --all
   ```

Os resultados dos experimentos (como o número de *bins* utilizados, tempo de execução, etc.) serão salvos no arquivo `resultado.txt` e também serão impressos no console.

## Adicionando novas instâncias
Para testar o algoritmo com outros dados, adicione os novos arquivos `.txt` dentro da pasta `instances/` e certifique-se de que estão seguindo o mesmo formato de leitura estabelecido, descrito em `bpp_formato.txt`, caso aplicável.
