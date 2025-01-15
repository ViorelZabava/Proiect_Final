import sim
import random

class Csp:
    def __init__(self, num_inputs=16, history_length=16):
        """
        Initializează perceptronul și buffer-ul pentru istoricul de "taken"/"not taken".
        """
        self.num_inputs = num_inputs
        self.history_length = history_length
        #self.weights = [random.uniform(-0.5, 0.5) for _ in range(history_length)]  # Greutăți pentru istoricul recent
        self.weights = [0.5 if i % 2 == 0 else -0.5 for i in range(num_inputs)]
        #self.bias = random.uniform(-0.5, 0.5)  # Bias-ul perceptronului
        self.bias=0.1
        self.history = [0] * history_length  # Buffer pentru istoricul recent
        self.branch_count = 0
        self.taken_count = 0
        self.not_taken_count = 0
        sim.util.EveryBranch(self.handle_branch)

    def handle_branch(self, ip, predicted, actual, indirect, core_id):
        """
        Actualizează istoricul și procesează o ramură.
        """
        self.branch_count += 1
        self.last_ip = ip
        self.actual_output = actual
        # Actualizează istoricul de "taken"/"not taken"
        self.history.pop(0)  # Elimină cea mai veche decizie
        if actual == True:
            self.history.append(1)  # Adaugă decizia curentă
        else:
            self.history.append(0)
        #print(f"Istoric:{self.history}")

        # Statistici
        if actual:
            self.taken_count += 1
        else:
            self.not_taken_count += 1

        # Realizează predicția pe baza istoricului
        predicted_output = self.predict()

        # Antrenează perceptronul dacă predicția este greșită
        self.train(predicted_output, actual)

    def predict(self):
        """
        Realizează o predicție folosind istoricul recent.
        """
        weighted_sum = sum(w * h for w, h in zip(self.weights, self.history)) + self.bias
        return 0 if weighted_sum >= 0 else 5

    def train(self, predicted_output, actual_output):
        """
        Ajustează greutățile perceptronului dacă predicția este greșită.
        """
        learning_rate = 0.0000002
        if predicted_output != actual_output:
            for i in range(self.history_length):
                self.weights[i] += learning_rate * (actual_output - predicted_output) * self.history[i]
            self.bias += learning_rate * (actual_output - predicted_output)
            self.bias = max(min(self.bias, 10), -10)  # Bias limitat între -10 și 10
            #print(f"Biasul este:{self.bias}")

    def reset(self):
        """
        Resetează greutățile și bias-ul perceptronului.
        """
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(self.history_length)]
        self.bias = random.uniform(-0.5, 0.5)

    def hook_sim_end(self):
        """
        Afișează statistici la finalul simulării.
        """
        print("\n[BRANCH_MARKOV] Final Statistics:")
        print(f"Total branches encountered: {self.branch_count}")
        print(f"Taken branches: {self.taken_count} ({self.taken_count / self.branch_count * 100:.2f}%)")
        print(f"Not taken branches: {self.not_taken_count} ({self.not_taken_count / self.branch_count * 100:.2f}%)")


# Înregistrarea clasei în simulator
sim.util.register(Csp())
