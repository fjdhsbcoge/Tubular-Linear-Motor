"""
Tubular Linear Motor - Correct MMK Simulation (Test Setup)
===========================================================

This simulation models the TEST SETUP configuration:
- 18 coils (3 × AbCaBc blocks) distributed ALONG motor length
- Stator has sinusoidal B-field: B(x) = B_max * sin(2πx/λ)
- Each coil produces MMK that interacts with LOCAL stator field
- Force = MMK × B_field at each position, summed across all 18 coils

AbCaBc Winding Layout (Test Setup - 3 blocks = 90mm total):
  Block 1 (0-30mm):   Block 2 (30-60mm):   Block 3 (60-90mm):
  [A]  [b]  [C]      [A]  [b]  [C]        [A]  [b]  [C]
  [a]  [B]  [c]      [a]  [B]  [c]        [a]  [B]  [c]

Key Physics:
- MMK from each coil is concentrated at its position
- Force = Σ (MMK_coil × B_stator(x_coil)) across all 18 coils
- The traveling MMK wave "locks" into the stator field and pulls the mover
- Force values are RELATIVE (simplified 1D model)
- Actual force from FEMM: 60 N at 2 A (with full 2D geometry)
"""

import numpy as np
import matplotlib.pyplot as plt


def simulate_linear_motor(time_points, pole_pitch_mm=30.0, coil_width_mm=5.0, n_blocks=3):
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
    n_blocks : int
        Number of AbCaBc blocks (test setup: 3 blocks = 18 coils, 90mm)
    
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
        Positions of all coils [mm]
    coil_currents : 2D array
        Current in each coil at each time [n_coils x time]
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
    
    # Coil layout along motor length (AbCaBc pattern, repeated n_blocks times)
    # Each block has 6 coils spaced by pole_pitch/6 = 5mm
    block_positions = np.array([0, 5, 10, 15, 20, 25])  # mm within one pole pitch
    block_phases = ['U', 'V', 'W', 'U', 'V', 'W']
    block_directions = [1, -1, 1, -1, 1, -1]  # A(+), b(-), C(+), a(-), B(+), c(-)
    
    # Generate all coil positions for n_blocks
    coil_positions_mm = []
    coil_phases = []
    coil_directions = []
    
    for block in range(n_blocks):
        offset = block * pole_pitch_mm
        for pos, phase, direction in zip(block_positions, block_phases, block_directions):
            coil_positions_mm.append(offset + pos)
            coil_phases.append(phase)
            coil_directions.append(direction)
    
    coil_positions_mm = np.array(coil_positions_mm)
    n_coils = len(coil_positions_mm)
    
    # Current in each coil at each time
    coil_currents = np.zeros((n_coils, len(time_points)))
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
        
        for coil_idx in range(n_coils):
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
    ax1.set_xlim(-5, max(coil_positions) + 10)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Input Voltages and Neutral (showing floating neutral mechanism)
    ax2 = axes[0, 1]
    omega = 2 * np.pi * 50
    V_amp = 2.0
    V_offset = 2.0
    
    # Unipolar 0-4V PWM output from driver
    v_U = V_amp*np.sin(omega*time) + V_offset
    v_V = V_amp*np.sin(omega*time - 2*np.pi/3) + V_offset
    v_W = V_amp*np.sin(omega*time - 4*np.pi/3) + V_offset
    v_n = (v_U + v_V + v_W) / 3  # Floating neutral
    
    ax2.plot(time*1000, v_U, 'b-', linewidth=2, label='V_U (0-4V)')
    ax2.plot(time*1000, v_V, 'orange', linewidth=2, label='V_V (0-4V)')
    ax2.plot(time*1000, v_W, 'g-', linewidth=2, label='V_W (0-4V)')
    ax2.plot(time*1000, v_n, 'r--', linewidth=2, label='V_neutral (2V)')
    ax2.axhline(y=2, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel('Time [ms]')
    ax2.set_ylabel('Voltage [V]')
    ax2.set_title('Driver Output Voltages (Unipolar 0-4V)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.5, 4.5)
    
    # Plot 3: Phase Currents (bipolar, created by floating neutral)
    ax3 = axes[1, 0]
    R = 4.0
    i_U = (v_U - v_n) / R
    i_V = (v_V - v_n) / R
    i_W = (v_W - v_n) / R
    
    ax3.plot(time*1000, i_U, 'b-', linewidth=2, label='I_U (±0.5A)')
    ax3.plot(time*1000, i_V, 'orange', linewidth=2, label='I_V (±0.5A)')
    ax3.plot(time*1000, i_W, 'g-', linewidth=2, label='I_W (±0.5A)')
    ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax3.set_xlabel('Time [ms]')
    ax3.set_ylabel('Current [A]')
    ax3.set_title('Phase Currents (Bipolar via Floating Neutral)', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Force over time
    ax4 = axes[1, 1]
    ax4.plot(time*1000, force, 'k-', linewidth=2)
    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Time [ms]')
    ax4.set_ylabel('Force [N]')
    ax4.set_title('Resultant Force on Mover (Relative)', fontsize=12, fontweight='bold')
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
                           coil_currents, time, pole_pitch, n_blocks=3,
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
        ax.set_xlim(-2, n_blocks * 30 + 2)
        ax.set_ylim(-0.7, 0.7)
        if idx == 0:
            ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Add coil labels (repeating A-b-C-a-B-c for each block)
        coil_names = []
        for block in range(n_blocks):
            coil_names.extend(['A', 'b', 'C', 'a', 'B', 'c'])
        for pos, name in zip(coil_positions, coil_names):
            ax.text(pos, -0.6, name, ha='center', fontsize=8, fontweight='bold')
    
    plt.suptitle(f'Linear Motor: MMK (bars) interacting with Stator B-field (blue curve)\n'
                f'{len(coil_positions)} coils ({n_blocks}× AbCaBc blocks) — '
                f'Force = Σ (MMK × B) at each coil position', 
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


def main():
    print("Tubular Linear Motor Simulation (Test Setup)")
    print("=" * 50)
    
    t = np.linspace(0, 0.04, 400)  # 2 periods at 50Hz
    
    # Test setup: 3 blocks = 18 coils = 90mm total
    n_blocks = 3
    positions_mm, b_field, mmk_data, force, coil_pos, coil_curr, pole_pitch = \
        simulate_linear_motor(t, pole_pitch_mm=30.0, coil_width_mm=5.0, n_blocks=n_blocks)
    
    print(f"\nMotor Parameters (Test Setup):")
    print(f"  Number of AbCaBc blocks: {n_blocks}")
    print(f"  Total coils: {len(coil_pos)} (6 coils per block)")
    print(f"  Total mover length: {n_blocks * 30} mm")
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
                          t, pole_pitch, n_blocks, 'linear_motor_snapshots.png')
    
    print("\nKey Physics:")
    print("  - Coils distributed ALONG motor length (0, 5, 10, 15, 20, 25 mm)")
    print("  - Each coil sees LOCAL B-field from stator")
    print("  - Force = Σ (MMK × B) at each coil position")
    print("  - MMK wave travels as currents change, creating continuous force")


if __name__ == "__main__":
    main()
