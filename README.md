# IPPA-py

IPPA-py implements the IPPA in python


#### Dependency

- Python > 3.6
- pandas


## Example data
see [Pseudo data set](https://github.com/PatientPathwayAnalysis/IPPA-data/tree/master/Input)


## How to use

### Step 0. Load packages
```python
import pandas as pd
import tb
```


### Step 1. Initialise a new IPPA

**tb.IPPA** is a controller, managing the analysis
```python
ctrl = tb.IPPA('TB', tor=60, toe=60, tot=30)
```

Time-out
- **tor** Time-out of Related illness dimension
- **toe** Time-out of Evaluation dimension
- **tot** Time-out of Treatment dimension

Two records are relevant if the next came before the Time-out of the previous. 

### Step 2. Set the definition of events

This step tells the controller how to link data to clinical information.


##### Take EventReader from the controller
```python
ER = ctrl.EventReader
```

##### Define TB related information
```python
### Indicate the column of TB diagnosis (boolean)
ER.define_disease('TB_DIAG')

### Indicate the column of TB related medical procedure
ER.define_procedure('TB_PROC', {'L': list(range(0, 5)), 'H': list(range(5, 9))})

### Indicate the column of types and dosage TB drugs
ER.define_drug('TB_DRUG', 'TB_DRUG_DAY', 
                {'2nd': list(range(0, 5)), '1st': list(range(5, 8))})
```

Procedures be encoded as a string of numbers: 0 for none 
- **L** : Evaluations possibly for TB
- **H** : Evaluations probably for TB
- In the example, **L**: 0-4, **H**: 5-8
    - 11000000 equals **2L0H**
    - 00200010 equals **2L1H** 

The cut points might be different from setting to setting, depending on clinical practices.

Drugs as well

- **1st** : 1st line anti-TB drugs
- **2nd** : 2nd line anti-TB drugs, usually more aggressive and higher risk
- In the example, ****: 0-4, **H**: 5-7
    - 2010000 implies the patient is under 1st line treatment
    - 0010021 implies the patient is under 2nd line treatment


##### Map the columns of comorbidities and the name shown in the results
```python
ER.add_related_disease('CLD', 'CLD_DIAG')
ER.add_related_disease('ARD', 'RES_DIAG')
ER.add_related_disease('NTM', 'NTM_DIAG')
```


### Step 3. Input data

```python
### Set input folder
folder_i = ("directory of the input files")

### Read patient data
patients = pd.read_csv(folder_i + 'IPPA_patients.csv', index_col=0)
ctrl.input_patients(patients, p_leave='OUT_DAY')


### Read hospital data
hospitals = pd.read_csv(folder_i + 'IPPA_hospitals.csv', index_col=0)
ctrl.input_hospitals(hospitals, h_level='LEVEL')


### Read healthcare records
records = pd.read_csv(folder_i + 'IPPA_records.csv', index_col=0)
ctrl.input_records(records, 'ID', 'HOSP_ID', 'DAY')
```



### Step 4. Run the analysis

A live demo of the pathway extract can be found in [LINK](https://patientpathwayanalysis.github.io/IPPA-ext-demo/)

```python
ctrl.events2processes2episodes(read_end=3651)
ctrl.episodes2pathways()
ctrl.pathways2statistics()
ctrl.link_hospitals()
```


### Step 5. Output

The results produced from the pseudo data input can be found in [LINK](https://github.com/PatientPathwayAnalysis/IPPA-data/tree/master/output)

```python
### Set output folder
folder_i = ("directory for storing out files")

### Output to json format
ctrl.results2json(folder_o + 'pathways.json')

### Output to csv format
ctrl.statistics2csv(folder_o + 'pathways.csv')
ctrl.hospital2csv(folder_o + 'hospital.csv')
```

## Next

The output of this analysis can be 
- visualised
    - [IPPA-d3](https://github.com/PatientPathwayAnalysis/IPPA-d3) 
        - For **.json** outputs
        - Using R and ggplot2
        - For documentation
           
    - [IPPA-vis](https://github.com/PatientPathwayAnalysis/IPPA-vis)
        - For **.csv** outputs 
        - Using javascript and d3.js
        - For demonstration and presentation 

- linked to risk factors
    - using the information in "pathways.csv" and "hospital.csv"
    
    
    
## License
See [LICENSE](LICENSE.txt)
