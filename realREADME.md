# DOSYFACE

DOSYFACE is a Python-based interface for evaluating DOSY (Diffusion Ordered Spectroscopy) NMR experiments using the Stejskal–Tanner equation.  
The software was developed as a student project with the aim of simplifying diffusion coefficient evaluation for users without extensive scripting experience.

The project focuses on importing processed NMR integral datasets, normalizing signal intensities, generating diffusion fits, and calculating diffusion coefficients through a graphical interface.

---

## Project Background

This software was created during a university project with no prior professional software engineering background.  
While the software is not fully completed and several features remain experimental or unfinished, the project served as a major learning experience in:

- Python development
- GUI programming
- Scientific data processing
- Automation workflows
- Git/GitHub version control
- Numerical fitting and data analysis

More than **50–60 hours** were invested into development across approximately **15 software versions**.

The repository intentionally includes multiple historical versions so future contributors can understand the development process and ideas behind the project.

---

## Purpose

Evaluating DOSY-NMR experiments typically requires script-based processing of multiple datasets.  
DOSYFACE was designed to make this process more accessible through a GUI-based workflow.

Main goals included:

- Faster evaluation of diffusion datasets
- Easier normalization of NMR integrals
- Simplified parameter handling
- Automated diffusion coefficient fitting
- Support for different isotopes (`1H`, `19F`)
- Potential future support for global fitting and graphical fit analysis

---

# Mathematical Background

The software uses the **Stejskal–Tanner equation** to determine diffusion coefficients from diffusion-weighted NMR experiments.

Relevant parameters include:

| Parameter | Meaning |
|---|---|
| `gpz6` | Gradient strength |
| `p30` | Gradient length |
| `D20` | Diffusion time |
| `1H` | Proton NMR |
| `19F` | Fluorine NMR |

The fitting process evaluates signal attenuation caused by molecular diffusion during the NMR experiment.

---

# Features

## Implemented Features

### Data Import
- Import processed integral datasets
- Parse metadata from TopSpin/Bruker output files
- Extract gradient and isotope information

### Integral Normalization
- Selection of integral regions
- Automatic normalization using the largest signal intensity

### Diffusion Fit Generation
- Calculation of diffusion coefficients
- Support for:
  - `gpz6-1H`
  - `gpz6-19F`
  - `p30-1H`
  - `p30-19F`

### Increment Calculation
- Automatic increment generation from percentage ranges
- Manual increment input support

### Variable Conversion
- Automatic unit conversion (`µs`, `ms`, `s`)

---

# Current Limitations

The project is intentionally published in an unfinished state.  
Several planned features were not completed successfully.

## Known Issues

### Global Fit
Global fitting of multiple datasets was not successfully implemented.

### Graphical Fit Visualization
Graphical fit analysis and residual visualization are incomplete.

### Standard Deviation
Standard deviation/error estimation for fitted diffusion coefficients is currently not implemented.

### Converter Window
The converter functionality does not work fully as intended and requires manual input workarounds.

---

# Requirements

The following Python package versions were used during development:

```txt
cmcrameri==1.9
contourpy==1.3.3
cycler==0.12.1
fonttools==4.59.1
kiwisolver==1.4.9
matplotlib==3.10.5
mpmath==1.3.0
numpy==2.2.6
packaging==25.0
pandas==2.3.1
pillow==11.3.0
pip==25.1.1
pyparsing==3.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
scipy==1.16.1
six==1.17.0
sympy==1.14.0
tzdata==2025.2
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your-repository>/DOSYFACE.git
cd DOSYFACE
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate environment:

### Windows
```bash
.venv\Scripts\activate
```

### Linux/macOS
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

# Usage Workflow

## 1. Import Dataset
- Browse for processed DOSY text files
- Import metadata and integral data

## 2. Choose Integral Region
- Open normalization window
- Select desired integral region
- Normalize intensities

## 3. Configure Variables
Set:
- Diffusion time (`D20`)
- Fixed variables (`gpz6` or `p30`)
- Increment settings

## 4. Generate Fit
- Press `Generate Fit`
- Software calculates diffusion coefficient

---

# Educational Value

Although the project did not achieve all original goals, it demonstrates:

- Scientific software prototyping
- GUI-based scientific workflows
- Numerical fitting pipelines
- Experimental automation concepts
- Git/GitHub workflow management
- Python-based scientific computing

The project was primarily a learning experience and significantly improved the developer’s Python and automation skills.

---

# Contribution

This repository is published openly because the project still has potential for improvement.

Possible future improvements:

- Complete graphical fit visualization
- Residual analysis
- Standard deviation/error propagation
- Stable global fitting support
- Improved GUI design
- Better code modularization
- Automatic dataset handling
- Improved unit conversion logic
- Documentation cleanup

If you are interested in scientific Python development, DOSY-NMR analysis, or GUI automation tools, feel free to improve and expand the project.

---

# Disclaimer

This software is an experimental academic student project and should not currently be considered validated scientific production software.

Fit quality and diffusion coefficients strongly depend on correct input parameters and preprocessing.

---

# Acknowledgements

- Bruker TopSpin ecosystem
- Python scientific stack
- Open-source scientific computing community
- GitHub version control ecosystem

---

# Repository Notes

The repository may contain:
- Multiple historical versions
- Experimental branches
- Legacy code fragments
- Incomplete implementations

These are intentionally preserved to document the project evolution and development process.

---

# Author Note

> “I learned an incredible amount throughout the entirety of the project and will definitely continue using Python in my scientific career.”
