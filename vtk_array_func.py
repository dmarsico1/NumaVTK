import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import scipy.io

def vtk_array_function(f_name,nopx,nopy,nopz,nelx,nely,nelz,grid_num,num):
	
	reader = vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName(f_name)
	reader.Update()

	nodes_vtk_array= reader.GetOutput().GetPoints().GetData()
	
	numpy_nodes=vtk_to_numpy(nodes_vtk_array)

	x_points=numpy_nodes[:,0]
	y_points=numpy_nodes[:,1]
	z_points=numpy_nodes[:,2]

	theta_vtk_array = reader.GetOutput().GetPointData().GetAbstractArray("theta")

	theta_array = vtk_to_numpy(theta_vtk_array)

	rho_vtk_array = reader.GetOutput().GetPointData().GetAbstractArray("rho")

	rho_array = vtk_to_numpy(theta_vtk_array)

	vel_vtk_array = reader.GetOutput().GetPointData().GetAbstractArray("velocity")

	vel_array = vtk_to_numpy(vel_vtk_array)
	
	u_array = vel_array[:,0]
	v_array = vel_array[:,1]
	w_array = vel_array[:,2]

	ngx=nopx
	ngy=nopy
	ngz=nopz
	NGX=(ngx)*nelx
	NGY=(ngy)*nely
	NGZ=(ngz)*nelz

	xc=np.zeros((nelx*(ngx-1)))
	yc=np.zeros((NGY))
	zc=np.zeros((nelz*(ngz-1)))


	for e in range(0,nelx):
		for j in range(0,ngx-1):
			indx=e*(ngx-1)+j
			ind_vec=e*ngx*NGY*NGZ+j
			xc[indx]=x_points[ind_vec]

	for e in range(0,nelz):
		for j in range(0,ngz-1):
			indz=e*(ngz-1)+j
			ind_vec=e*(NGY)*ngx*ngz+ngx*NGY*j
			zc[indz]=z_points[ind_vec]

	
	u=np.zeros(((ngz-1)*nelz,(ngx-1)*nelx,NGY))
	v=np.zeros(((ngz-1)*nelz,(ngx-1)*nelx,NGY))
	w=np.zeros(((ngz-1)*nelz,(ngx-1)*nelx,NGY))
	rho=np.zeros(((ngz-1)*nelz,(ngx-1)*nelx,NGY))
	theta=np.zeros(((ngz-1)*nelz,(ngx-1)*nelx,NGY))


	for e in range(0,nelx):
		for i in range(0,nelz):
			for k in range(0,NGY):
				for j in range(0,ngz-1):
					for m in range(0,ngx-1):
						indx=(e)*(ngx-1)+m
						indy=k
						indz=i*(ngz-1)+j
						ind_vec=(e)*NGY*(ngx)*(NGZ)+i*(NGY)*(ngx)*(ngz)+k*ngx+(ngx)*(NGY)*j+m
						u[indz,indx,indy]=u_array[ind_vec]
						v[indz,indx,indy]=v_array[ind_vec]
						w[indz,indx,indy]=w_array[ind_vec]
						theta[indz,indx,indy]=theta_array[ind_vec]
						rho[indz,indx,indy]=rho_array[ind_vec]



	u_str='u'+str(grid_num)+str(num)
	v_str='v'+str(grid_num)+str(num)
	w_str='w'+str(grid_num)+str(num)
	theta_str='theta'+str(grid_num)+str(num)
	rho_str='rho'+str(grid_num)+str(num)
	x_str='xc'+str(grid_num)
	z_str='zc'+str(grid_num)

	scipy.io.savemat(u_str+'.mat',{u_str:u})
	scipy.io.savemat(v_str+'.mat',{v_str:v})
	scipy.io.savemat(w_str+'.mat',{w_str:w})
	scipy.io.savemat(theta_str+'.mat',{theta_str:theta})
	scipy.io.savemat(rho_str+'.mat',{rho_str:rho})
	
	scipy.io.savemat(x_str+'.mat',{x_str:xc})
	scipy.io.savemat(z_str+'.mat',{z_str:zc})





