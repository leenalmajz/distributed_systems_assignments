import pickle
from mpi4py import MPI
from config import load_config
from queue_mngr import QueueManager
import time
import os

class MLService:
    def __init__(self, queue_manager: QueueManager, model_path: str):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.queue_manager = queue_manager
        self.model = None
        
        if self.rank == 0:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file {model_path} not found")
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)

    def process_transactions(self, transactions_queue = 'transactions', results_queue  = 'results'):
        if self.rank == 0:
            while True:
                transactions = []
                for _ in range(self.size - 1):
                    transaction = self.queue_manager.pull(transactions_queue)
                    if transaction is None: # If there are no more transactions
                        break
                    transactions.append(transaction)
                
                if len(transactions) == 0:
                    time.sleep(1)   # wait for 1 second if the queue is empty
                    continue
            
                # Distributing transactions between processes
                for i, transaction in enumerate(transactions):
                    self.comm.send(transaction, dest = i+1, tag = 1)    # tag is 1 for sending, 2 for receiving if rang = 0. If not, the numbers are flipped

                # Gathering results
                results = []
                for i in range(len(transactions)):
                    result = self.comm.recv(source = i+1, tag = 2)
                    results.append(result)

                for result in results:  # Pushing results to the queue
                    self.queue_manager.push(results_queue, {'body': result})

        else:
            while True:
                transaction = self.comm.recv(source = 0, tag = 1)

                # TODO: This is a placeholder
                result = {
                    'transaction_id': transaction['transaction_id'],
                    'timestamp': time.time(),
                    'is_fraudulent': False,
                    'confidence': 0.0
                }
                self.comm.send(result, dest = 0, tag = 2)



if __name__ == "__main__":
    conf = load_config()    # Loads data from the config file
    queue_data = conf['QueueManager']
    
    queue_manager = QueueManager(queue_data['path'], queue_data['max_length'], queue_data['save_period_time'])  # Creates a QueueManager instance

    if not queue_manager.create_queue('transactions'):
        print('"transactions" queue already exists!')
    if not queue_manager.create_queue('results'):
        print('"results" queue already exists!')

    service = MLService(queue_manager, conf['MLModel']['path'])