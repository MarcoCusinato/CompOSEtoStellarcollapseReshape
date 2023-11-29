# CompOSE to stellarcollapse table reshape
## Introduction
Many codes used to simulate core collapse supernova events use the equations of state (EOS) for nuclear matter that comes from or are tabulated in the format of [stellarcollapse](https://stellarcollapse.org/equationofstate.html). However, [CompOSE](https://compose.obspm.fr/home) provides a large database of EOSs as well as a [code](https://compose.obspm.fr/software) to generate EOS tables both in ASCII and h5 formats.
## What does it do?
This script takes a CompOSE EOS table in h5 format and reshapes it in the format of the stellarcollapse tables, always in h5. It was meant to work for *general purpose* EOSs, so I did not test for the other families.
## What it does not do?
It does not interpolate any quantity in the EOS table. If you want to interpolate, you have to do with the CompOSE code before using this script.
## Requirements
### Python requirements
This script requires the following python packages:
 - [h5py](http://www.h5py.org/)
 - [numpy](http://www.numpy.org/)

to install them, you can use pip and the provided `requirements.txt` file:
```
pip install -r requirements.txt
```
### File hard requirements
The scripts requires the following files:
 - `eoscompose.h5`: the CompOSE EOS table in h5 format, needed to read in the data
 - `eos.info.json`: the indices dictionary, needed to read in the data and to know which index corresponds to which quantity
### File soft requirements
There is one additional file that is not required, but it is needed to have a more consistent table conversion:
 - `eos.thermo`: from this file is only needed the first row, where the neutron and proton masses used to generate this particular EOS table are stored. If it is not present, the masses are set to the default values of 939.56542052 Mev and 938.2720813 Mev, respectively.
### Quantities that need to be stored in the `eoscompose.h5` file
The three independent variables temperature ($T$), baryon number density ($n_b$) and charge fraction ($Y_q$) need to be stored as  well as the following quantities:
 - *Thermodynamic quantities*
   - Pressure ($P$)
   - Entropy per baryon ($s$)
   - Shifted baryon chemical potential $\mu_b-m_n$
   - Scaled internal energy per baryon $\frac{\varepsilon}{m_n}-1$
   - Square of speed of sound $c_s^2$
   - Charge chemical potential $\mu_q$
   - Lepton chemical potential $\mu_l$
   - Epsilon (energy density)
 - *Chemical composition*
   - Proton ($p$)
   - Neutron ($n$)
   - Alpha ($\alpha$)
   - Heavy nuclei ($A>4$)
## How to use it?
Just run the `reshape_EOS.py`, it will ask you to provide the path of the folder where the files are stored and the how you wish to name the output file. The output file will be stored in the same folder as the input files. </br>
If you renamed any of the files, fear not, it will ask you to provide the new names.
## Output file
The output file contains at least:
 - The three independent variables temperature ($T$), density ($\rho$), in `logscale`, and electron fraction ($Y_e$)
 - Mass fraction of proton, neutrons and alpha particles ($X_*$)
 - Mass fraction, average mass number and average proton number of heavy nuclei ($X_A$, $\overline{A}$, $\overline{Z}$)
 - pressure and internal energy (in `logscale`), an energy shift is applied to the internal energy to make it always positive
 - entropy per baryon ($s$), square of speed of sound ($c_s^2$) and adiabatic index ($\Gamma$)
 - chemical potential of proton, neutron and electron including their rest masses ($\mu_*$)
 - $\hat{\mu} = \mu_n - \mu_p$ and $\mu_\nu =  \mu_e - \hat{\mu}$
In addition it could contain(dependin on what is stored in the `eoscompose.h5`):
 - Mass fraction of any additional particle with $A\leq 4$
 - Fractions of any subatomic particles $Y_*$
 - Derivatives of the thermodynamic quantities
 
## What to pay attention to?
### Units
*CompOSE* tables are given in natural units $k_b = c = \hbar =1$, while *stellarcollapse* tables are given in CGS units. The scripts will convert them from one to the other.
### Adiabatic index
*CompOSE* tables store the adiabatic index as
$$\Gamma =\frac{c_P}{c_V},$$
while *stellarcollapse* tables store it as
$$\Gamma = \frac{d\ln P}{d\ln \rho} \approx \frac{c_s^2\cdot \varepsilon}{P}.$$
So even if you store $\Gamma$ in the *CompOSE* table, the script will not use it and convert it instead.
### Electron fraction
*CompOSE* does not use the electron fraction as an independent variable, rather it uses the charge fraction $Y_q = Y_e + Y_\mu$, that is identical to the electron fraction if there are no muons. So, since the *stellarcollapse* standard requires the $Y_e$, at present time the script cannot convert EOSs with muons (if you have any sugestion on how to do it, let me know).
### Heavy nuclei
Some *CompOSE* tables store heavy nuclei as two different quantities (one for $2\leq A <20$ and one for $A\geq 20$), while in the *stellarcollapse* standard are stored as a single quantity with $A>4$. If we are in this case, the script will, first, transform the first quantity from the fraction of nuclei with $2\leq A <20$ to the fraction of nuclei with $4 < A <20 $, then it will aveage it with the second quantity. However, some ``smoothing'' corrections to the arrays are applied, in particular the script will set every value that is smaller than the minimum mass number that should be found in that array ($A=2$ in the first array and $A=20$ in the second) or that has a proton number lower than 1 to zero. Moreover, whereve a the fraction of heavy nuclei is negative it will be set to zero. 
## Final remarks
Please note that the scripts provided here come with absolutely no warranty and I will not guarantee that mistake have not been made during conversions. If you decided to use it anyway, please check the output file and make sure that the results are physical. If you find any mistake, please let me know and I will try to fix it.
**I do not make any claim on the EOS tables provided here, they are provided as they are, and all the rights goes to CompOSE and stellarcollapse for their standards.**

