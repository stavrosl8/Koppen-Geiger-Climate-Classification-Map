import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib as mpl
import pandas as pd
import numpy as np

plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

def KG_plot (ds, cmap, bounds, bounds_ticks, Domain, Region):

        cbar_kwargs = {"spacing": "proportional",'shrink':0.7,'pad':0.05,
               'orientation': 'vertical','label': 'Climate Classes'}

        plt.figure(figsize=(14, 8))
        
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax1 = ds.plot(cmap=cmap, vmin= bounds[0] - .5, vmax=bounds[-1] + .5,
                      cbar_kwargs=cbar_kwargs)
        
        colorbar = ax1.colorbar
        colorbar.set_ticks(bounds)
        colorbar.set_ticklabels(bounds_ticks)
        
        ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), linewidth=0.4,
                               edgecolor='black', facecolor='none', alpha=1)
        
        ax.set_extent(Domain) # set the domain E/W/S/N 
        
        ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1,
                     color='k', alpha=0, linestyle='--')
        ax.tick_params(labelsize= 30)  
        
        plt.title(Region + ' Map of the Köppen−Geiger Climate Classification',
                  y=1.05, fontweight="bold",fontsize = 18)
        plt.savefig('KG.png', dpi = 150, bbox_inches = "tight")
        plt.close()

def KG (Data, Domain, Resolution='Fine', Region='World'):

    if Resolution == 'Fine':
        
        Class_replacement = {'Af':1,'Am':2,'As':3,'Aw':4,'BWk':5,'BWh':6,'BSk':7,'BSh':8,
                'Cfa':9,'Cfb':10,'Cfc':11,'Csa':12,'Csb':13,'Csc':14,'Cwa':15,
                'Cwb':16,'Cwc':17,'Dfa':18,'Dfb':19,'Dfc':20,'Dfd':21,'Dsa':22,
                'Dsb':23,'Dsc':24,'Dsd':25,'Dwa':26,'Dwb':27,'Dwc':28,'Dwd':29,
                'EF':30,'ET':31}
        
        colors = ["#960000","#FF0000","#FF6E6E","#FFCCCC","#FFFF64","#FFCC00",
                  "#CCAA54","#CC8D14","#003200","#005000","#007800","#AAFF32",
                  "#00D700","#96FF00","#D2691E","#A9561E","#653700","#550055",
                  "#820082","#C800C8","#FF6EFF","#646464","#8C8C8C","#BEBEBE",
                  "#E6E6E6","#6E28B4","#B464FA","#C89BFA","#C8C8FF","#6496FF",
                  "#64FFFF"]
        
        bounds = np.arange(1,32,1)
        
        Data['Cls_number'] = Data['Cls'].replace(Class_replacement)
        
        lat = Data['Lat'].to_numpy() ; lon = Data['Lon'].to_numpy()
        variable = Data['Cls_number'].to_numpy()

        arrays = [lat, lon] ; tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples, names=['Lat', 'Lon'])

        df_merged = pd.DataFrame(data = variable, columns= ["Cls"], index = index)

        ds = df_merged['Cls'].to_xarray()
        
        cmap = mpl.colors.ListedColormap(colors)
        
        bounds_ticks = np.array(list((Class_replacement.keys())))
        
        KG_plot(ds, cmap, bounds, bounds_ticks, Domain, Region)
    
    else:
        
        Class_replacement = {'Af':1,'Am':1,'As':1,'Aw':1,'BWk':2,'BWh':2,'BSk':2,'BSh':2,
                'Cfa':3,'Cfb':3,'Cfc':3,'Csa':3,'Csb':3,'Csc':3,'Cwa':3,
                'Cwb':3,'Cwc':3,'Dfa':4,'Dfb':4,'Dfc':4,'Dfd':4,'Dsa':4,
                'Dsb':4,'Dsc':4,'Dsd':4,'Dwa':4,'Dwb':4,'Dwc':4,'Dwd':4,
                'EF':5,'ET':5}
        
        colors = ['g', 'gold', 'r', 'dimgray','dodgerblue']
        
        bounds = np.arange(1,6,1)

        cmap = mpl.colors.ListedColormap(colors)
        bounds_ticks = ['A','B','C','D','E']
        
        Data['Cls_number'] = Data['Cls'].replace(Class_replacement)
        
        lat = Data['Lat'].to_numpy() ; lon = Data['Lon'].to_numpy()
        variable = Data['Cls_number'].to_numpy()

        arrays = [lat, lon] ; tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples, names=['Lat', 'Lon'])

        df_merged = pd.DataFrame(data=variable, columns=["Cls"], index=index)

        ds = df_merged['Cls'].to_xarray()
        
        KG_plot(ds, cmap, bounds, bounds_ticks, Domain, Region)
        
df = pd.read_csv('Koeppen-Geiger-ASCII.txt', delim_whitespace=True) # read the climate classification classes based on Koeppen-Geiger at 0.5 spatial resolution
append = {"Lat":83.76, "Lon":-28.76, "Cls":"Dsd"} # in ASCII file is missing the Dsd climate class
df = df.append(append, ignore_index=True)

fname = '../gadm36_0.shp' # Set the directory of shape file
adm1_shapes = list(shpreader.Reader(fname).geometries())

domain = [-180, 180, -90, 90] # Domain for all the world
#domain = [-14, 53, 30, 72] # Domain for Europe

KG(df, domain, Resolution='Fine', Region='Europe')
