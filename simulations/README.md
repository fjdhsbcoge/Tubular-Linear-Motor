# FEMM Simulations

This directory contains FEMM (Finite Element Method Magnetics) simulation files and results.

## Simulation Approach

To speed up simulation iteration, a **2D axisymmetric slice** approach was used:

1. **Model a 1mm axial slice** of the motor
2. **Simulate** the 2D field distribution
3. **Multiply results** by the circumference (87.976 mm) to get total force

This is valid because:
- The motor is cylindrical and uniform along its length
- End effects are negligible for multi-pole designs
- Computation time is drastically reduced vs 3D simulation

## Images

### Field Line Distribution
![Field Lines](images/femm_field_lines.png)

Shows the magnetic flux lines from the stator (magnet/steel stack in blue) interacting with the mover (green). The characteristic bulging pattern creates the sine-wave field distribution.

### Tangential Field Profile
![Field Values](images/femm_field_lines_mover.png)

The tangential magnetic flux density (B.t) along the length shows a clean sine wave:
- **Peak B-field**: ~0.02 Tesla
- **Period**: One pole pitch
- **Shape**: Near-ideal sinusoid

This sinusoidal field is what creates the "magnetic gear teeth" — smooth, continuous field variations that mesh between stator and mover.

## File Formats

FEMM uses the following file extensions:
- **.femm** - Main project file (geometry, materials, boundaries)
- **.ans** - Solution file (contains mesh and field results)
- **.lua** - Lua scripts for automation/post-processing

## Running Simulations

1. Open FEMM (https://www.femm.info/)
2. Load the .femm project file
3. Define materials and boundary conditions
4. Generate mesh and solve
5. Post-process using Lua scripts or built-in tools

## Validation

The sine-wave field profile validates the design:
- Rounded ferromagnetic discs successfully shape the field
- Field strength is sufficient for force production
- Periodicity matches the pole pitch design

This field pattern enables smooth force production with minimal cogging when combined with proper FOC control.

## Future Simulations

Planned additions:
- [ ] Full motor model with all 3 phases
- [ ] Force vs. current characterization
- [ ] Cogging torque analysis
- [ ] Eddy current losses (if using conducting materials)
