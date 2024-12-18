print("###############################################################################")
print("Welcome!")
print("This code simulates the probability distribution of a random set of cubes.")
print("The goal is to illustrate the principle of transformation groups.")
print("The cubes have randomly set sizes based on different generating sets:")
print("\t uniform distribution of side lengths (blue)")
print("\t uniform distribution of surface areas (green)")
print("\t uniform distribution of volumes (red)")
print("The final column takes random samples of each set.")
print("###############################################################################")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Seed for reproducibility
seed = 12
rng  = np.random.default_rng(seed)

# Generate sample sets
sample_count  = 300000
length_min    = 3
length_max    = 5
side_lengths  = rng.uniform(length_min,      length_max,      sample_count)
surface_areas = rng.uniform(6*length_min**2, 6*length_max**2, sample_count)
volumes       = rng.uniform(length_min**3,   length_max**3,   sample_count)


# Calculate corresponding side lengths, areas, and volumes
lengths              = side_lengths
lengths_from_areas   = np.sqrt(surface_areas / 6)
lengths_from_volumes = np.cbrt(volumes)

areas_from_lengths   = 6 * (side_lengths ** 2)
areas                = surface_areas
areas_from_volumes   = 6 * (lengths_from_volumes ** 2)

volumes_from_lengths = side_lengths ** 3
volumes_from_areas   = (lengths_from_areas ** 3)
volumes              = volumes

# Additional random samples for new row
lengths_sample              = rng.choice(lengths,              size=int(sample_count/3))
lengths_sample_from_areas   = rng.choice(lengths_from_areas,   size=int(sample_count/3))
lengths_sample_from_volumes = rng.choice(lengths_from_volumes, size=int(sample_count/3))

areas_sample_from_lengths   = rng.choice(areas_from_lengths,   size=int(sample_count/3))
areas_sample                = rng.choice(areas,                size=int(sample_count/3))
areas_sample_from_volumes   = rng.choice(areas_from_volumes,   size=int(sample_count/3))

volumes_sample_from_lengths = rng.choice(volumes_from_lengths, size=int(sample_count/3))
volumes_sample_from_areas   = rng.choice(volumes_from_areas,   size=int(sample_count/3))
volumes_sample              = rng.choice(volumes,              size=int(sample_count/3))


# Statistical analysis
lengths_combined = np.concatenate([lengths_sample, lengths_sample_from_areas, lengths_sample_from_volumes])
areas_combined   = np.concatenate([areas_sample_from_lengths, areas_sample, areas_sample_from_volumes])
volumes_combined = np.concatenate([volumes_sample_from_lengths, volumes_sample_from_areas, volumes_sample])

lengths_avg      = np.round(np.mean(lengths_combined), 1)
areas_avg        = np.round(np.mean(areas_combined),   1) # np.round(np.mean(np.sqrt(areas_combined/6)), 3)
volumes_avg      = np.round(np.mean(volumes_combined), 1) # np.round(np.mean(np.cbrt(volumes_combined)), 3)

lengths_stdev    = np.round(np.std(lengths_combined),  1)
areas_stdev      = np.round(np.std(areas_combined),    1) # np.round(np.std(np.sqrt(areas_combined/6)), 3)
volumes_stdev    = np.round(np.std(volumes_combined),  1) # np.round(np.std(np.cbrt(volumes_combined)), 3)


# Curve comparison
def func(x):
    return 1000000 / (6 * x**(2/3))
x = np.linspace(length_min**3,    length_max**3,   100)
y = func(x)

def func2(x):
    return 900000 / (4 * (6*x)**(1/2))
x2 = np.linspace(6*length_min**2, 6*length_max**2, 100)
y2 = func2(x)

# Plotting
fig = plt.figure(figsize=(10, 6))
gs  = GridSpec(3, 4, figure=fig)


# Row 1: Side lengths
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(lengths, bins=30, color='blue', alpha=0.7)
ax1.set_title("Lengths")

ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(lengths_from_areas, bins=30, color='green', alpha=0.7)
ax2.set_title("Lengths from Areas")

ax3 = fig.add_subplot(gs[0, 2])
ax3.hist(lengths_from_volumes, bins=30, color='red', alpha=0.7)
ax3.set_title("Lengths from Volumes")

ax4 = fig.add_subplot(gs[0, 3])
ax4.hist(lengths_sample, bins=30, color='blue', alpha=0.7)
ax4.hist(lengths_sample_from_areas, bins=30, color='green', alpha=0.5)
ax4.hist(lengths_sample_from_volumes, bins=30, color='red', alpha=0.3)
ax4.set_title("Lengths from Sampling")
ax4.text(0.5, 0.1, f'{lengths_avg} ± {lengths_stdev}', fontsize=10, color='w', ha='center', va='center', transform=plt.gca().transAxes)


# Row 2: Surface areas
ax5 = fig.add_subplot(gs[1, 0])
ax5.hist(areas_from_lengths, bins=30, color='blue', alpha=0.7)
#ax5.plot(x2, y2, color='blue')
ax5.set_title("Areas from Lengths")

ax6 = fig.add_subplot(gs[1, 1])
ax6.hist(areas, bins=30, color='green', alpha=0.7)
ax6.set_title("Areas")

ax7 = fig.add_subplot(gs[1, 2])
ax7.hist(areas_from_volumes, bins=30, color='red', alpha=0.7)
ax7.set_title("Areas from Volumes")

ax8 = fig.add_subplot(gs[1, 3])
ax8.hist(areas_sample_from_lengths, bins=30, color='green', alpha=0.7, label="Sample Areas")
ax8.hist(areas_sample, bins=30, color='blue', alpha=0.5, label="Converted Lengths")
ax8.hist(areas_sample_from_volumes, bins=30, color='red', alpha=0.3, label="Converted Volumes")
ax8.set_title("Areas from Sampling")
ax8.text(0.5, 0.1, f'{areas_avg} ± {areas_stdev}', fontsize=10, color='w', ha='center', va='center', transform=plt.gca().transAxes)


# Row 3: Volumes
ax9 = fig.add_subplot(gs[2, 0])
ax9.hist(volumes_from_lengths, bins=30, color='blue', alpha=0.7)
ax9.plot(x, y, color='blue')
ax9.set_title("Volumes from Lengths")

ax10 = fig.add_subplot(gs[2, 1])
ax10.hist(volumes_from_areas, bins=30, color='green', alpha=0.7)
ax10.set_title("Volumes from Areas")

ax11 = fig.add_subplot(gs[2, 2])
ax11.hist(volumes, bins=30, color='red', alpha=0.7)
ax11.set_title("Volumes")

ax12 = fig.add_subplot(gs[2, 3])
ax12.hist(volumes_sample_from_lengths, bins=30, color='red', alpha=0.7, label="Sample Volumes")
ax12.hist(volumes_sample_from_areas, bins=30, color='blue', alpha=0.5, label="Converted Lengths")
ax12.hist(volumes_sample, bins=30, color='green', alpha=0.3, label="Converted Areas")
ax12.set_title("Volumes from Sampling")
ax12.text(0.5, 0.1, f'{volumes_avg} ± {volumes_stdev}', fontsize=10, color='w', ha='center', va='center', transform=plt.gca().transAxes)


# Adjust layout
plt.tight_layout()
plt.show()
