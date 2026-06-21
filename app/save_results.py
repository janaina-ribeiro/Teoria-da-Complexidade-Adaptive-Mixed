
class ResultadosExperimento:

    """
    Resultados do Experimento
    ------------------------
    Classe auxiliar para salvar resultados em arquivo e imprimir no console. 
    """
  
    def __init__(self, stream1, stream2):
        self._s1 = stream1
        self._s2 = stream2

    def write(self, data):
        self._s1.write(data)
        self._s2.write(data)

    def flush(self):
        self._s1.flush()
        self._s2.flush()

    def __getattr__(self, name):
        return getattr(self._s1, name)

