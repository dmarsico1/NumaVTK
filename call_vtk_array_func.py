import vtk_array_func

time_str=["0.0100","0.0050","0.0025","0.0013","0.0006"]

num_grids=5

for i in range(0,num_grids):
	grid_str=time_str[i]
	print(grid_str)
	vtk_array_func.vtk_array_function("/grad/dmarsico/numa/Test11/numa3d-IMEX/test3/sc_"+grid_str+"_set2nc_cgd_rk_P4est_0010.vtu",3,3,3,10*2**i,1,10*2**i,i+1,1)
