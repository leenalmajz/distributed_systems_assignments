import joblib, time, datetime, os, threading
from mpi4py import MPI
from queue_mngr import QueueManager

class MLService():
    def __init__(self, queue_manager: QueueManager, model_path: str, num_processors: int):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()    # Gets the ranks of the processes: 0 = master, anything else is a worker process
        self.size = num_processors          # Number of processors is the number of worker processors. Set to 5 as default in the config file
        self.queue_manager = queue_manager
        self.model = self.load_model(model_path)    # Loads the pre-trained model

        if self.rank == 0:
            print(f"Master initialized with {self.size-1} workers")
        else:
            print(f"Worker {self.rank} ready")

        self.thread_lock = threading.Lock()
        t = threading.Thread(target=self.process_transactions)   # setting up a thread to run the processes in the background
        t.start()
        
    def load_model(self, model_path: str):  # Loads the pre-trained model from the pkl file
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
                for i in range(min(len(transactions), self.size)): # If there would be (somehow) more transactions than processes, limit the transactions sent
                    self.comm.send(transactions[i], dest = i+1, tag = 1)    # tag is 1 for transactions, 2 is for results

                # Gathering results
                results = []
                for i in range(len(transactions)):
                    result = self.comm.recv(source = i+1, tag = 2)
                    results.append(result)

                for result in results:  # Pushing results to the queue
                    self.queue_manager.push(results_queue, {'body': result})

        else:   # Worker
            while True:
                transaction = self.comm.recv(source = 0, tag = 1)   # Gets the transaction from the master process
                time.sleep(0.5)

                result = self.predict_from_transaction(transaction) # Getting the result from the model (if it's fraudulent or not)
                time.sleep(0.5) # just some buffer time

                self.comm.send(result, dest = 0, tag = 2)   # sends the results to the master process

    def predict_from_transaction(self, transaction):    # This code is the modification of the code from the exercises folder
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