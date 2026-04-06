"""
Tubular Linear Motor - Correct MMK Simulation
==============================================

This simulation models the actual physics of a tubular linear motor:
- 6 coils distributed ALONG the motor length (not angularly)
- Stator has sinusoidal B-field along its length: B(x) = B_max * sin(2πx/λ)
- Each coil produces MMK that interacts with LOCAL stator field
- Force = MMK × B_field at each position, summed across all coils

AbCaBc Winding Layout (along motor length):
  Position:  0mm    5mm    10mm   15mm   20mm   25mm   30mm (pole pitch)
             [A]    [b]    [C]    [a]    [B]    [c]
             │      │      │      │      │      │
  Phase:     U      V      W      U      V      W
  Direction: +      -      +      -      +      -

Key Physics:
- MMK from each coil is concentrated at its position (not distributed)
- Force = Σ (MMK_coil × B_stator(x_coil)) across all 6 coils
- The traveling MMK wave "locks" into the stator field and pulls the mover
"""

import numpy as np
import matplotlib.pyplot as plt


def simulate_linear_motor(time_points, pole_pitch_mm=30.0, coil_width_mm=5.0):
    """
    Simulate the tubular linear motor with correct spatial physics.
    
    Parameters:
    -----------
    time_points : array
        Time vector in seconds
    pole_pitch_mm : float
        Distance between same poles (N-to-N) in mm
    coil_width_mm : float
        Width of each coil in mm (pole_pitch/6 for concentrated winding)
    
    Returns:
    --------
    positions_mm : array
        Spatial positions along motor length [mm]
    b_field : array
        Stator B-field distribution [T]
    mmk_distribution : 2D array
        MMK from coils at each time step [time x position]
    force : array
        Total force at each time step [N]
    coil_positions_mm : array
        Positions of the 6 coils [mm]
    coil_currents : 2D array
        Current in each coil at each time [6 x time]
    """
    
    omega = 2 * np.pi * 50  # 50 Hz electrical
    V_amp = 2.0  # For 0-4V PWM
    V_offset = 2.0
    R_phase = 4.0  # Ohms
    
    # Three phase voltages (0-4V unipolar)
    v_U = V_amp * np.sin(omega * time_points) + V_offset
    v_V = V_amp * np.sin(omega * time_points - 2*np.pi/3) + V_offset
    v_W = V_amp * np.sin(omega * time_points - 4*np.pi/3) + V_offset
    
    # Floating neutral (2V for balanced phases)
    v_n = (v_U + v_V + v_W) / 3
    
    # Bipolar currents
    i_U = (v_U - v_n) / R_phase
    i_V = (v_V - v_n) / R_phase
    i_W = (v_W - v_n) / R_phase
    
    # Coil layout along motor length (AbCaBc pattern)
    # Coils are spaced by pole_pitch/6 = 5mm
    coil_positions_mm = np.array([0, 5, 10, 15, 20, 25])  # mm along motor
    coil_phases = ['U', 'V', 'W', 'U', 'V', 'W']
    coil_directions = [1, -1, 1, -1, 1, -1]  # A(+), b(-), C(+), a(-), B(+), c(-)
    
    # Current in each coil at each time
    coil_currents = np.zeros((6, len(time_points)))
    for i, phase in enumerate(coil_phases):
        if phase == 'U':
            coil_currents[i] = i_U * coil_directions[i]
        elif phase == 'V':
            coil_currents[i] = i_V * coil_directions[i]
        else:  # 'W'
            coil_currents[i] = i_W * coil_directions[i]
    
    # Spatial grid along motor length (2 pole pitches for visualization)
    positions_mm = np.linspace(-5, 65, 500)  # -5 to 65 mm
    
    # Peak B-field: Using relative scaling - actual force from FEMM is 60N at 2A
    B_max = 0.5  # Tesla (relative scaling factor, not absolute)
    b_field = B_max * np.sin(2 * np.pi * positions_mm / pole_pitch_mm)
    
    # Calculate MMK distribution and force at each time step
    mmk_distribution = np.zeros((len(time_points), len(positions_mm)))
    force = np.zeros(len(time_points))
    
    for t_idx in range(len(time_points)):
        mmk = np.zeros_like(positions_mm)
        instantaneous_force = 0
        
        for coil_idx in range(6):
            coil_pos = coil_positions_mm[coil_idx]
            coil_current = coil_currents[coil_idx, t_idx]
            
            # MMK is concentrated at coil position (rectangular approximation)
            # Width = coil_width_mm, centered at coil_pos
            coil_mask = (positions_mm >= coil_pos - coil_width_mm/2) & \
                       (positions_mm < coil_pos + coil_width_mm/2)
            mmk[coil_mask] = coil_current
            
            # Force contribution: F = MMK × B at coil position
            # B at coil center:
            b_at_coil = B_max * np.sin(2 * np.pi * coil_pos / pole_pitch_mm)
            instantaneous_force += coil_current * b_at_coil
        
        mmk_distribution[t_idx, :] = mmk
        force[t_idx] = instantaneous_force
    
    return positions_mm, b_field, mmk_distribution, force, coil_positions_mm, coil_currents, pole_pitch_mm


def plot_linear_motor_overview(positions_mm, b_field, mmk_data, force, time, 
                                coil_positions, coil_currents, pole_pitch,
                                save_path='linear_motor_overview.png'):
    """Create overview plots for the linear motor simulation."""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Stator B-Field (static, along length)
    ax1 = axes[0, 0]
    ax1.fill_between(positions_mm, b_field, alpha=0.3, color='blue')
    ax1.plot(positions_mm, b_field, 'b-', linewidth=2, label='B-field')
    # Mark coil positions
    for pos in coil_positions:
        ax1.axvline(x=pos, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax1.set_xlabel('Position along motor [mm]')
    ax1.set_ylabel('B-field [T]')
    ax1.set_title('Stator B-Field Distribution (Static)', fontsize=12, fontweight='bold')
    ax1.set_xlim(-5, 35)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Phase Currents over time
    ax2 = axes[0, 1]
    omega = 2 * np.pi * 50
    R = 4.0
    v_U = 2*np.sin(omega*time) + 2
    v_V = 2*np.sin(omega*time - 2*np.pi/3) + 2
    v_W = 2*np.sin(omega*time - 4*np.pi/3) + 2
    v_n = (v_U + v_V + v_W) / 3
    i_U = (v_U - v_n) / R
    i_V = (v_V - v_n) / R
    i_W = (v_W - v_n) / R
    
    ax2.plot(time*1000, i_U, 'b-', linewidth=2, label='Phase U (A, a)')
    ax2.plot(time*1000, i_V, 'orange', linewidth=2, label='Phase V (b, B)')
    ax2.plot(time*1000, i_W, 'g-', linewidth=2, label='Phase W (C, c)')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax2.set_xlabel('Time [ms]')
    ax2.set_ylabel('Current [A]')
    ax2.set_title('Phase Currents (Bipolar)', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Space-Time Diagram of MMK
    ax3 = axes[1, 0]
    # Show only first period for clarity
    t_end_idx = len(time) // 2
    im = ax3.imshow(mmk_data[:t_end_idx, :], aspect='auto', cmap='RdBu_r',
                    extent=[positions_mm[0], positions_mm[-1], time[t_end_idx]*1000, 0],
                    vmin=-0.6, vmax=0.6, interpolation='nearest')
    ax3.set_xlabel('Position along motor [mm]')
    ax3.set_ylabel('Time [ms]')
    ax3.set_title('MMK Space-Time Diagram (Traveling Wave)', fontsize=12, fontweight='bold')
    ax3.set_xlim(-5, 35)
    cbar = plt.colorbar(im, ax=ax3)
    cbar.set_label('MMK [A]', rotation=270, labelpad=20)
    
    # Plot 4: Force over time
    ax4 = axes[1, 1]
    ax4.plot(time*1000, force, 'k-', linewidth=2)
    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Time [ms]')
    ax4.set_ylabel('Force [N]')
    ax4.set_title('Resultant Force on Mover', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    # Add average force line
    avg_force = np.mean(force)
    ax4.axhline(y=avg_force, color='red', linestyle='--', alpha=0.7, 
                label=f'Average: {avg_force:.3f} N')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def plot_snapshots_linear(positions_mm, b_field, mmk_data, coil_positions, 
                           coil_currents, time, pole_pitch,
                           save_path='linear_motor_snapshots.png'):
    """Plot snapshots showing B-field and MMK interaction at different times."""
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    
    # Electrical angles to show
    angles = [0, 30, 60, 90, 120, 180]
    labels = ['0°', '30°', '60°', '90°', '120°', '180°']
    
    B_max = np.max(np.abs(b_field))
    
    for idx, (angle_deg, label) in enumerate(zip(angles, labels)):
        ax = axes[idx]
        t_idx = int(angle_deg/180 * len(time)/4)
        
        # Plot B-field (static, background)
        ax.fill_between(positions_mm, b_field, alpha=0.2, color='blue')
        ax.plot(positions_mm, b_field, 'b--', linewidth=1.5, alpha=0.6, label='B-field (stator)')
        
        # Plot MMK at this time step
        ax.bar(coil_positions, coil_currents[:, t_idx], 
               width=4, color='red', alpha=0.7, edgecolor='darkred', linewidth=1.5,
               label='MMK (coils)')
        
        # Add value labels on bars
        for pos, curr in zip(coil_positions, coil_currents[:, t_idx]):
            ax.text(pos, curr + 0.05*np.sign(curr), f'{curr:+.2f}', 
                   ha='center', va='bottom' if curr > 0 else 'top',
                   fontsize=8, fontweight='bold')
        
        # Calculate and display force
        force_at_t = 0
        for i, pos in enumerate(coil_positions):
            b_at_coil = B_max * np.sin(2 * np.pi * pos / pole_pitch)
            force_at_t += coil_currents[i, t_idx] * b_at_coil
        
        ax.set_title(f'ωt = {label}, Force = {force_at_t:+.3f} N', 
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Position [mm]')
        if idx % 3 == 0:
            ax.set_ylabel('MMK [A] / B-field [T]')
        ax.set_xlim(-2, 32)
        ax.set_ylim(-0.7, 0.7)
        if idx == 0:
            ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Add coil labels
        coil_names = ['A', 'b', 'C', 'a', 'B', 'c']
        for pos, name in zip(coil_positions, coil_names):
            ax.text(pos, -0.6, name, ha='center', fontsize=9, fontweight='bold')
    
    plt.suptitle('Linear Motor: MMK (bars) interacting with Stator B-field (blue curve)\n' +
                'Force = Σ (MMK × B) at each coil position', 
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def main():
    print("Tubular Linear Motor Simulation")
    print("=" * 50)
    
    t = np.linspace(0, 0.04, 400)  # 2 periods at 50Hz
    
    positions_mm, b_field, mmk_data, force, coil_pos, coil_curr, pole_pitch = \
        simulate_linear_motor(t, pole_pitch_mm=30.0, coil_width_mm=5.0)
    
    print(f"\nMotor Parameters:")
    print(f"  Pole pitch: {pole_pitch} mm")
    print(f"  Coil positions: {coil_pos} mm")
    print(f"  Peak B-field: {np.max(b_field):.2f} T")
    print(f"  Current amplitude: ±{np.max(np.abs(coil_curr)):.2f} A")
    print(f"  NOTE: Force values are RELATIVE (simplified 1D model)")
    print(f"  Actual test setup: 60 N at 2 A (from FEMM with full 2D geometry)")
    print(f"  Average force: {np.mean(force):.3f} N (relative)")
    print(f"  Force ripple: {np.std(force):.3f} N (relative)")
    
    plot_linear_motor_overview(positions_mm, b_field, mmk_data, force, t,
                                coil_pos, coil_curr, pole_pitch,
                                'linear_motor_overview.png')
    plot_snapshots_linear(positions_mm, b_field, mmk_data, coil_pos, coil_curr,
                          t, pole_pitch, 'linear_motor_snapshots.png')
    
    print("\nKey Physics:")
    print("  - Coils distributed ALONG motor length (0, 5, 10, 15, 20, 25 mm)")
    print("  - Each coil sees LOCAL B-field from stator")
    print("  - Force = Σ (MMK × B) at each coil position")
    print("  - MMK wave travels as currents change, creating continuous force")


if __name__ == "__main__":
    main()
