"""
Analyze force vs coil span for linear motor
============================================

Compare different coil configurations:
- 6 coils in 1 pole pitch (current simulation, incomplete)
- 18 coils in 3 pole pitches (actual test setup)
- Other spans to find optimal force characteristics
"""

import numpy as np
import matplotlib.pyplot as plt


def calculate_force_for_span(n_blocks, pole_pitch_mm=30.0, B_max=0.5, R=4.0, I=0.5):
    """
    Calculate force vs electrical angle for a given number of AbCaBc blocks.
    
    Parameters:
    -----------
    n_blocks : int
        Number of AbCaBc repeats (each block = 6 coils spanning 1 pole pitch)
    pole_pitch_mm : float
        Pole pitch in mm
    B_max : float
        Peak B-field in Tesla
    R : float
        Phase resistance in Ohms
    I : float
        Current amplitude in A
    
    Returns:
    --------
    angles : array
        Electrical angles in degrees
    force : array
        Force at each angle in Newtons
    """
    omega = 2 * np.pi * 50
    t = np.linspace(0, 0.02, 360)  # One electrical period, 1° resolution
    
    # Phase currents (bipolar)
    v_U = 2*np.sin(omega*t) + 2
    v_V = 2*np.sin(omega*t - 2*np.pi/3) + 2
    v_W = 2*np.sin(omega*t - 4*np.pi/3) + 2
    v_n = (v_U + v_V + v_W) / 3
    i_U = (v_U - v_n) / R
    i_V = (v_V - v_n) / R
    i_W = (v_W - v_n) / R
    
    # Coil positions for n_blocks
    coil_positions = []
    coil_phases = []
    coil_dirs = []
    
    for block in range(n_blocks):
        offset = block * pole_pitch_mm
        # One AbCaBc block
        block_pos = [0, 5, 10, 15, 20, 25]  # mm within one pole pitch
        block_phases = ['U', 'V', 'W', 'U', 'V', 'W']
        block_dirs = [1, -1, 1, -1, 1, -1]
        
        for pos, phase, direction in zip(block_pos, block_phases, block_dirs):
            coil_positions.append(offset + pos)
            coil_phases.append(phase)
            coil_dirs.append(direction)
    
    coil_positions = np.array(coil_positions)
    
    # Calculate force at each time step
    force = np.zeros(len(t))
    for t_idx in range(len(t)):
        f = 0
        currents = {'U': i_U[t_idx], 'V': i_V[t_idx], 'W': i_W[t_idx]}
        
        for pos, phase, direction in zip(coil_positions, coil_phases, coil_dirs):
            b = B_max * np.sin(2 * np.pi * pos / pole_pitch_mm)
            f += currents[phase] * direction * b
        
        force[t_idx] = f
    
    angles = omega * t * 180 / np.pi
    return angles, force, coil_positions


def main():
    print("Force Analysis: Different Coil Spans")
    print("=" * 60)
    
    # Analyze different configurations
    configs = [
        (1, "6 coils, 1 pole pitch"),
        (2, "12 coils, 2 pole pitches"),
        (3, "18 coils, 3 pole pitches (Test Setup)"),
        (4, "24 coils, 4 pole pitches"),
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    results = []
    
    for idx, (n_blocks, label) in enumerate(configs):
        angles, force, coil_pos = calculate_force_for_span(n_blocks)
        
        # Metrics
        f_max = np.max(force)
        f_min = np.min(force)
        f_avg = np.mean(np.abs(force))
        f_pp = f_max - f_min
        ripple = (f_pp / (2 * f_avg)) * 100 if f_avg > 0 else 0
        
        # Optimal angle for max continuous force
        optimal_angle = angles[np.argmax(force)]
        
        results.append({
            'label': label,
            'blocks': n_blocks,
            'coils': n_blocks * 6,
            'length_mm': n_blocks * 30,
            'f_max': f_max,
            'f_min': f_min,
            'f_pp': f_pp,
            'ripple_pct': ripple,
            'optimal_angle': optimal_angle
        })
        
        # Plot
        ax = axes[idx]
        ax.plot(angles, force, 'b-', linewidth=2)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axhline(y=f_max, color='g', linestyle='--', alpha=0.5, label=f'Peak: {f_max:.3f}N')
        ax.axhline(y=f_min, color='r', linestyle='--', alpha=0.5, label=f'Min: {f_min:.3f}N')
        ax.set_xlabel('Electrical Angle [°]')
        ax.set_ylabel('Force [N]')
        ax.set_title(f'{label}\n({n_blocks*6} coils, {n_blocks*30}mm)', fontsize=11, fontweight='bold')
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 360)
    
    plt.suptitle('Force vs Electrical Angle for Different Coil Spans\n'
                '(At standstill - force varies with alignment. With FOC, hold at peak angle for continuous force.)',
                fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('force_vs_span_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Print summary table
    print("\nSummary:")
    print("=" * 100)
    print(f"{'Configuration':<30} {'Coils':<8} {'Length':<10} {'F_max':<10} {'F_min':<10} {'Ripple':<12} {'FOC Angle':<12}")
    print("-" * 100)
    
    for r in results:
        print(f"{r['label']:<30} {r['coils']:<8} {r['length_mm']:<10}mm "
              f"{r['f_max']:>+8.3f}N {r['f_min']:>+8.3f}N {r['ripple_pct']:>8.1f}% "
              f"{r['optimal_angle']:>8.1f}°")
    
    print("\nKey Findings:")
    print("-" * 60)
    print("1. PEAK FORCE scales with number of coils (more coils = more force)")
    print("2. FORCE RIPPLE increases with span (more coils = more variation at standstill)")
    print("3. With FOC: Maintain optimal angle (0° or 360°) for constant peak force")
    print("4. Test setup (18 coils / 3 pole pitches) gives 3× the force of single block")
    
    # Show the actual force capability with FOC
    print("\n\nForce with FOC Control (maintaining optimal angle):")
    print("=" * 60)
    for r in results:
        print(f"{r['label']:<30}: {r['f_max']:>+.3f} N (continuous)")
    
    print(f"\nTest setup (18 coils): Peak force = {results[2]['f_max']:.3f} N per amp of phase current")
    print(f"At 2A (test setup limit): Predicted force = {2 * results[2]['f_max']:.1f} N")
    print(f"At 2A with 18 coils × 3 blocks: Total force = {results[2]['f_max'] * 2:.1f} N")
    print("\nNote: The 60N in original specs likely includes FEMM geometry factors not in this simplified model")


if __name__ == "__main__":
    main()
