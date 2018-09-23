from numpy import*
import matplotlib.pyplot as plt

def discretizar(I, a, T, dt, theta):
	#u'(t) = −au(t) (con t ∈ (0, T ])
	
	ciclo = int(round(T/dt)) 
	T = ciclo*dt #Se redefine el intervalo T         
	u = zeros(ciclo+1)  # array[ciclo+1]         
	t = linspace(0, T, ciclo+1)  # linespace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
	u[0] = I # condicion inicial	  

	for n in range(0, ciclo):    
		u[n+1] = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)*u[n] #Regla θ que permite unificar los tres esquemas
		
	mostrarEsquema(t, u, a, I, theta) #Muestra el array[t], y el array u[t]. Y plotea los graficos 
	
def saberEsquema(theta):
	esquema = ''	
	if(theta == 1):
		esquema = 'Forward-Euler'  
	if(theta == 2):
		esquema = 'Backward-Euler'
	if (theta == 3):
		esquema = 'Crank-Nicholson'
	return esquema

def mostrarEsquema(t, u, a, I, theta):	
	print ('OUTPUT')
	esquema = saberEsquema(theta)
	#Muestra el array[t], y el array u[t]
	for i in range(len(t)):
		print ('t['+str(i)+'] = ' + str(t[i]),' u['+str(i)+'] = ' + str(u[i])) 

	#Ploteo de la funcion exponencial exacta y de la discretizacion temporal
	real=I*exp(-a*t) #Funcion exponencial con constante I
	fig = plt.figure()
	ax = plt.scatter(t,u,color='red')
	ax2 = plt.plot(t,real, color='green')
	plt.xlabel('Tiempo t')
	plt.ylabel('u(t)')
	plt.title('Esquema: ' + esquema)
	plt.grid(True)
	plt.savefig("test.png")
	plt.show()
	
def main():
	import os
	os.system('clear')	
	print ('******************************************************************')
	print ('PRACTICA 3 - METODO DE DIFERENCIAS FINITAS \n')
	I = float(input("Ingrese la condición inicial (Variable: 'I') >> "))
	T = float(input("Ingrese el intervalo (0,T] >> "))
	a = float(input("Ingrese el valor de la constante 'a' de la funcion exponencial >> "))
	dt = float(input("Ingrese el intervalo de longitud 'dt' >> "))
	ciclo_theta = True
	while(ciclo_theta):
		theta = float(input("Ingrese el esquema deseado: \n | Forward-Euler:   θ = 0   | \n | Backward-Euler:  θ = 1   | \n | Crank-Nicholson: θ = 0.5 | \n ... >> "))	
		if(theta==0.0 or theta==1.0 or theta==0.5):
			ciclo_theta=False	
	print ('******************************************************************')
	example=discretizar(I,a,T,dt,theta)

main()

