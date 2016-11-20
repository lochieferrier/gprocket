import gpkit
from gpkit import Variable, VectorVariable, Model
from gpkit.tools import te_exp_minus1
from gpkit.feasibility import feasibility_model
n_stages = 2

dV_requirement = Variable("dV_requirement",100,"m/s")
dV = VectorVariable(n_stages,"dV","m/s")

Isp = VectorVariable(n_stages,"Isp",[450,450],"s") #Value from wiki on specific impulse
theta_fuel = VectorVariable(n_stages,"theta_fuel",[0.9,0.9],"-")
z = VectorVariable(n_stages,"z","-")
m_fuel = VectorVariable(n_stages,"m_fuel","kg")
m_zfw = VectorVariable(n_stages,"m_zfw",[10,1],"kg")
m_dot = VectorVariable(n_stages,"m_dot","kg/s")
v_exhaust_effective = VectorVariable(n_stages,"v_exhaust_effective","m/s")
F_thrust = VectorVariable(n_stages,"F_thrust","N")

m_total = Variable("m_total","kg")

g = Variable("g",9.8,"m/s/s")

constraints = []
for stage in range(n_stages):
	constraints += [
		Isp[stage] == v_exhaust_effective[stage]/g,
		m_dot[stage] == F_thrust[stage]/(g*Isp[stage]),
		z[stage] >= (dV[stage]+g*(m_fuel[stage]/m_dot[stage]))/v_exhaust_effective[stage],
		theta_fuel[stage] == m_fuel[stage]/m_zfw[stage],
		theta_fuel[stage] >= te_exp_minus1(z[stage],5),
	]

constraints+=[
			m_total >= m_zfw[0] + m_fuel[0] + m_zfw[1] + m_fuel[1]]

with gpkit.SignomialsEnabled():
	constraints+=[
		dV_requirement <= dV[0] + dV[1]
	]
objective = m_total

m = Model(objective,constraints)
# so2 = feasibility_model(m.gp(),"max")
sol = m.localsolve(verbosity=1)
print sol.table()
