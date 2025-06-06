import joblib
from mpi4py import MPI
from config import load_config
from queue_mngr import QueueManager
import time
import datetime
import os

class MLService():
    def __init__(self, queue_manager: QueueManager, model_path: str, num_processors: int):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = num_processors
        self.queue_manager = queue_manager
        self.model = self.load_model(model_path)
        
    def load_model(self, model_path: str):
        if self.rank == 0:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file {model_path} not found.")
            return joblib.load(model_path)

    def process_transactions(self, transactions_queue = 'transactions', results_queue  = 'results'):
        if self.rank == 0:  # Master
            while True:
                transactions = []
                for _ in range(self.size):
                    transaction = self.queue_manager.pull(transactions_queue)
                    if transaction is None: # If there are no more transactions
                        break
                    transactions.append(transaction)
                
                if len(transactions) == 0:
                    time.sleep(1)   # wait for 1 second if the queue is empty
                    continue
            
                # Distributing transactions between processes
                for i, transaction in range(min(len(transactions), self.size)): # If there would be (somehow) more transactions than processes, limit the transactions sent
                    self.comm.send(transactions[i], dest = i+1, tag = 1)    # tag is 1 for sending, 2 for receiving if rang = 0. If not, the numbers are flipped

                # Gathering results
                results = []
                for i in range(len(transactions)):
                    result = self.comm.recv(source = i+1, tag = 2)
                    results.append(result)

                for result in results:  # Pushing results to the queue
                    self.queue_manager.push(results_queue, {'body': result})

        else:   # Worker
            while True:
                transaction = self.comm.recv(source = 0, tag = 1)
                time.sleep(0.5)

                result = self.predict_from_transaction(transaction)
                time.sleep(0.5)

                self.comm.send(result, dest = 0, tag = 2)

    def predict_from_transaction(self, transaction):
        # Save customer_id for reference
        customer_id = transaction['customer']['user_id']

        # Preprocess
        df_processed = transaction.copy()
        df_processed.update({'timestamp': datetime.datetime.now()})

        # Drop unused columns
        df_processed.pop('customer')
        df_processed.pop('transaction_id')

        # Generate predictions
        predictions = self.model.predict(df_processed)

        # Return predictions alongside customer_id
        result = {
            'customer_id': customer_id,
            'predicted_fraudulent': predictions
        }

        return result


if __name__ == "__main__":
    conf = load_config()    # Loads data from the config file
    queue_data = conf['QueueManager']
    
    queue_manager = QueueManager(queue_data['path'], queue_data['max_length'], queue_data['save_period_time'])  # Creates a QueueManager instance

    if not queue_manager.create_queue('transactions'):
        print('"transactions" queue already exists!')
    if not queue_manager.create_queue('results'):
        print('"results" queue already exists!')

    ml_data = conf['MLModel']
    service = MLService(queue_manager, ml_data['path'], ml_data['num_processors'])