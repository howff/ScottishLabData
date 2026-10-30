# Linux

Use postgresql in a docker container
```
docker pull postgres:18
```

To run in a private network:
```
docker network create scala
docker run --name postgres-scala --network scala -e POSTGRES_PASSWORD=pgscala -d postgres:18
docker run -it --rm --network scala -e PGPASSWORD=pgscala postgres:18 psql -h postgres-scala -U postgres -c 'CREATE DATABASE scala;'
alias pscala='docker run -it --rm --network scala -e PGPASSWORD=pgscala postgres:18 psql -h postgres-scala -U postgres scala'
```

That will make it difficult to contact from the localhost, so
to run locally:
```
docker run --name postgres-scala -p 5432:5432 -e POSTGRES_PASSWORD=pgscala -d postgres:18
PGIP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres-scala)
docker run -it --rm -e PGPASSWORD=pgscala postgres:18 psql -h $PGIP -U postgres -c 'CREATE DATABASE scala;'
alias pscala="docker run -it --rm -e PGPASSWORD=pgscala postgres:18 psql -h $PGIP -U postgres scala"
```

Then install the packages for the import script
```
pip3 install pandas sqlalchemy psycopg2-binary
```

Run the import script
```
python3 importcsv.py ExemplarTestData/DaSH.csv                DaSH
python3 importcsv.py ExemplarTestData/Demography_DaSH.csv     Demography_DaSH
python3 importcsv.py ExemplarTestData/Demography_Glasgow.csv  Demography_Glasgow
python3 importcsv.py ExemplarTestData/Demography_HIC.csv      Demography_HIC
python3 importcsv.py ExemplarTestData/Demography_Lothian.csv  Demography_Lothian
python3 importcsv.py ExemplarTestData/Glasgow.csv             Glasgow.csv
python3 importcsv.py ExemplarTestData/HIC.csv                 HIC
python3 importcsv.py ExemplarTestData/Lothian.csv             Lothian
python3 importcsv.py ExemplarTestData/Lothian_TestCode2ReadCode.csv  Lothian_TestCode2ReadCode
```

Test the import
```
pscala -c 'select * from "Glasgow" limit 3;'
```

# Run the script

Modify the scripts to:
* remove the dbo scheme (e.g. dbo.DaSH becomes DaSH)
* quote the table names (e.g. DaSH becomes "DaSH")
* comment out the SQL relating to real tables (not needed if only using example data)
* change Latin1_general_BIN into "C"
* add functions for len() charindex() and isnumeric()
* convert the auto-generated columns high and low from text into real
```
ALTER TABLE "DaSH_v2" ALTER COLUMN high TYPE real USING high::real;
ALTER TABLE "DaSH_v2" ALTER COLUMN low  TYPE real USING low::real;
```

Run script using
```
docker run -it --rm -e PGPASSWORD=pgscala -v "$(pwd)":/s postgres:18 psql -h $PGIP -U postgres scala -f "/s/a DaSH2FHIRscot.sql"
```

# Sample data

```
==> ExemplarTestData/DaSH.csv <==
"","X.1","X","prochi","age_band","date_of_test","date_of_sample","order_code","order_code_desc","test_code","test_description","read_code","result","result_extension","test_units","reference_range","category"
"2",2,2,3837,2,"2019-05-23","2021-04-13","FBC","Full Blood Count","NEUT","RBC","42P..","85","13.8","x10^9/l","0.05{0.50","biochemistry"
"3",3,3,3484,4,"2021-12-22","2015-03-10","FBC","Full Blood Count","MCH","CHCM","42bE.","0.06","5.7","fl","","biochemistry"

==> ExemplarTestData/Demography_DaSH.csv <==
PROCHI,CHI_STATUS,sex,CURRENT_GP,anon_date_of_birth,DATE_ADDRESS_CHANGED,CALCULATED_AGE,DATE_IN,DATE_OUT,HB_EXTRACT,HBSIMD5,HBSIMD10,scsimd5,SCSIMD10,AN0NPRAC,SEUR6,CURRENTRECORD,POSTCODE_DISTRICT
3001,C,F,01/04/2013 00:00,01/08/1961 00:00,06/09/1990 00:00,65,15/01/2016 00:00,,G,5,10,1,1,A83,1,1,G76
3002,,F,01/04/2011 00:00,01/02/1951 00:00,31/07/2002 00:00,41,,,G,3,,2,5,,1,1,PA5

==> ExemplarTestData/Demography_Glasgow.csv <==
PROCHI,CHI_STATUS,sex,CURRENT_GP,anon_date_of_birth,DATE_ADDRESS_CHANGED,CALCULATED_AGE,DATE_IN,DATE_OUT,HB_EXTRACT,HBSIMD5,HBSIMD10,scsimd5,SCSIMD10,AN0NPRAC,SEUR6,CURRENTRECORD,POSTCODE_DISTRICT
2001,,F,01/07/2019 00:00,01/08/1952 00:00,24/07/2001 00:00,75,,,G,5,,1,1,A1562,,1,G61
2002,,M,07/12/2015 00:00,01/08/1962 00:00,15/12/2015 00:00,52,,,C,4,3,3,9,A391,5,1,G52

==> ExemplarTestData/Demography_HIC.csv <==
PROCHI,CHI_STATUS,sex,CURRENT_GP,anon_date_of_birth,DATE_ADDRESS_CHANGED,CALCULATED_AGE,DATE_IN,DATE_OUT,HB_EXTRACT,HBSIMD5,HBSIMD10,scsimd5,SCSIMD10,AN0NPRAC,SEUR6,CURRENTRECORD,POSTCODE_DISTRICT
1,,F,01/08/1991 00:00,01/02/1978 00:00,,58,,,G,1,10,5,1,,6,1,PA18
2,C,F,30/06/2020 00:00,01/05/1952 00:00,17/05/1994 00:00,75,,,C,3,3,,10,A808,1,1,G20

==> ExemplarTestData/Demography_Lothian.csv <==
PROCHI,CHI_STATUS,sex,CURRENT_GP,anon_date_of_birth,DATE_ADDRESS_CHANGED,CALCULATED_AGE,DATE_IN,DATE_OUT,HB_EXTRACT,HBSIMD5,HBSIMD10,scsimd5,SCSIMD10,AN0NPRAC,SEUR6,CURRENTRECORD,POSTCODE_DISTRICT
1001,,F,11/09/2014 00:00,01/05/1962 00:00,13/07/2021 00:00,60,,,C,2,5,3,10,A726,1,1,PA7
1002,C,F,01/09/2014 00:00,01/11/1930 00:00,29/02/2012 00:00,82,,,G,2,6,1,1,A726,1,1,G66

==> ExemplarTestData/Glasgow.csv <==
"","X.1","X","prochi","discipline","sampledate","sampletime","reportdate","reporttime","fasting","samplename","tissuetype","clinicalcodevalue","clinicalcodedescription","clinicalcodevaluelocal","clinicalcodedescriptionlocal","arithmeticcomparator","quantityvalue","quantityunit","rangehighvalue","rangelowvalue","rangeunit","testid","sampleid"
"1",1,1,2055,"Biochemistry","16/10/2019 00:00:00","21:11:00","23/07/2021 00:00:00","09:22:00","","Blood","B","42A..","Total Bilirubin","CHL","Calcium (adjusted)","",2.46,"g/L",7.8,9,"mmol/L","63564976f1acca0a19d8504038d8e9df","6ab46bbdcd6efc2c38dfd02ea537a89e"
"3",3,3,2569,"Haematology","10/11/2017 00:00:00","10:02:00","22/08/2019 00:00:00","14:27:00","","Blood","B","44G3.","Complement C4","ALP","Albumin","",14,"mmol/L",50,-32768,"x10^9/l","e90df8cb852bb5359cd94b11a87dedd1","ce8bed330ec58ecd9b25fc63b25132b3"

==> ExemplarTestData/HIC.csv <==
"","X.2","X.1","X","prochi","clinicalcircumstancedescription","labnumber","testreportid","testidentifier","providingorganisationid","requestingpartyposition","hb_extract","datetimesampled","samplename","quantityvalue","quantityunit","arithmeticcomparator","rangehighvalue","rangelowvalue","rangeunit","interpretation","localclinicalcodevalue","localclinicalcodedescription","readcodevalue","readcodedescription","readcodescheme","testresultorder","testset_clinicalcircumstancedescription","testset_readcodescheme","testset_readcodedescription","testset_localclinicalcodedescription","testset_readcodevalue","testset_localclinicalcodevalue"
"1",1,1,1,34,"Neutrophil count","c2219574c85f401b0abbd5a87c155803","1b1f29b01cf57aeecacc4186f5b1af85","6139d72d9696b6762748825a02ffd4cd","NINEWELL","Consultant",FALSE,"30/11/2020 08:00:00","EDTA",117,"fl","",410,120,"pg","","MCHC","EO#","42N..","Mean corpusc. Hb. conc. (MCHC)","R1",3,"FBC","1.0","FBC","FBC","424..","FBC"
"2",2,2,2,420,"Monocyte count","c2d05486ae2f4fd78f81ac5f0ea5d80b","c2422c730f5b52229e3455c3a0994421","251a8959eea8069acde772823d57b3cc","PMIP","Consultant",FALSE,"01/05/2019 09:30:00","EDTA",151,"","",11,0,"%","","IMG","Mono","426..","Basophil count","R1",1,"FBC","1.0","Full blood count - FBC","FBC","424..","CS"

==> ExemplarTestData/Lothian.csv <==
"","prochi","pid","specimencollectiondate","specimencollectiontime","testitem","testitemcode","value","unit","rangemin","rangemax"
"1",1082,1327,"30/11/2020 08:00:00","16:35","Lymphocyte Count","BGGT","1.1","fL",3,120
"2",1387,1632,"01/05/2019 09:30:00","06:40","Mean cell Hb conc.","BALT","No Numeric Result","ratio",9,0.54

==> ExemplarTestData/Lothian_TestCode2ReadCode.csv <==
Test_Code	Read_Code	Test_Expansion
ABO	431..	ABO Blood Group
AKIR	451L.	Acute Kidney Injury
```
