"""Utility functions for SBI Hackathon notebooks."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def corner_plot(
    samples_list,
    labels=None,
    param_names=None,
    theta_true=None,
    limits=None,
    figsize=None,
    bins=30,
    alpha=0.6,
    scatter_alpha=0.3,
    scatter_size=3,
):
    """Create a corner plot for comparing posterior distributions.

    Args:
        samples_list: List of sample tensors, each of shape (n_samples, n_params).
                      Can also be a single tensor for one distribution.
        labels: List of labels for legend (one per distribution). Default: None.
        param_names: List of parameter names for axis labels. Default: None.
        theta_true: True parameter values to mark (tensor of shape (n_params,)). Default: None.
        limits: List of [low, high] for each parameter. Default: auto from samples.
        figsize: Figure size. Default: (2*n_params, 2*n_params).
        bins: Number of histogram bins. Default: 30.
        alpha: Histogram alpha. Default: 0.6.
        scatter_alpha: Scatter plot alpha. Default: 0.3.
        scatter_size: Scatter marker size. Default: 3.

    Returns:
        fig, axes: Matplotlib figure and axes array.
    """
    # Handle single sample array
    if not isinstance(samples_list, list):
        samples_list = [samples_list]

    # Convert to numpy
    samples_np = [s.numpy() if hasattr(s, 'numpy') else np.asarray(s) for s in samples_list]
    n_params = samples_np[0].shape[1]
    n_dists = len(samples_np)

    # Get colors from default cycle
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][:n_dists]

    # Set defaults
    if param_names is None:
        param_names = [f'$\\theta_{{{i}}}$' for i in range(n_params)]
    if figsize is None:
        figsize = (2 * n_params, 2 * n_params)

    # Compute limits from all samples if not provided
    if limits is None:
        all_samples = np.concatenate(samples_np, axis=0)
        limits = [[all_samples[:, i].min(), all_samples[:, i].max()] for i in range(n_params)]
        # Add 5% padding
        for i in range(n_params):
            margin = 0.05 * (limits[i][1] - limits[i][0])
            limits[i] = [limits[i][0] - margin, limits[i][1] + margin]

    # Create figure with upper triangle + diagonal layout
    fig, axes = plt.subplots(n_params, n_params, figsize=figsize)

    for i in range(n_params):
        for j in range(n_params):
            ax = axes[i, j]

            if i > j:
                # Lower triangle: hide
                ax.axis('off')
            elif i == j:
                # Diagonal: 1D histograms
                for k, (samples, color) in enumerate(zip(samples_np, colors)):
                    ax.hist(samples[:, i], bins=bins, density=True, alpha=alpha,
                           color=color, edgecolor='none')

                # True parameter as vertical line
                if theta_true is not None:
                    theta_val = theta_true[i].item() if hasattr(theta_true[i], 'item') else theta_true[i]
                    ax.axvline(theta_val, color='k', linestyle='--', linewidth=1.5, zorder=10)

                ax.set_xlim(limits[i])
                ax.set_yticks([])
                ax.set_xlabel(param_names[i])
            else:
                # Upper triangle: 2D scatter (j > i means we're above diagonal)
                for k, (samples, color) in enumerate(zip(samples_np, colors)):
                    ax.scatter(samples[:, j], samples[:, i], s=scatter_size,
                              alpha=scatter_alpha, color=color, edgecolor='none')

                # True parameter as cross
                if theta_true is not None:
                    theta_j = theta_true[j].item() if hasattr(theta_true[j], 'item') else theta_true[j]
                    theta_i = theta_true[i].item() if hasattr(theta_true[i], 'item') else theta_true[i]
                    ax.scatter([theta_j], [theta_i], marker='+', s=100, c='k',
                              linewidths=2, zorder=10)

                ax.set_xlim(limits[j])
                ax.set_ylim(limits[i])

                # Only show labels on edges
                if i == 0:
                    ax.set_title(param_names[j], fontsize=10)
                if j == n_params - 1:
                    ax.yaxis.set_label_position('right')
                    ax.set_ylabel(param_names[i], fontsize=10, rotation=270, labelpad=15)

                # Hide tick labels except on edges
                if i > 0:
                    ax.set_xticklabels([])
                if j < n_params - 1:
                    ax.set_yticklabels([])

    # Add legend in lower-left (empty space of lower triangle)
    if labels is not None:
        legend_handles = [Patch(facecolor=c, alpha=alpha, label=l)
                         for c, l in zip(colors, labels)]
        if theta_true is not None:
            legend_handles.append(Line2D([0], [0], color='k', linestyle='--',
                                        linewidth=1.5, label=r'$\theta_{\mathrm{true}}$'))
        # Place legend in lower-left corner (in the empty lower triangle area)
        fig.legend(handles=legend_handles, loc='lower left',
                  bbox_to_anchor=(0.02, 0.02), fontsize=10)

    plt.tight_layout()
    return fig, axes
