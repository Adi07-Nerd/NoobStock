from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot


class WorkerSignals(QObject):
    finished = pyqtSignal(tuple)
    error = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, client, name, ticker):
        ######
        # client is object who called method
        # name contains company name to search from dictionary of tickers
        # ticker is hardcoded ticker value
        ###
        super().__init__()
        self.signals = WorkerSignals()
        self.client = client
        self.c_name = name
        self.ticker_name = ticker

    @pyqtSlot()
    def run(self):
        try:
            print("Im in run")
            result = self.client.main.data_provider.getData(
                self.c_name, self.ticker_name)
            print("Im done with task")
        except Exception as e:
            self.signals.error.emit(str(e))
            print("oops i got an error")
        else:
            print("OO im safe")
            self.signals.finished.emit(result)
