import joblib, time, datetime, os, pandas
from mpi4py import MPI
from queue_mngr import QueueManager
from config import load_config
from models import Message
import secrets

class MLService():
    def __init__(self, queue_manager: QueueManager, model_path: str):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()    # Gets the ranks of the processes: 0 = master, anything else is a worker process
        self.size = self.comm.Get_size()    # Number of processors is the number of worker processors. Set to 5 as default in the docker-compose.yml
        self.queue_manager = queue_manager
        self.model = self.load_model(model_path)    # Loads the pre-trained model

        if self.rank == 0:
            print(f"Master initialized with {self.size-1} workers")
        else:
            print(f"Worker {self.rank} ready")
        
    def load_model(self, model_path: str):  # Loads the pre-trained model from the pkl file
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
                for i in range(min(len(transactions), self.size - 1)): # If there would be (somehow) more transactions than worker processes, limit the transactions sent
                    self.comm.send(transactions[i], dest = i+1, tag = 1)    # tag is 1 for transactions, 2 is for results

                # Gathering results
                results = []
                received_results_count = 0
                while received_results_count < min(len(transactions), self.size - 1):
                        status = MPI.Status()
                        result = self.comm.recv(source = MPI.ANY_SOURCE, tag = 2, status = status)
                        results.append(result)
                        received_results_count += 1

                for result in results:  # Pushing results to the queue
                    self.queue_manager.push(results_queue, Message(body=result))

        else:   # Worker
            while True:
                try:
                    status = MPI.Status()
                    transaction = self.comm.recv(source = 0, tag = 1, status = status)   # Gets the transaction from the master process
                except Exception as e:
                    time.sleep(1) # Wait before trying again
                    continue
                time.sleep(0.5)

                result = self.predict_from_transaction(transaction) # Getting the result from the model (if it's fraudulent or not)
                time.sleep(0.5) # just some buffer time

                self.comm.send(result, dest = 0, tag = 2)   # sends the results to the master process


    def predict_from_transaction(self, transaction):    # This code is the modification of the code from the exercises folder
        # Save customer_id for reference
        transaction_id = transaction['transaction_id']

        transaction = {
            'timestamp': time.time(),
            'status': transaction['status'],
            'vendor_id': transaction['vendor_id'],
            'amount': transaction['amount']
        }

        df_processed = pandas.DataFrame(transaction, index=[0])

        # Generate predictions
        predictions = self.model.predict(df_processed)

        # Return predictions alongside customer_id
        result = {
            "result_id": f"res_{secrets.token_hex(8)}",
            "transaction_id": transaction_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "is_fraudulent": predictions.tolist()[0],
            "confidence": 0.5,
        }

        return result
    
def run():
    conf = load_config()    # Loads data from the config file
    queue_data = conf['QueueManager']
    ml_data = conf['MLModel']

    queue_manager = QueueManager.get_instance(queue_data['path'], queue_data['max_length'], queue_data['save_period_time']) # Creates a QueueManager instance
    ml_service = MLService(queue_manager, ml_data['path'])   # Creates the MLService class instance
    ml_service.process_transactions()

if __name__ == "__main__":
    run()