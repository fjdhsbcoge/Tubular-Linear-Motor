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
    
    Parameters:
    -----------
    time_points : array
        Time vector in seconds
    R_phases : list/array
        Phase resistances [Ohm] - default 4.0 Ohm for balanced operation
    
    Returns:
    --------
    theta_space : array
        Spatial angle 0..2*pi [rad]
    time_points : array
        Input time vector
    mmk_time_space : 2D array
        MMK distribution [time x space]
    v_neutral : array
        Neutral point voltage over time [V]
    currents : 2D array
        Phase currents [6 coils x time] [A]
    """
    omega = 2 * np.pi * 50  # 50 Hz electrical frequency
    V_amp = 2.0  # Amplitude for 0-4V range (2V +/-)
    V_offset = 2.0  # DC offset (center at 2V)
    
    # Three phase voltages (0-4V, unipolar, 120° phase shifted)
    v_U = V_amp * np.sin(omega * time_points) + V_offset       # Phase U
    v_V = V_amp * np.sin(omega * time_points - 2*np.pi/3) + V_offset  # Phase V (-120°)
    v_W = V_amp * np.sin(omega * time_points - 4*np.pi/3) + V_offset  # Phase W (-240°)
    
    # Floating neutral point voltage (weighted average based on conductance)
    # For equal resistances: v_n = (v_U + v_V + v_W) / 3 = 2.0V (constant!)
    G_total = 1/R_phases[0] + 1/R_phases[1] + 1/R_phases[2]
    v_n = (v_U/R_phases[0] + v_V/R_phases[1] + v_W/R_phases[2]) / G_total
    
    # Effective voltage across each phase winding (bipolar!)
    # This is the voltage that actually drives current through the motor
    u_U = v_U - v_n
    u_V = v_V - v_n
    u_W = v_W - v_n
    
    # Phase currents (bipolar - these create the MMK!)
    i_U = u_U / R_phases[0]
    i_V = u_V / R_phases[1]
    i_W = u_W / R_phases[2]
    
    # AbCaBc winding: 6 individual coils in series pairs
    # Coil order: A(0°), b(60°), C(120°), a(180°), B(240°), c(300°)
    # Phase U: A and a carry i_U
    # Phase V: b and B carry i_V 
    # Phase W: C and c carry i_W
    currents = np.array([i_U, i_V, i_W, i_U, i_V, i_W])  # Shape: (6, time)
    
    # Spatial grid for magnetic field calculation (0..360°)
    theta_space = np.linspace(0, 2*np.pi, 360)
    
    # Spatial positions of coils [rad]: 0°, 60°, 120°, 180°, 240°, 300°
    theta_spatial = np.array([0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3])
    
    # Winding directions: +1 for A,C,B; -1 for b,a,c (alternating in AbCaBc)
    winding_sign = np.array([1, -1, 1, -1, 1, -1])
    
    # Calculate MMK for each time step and spatial position
    mmk_time_space = np.zeros((len(time_points), len(theta_space)))
    
    for t_idx in range(len(time_points)):
        mmk = np.zeros_like(theta_space)
        for i in range(6):
            # MMK contribution: sign * current * cos(spatial_angle - coil_position)
            mmk += winding_sign[i] * currents[i, t_idx] * np.cos(theta_space - theta_spatial[i])
        mmk_time_space[t_idx, :] = mmk
    
    return theta_space, time_points, mmk_time_space, v_n, currents


def plot_overview(theta_space, time, mmk_data, v_neutral, currents, 
                  save_path='mmk_overview.png'):
    """Create overview plots showing voltages, currents, and traveling wave."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Output Voltages (Unipolar 0-4V)
    ax1 = axes[0, 0]
    ax1.plot(time*1000, 2*np.sin(2*np.pi*50*time) + 2, 
             label='Phase U', color='blue', linewidth=2)
    ax1.plot(time*1000, 2*np.sin(2*np.pi*50*time - 2*np.pi/3) + 2, 
             label='Phase V', color='orange', linewidth=2)
    ax1.plot(time*1000, 2*np.sin(2*np.pi*50*time - 4*np.pi/3) + 2, 
             label='Phase W', color='green', linewidth=2)
    ax1.axhline(y=2, color='gray', linestyle='--', alpha=0.5, label='Midpoint (2V)')
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_title('Driver Output Voltages (Unipolar 0-4V)', 
                  fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time [ms]')
    ax1.set_ylabel('Voltage [V]')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Neutral Point Voltage
    ax2 = axes[0, 1]
    ax2.plot(time*1000, v_neutral, color='red', linewidth=2, label='Neutral Point')
    ax2.axhline(y=2, color='gray', linestyle='--', alpha=0.7, label='Ideal: 2.0V')
    ax2.set_title(f'Floating Neutral Voltage ({v_neutral.min():.3f}V - {v_neutral.max():.3f}V)', 
                  fontsize=12, fontweight='bold')
    ax2.set_xlabel('Time [ms]')
    ax2.set_ylabel('Voltage [V]')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Phase Currents (Bipolar!)
    ax3 = axes[1, 0]
    ax3.plot(time*1000, currents[0], label='Phase U Current', 
             color='blue', linewidth=2)
    ax3.plot(time*1000, currents[1], label='Phase V Current', 
             color='orange', linewidth=2)
    ax3.plot(time*1000, currents[2], label='Phase W Current', 
             color='green', linewidth=2)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.set_title('Phase Currents (Bipolar due to Floating Neutral)', 
                  fontsize=12, fontweight='bold')
    ax3.set_xlabel('Time [ms]')
    ax3.set_ylabel('Current [A]')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Space-Time Diagram of MMK (Traveling Wave)
    ax4 = axes[1, 1]
    im = ax4.imshow(mmk_data, aspect='auto', cmap='RdBu_r', 
                    extent=[0, 360, time[-1]*1000, 0], 
                    vmin=-1.5, vmax=1.5, interpolation='bilinear')
    ax4.set_xlabel('Spatial Angle [°]')
    ax4.set_ylabel('Time [ms]')
    ax4.set_title('MMK Space-Time Diagram (Traveling Wave)', 
                  fontsize=12, fontweight='bold')
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('MMK [A·turns]', rotation=270, labelpad=20)
    
    # Add diagonal line showing wave propagation
    ax4.plot([0, 360], [0, time[-1]*1000/2], 'w--', alpha=0.5, linewidth=1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def plot_spatial_distribution(theta_space, time, currents, 
                               save_path='mmk_spatial.png'):
    """Plot spatial MMK distribution at different electrical angles."""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    
    # Electrical angles for snapshots
    snapshots = [0, 30, 60, 90, 120, 180]  # degrees
    labels = ['0°', '30°', '60°', '90°', '120°', '180°']
    
    theta_spatial = np.array([0, 60, 120, 180, 240, 300]) * np.pi/180
    winding_sign = np.array([1, -1, 1, -1, 1, -1])
    
    for idx, (phase_deg, label) in enumerate(zip(snapshots, labels)):
        # Find closest time index
        t_idx = int(phase_deg/180 * len(time)/4)
        
        ax = axes[idx]
        
        # Individual coil contributions (faint dashed)
        colors = ['blue', 'orange', 'green', 'blue', 'orange', 'green']
        mmk_total = np.zeros_like(theta_space)
        
        for i in range(6):
            contribution = (winding_sign[i] * currents[i, t_idx] * 
                          np.cos(theta_space - theta_spatial[i]))
            mmk_total += contribution
            ax.plot(np.degrees(theta_space), contribution, 
                   color=colors[i], alpha=0.4, linestyle='--', linewidth=1.5)
        
        # Resultant MMK (thick black line)
        ax.plot(np.degrees(theta_space), mmk_total, 'k-', 
               linewidth=2.5, label='Resultant MMK')
        
        # Mark coil positions
        for pos in np.degrees(theta_spatial):
            ax.axvline(x=pos, color='gray', linestyle=':', alpha=0.3, linewidth=0.8)
        
        ax.set_title(f'Electrical Angle ωt = {label}', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 360)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('Spatial Angle [°]')
        if idx % 3 == 0:
            ax.set_ylabel('MMK [A·turns]')
        if idx == 0:
            ax.legend(loc='upper right', fontsize=7)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Spatial MMK Distribution at Different Electrical Angles\n' + 
                '(Individual coil contributions sum to form the resultant MMK)', 
                fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def plot_spatial_with_sum_bars(theta_space, time, currents, 
                                save_path='mmk_spatial_with_bars.png'):
    """Plot spatial MMK with a bar chart showing the sum at a specific angle."""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Electrical angles for snapshots
    snapshots = [0, 30, 60, 90, 120, 180]  # degrees
    labels = ['0°', '30°', '60°', '90°', '120°', '180°']
    
    theta_spatial = np.array([0, 60, 120, 180, 240, 300]) * np.pi/180
    winding_sign = np.array([1, -1, 1, -1, 1, -1])
    
    for idx, (phase_deg, label) in enumerate(zip(snapshots, labels)):
        # Find closest time index
        t_idx = int(phase_deg/180 * len(time)/4)
        
        ax = axes[idx]
        
        # Individual coil contributions (faint dashed)
        colors = ['blue', 'orange', 'green', 'blue', 'orange', 'green']
        mmk_total = np.zeros_like(theta_space)
        
        for i in range(6):
            contribution = (winding_sign[i] * currents[i, t_idx] * 
                          np.cos(theta_space - theta_spatial[i]))
            mmk_total += contribution
            ax.plot(np.degrees(theta_space), contribution, 
                   color=colors[i], alpha=0.4, linestyle='--', linewidth=1.5)
        
        # Resultant MMK (thick black line)
        ax.plot(np.degrees(theta_space), mmk_total, 'k-', 
               linewidth=2.5, label='Resultant MMK')
        
        # Add a vertical line at theta=0 and show the values as a stacked bar
        theta_check = 0  # Check at spatial angle 0°
        values_at_check = []
        for i in range(6):
            val = winding_sign[i] * currents[i, t_idx] * np.cos(theta_check - theta_spatial[i])
            values_at_check.append(val)
        
        # Plot a marker at the sum point
        total_at_check = sum(values_at_check)
        ax.plot(0, total_at_check, 'r*', markersize=15, zorder=10)
        
        # Mark coil positions
        for pos in np.degrees(theta_spatial):
            ax.axvline(x=pos, color='gray', linestyle=':', alpha=0.3, linewidth=0.8)
        
        # Add text showing the sum
        ax.text(0.02, 0.98, f'Sum at θ=0°: {total_at_check:+.3f}', 
               transform=ax.transAxes, fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(f'Electrical Angle ωt = {label}', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 360)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('Spatial Angle [°]')
        if idx % 3 == 0:
            ax.set_ylabel('MMK [A·turns]')
        if idx == 0:
            ax.legend(loc='upper right', fontsize=7)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Spatial MMK Distribution (red star = value at θ=0°)', 
                fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def main():
    """Run the simulation and generate plots."""
    print("AbCaBc Motor Simulation")
    print("=" * 50)
    
    # Generate time vector (2 periods at 50Hz = 40ms)
    t = np.linspace(0, 0.04, 400)
    
    # Run simulation with EQUAL resistances (4.0 Ohm for all phases)
    theta_space, time, mmk_data, v_neutral, currents = calculate_mmk_unipolar(
        t, R_phases=[4.0, 4.0, 4.0]
    )
    
    print(f"\nSimulation Parameters:")
    print(f"  Phase Resistances: 4.0 Ω (balanced)")
    print(f"  Neutral Point: {v_neutral.min():.3f}V - {v_neutral.max():.3f}V " +
          f"(constant 2.0V for equal R)")
    print(f"  Current Amplitude: ±{np.max(np.abs(currents[0])):.2f}A")
    
    # Generate plots
    plot_overview(theta_space, time, mmk_data, v_neutral, currents, 
                  'mmk_overview.png')
    plot_spatial_distribution(theta_space, time, currents, 
                               'mmk_spatial.png')
    plot_spatial_with_sum_bars(theta_space, time, currents,
                                'mmk_spatial_with_bars.png')
    
    print("\nKey Insight:")
    print("  Unipolar 0-4V voltages create bipolar currents through the")
    print("  floating neutral mechanism, generating a rotating magnetic field!")


if __name__ == "__main__":
    main()
