import gpkit
from gpkit import Variable, Model
from gpkit.tools import te_exp_minus1
from gpkit.feasibility import feasibility_model

dV_requirement = Variable("dV_requirement",100,"m/s")
dV_total = Variable("dV_total","m/s")

Isp = Variable("Isp",450,"s") #Value from wiki on specific impulse
theta_fuel = Variable("theta_fuel",0.9,"-")
z = Variable("z","-")
m_fuel = Variable("m_fuel","kg")
m_zfw = Variable("m_zfw",10,"kg")
m_total = Variable("m_total","kg")
m_dot = Variable("m_dot","kg/s")
v_exhaust_effective = Variable("v_exhaust_effective","m/s")

g = Variable("g",9.8,"m/s/s")
F_thrust = Variable("F_thrust","N")


constraints = [
	Isp == v_exhaust_effective/g,
	m_dot == F_thrust/(g*Isp),
	z >= (dV_total+g*(m_fuel/m_dot))/v_exhaust_effective,
	theta_fuel == m_fuel/m_zfw,
	theta_fuel >= te_exp_minus1(z,5),
	dV_total >= dV_requirement,
	m_total >= m_zfw + m_fuel
]
# with gpkit.SignomialsEnabled():
objective = m_total

m = Model(objective,constraints)
so2 = feasibility_model(m.gp(),"max")
sol = m.solve(verbosity=1)
print sol.table()
