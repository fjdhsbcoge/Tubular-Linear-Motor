"""
AbCaBc Star-Connected BLDC Motor Simulation
============================================

This simulation demonstrates how unipolar 0-4V PWM voltages from a SimpleFOC driver
create bipolar currents and a rotating magnetic field in a star-connected motor.

Key Physics:
- The neutral point "floats" to a voltage determined by the weighted average of phase voltages
- Current becomes bipolar: I = (V_phase - V_neutral) / R
- Even with 0-4V unipolar output, the motor sees ±2V effective voltage
- The AbCaBc winding (6 coils, alternating directions) creates a traveling wave

Author: [Your Name]
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt


def calculate_mmk_unipolar(time_points, R_phases=[4.0, 4.0, 4.0]):
    """
    Calculate MMK (Magnetomotive Force) based on unipolar 0-4V output voltages
    with floating neutral point (star connection).
    """
    omega = 2 * np.pi * 50
    V_amp = 2.0
    V_offset = 2.0
    
    v_U = V_amp * np.sin(omega * time_points) + V_offset
    v_V = V_amp * np.sin(omega * time_points - 2*np.pi/3) + V_offset
    v_W = V_amp * np.sin(omega * time_points - 4*np.pi/3) + V_offset
    
    G_total = 1/R_phases[0] + 1/R_phases[1] + 1/R_phases[2]
    v_n = (v_U/R_phases[0] + v_V/R_phases[1] + v_W/R_phases[2]) / G_total
    
    u_U = v_U - v_n
    u_V = v_V - v_n
    u_W = v_W - v_n
    
    i_U = u_U / R_phases[0]
    i_V = u_V / R_phases[1]
    i_W = u_W / R_phases[2]
    
    currents = np.array([i_U, i_V, i_W, i_U, i_V, i_W])
    
    theta_space = np.linspace(0, 2*np.pi, 360)
    theta_spatial = np.array([0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3])
    winding_sign = np.array([1, -1, 1, -1, 1, -1])
    
    mmk_time_space = np.zeros((len(time_points), len(theta_space)))
    
    for t_idx in range(len(time_points)):
        mmk = np.zeros_like(theta_space)
        for i in range(6):
            mmk += winding_sign[i] * currents[i, t_idx] * np.cos(theta_space - theta_spatial[i])
        mmk_time_space[t_idx, :] = mmk
    
    return theta_space, time_points, mmk_time_space, v_n, currents


def plot_spatial_clear_layers(theta_space, time, currents, save_path='mmk_spatial_layers.png'):
    """
    Plot showing:
    1. Individual coil contributions (6 dashed lines, very faint)
    2. Phase pair contributions (3 medium lines)  
    3. Total resultant MMK (black line)
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    
    snapshots = [0, 30, 60, 90, 120, 180]
    labels = ['0°', '30°', '60°', '90°', '120°', '180°']
    
    theta_spatial = np.array([0, 60, 120, 180, 240, 300]) * np.pi/180
    winding_sign = np.array([1, -1, 1, -1, 1, -1])
    
    for idx, (phase_deg, label) in enumerate(zip(snapshots, labels)):
        t_idx = int(phase_deg/180 * len(time)/4)
        ax = axes[idx]
        
        # Calculate all contributions
        coil_contributions = []
        for i in range(6):
            contrib = winding_sign[i] * currents[i, t_idx] * np.cos(theta_space - theta_spatial[i])
            coil_contributions.append(contrib)
        
        # Layer 1: Individual coils (very faint, dotted)
        colors = ['blue', 'orange', 'green', 'blue', 'orange', 'green']
        for i in range(6):
            ax.plot(np.degrees(theta_space), coil_contributions[i], 
                   color=colors[i], alpha=0.2, linestyle=':', linewidth=1)
        
        # Layer 2: Phase pairs (medium weight)
        # Phase U: Coil 0 (A at 0°) + Coil 3 (a at 180°)
        phase_U = coil_contributions[0] + coil_contributions[3]
        # Phase V: Coil 1 (b at 60°) + Coil 4 (B at 240°)
        phase_V = coil_contributions[1] + coil_contributions[4]
        # Phase W: Coil 2 (C at 120°) + Coil 5 (c at 300°)
        phase_W = coil_contributions[2] + coil_contributions[5]
        
        ax.plot(np.degrees(theta_space), phase_U, 'b-', alpha=0.5, linewidth=2, label='Phase U (A+a)')
        ax.plot(np.degrees(theta_space), phase_V, 'orange', alpha=0.5, linewidth=2, label='Phase V (b+B)')
        ax.plot(np.degrees(theta_space), phase_W, 'g-', alpha=0.5, linewidth=2, label='Phase W (C+c)')
        
        # Layer 3: Total resultant (thick black)
        total = phase_U + phase_V + phase_W
        ax.plot(np.degrees(theta_space), total, 'k-', linewidth=3, label='Total MMK')
        
        # Mark coil positions
        for pos in np.degrees(theta_spatial):
            ax.axvline(x=pos, color='gray', linestyle=':', alpha=0.3, linewidth=0.8)
        
        # Add annotation explaining the sum
        ax.text(0.02, 0.98, 
               f'At θ=0°:\n'
               f'  U: {phase_U[0]:+.3f}\n'
               f'  V: {phase_V[0]:+.3f}\n'
               f'  W: {phase_W[0]:+.3f}\n'
               f'  ───────\n'
               f'  Σ: {total[0]:+.3f}', 
               transform=ax.transAxes, fontsize=9, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
        
        ax.set_title(f'Electrical Angle ωt = {label}', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 360)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('Spatial Angle [°]')
        if idx % 3 == 0:
            ax.set_ylabel('MMK [A·turns]')
        if idx == 0:
            ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('MMK = Phase_U + Phase_V + Phase_W\n'
                'Each phase = 2 coils (e.g., A at 0° + a at 180°)\n'
                'Faint dots = individual coils, colored lines = phase pairs, black = total', 
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def plot_overview(theta_space, time, mmk_data, v_neutral, currents, save_path='mmk_overview.png'):
    """Create overview plots."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Output Voltages
    ax1 = axes[0, 0]
    ax1.plot(time*1000, 2*np.sin(2*np.pi*50*time) + 2, label='Phase U', color='blue', linewidth=2)
    ax1.plot(time*1000, 2*np.sin(2*np.pi*50*time - 2*np.pi/3) + 2, label='Phase V', color='orange', linewidth=2)
    ax1.plot(time*1000, 2*np.sin(2*np.pi*50*time - 4*np.pi/3) + 2, label='Phase W', color='green', linewidth=2)
    ax1.axhline(y=2, color='gray', linestyle='--', alpha=0.5, label='Midpoint (2V)')
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_title('Driver Output Voltages (Unipolar 0-4V)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time [ms]')
    ax1.set_ylabel('Voltage [V]')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Neutral Point
    ax2 = axes[0, 1]
    ax2.plot(time*1000, v_neutral, color='red', linewidth=2, label='Neutral Point')
    ax2.axhline(y=2, color='gray', linestyle='--', alpha=0.7, label='Ideal: 2.0V')
    ax2.set_title(f'Floating Neutral Voltage ({v_neutral.min():.3f}V - {v_neutral.max():.3f}V)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Time [ms]')
    ax2.set_ylabel('Voltage [V]')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Phase Currents
    ax3 = axes[1, 0]
    ax3.plot(time*1000, currents[0], label='Phase U', color='blue', linewidth=2)
    ax3.plot(time*1000, currents[1], label='Phase V', color='orange', linewidth=2)
    ax3.plot(time*1000, currents[2], label='Phase W', color='green', linewidth=2)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.set_title('Phase Currents (Bipolar)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Time [ms]')
    ax3.set_ylabel('Current [A]')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Space-Time Diagram
    ax4 = axes[1, 1]
    im = ax4.imshow(mmk_data, aspect='auto', cmap='RdBu_r', extent=[0, 360, time[-1]*1000, 0], vmin=-1.5, vmax=1.5)
    ax4.set_xlabel('Spatial Angle [°]')
    ax4.set_ylabel('Time [ms]')
    ax4.set_title('MMK Space-Time Diagram (Traveling Wave)', fontsize=12, fontweight='bold')
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('MMK [A·turns]', rotation=270, labelpad=20)
    ax4.plot([0, 360], [0, time[-1]*1000/2], 'w--', alpha=0.5, linewidth=1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def main():
    print("AbCaBc Motor Simulation")
    print("=" * 50)
    
    t = np.linspace(0, 0.04, 400)
    theta_space, time, mmk_data, v_neutral, currents = calculate_mmk_unipolar(t, R_phases=[4.0, 4.0, 4.0])
    
    print(f"\nSimulation Parameters:")
    print(f"  Phase Resistances: 4.0 Ω (balanced)")
    print(f"  Neutral Point: {v_neutral.min():.3f}V - {v_neutral.max():.3f}V")
    print(f"  Current Amplitude: ±{np.max(np.abs(currents[0])):.2f}A")
    
    plot_overview(theta_space, time, mmk_data, v_neutral, currents, 'mmk_overview.png')
    plot_spatial_clear_layers(theta_space, time, currents, 'mmk_spatial_layers.png')
    
    print("\nKey Insight: Unipolar 0-4V creates bipolar currents via floating neutral!")


if __name__ == "__main__":
    main()
