# GPSANS to GRASP

## Help:
```
$ ./convert_to_grasp.py -h
usage: convert_to_grasp.py [-h] -i INFILE -o OUTFILE [-p {linear,log}]

Convert Mantid NeXus corrected to Grasp.

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Mantid Corrected Nexus file to read the data
  -o OUTFILE, --outfile OUTFILE
                        Output file (data from the nexus file + metadata from
                        the raw file)
  -p {linear,log}, --plot {linear,log}
                        Ploting options

```

## Use:

1. Create a metadata.cfg in the folder that you will run the script if any additional metadata is needed.
See metadata.cfg ffor format

2. Configure the export format and mantid plot path in the config.cfg.
Several exporters are available in the file exporter.cfg

3. Launch as:

```
./convert_to_grasp.py -i <file exported from mantid> -o <file to input in grasp>
```
