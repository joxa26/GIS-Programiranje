# Prikaz rasprostranjenosti divljih životinjskih vrsta na šumskim površinama u Srbiji
import rasterio
from rasterio.transform import from_origin
import numpy as np
import matplotlib.pyplot as plt

# Podešavanje boja podataka (šume i životinje) za prikazivanje na mapi
forest_cmap = plt.cm.Greens
animal_cmap = plt.cm.Blues

# Putanja do CLC18 raster fajla za Srbiju
clc_file_path = "C:\\CLC18_SRB\\CLC2018_V2018_20b2_SRB.tif"

# Putanja do raster fajla o životinjskim vrstama
animal_layer_path = "C:\\Users\\Marko\\OneDrive\\Desktop\\Feature exports\\SRBZivotinjskeVrsteRaster.tif"

# Definisanje kodova za šume u Corine Land Cover-u
forest_codes = [311, 312, 313]

# Otvaranje CLC18 raster fajla
with rasterio.open(clc_file_path) as clc_dataset:
    clc_data = clc_dataset.read(1)
    transform = clc_dataset.transform
    crs = clc_dataset.crs
    new_shape = clc_data.shape

# Otvaranje geotif lejera o životinjskim vrstama i risemplovanje
with rasterio.open(animal_layer_path) as animal_dataset:
    animal_data = animal_dataset.read(1, out_shape=new_shape, resampling=rasterio.enums.Resampling.nearest)
    animal_transform = from_origin(transform.xoff, transform.yoff, transform.a, transform.e)

# Kreiranje maske za šumske površine
forest_mask = np.isin(clc_data, forest_codes)

# Preklapanje podataka o životinjama na masku šumskih površina
overlayed_data = np.where(forest_mask, animal_data, np.nan)

# Dobijanje granica iz transformisanog ekstenta
bounds = rasterio.coords.BoundingBox(
    left=transform.xoff,
    bottom=transform.yoff + (transform.e * new_shape[0]),
    right=transform.xoff + (transform.a * new_shape[1]),
    top=transform.yoff
)

# Plotovanje samo šumskih površina
plt.figure(figsize=(10, 10))
plt.imshow(forest_mask, cmap=forest_cmap, extent=bounds, origin='upper')
plt.colorbar(label="Šume")
plt.title("Šumske površine")
plt.xlabel("Geografska širina")
plt.ylabel("Geografska dužina")
plt.show()


# Plotovanje životinjskih vrsta
plt.figure(figsize=(10, 10))
plt.imshow(overlayed_data, cmap=animal_cmap, extent=bounds, origin='upper')
plt.colorbar(label="Životinje")
plt.title("Rasprostranjenost divljih životinjskih vrsta u Srbiji")
plt.xlabel("Geografska širina")
plt.ylabel("Geografska dužina")
plt.show()

# Plotovanje preklopljenih podataka
plt.figure(figsize=(10, 10))

# Plotovanje šumskih površina u zelenoj boji
plt.imshow(forest_mask, cmap=forest_cmap, extent=bounds, origin='upper', alpha=0.7)

# Plotovanje podataka o životinjskim vrstama u plavoj boji
animal_plot = plt.imshow(overlayed_data, cmap=animal_cmap, extent=bounds, origin='upper')

# Dodavanje colorbar-a
forest_colorbar = plt.colorbar(mappable=animal_plot, ax=plt.gca(), orientation='vertical', label="Podaci o životinjama")

# Dodavanje legende
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=forest_cmap(0.6), markersize=10, label='Šume'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=animal_cmap(0.6), markersize=10, label='Životinje')
]
plt.legend(handles=legend_elements, loc='upper left')

plt.title("Prikaz divljih životinjskih vrsta na šumskim površinama u Srbiji")
plt.xlabel("Geografska dužina")
plt.ylabel("Geografska širina")
plt.show()
