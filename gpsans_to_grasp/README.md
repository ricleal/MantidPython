# GPSANS to GRASP

Converts Mantid non Reduced Data (Detector coordinates to GRASP)

### Help
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
✔ ~/git/MantidPython/gpsans_to_grasp [mast
```

### Run

Edit ```config.cfg``` and edit the entries:
```
[Mantid]
# Mantid Path (where you have MantidPlot executable!)
path = /home/rhf/git/mantid/Build/bin

[General]
# Format of output file
#exporter = exporter.Config
exporter = exporter.Raw
#exporter = exporter.Json
```

There are several formats for the output file. The exporter ```exporter.Raw``` produces a file of the format:

```
Counters_detector=4935468.000000
Counters_monitor=29205906.000000
Counters_psd=4028583.000000
Counters_time=3600.000000
Header_Beam_Blocked_Run_Number=0
Header_Builtin_Command=scan preset time 3600
Header_Command=scan preset time 3600
Header_Comment=none
Header_Detector_Sensitivity_Run_Number=0
Header_Empty_Run_Number=0
Header_Experiment_Title=IPTS-2758 SANS study of the impact of water miscible ILs
 on the solution conformation and aggregation state of proteins
Header_Experiment_number=61
Header_ImagePath=Images/BioSANS_exp61_scan0004_0001.png
Header_Instrument=GPSANS
Header_Local_Contact=William Heller
Header_Number_of_X_Pixels=192
Header_Number_of_Y_Pixels=192
Header_Reactor_Power=85.000000
Header_Sample_CountRate=8112.751667
Header_Sample_Thickness=0.000000
Header_Scan_Number=4
Header_Scan_Title=GFP in H2O 6m
Header_Transmission=False
Header_Transmission_for_Scan=-1
Header_Users=William Heller, Hugh O'Neill, Gary Baker
Header_absolute_intensity_constant=0.000000
Header_beam_center_x_pixel=0.000000
Header_beam_center_y_pixel=0.000000
Header_beamtrap_diameter=0.000000
Header_sample_aperture_size=14.000000
Header_sample_aperture_to_flange=171.000000
Header_sample_to_flange=146.000000
Header_source_aperture_size=40.000000
Header_source_distance=9351.200000
Header_tank_internal_offset=665.400000
Header_wavelength=6.000000
Header_wavelength_spread=0.140000
Header_x_mm_per_pixel=5.152200
Header_y_mm_per_pixel=5.146200
Motor_Positions_aperture_x=-15.001240
Motor_Positions_attenuation=0.000000
Motor_Positions_attenuator_pos=-447.998853
Motor_Positions_beam_trap_size=101.000000
Motor_Positions_beam_trap_x=65.999970
Motor_Positions_coll_1=223.278484
Motor_Positions_coll_2=223.632954
Motor_Positions_coll_3=222.018441
Motor_Positions_coll_4=217.499654
Motor_Positions_coll_5=95.874878
Motor_Positions_coll_6=3.991077
Motor_Positions_coll_7=5.504332
Motor_Positions_coll_8=103.625968
Motor_Positions_detector_trans=399.999962
Motor_Positions_dlambda_rel_fwhm=0.000000
Motor_Positions_lambda=0.000000
Motor_Positions_nguides=4.000000
Motor_Positions_sample_det_dist=6.000000
Motor_Positions_sample_x=82.401410
Motor_Positions_temp=297.000000
Motor_Positions_trap_y_101mm=25.000001
Motor_Positions_trap_y_25mm=25.000001
Motor_Positions_trap_y_50mm=25.000001
Motor_Positions_trap_y_76mm=548.000022
Parameter_Positions_tsample=28.000000
beam-trap-diameter=76.2
monitor=29205906.0
number-of-guides=4
run_start=2009-12-04
run_title=GFP in H2O 6m
sample-aperture-diameter=14.0
sample-detector-distance=6000.0
sample-detector-distance-offset=665.4
sample-si-window-distance=146.0
sample-thickness=0.0
sample_detector_distance=6000.0
source-aperture-diameter=40.0
source-sample-distance=9351.2
start_time=2009-12-04
timer=3600.0
total-sample-detector-distance=6811.4
wavelength=6.0
wavelength-spread=0.14
aperture-distances=1919.1,
default-incident-monitor-spectrum=1.0
default-incident-timer-spectrum=2.0
detector-distance-offset=711.0
detector-name=detector1
number-of-monitors=2.0
number-of-x-pixels=192.0
number-of-y-pixels=192.0
x-pixel-size=5.15
y-pixel-size=5.15
attenuator_pos=456
mag_current=123
sample_rotation=789

318     98      109     103     95      119     111     117     109     105     111     99      88      118     108     87      102     109     125     125     127     104     115     107     111     137     128     90      128     113     131     98      123     122     114     118     126     89      113     107     113     129     118     127     126     134     117     117     131     109     126     131     108     128     113     131     121     140     142     106     125     127     124     121     140     122     142     124     127     135     124     113     118     108     125     119     158     159     131     129     123     135     139     131     132     131     110     130     122     148     120     137     141     132     144     135     144     135     131     137     126     146     143     145     150     143     122     118     138     138     147     124     153     153     136     131     143     140     126     152     142     130     130     142     137     135     126     141     126     120     116     120     128     103     154     115     119     119     113     139     125     114     125     99      127     139     146     124     125     128     145     112     139     119     136     120     118     120     140     108     151     128     137     142     134     116     137     102     117     124     127     108     127     149     123     146     126     135     137     121     132     113     126     140     123     112     129     109     133     121     125     328
390     123     106     111     118     99      104     101     105     117     102     95      135     110     124     123     117     102     106     107     148     116     97      106     122     104     95      116     100     107     102     101     125     108     149     106     112     132     125     123     109     113     124     124     121     129     119     123     113     117     127     126     137     133     128     106     138     117     129     125     112     120     124     108     133     123     115     132     114     111     114     131     151     113     142     115     136     91      113     122     112     95      147     105     125     113     129     118     123     95      139     112     147     123     139     132     124     129     136     136     158     122     146     134     156     122     125     128     123     113     152     129     140     141     116     122     130     134     132     118     144     117     123     122     128     116     128     120     152     118     123     93      124     107     121     106     141     115     133     120     118     96      106     114     130     123     135     115     108     109     112     101     109     102     114     85      87      106     120     104     118     98      112     129     117     109     100     100     104     100     97      101     111     109     124     119     110     113     89      94      106     121     120     120     129     103     104     122     132     116     187     224
(...)
```

Example launching the converter with a a log plot of the detector:

```
./convert_to_grasp.py -i data/data.nxs -o data/data_0001.raw -p log
```

### Additional info

If more information is needed (or need to be overwritten) in the exported file, create a file `metadata.cfg` in the current directory, with pairs of key = values.
It will be added to the exported file. Example of a `metadata.cfg`:
```
[Metadata]
# Metadata to add to the output data file
# User added. Must be where the command is called
mag_current = 123
attenuator_pos = 456
sample_rotation = 789
```
