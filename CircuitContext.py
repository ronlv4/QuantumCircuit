class CircuitContext(object):
    def __init__(self, t, shots, samples, theta_range):
        self.t = t
        self.shots = shots
        self.samples = samples
        self.theta_range = theta_range

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_circuit_specifier(self):
        raise NotImplementedError

    def get_analytic_label(self):
        raise NotImplementedError

    def get_analytic_expression(self):
        raise NotImplementedError

    def get_parametrized_circuits(self):
        raise NotImplementedError
