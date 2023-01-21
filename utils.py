from __future__ import annotations

from enum import Enum

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from qiskit.providers.ibmq import IBMQ


class BackendType(Enum):
    Hardware = 'Hardware'
    Simulator = 'Simulator'


class Provider(Enum):
    def __str__(self):
        return str(self.value)


class HardwareProvider(str, Provider):
    Nairobi = 'ibm_nairobi'
    Oslo = 'ibm_oslo'
    Manila = 'ibmq_manila'
    Quito = 'ibmq_quito'
    Belem = 'ibmq_belem'
    Lima = 'ibmq_lima'


class SimulatorProvider(str, Provider):
    Stabilizer = 'simulator_stabilizer'
    Mps = 'simulator_mps'
    ExtendedStabilizer = 'simulator_extended_stabilizer'
    QasmSim = 'ibmq_qasm_simulator'
    StateVector = 'simulator_statevector'


simulator_providers_list = [sim_provider for sim_provider in SimulatorProvider]

hardware_providers_list = [hardware_provider for hardware_provider in HardwareProvider]

all_providers_list = simulator_providers_list + hardware_providers_list


def authenticate():
    IBMQ.enable_account('<INSERT YOUR API KEY HERE>')


def get_backend(name=None, provider=None, type=BackendType.Simulator, filters=None):
    if provider is None:
        provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
    if name is not None:
        return provider.get_backend(name)
    typed_provider = simulator_providers_list[0] if type is BackendType.Simulator else hardware_providers_list[0]
    return provider.get_backend(typed_provider)


def get_shortest_queue_backend():
    # TODO
    raise NotImplemented


def plot_results(theta_range, probabilities, analytic, **kwargs):
    save_name, title, xlabel, ylabel, analytic_label = None, None, None, None, 'Analytic Solution'
    if kwargs.get('save', None) is not None:
        save_name = kwargs['save']
    if kwargs.get('title', None) is not None:
        title = kwargs['title']
    if kwargs.get('xlabel', None) is not None:
        xlabel = kwargs['xlabel']
    if kwargs.get('ylabel', None) is not None:
        ylabel = kwargs['ylabel']
    if kwargs.get('analytic_label', None) is not None:
        analytic_label = kwargs['analytic_label']

    fig = plt.figure(figsize=(8, 6))
    ax: Axes = fig.add_subplot()
    ax.plot(theta_range, probabilities, '*', label='IBM-composer')
    ax.plot(theta_range, analytic(theta_range), label=analytic_label)
    ax.set_xticks([i * np.pi / 2 for i in range(7)])
    ax.set_xticklabels(
        ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$', r'$\frac{5\pi}{2}$', r'$3\pi$'],
        fontsize=14)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=14)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=14)
    if title:
        ax.set_title(title, fontsize=16)
    ax.legend(fontsize=10, loc='upper right')
    if save_name is not None:
        plt.savefig(save_name)
    plt.show()
