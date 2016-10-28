"Problem - optimize a single stage solid fuel rocket"
from gpkit import Variable, Model

# Decision variable
m_final = Variable('m_final','kg')
m_propellant = Variable('m_propellant','kg')
m_parachute = Variable('m_parachute','kg')
m_structure = Variable('m_structure','kg')

w_initial = Variable('w_initial',1000,'N')
I_specific = Variable("I_specific",240,'s')
I_total = Variable('I_total','N*s')

C_d = Variable("C_d",1.1,"-")
diameter = Variable("diameter","m")
length = Variable("length","m")

length_motor = Variable("length_motor","m")
length_parachute = Variable("length_parachute","m")

volume_motor = Variable("volume_motor","m^3")
volume_parachute = Variable("volume_parachute","m^3")
density_motor = Variable("density_motor",1600,"kg/m^3")
density_parachute = Variable("density_motor",276,"kg/m^3")


g = Variable("g",9.8,"m/s^2")


# Constraint
constraints = [
			   I_total <= I_specific*m_propellant*g,
			   w_initial >= (m_propellant+m_final)*g,
			   m_propellant*g/w_initial <= 0.90]

# Objective (to minimize)
objective = w_initial/I_total

# Formulate the Model
m = Model(objective, constraints)

# Solve the Model
sol = m.solve(verbosity=1)
sol.table()
print sol(m_propellant*g/w_initial)