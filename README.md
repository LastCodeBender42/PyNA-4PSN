# PyNA-4PSN
A PyMOL plugin for protein structure network analysis and visualization in PyMOL.

## 1) Copy and paste the following code into a terminal and return. This will clone the PyNA-4PSN repo to the local directory of the user's choice:

```bash
git clone https://github.com/LastCodeBender42/PyNA-4PSN.git
```

## 2) cd into the directory PyNA-4PSN and run execute the requirements.txt file to install the necessary the dependnecies:

```bash
pip install -r requirements.txt
```

## 3) Start the program by running:

```bash
python main_test.py
```

## 4) The following Gui will appear select "Start API" and navigate to the .cif file of interest and select "Open". In this example, we select 1yok.cif:

<img src="./data/startAPI.png" alt="Start API">

### Once the API is started, it connects with the RING server and submits the .cif file and after a few moments the protein strutcure network is retrieved. It will be a file with a .cif_ringEdges ending.

## 5) After the API has finished running, the next step is to perform the network analysis. Do this by selecting "Start Analysis" and select the .cif_ringEdges file:

<img src="./data/startAnalysis.png" alt="Start Analysis"
