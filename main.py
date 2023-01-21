from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from qiskit import transpile

import utils
from A1Context import A1Context
from A2Context import A2Context
from A3Context import A3Context
from CircuitContext import CircuitContext
from utils import HardwareProvider, SimulatorProvider

if TYPE_CHECKING:
    from qiskit.providers.ibmq import IBMQBackend, IBMQJob

N = 50
T = 3 * np.pi
shots = 1024
samples = 64
theta_range = np.linspace(0, T, samples)
circuit_specifier = 'A2'
provider = SimulatorProvider.QasmSim

utils.authenticate()


def get_context(circuit_specifier) -> CircuitContext:
    if circuit_specifier == 'A1':
        return A1Context(N, T, shots, samples, theta_range)
    elif circuit_specifier == 'A2':
        return A2Context(N, T, shots, samples, theta_range)
    elif circuit_specifier == 'A3':
        return A3Context(N, T, shots, samples, theta_range)
    else:
        raise ValueError(f'Unknown circuit specifier: {circuit_specifier}')


def run_circuit(circuit, backend: IBMQBackend, name):
    job: IBMQJob = backend.run(transpile(circuit, backend), shots=shots)
    job.update_name(name)
    return job.job_id()


def get_job_results(backend: IBMQBackend, job_id):
    job = backend.retrieve_job(job_id)
    counts = job.result().get_counts()
    probabilities = np.array([counts_i.get('0', 0) for counts_i in counts]) / shots
    return probabilities


def main():
    with get_context(circuit_specifier) as context:  # type: CircuitContext
        circuit = context.get_parametrized_circuits()
        backend: IBMQBackend = utils.get_backend(provider)
        job_id = run_circuit(circuit, backend, f'{context.get_circuit_specifier()}_N{N}')

        # TODO: make plot_config per CircuitContext
        plot_config = {
            'title': f'Probability of measuring \'0\' vs. $\\theta, \epsilon = 1, N={N}$',
            'xlabel': r'$\theta [rad]$',
            'ylabel': 'Probability',
            'analytic_label': context.get_analytic_label(),
            'save': f'{circuit_specifier}_N{N}'
        }

        utils.plot_results(
            theta_range,
            get_job_results(backend, job_id),
            context.get_analytic_expression(),
            **plot_config)


if __name__ == '__main__':
    main()
