import gpkit
from gpkit import Variable, VectorVariable, Model
from gpkit.tools import te_exp_minus1
from gpkit.feasibility import feasibility_model
n_stages = 2

dV_requirement = Variable("dV_requirement",4000,"m/s")
dV = VectorVariable(n_stages,"dV","m/s")

Isp = VectorVariable(n_stages,"Isp",[282,348],"s") #Value from wiki on specific impulse
theta_fuel = VectorVariable(n_stages,"theta_fuel",[0.97,0.95],"-")
z = VectorVariable(n_stages,"z","-")
m_fuel = VectorVariable(n_stages,"m_fuel","kg")
m_payload = Variable("m_payload",100,"kg")
m_zfw = VectorVariable(n_stages,"m_zfw","kg")
m_dot = VectorVariable(n_stages,"m_dot","kg/s")
v_exhaust_effective = VectorVariable(n_stages,"v_exhaust_effective","m/s")
F_thrust = VectorVariable(n_stages,"F_thrust","N")
total_mass = VectorVariable(n_stages,"total_mass","kg")
m_total = Variable("m_total","kg")

g = Variable("g",9.8,"m/s/s")

constraints = []
for stage in range(n_stages):
	constraints += [
		Isp[stage] == v_exhaust_effective[stage]/g,
		m_dot[stage] == F_thrust[stage]/(g*Isp[stage]),
		z[stage] >= (dV[stage]+g*(m_fuel[stage]/m_dot[stage]))/v_exhaust_effective[stage],
		theta_fuel[stage] >= te_exp_minus1(z[stage],5)
	]
	if stage == 0:
		constraints+=[F_thrust[stage]/g >= m_fuel[0] + m_zfw[0] + m_fuel[1] + m_zfw[1] + m_payload,
					  total_mass[stage] >= m_fuel[stage]+m_fuel[stage+1]+m_zfw[stage]+m_zfw[stage+1]+m_payload,
					  theta_fuel[stage] == m_fuel[stage]/total_mass[stage]]
	if stage == 1:
		constraints+=[F_thrust[stage]/g >= m_fuel[stage] + m_zfw[stage],
					total_mass[stage] >= m_fuel[stage]+m_zfw[stage] + m_payload,
					theta_fuel[stage] == m_fuel[stage]/total_mass[stage]]

constraints+=[
			m_total >= m_zfw[0] + m_fuel[0] + m_zfw[1] + m_fuel[1] + m_payload]

with gpkit.SignomialsEnabled():
	constraints+=[
		dV_requirement <= dV[0] + dV[1]
	]

objective = m_fuel[0] + m_fuel[1]
# objective = 1/dV[0] + 1/dV[1]
m = Model(objective,constraints)
# so2 = feasibility_model(m.gp(),"max")
sol = m.localsolve(verbosity=1)
print sol.table()
print (1/sol['cost'])
#
# m.substitutions.update({dV_requirement:('sweep', [400,800,1200])})
# a = m.localsolve(printing='false')
#
# print a.table()
