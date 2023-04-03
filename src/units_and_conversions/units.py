from src.load_files.read_proton_neutron_masses import read_n_p_mass


class units:
    """
    Class containing the units used in the code in cgs.
    In cgs lenght is measured in cm, mass in g, time in s,
    energy in erg, pressure in dyn/cm^2. The temperature is
    measured in MeV.
    """
    def __init__(self, path):
        self.neutron_mass, self.proton_mass = read_n_p_mass(path)
        self.c = 29979245800
        self.fm = 1e-13
        self.MeV = 1.602176634e-6

class conversions:
    def __init__(self, path):
        self.units = units(path)
    
    def pressure(self, quantity):
        """
        Convert the given pressure from MeV/fm^3 to dyn/cm^2.
        """
        return quantity * self.units.MeV / self.units.fm**3
    
    def mass_density(self, quantity):
        """
        Convert the given baryon number density to mass density.
        """
        return (quantity * self.units.neutron_mass *  self.units.MeV) / \
               (self.units.fm**3 * self.units.c**2)
    
    def dpdrho(self, quantity):
        """
        Convert the given dp/drho|e from MeV to dyn * cm/ g.
        """
        return quantity * self.units.c ** 2 / self.units.neutron_mass
    
    def dpde(self, quantity, logrho):
        """
        Convert the given dp/de|rho from 1 / fm^3 to dyn * cm/ g.
        """
        return quantity * 10 ** logrho
    
    def speed_squared(self, quantity):
        """
        Convert the given speed squared from 1 to cm^2 / s^2.
        """
        return quantity * self.units.c ** 2
    
    def specific_energy(self, quantity, logrho, nb):
        """
        Convert the given specific energy from 1 to erg / g.
        """
        return quantity * (self.units.MeV * self.units.neutron_mass * nb) / \
                (self.units.fm ** 3 * 10 ** logrho)
    

    
